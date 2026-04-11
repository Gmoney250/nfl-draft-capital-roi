# NFL Draft Capital ROI Analysis — Full Project Write-Up

---

## 1. PROJECT TITLE

**NFL Draft Capital ROI: Quantifying Return on Investment by Draft Position, Round, and Position Group (2013–2024)**

---

## 2. QUICK SUMMARY

This project analyzes 61 NFL players drafted between 2013 and 2024 to measure which draft positions deliver the best return on investment by comparing player production (Career Approximate Value) against rookie contract cost. The analysis reveals that late-round picks deliver 8–20x more value per dollar than top-5 picks, that the quarterback position shows the most extreme ROI disparity in the entire draft, and that mid-round tight ends and linebackers represent the most consistently efficient investments. These findings mirror real-world principles in venture capital and talent acquisition — the most expensive assets aren't always the best investments.

---

## 3. PROBLEM / IDEA

NFL teams spend tens of millions of dollars on rookie contracts, with first overall picks commanding 10x the guaranteed money of fourth-round selections. But does paying more for draft position actually translate to proportionally better performance? This is the same question investors ask when evaluating high-priced stocks versus undervalued ones: **is the premium justified by the return?**

This matters because every NFL franchise operates under a hard salary cap. Teams that extract more production per dollar from their draft picks can spend the savings elsewhere — creating a compounding competitive advantage. The same logic applies in business: companies that hire efficiently (finding high-output talent at below-market cost) outperform those that overpay for brand-name credentials.

---

## 4. DATASET

See `nfl_draft_roi_data.csv` — 61 players, 14 columns, spanning draft classes from 2013 to 2024 across 10 NFL position groups.

---

## 5. ANALYSIS (RESULTS)

### By Draft Round

| Round | Players | Avg AV | Avg Cost ($M) | AV/$M | Avg Pro Bowls |
|-------|---------|--------|----------------|-------|---------------|
| 1     | 42      | 25.9   | 24.5           | 1.19  | 0.69          |
| 2     | 4       | 30.5   | 9.2            | 3.82  | 1.50          |
| 3     | 6       | 38.2   | 5.9            | 6.26  | 1.33          |
| 4     | 3       | 51.3   | 4.5            | 12.29 | 2.00          |
| 5     | 5       | 34.8   | 3.9            | 9.41  | 1.80          |
| 7     | 1       | 42.0   | 3.7            | 11.35 | 1.00          |

### By Pick Tier

| Tier           | N  | Avg AV | Avg Cost | AV/$M | Hit Rate |
|----------------|----|--------|----------|-------|----------|
| Top 5          | 13 | 24.5   | 35.1     | 0.71  | 61.5%    |
| 6-15           | 16 | 29.6   | 23.2     | 1.30  | 56.2%    |
| 16-32          | 13 | 22.6   | 15.3     | 1.54  | 30.8%    |
| 33-70 (Rd 2-3) | 9 | 37.0   | 7.5      | 5.49  | 55.6%    |
| 71-145 (Rd 3-5)| 5 | 36.4   | 4.5      | 8.56  | 60.0%    |
| 146+ (Rd 5-7)  | 5 | 41.2   | 3.8      | 11.19 | 100.0%   |

### Top 5 Value Picks (Efficiency Score)

1. **Dak Prescott** (Rd 4, Pick 135) — 19.43 AV/$M, Efficiency: 29.44
2. **Tyreek Hill** (Rd 5, Pick 165) — 17.57 AV/$M, Efficiency: 28.63
3. **George Kittle** (Rd 5, Pick 146) — 16.18 AV/$M, Efficiency: 25.19
4. **Brock Purdy** (Rd 7, Pick 262) — 11.35 AV/$M, Efficiency: 22.70
5. **Travis Kelce** (Rd 3, Pick 63) — 13.71 AV/$M, Efficiency: 17.01

### QB Value Comparison

Late-round QBs delivered **20x more value per dollar** than top-5 QBs on their rookie contracts. Dak Prescott's 19.43 AV/$M dwarfs Caleb Williams' 0.35 and Bryce Young's 0.32.

---

## 6. WHAT THE PROJECT FOUND

1. **Late-round picks are dramatically more capital-efficient.** Rounds 4-7 averaged 9.4–12.3 AV per million dollars, while Round 1 averaged just 1.19 AV/$M. The cheapest picks produce the most value relative to their cost.

2. **Top-5 draft picks are the worst investment tier.** Despite having the highest hit rate (61.5%), their cost efficiency (0.71 AV/$M) is the lowest in the draft. You're paying a massive premium for only marginal improvement in hit probability.

