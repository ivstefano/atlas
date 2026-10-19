// Atlas command center. One fetch (/api/cc) renders everything; approvals post to the queue API on this port.
// Nothing here sends on its own: every approve is a click plus a confirm.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const ic = (id, cls = 'ic') => `<svg class="${cls}" aria-hidden="true"><use href="/static/icons.svg#${id}"/></svg>`;
  const H = { 'Content-Type': 'application/json', 'X-Approvals': '1' };
  let D = null, week = 0, show = localStorage.getItem('atlas.show') || 'client', drawer = null, timer = null;

  const KIND = { slack_post: 'Slack post', slack_thread_reply: 'Thread reply', gmail_draft: 'Gmail draft', email_draft: 'Email',
    status_entry: 'STATUS entry', note: 'Note', form: 'Form', calendar_event: 'Calendar' };
  const GO = { slack_post: 'Post to Slack', slack_thread_reply: 'Reply in thread', gmail_draft: 'Create Gmail draft', status_entry: 'Write STATUS' };
  const ASK = { slack_post: 'Post this to Slack now, as you?', slack_thread_reply: 'Post this thread reply now, as you?',
    gmail_draft: 'Create a Gmail draft? Nothing is sent.', status_entry: 'Write this into STATUS and commit it?' };

  // ------------------------------------------------------------ time helpers
  const T = iso => new Date(iso);
  const hm = iso => iso ? T(iso).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : '';
  const dayName = d => T(d + 'T12:00:00').toLocaleDateString('en-GB', { weekday: 'short' });
  const dayNum = d => T(d + 'T12:00:00').getDate();
  const longDay = d => T(d + 'T12:00:00').toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
  function rel(iso) {
    const m = Math.round((T(iso) - Date.now()) / 60000);
    if (m <= 0) return '';
    if (m < 60) return `in ${m} min`;
    const h = Math.floor(m / 60), r = m % 60;
    return `in ${h} h${r ? ' ' + r + ' min' : ''}`;
  }
  function late(due) {
    const d = Math.round((T(D.today + 'T12:00:00') - T(due + 'T12:00:00')) / 864e5);
    return d > 0 ? `${d}d late` : 'today';
  }
  const ago = iso => { if (!iso) return 'never'; const m = Math.round((Date.now() - T(iso)) / 60000); return m < 1 ? 'just now' : m < 60 ? `${m} min ago` : hm(iso); };

  function toast(msg) { const t = $('#toast'); t.textContent = msg; t.hidden = false; clearTimeout(t._h); t._h = setTimeout(() => t.hidden = true, 3800); }

  // ------------------------------------------------------------ data
  async function load() {
    try {
      const r = await fetch('/api/cc?week=' + week);
      D = await r.json();
    } catch (e) { $('#banner').innerHTML = `<p class="banner">Server not reachable. Retrying.</p>`; return; }
    render();
    clearTimeout(timer);
    timer = setTimeout(load, D.crm.running ? 10000 : 60000);
  }

  const allRows = () => D.week.days.flatMap(d => d.events);
  const rowByKey = k => allRows().find(r => r.key === k);
  const draftsFor = eng => D.drafts.filter(i => i.engagement === eng);
  const isNow = r => T(r.start) <= Date.now() && Date.now() < T(r.end);
  const isPast = r => T(r.end) <= Date.now();

  // ------------------------------------------------------------ render
  function render() {
    $('#today-label').textContent = longDay(D.today);
    const n = D.drafts.length;
    $('#nav-n').hidden = !n; $('#nav-n').textContent = n;
    renderAsof(); renderFresh(); renderStrip(); renderWeek(); renderTime();
    $('#banner').innerHTML = D.cal.error ? `<p class="banner">${esc(D.cal.error)}. Showing the copy from ${esc(hm(D.cal.at) || 'never')}.</p>` : '';
    if (drawer && !editing()) openDrawer(drawer, true);
  }

  function renderAsof() {
    const c = D.crm, run = c.running;
    const at = c.hubspot.as_of || c.asana.as_of;
    const err = c.hubspot.error || c.asana.error;
    $('#asof').innerHTML = run ? 'CRM refreshing&hellip;' :
      `CRM as of <b class="num">${at ? hm(at) : 'never'}</b>${err ? `<br><span class="err">${esc(err.slice(0, 60))}</span>` : ''}`;
    const b = $('#refresh'); b.classList.toggle('spin', run); b.disabled = run;
  }

  function renderFresh() {
    const c = D.crm;
    $('#fresh').innerHTML = `Calendar <b>${esc(hm(D.cal.at) || '-')}</b><br>HubSpot <b>${esc(hm(c.hubspot.as_of) || '-')}</b>${c.hubspot.error ? ' <span class="bad">!</span>' : ''}`
      + ` &middot; Asana <b>${esc(hm(c.asana.as_of) || '-')}</b>${c.asana.error ? ' <span class="bad">!</span>' : ''}`
      + `<br>Spend today <b>$${D.spend.toFixed(2)}</b> of $${D.caps.soft.toFixed(2)}`;
  }

  function briefChip(b) {
    if (!b) return '';
    if (b.state === 'ready') return `<span class="chip ready">${ic('ai-icon-check-circle')}Brief</span>`;
    if (b.state === 'planned') return `<span class="chip planned">Brief ${esc(hm(b.at))}</span>`;
    if (b.state === 'none') return `<span class="chip out">No brief</span>`;
    return `<span class="chip warn">Brief ${esc(b.state)}</span>`;
  }
  function owedCount(r) {
    const f = r.followups; if (!f) return 0;
    return f.actions.filter(a => a.ours).length;
  }
  function dealOf(r) {
    const e = r.engagement && D.engagements[r.engagement];
    return (e && e.deals[0]) || (r.deals && r.deals[0]) || null;
  }

  function renderStrip() {
    const S = D.today_strip;
    const hero = (S.current && S.current.client ? S.current : null) || S.next_client || S.current || S.next;
    let a;
    if (hero) {
      const now = isNow(hero), e = hero.engagement && D.engagements[hero.engagement];
      const owed = owedCount(hero), dr = hero.engagement ? draftsFor(hero.engagement).length : 0, deal = dealOf(hero);
      const after = [S.current, S.next].filter(x => x && x.key !== hero.key)[0];
      a = `<div class="tile">
        <div class="lu">${now ? 'Now' : 'Next'}${hero.client ? '' : ' <span class="chip out">internal</span>'}</div>
        <h3 class="nowt" data-open="${esc(hero.key)}">${esc(hero.title)}</h3>
        <div class="when"><span class="num">${hm(hero.start)}-${hm(hero.end)}</span>${now ? `<span class="soon">ends ${hm(hero.end)}</span>` : `<span class="soon">${rel(hero.start)}</span>`}
          ${hero.eng_label ? `<span class="chip name">${esc(hero.eng_label)}</span>` : ''}${briefChip(hero.brief)}</div>
        ${hero.client ? `<div class="signals"><span><b>${owed}</b>we owe</span><span><b>${dr}</b>drafts</span>${deal ? `<span>${esc(deal.stage)}</span>` : ''}${e && e.status && e.status.blocked ? `<span title="${esc(e.status.blocked)}">Blocked: ${esc(e.status.blocked.slice(0, 70))}</span>` : ''}</div>` : ''}
        <div class="acts">
          ${hero.link ? `<a class="btn primary sm" href="${esc(hero.link)}" target="_blank">${ic('ai-icon-launch')}Join</a>` : ''}
          ${hero.brief && hero.brief.url ? `<a class="btn sm" href="${esc(hero.brief.url)}" target="_blank">Brief</a>` : ''}
          ${hero.live ? `<a class="btn sm" href="/live/${encodeURIComponent(hero.key)}" target="_blank">Live</a>` : ''}
          ${hero.client ? `<button class="btn sm" data-open="${esc(hero.key)}">Details</button>` : ''}
          ${after ? `<span class="muted" style="margin-left:auto;font-size:12px;align-self:center">Then ${hm(after.start)} ${esc(after.title.slice(0, 40))}</span>` : ''}
        </div></div>`;
    } else {
      const first = allRows().find(r => r.client && T(r.start) > Date.now());
      const day = first ? first.start.slice(0, 10) : '';
      const list = first ? allRows().filter(r => r.client && r.start.slice(0, 10) === day) : [];
      a = `<div class="tile"><div class="lu">Done for today${first ? ` <span class="chip out">next: ${esc(longDay(day))}</span>` : ''}</div>
        ${list.length ? `<ul class="duel">${list.map(r => `<li><span class="eng num">${hm(r.start)}</span><span class="what"><a href="#m=${encodeURIComponent(r.key)}">${esc(r.title)}</a>
          ${r.eng_label ? `<span class="own"> ${esc(r.eng_label)}</span>` : ''}</span>${briefChip(r.brief)}</li>`).join('')}</ul>` : '<p class="empty">No client calls left this week.</p>'}</div>`;
    }
    const due = S.due, mine = due.filter(x => x.ivo), others = due.length - mine.length;
    const list = (mine.length ? mine : due).slice(0, 5);
    const b = `<div class="tile"><div class="lu">Due today and overdue <span class="num">${due.length}</span></div>
      ${list.length ? `<ul class="duel">${list.map(x => `<li><span class="eng" title="${esc(x.eng_label)}">${esc(x.eng_label || x.src)}</span>
        <span class="what" title="${esc(x.what)}">${x.url ? `<a href="${esc(x.url)}" target="_blank">${esc(x.what)}</a>` : x.eng ? `<a href="#e=${esc(x.eng)}">${esc(x.what)}</a>` : esc(x.what)}</span>
        <span class="chip ${x.due === D.today ? 'warn' : 'late'}">${late(x.due)}</span></li>`).join('')}</ul>` : '<p class="empty">Nothing dated today. Undated next actions are on each meeting card.</p>'}
      <div class="muted" style="font-size:12px;margin-top:auto">${mine.length > 5 ? `${mine.length - 5} more of yours. ` : ''}${others ? `${others} owned by others.` : ''} From STATUS, ARTEFACTS, Asana.</div></div>`;
    const by = {};
    D.drafts.forEach(i => { by[i.engagement] = (by[i.engagement] || 0) + 1; });
    const top = Object.entries(by).sort((x, y) => y[1] - x[1]);
    const c = `<div class="tile"><div class="lu">Drafts waiting</div>
      <div class="big">${D.drafts.length}<small>${D.undoable.length ? D.undoable.length + ' auto-written, undo open' : 'nothing sends without a click'}</small></div>
      <ul class="byeng">${top.slice(0, 4).map(([k, v]) => `<li><span>${esc(D.engagements[k] ? D.engagements[k].label : k)}</span><span class="num">${v}</span></li>`).join('')}</ul>
      <div class="acts"><a class="btn sm ${D.drafts.length ? 'primary' : ''}" href="#drafts">Review drafts</a></div></div>`;
    $('#strip').innerHTML = a + b + c;
  }

  function mcard(r) {
    const owed = owedCount(r), dr = r.engagement ? draftsFor(r.engagement).length : 0, deal = dealOf(r);
    const cls = ['mcard', isNow(r) ? 'now' : '', isPast(r) ? 'done' : '', drawer && drawer.key === r.key ? 'sel' : ''].join(' ');
    return `<button type="button" class="${cls}" data-open="${esc(r.key)}">
      <span class="tm"><span class="num">${hm(r.start)}-${hm(r.end)}</span>${isNow(r) ? '<span class="live">NOW</span>' : ''}</span>
      <span class="tt">${esc(r.title)}</span>
      ${r.eng_label ? `<span class="en">${esc(r.eng_label)}</span>` : `<span class="en un">No engagement match${r.external[0] ? ', ' + esc(r.external[0].split('@').pop()) : ''}</span>`}
      <span class="chips">${briefChip(r.brief)}${owed ? `<span class="chip">${owed} owed</span>` : ''}${dr ? `<span class="chip warn">${dr} draft${dr > 1 ? 's' : ''}</span>` : ''}</span>
      ${deal ? `<span class="stage" title="${esc(deal.name)}">${esc(deal.stage)}</span>` : ''}
    </button>`;
  }

  function renderWeek() {
    const days = D.week.days;
    const wk = D.week.offset === 0 ? 'This week' : D.week.offset === 1 ? 'Next week' : D.week.offset === -1 ? 'Last week' : `Week of ${longDay(D.week.monday)}`;
    $('#week-title').textContent = wk;
    const nClient = allRows().filter(r => r.client).length;
    $('#week-count').textContent = `${nClient} client calls`;
    document.querySelectorAll('.seg [data-show]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.show === show)));
    $('#wk-now').hidden = D.week.offset === 0;
    $('#weekgrid').innerHTML = days.map(d => {
      const ev = d.events, cl = ev.filter(r => r.client), inn = ev.filter(r => !r.client);
      const today = d.date === D.today, past = d.date < D.today;
      const items = show === 'all' ? ev.map(r => r.client ? mcard(r) : irow(r)).join('') :
        cl.map(mcard).join('') + (inn.length ? `<button type="button" class="linkish more-int" data-show-all>${inn.length} internal</button>` : '');
      return `<div class="day ${today ? 'today' : ''} ${past ? 'past' : ''}">
        <div class="dayh"><span class="dn">${dayName(d.date)}</span><span class="dd num">${dayNum(d.date)}</span><span class="dc">${cl.length ? cl.length + ' client' : ''}</span></div>
        ${items || '<div class="noev">No meetings</div>'}</div>`;
    }).join('');
  }
  const irow = r => `<div class="irow ${isPast(r) ? 'past' : ''}" title="${esc(r.title)}"><span class="num">${hm(r.start)}</span><span>${esc(r.title)}</span></div>`;

  function renderTime() {
    const t = D.time_cost, el = $('#timecost');
    if (!t || !(t.items || []).length) { el.hidden = true; return; }
    const max = Math.max(...t.items.map(x => +x.hours || 0), 1);
    el.hidden = false;
    el.innerHTML = `<div class="sec-head"><h2>Time</h2><span class="count">${esc(t.week || '')}</span></div>
      <div class="panel tcard"><div><div class="big">${esc((+t.total_h || t.items.reduce((s, x) => s + (+x.hours || 0), 0)).toFixed(1))}<small>h attention</small></div>
      ${t.note ? `<p class="muted" style="font-size:12px">${esc(t.note)}</p>` : ''}</div>
      <div class="bars">${t.items.slice(0, 8).map(x => `<div class="bar"><span>${esc(x.label)}</span><span class="tr"><i style="width:${(100 * (+x.hours || 0) / max).toFixed(0)}%"></i></span><span class="h num">${(+x.hours || 0).toFixed(1)}h</span></div>`).join('')}</div></div>`;
  }

  // ------------------------------------------------------------ drawer
  const editing = () => !!document.querySelector('#drawer textarea[data-dirty="1"], #drawer textarea:focus');

  function openDrawer(what, keep) {
    drawer = what;
    const dh = $('#dhead'), db = $('#dbody');
    const top = keep ? db.scrollTop : 0;
    if (what.type === 'drafts') drawDrafts(dh, db);
    else if (what.type === 'm') { const r = rowByKey(what.key); if (!r) return closeDrawer(); drawMeeting(dh, db, r); }
    else if (what.type === 'e') drawEngagement(dh, db, what.key);
    $('#drawer').classList.add('open'); $('#drawer').setAttribute('aria-hidden', 'false'); $('#scrim').hidden = false;
    db.scrollTop = top;
    document.querySelectorAll('.mcard').forEach(c => c.classList.toggle('sel', what.type === 'm' && c.dataset.open === what.key));
  }
  function closeDrawer() {
    drawer = null;
    $('#drawer').classList.remove('open'); $('#drawer').setAttribute('aria-hidden', 'true'); $('#scrim').hidden = true;
    document.querySelectorAll('.mcard.sel').forEach(c => c.classList.remove('sel'));
    if (location.hash.match(/^#(drafts|m=|e=)/)) history.replaceState(null, '', location.pathname);
  }

  const head = (bracket, title, sub, acts) => `<div class="row1">${bracket ? `<span class="bracket">${esc(bracket)}</span>` : ''}
    <button class="icon-btn x" data-close title="Close (Esc)">${ic('ai-icon-cross')}</button></div>
    <h2>${esc(title)}</h2>${sub ? `<div class="when">${sub}</div>` : ''}${acts ? `<div class="acts">${acts}</div>` : ''}`;

  function drawMeeting(dh, db, r) {
    const e = r.engagement ? D.engagements[r.engagement] : null;
    dh.innerHTML = head(r.eng_label || 'Unmatched', r.title,
      `<span class="num">${longDay(r.start.slice(0, 10))} ${hm(r.start)}-${hm(r.end)}</span>${isNow(r) ? '<span class="soon">now</span>' : T(r.start) > Date.now() ? `<span class="soon">${rel(r.start)}</span>` : ''}${briefChip(r.brief)}`,
      `${r.link ? `<a class="btn primary sm" href="${esc(r.link)}" target="_blank">${ic('ai-icon-launch')}Join</a>` : ''}
       ${r.brief && r.brief.url ? `<a class="btn sm" href="${esc(r.brief.url)}" target="_blank">Open brief</a>` : ''}
       ${r.live ? `<a class="btn sm" href="/live/${encodeURIComponent(r.key)}" target="_blank">Live page</a>` : ''}
       ${r.cal ? `<a class="btn ghost sm" href="${esc(r.cal)}" target="_blank">Calendar</a>` : ''}`);
    let h = '';
    // brief
    const b = r.brief || {};
    h += sec('Brief', '', b.state === 'ready' ? `<p>Ready. <a href="${esc(b.url)}" target="_blank">Open the brief</a>.</p>` :
      b.state === 'planned' ? `<p>Autopilot writes it at <b class="num">${hm(b.at)}</b> (T-12).</p>` :
      b.state === 'none' ? `<p class="muted">No engagement matched, so no automatic brief. Add the client to engagements/_aliases.yaml.</p>` :
      `<p>${esc(b.note || b.state)}</p>`);
    // follow-ups
    const f = r.followups;
    if (f) {
      const ours = f.actions.filter(a => a.ours), theirs = f.actions.filter(a => !a.ours);
      h += sec('Follow-ups', ours.length + theirs.length, `<p class="muted" style="font-size:12px">From ${esc(r.followups_from)}: ${esc(f.title)}, ${esc(f.date)}</p>
        ${ours.length ? `<div class="sub">We owe</div><ul class="plain">${ours.map(actLi).join('')}</ul>` : ''}
        ${theirs.length ? `<div class="sub">They owe</div><ul class="plain">${theirs.map(actLi).join('')}</ul>` : ''}`);
    } else if (r.client) {
      h += sec('Follow-ups', '', `<p class="muted">No call digest yet for ${esc(r.eng_label || 'this client')}. Next actions from STATUS below.</p>`);
    }
    // drafts
    if (r.engagement) {
      const ds = draftsFor(r.engagement), un = D.undoable.filter(i => i.engagement === r.engagement);
      h += sec('Drafts waiting', ds.length, ds.length || un.length ? ds.map(draftCard).join('') + un.map(draftCard).join('') : '<p class="muted">None.</p>');
    }
    if (e) h += engSections(e);
    else if (r.deals && r.deals.length) h += sec('HubSpot', r.deals.length, r.deals.map(dealCard).join('') + '<p class="muted" style="font-size:12px">Matched by company name in the title.</p>', crmAsof('hubspot'));
    if (r.external.length) h += sec('Client side', r.external.length, `<p class="muted" style="font-size:12px">${r.external.map(esc).join(', ')}</p>`);
    db.innerHTML = h;
  }

  function drawEngagement(dh, db, eng) {
    const e = D.engagements[eng];
    if (!e) { dh.innerHTML = head('', eng, '', ''); db.innerHTML = '<p class="muted">Not in this week.</p>'; return; }
    dh.innerHTML = head(e.alias_status || 'engagement', e.label, '', '');
    const ds = draftsFor(eng);
    db.innerHTML = sec('Drafts waiting', ds.length, ds.length ? ds.map(draftCard).join('') : '<p class="muted">None.</p>') + engSections(e);
  }

  const actLi = a => `<li><span class="grow">${esc(a.what)}</span><span class="side-m">${esc(a.owner)}${a.when && a.when !== 'unspecified' ? ', ' + esc(a.when) : ''}</span></li>`;
  const sec = (title, n, body, right) => `<section class="dsec"><div class="lu">${esc(title)}${n !== '' && n != null ? ` <span class="num">${n}</span>` : ''}${right ? `<span class="asof">${right}</span>` : ''}</div>${body}</section>`;
  const crmAsof = src => { const s = D.crm[src]; return s.as_of ? `as of ${hm(s.as_of)}${s.error ? ', last refresh failed' : ''}` : (s.error ? esc(s.error.slice(0, 50)) : 'not fetched yet'); };

  function engSections(e) {
    let h = '';
    const s = e.status;
    if (s) {
      const acts = s.actions || [];
      h += sec('Latest STATUS', '', `<p class="muted" style="font-size:12px">${esc(s.head)}${s.auto ? ' (autopilot)' : ''}${s.stage ? ' &middot; ' + esc(s.stage) : ''}</p>
        ${acts.map(a => `<div class="na"><b>Next:</b> ${esc(a.what)}${a.owner ? ` <span class="muted">(${esc(a.owner)}${a.by ? ', by ' + esc(a.by) : ''})</span>` : ''}</div>`).join('')}
        ${s.blocked ? `<p class="blocked"><span class="lu">Blocked</span>${esc(s.blocked)}</p>` : ''}
        <details class="full"><summary class="linkish">Full entry, ${s.bullets.length} lines</summary><ul>${s.bullets.map(x => `<li>${esc(x)}</li>`).join('')}</ul></details>`);
    }
    if (e.pending.length) h += sec('Pending artefacts', e.pending.length, `<ul class="plain">${e.pending.slice(0, 4).map(p => `<li><span class="grow">${esc(p.text)}</span></li>`).join('')}</ul>
      ${e.pending.length > 4 ? `<details class="full"><summary class="linkish">${e.pending.length - 4} more</summary><ul>${e.pending.slice(4).map(p => `<li>${esc(p.text)}</li>`).join('')}</ul></details>` : ''}`);
    h += sec('HubSpot', e.deals.length, e.deals.length ? e.deals.map(dealCard).join('') : '<p class="muted">No deal matched.</p>', crmAsof('hubspot'));
    h += sec('Asana', e.tasks.length, e.tasks.length ? `<ul class="plain">${e.tasks.map(t => {
      const pipe = (t.name || '').startsWith('[PIPELINE]');
      return `<li><span class="grow">${t.url ? `<a href="${esc(t.url)}" target="_blank">${esc(pipe ? t.name.replace('[PIPELINE] ', '') : t.name)}</a>` : esc(t.name)}${pipe ? ' <span class="chip out">pipeline</span>' : ''}</span>
        <span class="side-m">${t.due_on ? `<span class="chip ${t.due_on < D.today ? 'late' : t.due_on === D.today ? 'warn' : 'out'}">${esc(t.due_on.slice(5))}</span> ` : ''}${esc((t.assignee || '').split(' ')[0])}</span></li>`;
    }).join('')}</ul>` : '<p class="muted">No open task matched.</p>', crmAsof('asana'));
    return h;
  }

  function dealCard(d) {
    const url = d.id ? `https://app.hubspot.com/contacts/2048671/record/0-3/${encodeURIComponent(d.id)}` : '';
    const amt = d.amount ? `${d.currency || 'EUR'} ${Number(d.amount).toLocaleString('en-GB')}` : '';
    return `<div class="deal"><div class="dn"><span class="chip ready">${esc(d.stage)}</span>${url ? `<a href="${url}" target="_blank">${esc(d.name)}</a>` : esc(d.name)}</div>
      <div class="meta">${amt ? `<span>${esc(amt)}</span>` : ''}${d.close_date ? `<span>Close ${esc(d.close_date)}</span>` : ''}${d.owner ? `<span>${esc(d.owner)}</span>` : ''}${d.modified ? `<span>Updated ${esc(d.modified)}</span>` : ''}</div>
      ${d.next_step ? `<div class="ns"><span class="lu">Next step</span>${esc(d.next_step)}</div>` : ''}</div>`;
  }

  function drawDrafts(dh, db) {
    dh.innerHTML = head('Approvals', 'Drafts waiting', `<span>${D.drafts.length} pending. Nothing is sent until you click.</span>`, '');
    const g = {};
    D.drafts.forEach(i => (g[i.engagement] = g[i.engagement] || []).push(i));
    const order = Object.keys(g).sort((a, b) => g[b][0].created.localeCompare(g[a][0].created));
    let h = order.map(k => `<div class="dgrp"><h3>${esc(D.engagements[k] ? D.engagements[k].label : k)} <span class="num">${g[k].length}</span></h3>${g[k].map(draftCard).join('')}</div>`).join('');
    if (D.undoable.length) h += `<div class="dgrp"><h3>Written by the autopilot, undo open <span class="num">${D.undoable.length}</span></h3>${D.undoable.map(draftCard).join('')}</div>`;
    db.innerHTML = h || '<p class="empty" style="margin-top:16px">Nothing waiting.</p>';
  }

  function target(i) {
    const t = i.target || {};
    if (i.kind.startsWith('slack')) return ('#' + (t.channel_name || 'active-engagements').replace(/^#/, '')) + (t.thread_ts ? ' thread' : '');
    const to = Array.isArray(t.to) ? t.to.join(', ') : (t.to || '');
    return to || t.path || t.form_url || t.owner || '';
  }

  function draftCard(i) {
    const pend = i.status === 'pending';
    return `<div class="draft ${pend ? '' : 'done'}" data-id="${esc(i.id)}" data-kind="${esc(i.kind)}">
      <div class="dh"><span class="chip ${i.executable ? 'ready' : 'out'}">${esc(KIND[i.kind] || i.kind)}</span><span class="chip out">${esc(i.source)}</span><span class="wh">${esc(i.created.slice(5, 16).replace('T', ' '))}</span></div>
      <div class="dt">${esc(i.title)}</div>${target(i) ? `<div class="tg">${esc(target(i))}</div>` : ''}
      <div class="pv" data-act="edit" title="Click to edit">${esc(i.body.slice(0, 400))}</div>
      <div class="row">
        ${pend && i.executable ? `<button class="btn primary sm" data-act="approve">${esc(GO[i.kind] || 'Approve')}</button>` : ''}
        ${pend ? `<button class="btn sm" data-act="edit">Edit</button>` : ''}
        <button class="btn sm" data-act="copy">${ic('ai-icon-copy')}Copy</button>
        ${i.open_url ? `<a class="btn sm" href="${esc(i.open_url)}" target="_blank">Open target</a>` : ''}
        ${pend ? `<button class="btn ghost sm" data-act="done">Mark done</button><button class="btn ghost sm danger" data-act="reject">Reject</button>` : ''}
        ${i.can_undo ? `<button class="btn sm danger" data-act="undo">Undo write</button>` : ''}
        <span class="st">${pend ? '' : esc(i.status)}</span>
      </div></div>`;
  }

  async function post(u, d) {
    const r = await fetch(u, { method: 'POST', headers: H, body: JSON.stringify(d || {}) });
    try { return await r.json(); } catch (e) { return { ok: false, error: 'HTTP ' + r.status }; }
  }

  async function draftAction(card, act) {
    const id = card.dataset.id, kind = card.dataset.kind, it = D.drafts.concat(D.undoable).find(x => x.id === id);
    const ta = card.querySelector('textarea');
    const body = ta ? ta.value : it.body;
    if (act === 'edit') {
      if (ta) return ta.focus();
      const t = document.createElement('textarea');
      t.value = it.body; t.addEventListener('input', () => t.dataset.dirty = '1');
      card.querySelector('.pv').replaceWith(t);
      const row = card.querySelector('.row');
      const save = document.createElement('button'); save.className = 'btn sm'; save.dataset.act = 'save'; save.textContent = 'Save edit';
      row.querySelector('[data-act="edit"]').replaceWith(save);
      t.focus(); return;
    }
    if (act === 'copy') { await navigator.clipboard.writeText(body); return toast('Copied'); }
    if (act === 'save') { await post(`/api/items/${id}/save`, { body }); if (ta) ta.dataset.dirty = ''; toast('Saved'); return load(); }
    if (act === 'approve') {
      if (!confirm(ASK[kind] || 'Approve?')) return;
      const r = await post(`/api/items/${id}/approve`, { body });
      toast(r.ok ? r.result : 'Failed: ' + (r.error || r.detail)); if (ta) ta.dataset.dirty = ''; return load();
    }
    if (act === 'undo') {
      if (!confirm('Revert this STATUS entry? Adds a revert commit in engagements.')) return;
      const r = await post(`/api/items/${id}/undo`); toast(r.ok ? r.result : 'Failed: ' + (r.error || r.detail)); return load();
    }
    if (act === 'reject' && !confirm('Reject this draft?')) return;
    if (ta && ta.dataset.dirty === '1' && act === 'done') await post(`/api/items/${id}/save`, { body });
    await post(`/api/items/${id}/${act}`); toast(act === 'done' ? 'Marked done' : 'Rejected'); load();
  }

  // ------------------------------------------------------------ routing + events
  function route() {
    const h = location.hash;
    if (h === '#drafts') openDrawer({ type: 'drafts' });
    else if (h.startsWith('#m=')) openDrawer({ type: 'm', key: decodeURIComponent(h.slice(3)) });
    else if (h.startsWith('#e=')) openDrawer({ type: 'e', key: decodeURIComponent(h.slice(3)) });
    else if (h === '#week' || h === '#today') { closeDrawer(); document.getElementById(h.slice(1)).scrollIntoView({ behavior: 'smooth' }); }
  }

  document.addEventListener('click', ev => {
    const o = ev.target.closest('[data-open]');
    if (o) { ev.preventDefault(); location.hash = 'm=' + encodeURIComponent(o.dataset.open); return; }
    if (ev.target.closest('[data-close]') || ev.target.id === 'scrim') return closeDrawer();
    if (ev.target.closest('[data-show-all]')) { show = 'all'; localStorage.setItem('atlas.show', show); return renderWeek(); }
    const s = ev.target.closest('.seg [data-show]');
    if (s) { show = s.dataset.show; localStorage.setItem('atlas.show', show); return renderWeek(); }
    const a = ev.target.closest('.draft [data-act]');
    if (a) { ev.preventDefault(); return draftAction(a.closest('.draft'), a.dataset.act); }
  });
  window.addEventListener('hashchange', () => D && route());
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && drawer) closeDrawer(); });
  window.addEventListener('scroll', () => $('#top').classList.toggle('scrolled', scrollY > 4), { passive: true });
  $('#wk-prev').onclick = () => { week--; load(); };
  $('#wk-next').onclick = () => { week++; load(); };
  $('#wk-now').onclick = () => { week = 0; load(); };
  $('#refresh').onclick = async () => {
    const r = await post('/api/refresh');
    toast(r.ok ? 'Refreshing HubSpot and Asana, about 3 min' : 'Not started: ' + (r.error || r.detail));
    load();
  };

  load().then(route);
})();
