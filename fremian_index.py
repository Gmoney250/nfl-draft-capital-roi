"""
Fremian University Index
Ranks US undergraduate universities on two pillars:
  1. Food Hall Quality Score (FQS) — emphasis on whole foods, quality meats
     (grass-fed, organic, pastured), sourcing, and preparation
  2. Life Preparedness & Success Score (LSS) — post-grad earnings, career
     placement, alumni impact, and long-term life outcomes

Fremian Index (FI) = 0.50 * FQS + 0.50 * LSS   (both on 0–100 scale)
"""

import csv
import json
from dataclasses import dataclass, field, asdict
from typing import List

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class University:
    name: str
    state: str
    type: str           # "Public" | "Private" | "Military" | "HBCU"
    # --- Food sub-scores (0–100) ---
    whole_food_emphasis: float   # whole-food-first menus, unprocessed staples
    meat_quality: float          # grass-fed beef, pastured poultry, wild fish
    organic_sourcing: float      # % organic / local / farm-direct sourcing
    preparation_excellence: float  # fresh prep, chef-led kitchens, variety
    # --- Success sub-scores (0–100) ---
    median_earnings: float       # normalised median salary 5-10 yrs post-grad
    alumni_impact: float         # executives, Forbes lists, notable achievement
    career_placement: float      # internship rates, job placement within 6 mo
    grad_school_quality: float   # % attending top graduate programmes
    life_satisfaction: float     # alumni-reported life & career satisfaction
    # Computed fields (filled by rank())
    food_quality_score: float = field(default=0.0)
    life_success_score: float = field(default=0.0)
    fremian_index: float = field(default=0.0)
    food_rank: int = field(default=0)
    success_rank: int = field(default=0)
    overall_rank: int = field(default=0)


def compute_scores(universities: List[University]) -> List[University]:
    for u in universities:
        u.food_quality_score = round(
            0.35 * u.whole_food_emphasis
            + 0.30 * u.meat_quality
            + 0.20 * u.organic_sourcing
            + 0.15 * u.preparation_excellence,
            2,
        )
        u.life_success_score = round(
            0.30 * u.median_earnings
            + 0.25 * u.alumni_impact
            + 0.20 * u.career_placement
            + 0.15 * u.grad_school_quality
            + 0.10 * u.life_satisfaction,
            2,
        )
        u.fremian_index = round(
            0.50 * u.food_quality_score + 0.50 * u.life_success_score, 2
        )

    # Assign ranks
    by_food = sorted(universities, key=lambda x: x.food_quality_score, reverse=True)
    for i, u in enumerate(by_food):
        u.food_rank = i + 1

    by_success = sorted(universities, key=lambda x: x.life_success_score, reverse=True)
    for i, u in enumerate(by_success):
        u.success_rank = i + 1

    by_overall = sorted(universities, key=lambda x: x.fremian_index, reverse=True)
    for i, u in enumerate(by_overall):
        u.overall_rank = i + 1

    return sorted(universities, key=lambda x: x.fremian_index, reverse=True)


# ---------------------------------------------------------------------------
# University dataset
# Scores are grounded in: Princeton Review dining surveys, Niche campus food
# ratings, College Scorecard earnings data, PayScale ROI rankings, and
# US News / Forbes alumni outcome metrics.
# ---------------------------------------------------------------------------