3. **The QB market is wildly inefficient.** Late-round quarterbacks like Prescott and Purdy generated elite production at a fraction of the cost. Top-5 QBs averaged just 0.49 AV/$M — the worst of any position/tier combination.

4. **Tight ends drafted in Rounds 2-5 are hidden gems.** TEs led all positions in AV/$M (6.77), suggesting the position is systematically undervalued in early rounds.

5. **EDGE and CB are the riskiest first-round bets per dollar.** These positions showed the widest spread between best and worst outcomes, making them the most volatile investments.

---

## 7. TEACH ME HOW IT WORKS

### What Is "Approximate Value" (AV)?

AV is a metric created by Pro Football Reference that assigns a single number to every player's season. It tries to capture total contribution — touchdowns, tackles, wins, everything — in one comparable number. Think of it like a player's "stock price" for their career output. A career AV of 50+ is very strong; 80+ is borderline Hall of Fame territory.

### What Is "AV Per Million" (AV/$M)?

This is the core ROI metric. It divides a player's total career production (AV) by their rookie contract cost (in millions). If a player has 50 AV and cost $5M, their AV/$M is 10.0 — meaning you got 10 units of production for every million you spent. Higher is better. This is exactly like calculating "earnings per dollar invested" in finance.

### What Is the "Efficiency Score"?

Raw AV/$M slightly favors late picks just because they're cheap. To make it fairer, the Efficiency Score multiplies AV/$M by a pick-position weight: `1 + (pick / 262)`. This means a 7th-round pick at #262 gets a 2x multiplier, while a #1 pick gets almost no bonus. This captures true *surplus value* — production you got that the market didn't expect.

### What Is "Hit Rate"?

Hit rate is the percentage of players in a tier that reached a Career AV of 20 or higher. It measures how often a draft tier produces a "useful starter-level player." A 60% hit rate means 6 out of 10 picks became meaningful contributors.

### Why Does This Analysis Matter?

Think about it like investing. If you have $100M to build a portfolio, do you put it all into one expensive stock (a top-5 pick), or diversify into many undervalued picks? This analysis shows that the "diversified, undervalued" strategy produces far more total value per dollar — just like index investing often beats picking individual expensive stocks.

### What To Look For Next Time

When you build a project like this, the key analytical move is: **find the ratio between cost and output, then slice it by every category you can.** Round, pick tier, position, year — each slice reveals different patterns. The most interesting findings come from categories where the ratio diverges dramatically (like late-round QBs vs. top-5 QBs). That divergence is where the real insight lives.

---

## 8. PYTHON CODE

See `analysis.py` — fully functional, zero external dependencies, ready to run with `python analysis.py`.

---

## 9. VISUALIZATION IDEAS

### Chart 1: Scatter Plot — Draft Pick vs. AV/$M (Color by Position)
Plot every player as a dot: X-axis = draft pick number, Y-axis = AV per million dollars. Color each dot by position group. You'll see a clear upward curve as later picks cluster at the top (high efficiency) and early picks cluster at the bottom. This is the single most powerful chart for the project — it makes the core finding visual instantly.

### Chart 2: Grouped Bar Chart — AV/$M by Draft Tier
Show 6 bars (one per tier: Top 5, 6-15, 16-32, Rd 2-3, Rd 3-5, Rd 5-7) with the average AV/$M for each. The progressive increase from left to right tells the whole story of draft capital inefficiency in one glance. Add a secondary axis showing hit rate as a line to show the cost/probability tradeoff.

### Chart 3: QB-Specific Bubble Chart — Pick vs. AV, Sized by Contract Value
Plot only QBs: X-axis = pick number, Y-axis = career AV, bubble size = contract value. Dak Prescott and Brock Purdy will appear as small bubbles (cheap) near the top (high AV), while top-5 QBs will be giant bubbles near the bottom. This makes the QB market inefficiency visually undeniable.

---

## 10. README

See `README.md` — polished and GitHub-ready.

---

## 11. EXTENSION IDEA

**Build a Draft Value Prediction Model Using Machine Learning**

Collect NFL Combine data (40-yard dash, vertical jump, bench press, etc.), college stats (yards, touchdowns, awards), and team context (winning percentage, positional need) for every draft pick in the last 15 years. Train a gradient-boosted classifier (XGBoost) to predict whether a pick will become a "hit" (Career AV ≥ 20) based on these pre-draft features. Then combine the predicted hit probability with the known rookie contract cost at each pick slot to build a **Draft Value Calculator** — a tool that tells you the expected ROI of any given pick before the draft happens. This would be a genuinely useful tool that NFL analytics departments actually build, and it combines machine learning, sports analytics, and financial modeling in a single project. You could deploy it as a Streamlit web app where users input a prospect's combine numbers and get an estimated ROI grade.
