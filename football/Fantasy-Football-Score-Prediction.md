> From: https://chatgpt.com/c/6a2bbe1a-e460-83ed-a2f7-348bcf3be6bd

# you asked

message time: 2026-06-12 11:06:50

we're having fantasy football for the world cup, is there a really reliable mechanism to guess the scores for the matches for it that's proven to work ??

---

# chatgpt response

I’ll treat this as “how do we make the best score picks, not magic certainty.” I’ll check what has actually held up: betting markets, Elo-style ratings, and Poisson/xG models, then give you a practical workflow.

There is **no reliable mechanism to guess exact scores** in football in the sense of “this consistently predicts 2–1 / 1–0 correctly.” Football is too low-scoring and random. But there **are proven better-than-vibes mechanisms** that work well enough to beat casual guessing.

The best practical method is:

## 1. Use bookmaker odds as the strongest baseline

Bookmaker markets are very hard to beat because they aggregate injuries, team strength, public/private info, betting flow, and expert pricing. Recent forecasting research still treats betting odds as one of the strongest information sources; one 2026 model uses odds from **24 bookmakers** as part of its team-strength estimates. ([zeileis.org](https://www.zeileis.org/news/fifa2026/))

For fantasy score prediction, this means:  
**do not start from your opinion. Start from market probabilities.**

## 2. Convert match odds into expected goals

The best classic score-prediction framework is:

**Team strength / odds / Elo → expected goals → Poisson score probabilities**

This is basically how many serious football forecasting models work. The 2026 World Cup forecasting model by Zeileis/Groll/Hvattum et al. estimates predicted goals for possible matches and then computes probabilities for scores like 0–0, 1–0, 2–1 using a bivariate Poisson distribution. ([zeileis.org](https://www.zeileis.org/news/fifa2026/))

Older World Cup work also uses **Elo + Poisson regression + Monte Carlo simulations** to estimate match and tournament probabilities. ([arXiv](https://arxiv.org/abs/1806.01930))

## 3. Use Elo/FIFA form only as adjustment, not as the base

Elo ratings are useful. There is long-standing research showing that Elo-based covariates help predict football match results. ([IDEAS/RePEc](https://ideas.repec.org/a/eee/intfor/v26yi3p460-470.html))

But for your game, I would use Elo like this:

> “Bookmaker odds say 55% Brazil, 27% draw, 18% Serbia. Elo agrees, so don’t overthink it.”  
> “Bookmaker odds say close match, but Elo/form/injuries slightly favor one side — adjust the scoreline by one goal max.”

Do **not** make brave emotional picks like “Argentina will smash them 4–0” unless the odds and expected goals support it.

## 4. Pick the score that maximizes fantasy points, not the most romantic score

Most common high-probability football scores are boring:

| Match type | Safer score picks |
|---|---|
| Strong favorite vs weak team | 2–0, 2–1, 3–0 |
| Medium favorite | 1–0, 2–1 |
| Close teams | 1–1, 1–0, 0–1 |
| Defensive/low total | 0–0, 1–0, 1–1 |
| High total / attacking teams | 2–1, 2–2, 3–1 |

Even good models usually predict **outcome** much better than **exact score**. A current World Cup model cited by El País reports around **59% accuracy for win/draw/loss**, but that is not the same as exact score accuracy; exact scores are much harder. ([El País](https://elpais.com/deportes/mundial-futbol/2026-06-11/quien-ganara-el-mundial-asi-arrancan-nuestras-predicciones.html?utm_source=chatgpt.com))

## My recommended “Ivo fantasy mechanism”

For each match:

1. Look at **1X2 odds**: win/draw/loss.
2. Look at **over/under 2.5 goals**.
3. Look at **both teams to score** odds.
4. Pick from a small score template:

| Market signal | Pick |
|---|---|
| Favorite + under 2.5 | 1–0 or 2–0 |
| Favorite + over 2.5 + BTTS yes | 2–1 |
| Heavy favorite + over 2.5 | 3–0 or 3–1 |
| Balanced + under 2.5 | 1–1 or 0–0 |
| Balanced + over 2.5 | 2–2 or 2–1 either way |
| Underdog value but not crazy | 1–1, not 0–3 |

## The honest answer

The most “proven” system is **bookmaker consensus + Poisson expected-goals model + Elo/team-news adjustment**. It will not make you reliably guess exact scores, but it should beat people picking emotionally.

For a friend group fantasy game, the winning approach is usually:  
**play conservative in group-stage obvious matches, use 1–1 more than your ego wants, avoid too many 3–0s, and only take spicy differentials when you need to catch up.**

---

# you asked

message time: 2026-06-12 11:47:29

So this is the full list which matches should I predict and how: ⚽
Iris World Cup 2026 Predictions
Matches
Results
Leaderboard
Players
ivo
Logout
🏆 World Cup 2026 Matches
Canada
vs
Bosnia & Herzegovina
📅 Jun 12, 10:00 PM
Group B
⏰ 10h 13m left
📊 Odds: 1.85 | 3.58 | 4.66
Predict
USA
vs
Paraguay
📅 Jun 13, 04:00 AM
Group D
⏰ 16h 13m left
📊 Odds: 1.97 | 3.49 | 4.16
Predict
Qatar
vs
Switzerland
📅 Jun 13, 10:00 PM
Group B
⏰ 1d 10h 13m left
📊 Odds: 12.86 | 6.85 | 1.23
Predict
Brazil
vs
Morocco
📅 Jun 14, 01:00 AM
Group C
⏰ 1d 13h 13m left
📊 Odds: 1.68 | 3.77 | 5.6
Predict
Haiti
vs
Scotland
📅 Jun 14, 04:00 AM
Group C
⏰ 1d 16h 13m left
📊 Odds: 6.01 | 4.3 | 1.56
Predict
Australia
vs
Turkey
📅 Jun 14, 07:00 AM
Group D
⏰ 1d 19h 13m left
📊 Odds: 5.22 | 3.88 | 1.7
Predict
Germany
vs
Curacao
📅 Jun 14, 08:00 PM
Group E
⏰ 2d 8h 13m left
Predict
Netherlands
vs
Japan
📅 Jun 14, 11:00 PM
Group F
⏰ 2d 11h 13m left
📊 Odds: 2.04 | 3.62 | 3.72
Predict
Ivory Coast
vs
Ecuador
📅 Jun 15, 02:00 AM
Group E
⏰ 2d 14h 13m left
📊 Odds: 3.69 | 2.83 | 2.45
Predict
Sweden
vs
Tunisia
📅 Jun 15, 05:00 AM
Group F
⏰ 2d 17h 13m left
📊 Odds: 1.93 | 3.48 | 4.32
Predict
Spain
vs
Cape Verde
📅 Jun 15, 07:00 PM
Group H
⏰ 3d 7h 13m left
📊 Odds: 1.08 | 11.78 | 28.81
Predict
Belgium
vs
Egypt
📅 Jun 15, 10:00 PM
Group G
⏰ 3d 10h 13m left
📊 Odds: 1.65 | 4.0 | 5.6
Predict
Saudi Arabia
vs
Uruguay
📅 Jun 16, 01:00 AM
Group H
⏰ 3d 13h 13m left
📊 Odds: 7.75 | 4.47 | 1.46
Predict
Iran
vs
New Zealand
📅 Jun 16, 04:00 AM
Group G
⏰ 3d 16h 13m left
📊 Odds: 1.84 | 3.57 | 4.73
Predict
France
vs
Senegal
📅 Jun 16, 10:00 PM
Group I
⏰ 4d 10h 13m left
📊 Odds: 1.49 | 4.4 | 7.09
Predict
Iraq
vs
Norway
📅 Jun 17, 01:00 AM
Group I
⏰ 4d 13h 13m left
📊 Odds: 14.39 | 7.3 | 1.2
Predict
Argentina
vs
Algeria
📅 Jun 17, 04:00 AM
Group J
⏰ 4d 16h 13m left
📊 Odds: 1.41 | 4.56 | 9.05
Predict
Austria
vs
Jordan
📅 Jun 17, 07:00 AM
Group J
⏰ 4d 19h 13m left
📊 Odds: 1.33 | 5.52 | 9.25
Predict
Portugal
vs
DR Congo
📅 Jun 17, 08:00 PM
Group K
⏰ 5d 8h 13m left
📊 Odds: 1.28 | 5.84 | 11.74
Predict
England
vs
Croatia
📅 Jun 17, 11:00 PM
Group L
⏰ 5d 11h 13m left
📊 Odds: 1.74 | 3.9 | 4.91
Predict
Ghana
vs
Panama
📅 Jun 18, 02:00 AM
Group L
⏰ 5d 14h 13m left
📊 Odds: 2.18 | 3.51 | 3.45
Predict
Uzbekistan
vs
Colombia
📅 Jun 18, 05:00 AM
Group K
⏰ 5d 17h 13m left
📊 Odds: 9.17 | 4.74 | 1.39
Predict
Czech Republic
vs
South Africa
📅 Jun 18, 07:00 PM
Group A
⏰ 6d 7h 13m left
📊 Odds: 1.93 | 3.3 | 4.07
Predict
Switzerland
vs
Bosnia & Herzegovina
📅 Jun 18, 10:00 PM
Group B
⏰ 6d 10h 13m left
📊 Odds: 1.58 | 3.93 | 5.3
Predict
Canada
vs
Qatar
📅 Jun 19, 01:00 AM
Group B
⏰ 6d 13h 13m left
📊 Odds: 1.29 | 5.03 | 9.6
Predict
Mexico
vs
South Korea
📅 Jun 19, 04:00 AM
Group A
⏰ 6d 16h 13m left
📊 Odds: 1.75 | 3.61 | 4.5
Predict
USA
vs
Australia
📅 Jun 19, 10:00 PM
Group D
⏰ 7d 10h 13m left
📊 Odds: 1.71 | 3.95 | 4.3
Predict
Scotland
vs
Morocco
📅 Jun 20, 01:00 AM
Group C
⏰ 7d 13h 13m left
📊 Odds: 4.1 | 3.2 | 1.95
Predict
Brazil
vs
Haiti
📅 Jun 20, 03:30 AM
Group C
⏰ 7d 15h 43m left
📊 Odds: 1.09 | 13.0 | 34.0
Predict
Turkey
vs
Paraguay
📅 Jun 20, 06:00 AM
Group D
⏰ 7d 18h 13m left
📊 Odds: 2.2 | 3.13 | 3.42
Predict
Netherlands
vs
Sweden
📅 Jun 20, 08:00 PM
Group F
⏰ 8d 8h 13m left
📊 Odds: 1.61 | 4.02 | 4.95
Predict
Germany
vs
Ivory Coast
📅 Jun 20, 11:00 PM
Group E
⏰ 8d 11h 13m left
📊 Odds: 1.54 | 4.27 | 5.29
Predict
Ecuador
vs
Curacao
📅 Jun 21, 03:00 AM
Group E
⏰ 8d 15h 13m left
Predict
Tunisia
vs
Japan
📅 Jun 21, 07:00 AM
Group F
⏰ 8d 19h 13m left
📊 Odds: 5.25 | 3.57 | 1.66
Predict
Spain
vs
Saudi Arabia
📅 Jun 21, 07:00 PM
Group H
⏰ 9d 7h 13m left
📊 Odds: 1.09 | 10.21 | 21.54
Predict
Belgium
vs
Iran
📅 Jun 21, 10:00 PM
Group G
⏰ 9d 10h 13m left
📊 Odds: 1.37 | 4.62 | 7.75
Predict
Uruguay
vs
Cape Verde
📅 Jun 22, 01:00 AM
Group H
⏰ 9d 13h 13m left
📊 Odds: 1.4 | 4.47 | 7.28
Predict
New Zealand
vs
Egypt
📅 Jun 22, 04:00 AM
Group G
⏰ 9d 16h 13m left
📊 Odds: 4.33 | 3.81 | 1.73
Predict
Argentina
vs
Austria
📅 Jun 22, 08:00 PM
Group J
⏰ 10d 8h 13m left
📊 Odds: 1.61 | 3.71 | 5.49
Predict
France
vs
Iraq
📅 Jun 23, 12:00 AM
Group I
⏰ 10d 12h 13m left
📊 Odds: 1.11 | 8.06 | 24.06
Predict
Norway
vs
Senegal
📅 Jun 23, 03:00 AM
Group I
⏰ 10d 15h 13m left
📊 Odds: 2.09 | 3.51 | 3.28
Predict
Jordan
vs
Algeria
📅 Jun 23, 06:00 AM
Group J
⏰ 10d 18h 13m left
📊 Odds: 6.2 | 4.17 | 1.48
Predict
Portugal
vs
Uzbekistan
📅 Jun 23, 08:00 PM
Group K
⏰ 11d 8h 13m left
📊 Odds: 1.21 | 6.31 | 10.82
Predict
England
vs
Ghana
📅 Jun 23, 11:00 PM
Group L
⏰ 11d 11h 13m left
📊 Odds: 1.29 | 5.32 | 8.93
Predict
Panama
vs
Croatia
📅 Jun 24, 02:00 AM
Group L
⏰ 11d 14h 13m left
📊 Odds: 6.29 | 3.68 | 1.55
Predict
Colombia
vs
DR Congo
📅 Jun 24, 05:00 AM
Group K
⏰ 11d 17h 13m left
📊 Odds: 1.43 | 4.23 | 7.22
Predict
Switzerland
vs
Canada
📅 Jun 24, 10:00 PM
Group B
⏰ 12d 10h 13m left
📊 Odds: 2.1 | 3.33 | 3.44
Predict
Bosnia & Herzegovina
vs
Qatar
📅 Jun 24, 10:00 PM
Group B
⏰ 12d 10h 13m left
📊 Odds: 1.62 | 3.64 | 5.49
Predict
Morocco
vs
Haiti
📅 Jun 25, 01:00 AM
Group C
⏰ 12d 13h 13m left
📊 Odds: 1.3 | 5.06 | 9.14
Predict
Scotland
vs
Brazil
📅 Jun 25, 01:00 AM
Group C
⏰ 12d 13h 13m left
📊 Odds: 5.37 | 4.82 | 1.47
Predict
South Africa
vs
South Korea
📅 Jun 25, 04:00 AM
Group A
⏰ 12d 16h 13m left
📊 Odds: 4.03 | 3.35 | 1.92
Predict
Czech Republic
vs
Mexico
📅 Jun 25, 04:00 AM
Group A
⏰ 12d 16h 13m left
📊 Odds: 4.54 | 3.56 | 1.75
Predict
Curacao
vs
Ivory Coast
📅 Jun 25, 11:00 PM
Group E
⏰ 13d 11h 13m left
Predict
Ecuador
vs
Germany
📅 Jun 25, 11:00 PM
Group E
⏰ 13d 11h 13m left
📊 Odds: 4.5 | 3.7 | 1.73
Predict
Tunisia
vs
Netherlands
📅 Jun 26, 02:00 AM
Group F
⏰ 13d 14h 13m left
📊 Odds: 6.28 | 4.22 | 1.47
Predict
Japan
vs
Sweden
📅 Jun 26, 02:00 AM
Group F
⏰ 13d 14h 13m left
📊 Odds: 2.08 | 3.37 | 3.47
Predict
Turkey
vs
USA
📅 Jun 26, 05:00 AM
Group D
⏰ 13d 17h 13m left
📊 Odds: 2.56 | 3.52 | 2.56
Predict
Paraguay
vs
Australia
📅 Jun 26, 05:00 AM
Group D
⏰ 13d 17h 13m left
📊 Odds: 2.12 | 3.17 | 3.57
Predict
Norway
vs
France
📅 Jun 26, 10:00 PM
Group I
⏰ 14d 10h 13m left
📊 Odds: 4.16 | 3.54 | 1.83
Predict
Senegal
vs
Iraq
📅 Jun 26, 10:00 PM
Group I
⏰ 14d 10h 13m left
📊 Odds: 1.38 | 4.55 | 7.6
Predict
Cape Verde
vs
Saudi Arabia
📅 Jun 27, 03:00 AM
Group H
⏰ 14d 15h 13m left
📊 Odds: 2.52 | 3.27 | 2.75
Predict
Uruguay
vs
Spain
📅 Jun 27, 03:00 AM
Group H
⏰ 14d 15h 13m left
📊 Odds: 5.15 | 3.86 | 1.61
Predict
New Zealand
vs
Belgium
📅 Jun 27, 06:00 AM
Group G
⏰ 14d 18h 13m left
📊 Odds: 9.66 | 5.73 | 1.25
Predict
Egypt
vs
Iran
📅 Jun 27, 06:00 AM
Group G
⏰ 14d 18h 13m left
📊 Odds: 2.22 | 2.99 | 3.55
Predict
Panama
vs
England
📅 Jun 28, 12:00 AM
Group L
⏰ 15d 12h 13m left
📊 Odds: 7.56 | 6.38 | 1.27
Predict
Croatia
vs
Ghana
📅 Jun 28, 12:00 AM
Group L
⏰ 15d 12h 13m left
📊 Odds: 1.6 | 3.78 | 5.51
Predict
Colombia
vs
Portugal
📅 Jun 28, 02:30 AM
Group K
⏰ 15d 14h 43m left
📊 Odds: 3.46 | 3.27 | 2.12
Predict
DR Congo
vs
Uzbekistan
📅 Jun 28, 02:30 AM
Group K
⏰ 15d 14h 43m left
📊 Odds: 2.29 | 3.32 | 3.05
Predict
Algeria
vs
Austria
📅 Jun 28, 05:00 AM
Group J
⏰ 15d 17h 13m left
📊 Odds: 3.74 | 3.03 | 2.13
Predict
Jordan
vs
Argentina
📅 Jun 28, 05:00 AM
Group J
⏰ 15d 17h 13m left
📊 Odds: 13.33 | 7.12 | 1.16
Predict

---

# chatgpt response

I’ll convert the listed 1X2 odds into normalized implied probabilities, then use a simple Poisson-style score template. Where odds are missing, I’ll mark it as a manual conservative pick rather than pretend it is model-derived.

I’d use the **Pick** column as your default. The **Alt** column is only for cases where you want to be slightly different from everyone else.

I converted your odds into normalized implied probabilities and used a simple Poisson score template. The fixture list matches the official World Cup schedule structure, but the predictions below are based mainly on the odds you pasted, not secret team news. FIFA confirms this is the 48-team 2026 format with group-stage fixtures across the listed June dates. ([FIFA](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums?utm_source=chatgpt.com))

| Match | Pick | Confidence | Alt if chasing |
|---|---:|---|---:|
| Canada vs Bosnia & Herzegovina | **1–0** | Low | 1–1 |
| USA vs Paraguay | **1–0** | Low | 1–1 |
| Qatar vs Switzerland | **0–2** | High | 0–3 |
| Brazil vs Morocco | **1–0** | Medium | 2–0 |
| Haiti vs Scotland | **0–1** | Medium | 0–2 |
| Australia vs Turkey | **0–1** | Medium | 0–2 |
| Germany vs Curacao | **3–0** | Manual | 4–0 |
| Netherlands vs Japan | **1–0** | Low | 1–1 |
| Ivory Coast vs Ecuador | **0–0** | Low | 0–1 |
| Sweden vs Tunisia | **1–0** | Low | 1–1 |
| Spain vs Cape Verde | **3–0** | High | 4–0 |
| Belgium vs Egypt | **1–0** | Medium | 2–0 |
| Saudi Arabia vs Uruguay | **0–1** | Medium | 0–2 |
| Iran vs New Zealand | **1–0** | Low | 1–1 |
| France vs Senegal | **1–0** | Medium | 2–0 |
| Iraq vs Norway | **0–2** | High | 0–3 |
| Argentina vs Algeria | **1–0** | Medium | 2–0 |
| Austria vs Jordan | **2–0** | High | 1–0 |
| Portugal vs DR Congo | **2–0** | High | 3–0 |
| England vs Croatia | **1–0** | Medium | 1–1 |
| Ghana vs Panama | **1–1** | Low | 1–0 |
| Uzbekistan vs Colombia | **0–1** | Medium | 0–2 |
| Czech Republic vs South Africa | **1–0** | Low | 1–1 |
| Switzerland vs Bosnia & Herzegovina | **1–0** | Medium | 2–0 |
| Canada vs Qatar | **2–0** | High | 1–0 |
| Mexico vs South Korea | **1–0** | Low | 1–1 |
| USA vs Australia | **1–1** | Low | 1–0 |
| Scotland vs Morocco | **0–1** | Low | 1–1 |
| Brazil vs Haiti | **3–0** | High | 4–0 |
| Turkey vs Paraguay | **1–0** | Low | 1–1 |
| Netherlands vs Sweden | **1–0** | Medium | 1–1 |
| Germany vs Ivory Coast | **1–0** | Medium | 2–0 |
| Ecuador vs Curacao | **2–0** | Manual | 3–0 |
| Tunisia vs Japan | **0–1** | Medium | 0–2 |
| Spain vs Saudi Arabia | **3–0** | High | 4–0 |
| Belgium vs Iran | **1–0** | Medium | 2–0 |
| Uruguay vs Cape Verde | **1–0** | Medium | 2–0 |
| New Zealand vs Egypt | **0–1** | Low | 1–1 |
| Argentina vs Austria | **1–0** | Medium | 2–0 |
| France vs Iraq | **2–0** | High | 3–0 |
| Norway vs Senegal | **1–1** | Low | 1–0 |
| Jordan vs Algeria | **0–1** | Medium | 0–2 |
| Portugal vs Uzbekistan | **2–0** | High | 3–0 |
| England vs Ghana | **2–0** | High | 1–0 |
| Panama vs Croatia | **0–1** | Medium | 0–2 |
| Colombia vs DR Congo | **1–0** | Medium | 2–0 |
| Switzerland vs Canada | **1–0** | Low | 1–1 |
| Bosnia & Herzegovina vs Qatar | **1–0** | Medium | 2–0 |
| Morocco vs Haiti | **2–0** | High | 1–0 |
| Scotland vs Brazil | **1–2** | Medium | 0–2 |
| South Africa vs South Korea | **0–1** | Low | 1–1 |
| Czech Republic vs Mexico | **0–1** | Low | 1–1 |
| Curacao vs Ivory Coast | **0–2** | Manual | 0–1 |
| Ecuador vs Germany | **0–1** | Low | 1–1 |
| Tunisia vs Netherlands | **0–1** | Medium | 0–2 |
| Japan vs Sweden | **1–0** | Low | 1–1 |
| Turkey vs USA | **1–1** | Low | 0–1 |
| Paraguay vs Australia | **1–0** | Low | 1–1 |
| Norway vs France | **0–1** | Low | 1–1 |
| Senegal vs Iraq | **1–0** | Medium | 2–0 |
| Cape Verde vs Saudi Arabia | **1–1** | Low | 1–0 |
| Uruguay vs Spain | **0–1** | Medium | 0–2 |
| New Zealand vs Belgium | **0–2** | High | 0–1 |
| Egypt vs Iran | **1–0** | Low | 0–0 |
| Panama vs England | **1–2** | High | 0–2 |
| Croatia vs Ghana | **1–0** | Medium | 2–0 |
| Colombia vs Portugal | **0–1** | Low | 1–1 |
| DR Congo vs Uzbekistan | **1–1** | Low | 1–0 |
| Algeria vs Austria | **0–1** | Low | 0–0 |
| Jordan vs Argentina | **0–2** | High | 0–3 |

The main pattern: **don’t overuse 3–0/4–0**. Exact-score games are usually won by boring picks: **1–0, 1–1, 2–0, 0–1**.  

The ones I’d be most comfortable locking are: **Spain 3–0 Cape Verde, Brazil 3–0 Haiti, France 2–0 Iraq, Portugal 2–0 Uzbekistan, England 2–0 Ghana, Jordan 0–2 Argentina, Qatar 0–2 Switzerland**.

---

# you asked

message time: 2026-06-12 11:54:52

should I input all or just for this round?

---

# chatgpt response

I’d input **only this round / the matches that lock soon**, unless the game forces you to predict all upfront.

Why:

**Best strategy: predict as late as possible.**  
You get more info closer to kick-off: injuries, lineups, motivation, whether a team already qualified, rotation, odds movement, etc.

For this format, do this:

### Input now
Predict the matches happening in the next **2–3 days**:

| Match | Prediction |
|---|---:|
| Canada vs Bosnia & Herzegovina | **1–0** |
| USA vs Paraguay | **1–0** |
| Qatar vs Switzerland | **0–2** |
| Brazil vs Morocco | **1–0** |
| Haiti vs Scotland | **0–1** |
| Australia vs Turkey | **0–1** |
| Germany vs Curacao | **3–0** |
| Netherlands vs Japan | **1–0** |
| Ivory Coast vs Ecuador | **0–0** |
| Sweden vs Tunisia | **1–0** |

### Do not input all yet, especially final group games

The last group matches are the most dangerous to predict early because teams may:
- already qualify and rotate players;
- need a draw only;
- chase goal difference;
- rest stars;
- become desperate after bad results.

So for matches like **Uruguay vs Spain**, **Colombia vs Portugal**, **Jordan vs Argentina**, etc., wait.

### Exception

If the app has **one deadline for all group-stage predictions**, then yes, input all now using the table I gave. But if each match locks separately, predict them in batches.

My recommendation: **enter the first 10 now**, then update the next batch every evening.

---

# you asked

message time: 2026-06-12 11:56:27

a lot of 1-0 and 0-1 why is that?

---

# chatgpt response

Because with only **1X2 odds** available, the safest model becomes quite conservative.

Football has low scoring, and when a team is only a **mild or medium favourite**, the most likely exact-score outcomes usually cluster around:

**1–0, 1–1, 0–1, 2–1, 2–0**

So when odds say something like:

- **1.85 | 3.58 | 4.66** → home favourite, but not dominant  
- **2.04 | 3.62 | 3.72** → almost balanced  
- **1.75 | 3.61 | 4.50** → mild favourite  

the model says: “They probably win, but not by a lot.”  
That often translates to **1–0**.

The important thing: **1–0 does not mean I think the team will dominate.** It means:

> “Most likely winner + low/normal total goals + exact-score risk control.”

For heavy favourites, I moved to **2–0 / 3–0**, for example:

- Spain vs Cape Verde → **3–0**
- Brazil vs Haiti → **3–0**
- Portugal vs Uzbekistan → **2–0**
- France vs Iraq → **2–0**
- Jordan vs Argentina → **0–2**

But for matches like **Canada–Bosnia**, **USA–Paraguay**, **Netherlands–Japan**, **Mexico–South Korea**, going too often to 2–0 or 2–1 becomes more emotional than statistical.

That said, your table may be **too conservative** if your fantasy scoring rewards exact goal difference or total goals more than exact score. To make it less boring, I’d upgrade some 1–0s like this:

| Original | Slightly more aggressive |
|---|---:|
| Brazil vs Morocco 1–0 | **2–0** |
| Belgium vs Egypt 1–0 | **2–0** |
| France vs Senegal 1–0 | **2–0** |
| Argentina vs Algeria 1–0 | **2–0** |
| Germany vs Ivory Coast 1–0 | **2–0** |
| Switzerland vs Bosnia 1–0 | **2–0** |
| Netherlands vs Sweden 1–0 | **2–1** |
| England vs Croatia 1–0 | **1–1** or **2–1** |

My practical recommendation: keep the boring 1–0s for **low-confidence matches**, but use **2–0 / 2–1** for stronger teams where you believe they can actually control the game.

So your final style should be:

**Safe mode:** many 1–0s, 0–1s, 1–1s.  
**Fun-but-still-rational mode:** convert 20–30% of those into 2–0 or 2–1.

---

# you asked

message time: 2026-06-12 11:57:26

okay so what would the final list for the round look like

---

# chatgpt response

I’ll make this as a practical “enter these now” list for the first batch, with a bit less 1–0 spam but still odds-driven.

---

# you asked

message time: 2026-06-12 11:57:52

also if you have to predict South Korea
vs
Czech Republic and mexico vs south africa how would you predict them

---

# chatgpt response

Yes — assuming **“round” = first match for every team / Matchday 1**, I’d input this:

| Match | Final pick |
|---|---:|
| Mexico vs South Africa | **2–0** |
| South Korea vs Czech Republic | **2–1** |
| Canada vs Bosnia & Herzegovina | **1–1** |
| USA vs Paraguay | **1–0** |
| Qatar vs Switzerland | **0–2** |
| Brazil vs Morocco | **2–0** |
| Haiti vs Scotland | **0–1** |
| Australia vs Turkey | **0–1** |
| Germany vs Curacao | **3–0** |
| Netherlands vs Japan | **1–1** |
| Ivory Coast vs Ecuador | **1–1** |
| Sweden vs Tunisia | **1–0** |
| Spain vs Cape Verde | **3–0** |
| Belgium vs Egypt | **2–0** |
| Saudi Arabia vs Uruguay | **0–2** |
| Iran vs New Zealand | **1–0** |
| France vs Senegal | **2–0** |
| Iraq vs Norway | **0–2** |
| Argentina vs Algeria | **2–0** |
| Austria vs Jordan | **2–0** |
| Portugal vs DR Congo | **2–0** |
| England vs Croatia | **2–1** |
| Ghana vs Panama | **1–1** |
| Uzbekistan vs Colombia | **0–2** |

Small note: **Mexico–South Africa already finished 2–0**, and **South Korea–Czech Republic already finished 2–1**, according to Reuters, so only use those if your game still accepts them or you’re filling historical predictions. ([Reuters](https://www.reuters.com/sports/soccer/mexico-get-world-cup-party-started-with-2-0-win-over-nine-man-south-africa-2026-06-11/?utm_source=chatgpt.com))

For the not-yet-played ones, the ones I’d feel best about are:

**Qatar 0–2 Switzerland, Spain 3–0 Cape Verde, Portugal 2–0 DR Congo, Austria 2–0 Jordan, Iraq 0–2 Norway, Argentina 2–0 Algeria.**

The “spicy but reasonable” ones are:

**Canada 1–1 Bosnia**, **Netherlands 1–1 Japan**, **England 2–1 Croatia**.

---

# you asked

message time: 2026-06-12 12:03:07

so was your prediction Mexico vs South Africa	2–0
South Korea vs Czech Republic	2–1 or you checked online, I want to see if your prediction would have won them now that we know the results

---

# chatgpt response

I checked online.

So **no, those two were not a clean pre-match prediction from me**. I should have made that clearer.

When you asked about:

| Match | I gave |
|---|---:|
| Mexico vs South Africa | 2–0 |
| South Korea vs Czech Republic | 2–1 |

I had already seen current result info: Mexico beat South Africa **2–0**, and South Korea beat Czech Republic **2–1**. Reuters confirms both results. ([Reuters](https://www.reuters.com/sports/soccer/mexicans-celebrate-breaking-opening-day-curse-with-2-0-win-2026-06-11/?utm_source=chatgpt.com))

So those two **cannot be counted as proof that the prediction method worked**.

The valid test is the remaining matches from your list where we predicted before knowing the result, e.g.:

| Match | Our pick |
|---|---:|
| Canada vs Bosnia | 1–1 |
| USA vs Paraguay | 1–0 |
| Qatar vs Switzerland | 0–2 |
| Brazil vs Morocco | 2–0 |
| Haiti vs Scotland | 0–1 |
| Australia vs Turkey | 0–1 |

For measuring whether the method works, we should track:
**exact score hit**, **correct outcome**, and **close result** separately.

---

# you asked

message time: 2026-06-12 12:04:18

I already used these based on earlier prediction: 🏆 World Cup 2026 Matches
Canada
vs
Bosnia & Herzegovina
📅 Jun 12, 10:00 PM
Group B
⏰ 9h 56m left
📊 Odds: 1.85 | 3.58 | 4.66
Your pick: 1 - 0
Edit
USA
vs
Paraguay
📅 Jun 13, 04:00 AM
Group D
⏰ 15h 56m left
📊 Odds: 1.97 | 3.49 | 4.16
Your pick: 1 - 0
Edit
Qatar
vs
Switzerland
📅 Jun 13, 10:00 PM
Group B
⏰ 1d 9h 56m left
📊 Odds: 12.86 | 6.85 | 1.23
Your pick: 0 - 2
Edit
Brazil
vs
Morocco
📅 Jun 14, 01:00 AM
Group C
⏰ 1d 12h 56m left
📊 Odds: 1.68 | 3.77 | 5.6
Your pick: 1 - 0
Edit
Haiti
vs
Scotland
📅 Jun 14, 04:00 AM
Group C
⏰ 1d 15h 56m left
📊 Odds: 6.01 | 4.3 | 1.56
Your pick: 0 - 1
Edit
Australia
vs
Turkey
📅 Jun 14, 07:00 AM
Group D
⏰ 1d 18h 56m left
📊 Odds: 5.22 | 3.88 | 1.7
Your pick: 0 - 1
Edit
Germany
vs
Curacao
📅 Jun 14, 08:00 PM
Group E
⏰ 2d 7h 56m left
Your pick: 3 - 0
Edit
Netherlands
vs
Japan
📅 Jun 14, 11:00 PM
Group F
⏰ 2d 10h 56m left
📊 Odds: 2.04 | 3.62 | 3.72
Your pick: 1 - 0
Edit
Ivory Coast
vs
Ecuador
📅 Jun 15, 02:00 AM
Group E
⏰ 2d 13h 56m left
📊 Odds: 3.69 | 2.83 | 2.45
Your pick: 0 - 0
Edit
Sweden
vs
Tunisia
📅 Jun 15, 05:00 AM
Group F
⏰ 2d 16h 56m left
📊 Odds: 1.93 | 3.48 | 4.32
Your pick: 1 - 0

---

# chatgpt response

Given these are already entered and still editable, I’d only change picks where the earlier list was overly conservative. I’ll separate “keep” from “worth editing,” not rewrite everything blindly.

These are **not bad picks**. I would **not panic-edit all of them**.

But if edits are free, I’d change only these:

| Match | Your pick | I’d change to | Why |
|---|---:|---:|---|
| **Canada vs Bosnia** | 1–0 | **1–1** | Canada are favourites, but several previews point to a tight/low-scoring match; Bosnia are not a joke opponent. Reuters notes Džeko is fit and Bosnia are approaching it as a big underdog fight. ([Reuters](https://www.reuters.com/sports/soccer/bosnia-will-play-with-hearts-world-cup-opener-says-coach-barbarez-2026-06-12/?utm_source=chatgpt.com)) |
| **Brazil vs Morocco** | 1–0 | **2–0** | Brazil are a clearer favourite than the 1–0 suggests. 1–0 is safe, but 2–0 feels better for a strong-team group opener. |
| **Netherlands vs Japan** | 1–0 | **1–1** | Japan are dangerous, and Group F previews flag this as a possible upset-watch game rather than an easy Dutch win. ([New York Post](https://nypost.com/2026/06/10/sports/world-cup-2026-group-f-preview-prediction-odds-full-team-overviews/?utm_source=chatgpt.com)) |
| **Ivory Coast vs Ecuador** | 0–0 | **1–1** | Draw is logical, but 0–0 is very specific. 1–1 gives you the same draw call with a more common football score. |

I would **keep these**:

| Match | Keep |
|---|---:|
| USA vs Paraguay | **1–0** |
| Qatar vs Switzerland | **0–2** |
| Haiti vs Scotland | **0–1** |
| Australia vs Turkey | **0–1** |
| Germany vs Curacao | **3–0** |
| Sweden vs Tunisia | **1–0** |

So my cleaned-up version for this round would be:

| Match | Final pick |
|---|---:|
| Canada vs Bosnia & Herzegovina | **1–1** |
| USA vs Paraguay | **1–0** |
| Qatar vs Switzerland | **0–2** |
| Brazil vs Morocco | **2–0** |
| Haiti vs Scotland | **0–1** |
| Australia vs Turkey | **0–1** |
| Germany vs Curacao | **3–0** |
| Netherlands vs Japan | **1–1** |
| Ivory Coast vs Ecuador | **1–1** |
| Sweden vs Tunisia | **1–0** |

If you want to be more conservative and not over-edit, the **top 2 changes** I’d make are:

**Brazil 1–0 → 2–0**  
**Netherlands 1–0 → 1–1**

The rest are judgment calls.

---

# you asked

message time: 2026-06-12 12:08:58

why didn't we include Spain
vs
Cape Verde
📅 Jun 15, 07:00 PM
Group H
⏰ 3d 6h 51m left
📊 Odds: 1.08 | 11.78 | 28.81
Predict
Belgium
vs
Egypt
📅 Jun 15, 10:00 PM
Group G
⏰ 3d 9h 51m left
📊 Odds: 1.65 | 4.0 | 5.6

---

# chatgpt response

Because I cut the “enter now” batch at the first **10 matches** shown in your screen — up to **Sweden vs Tunisia**. That was a practical cutoff, not because Spain and Belgium should be skipped.

You **should include them** if you are entering the full first round / next few days.

Add these:

| Match | Pick | Confidence |
|---|---:|---|
| Spain vs Cape Verde | **3–0** | Very high |
| Belgium vs Egypt | **2–0** | Medium-high |

Why:

**Spain vs Cape Verde — 3–0**  
Odds **1.08 | 11.78 | 28.81** basically say Spain are massive favourites. The question is not “Spain win?” but “2–0, 3–0, or 4–0?” I’d take **3–0** as the balanced exact-score pick.

**Belgium vs Egypt — 2–0**  
Odds **1.65 | 4.00 | 5.60** make Belgium a clear but not insane favourite. Earlier I gave **1–0**, but if we are making the list less conservative, **2–0** is better.

So the updated next-batch ending should be:

| Match | Final pick |
|---|---:|
| Sweden vs Tunisia | **1–0** |
| Spain vs Cape Verde | **3–0** |
| Belgium vs Egypt | **2–0** |

I’d input those two as well.

---

# you asked

message time: 2026-06-15 10:18:49

Okay this is what's up so far ⚽
Iris.ai World Cup 2026 Predictions
Matches
Results
Leaderboard
Players
ivo
Logout
📋 Results
Sweden
vs
Tunisia
📅 Jun 15, 05:00 AM
Group F
5 - 1
Your pick: 1 - 0 +1pts
Ivory Coast
vs
Ecuador
📅 Jun 15, 02:00 AM
Group E
1 - 0
Your pick: 1 - 1 +0pts
Netherlands
vs
Japan
📅 Jun 14, 11:00 PM
Group F
2 - 2
Your pick: 1 - 1 +1pts
Germany
vs
Curacao
📅 Jun 14, 08:00 PM
Group E
7 - 1
Your pick: 3 - 0 +1pts
Australia
vs
Turkey
📅 Jun 14, 07:00 AM
Group D
2 - 0
Your pick: 0 - 1 +0pts
Haiti
vs
Scotland
📅 Jun 14, 04:00 AM
Group C
0 - 1
Your pick: 0 - 1 +3pts
Brazil
vs
Morocco
📅 Jun 14, 01:00 AM
Group C
1 - 1
Your pick: 2 - 0 +0pts
Qatar
vs
Switzerland
📅 Jun 13, 10:00 PM
Group B
1 - 1
Your pick: 0 - 2 +0pts
USA
vs
Paraguay
📅 Jun 13, 04:00 AM
Group D
4 - 1
Your pick: 1 - 0 +1pts
Canada
vs
Bosnia & Herzegovina
📅 Jun 12, 10:00 PM
Group B
1 - 1
Your pick: 1 - 1 +3pts
South Korea
vs
Czech Republic
📅 Jun 12, 05:00 AM
Group A
2 - 1
Mexico
vs
South Africa
📅 Jun 11, 10:00 PM
Group A
2 - 0 and what we've guessed which brought me to second place

---

# chatgpt response

Nice — that’s actually a **solid start**.

From the 10 entered predictions shown:

| Metric | Result |
|---|---:|
| Exact scores | **2/10** |
| Correct result direction | **6/10** |
| Points | **10 pts** |
| Big misses | Brazil, Switzerland, Australia/Turkey |
| Best hits | Canada 1–1, Haiti 0–1 |

So the system did what we wanted in one sense: it got you **points often enough** and hit two exacts. For exact-score fantasy, **2 exact scores from 10 is good**.

The lesson, though: we were **too conservative on favourites**.

Examples:

| Match | Pick | Actual | Lesson |
|---|---:|---:|---|
| Germany vs Curacao | 3–0 | 7–1 | Heavy favourites can explode |
| Sweden vs Tunisia | 1–0 | 5–1 | Some “modest favourite” picks need 2–0/2–1/3–1 |
| USA vs Paraguay | 1–0 | 4–1 | USA stronger than odds implied / game opened up |
| Brazil vs Morocco | 2–0 | 1–1 | Still don’t over-trust big names |
| Qatar vs Switzerland | 0–2 | 1–1 | Away favourite in World Cup group opener is risky |

So for the next picks I’d adjust the model like this:

### New rule for the next round

**1. Heavy favourite:** use **3–0 / 3–1**, not always 2–0.  
Example: Spain vs Cape Verde → **3–0**, maybe even **4–0** if chasing.

**2. Clear favourite but not elite mismatch:** use **2–0 or 2–1**, not 1–0.  
Example: Belgium vs Egypt → **2–0** or **2–1**.

**3. Close match:** keep using **1–1** more often.  
Canada 1–1 and Netherlands 2–2 show that draw-picking is valuable.

**4. Be careful with away favourites.**  
Switzerland and Turkey both burned us. Away favourite does not automatically mean 0–1.

For the immediate next two you asked about earlier, I’d still enter:

| Match | Pick |
|---|---:|
| Spain vs Cape Verde | **3–0** |
| Belgium vs Egypt | **2–0** |

But after seeing Germany 7–1, USA 4–1, Sweden 5–1, I’d say:

| Safer | More aggressive |
|---|---:|
| Spain 3–0 Cape Verde | **Spain 4–0 Cape Verde** |
| Belgium 2–0 Egypt | **Belgium 2–1 Egypt** |

My choice: **Spain 3–0**, **Belgium 2–0**.

You’re second, so don’t go crazy. Keep the odds-based base, but upgrade some boring 1–0s into **2–0 / 2–1 / 3–1** where the favourite has real attacking upside.

---

# you asked

message time: 2026-06-15 10:20:21

what do those odds mean: Spain
vs
Cape Verde
📅 Jun 15, 07:00 PM
Group H
⏰ 8h 39m left
📊 Odds: 1.08 | 11.78 | 28.81
Your pick: 3 - 0
Edit
Belgium
vs
Egypt
📅 Jun 15, 10:00 PM
Group G
⏰ 11h 39m left
📊 Odds: 1.65 | 4.0 | 5.6

---

# chatgpt response

These are **decimal 1X2 odds**:

**Home win | Draw | Away win**

So:

## Spain vs Cape Verde  
**1.08 | 11.78 | 28.81**

| Outcome | Odds | Raw implied chance | Normalized chance |
|---|---:|---:|---:|
| Spain win | 1.08 | 92.6% | **~88.6%** |
| Draw | 11.78 | 8.5% | **~8.1%** |
| Cape Verde win | 28.81 | 3.5% | **~3.3%** |

Meaning: bookmakers see Spain as an **overwhelming favourite**.  
A €10 bet on Spain at 1.08 returns **€10.80 total**, so only **€0.80 profit**. Very safe-looking, very low reward.

For fantasy: **Spain win is highly likely**, but the exact score is the question. Your **3–0** is sensible. Alternatives would be **4–0** if you want more upside, or **2–0** if you want safer/conservative.

## Belgium vs Egypt  
**1.65 | 4.00 | 5.60**

| Outcome | Odds | Raw implied chance | Normalized chance |
|---|---:|---:|---:|
| Belgium win | 1.65 | 60.6% | **~58.6%** |
| Draw | 4.00 | 25.0% | **~24.2%** |
| Egypt win | 5.60 | 17.9% | **~17.3%** |

Meaning: Belgium are clear favourites, but **not close to Spain-level certainty**. A draw or Egypt upset is still quite possible.

For fantasy: **2–0 Belgium** is reasonable, but this is more fragile than Spain. If you wanted a slightly more “World Cup chaos” pick, **2–1 Belgium** may be better because Egypt scoring once is not crazy.

My picks would stay:

| Match | Pick |
|---|---:|
| Spain vs Cape Verde | **3–0** |
| Belgium vs Egypt | **2–0** |

The odds say: **Spain pick is mostly about goal margin; Belgium pick is still about whether they control the game.**

---

# you asked

message time: 2026-06-15 10:21:31

can we do Saudi Arabia
vs
Uruguay
📅 Jun 16, 01:00 AM
Group H
⏰ 14h 38m left
📊 Odds: 7.75 | 4.47 | 1.46
Predict
Iran
vs
New Zealand
📅 Jun 16, 04:00 AM
Group G
⏰ 17h 38m left
📊 Odds: 1.84 | 3.57 | 4.73 
---
I'd continue feeding you more the next days

---

# chatgpt response

I’ll update the model using what we learned from the first 10: more goals when the favourite has attacking upside, but still cautious with away favourites and group-openers.

Yes — for these two I’d go:

| Match | Odds meaning | Final pick | Backup |
|---|---|---:|---:|
| Saudi Arabia vs Uruguay | Uruguay ~66% win chance after normalizing odds | **0–1** | 0–2 |
| Iran vs New Zealand | Iran ~52–53% win chance, draw quite live | **1–1** | 1–0 |

## Saudi Arabia vs Uruguay — pick **0–1**

Odds: **7.75 | 4.47 | 1.46**

Normalized roughly:

| Outcome | Chance |
|---|---:|
| Saudi win | ~12% |
| Draw | ~22% |
| Uruguay win | ~66% |

Uruguay are clear favourites, but not “Spain vs Cape Verde” level. Also, Uruguay’s prep had some disruption from travel delays, and previews describe this as a match where Saudi Arabia can make Uruguay work rather than a guaranteed blowout. ([The Guardian](https://www.theguardian.com/football/2026/jun/15/uruguay-delayed-by-plane-paperwork-as-world-cup-travel-challenges-continue?utm_source=chatgpt.com))

So I would **not** go 0–3.  
I’d choose **Saudi Arabia 0–1 Uruguay**.

Why not 0–2? It’s fine, but given the first-round chaos and the fact that Saudi Arabia often make these games annoying, **0–1 feels better for exact score**.

## Iran vs New Zealand — pick **1–1**

Odds: **1.84 | 3.57 | 4.73**

Normalized roughly:

| Outcome | Chance |
|---|---:|
| Iran win | ~52.5% |
| Draw | ~27% |
| New Zealand win | ~20.5% |

Iran are favourites, but not by enough to confidently call 2–0. There’s also noise around Iran’s preparation and political pressure, while New Zealand have Chris Wood available and are treating this as a focused football match. ([Reuters](https://www.reuters.com/sports/soccer/irans-manager-striker-pledge-play-all-iranians-despite-protests-2026-06-15/?utm_source=chatgpt.com))

So here I’d avoid overcommitting to Iran.

My pick: **Iran 1–1 New Zealand**.  
If you want to be safer with the odds: **Iran 1–0 New Zealand**.

Since you’re second, my actual entries would be:

| Enter this |
|---|
| Saudi Arabia 0–1 Uruguay |
| Iran 1–1 New Zealand |

---

# you asked

message time: 2026-06-15 10:24:21

if I were to bet in real life on all games let's say 10 euros would I be winning or losing?

---

# chatgpt response

I’ll separate two things, because the answer changes massively: betting the **1X2 outcome** from our score picks versus betting the **exact score** itself. Exact score betting is a different beast and much harsher.

For **real betting**, you would probably be **losing long-term** if you bet €10 on every game.

But there are two different cases:

## 1. Betting €10 on the match outcome from our picks

Example: our score pick **1–0 USA** means betting **USA win**, not exact score.

For the completed games where we had odds, this would actually be **up so far**:

| Match | Our outcome bet | Result | Profit/loss on €10 |
|---|---|---:|---:|
| Canada vs Bosnia | Draw @ 3.58 | 1–1 | **+€25.80** |
| USA vs Paraguay | USA @ 1.97 | 4–1 | **+€9.70** |
| Qatar vs Switzerland | Switzerland @ 1.23 | 1–1 | **-€10** |
| Brazil vs Morocco | Brazil @ 1.68 | 1–1 | **-€10** |
| Haiti vs Scotland | Scotland @ 1.56 | 0–1 | **+€5.60** |
| Australia vs Turkey | Turkey @ 1.70 | 2–0 | **-€10** |
| Netherlands vs Japan | Draw @ 3.62 | 2–2 | **+€26.20** |
| Ivory Coast vs Ecuador | Draw @ 2.83 | 1–0 | **-€10** |
| Sweden vs Tunisia | Sweden @ 1.93 | 5–1 | **+€9.30** |

Total staked: **€90**  
Total returned: **€126.60**  
Profit so far: **+€36.60**

So **so far**, betting the 1X2 outcomes from our score picks would be winning.

But that is a tiny sample and includes lucky high-value draw hits: **Canada 1–1** and **Netherlands 2–2**.

## 2. Betting €10 on exact scores

This is much riskier.

Our fantasy exact scores so far:

| Exact score hits | Result |
|---|---:|
| Canada 1–1 | Hit |
| Haiti 0–1 | Hit |
| Others | Missed |

So we hit **2 exact scores out of 10**, which is good for fantasy. But exact-score betting odds have bigger variance and often worse margins. Without knowing the exact-score odds offered, we cannot calculate the real profit.

## Why you probably lose long-term

Bookmakers build a margin into the odds. You can see it in the odds you pasted. For Spain vs Cape Verde, the implied probabilities add up to about **104.5%**, not 100%. For Belgium vs Egypt, they add up to about **103.5%**. That extra percentage is the bookmaker’s margin/overround. Betting literature commonly uses overround to estimate bookmaker margin, and responsible-gambling guidance frames gambling as entertainment rather than a way to make money. ([Karl Whelan](https://www.karlwhelan.com/Papers/Overround.pdf?utm_source=chatgpt.com))

Also, betting every game is usually worse than being selective. A model can be decent for fantasy but still not profitable, because fantasy rewards “close enough” and outcome points, while betting only rewards the exact market you chose.

## My honest take

For your fantasy game: **yes, continue using the model. It’s working decently.**

For real betting: I would **not bet €10 on every game**. At most, treat it as entertainment money. The smarter version would be:

| Approach | Better/worse |
|---|---|
| €10 on every match | Bad long-term |
| €10 only on strongest picks | Better |
| Small fun accumulator/parlay | Fun, but high-risk |
| Exact-score bets | Very high-risk |
| Fantasy predictions only | Best use of this model |

So if you had done **1X2 betting so far**, you’d be ahead. But if you continue blindly over all games, the most likely long-term outcome is that the bookmaker margin catches up.

---

# you asked

message time: 2026-06-16 18:29:31

Really strange event look: Iran
vs
New Zealand
📅 Jun 16, 04:00 AM
Group G
2 - 2
Your pick: 1 - 1 +1pts
Saudi Arabia
vs
Uruguay
📅 Jun 16, 01:00 AM
Group H
1 - 1
Your pick: 0 - 1 +0pts
Belgium
vs
Egypt
📅 Jun 15, 10:00 PM
Group G
1 - 1
Your pick: 2 - 0 +0pts
Spain
vs
Cape Verde
📅 Jun 15, 07:00 PM
Group H
0 - 0
Your pick: 3 - 0 +0pts

---

# chatgpt response

Yes, that is a **proper chaos day**. Not just “we guessed badly” — the results themselves are weird.

All four matches ended in draws: **Spain 0–0 Cape Verde, Belgium 1–1 Egypt, Saudi Arabia 1–1 Uruguay, Iran 2–2 New Zealand**. SBS described it as a historically unusual World Cup day: there had been a day in 1958 with four drawn matches, but that day had eight games; this was effectively a full draw sweep across the day. ([SBS Australia](https://www.sbs.com.au/news/article/fifa-world-cup-2026-results-june-16/i9qjp4lto?utm_source=chatgpt.com))

What happened to our model:

| Match | Pick | Result | Lesson |
|---|---:|---:|---|
| Spain vs Cape Verde | 3–0 | 0–0 | Even massive favourites can fail if they don’t score early |
| Belgium vs Egypt | 2–0 | 1–1 | Clear favourites are not safe enough for clean sheets |
| Saudi Arabia vs Uruguay | 0–1 | 1–1 | Away/neutral favourites are dangerous |
| Iran vs New Zealand | 1–1 | 2–2 | Draw call was right, score was too low |

Your points from these four: **+1 only**, from Iran–New Zealand.

The big signal for future predictions is this:

## We need fewer “favourite clean-sheet wins”

The model has been overusing:

**2–0, 3–0, 0–1, 0–2**

But this World Cup so far is giving us a lot of:

**1–1, 2–2, favourites conceding, favourites failing to break teams down**

Cape Verde’s 0–0 against Spain was a major upset; reports note Spain were held scoreless by World Cup debutants Cape Verde. ([SBS Australia](https://www.sbs.com.au/news/article/fifa-world-cup-2026-results-june-16/i9qjp4lto?utm_source=chatgpt.com)) Uruguay also needed to come back after Saudi Arabia scored first, with Reuters reporting both goals in that match came from goalkeeping errors. ([Reuters](https://www.reuters.com/sports/soccer/uruguay-held-1-1-draw-by-saudi-arabia-world-cup-opener-2026-06-16/?utm_source=chatgpt.com)) Iran also twice came from behind against New Zealand in a 2–2 draw. ([The Guardian](https://www.theguardian.com/football/live/2026/jun/16/fifa-world-cup-2026-live-iran-v-new-zealand-updates-irn-vs-nzl-group-f-match-score-latest?utm_source=chatgpt.com))

## Updated rule from now

For the next matches, I’d change our approach:

| Old habit | New habit |
|---|---|
| Big favourite = 3–0 | Big favourite = **2–1 or 2–0**, unless opponent is truly awful |
| Clear favourite = 2–0 | Clear favourite = **1–1 / 2–1 risk check** |
| Away favourite = 0–1 | Away favourite = **1–1 more often** |
| Weak underdog = won’t score | Assume underdogs can score once |

Your current situation is still okay. From the entered predictions, you have **2 exact hits** — Canada 1–1 and Haiti 0–1 — and several +1s. But for the next round, we should become more draw-aware and avoid assuming favourites keep clean sheets.

---

# you asked

message time: 2026-06-16 18:30:56

I want for those now: France
vs
Senegal
📅 Jun 16, 10:00 PM
Group I
⏰ 3h 30m left
📊 Odds: 1.49 | 4.4 | 7.09
Predict
Iraq
vs
Norway
📅 Jun 17, 01:00 AM
Group I
⏰ 6h 30m left
📊 Odds: 14.39 | 7.3 | 1.2
Predict
Argentina
vs
Algeria
📅 Jun 17, 04:00 AM
Group J
⏰ 9h 30m left
📊 Odds: 1.41 | 4.56 | 9.05
Predict
Austria
vs
Jordan
📅 Jun 17, 07:00 AM
Group J
⏰ 12h 30m left
📊 Odds: 1.33 | 5.52 | 9.25
Predict
Portugal
vs
DR Congo
📅 Jun 17, 08:00 PM
Group K
⏰ 1d 1h 30m left
📊 Odds: 1.28 | 5.84 | 11.74
Predict
England
vs
Croatia
📅 Jun 17, 11:00 PM
Group L
⏰ 1d 4h 30m left
📊 Odds: 1.74 | 3.9 | 4.91
Predict
Ghana
vs
Panama
📅 Jun 18, 02:00 AM
Group L
⏰ 1d 7h 30m left
📊 Odds: 2.18 | 3.51 | 3.45
Predict
Uzbekistan
vs
Colombia
📅 Jun 18, 05:00 AM
Group K
⏰ 1d 10h 30m left
📊 Odds: 9.17 | 4.74 | 1.39


---

Here are all results so far: Iran
vs
New Zealand
📅 Jun 16, 04:00 AM
Group G
2 - 2
Your pick: 1 - 1 +1pts
Saudi Arabia
vs
Uruguay
📅 Jun 16, 01:00 AM
Group H
1 - 1
Your pick: 0 - 1 +0pts
Belgium
vs
Egypt
📅 Jun 15, 10:00 PM
Group G
1 - 1
Your pick: 2 - 0 +0pts
Spain
vs
Cape Verde
📅 Jun 15, 07:00 PM
Group H
0 - 0
Your pick: 3 - 0 +0pts
Sweden
vs
Tunisia
📅 Jun 15, 05:00 AM
Group F
5 - 1
Your pick: 1 - 0 +1pts
Ivory Coast
vs
Ecuador
📅 Jun 15, 02:00 AM
Group E
1 - 0
Your pick: 1 - 1 +0pts
Netherlands
vs
Japan
📅 Jun 14, 11:00 PM
Group F
2 - 2
Your pick: 1 - 1 +1pts
Germany
vs
Curacao
📅 Jun 14, 08:00 PM
Group E
7 - 1
Your pick: 3 - 0 +1pts
Australia
vs
Turkey
📅 Jun 14, 07:00 AM
Group D
2 - 0
Your pick: 0 - 1 +0pts
Haiti
vs
Scotland
📅 Jun 14, 04:00 AM
Group C
0 - 1
Your pick: 0 - 1 +3pts
Brazil
vs
Morocco
📅 Jun 14, 01:00 AM
Group C
1 - 1
Your pick: 2 - 0 +0pts
Qatar
vs
Switzerland
📅 Jun 13, 10:00 PM
Group B
1 - 1
Your pick: 0 - 2 +0pts
USA
vs
Paraguay
📅 Jun 13, 04:00 AM
Group D
4 - 1
Your pick: 1 - 0 +1pts
Canada
vs
Bosnia & Herzegovina
📅 Jun 12, 10:00 PM
Group B
1 - 1
Your pick: 1 - 1 +3pts
South Korea
vs
Czech Republic
📅 Jun 12, 05:00 AM
Group A
2 - 1
Mexico
vs
South Africa
📅 Jun 11, 10:00 PM
Group A
2 - 0

---

# chatgpt response

I’ll treat the latest results as a signal that this tournament is draw-heavy and underdogs are scoring more than expected, then balance that against the odds for these eight.

Yes. Based on the chaos so far, I’d **stop assuming clean sheets**, but I would **not overreact so much that we pick draws everywhere**.

Here’s what I’d enter:

| Match | Pick | Confidence | Why |
|---|---:|---|---|
| France vs Senegal | **2–1** | Medium | France favourite, but Senegal are strong enough to score. France are heavily covered as a top side, but previews also frame Senegal as a serious opponent, not a pushover. ([New York Post](https://nypost.com/2026/06/16/betting/senegal-vs-france-world-cup-prediction-odds-picks-and-best-bets-for-tuesdays-match/?utm_source=chatgpt.com)) |
| Iraq vs Norway | **1–3** | High | Norway are one of the clearest favourites on this slate. After the recent underdog goals, I prefer 1–3 over 0–2. |
| Argentina vs Algeria | **2–0** | Medium-high | Argentina are strong favourites, but Algeria are not Cape Verde-tier weak. I’d keep the clean sheet here more than with France because Argentina are usually more control-oriented in these matches. |
| Austria vs Jordan | **2–0** | High | Austria are a big favourite; Jordan are debutants/underdogs. Austria’s pressing style is the main reason I prefer 2–0 over 1–0. |
| Portugal vs DR Congo | **2–1** | Medium-high | Portugal should win, but after this tournament pattern, DR Congo scoring once is plausible. |
| England vs Croatia | **1–1** | Low-medium | England are favourites, but Croatia are exactly the type of side that can make this ugly and experienced. A draw is a useful differential. |
| Ghana vs Panama | **1–1** | Low | Odds are close. This screams low-confidence draw rather than forcing Ghana. |
| Uzbekistan vs Colombia | **1–2** | Medium-high | Colombia are clear favourites, but again I’d allow the underdog goal. |

My actual entries would be:

| Enter |
|---|
| **France 2–1 Senegal** |
| **Iraq 1–3 Norway** |
| **Argentina 2–0 Algeria** |
| **Austria 2–0 Jordan** |
| **Portugal 2–1 DR Congo** |
| **England 1–1 Croatia** |
| **Ghana 1–1 Panama** |
| **Uzbekistan 1–2 Colombia** |

Most important adjustment from before: **fewer 2–0 / 3–0 clean-sheet assumptions**. Spain 0–0 Cape Verde, Belgium 1–1 Egypt, Saudi 1–1 Uruguay, and Iran 2–2 New Zealand are telling us that underdogs are surviving and scoring more than the odds suggested. Reuters also framed Uruguay–Saudi as another favourite held after the Spain draw had already shaken Group H. ([reuters.com](https://www.reuters.com/sports/soccer/uruguay-held-1-1-draw-by-saudi-arabia-world-cup-opener-2026-06-16/?utm_source=chatgpt.com))

---

# you asked

message time: 2026-06-16 18:33:24

what do we do with the low and medium  confidences

---

# chatgpt response

Use confidence as a **risk-control tool**, not as “change all low ones.”

Since you’re currently near the top, I’d play like this:

## Rule

| Confidence | What to do |
|---|---|
| **High** | Follow the odds. Don’t get cute. Pick favourite win. |
| **Medium** | Slightly adjust for tournament chaos: favourites win but concede, e.g. **2–1** instead of **2–0**. |
| **Low** | Use these as your controlled differentials: **1–1**, **2–1**, or **1–0** depending on odds. |

## For your current picks

I’d keep them like this:

| Match | Pick | Risk type | Action |
|---|---:|---|---|
| France vs Senegal | **2–1** | Medium | Keep |
| Iraq vs Norway | **1–3** | High | Keep |
| Argentina vs Algeria | **2–0** | Medium-high | Keep |
| Austria vs Jordan | **2–0** | High | Keep |
| Portugal vs DR Congo | **2–1** | Medium-high | Keep |
| England vs Croatia | **1–1** | Low-medium | Keep if you want a smart differential |
| Ghana vs Panama | **1–1** | Low | Keep |
| Uzbekistan vs Colombia | **1–2** | Medium-high | Keep |

The only one I’d consider changing is:

| Match | Current | Safer alternative |
|---|---:|---:|
| England vs Croatia | **1–1** | **2–1 England** |

But because this tournament has already given many favourite draws, I actually like **1–1** there.

## The practical strategy

Because you’re second, don’t gamble everywhere. Use this split:

**Safe/core picks:**  
Norway win, Argentina win, Austria win, Portugal win, Colombia win.

**Differential picks:**  
England 1–1, Ghana 1–1, France 2–1 instead of 2–0.

So I would **not change the list**. The low-confidence picks are not “bad”; they are where we intentionally accept uncertainty to possibly gain points others miss.

---

# you asked

message time: 2026-06-18 17:46:08

Look what happened: Uzbekistan
vs
Colombia
📅 Jun 18, 05:00 AM
Group K
1 - 3
Your pick: 1 - 2 +1pts
Ghana
vs
Panama
📅 Jun 18, 02:00 AM
Group L
1 - 0
Your pick: 1 - 1 +0pts
England
vs
Croatia
📅 Jun 17, 11:00 PM
Group L
4 - 2
Your pick: 2 - 1 +1pts
Portugal
vs
DR Congo
📅 Jun 17, 08:00 PM
Group K
1 - 1
Your pick: 2 - 1 +0pts
Austria
vs
Jordan
📅 Jun 17, 07:00 AM
Group J
3 - 1
Your pick: 2 - 0 +1pts
Argentina
vs
Algeria
📅 Jun 17, 04:00 AM
Group J
3 - 0
Your pick: 2 - 0 +1pts
Iraq
vs
Norway
📅 Jun 17, 01:00 AM
Group I
1 - 4
Your pick: 1 - 3 +1pts
France
vs
Senegal
📅 Jun 16, 10:00 PM
Group I
3 - 1
Your pick: 2 - 1 +1pts

---

# chatgpt response

This batch was **much better directionally**, but still missed exact scores.

| Metric | Result |
|---|---:|
| Matches | 8 |
| Correct outcome | **6/8** |
| Exact scores | **0/8** |
| Points | **6 pts** |
| Main miss type | We underestimated total goals |

The model was basically saying the right teams would win, but by **too small a scoreline**.

Examples:

| Match | Pick | Actual | What it tells us |
|---|---:|---:|---|
| France vs Senegal | 2–1 | 3–1 | Good direction, too low by one France goal |
| Iraq vs Norway | 1–3 | 1–4 | Very good read, Norway one goal higher |
| Argentina vs Algeria | 2–0 | 3–0 | Correct clean sheet, too low by one Argentina goal |
| Austria vs Jordan | 2–0 | 3–1 | Right winner, should have allowed Jordan goal |
| England vs Croatia | 2–1 | 4–2 | Right idea, game was much more open |
| Uzbekistan vs Colombia | 1–2 | 1–3 | Good read, Colombia one goal higher |

The two real misses:

| Match | Pick | Actual | Lesson |
|---|---:|---:|---|
| Portugal vs DR Congo | 2–1 | 1–1 | Portugal joined the “big favourite held” pattern |
| Ghana vs Panama | 1–1 | 1–0 | Close low-confidence game; these are coin flips |

## Updated model after this batch

We should now adjust like this:

### 1. For strong favourites, increase by one goal

Old: **2–0 / 2–1**  
New: **3–0 / 3–1**

This would have improved France, Norway, Argentina, Austria, Colombia.

### 2. Keep underdog-goal logic

The idea that underdogs can score was good:

- France 3–1 Senegal
- Iraq 1–4 Norway
- Austria 3–1 Jordan
- England 4–2 Croatia
- Uzbekistan 1–3 Colombia

So for future picks, **3–1 is becoming a very useful scoreline**.

### 3. Use 1–1 only selectively

1–1 helped earlier, but now we used it a bit too defensively. For matches with a favourite around **1.7–2.2 odds**, we should choose between:

- **2–1 favourite**
- **1–1 draw**
- **1–0 favourite**

depending on team style and group situation.

## The big takeaway

Our latest prediction style was **good for fantasy points**, but not aggressive enough for exact scores.

For the next set, I’d use this template:

| Match type | New default |
|---|---:|
| Huge favourite | **3–0 / 4–1** |
| Strong favourite | **3–1** |
| Clear favourite but tough opponent | **2–1** |
| Very close match | **1–1** |
| Defensive close match | **1–0** |
| Away favourite | **1–2 / 1–3** |

So yes — the model is learning. Next round, I’d be more willing to pick **3–1, 1–3, 3–0**, not just 2–1 and 2–0.

---

# you asked

message time: 2026-06-18 17:46:48

why the initial logic got me 3 exact matches you think?

---

# chatgpt response

Because the **initial logic was boring but statistically well-aligned with exact-score fantasy**.

The first version used mostly:

**1–0, 0–1, 1–1, 2–0**

That works surprisingly well because football’s most common exact scores are concentrated around those results. Even when the model is not “smart,” it benefits from base rates.

## Why it got exacts

### 1. It respected low-scoring football

Exact-score prediction is not about “who is better?” only. It is about the most common shapes of football matches.

Common realistic scores:

**1–0, 1–1, 2–0, 2–1, 0–1**

So when we picked **Canada 1–1** and **Haiti 0–1**, those were not genius reads; they were good “base-rate” picks.

### 2. It avoided overreacting to team names

The initial logic did not say:

- Brazil must smash Morocco.
- Switzerland must easily beat Qatar.
- Belgium must beat Egypt.
- Spain must destroy Cape Verde.

That mindset is exactly what later punished us. Big names did not always convert dominance into goals.

### 3. It used odds to choose direction, then conservative scores

The strongest part was:

> odds tell us the likely direction, but exact score should stay modest.

So for medium favourites, **1–0 / 0–1** was often more rational than **3–0**.

### 4. Early tournament matches are often weird

First group matches can be cautious. Teams don’t want to lose. Underdogs defend deeply. Favourites sometimes start slowly. That makes low scores and draws more likely than our emotional football brain expects.

## Why the later “improved” logic got fewer exacts

After Germany 7–1, Sweden 5–1, USA 4–1, we overcorrected toward higher scores:

- France 2–1 instead of maybe 3–1: direction right, not exact.
- Norway 1–3 instead of 1–4: direction right, not exact.
- Argentina 2–0 instead of 3–0: direction right, not exact.
- England 2–1 instead of 4–2: direction right, not exact.

That batch was good for **outcome points**, but less good for **exact score**.

## The lesson

For fantasy exact scores, we should not chase every pattern. The best hybrid is:

| Match type | Better exact-score default |
|---|---:|
| Huge mismatch | **3–0** |
| Strong favourite, opponent can score | **2–1** or **3–1** |
| Medium favourite | **1–0** or **2–1** |
| Close match | **1–1** |
| Away favourite | **0–1** or **1–2** |
| Chaos/tournament caution | **1–1** |

So the initial logic worked because it was **base-rate disciplined**. The updated logic helped with outcomes, but became a bit too reactive to recent high-scoring games.

Going forward, I’d use a split:  
**70% base-rate boring picks, 30% adjusted-for-form/chaos picks.**

---

# you asked

message time: 2026-06-18 17:47:50

Okay let's do next batch Czech Republic
vs
South Africa
📅 Jun 18, 07:00 PM
Group A
⏰ 1h 13m left
📊 Odds: 1.93 | 3.3 | 4.07
Predict
Switzerland
vs
Bosnia & Herzegovina
📅 Jun 18, 10:00 PM
Group B
⏰ 4h 13m left
📊 Odds: 1.58 | 3.93 | 5.3
Predict
Canada
vs
Qatar
📅 Jun 19, 01:00 AM
Group B
⏰ 7h 13m left
📊 Odds: 1.29 | 5.03 | 9.6
Predict
Mexico
vs
South Korea
📅 Jun 19, 04:00 AM
Group A
⏰ 10h 13m left
📊 Odds: 1.75 | 3.61 | 4.5
Predict
USA
vs
Australia
📅 Jun 19, 10:00 PM
Group D
⏰ 1d 4h 13m left
📊 Odds: 1.71 | 3.95 | 4.3
Predict
Scotland
vs
Morocco
📅 Jun 20, 01:00 AM
Group C
⏰ 1d 7h 13m left
📊 Odds: 4.1 | 3.2 | 1.95
Predict
Brazil
vs
Haiti
📅 Jun 20, 03:30 AM
Group C
⏰ 1d 9h 43m left
📊 Odds: 1.09 | 13.0 | 34.0
Predict
Turkey
vs
Paraguay
📅 Jun 20, 06:00 AM
Group D
⏰ 1d 12h 13m left
📊 Odds: 2.2 | 3.13 | 3.42
Predict
Netherlands
vs
Sweden
📅 Jun 20, 08:00 PM
Group F
⏰ 2d 2h 13m left
📊 Odds: 1.61 | 4.02 | 4.95
Predict
Germany
vs
Ivory Coast
📅 Jun 20, 11:00 PM
Group E
⏰ 2d 5h 13m left
📊 Odds: 1.54 | 4.27 | 5.29
Predict
Ecuador
vs
Curacao
📅 Jun 21, 03:00 AM
Group E
⏰ 2d 9h 13m left
Predict
Tunisia
vs
Japan
📅 Jun 21, 07:00 AM
Group F
⏰ 2d 13h 13m left
📊 Odds: 5.25 | 3.57 | 1.66
Predict
Spain
vs
Saudi Arabia
📅 Jun 21, 07:00 PM
Group H
⏰ 3d 1h 13m left
📊 Odds: 1.09 | 10.21 | 21.54
Predict
Belgium
vs
Iran
📅 Jun 21, 10:00 PM
Group G
⏰ 3d 4h 13m left
📊 Odds: 1.37 | 4.62 | 7.75
Predict

---

# chatgpt response

I’ll use the same hybrid now: boring base-rate exact scores first, then adjust only where the group situation/results so far clearly push toward higher goals or draws.

Yes — this batch needs the **hybrid model**, not pure odds. The pattern so far is:

**favourites often win, but underdogs score; close games often draw; huge favourites can still stall.**

I’d enter these:

| Match | Pick | Confidence | Why |
|---|---:|---|---|
| Czech Republic vs South Africa | **1–0** | Medium | Czechia need the win, but this looks low-scoring. Previews also expect a tactical/under 2.5 type match. ([New York Post](https://nypost.com/2026/06/18/betting/czechia-vs-south-africa-world-cup-prediction-odds-picks-best-bets-for-group-a-clash/?utm_source=chatgpt.com)) |
| Switzerland vs Bosnia & Herzegovina | **2–1** | Medium | Switzerland are favourites and need to recover after the Qatar draw, but Bosnia scoring is realistic. |
| Canada vs Qatar | **2–1** | Medium-high | Canada at home, Davies fit/available, and the group is totally open after both first games were 1–1. ([Reuters](https://www.reuters.com/sports/soccer/canada-seeking-take-control-early-qatar-world-cup-showdown-2026-06-18/?utm_source=chatgpt.com)) |
| Mexico vs South Korea | **2–1** | Medium | Both won first game; Mexico at home, but South Korea have momentum and can score. The Guardian frames it as one of the key matches of the day. ([The Guardian](https://www.theguardian.com/football/2026/jun/18/how-to-watch-world-cup-mexico-south-korea?utm_source=chatgpt.com)) |
| USA vs Australia | **2–1** | Medium | USA looked explosive, Australia already proved dangerous. I avoid clean sheet. |
| Scotland vs Morocco | **1–1** | Low-medium | Morocco are favourites, but Scotland already banked 3 points and can make it ugly. |
| Brazil vs Haiti | **3–0** | High | Huge mismatch, but after Spain 0–0 Cape Verde I’m not going 4–0. |
| Turkey vs Paraguay | **1–1** | Low | Odds are close and both teams need a response. Classic 1–1 spot. |
| Netherlands vs Sweden | **2–2** | Low-medium | Sweden just scored 5, Netherlands drew 2–2 with Japan. This group looks goal-heavy. |
| Germany vs Ivory Coast | **3–1** | Medium-high | Germany scored 7, Ivory Coast won 1–0. Germany win, but no clean sheet. |
| Ecuador vs Curacao | **2–0** | Manual | No odds shown. Ecuador should be stronger; Curacao conceded 7 to Germany. |
| Tunisia vs Japan | **1–2** | Medium | Japan scored twice vs Netherlands; Tunisia conceded 5 vs Sweden. Japan win but Tunisia may respond. |
| Spain vs Saudi Arabia | **2–0** | Medium-high | Spain should win, but after 0–0 Cape Verde I would not go wild. |
| Belgium vs Iran | **2–1** | Medium | Belgium need to improve after 1–1 Egypt; Iran just drew 2–2, so they can score. |

## My actual entries

| Enter this |
|---|
| **Czech Republic 1–0 South Africa** |
| **Switzerland 2–1 Bosnia & Herzegovina** |
| **Canada 2–1 Qatar** |
| **Mexico 2–1 South Korea** |
| **USA 2–1 Australia** |
| **Scotland 1–1 Morocco** |
| **Brazil 3–0 Haiti** |
| **Turkey 1–1 Paraguay** |
| **Netherlands 2–2 Sweden** |
| **Germany 3–1 Ivory Coast** |
| **Ecuador 2–0 Curacao** |
| **Tunisia 1–2 Japan** |
| **Spain 2–0 Saudi Arabia** |
| **Belgium 2–1 Iran** |

Most “exact-score hunting” picks here: **Czech 1–0**, **Turkey 1–1**, **Brazil 3–0**, **Spain 2–0**.  
Most risky but potentially valuable: **Netherlands 2–2 Sweden**, **Scotland 1–1 Morocco**.

---

# you asked

message time: 2026-06-22 10:19:04

I missed to matches also the results were different: New Zealand
vs
Egypt
📅 Jun 22, 04:00 AM
Group G
1 - 3
Uruguay
vs
Cape Verde
📅 Jun 22, 01:00 AM
Group H
2 - 2
Belgium
vs
Iran
📅 Jun 21, 10:00 PM
Group G
0 - 0
Your pick: 2 - 1 +0pts
Spain
vs
Saudi Arabia
📅 Jun 21, 07:00 PM
Group H
4 - 0
Your pick: 2 - 0 +1pts
Tunisia
vs
Japan
📅 Jun 21, 07:00 AM
Group F
0 - 4
Your pick: 1 - 2 +1pts
Ecuador
vs
Curacao
📅 Jun 21, 03:00 AM
Group E
0 - 0
Your pick: 2 - 0 +0pts
Germany
vs
Ivory Coast
📅 Jun 20, 11:00 PM
Group E
2 - 1
Your pick: 3 - 1 +1pts
Netherlands
vs
Sweden
📅 Jun 20, 08:00 PM
Group F
5 - 1
Your pick: 2 - 2 +0pts
Turkey
vs
Paraguay
📅 Jun 20, 06:00 AM
Group D
0 - 1
Your pick: 1 - 1 +0pts
Brazil
vs
Haiti
📅 Jun 20, 03:30 AM
Group C
3 - 0
Your pick: 3 - 0 +3pts
Scotland
vs
Morocco
📅 Jun 20, 01:00 AM
Group C
0 - 1
Your pick: 1 - 1 +0pts
USA
vs
Australia
📅 Jun 19, 10:00 PM
Group D
2 - 0
Your pick: 2 - 1 +1pts
Mexico
vs
South Korea
📅 Jun 19, 04:00 AM
Group A
1 - 0
Your pick: 2 - 1 +1pts
Canada
vs
Qatar
📅 Jun 19, 01:00 AM
Group B
6 - 0
Your pick: 2 - 1 +1pts
Switzerland
vs
Bosnia & Herzegovina
📅 Jun 18, 10:00 PM
Group B
4 - 1
Your pick: 2 - 1 +1pts
Czech Republic
vs
South Africa
📅 Jun 18, 07:00 PM
Group A
1 - 1
Your pick: 1 - 0 +0pts
Uzbekistan
vs
Colombia
📅 Jun 18, 05:00 AM
Group K
1 - 3
Your pick: 1 - 2 +1pts
Ghana
vs
Panama
📅 Jun 18, 02:00 AM
Group L
1 - 0
Your pick: 1 - 1 +0pts
England
vs
Croatia
📅 Jun 17, 11:00 PM
Group L
4 - 2
Your pick: 2 - 1 +1pts
Portugal
vs
DR Congo
📅 Jun 17, 08:00 PM
Group K
1 - 1
Your pick: 2 - 1 +0pts
Austria
vs
Jordan
📅 Jun 17, 07:00 AM
Group J
3 - 1
Your pick: 2 - 0 +1pts
Argentina
vs
Algeria
📅 Jun 17, 04:00 AM
Group J
3 - 0
Your pick: 2 - 0 +1pts
Iraq
vs
Norway
📅 Jun 17, 01:00 AM
Group I
1 - 4
Your pick: 1 - 3 +1pts
France
vs
Senegal
📅 Jun 16, 10:00 PM
Group I
3 - 1
Your pick: 2 - 1 +1pts
Iran
vs
New Zealand
📅 Jun 16, 04:00 AM
Group G
2 - 2
Your pick: 1 - 1 +1pts
Saudi Arabia
vs
Uruguay
📅 Jun 16, 01:00 AM
Group H
1 - 1
Your pick: 0 - 1 +0pts
Belgium
vs
Egypt
📅 Jun 15, 10:00 PM
Group G
1 - 1
Your pick: 2 - 0 +0pts
Spain
vs
Cape Verde
📅 Jun 15, 07:00 PM
Group H
0 - 0
Your pick: 3 - 0 +0pts
Sweden
vs
Tunisia
📅 Jun 15, 05:00 AM
Group F
5 - 1
Your pick: 1 - 0 +1pts
Ivory Coast
vs
Ecuador
📅 Jun 15, 02:00 AM
Group E
1 - 0
Your pick: 1 - 1 +0pts
Netherlands
vs
Japan
📅 Jun 14, 11:00 PM
Group F
2 - 2
Your pick: 1 - 1 +1pts
Germany
vs
Curacao
📅 Jun 14, 08:00 PM
Group E
7 - 1
Your pick: 3 - 0 +1pts
Australia
vs
Turkey
📅 Jun 14, 07:00 AM
Group D
2 - 0
Your pick: 0 - 1 +0pts
Haiti
vs
Scotland
📅 Jun 14, 04:00 AM
Group C
0 - 1
Your pick: 0 - 1 +3pts
Brazil
vs
Morocco
📅 Jun 14, 01:00 AM
Group C
1 - 1
Your pick: 2 - 0 +0pts
Qatar
vs
Switzerland
📅 Jun 13, 10:00 PM
Group B
1 - 1
Your pick: 0 - 2 +0pts
USA
vs
Paraguay
📅 Jun 13, 04:00 AM
Group D
4 - 1
Your pick: 1 - 0 +1pts
Canada
vs
Bosnia & Herzegovina
📅 Jun 12, 10:00 PM
Group B
1 - 1
Your pick: 1 - 1 +3pts
South Korea
vs
Czech Republic
📅 Jun 12, 05:00 AM
Group A
2 - 1
Mexico
vs
South Africa
📅 Jun 11, 10:00 PM
Group A
2 - 0



----
I can show you how the first two people guessed
📊 Vandal's Predictions
Total Points
34
Earned
34
Scored Predictions
40
Match	Prediction	Result	Points
New Zealand vs Egypt
Jun 22 · Group G
0 - 1	1 - 3	1
Uruguay vs Cape Verde
Jun 21 · Group H
2 - 0	2 - 2	0
Belgium vs Iran
Jun 21 · Group G
2 - 1	0 - 0	0
Spain vs Saudi Arabia
Jun 21 · Group H
2 - 0	4 - 0	1
Tunisia vs Japan
Jun 21 · Group F
0 - 2	0 - 4	1
Ecuador vs Curacao
Jun 21 · Group E
2 - 0	0 - 0	0
Germany vs Ivory Coast
Jun 20 · Group E
2 - 0	2 - 1	1
Netherlands vs Sweden
Jun 20 · Group F
2 - 1	5 - 1	1
Turkey vs Paraguay
Jun 20 · Group D
1 - 0	0 - 1	0
Brazil vs Haiti
Jun 20 · Group C
3 - 0	3 - 0	3
Scotland vs Morocco
Jun 19 · Group C
0 - 1	0 - 1	3
USA vs Australia
Jun 19 · Group D
2 - 1	2 - 0	1
Mexico vs South Korea
Jun 19 · Group A
2 - 1	1 - 0	1
Canada vs Qatar
Jun 18 · Group B
1 - 0	6 - 0	1
Switzerland vs Bosnia & Herzegovina
Jun 18 · Group B
2 - 1	4 - 1	1
Czech Republic vs South Africa
Jun 18 · Group A
1 - 0	1 - 1	0
Uzbekistan vs Colombia
Jun 18 · Group K
0 - 1	1 - 3	1
Ghana vs Panama
Jun 17 · Group L
1 - 0	1 - 0	3
England vs Croatia
Jun 17 · Group L
2 - 1	4 - 2	1
Portugal vs DR Congo
Jun 17 · Group K
3 - 0	1 - 1	0
Austria vs Jordan
Jun 17 · Group J
2 - 0	3 - 1	1
Argentina vs Algeria
Jun 17 · Group J
1 - 0	3 - 0	1
Iraq vs Norway
Jun 16 · Group I
0 - 1	1 - 4	1
France vs Senegal
Jun 16 · Group I
1 - 1	3 - 1	0
Iran vs New Zealand
Jun 16 · Group G
1 - 0	2 - 2	0
Saudi Arabia vs Uruguay
Jun 15 · Group H
0 - 2	1 - 1	0
Belgium vs Egypt
Jun 15 · Group G
2 - 1	1 - 1	0
Spain vs Cape Verde
Jun 15 · Group H
2 - 0	0 - 0	0
Sweden vs Tunisia
Jun 15 · Group F
1 - 1	5 - 1	0
Ivory Coast vs Ecuador
Jun 14 · Group E
1 - 0	1 - 0	3
Netherlands vs Japan
Jun 14 · Group F
2 - 1	2 - 2	0
Germany vs Curacao
Jun 14 · Group E
2 - 0	7 - 1	1
Australia vs Turkey
Jun 14 · Group D
0 - 1	2 - 0	0
Haiti vs Scotland
Jun 14 · Group C
0 - 2	0 - 1	1
Brazil vs Morocco
Jun 13 · Group C
2 - 1	1 - 1	0
Qatar vs Switzerland
Jun 13 · Group B
1 - 1	1 - 1	3
USA vs Paraguay
Jun 13 · Group D
2 - 2	4 - 1	0
Canada vs Bosnia & Herzegovina
Jun 12 · Group B
1 - 0	1 - 1	0
South Korea vs Czech Republic
Jun 12 · Group A
1 - 1	2 - 1	0
Mexico vs South Africa
Jun 11 · Group A
2 - 0	2 - 0	3

📊 100kila's Predictions
Total Points
34
Earned
34
Scored Predictions
40
Match	Prediction	Result	Points
New Zealand vs Egypt
Jun 22 · Group G
0 - 1	1 - 3	1
Uruguay vs Cape Verde
Jun 21 · Group H
2 - 0	2 - 2	0
Belgium vs Iran
Jun 21 · Group G
1 - 0	0 - 0	0
Spain vs Saudi Arabia
Jun 21 · Group H
4 - 1	4 - 0	1
Tunisia vs Japan
Jun 21 · Group F
1 - 3	0 - 4	1
Ecuador vs Curacao
Jun 21 · Group E
0 - 0	0 - 0	3
Germany vs Ivory Coast
Jun 20 · Group E
1 - 0	2 - 1	1
Netherlands vs Sweden
Jun 20 · Group F
1 - 0	5 - 1	1
Turkey vs Paraguay
Jun 20 · Group D
0 - 0	0 - 1	0
Brazil vs Haiti
Jun 20 · Group C
4 - 0	3 - 0	1
Scotland vs Morocco
Jun 19 · Group C
0 - 1	0 - 1	3
USA vs Australia
Jun 19 · Group D
1 - 0	2 - 0	1
Mexico vs South Korea
Jun 19 · Group A
2 - 0	1 - 0	1
Canada vs Qatar
Jun 18 · Group B
2 - 0	6 - 0	1
Switzerland vs Bosnia & Herzegovina
Jun 18 · Group B
2 - 0	4 - 1	1
Czech Republic vs South Africa
Jun 18 · Group A
2 - 0	1 - 1	0
Uzbekistan vs Colombia
Jun 18 · Group K
0 - 2	1 - 3	1
Ghana vs Panama
Jun 17 · Group L
2 - 1	1 - 0	1
England vs Croatia
Jun 17 · Group L
2 - 1	4 - 2	1
Portugal vs DR Congo
Jun 17 · Group K
4 - 0	1 - 1	0
Austria vs Jordan
Jun 17 · Group J
4 - 0	3 - 1	1
Argentina vs Algeria
Jun 17 · Group J
4 - 0	3 - 0	1
Iraq vs Norway
Jun 16 · Group I
0 - 3	1 - 4	1
France vs Senegal
Jun 16 · Group I
3 - 0	3 - 1	1
Iran vs New Zealand
Jun 16 · Group G
2 - 0	2 - 2	0
Saudi Arabia vs Uruguay
Jun 15 · Group H
0 - 4	1 - 1	0
Belgium vs Egypt
Jun 15 · Group G
3 - 0	1 - 1	0
Spain vs Cape Verde
Jun 15 · Group H
3 - 0	0 - 0	0
Sweden vs Tunisia
Jun 15 · Group F
3 - 1	5 - 1	1
Ivory Coast vs Ecuador
Jun 14 · Group E
2 - 2	1 - 0	0
Netherlands vs Japan
Jun 14 · Group F
2 - 2	2 - 2	3
Germany vs Curacao
Jun 14 · Group E
3 - 1	7 - 1	1
Australia vs Turkey
Jun 14 · Group D
3 - 1	2 - 0	1
Haiti vs Scotland
Jun 14 · Group C
0 - 2	0 - 1	1
Brazil vs Morocco
Jun 13 · Group C
2 - 0	1 - 1	0
Qatar vs Switzerland
Jun 13 · Group B
0 - 2	1 - 1	0
USA vs Paraguay
Jun 13 · Group D
2 - 1	4 - 1	1
Canada vs Bosnia & Herzegovina
Jun 12 · Group B
2 - 1	1 - 1	0
South Korea vs Czech Republic
Jun 12 · Group A
1 - 1	2 - 1	0
Mexico vs South Africa
Jun 11 · Group A
2 - 0	2 - 0	3


---

how would we predict better the rest: Argentina
vs
Austria
📅 Jun 22, 08:00 PM
Group J
⏰ 9h 41m left
📊 Odds: 1.61 | 3.71 | 5.49
Predict
France
vs
Iraq
📅 Jun 23, 12:00 AM
Group I
⏰ 13h 41m left
📊 Odds: 1.11 | 8.06 | 24.06
Predict
Norway
vs
Senegal
📅 Jun 23, 03:00 AM
Group I
⏰ 16h 41m left
📊 Odds: 2.09 | 3.51 | 3.28
Predict
Jordan
vs
Algeria
📅 Jun 23, 06:00 AM
Group J
⏰ 19h 41m left
📊 Odds: 6.2 | 4.17 | 1.48
Predict
Portugal
vs
Uzbekistan
📅 Jun 23, 08:00 PM
Group K
⏰ 1d 9h 41m left
📊 Odds: 1.21 | 6.31 | 10.82
Predict
England
vs
Ghana
📅 Jun 23, 11:00 PM
Group L
⏰ 1d 12h 41m left
📊 Odds: 1.29 | 5.32 | 8.93
Predict
Panama
vs
Croatia
📅 Jun 24, 02:00 AM
Group L
⏰ 1d 15h 41m left
📊 Odds: 6.29 | 3.68 | 1.55
Predict
Colombia
vs
DR Congo
📅 Jun 24, 05:00 AM
Group K
⏰ 1d 18h 41m left
📊 Odds: 1.43 | 4.23 | 7.22
Predict
Switzerland
vs
Canada
📅 Jun 24, 10:00 PM
Group B
⏰ 2d 11h 41m left
📊 Odds: 2.1 | 3.33 | 3.44
Predict
Bosnia & Herzegovina
vs
Qatar
📅 Jun 24, 10:00 PM
Group B
⏰ 2d 11h 41m left
📊 Odds: 1.62 | 3.64 | 5.49
Predict
Morocco
vs
Haiti
📅 Jun 25, 01:00 AM
Group C
⏰ 2d 14h 41m left
📊 Odds: 1.3 | 5.06 | 9.14
Predict
Scotland
vs
Brazil
📅 Jun 25, 01:00 AM
Group C
⏰ 2d 14h 41m left
📊 Odds: 5.37 | 4.82 | 1.47
Predict
South Africa
vs
South Korea
📅 Jun 25, 04:00 AM
Group A
⏰ 2d 17h 41m left
📊 Odds: 4.03 | 3.35 | 1.92
Predict
Czech Republic
vs
Mexico
📅 Jun 25, 04:00 AM
Group A
⏰ 2d 17h 41m left
📊 Odds: 4.54 | 3.56 | 1.75
Predict
Curacao
vs
Ivory Coast
📅 Jun 25, 11:00 PM
Group E
⏰ 3d 12h 41m left
Predict
Ecuador
vs
Germany
📅 Jun 25, 11:00 PM
Group E
⏰ 3d 12h 41m left
📊 Odds: 4.5 | 3.7 | 1.73
Predict
Tunisia
vs
Netherlands
📅 Jun 26, 02:00 AM
Group F
⏰ 3d 15h 41m left
📊 Odds: 6.28 | 4.22 | 1.47
Predict
Japan
vs
Sweden
📅 Jun 26, 02:00 AM
Group F
⏰ 3d 15h 41m left
📊 Odds: 2.08 | 3.37 | 3.47
Predict
Turkey
vs
USA
📅 Jun 26, 05:00 AM
Group D
⏰ 3d 18h 41m left
📊 Odds: 2.56 | 3.52 | 2.56
Predict
Paraguay
vs
Australia
📅 Jun 26, 05:00 AM
Group D
⏰ 3d 18h 41m left
📊 Odds: 2.12 | 3.17 | 3.57
Predict
Norway
vs
France
📅 Jun 26, 10:00 PM
Group I
⏰ 4d 11h 41m left
📊 Odds: 4.16 | 3.54 | 1.83
Predict
Senegal
vs
Iraq
📅 Jun 26, 10:00 PM
Group I
⏰ 4d 11h 41m left
📊 Odds: 1.38 | 4.55 | 7.6
Predict
Cape Verde
vs
Saudi Arabia
📅 Jun 27, 03:00 AM
Group H
⏰ 4d 16h 41m left
📊 Odds: 2.52 | 3.27 | 2.75
Predict
Uruguay
vs
Spain
📅 Jun 27, 03:00 AM
Group H
⏰ 4d 16h 41m left
📊 Odds: 5.15 | 3.86 | 1.61
Predict
New Zealand
vs
Belgium
📅 Jun 27, 06:00 AM
Group G
⏰ 4d 19h 41m left
📊 Odds: 9.66 | 5.73 | 1.25
Predict
Egypt
vs
Iran
📅 Jun 27, 06:00 AM
Group G
⏰ 4d 19h 41m left
📊 Odds: 2.22 | 2.99 | 3.55
Predict
Panama
vs
England
📅 Jun 28, 12:00 AM
Group L
⏰ 5d 13h 41m left
📊 Odds: 7.56 | 6.38 | 1.27
Predict
Croatia
vs
Ghana
📅 Jun 28, 12:00 AM
Group L
⏰ 5d 13h 41m left
📊 Odds: 1.6 | 3.78 | 5.51
Predict
Colombia
vs
Portugal
📅 Jun 28, 02:30 AM
Group K
⏰ 5d 16h 11m left
📊 Odds: 3.46 | 3.27 | 2.12
Predict
DR Congo
vs
Uzbekistan
📅 Jun 28, 02:30 AM
Group K
⏰ 5d 16h 11m left
📊 Odds: 2.29 | 3.32 | 3.05
Predict
Algeria
vs
Austria
📅 Jun 28, 05:00 AM
Group J
⏰ 5d 18h 41m left
📊 Odds: 3.74 | 3.03 | 2.13
Predict
Jordan
vs
Argentina
📅 Jun 28, 05:00 AM
Group J
⏰ 5d 18h 41m left
📊 Odds: 13.33 | 7.12 | 1.16
Predict

---

# chatgpt response

I’ll use this as a real forecasting update now: not just odds, but group motivation, score patterns so far, and what the leaders’ picks reveal about their style.

You’re very close. The leaders are not doing anything magical — they are mostly using **base-rate scores** like **2–0, 2–1, 1–0, 0–1**, with a few exact hits. Missing **New Zealand–Egypt** probably cost you only **1 point** versus both leaders, because both had Egypt outcome right but not exact.

For the rest, don’t go crazy chasing. We need **mostly safe outcomes**, with a few smart draw/differential picks. ESPN’s current schedule/results confirms this is now moving into the decisive second/third group games, where motivation and rotation matter more. ([ESPN](https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket?utm_source=chatgpt.com)) Reuters also notes Norway’s strong 4–1 start but warns Senegal are dangerous, which is exactly the type of match where we should avoid overconfidence. ([Reuters](https://www.reuters.com/sports/soccer/solbakken-wary-senegal-threat-norway-look-build-flying-start-2026-06-22/?utm_source=chatgpt.com))

## Enter these now

| Match | Pick | Confidence |
|---|---:|---|
| Argentina vs Austria | **2–1** | Medium-high |
| France vs Iraq | **3–1** | High |
| Norway vs Senegal | **2–1** | Medium |
| Jordan vs Algeria | **1–2** | Medium |
| Portugal vs Uzbekistan | **3–1** | High |
| England vs Ghana | **3–1** | High |
| Panama vs Croatia | **0–2** | Medium-high |
| Colombia vs DR Congo | **2–1** | Medium-high |

The most important ones here: **France 3–1**, **Portugal 3–1**, **England 3–1**, **Colombia 2–1**.

## Provisional picks for the rest

Only input these now if the app forces you. If you can wait, we should revisit because final group matches depend heavily on qualification scenarios.

| Match | Pick | Confidence |
|---|---:|---|
| Switzerland vs Canada | **1–1** | Low-medium |
| Bosnia & Herzegovina vs Qatar | **2–1** | Medium |
| Morocco vs Haiti | **2–0** | High |
| Scotland vs Brazil | **0–2** | Medium-high |
| South Africa vs South Korea | **1–2** | Medium |
| Czech Republic vs Mexico | **1–1** | Low |
| Curacao vs Ivory Coast | **0–1** | Manual/medium |
| Ecuador vs Germany | **1–2** | Medium |
| Tunisia vs Netherlands | **1–3** | High |
| Japan vs Sweden | **2–2** | Low-medium |
| Turkey vs USA | **1–1** | Low |
| Paraguay vs Australia | **1–1** | Low |
| Norway vs France | **1–2** | Medium |
| Senegal vs Iraq | **3–1** | High |
| Cape Verde vs Saudi Arabia | **1–1** | Low |
| Uruguay vs Spain | **1–2** | Medium |
| New Zealand vs Belgium | **1–2** | Medium |
| Egypt vs Iran | **1–1** | Low-medium |
| Panama vs England | **0–3** | High |
| Croatia vs Ghana | **2–1** | Medium |
| Colombia vs Portugal | **1–1** | Low-medium |
| DR Congo vs Uzbekistan | **2–1** | Low-medium |
| Algeria vs Austria | **1–2** | Medium |
| Jordan vs Argentina | **0–3** | High |

## Why this version should be better

The leaders are scoring because they are not overcomplicating. They pick the favourite, usually with a normal exact score. So we should not try to be “genius” everywhere.

The improved logic:

| Situation | New default |
|---|---:|
| Strong favourite, opponent can score | **3–1** |
| Strong favourite, weak opponent | **3–0** |
| Medium favourite | **2–1** |
| Close group-decider | **1–1** |
| Away favourite | **1–2** |
| Defensive mismatch | **0–2** |

So for this batch, I’d lock:

**Argentina 2–1 Austria**  
**France 3–1 Iraq**  
**Norway 2–1 Senegal**  
**Jordan 1–2 Algeria**  
**Portugal 3–1 Uzbekistan**  
**England 3–1 Ghana**  
**Panama 0–2 Croatia**  
**Colombia 2–1 DR Congo**

---

# you asked

message time: 2026-06-25 00:30:02

give me for those:
Morocco
vs
Haiti
📅 25 Jun, 01:00
Group C
⏰ 32m left
📊 Odds: 1.3 | 5.06 | 9.14
Predict
Scotland
vs
Brazil
📅 25 Jun, 01:00
Group C
⏰ 32m left
📊 Odds: 5.37 | 4.82 | 1.47
Predict
South Africa
vs
South Korea
📅 25 Jun, 04:00
Group A
⏰ 3h 32m left
📊 Odds: 4.03 | 3.35 | 1.92
Predict
Czech Republic
vs
Mexico
📅 25 Jun, 04:00
Group A
⏰ 3h 32m left
📊 Odds: 4.54 | 3.56 | 1.75
Predict

---
Vandal who's winning predictions so far
 Vandal's Predictions
Total Points
46
Earned
46
Scored Predictions
48
Match	Prediction	Result	Points
Colombia vs DR Congo
Jun 24 · Group K
2 - 1	1 - 0	1
Panama vs Croatia
Jun 23 · Group L
0 - 2	0 - 1	1
England vs Ghana
Jun 23 · Group L
2 - 1	0 - 0	0
Portugal vs Uzbekistan
Jun 23 · Group K
2 - 0	5 - 0	1
Jordan vs Algeria
Jun 23 · Group J
1 - 2	1 - 2	3
Norway vs Senegal
Jun 23 · Group I
1 - 1	3 - 2	0
France vs Iraq
Jun 22 · Group I
3 - 0	3 - 0	3
Argentina vs Austria
Jun 22 · Group J
2 - 0	2 - 0	3
New Zealand vs Egypt
Jun 22 · Group G
0 - 1	1 - 3	1
Uruguay vs Cape Verde
Jun 21 · Group H
2 - 0	2 - 2	0
Belgium vs Iran
Jun 21 · Group G
2 - 1	0 - 0	0
Spain vs Saudi Arabia
Jun 21 · Group H
2 - 0	4 - 0	1
Tunisia vs Japan
Jun 21 · Group F
0 - 2	0 - 4	1
Ecuador vs Curacao
Jun 21 · Group E
2 - 0	0 - 0	0
Germany vs Ivory Coast
Jun 20 · Group E
2 - 0	2 - 1	1
Netherlands vs Sweden
Jun 20 · Group F
2 - 1	5 - 1	1
Turkey vs Paraguay
Jun 20 · Group D
1 - 0	0 - 1	0
Brazil vs Haiti
Jun 20 · Group C
3 - 0	3 - 0	3
Scotland vs Morocco
Jun 19 · Group C
0 - 1	0 - 1	3
USA vs Australia
Jun 19 · Group D
2 - 1	2 - 0	1
Mexico vs South Korea
Jun 19 · Group A
2 - 1	1 - 0	1
Canada vs Qatar
Jun 18 · Group B
1 - 0	6 - 0	1
Switzerland vs Bosnia & Herzegovina
Jun 18 · Group B
2 - 1	4 - 1	1
Czech Republic vs South Africa
Jun 18 · Group A
1 - 0	1 - 1	0
Uzbekistan vs Colombia
Jun 18 · Group K
0 - 1	1 - 3	1
Ghana vs Panama
Jun 17 · Group L
1 - 0	1 - 0	3
England vs Croatia
Jun 17 · Group L
2 - 1	4 - 2	1
Portugal vs DR Congo
Jun 17 · Group K
3 - 0	1 - 1	0
Austria vs Jordan
Jun 17 · Group J
2 - 0	3 - 1	1
Argentina vs Algeria
Jun 17 · Group J
1 - 0	3 - 0	1
Iraq vs Norway
Jun 16 · Group I
0 - 1	1 - 4	1
France vs Senegal
Jun 16 · Group I
1 - 1	3 - 1	0
Iran vs New Zealand
Jun 16 · Group G
1 - 0	2 - 2	0
Saudi Arabia vs Uruguay
Jun 15 · Group H
0 - 2	1 - 1	0
Belgium vs Egypt
Jun 15 · Group G
2 - 1	1 - 1	0
Spain vs Cape Verde
Jun 15 · Group H
2 - 0	0 - 0	0
Sweden vs Tunisia
Jun 15 · Group F
1 - 1	5 - 1	0
Ivory Coast vs Ecuador
Jun 14 · Group E
1 - 0	1 - 0	3
Netherlands vs Japan
Jun 14 · Group F
2 - 1	2 - 2	0
Germany vs Curacao
Jun 14 · Group E
2 - 0	7 - 1	1
Australia vs Turkey
Jun 14 · Group D
0 - 1	2 - 0	0
Haiti vs Scotland
Jun 14 · Group C
0 - 2	0 - 1	1
Brazil vs Morocco
Jun 13 · Group C
2 - 1	1 - 1	0
Qatar vs Switzerland
Jun 13 · Group B
1 - 1	1 - 1	3
USA vs Paraguay
Jun 13 · Group D
2 - 2	4 - 1	0
Canada vs Bosnia & Herzegovina
Jun 12 · Group B
1 - 0	1 - 1	0
South Korea vs Czech Republic
Jun 12 · Group A
1 - 1	2 - 1	0
Mexico vs South Africa
Jun 11 · Group A
2 - 0	2 - 0	3

---

# chatgpt response

I’ll optimize these four as “late group-stage” picks: use the odds, but also infer motivation from the results you pasted. Vandal’s style is conservative, so we need one or two smart differentials, not wild guesses.

For these four, I’d enter **now**:

| Match | Pick | Confidence | Reason |
|---|---:|---|---|
| Morocco vs Haiti | **2–0** | High | Morocco are clearly stronger, but they are more controlled than explosive. Haiti lost 0–1 to Scotland and 0–3 to Brazil, so **2–0** is the clean base-rate pick. Fox notes Morocco drew Brazil and beat Scotland, while Haiti lost both opening matches. ([FOX Sports](https://www.foxsports.com/stories/soccer/how-to-watch-morocco-vs-haiti-tv-channel-live-stream-2026-fifa-world-cup-group-c?utm_source=chatgpt.com)) |
| Scotland vs Brazil | **0–2** | Medium-high | Brazil should win, but they have not looked fully convincing. I would not go 0–3 unless chasing. The Guardian reports skepticism around Brazil’s performances despite their quality. ([The Guardian](https://www.theguardian.com/football/2026/jun/24/view-brazil-scotland-neymar-casemiro-endrick-world-cup-2026?utm_source=chatgpt.com)) |
| South Africa vs South Korea | **1–1** | Low-medium | South Korea can qualify with a draw, while South Africa must win; that creates a classic tense 1–1 setup. Group A scenarios say South Korea advance with a win or draw, while South Africa need a win plus help. ([SB Nation](https://www.sbnation.com/fifa-world-cup/1118965/world-cup-2026-what-are-the-scenarios-for-group-a?utm_source=chatgpt.com)) |
| Czech Republic vs Mexico | **0–1** | Medium | Mexico already secured top spot, so rotation risk exists, but they are still the better side. Czechia need a win, which may open space late. ([SB Nation](https://www.sbnation.com/fifa-world-cup/1118965/world-cup-2026-what-are-the-scenarios-for-group-a?utm_source=chatgpt.com)) |

## My actual entries

**Morocco 2–0 Haiti**  
**Scotland 0–2 Brazil**  
**South Africa 1–1 South Korea**  
**Czech Republic 0–1 Mexico**

If you are behind Vandal and need differentials, only change one:

| Safer | Chasing version |
|---|---:|
| South Africa 1–1 South Korea | **South Africa 1–2 South Korea** |

I’d personally keep **1–1** because South Korea only need a draw, and these final group games often become tactical.

---

# you asked

message time: 2026-06-25 00:32:15

how does vandal have so many correct predictions

---

# chatgpt response

Because Vandal is not necessarily “predicting better” in a deep football sense — he is using the **best exact-score fantasy strategy** more consistently:

> **Pick the favourite, use boring common scores, and don’t overthink.**

Looking at his 48 scored predictions:

| Vandal metric | Count |
|---|---:|
| Exact scores | **9** |
| Correct outcome but not exact | **19** |
| Misses | **20** |
| Total points | **46** |

So he is not magically accurate on every match. He has **20 misses**. But the scoring system rewards exact hits heavily, and he got enough of those.

## His winning pattern

Most of his exacts came from very common football scores:

| Match | Vandal pick | Result |
|---|---:|---:|
| Mexico vs South Africa | 2–0 | 2–0 |
| Qatar vs Switzerland | 1–1 | 1–1 |
| Ivory Coast vs Ecuador | 1–0 | 1–0 |
| Ghana vs Panama | 1–0 | 1–0 |
| Scotland vs Morocco | 0–1 | 0–1 |
| Brazil vs Haiti | 3–0 | 3–0 |
| Argentina vs Austria | 2–0 | 2–0 |
| France vs Iraq | 3–0 | 3–0 |
| Jordan vs Algeria | 1–2 | 1–2 |

These are not exotic predictions. They are mostly:

**1–0, 0–1, 2–0, 3–0, 1–1, 1–2**

That’s the whole trick.

## What he does better than us

We sometimes tried to adapt too much to “chaos”:

- Belgium vs Iran: we picked **2–1**, actual **0–0**
- Netherlands vs Sweden: we picked **2–2**, actual **5–1**
- Scotland vs Morocco: we picked **1–1**, actual **0–1**
- Ghana vs Panama earlier: we picked **1–1**, actual **1–0**

Vandal often just picks the boring favourite score:

- Scotland vs Morocco: **0–1**
- Ghana vs Panama: **1–0**
- France vs Iraq: **3–0**
- Argentina vs Austria: **2–0**

He is not chasing “story”; he is playing the scoring system.

## Main lesson

For this game, the optimal style is probably:

| Situation | Best default |
|---|---:|
| Heavy favourite | **3–0** or **2–0** |
| Strong favourite | **2–0** or **2–1** |
| Slight favourite | **1–0** |
| Away slight favourite | **0–1** |
| Close match | **1–1** |
| Underdog likely to score | **2–1 / 1–2** |

Vandal’s edge is that he stays inside this range almost all the time. He does not predict many **2–2s**, **3–1s**, or complicated outcomes unless needed.

## What we should do now

To catch him, don’t become wild. Use his base-rate logic, but choose **a few spots where he likely goes boring** and we choose a smart alternative.

For example:

| If Vandal likely picks | We can sometimes pick |
|---|---:|
| 2–0 favourite | **2–1** |
| 1–0 favourite | **1–1** |
| 0–1 away favourite | **0–2** |
| 3–0 heavy favourite | **4–0** only rarely |

But 80% of picks should stay boring. That’s why the initial logic gave us exacts too.

---

# you asked

message time: 2026-06-25 00:33:52

so follow his logic for next matches

---

# chatgpt response

Yes — for the next matches, we should **mostly follow Vandal’s logic**, because it fits this scoring system better.

Not because he knows more football, but because he is playing the **exact-score base rates** well:

**1–0, 0–1, 2–0, 2–1, 0–2, 1–1, 3–0**

That’s where most exact-score points come from.

## Updated rule

| Match type | Pick style |
|---|---:|
| Huge favourite | **3–0** |
| Strong favourite | **2–0** |
| Strong favourite but opponent can score | **2–1** |
| Slight favourite | **1–0** |
| Away favourite | **0–1** |
| Close match | **1–1** |
| Need differential | only tweak one goal |

So yes: **less 2–2, less 3–1, less overthinking.**

## For the four urgent matches

I’d slightly adjust to be more Vandal-like:

| Match | Previous idea | Vandal-style final |
|---|---:|---:|
| Morocco vs Haiti | 2–0 | **2–0** |
| Scotland vs Brazil | 0–2 | **0–2** |
| South Africa vs South Korea | 1–1 | **0–1** |
| Czech Republic vs Mexico | 0–1 | **0–1** |

So enter:

**Morocco 2–0 Haiti**  
**Scotland 0–2 Brazil**  
**South Africa 0–1 South Korea**  
**Czech Republic 0–1 Mexico**

The only one I’m changing from my previous list is **South Africa–South Korea: 1–1 → 0–1**. If we follow Vandal’s logic, slight away favourite usually becomes **0–1**, not a tactical draw.