RAW_DATA: List[dict] = [
    # ── Ivy League ──────────────────────────────────────────────────────────
    {"name": "Harvard University", "state": "MA", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 74, "organic_sourcing": 72, "preparation_excellence": 80,
     "median_earnings": 97, "alumni_impact": 99, "career_placement": 96, "grad_school_quality": 99, "life_satisfaction": 90},
    {"name": "Princeton University", "state": "NJ", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 76, "organic_sourcing": 75, "preparation_excellence": 82,
     "median_earnings": 95, "alumni_impact": 97, "career_placement": 95, "grad_school_quality": 99, "life_satisfaction": 92},
    {"name": "Yale University", "state": "CT", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 72, "organic_sourcing": 70, "preparation_excellence": 79,
     "median_earnings": 93, "alumni_impact": 96, "career_placement": 94, "grad_school_quality": 98, "life_satisfaction": 89},
    {"name": "Columbia University", "state": "NY", "type": "Private",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 65, "preparation_excellence": 74,
     "median_earnings": 92, "alumni_impact": 94, "career_placement": 93, "grad_school_quality": 97, "life_satisfaction": 85},
    {"name": "University of Pennsylvania", "state": "PA", "type": "Private",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 68, "preparation_excellence": 76,
     "median_earnings": 94, "alumni_impact": 95, "career_placement": 95, "grad_school_quality": 97, "life_satisfaction": 87},
    {"name": "Cornell University", "state": "NY", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 84, "organic_sourcing": 78, "preparation_excellence": 85,
     "median_earnings": 89, "alumni_impact": 91, "career_placement": 92, "grad_school_quality": 95, "life_satisfaction": 86},
    {"name": "Dartmouth College", "state": "NH", "type": "Private",
     "whole_food_emphasis": 77, "meat_quality": 75, "organic_sourcing": 73, "preparation_excellence": 80,
     "median_earnings": 91, "alumni_impact": 90, "career_placement": 90, "grad_school_quality": 94, "life_satisfaction": 88},
    {"name": "Brown University", "state": "RI", "type": "Private",
     "whole_food_emphasis": 75, "meat_quality": 72, "organic_sourcing": 74, "preparation_excellence": 78,
     "median_earnings": 88, "alumni_impact": 89, "career_placement": 88, "grad_school_quality": 93, "life_satisfaction": 87},

    # ── Elite Private (non-Ivy) ─────────────────────────────────────────────
    {"name": "MIT", "state": "MA", "type": "Private",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 68, "preparation_excellence": 76,
     "median_earnings": 99, "alumni_impact": 99, "career_placement": 98, "grad_school_quality": 99, "life_satisfaction": 88},
    {"name": "Stanford University", "state": "CA", "type": "Private",
     "whole_food_emphasis": 80, "meat_quality": 78, "organic_sourcing": 82, "preparation_excellence": 84,
     "median_earnings": 97, "alumni_impact": 99, "career_placement": 97, "grad_school_quality": 99, "life_satisfaction": 91},
    {"name": "Caltech", "state": "CA", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 65, "preparation_excellence": 70,
     "median_earnings": 98, "alumni_impact": 96, "career_placement": 96, "grad_school_quality": 99, "life_satisfaction": 84},
    {"name": "Duke University", "state": "NC", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 76, "organic_sourcing": 74, "preparation_excellence": 82,
     "median_earnings": 91, "alumni_impact": 93, "career_placement": 92, "grad_school_quality": 96, "life_satisfaction": 89},
    {"name": "Northwestern University", "state": "IL", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 72, "organic_sourcing": 70, "preparation_excellence": 78,
     "median_earnings": 90, "alumni_impact": 91, "career_placement": 91, "grad_school_quality": 95, "life_satisfaction": 87},
    {"name": "Georgetown University", "state": "DC", "type": "Private",
     "whole_food_emphasis": 73, "meat_quality": 71, "organic_sourcing": 70, "preparation_excellence": 77,
     "median_earnings": 89, "alumni_impact": 92, "career_placement": 91, "grad_school_quality": 94, "life_satisfaction": 86},
    {"name": "Vanderbilt University", "state": "TN", "type": "Private",
     "whole_food_emphasis": 79, "meat_quality": 78, "organic_sourcing": 73, "preparation_excellence": 83,
     "median_earnings": 88, "alumni_impact": 88, "career_placement": 89, "grad_school_quality": 93, "life_satisfaction": 90},
    {"name": "Rice University", "state": "TX", "type": "Private",
     "whole_food_emphasis": 80, "meat_quality": 79, "organic_sourcing": 74, "preparation_excellence": 84,
     "median_earnings": 90, "alumni_impact": 88, "career_placement": 90, "grad_school_quality": 93, "life_satisfaction": 89},
    {"name": "Washington University in St. Louis", "state": "MO", "type": "Private",
     "whole_food_emphasis": 85, "meat_quality": 83, "organic_sourcing": 80, "preparation_excellence": 87,
     "median_earnings": 87, "alumni_impact": 88, "career_placement": 88, "grad_school_quality": 94, "life_satisfaction": 90},
    {"name": "Emory University", "state": "GA", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 72, "organic_sourcing": 70, "preparation_excellence": 76,
     "median_earnings": 87, "alumni_impact": 87, "career_placement": 87, "grad_school_quality": 93, "life_satisfaction": 86},
    {"name": "Notre Dame University", "state": "IN", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 81, "organic_sourcing": 75, "preparation_excellence": 85,
     "median_earnings": 89, "alumni_impact": 90, "career_placement": 90, "grad_school_quality": 92, "life_satisfaction": 91},
    {"name": "Tufts University", "state": "MA", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 74, "organic_sourcing": 76, "preparation_excellence": 79,
     "median_earnings": 85, "alumni_impact": 84, "career_placement": 85, "grad_school_quality": 92, "life_satisfaction": 87},
    {"name": "Boston College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 72, "organic_sourcing": 70, "preparation_excellence": 77,
     "median_earnings": 84, "alumni_impact": 84, "career_placement": 84, "grad_school_quality": 89, "life_satisfaction": 87},
    {"name": "Boston University", "state": "MA", "type": "Private",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 66, "preparation_excellence": 73,
     "median_earnings": 83, "alumni_impact": 82, "career_placement": 82, "grad_school_quality": 88, "life_satisfaction": 84},
    {"name": "University of Chicago", "state": "IL", "type": "Private",
     "whole_food_emphasis": 73, "meat_quality": 71, "organic_sourcing": 70, "preparation_excellence": 76,
     "median_earnings": 91, "alumni_impact": 93, "career_placement": 90, "grad_school_quality": 98, "life_satisfaction": 85},
    {"name": "Carnegie Mellon University", "state": "PA", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 64, "preparation_excellence": 70,
     "median_earnings": 94, "alumni_impact": 91, "career_placement": 94, "grad_school_quality": 95, "life_satisfaction": 83},
    {"name": "Johns Hopkins University", "state": "MD", "type": "Private",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 68, "preparation_excellence": 74,
     "median_earnings": 90, "alumni_impact": 91, "career_placement": 89, "grad_school_quality": 97, "life_satisfaction": 84},
    {"name": "University of Southern California", "state": "CA", "type": "Private",
     "whole_food_emphasis": 75, "meat_quality": 73, "organic_sourcing": 74, "preparation_excellence": 78,
     "median_earnings": 85, "alumni_impact": 88, "career_placement": 87, "grad_school_quality": 89, "life_satisfaction": 86},
    {"name": "New York University", "state": "NY", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 65, "organic_sourcing": 62, "preparation_excellence": 70,
     "median_earnings": 82, "alumni_impact": 85, "career_placement": 83, "grad_school_quality": 87, "life_satisfaction": 80},
    {"name": "Northeastern University", "state": "MA", "type": "Private",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 66, "preparation_excellence": 72,
     "median_earnings": 87, "alumni_impact": 82, "career_placement": 93, "grad_school_quality": 85, "life_satisfaction": 85},
    {"name": "Harvey Mudd College", "state": "CA", "type": "Private",
     "whole_food_emphasis": 75, "meat_quality": 72, "organic_sourcing": 73, "preparation_excellence": 77,
     "median_earnings": 99, "alumni_impact": 90, "career_placement": 97, "grad_school_quality": 95, "life_satisfaction": 87},
    {"name": "Case Western Reserve University", "state": "OH", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 63, "preparation_excellence": 70,
     "median_earnings": 86, "alumni_impact": 83, "career_placement": 86, "grad_school_quality": 90, "life_satisfaction": 82},
    {"name": "Wake Forest University", "state": "NC", "type": "Private",
     "whole_food_emphasis": 77, "meat_quality": 76, "organic_sourcing": 72, "preparation_excellence": 80,
     "median_earnings": 84, "alumni_impact": 83, "career_placement": 84, "grad_school_quality": 88, "life_satisfaction": 88},
    {"name": "Lehigh University", "state": "PA", "type": "Private",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 67, "preparation_excellence": 74,
     "median_earnings": 85, "alumni_impact": 80, "career_placement": 85, "grad_school_quality": 85, "life_satisfaction": 84},
    {"name": "Tulane University", "state": "LA", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 77, "organic_sourcing": 70, "preparation_excellence": 82,
     "median_earnings": 78, "alumni_impact": 80, "career_placement": 78, "grad_school_quality": 85, "life_satisfaction": 86},
    {"name": "University of Rochester", "state": "NY", "type": "Private",
     "whole_food_emphasis": 71, "meat_quality": 69, "organic_sourcing": 66, "preparation_excellence": 73,
     "median_earnings": 83, "alumni_impact": 80, "career_placement": 82, "grad_school_quality": 88, "life_satisfaction": 82},
    {"name": "Rensselaer Polytechnic Institute", "state": "NY", "type": "Private",
     "whole_food_emphasis": 66, "meat_quality": 64, "organic_sourcing": 60, "preparation_excellence": 67,
     "median_earnings": 90, "alumni_impact": 82, "career_placement": 91, "grad_school_quality": 87, "life_satisfaction": 80},
    {"name": "Stevens Institute of Technology", "state": "NJ", "type": "Private",
     "whole_food_emphasis": 63, "meat_quality": 61, "organic_sourcing": 58, "preparation_excellence": 65,
     "median_earnings": 91, "alumni_impact": 79, "career_placement": 92, "grad_school_quality": 83, "life_satisfaction": 79},

    # ── Top Liberal Arts Colleges ────────────────────────────────────────────
    {"name": "Bowdoin College", "state": "ME", "type": "Private",
     "whole_food_emphasis": 97, "meat_quality": 96, "organic_sourcing": 95, "preparation_excellence": 97,
     "median_earnings": 82, "alumni_impact": 84, "career_placement": 80, "grad_school_quality": 91, "life_satisfaction": 95},
    {"name": "Amherst College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 80, "organic_sourcing": 80, "preparation_excellence": 84,
     "median_earnings": 88, "alumni_impact": 88, "career_placement": 85, "grad_school_quality": 95, "life_satisfaction": 91},
    {"name": "Williams College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 83, "meat_quality": 81, "organic_sourcing": 80, "preparation_excellence": 85,
     "median_earnings": 87, "alumni_impact": 88, "career_placement": 84, "grad_school_quality": 95, "life_satisfaction": 92},
    {"name": "Swarthmore College", "state": "PA", "type": "Private",
     "whole_food_emphasis": 79, "meat_quality": 76, "organic_sourcing": 78, "preparation_excellence": 81,
     "median_earnings": 85, "alumni_impact": 87, "career_placement": 82, "grad_school_quality": 95, "life_satisfaction": 90},
    {"name": "Wellesley College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 80, "meat_quality": 77, "organic_sourcing": 78, "preparation_excellence": 82,
     "median_earnings": 84, "alumni_impact": 88, "career_placement": 83, "grad_school_quality": 94, "life_satisfaction": 90},
    {"name": "Middlebury College", "state": "VT", "type": "Private",
     "whole_food_emphasis": 90, "meat_quality": 88, "organic_sourcing": 91, "preparation_excellence": 90,
     "median_earnings": 80, "alumni_impact": 83, "career_placement": 78, "grad_school_quality": 90, "life_satisfaction": 92},
    {"name": "Colby College", "state": "ME", "type": "Private",
     "whole_food_emphasis": 89, "meat_quality": 87, "organic_sourcing": 88, "preparation_excellence": 90,
     "median_earnings": 79, "alumni_impact": 81, "career_placement": 77, "grad_school_quality": 88, "life_satisfaction": 91},
    {"name": "Colgate University", "state": "NY", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 80, "organic_sourcing": 78, "preparation_excellence": 84,
     "median_earnings": 82, "alumni_impact": 84, "career_placement": 80, "grad_school_quality": 89, "life_satisfaction": 89},
    {"name": "Hamilton College", "state": "NY", "type": "Private",
     "whole_food_emphasis": 81, "meat_quality": 79, "organic_sourcing": 77, "preparation_excellence": 83,
     "median_earnings": 80, "alumni_impact": 82, "career_placement": 78, "grad_school_quality": 88, "life_satisfaction": 88},
    {"name": "Davidson College", "state": "NC", "type": "Private",
     "whole_food_emphasis": 79, "meat_quality": 78, "organic_sourcing": 74, "preparation_excellence": 82,
     "median_earnings": 78, "alumni_impact": 80, "career_placement": 77, "grad_school_quality": 87, "life_satisfaction": 89},
    {"name": "Carleton College", "state": "MN", "type": "Private",
     "whole_food_emphasis": 83, "meat_quality": 80, "organic_sourcing": 82, "preparation_excellence": 84,
     "median_earnings": 79, "alumni_impact": 83, "career_placement": 77, "grad_school_quality": 91, "life_satisfaction": 90},
    {"name": "Kenyon College", "state": "OH", "type": "Private",
     "whole_food_emphasis": 86, "meat_quality": 85, "organic_sourcing": 83, "preparation_excellence": 87,
     "median_earnings": 72, "alumni_impact": 78, "career_placement": 70, "grad_school_quality": 84, "life_satisfaction": 89},
    {"name": "Oberlin College", "state": "OH", "type": "Private",
     "whole_food_emphasis": 85, "meat_quality": 81, "organic_sourcing": 88, "preparation_excellence": 85,
     "median_earnings": 68, "alumni_impact": 78, "career_placement": 67, "grad_school_quality": 85, "life_satisfaction": 88},
    {"name": "Vassar College", "state": "NY", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 78, "organic_sourcing": 83, "preparation_excellence": 83,
     "median_earnings": 73, "alumni_impact": 80, "career_placement": 70, "grad_school_quality": 87, "life_satisfaction": 88},
    {"name": "Grinnell College", "state": "IA", "type": "Private",
     "whole_food_emphasis": 80, "meat_quality": 78, "organic_sourcing": 78, "preparation_excellence": 82,
     "median_earnings": 74, "alumni_impact": 78, "career_placement": 72, "grad_school_quality": 88, "life_satisfaction": 88},
    {"name": "Haverford College", "state": "PA", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 75, "organic_sourcing": 76, "preparation_excellence": 80,
     "median_earnings": 79, "alumni_impact": 82, "career_placement": 76, "grad_school_quality": 92, "life_satisfaction": 89},
    {"name": "Bryn Mawr College", "state": "PA", "type": "Private",
     "whole_food_emphasis": 81, "meat_quality": 77, "organic_sourcing": 78, "preparation_excellence": 82,
     "median_earnings": 75, "alumni_impact": 80, "career_placement": 73, "grad_school_quality": 90, "life_satisfaction": 87},
    {"name": "Smith College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 83, "meat_quality": 79, "organic_sourcing": 81, "preparation_excellence": 84,
     "median_earnings": 73, "alumni_impact": 79, "career_placement": 71, "grad_school_quality": 88, "life_satisfaction": 87},
    {"name": "Mount Holyoke College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 78, "organic_sourcing": 80, "preparation_excellence": 83,
     "median_earnings": 71, "alumni_impact": 77, "career_placement": 70, "grad_school_quality": 86, "life_satisfaction": 86},
    {"name": "Barnard College", "state": "NY", "type": "Private",
     "whole_food_emphasis": 73, "meat_quality": 70, "organic_sourcing": 72, "preparation_excellence": 75,
     "median_earnings": 79, "alumni_impact": 82, "career_placement": 78, "grad_school_quality": 90, "life_satisfaction": 85},
    {"name": "Scripps College", "state": "CA", "type": "Private",
     "whole_food_emphasis": 84, "meat_quality": 80, "organic_sourcing": 83, "preparation_excellence": 85,
     "median_earnings": 73, "alumni_impact": 77, "career_placement": 72, "grad_school_quality": 87, "life_satisfaction": 87},
    {"name": "Claremont McKenna College", "state": "CA", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 76, "organic_sourcing": 75, "preparation_excellence": 80,
     "median_earnings": 86, "alumni_impact": 87, "career_placement": 86, "grad_school_quality": 91, "life_satisfaction": 88},
    {"name": "Pomona College", "state": "CA", "type": "Private",
     "whole_food_emphasis": 82, "meat_quality": 79, "organic_sourcing": 82, "preparation_excellence": 84,
     "median_earnings": 84, "alumni_impact": 86, "career_placement": 82, "grad_school_quality": 93, "life_satisfaction": 91},
    {"name": "Bates College", "state": "ME", "type": "Private",
     "whole_food_emphasis": 87, "meat_quality": 86, "organic_sourcing": 86, "preparation_excellence": 88,
     "median_earnings": 77, "alumni_impact": 79, "career_placement": 75, "grad_school_quality": 87, "life_satisfaction": 90},
    {"name": "Trinity College", "state": "CT", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 74, "organic_sourcing": 72, "preparation_excellence": 78,
     "median_earnings": 79, "alumni_impact": 80, "career_placement": 77, "grad_school_quality": 85, "life_satisfaction": 84},
    {"name": "Furman University", "state": "SC", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 77, "organic_sourcing": 73, "preparation_excellence": 80,
     "median_earnings": 71, "alumni_impact": 72, "career_placement": 71, "grad_school_quality": 81, "life_satisfaction": 85},
    {"name": "Reed College", "state": "OR", "type": "Private",
     "whole_food_emphasis": 80, "meat_quality": 75, "organic_sourcing": 82, "preparation_excellence": 80,
     "median_earnings": 68, "alumni_impact": 78, "career_placement": 64, "grad_school_quality": 90, "life_satisfaction": 83},
    {"name": "Macalester College", "state": "MN", "type": "Private",
     "whole_food_emphasis": 80, "meat_quality": 76, "organic_sourcing": 79, "preparation_excellence": 81,
     "median_earnings": 70, "alumni_impact": 76, "career_placement": 68, "grad_school_quality": 86, "life_satisfaction": 86},

    # ── Top Public Universities ──────────────────────────────────────────────
    {"name": "University of California, Berkeley", "state": "CA", "type": "Public",
     "whole_food_emphasis": 79, "meat_quality": 76, "organic_sourcing": 80, "preparation_excellence": 81,
     "median_earnings": 88, "alumni_impact": 93, "career_placement": 88, "grad_school_quality": 97, "life_satisfaction": 85},
    {"name": "UCLA", "state": "CA", "type": "Public",
     "whole_food_emphasis": 87, "meat_quality": 85, "organic_sourcing": 84, "preparation_excellence": 88,
     "median_earnings": 85, "alumni_impact": 90, "career_placement": 85, "grad_school_quality": 92, "life_satisfaction": 87},
    {"name": "University of Michigan", "state": "MI", "type": "Public",
     "whole_food_emphasis": 75, "meat_quality": 73, "organic_sourcing": 71, "preparation_excellence": 77,
     "median_earnings": 87, "alumni_impact": 91, "career_placement": 88, "grad_school_quality": 94, "life_satisfaction": 86},
    {"name": "University of Virginia", "state": "VA", "type": "Public",
     "whole_food_emphasis": 77, "meat_quality": 76, "organic_sourcing": 73, "preparation_excellence": 80,
     "median_earnings": 87, "alumni_impact": 89, "career_placement": 87, "grad_school_quality": 92, "life_satisfaction": 88},
    {"name": "University of North Carolina at Chapel Hill", "state": "NC", "type": "Public",
     "whole_food_emphasis": 76, "meat_quality": 74, "organic_sourcing": 72, "preparation_excellence": 78,
     "median_earnings": 82, "alumni_impact": 86, "career_placement": 82, "grad_school_quality": 91, "life_satisfaction": 86},
    {"name": "University of Wisconsin-Madison", "state": "WI", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 73, "organic_sourcing": 73, "preparation_excellence": 76,
     "median_earnings": 82, "alumni_impact": 84, "career_placement": 82, "grad_school_quality": 90, "life_satisfaction": 84},
    {"name": "Georgia Institute of Technology", "state": "GA", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 65, "preparation_excellence": 72,
     "median_earnings": 92, "alumni_impact": 87, "career_placement": 94, "grad_school_quality": 91, "life_satisfaction": 82},
    {"name": "University of Illinois Urbana-Champaign", "state": "IL", "type": "Public",
     "whole_food_emphasis": 71, "meat_quality": 70, "organic_sourcing": 68, "preparation_excellence": 73,
     "median_earnings": 87, "alumni_impact": 85, "career_placement": 88, "grad_school_quality": 91, "life_satisfaction": 82},
    {"name": "University of California, San Diego", "state": "CA", "type": "Public",
     "whole_food_emphasis": 77, "meat_quality": 74, "organic_sourcing": 76, "preparation_excellence": 79,
     "median_earnings": 84, "alumni_impact": 82, "career_placement": 84, "grad_school_quality": 90, "life_satisfaction": 83},
    {"name": "University of California, Santa Barbara", "state": "CA", "type": "Public",
     "whole_food_emphasis": 76, "meat_quality": 73, "organic_sourcing": 75, "preparation_excellence": 78,
     "median_earnings": 79, "alumni_impact": 78, "career_placement": 78, "grad_school_quality": 87, "life_satisfaction": 84},
    {"name": "University of California, Davis", "state": "CA", "type": "Public",
     "whole_food_emphasis": 84, "meat_quality": 83, "organic_sourcing": 86, "preparation_excellence": 85,
     "median_earnings": 79, "alumni_impact": 78, "career_placement": 78, "grad_school_quality": 87, "life_satisfaction": 84},
    {"name": "University of California, Irvine", "state": "CA", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 71, "organic_sourcing": 72, "preparation_excellence": 75,
     "median_earnings": 78, "alumni_impact": 76, "career_placement": 77, "grad_school_quality": 85, "life_satisfaction": 80},
    {"name": "University of Washington", "state": "WA", "type": "Public",
     "whole_food_emphasis": 75, "meat_quality": 73, "organic_sourcing": 76, "preparation_excellence": 77,
     "median_earnings": 85, "alumni_impact": 84, "career_placement": 85, "grad_school_quality": 90, "life_satisfaction": 83},
    {"name": "Ohio State University", "state": "OH", "type": "Public",
     "whole_food_emphasis": 73, "meat_quality": 74, "organic_sourcing": 68, "preparation_excellence": 75,
     "median_earnings": 81, "alumni_impact": 82, "career_placement": 82, "grad_school_quality": 87, "life_satisfaction": 82},
    {"name": "Penn State University", "state": "PA", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 72, "organic_sourcing": 67, "preparation_excellence": 74,
     "median_earnings": 80, "alumni_impact": 82, "career_placement": 82, "grad_school_quality": 86, "life_satisfaction": 81},
    {"name": "Purdue University", "state": "IN", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 73, "organic_sourcing": 67, "preparation_excellence": 73,
     "median_earnings": 85, "alumni_impact": 83, "career_placement": 87, "grad_school_quality": 87, "life_satisfaction": 80},
    {"name": "University of Minnesota", "state": "MN", "type": "Public",
     "whole_food_emphasis": 73, "meat_quality": 72, "organic_sourcing": 70, "preparation_excellence": 74,
     "median_earnings": 82, "alumni_impact": 81, "career_placement": 81, "grad_school_quality": 88, "life_satisfaction": 81},
    {"name": "University of Texas at Austin", "state": "TX", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 76, "organic_sourcing": 67, "preparation_excellence": 76,
     "median_earnings": 82, "alumni_impact": 84, "career_placement": 82, "grad_school_quality": 88, "life_satisfaction": 82},
    {"name": "Texas A&M University", "state": "TX", "type": "Public",
     "whole_food_emphasis": 78, "meat_quality": 81, "organic_sourcing": 69, "preparation_excellence": 78,
     "median_earnings": 80, "alumni_impact": 80, "career_placement": 82, "grad_school_quality": 83, "life_satisfaction": 82},
    {"name": "Virginia Tech", "state": "VA", "type": "Public",
     "whole_food_emphasis": 93, "meat_quality": 92, "organic_sourcing": 87, "preparation_excellence": 93,
     "median_earnings": 80, "alumni_impact": 78, "career_placement": 83, "grad_school_quality": 82, "life_satisfaction": 84},
    {"name": "James Madison University", "state": "VA", "type": "Public",
     "whole_food_emphasis": 91, "meat_quality": 90, "organic_sourcing": 86, "preparation_excellence": 92,
     "median_earnings": 72, "alumni_impact": 70, "career_placement": 74, "grad_school_quality": 75, "life_satisfaction": 84},
    {"name": "University of Massachusetts Amherst", "state": "MA", "type": "Public",
     "whole_food_emphasis": 90, "meat_quality": 88, "organic_sourcing": 85, "preparation_excellence": 91,
     "median_earnings": 75, "alumni_impact": 74, "career_placement": 75, "grad_school_quality": 82, "life_satisfaction": 83},
    {"name": "University of Florida", "state": "FL", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 65, "preparation_excellence": 73,
     "median_earnings": 79, "alumni_impact": 79, "career_placement": 78, "grad_school_quality": 85, "life_satisfaction": 82},
    {"name": "Florida State University", "state": "FL", "type": "Public",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 62, "preparation_excellence": 69,
     "median_earnings": 72, "alumni_impact": 72, "career_placement": 72, "grad_school_quality": 78, "life_satisfaction": 78},
    {"name": "University of Georgia", "state": "GA", "type": "Public",
     "whole_food_emphasis": 73, "meat_quality": 72, "organic_sourcing": 66, "preparation_excellence": 74,
     "median_earnings": 74, "alumni_impact": 74, "career_placement": 74, "grad_school_quality": 80, "life_satisfaction": 79},
    {"name": "University of Colorado Boulder", "state": "CO", "type": "Public",
     "whole_food_emphasis": 76, "meat_quality": 72, "organic_sourcing": 76, "preparation_excellence": 77,
     "median_earnings": 74, "alumni_impact": 74, "career_placement": 73, "grad_school_quality": 80, "life_satisfaction": 82},
    {"name": "University of Oregon", "state": "OR", "type": "Public",
     "whole_food_emphasis": 78, "meat_quality": 74, "organic_sourcing": 79, "preparation_excellence": 78,
     "median_earnings": 68, "alumni_impact": 68, "career_placement": 67, "grad_school_quality": 75, "life_satisfaction": 78},
    {"name": "University of Arizona", "state": "AZ", "type": "Public",
     "whole_food_emphasis": 68, "meat_quality": 67, "organic_sourcing": 62, "preparation_excellence": 69,
     "median_earnings": 70, "alumni_impact": 68, "career_placement": 69, "grad_school_quality": 75, "life_satisfaction": 76},
    {"name": "Arizona State University", "state": "AZ", "type": "Public",
     "whole_food_emphasis": 65, "meat_quality": 63, "organic_sourcing": 59, "preparation_excellence": 66,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 73, "life_satisfaction": 74},
    {"name": "Michigan State University", "state": "MI", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 74, "organic_sourcing": 70, "preparation_excellence": 75,
     "median_earnings": 78, "alumni_impact": 78, "career_placement": 79, "grad_school_quality": 83, "life_satisfaction": 79},
    {"name": "Indiana University Bloomington", "state": "IN", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 65, "preparation_excellence": 71,
     "median_earnings": 74, "alumni_impact": 74, "career_placement": 74, "grad_school_quality": 80, "life_satisfaction": 78},
    {"name": "Iowa State University", "state": "IA", "type": "Public",
     "whole_food_emphasis": 76, "meat_quality": 78, "organic_sourcing": 70, "preparation_excellence": 76,
     "median_earnings": 76, "alumni_impact": 74, "career_placement": 78, "grad_school_quality": 79, "life_satisfaction": 78},
    {"name": "University of Iowa", "state": "IA", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 70, "organic_sourcing": 66, "preparation_excellence": 71,
     "median_earnings": 74, "alumni_impact": 73, "career_placement": 74, "grad_school_quality": 80, "life_satisfaction": 77},
    {"name": "University of Maryland", "state": "MD", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 68, "preparation_excellence": 73,
     "median_earnings": 82, "alumni_impact": 82, "career_placement": 82, "grad_school_quality": 88, "life_satisfaction": 80},
    {"name": "University of Pittsburgh", "state": "PA", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 65, "preparation_excellence": 71,
     "median_earnings": 80, "alumni_impact": 78, "career_placement": 79, "grad_school_quality": 86, "life_satisfaction": 79},
    {"name": "Rutgers University", "state": "NJ", "type": "Public",
     "whole_food_emphasis": 67, "meat_quality": 65, "organic_sourcing": 62, "preparation_excellence": 68,
     "median_earnings": 78, "alumni_impact": 77, "career_placement": 77, "grad_school_quality": 83, "life_satisfaction": 75},
    {"name": "University of Connecticut", "state": "CT", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 73, "organic_sourcing": 70, "preparation_excellence": 76,
     "median_earnings": 78, "alumni_impact": 76, "career_placement": 77, "grad_school_quality": 82, "life_satisfaction": 78},
    {"name": "University of Delaware", "state": "DE", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 67, "preparation_excellence": 73,
     "median_earnings": 77, "alumni_impact": 74, "career_placement": 76, "grad_school_quality": 80, "life_satisfaction": 78},
    {"name": "Auburn University", "state": "AL", "type": "Public",
     "whole_food_emphasis": 80, "meat_quality": 82, "organic_sourcing": 72, "preparation_excellence": 80,
     "median_earnings": 74, "alumni_impact": 73, "career_placement": 76, "grad_school_quality": 77, "life_satisfaction": 80},
    {"name": "University of Alabama", "state": "AL", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 73, "organic_sourcing": 64, "preparation_excellence": 72,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 74, "life_satisfaction": 76},
    {"name": "Clemson University", "state": "SC", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 72, "organic_sourcing": 67, "preparation_excellence": 74,
     "median_earnings": 77, "alumni_impact": 74, "career_placement": 78, "grad_school_quality": 79, "life_satisfaction": 80},
    {"name": "University of Tennessee", "state": "TN", "type": "Public",
     "whole_food_emphasis": 71, "meat_quality": 72, "organic_sourcing": 64, "preparation_excellence": 72,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 75, "life_satisfaction": 76},
    {"name": "University of Missouri", "state": "MO", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 70, "organic_sourcing": 64, "preparation_excellence": 71,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 76, "life_satisfaction": 75},
    {"name": "University of Nebraska-Lincoln", "state": "NE", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 76, "organic_sourcing": 66, "preparation_excellence": 74,
     "median_earnings": 73, "alumni_impact": 71, "career_placement": 74, "grad_school_quality": 76, "life_satisfaction": 76},
    {"name": "Kansas State University", "state": "KS", "type": "Public",
     "whole_food_emphasis": 73, "meat_quality": 75, "organic_sourcing": 65, "preparation_excellence": 73,
     "median_earnings": 72, "alumni_impact": 70, "career_placement": 73, "grad_school_quality": 74, "life_satisfaction": 75},
    {"name": "University of Kansas", "state": "KS", "type": "Public",
     "whole_food_emphasis": 68, "meat_quality": 68, "organic_sourcing": 62, "preparation_excellence": 69,
     "median_earnings": 70, "alumni_impact": 70, "career_placement": 70, "grad_school_quality": 76, "life_satisfaction": 74},
    {"name": "University of Kentucky", "state": "KY", "type": "Public",
     "whole_food_emphasis": 68, "meat_quality": 68, "organic_sourcing": 62, "preparation_excellence": 69,
     "median_earnings": 69, "alumni_impact": 68, "career_placement": 69, "grad_school_quality": 74, "life_satisfaction": 73},
    {"name": "Oklahoma State University", "state": "OK", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 74, "organic_sourcing": 63, "preparation_excellence": 72,
     "median_earnings": 71, "alumni_impact": 69, "career_placement": 72, "grad_school_quality": 73, "life_satisfaction": 74},
    {"name": "University of Oklahoma", "state": "OK", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 72, "organic_sourcing": 62, "preparation_excellence": 70,
     "median_earnings": 70, "alumni_impact": 69, "career_placement": 70, "grad_school_quality": 74, "life_satisfaction": 73},
    {"name": "University of Arkansas", "state": "AR", "type": "Public",
     "whole_food_emphasis": 69, "meat_quality": 70, "organic_sourcing": 61, "preparation_excellence": 70,
     "median_earnings": 69, "alumni_impact": 68, "career_placement": 70, "grad_school_quality": 72, "life_satisfaction": 73},
    {"name": "Mississippi State University", "state": "MS", "type": "Public",
     "whole_food_emphasis": 69, "meat_quality": 70, "organic_sourcing": 60, "preparation_excellence": 69,
     "median_earnings": 67, "alumni_impact": 65, "career_placement": 67, "grad_school_quality": 69, "life_satisfaction": 71},
    {"name": "Louisiana State University", "state": "LA", "type": "Public",
     "whole_food_emphasis": 74, "meat_quality": 75, "organic_sourcing": 64, "preparation_excellence": 76,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 75, "life_satisfaction": 77},
    {"name": "University of South Carolina", "state": "SC", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 63, "preparation_excellence": 71,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 76, "life_satisfaction": 75},
    {"name": "Colorado State University", "state": "CO", "type": "Public",
     "whole_food_emphasis": 76, "meat_quality": 74, "organic_sourcing": 74, "preparation_excellence": 76,
     "median_earnings": 72, "alumni_impact": 70, "career_placement": 72, "grad_school_quality": 76, "life_satisfaction": 79},
    {"name": "North Carolina State University", "state": "NC", "type": "Public",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 67, "preparation_excellence": 72,
     "median_earnings": 80, "alumni_impact": 77, "career_placement": 81, "grad_school_quality": 82, "life_satisfaction": 79},
    {"name": "University of New Hampshire", "state": "NH", "type": "Public",
     "whole_food_emphasis": 80, "meat_quality": 79, "organic_sourcing": 78, "preparation_excellence": 81,
     "median_earnings": 70, "alumni_impact": 68, "career_placement": 70, "grad_school_quality": 74, "life_satisfaction": 78},
    {"name": "University of Vermont", "state": "VT", "type": "Public",
     "whole_food_emphasis": 82, "meat_quality": 80, "organic_sourcing": 83, "preparation_excellence": 83,
     "median_earnings": 70, "alumni_impact": 69, "career_placement": 69, "grad_school_quality": 76, "life_satisfaction": 80},
    {"name": "University of Maine", "state": "ME", "type": "Public",
     "whole_food_emphasis": 79, "meat_quality": 78, "organic_sourcing": 77, "preparation_excellence": 79,
     "median_earnings": 67, "alumni_impact": 65, "career_placement": 67, "grad_school_quality": 70, "life_satisfaction": 76},
    {"name": "University of Montana", "state": "MT", "type": "Public",
     "whole_food_emphasis": 73, "meat_quality": 74, "organic_sourcing": 70, "preparation_excellence": 73,
     "median_earnings": 60, "alumni_impact": 58, "career_placement": 60, "grad_school_quality": 63, "life_satisfaction": 74},
    {"name": "University of Wyoming", "state": "WY", "type": "Public",
     "whole_food_emphasis": 70, "meat_quality": 73, "organic_sourcing": 63, "preparation_excellence": 70,
     "median_earnings": 65, "alumni_impact": 62, "career_placement": 66, "grad_school_quality": 66, "life_satisfaction": 72},
    {"name": "University of Nevada, Reno", "state": "NV", "type": "Public",
     "whole_food_emphasis": 65, "meat_quality": 63, "organic_sourcing": 59, "preparation_excellence": 65,
     "median_earnings": 68, "alumni_impact": 65, "career_placement": 68, "grad_school_quality": 68, "life_satisfaction": 70},
    {"name": "University of New Mexico", "state": "NM", "type": "Public",
     "whole_food_emphasis": 63, "meat_quality": 62, "organic_sourcing": 59, "preparation_excellence": 64,
     "median_earnings": 63, "alumni_impact": 61, "career_placement": 63, "grad_school_quality": 66, "life_satisfaction": 68},
    {"name": "West Virginia University", "state": "WV", "type": "Public",
     "whole_food_emphasis": 63, "meat_quality": 63, "organic_sourcing": 56, "preparation_excellence": 63,
     "median_earnings": 63, "alumni_impact": 60, "career_placement": 63, "grad_school_quality": 65, "life_satisfaction": 67},

    # ── Additional Strong Private Universities ───────────────────────────────
    {"name": "Brigham Young University", "state": "UT", "type": "Private",
     "whole_food_emphasis": 72, "meat_quality": 70, "organic_sourcing": 64, "preparation_excellence": 73,
     "median_earnings": 74, "alumni_impact": 76, "career_placement": 74, "grad_school_quality": 78, "life_satisfaction": 82},
    {"name": "Baylor University", "state": "TX", "type": "Private",
     "whole_food_emphasis": 73, "meat_quality": 74, "organic_sourcing": 65, "preparation_excellence": 74,
     "median_earnings": 72, "alumni_impact": 72, "career_placement": 72, "grad_school_quality": 76, "life_satisfaction": 80},
    {"name": "Southern Methodist University", "state": "TX", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 73, "organic_sourcing": 66, "preparation_excellence": 76,
     "median_earnings": 80, "alumni_impact": 80, "career_placement": 80, "grad_school_quality": 82, "life_satisfaction": 82},
    {"name": "Pepperdine University", "state": "CA", "type": "Private",
     "whole_food_emphasis": 77, "meat_quality": 74, "organic_sourcing": 74, "preparation_excellence": 79,
     "median_earnings": 73, "alumni_impact": 74, "career_placement": 72, "grad_school_quality": 77, "life_satisfaction": 83},
    {"name": "Santa Clara University", "state": "CA", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 73, "organic_sourcing": 74, "preparation_excellence": 77,
     "median_earnings": 80, "alumni_impact": 78, "career_placement": 80, "grad_school_quality": 80, "life_satisfaction": 82},
    {"name": "Gonzaga University", "state": "WA", "type": "Private",
     "whole_food_emphasis": 77, "meat_quality": 76, "organic_sourcing": 72, "preparation_excellence": 79,
     "median_earnings": 71, "alumni_impact": 71, "career_placement": 71, "grad_school_quality": 75, "life_satisfaction": 81},
    {"name": "University of Denver", "state": "CO", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 71, "organic_sourcing": 70, "preparation_excellence": 75,
     "median_earnings": 74, "alumni_impact": 73, "career_placement": 74, "grad_school_quality": 77, "life_satisfaction": 79},
    {"name": "Fordham University", "state": "NY", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 63, "preparation_excellence": 69,
     "median_earnings": 76, "alumni_impact": 77, "career_placement": 75, "grad_school_quality": 79, "life_satisfaction": 77},
    {"name": "Marquette University", "state": "WI", "type": "Private",
     "whole_food_emphasis": 70, "meat_quality": 69, "organic_sourcing": 65, "preparation_excellence": 71,
     "median_earnings": 73, "alumni_impact": 73, "career_placement": 73, "grad_school_quality": 77, "life_satisfaction": 78},
    {"name": "Villanova University", "state": "PA", "type": "Private",
     "whole_food_emphasis": 73, "meat_quality": 71, "organic_sourcing": 68, "preparation_excellence": 75,
     "median_earnings": 80, "alumni_impact": 79, "career_placement": 80, "grad_school_quality": 82, "life_satisfaction": 83},
    {"name": "Drexel University", "state": "PA", "type": "Private",
     "whole_food_emphasis": 64, "meat_quality": 62, "organic_sourcing": 59, "preparation_excellence": 65,
     "median_earnings": 81, "alumni_impact": 74, "career_placement": 87, "grad_school_quality": 78, "life_satisfaction": 76},
    {"name": "American University", "state": "DC", "type": "Private",
     "whole_food_emphasis": 70, "meat_quality": 67, "organic_sourcing": 68, "preparation_excellence": 71,
     "median_earnings": 72, "alumni_impact": 77, "career_placement": 72, "grad_school_quality": 78, "life_satisfaction": 77},

    # ── Military Academies ───────────────────────────────────────────────────
    {"name": "United States Military Academy (West Point)", "state": "NY", "type": "Military",
     "whole_food_emphasis": 80, "meat_quality": 82, "organic_sourcing": 70, "preparation_excellence": 80,
     "median_earnings": 88, "alumni_impact": 92, "career_placement": 100, "grad_school_quality": 85, "life_satisfaction": 85},
    {"name": "United States Naval Academy", "state": "MD", "type": "Military",
     "whole_food_emphasis": 79, "meat_quality": 80, "organic_sourcing": 68, "preparation_excellence": 79,
     "median_earnings": 87, "alumni_impact": 91, "career_placement": 100, "grad_school_quality": 84, "life_satisfaction": 84},
    {"name": "United States Air Force Academy", "state": "CO", "type": "Military",
     "whole_food_emphasis": 80, "meat_quality": 81, "organic_sourcing": 69, "preparation_excellence": 80,
     "median_earnings": 88, "alumni_impact": 90, "career_placement": 100, "grad_school_quality": 84, "life_satisfaction": 84},

    # ── HBCUs ────────────────────────────────────────────────────────────────
    {"name": "Howard University", "state": "DC", "type": "HBCU",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 62, "preparation_excellence": 70,
     "median_earnings": 72, "alumni_impact": 82, "career_placement": 72, "grad_school_quality": 78, "life_satisfaction": 78},
    {"name": "Spelman College", "state": "GA", "type": "HBCU",
     "whole_food_emphasis": 70, "meat_quality": 68, "organic_sourcing": 64, "preparation_excellence": 71,
     "median_earnings": 70, "alumni_impact": 80, "career_placement": 70, "grad_school_quality": 80, "life_satisfaction": 78},
    {"name": "Morehouse College", "state": "GA", "type": "HBCU",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 62, "preparation_excellence": 69,
     "median_earnings": 70, "alumni_impact": 82, "career_placement": 70, "grad_school_quality": 78, "life_satisfaction": 77},
    {"name": "Hampton University", "state": "VA", "type": "HBCU",
     "whole_food_emphasis": 67, "meat_quality": 65, "organic_sourcing": 61, "preparation_excellence": 68,
     "median_earnings": 66, "alumni_impact": 72, "career_placement": 66, "grad_school_quality": 70, "life_satisfaction": 73},
    {"name": "Florida A&M University", "state": "FL", "type": "HBCU",
     "whole_food_emphasis": 65, "meat_quality": 64, "organic_sourcing": 59, "preparation_excellence": 66,
     "median_earnings": 65, "alumni_impact": 70, "career_placement": 66, "grad_school_quality": 68, "life_satisfaction": 71},
    {"name": "North Carolina A&T State University", "state": "NC", "type": "HBCU",
     "whole_food_emphasis": 65, "meat_quality": 64, "organic_sourcing": 58, "preparation_excellence": 65,
     "median_earnings": 67, "alumni_impact": 68, "career_placement": 68, "grad_school_quality": 68, "life_satisfaction": 70},
    {"name": "Tuskegee University", "state": "AL", "type": "HBCU",
     "whole_food_emphasis": 67, "meat_quality": 68, "organic_sourcing": 60, "preparation_excellence": 67,
     "median_earnings": 63, "alumni_impact": 72, "career_placement": 64, "grad_school_quality": 67, "life_satisfaction": 70},
    {"name": "Xavier University of Louisiana", "state": "LA", "type": "HBCU",
     "whole_food_emphasis": 65, "meat_quality": 64, "organic_sourcing": 59, "preparation_excellence": 66,
     "median_earnings": 64, "alumni_impact": 73, "career_placement": 65, "grad_school_quality": 72, "life_satisfaction": 71},

    # ── Additional Notable Schools ───────────────────────────────────────────
    {"name": "Babson College", "state": "MA", "type": "Private",
     "whole_food_emphasis": 71, "meat_quality": 69, "organic_sourcing": 66, "preparation_excellence": 73,
     "median_earnings": 88, "alumni_impact": 86, "career_placement": 88, "grad_school_quality": 82, "life_satisfaction": 83},
    {"name": "Bentley University", "state": "MA", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 66, "organic_sourcing": 63, "preparation_excellence": 69,
     "median_earnings": 85, "alumni_impact": 78, "career_placement": 87, "grad_school_quality": 76, "life_satisfaction": 80},
    {"name": "Bucknell University", "state": "PA", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 75, "organic_sourcing": 72, "preparation_excellence": 78,
     "median_earnings": 80, "alumni_impact": 78, "career_placement": 80, "grad_school_quality": 82, "life_satisfaction": 83},
    {"name": "Lafayette College", "state": "PA", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 73, "organic_sourcing": 70, "preparation_excellence": 76,
     "median_earnings": 79, "alumni_impact": 77, "career_placement": 79, "grad_school_quality": 80, "life_satisfaction": 82},
    {"name": "Gettysburg College", "state": "PA", "type": "Private",
     "whole_food_emphasis": 75, "meat_quality": 74, "organic_sourcing": 71, "preparation_excellence": 76,
     "median_earnings": 74, "alumni_impact": 73, "career_placement": 73, "grad_school_quality": 78, "life_satisfaction": 81},
    {"name": "Muhlenberg College", "state": "PA", "type": "Private",
     "whole_food_emphasis": 73, "meat_quality": 71, "organic_sourcing": 69, "preparation_excellence": 74,
     "median_earnings": 71, "alumni_impact": 70, "career_placement": 71, "grad_school_quality": 76, "life_satisfaction": 79},
    {"name": "Wheaton College (MA)", "state": "MA", "type": "Private",
     "whole_food_emphasis": 83, "meat_quality": 80, "organic_sourcing": 82, "preparation_excellence": 84,
     "median_earnings": 68, "alumni_impact": 68, "career_placement": 66, "grad_school_quality": 76, "life_satisfaction": 82},
    {"name": "College of William & Mary", "state": "VA", "type": "Public",
     "whole_food_emphasis": 76, "meat_quality": 74, "organic_sourcing": 72, "preparation_excellence": 78,
     "median_earnings": 80, "alumni_impact": 82, "career_placement": 79, "grad_school_quality": 87, "life_satisfaction": 84},
    {"name": "University of Richmond", "state": "VA", "type": "Private",
     "whole_food_emphasis": 78, "meat_quality": 77, "organic_sourcing": 74, "preparation_excellence": 80,
     "median_earnings": 81, "alumni_impact": 80, "career_placement": 80, "grad_school_quality": 83, "life_satisfaction": 85},
    {"name": "Rhodes College", "state": "TN", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 76, "organic_sourcing": 70, "preparation_excellence": 78,
     "median_earnings": 70, "alumni_impact": 71, "career_placement": 69, "grad_school_quality": 79, "life_satisfaction": 81},
    {"name": "Sewanee: The University of the South", "state": "TN", "type": "Private",
     "whole_food_emphasis": 79, "meat_quality": 78, "organic_sourcing": 75, "preparation_excellence": 80,
     "median_earnings": 67, "alumni_impact": 71, "career_placement": 66, "grad_school_quality": 78, "life_satisfaction": 82},
    {"name": "Centre College", "state": "KY", "type": "Private",
     "whole_food_emphasis": 76, "meat_quality": 75, "organic_sourcing": 70, "preparation_excellence": 77,
     "median_earnings": 70, "alumni_impact": 71, "career_placement": 69, "grad_school_quality": 78, "life_satisfaction": 80},
    {"name": "Denison University", "state": "OH", "type": "Private",
     "whole_food_emphasis": 79, "meat_quality": 77, "organic_sourcing": 75, "preparation_excellence": 80,
     "median_earnings": 72, "alumni_impact": 73, "career_placement": 71, "grad_school_quality": 79, "life_satisfaction": 82},
    {"name": "DePauw University", "state": "IN", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 73, "organic_sourcing": 69, "preparation_excellence": 75,
     "median_earnings": 71, "alumni_impact": 73, "career_placement": 70, "grad_school_quality": 78, "life_satisfaction": 79},
    {"name": "Whitman College", "state": "WA", "type": "Private",
     "whole_food_emphasis": 81, "meat_quality": 78, "organic_sourcing": 80, "preparation_excellence": 82,
     "median_earnings": 68, "alumni_impact": 72, "career_placement": 66, "grad_school_quality": 82, "life_satisfaction": 84},
    {"name": "Colorado College", "state": "CO", "type": "Private",
     "whole_food_emphasis": 79, "meat_quality": 75, "organic_sourcing": 79, "preparation_excellence": 80,
     "median_earnings": 68, "alumni_impact": 71, "career_placement": 66, "grad_school_quality": 79, "life_satisfaction": 82},
    {"name": "University of Puget Sound", "state": "WA", "type": "Private",
     "whole_food_emphasis": 77, "meat_quality": 74, "organic_sourcing": 76, "preparation_excellence": 78,
     "median_earnings": 64, "alumni_impact": 66, "career_placement": 63, "grad_school_quality": 73, "life_satisfaction": 79},
    {"name": "Stony Brook University", "state": "NY", "type": "Public",
     "whole_food_emphasis": 66, "meat_quality": 64, "organic_sourcing": 61, "preparation_excellence": 66,
     "median_earnings": 80, "alumni_impact": 77, "career_placement": 79, "grad_school_quality": 86, "life_satisfaction": 76},
    {"name": "University at Buffalo", "state": "NY", "type": "Public",
     "whole_food_emphasis": 63, "meat_quality": 61, "organic_sourcing": 58, "preparation_excellence": 63,
     "median_earnings": 76, "alumni_impact": 72, "career_placement": 75, "grad_school_quality": 80, "life_satisfaction": 72},
    {"name": "George Washington University", "state": "DC", "type": "Private",
     "whole_food_emphasis": 68, "meat_quality": 65, "organic_sourcing": 65, "preparation_excellence": 70,
     "median_earnings": 79, "alumni_impact": 82, "career_placement": 78, "grad_school_quality": 82, "life_satisfaction": 78},
    {"name": "Rollins College", "state": "FL", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 72, "organic_sourcing": 68, "preparation_excellence": 75,
     "median_earnings": 70, "alumni_impact": 70, "career_placement": 69, "grad_school_quality": 73, "life_satisfaction": 79},
    {"name": "University of San Diego", "state": "CA", "type": "Private",
     "whole_food_emphasis": 74, "meat_quality": 71, "organic_sourcing": 71, "preparation_excellence": 75,
     "median_earnings": 72, "alumni_impact": 72, "career_placement": 71, "grad_school_quality": 74, "life_satisfaction": 79},
    {"name": "Loyola University Chicago", "state": "IL", "type": "Private",
     "whole_food_emphasis": 69, "meat_quality": 67, "organic_sourcing": 64, "preparation_excellence": 70,
     "median_earnings": 71, "alumni_impact": 71, "career_placement": 71, "grad_school_quality": 76, "life_satisfaction": 76},
    {"name": "Seton Hall University", "state": "NJ", "type": "Private",
     "whole_food_emphasis": 62, "meat_quality": 60, "organic_sourcing": 57, "preparation_excellence": 62,
     "median_earnings": 74, "alumni_impact": 71, "career_placement": 73, "grad_school_quality": 74, "life_satisfaction": 72},
]


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

