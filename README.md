# NFL Draft Capital ROI Analysis
### Measuring Return on Investment by Draft Position and Position Group

## Overview

NFL teams invest heavily in draft capital — the higher the pick, the more expensive the rookie contract. But does spending more draft capital actually guarantee better results? This project quantifies the **return on investment (ROI)** of NFL draft picks by comparing player production (measured by Career Approximate Value) against their rookie contract cost. The analysis spans 61 players drafted between 2013 and 2024 across 10 position groups.

## Objective

To determine which draft rounds, pick tiers, and position groups deliver the highest value per dollar spent on rookie contracts — and to identify systematic inefficiencies in how NFL teams allocate draft capital.

## Dataset

The dataset includes 61 NFL players with the following attributes:

- **Player Info**: Name, team, draft year, round, pick number, position
- **Contract Data**: Total rookie contract value (millions), contract length
- **Performance**: Career Approximate Value (AV), Pro Bowl selections, games played/started, years active

Data reflects realistic career trajectories based on publicly available NFL statistics through the 2024 season.

## Methodology

1. **Cost Per AV Point** — Divides total rookie contract by Career AV to find the dollar cost of each unit of production
2. **AV Per Million** — Inverts the above to measure production per dollar (higher = better)
3. **AV Per Game** — Normalizes production by availability
4. **Draft Capital Efficiency Score** — A composite metric that multiplies AV/$M by a pick-position weight (later picks get a bonus multiplier), capturing true surplus value
5. **Tier Analysis** — Groups picks into meaningful tiers (Top 5, 6-15, 16-32, Rounds 2-3, Rounds 3-5, Rounds 5-7) and compares hit rates and efficiency
6. **Position-Level Breakdown** — Compares ROI across all 10 position groups
7. **QB-Specific Deep Dive** — Isolates the most expensive position to analyze where teams get the best and worst quarterback value

## Key Findings

1. **Late-round picks deliver 8-15x more value per dollar** than first-round picks on their rookie contracts. Rounds 4-7 averaged 10.00-19.43 AV/$M compared to 0.28-5.76 for Round 1.

2. **Top-5 picks have the worst cost efficiency** in the entire draft. Despite a 61.5% hit rate, their average AV/$M (0.71) is the lowest of any tier — they cost far more than the marginal production they provide over cheaper alternatives.

3. **The QB position shows the most extreme ROI disparity.** Late-round QBs (Dak Prescott, Brock Purdy, Lamar Jackson at pick 32) delivered roughly 20x more value per dollar than top-5 QBs on rookie deals.

4. **Tight ends and linebackers drafted in Rounds 2-5 are the most efficient investments**, combining solid hit rates with low contract costs (TE averaged 6.77 AV/$M across the dataset).

5. **EDGE rushers and cornerbacks have the widest ROI variance**, making them the riskiest first-round investments per dollar.

## Why It Matters

Every NFL front office operates under a salary cap. Understanding where draft capital is most efficiently spent — and where the market systematically overpays — is the foundation of sustainable team-building. This same framework (measuring ROI on human capital investment) translates directly to business hiring, venture capital portfolio construction, and any domain where you allocate limited resources to uncertain talent.

## How to Run

```bash
# Clone the repo
git clone https://github.com/yourusername/nfl-draft-capital-roi.git
cd nfl-draft-capital-roi

# Run the analysis (Python 3.6+, no external dependencies)
python analysis.py
```

## Future Improvements

- **Live Data Integration**: Pull real-time player stats from the ESPN or Pro Football Reference API to keep the dataset current
- **Machine Learning Model**: Train a classifier to predict draft pick "hit probability" based on combine metrics, college stats, and draft position
- **Interactive Dashboard**: Build a Streamlit or Plotly Dash app that lets users filter by team, year, and position to explore ROI interactively
- **Salary Cap Optimization**: Extend the analysis into a linear programming model that recommends optimal draft strategies given cap constraints
- **Historical Comparison**: Compare draft efficiency across decades to see if teams have gotten smarter over time

## Tech Stack

- Python 3 (standard library only — `csv`, `statistics`, `collections`)
- No external dependencies required

## License

MIT
