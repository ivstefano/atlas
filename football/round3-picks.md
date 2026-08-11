# Round 3 (final group games) — picks

Saved: 2026-06-25
Standing when picked: 5th, 42 pts. Leader Vandal 49 (9 exacts). 2nd 100kila 45. 4th zhenya 42.

Scoring decoded: exact score = 3pts, correct outcome = 1pt. Exacts win this.

## Final slate

| Match | Pick | Type |
|---|---:|---|
| Curacao vs Ivory Coast | 0-2 | lock |
| Ecuador vs Germany | 1-2 | ⚡ chase |
| Tunisia vs Netherlands | 0-2 | lock |
| Japan vs Sweden | 2-1 | ⚡ chase |
| Turkey vs USA | 1-1 | base |
| Paraguay vs Australia | 1-0 | base |
| Norway vs France | 1-1 | base |
| Senegal vs Iraq | 2-0 | lock |
| Cape Verde vs Saudi Arabia | 1-1 | base |
| Uruguay vs Spain | 1-2 | ⚡ chase |
| New Zealand vs Belgium | 0-2 | lock |
| Egypt vs Iran | 1-1 | base |
| Panama vs England | 0-2 | lock |
| Croatia vs Ghana | 2-1 | ⚡ chase |
| Colombia vs Portugal | 1-1 | ⚡ chase (differential) |
| DR Congo vs Uzbekistan | 2-0 | base |
| Algeria vs Austria | 1-1 | base |
| Jordan vs Argentina | 0-2 | lock |

⚡ = differential to catch leaders. If protecting position instead, revert these to safe: Ecuador-Germany 1-1, Japan-Sweden 1-1, Croatia-Ghana 2-0.

## Method (for next round)
1. Bookmaker 1X2 odds = base (favourite + margin).
2. Adjust for what each team needs from the final game: already-safe → rotate/relax/lower scoring; must-win → attack/open up.
3. Lesson from R1-R2: this WC is draw-heavy, favourites concede. Avoid clean-sheet 2-0/3-0 spam. Lean 2-1, 1-1.
4. Chasing from behind = pick exacts the field misses, not safe 1-pointers.

## Standings going into round 3 (from official MD1+MD2 results)
- A: Mexico 6 / South Korea 3 / Czechia 1 / South Africa 1
- B: Canada 4 / Switzerland 4 / Bosnia 1 / Qatar 1
- C: Brazil 4 / Morocco 4 / Scotland 3 / Haiti 0
- D: USA 6 / Australia 3 / Paraguay 3 / Turkey 0
- E: Germany 6 / Ivory Coast 3 / Ecuador 1 / Curacao 1
- F: Netherlands 4 / Japan 4 / Sweden 3 / Tunisia 0
- G: Egypt 4 / Iran 2 / Belgium 2 / New Zealand 1
- H: Spain 4 / Uruguay 2 / Cape Verde 2 / Saudi Arabia 1
- I: France 6 / Norway 6 / Senegal 0 / Iraq 0
- J: Argentina 6 / Austria 3 / Algeria 3 / Jordan 0
- K: Colombia 6 / Portugal 4 / Congo DR 1 / Uzbekistan 0
- L: England 4 / Ghana 4 / Croatia 3 / Panama 0

## RESULT (round 3 scored)
Moved 5th → 2nd. Round-3 exacts: Croatia 2-1 ✅, Egypt 1-1 ✅ (both ⚡ chase picks), Panama 0-2 England ✅ (consensus). Chase strategy worked — differentials scored the +3s.

Standing after round 3:
- 1st Vandal: 77 preds, 11 exact, 65 pts
- 2nd ivo: 66 preds, 9 exact, 63 pts  ← us
- 3rd zhenya: 72 preds, 9 exact, 60 pts
- 4th 100kila: 72 preds, 5 exact, 58 pts

Read: 2 behind leader but 11 FEWER predictions. Best exact-rate in top group (~14%). Vandal's lead is volume, not skill. Knockouts = shared fixed games → volume edge gone. Stay level per-game + find 1-2 differentials = catch him.

## Knockout strategy (when bracket sets)
1. Enter EVERY game. Vandal's only structural edge was volume — kill it.
2. No draws in scoring sense — extra time/pens. Pick the 90-min score; account for cagey knockout football (lower scoring than groups).
3. Factor rotation hangover vs full-strength, and who's carrying knockout pressure.
4. Differentials still the lever: out-read Vandal on 1-2 exacts, lead flips.

## SCORING CONFIRMED (from source, 2026-06-28)
App = Django on EC2 i-09e29707b367e6908 (eu-central-1, "World cup predictor", 172.31.8.235 via IRIS VPN, public 3.75.240.41). Code in ~/worldcup2026, app `predictions/`.
- `calculate_points` (models.py): exact both scores = 3pts; same outcome direction (incl. draw=draw) = 1pt; else 0. No knockout-special logic — groups and KO scored identically.
- Results pulled from the-odds-api `/scores` (fetch_results.py). That API reports soccer at REGULATION score, no penalty bump. So a 1-1 that goes to pens is stored 1-1.
- THEREFORE: a draw is a valid, scoreable KO pick. 1-1 on a shootout game = full 3pts regardless of who advances. Don't flip coin-flip draws to 1-0.
- Caveat to watch: if a KO result ever shows a +1 winner score for a game that finished level, the API is bumping it — revisit. First shootout confirms live.

## Round of 32 picks (saved 2026-06-28)
| Match | Pick | Type |
|---|---:|---|
| South Africa vs Canada | 0-2 | lock |
| Brazil vs Japan | 2-1 | ⚡ chase (Japan scores) |
| Germany vs Paraguay | 2-0 | lock |
| Netherlands vs Morocco | 1-1 | coin-flip (NL on pens) |
| Ivory Coast vs Norway | 1-2 | ⚡ chase (Norway away fav) |
| France vs Sweden | 2-0 | lock |
| USA vs Bosnia | 2-1 | manual (no odds shown) |
| Australia vs Egypt | 1-1 | coin-flip (Egypt on pens) |
| Argentina vs Cape Verde | 2-0 | lock |

KO method notes: pick 90-min score; KO football cagier/lower-scoring than groups; factor rotation hangover + knockout pressure. Differentials (⚡) are the lever to catch Vandal (2 ahead). Enter every game — his only edge was volume.

## Next
Round of 16 after these. Talk again when set.