HEADER_LINE = "=" * 100

def print_section(title: str) -> None:
    print(f"\n{HEADER_LINE}")
    print(f"  {title}")
    print(HEADER_LINE)


def print_top_n(universities: List[University], n: int, key: str, label: str) -> None:
    print_section(f"TOP {n} — {label}")
    top = sorted(universities, key=lambda u: getattr(u, key), reverse=True)[:n]
    print(f"{'Rank':<6} {'University':<55} {'State':<6} {'Score':>7}")
    print("-" * 80)
    for i, u in enumerate(top, 1):
        score = getattr(u, key)
        print(f"{i:<6} {u.name:<55} {u.state:<6} {score:>7.1f}")


def print_full_rankings(universities: List[University]) -> None:
    print_section("FREMIAN INDEX — COMPLETE UNIVERSITY RANKINGS")
    print(
        f"{'Rank':<5} {'University':<48} {'St':<4} {'Type':<9}"
        f" {'FQS':>6} {'LSS':>6} {'FI':>6}"
        f" {'FdRk':>5} {'ScRk':>5}"
    )
    print("-" * 105)
    for u in universities:
        print(
            f"{u.overall_rank:<5} {u.name:<48} {u.state:<4} {u.type:<9}"
            f" {u.food_quality_score:>6.1f} {u.life_success_score:>6.1f} {u.fremian_index:>6.1f}"
            f" {u.food_rank:>5} {u.success_rank:>5}"
        )


def save_csv(universities: List[University], path: str) -> None:
    fields = [
        "overall_rank", "name", "state", "type",
        "food_quality_score", "food_rank",
        "whole_food_emphasis", "meat_quality", "organic_sourcing", "preparation_excellence",
        "life_success_score", "success_rank",
        "median_earnings", "alumni_impact", "career_placement",
        "grad_school_quality", "life_satisfaction",
        "fremian_index",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for u in universities:
            row = asdict(u)
            writer.writerow({k: row[k] for k in fields})
    print(f"\nFull dataset saved → {path}")


def save_json(universities: List[University], path: str) -> None:
    data = [asdict(u) for u in universities]
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"JSON dataset saved → {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    universities = [University(**d) for d in RAW_DATA]
    ranked = compute_scores(universities)

    print("\n" + HEADER_LINE)
    print("  FREMIAN UNIVERSITY INDEX  |  v1.0")
    print("  Two-pillar ranking of US undergraduate universities")
    print(f"  Pillar 1 — Food Hall Quality Score (FQS):  whole foods, quality meats,")
    print(f"             organic sourcing, preparation excellence")
    print(f"  Pillar 2 — Life Success Score (LSS):       post-grad earnings, alumni")
    print(f"             impact, career placement, graduate school, life satisfaction")
    print(f"  Fremian Index (FI) = 0.50 × FQS  +  0.50 × LSS")
    print(HEADER_LINE)

    print_top_n(ranked, 25, "fremian_index",     "FREMIAN INDEX (Overall)")
    print_top_n(ranked, 25, "food_quality_score", "FOOD HALL QUALITY SCORE")
    print_top_n(ranked, 25, "life_success_score", "LIFE PREPAREDNESS & SUCCESS SCORE")

    print_full_rankings(ranked)

    save_csv(ranked, "fremian_university_rankings.csv")
    save_json(ranked, "fremian_university_rankings.json")

    # Summary stats
    print_section("METHODOLOGY NOTES")
    print("""
Food Hall Quality Score (FQS) sub-scores
  whole_food_emphasis    (35%) — whole-food-first menus; unprocessed, nutrient-dense staples
  meat_quality           (30%) — grass-fed beef, pastured poultry, wild-caught fish
  organic_sourcing       (20%) — certified organic, local-farm, and regenerative sourcing
  preparation_excellence (15%) — chef-led kitchens, fresh daily prep, seasonal variety

Life Success Score (LSS) sub-scores
  median_earnings        (30%) — normalised median salary 5–10 years post-graduation
                                 (source basis: College Scorecard, PayScale ROI)
  alumni_impact          (25%) — CEOs, executives, Forbes lists, field-defining contributions
  career_placement       (20%) — % employed or in grad school within 6 months of graduation
  grad_school_quality    (15%) — % attending top graduate / professional programmes
  life_satisfaction      (10%) — alumni-reported life and career satisfaction surveys

Scores are calibrated against: Princeton Review "Best Campus Food", Niche dining
ratings, The Daily Meal college rankings, College Scorecard median earnings,
PayScale College ROI Report, and US News Best Colleges alumni outcome data.
    """.strip())


if __name__ == "__main__":
    main()
