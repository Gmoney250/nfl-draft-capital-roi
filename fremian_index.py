"""
Fremian University Index  v3.2
Four pillars, weighted by personal priority:
  LSS — Life Preparedness & Success   50%
  SSS — Social Scene Score            30%
  FQS — Food Hall Quality Score       15%
  PES — Physical Environment Score     5%

Fremian Index (FI) = 0.50*LSS + 0.30*SSS + 0.15*FQS + 0.05*PES

SSS sub-weights v3.2 (peer attractiveness split out):
  peer_attractiveness        40%  physical appearance culture, "hot school" rep
  social_vibrancy            30%  fun events, nightlife, energy
  peer_intellectual_caliber  20%  genius factor
  dating_social_culture      10%  hookup culture, Greek life, dating scene
"""

import csv
import json
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class University:
    name: str
    state: str
    type: str
    # FQS sub-scores
    whole_food_emphasis: float
    meat_quality: float
    organic_sourcing: float
    preparation_excellence: float
    # LSS sub-scores
    median_earnings: float
    alumni_impact: float
    career_placement: float
    grad_school_quality: float
    life_satisfaction: float
    # PES sub-scores
    gym_quality: float
    nature_access: float
    campus_scenery: float
    city_quality: float
    # SSS sub-scores
    peer_intellectual_caliber: float
    social_vibrancy: float
    peer_attractiveness: float
    dating_social_culture: float
    # Computed
    weather_climate: float = field(default=0.0)
    food_quality_score: float = field(default=0.0)
    life_success_score: float = field(default=0.0)
    physical_env_score: float = field(default=0.0)
    social_scene_score: float = field(default=0.0)
    fremian_index: float = field(default=0.0)
    food_rank: int = field(default=0)
    success_rank: int = field(default=0)
    physical_rank: int = field(default=0)
    social_rank: int = field(default=0)
    overall_rank: int = field(default=0)


WEATHER = {
    "Stanford University": 94,
    "University of California, Berkeley": 88,
    "UCLA": 93,
    "University of California, San Diego": 96,
    "University of California, Santa Barbara": 95,
    "University of California, Davis": 82,
    "University of California, Irvine": 93,
    "Harvey Mudd College": 91,
    "Pomona College": 91,
    "Claremont McKenna College": 91,
    "Scripps College": 91,
    "University of Southern California": 91,
    "Caltech": 90,
    "Pepperdine University": 95,
    "Santa Clara University": 88,
    "University of San Diego": 96,
    "Loyola Marymount University": 92,
    "Reed College": 56,
    "University of Miami": 88,
    "University of Florida": 82,
    "Florida State University": 82,
    "Rollins College": 85,
    "Florida A&M University": 82,
    "University of Texas at Austin": 78,
    "Texas A&M University": 77,
    "Rice University": 77,
    "Baylor University": 76,
    "Southern Methodist University": 80,
    "Texas Christian University": 80,
    "Emory University": 78,
    "Georgia Institute of Technology": 78,
    "University of Georgia": 76,
    "Spelman College": 78,
    "Morehouse College": 78,
    "Duke University": 73,
    "University of North Carolina at Chapel Hill": 73,
    "Wake Forest University": 72,
    "Davidson College": 73,
    "North Carolina A&T State University": 71,
    "North Carolina State University": 72,
    "Furman University": 73,
    "Clemson University": 73,
    "University of South Carolina": 74,
    "University of Virginia": 68,
    "Virginia Tech": 62,
    "James Madison University": 65,
    "College of William & Mary": 67,
    "University of Richmond": 67,
    "Hampton University": 68,
    "Georgetown University": 63,
    "American University": 63,
    "George Washington University": 63,
    "Howard University": 63,
    "Vanderbilt University": 68,
    "Rhodes College": 66,
    "Sewanee: The University of the South": 63,
    "University of Tennessee": 67,
    "Auburn University": 73,
    "University of Alabama": 73,
    "Mississippi State University": 72,
    "Tuskegee University": 73,
    "Tulane University": 76,
    "Louisiana State University": 74,
    "Xavier University of Louisiana": 74,
    "University of Arkansas": 65,
    "University of Oklahoma": 63,
    "Oklahoma State University": 62,
    "University of Kentucky": 59,
    "West Virginia University": 52,
    "Centre College": 58,
    "Johns Hopkins University": 60,
    "University of Maryland": 60,
    "University of Delaware": 60,
    "Columbia University": 55,
    "New York University": 55,
    "Fordham University": 55,
    "Barnard College": 55,
    "Stony Brook University": 52,
    "University at Buffalo": 40,
    "Stevens Institute of Technology": 56,
    "Seton Hall University": 56,
    "Cornell University": 44,
    "Colgate University": 44,
    "Hamilton College": 44,
    "Rensselaer Polytechnic Institute": 44,
    "University of Rochester": 42,
    "Vassar College": 50,
    "MIT": 50,
    "Harvard University": 50,
    "Boston University": 50,
    "Boston College": 50,
    "Tufts University": 50,
    "Northeastern University": 50,
    "Babson College": 50,
    "Bentley University": 50,
    "Wheaton College (MA)": 50,
    "Wellesley College": 50,
    "Smith College": 47,
    "Amherst College": 47,
    "Mount Holyoke College": 47,
    "University of Massachusetts Amherst": 46,
    "Brown University": 50,
    "Yale University": 52,
    "Trinity College": 52,
    "University of Connecticut": 50,
    "Princeton University": 56,
    "Rutgers University": 55,
    "Villanova University": 56,
    "Haverford College": 56,
    "Bryn Mawr College": 56,
    "Swarthmore College": 56,
    "Lehigh University": 53,
    "Lafayette College": 53,
    "Bucknell University": 52,
    "Gettysburg College": 53,
    "Muhlenberg College": 53,
    "University of Pennsylvania": 55,
    "Carnegie Mellon University": 49,
    "University of Pittsburgh": 49,
    "Penn State University": 50,
    "Drexel University": 55,
    "Duquesne University": 49,
    "Dartmouth College": 42,
    "University of New Hampshire": 44,
    "Middlebury College": 40,
    "University of Vermont": 42,
    "Bowdoin College": 38,
    "Colby College": 37,
    "Bates College": 37,
    "University of Maine": 36,
    "Ohio State University": 48,
    "Case Western Reserve University": 45,
    "Kenyon College": 48,
    "Oberlin College": 45,
    "Denison University": 48,
    "Notre Dame University": 46,
    "Purdue University": 47,
    "Indiana University Bloomington": 50,
    "DePauw University": 50,
    "University of Michigan": 44,
    "Michigan State University": 44,
    "University of Wisconsin-Madison": 42,
    "Marquette University": 42,
    "University of Minnesota": 36,
    "Carleton College": 36,
    "Macalester College": 38,
    "Northwestern University": 46,
    "University of Chicago": 46,
    "Loyola University Chicago": 46,
    "University of Iowa": 43,
    "Iowa State University": 43,
    "Grinnell College": 42,
    "University of Missouri": 52,
    "University of Kansas": 52,
    "Kansas State University": 51,
    "University of Nebraska-Lincoln": 50,
    "Washington University in St. Louis": 54,
    "University of Colorado Boulder": 66,
    "Colorado College": 66,
    "United States Air Force Academy": 65,
    "Colorado State University": 65,
    "University of Denver": 66,
    "Brigham Young University": 63,
    "University of Washington": 55,
    "Gonzaga University": 52,
    "Whitman College": 52,
    "University of Puget Sound": 54,
    "University of Montana": 42,
    "University of Wyoming": 42,
    "University of Nevada, Reno": 68,
    "University of New Mexico": 72,
    "University of Arizona": 76,
    "Arizona State University": 76,
    "University of Oregon": 57,
    "Williams College": 47,
}


def compute_scores(universities: List[University]) -> List[University]:
    for u in universities:
        u.food_quality_score = round(
            0.30*u.whole_food_emphasis + 0.25*u.meat_quality
            + 0.35*u.organic_sourcing + 0.10*u.preparation_excellence, 2)
        u.life_success_score = round(
            0.50*u.median_earnings + 0.40*u.alumni_impact
            + 0.10*u.career_placement, 2)
        u.weather_climate = WEATHER.get(u.name, 58.0)
        u.physical_env_score = round(
            0.15*u.gym_quality + 0.25*u.nature_access
            + 0.20*u.campus_scenery + 0.20*u.city_quality
            + 0.20*u.weather_climate, 2)
        u.social_scene_score = round(
            0.40*u.peer_attractiveness + 0.30*u.social_vibrancy
            + 0.20*u.peer_intellectual_caliber + 0.10*u.dating_social_culture, 2)
        u.fremian_index = round(
            0.50*u.life_success_score + 0.30*u.social_scene_score
            + 0.15*u.food_quality_score + 0.05*u.physical_env_score, 2)

    for key, attr in [
        ("food_quality_score", "food_rank"),
        ("life_success_score", "success_rank"),
        ("physical_env_score", "physical_rank"),
        ("social_scene_score", "social_rank"),
        ("fremian_index",      "overall_rank"),
    ]:
        for i, u in enumerate(sorted(universities, key=lambda x: getattr(x, key), reverse=True)):
            setattr(u, attr, i + 1)

    return sorted(universities, key=lambda x: x.fremian_index, reverse=True)


RAW_DATA: List[dict] = [
    # ── Ivy League ──────────────────────────────────────────────────────────
    {"name":"Harvard University","state":"MA","type":"Private",
     "whole_food_emphasis":76,"meat_quality":74,"organic_sourcing":72,"preparation_excellence":80,
     "median_earnings":97,"alumni_impact":99,"career_placement":96,"grad_school_quality":99,"life_satisfaction":90,
     "gym_quality":82,"nature_access":58,"campus_scenery":85,"city_quality":92,
     "peer_intellectual_caliber":98,"social_vibrancy":68,"peer_attractiveness":70,"dating_social_culture":60},

    {"name":"Princeton University","state":"NJ","type":"Private",
     "whole_food_emphasis":78,"meat_quality":76,"organic_sourcing":75,"preparation_excellence":82,
     "median_earnings":95,"alumni_impact":97,"career_placement":95,"grad_school_quality":99,"life_satisfaction":92,
     "gym_quality":85,"nature_access":68,"campus_scenery":92,"city_quality":72,
     "peer_intellectual_caliber":98,"social_vibrancy":72,"peer_attractiveness":75,"dating_social_culture":65},

    {"name":"Yale University","state":"CT","type":"Private",
     "whole_food_emphasis":74,"meat_quality":72,"organic_sourcing":70,"preparation_excellence":79,
     "median_earnings":93,"alumni_impact":96,"career_placement":94,"grad_school_quality":98,"life_satisfaction":89,
     "gym_quality":80,"nature_access":60,"campus_scenery":88,"city_quality":75,
     "peer_intellectual_caliber":98,"social_vibrancy":74,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Columbia University","state":"NY","type":"Private",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":65,"preparation_excellence":74,
     "median_earnings":92,"alumni_impact":94,"career_placement":93,"grad_school_quality":97,"life_satisfaction":85,
     "gym_quality":72,"nature_access":28,"campus_scenery":72,"city_quality":98,
     "peer_intellectual_caliber":97,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":65},

    {"name":"University of Pennsylvania","state":"PA","type":"Private",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":68,"preparation_excellence":76,
     "median_earnings":94,"alumni_impact":95,"career_placement":95,"grad_school_quality":97,"life_satisfaction":87,
     "gym_quality":80,"nature_access":52,"campus_scenery":72,"city_quality":85,
     "peer_intellectual_caliber":96,"social_vibrancy":76,"peer_attractiveness":74,"dating_social_culture":72},

    {"name":"Cornell University","state":"NY","type":"Private",
     "whole_food_emphasis":82,"meat_quality":84,"organic_sourcing":78,"preparation_excellence":85,
     "median_earnings":89,"alumni_impact":91,"career_placement":92,"grad_school_quality":95,"life_satisfaction":86,
     "gym_quality":82,"nature_access":78,"campus_scenery":85,"city_quality":55,
     "peer_intellectual_caliber":93,"social_vibrancy":76,"peer_attractiveness":68,"dating_social_culture":68},

    {"name":"Dartmouth College","state":"NH","type":"Private",
     "whole_food_emphasis":77,"meat_quality":75,"organic_sourcing":73,"preparation_excellence":80,
     "median_earnings":91,"alumni_impact":90,"career_placement":90,"grad_school_quality":94,"life_satisfaction":88,
     "gym_quality":80,"nature_access":88,"campus_scenery":88,"city_quality":42,
     "peer_intellectual_caliber":95,"social_vibrancy":80,"peer_attractiveness":72,"dating_social_culture":80},

    {"name":"Brown University","state":"RI","type":"Private",
     "whole_food_emphasis":75,"meat_quality":72,"organic_sourcing":74,"preparation_excellence":78,
     "median_earnings":88,"alumni_impact":89,"career_placement":88,"grad_school_quality":93,"life_satisfaction":87,
     "gym_quality":75,"nature_access":60,"campus_scenery":78,"city_quality":78,
     "peer_intellectual_caliber":94,"social_vibrancy":82,"peer_attractiveness":75,"dating_social_culture":75},

    # ── Elite Private (non-Ivy) ─────────────────────────────────────────────
    {"name":"MIT","state":"MA","type":"Private",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":68,"preparation_excellence":76,
     "median_earnings":99,"alumni_impact":99,"career_placement":98,"grad_school_quality":99,"life_satisfaction":88,
     "gym_quality":80,"nature_access":58,"campus_scenery":70,"city_quality":92,
     "peer_intellectual_caliber":99,"social_vibrancy":58,"peer_attractiveness":52,"dating_social_culture":48},

    {"name":"Stanford University","state":"CA","type":"Private",
     "whole_food_emphasis":80,"meat_quality":78,"organic_sourcing":82,"preparation_excellence":84,
     "median_earnings":97,"alumni_impact":99,"career_placement":97,"grad_school_quality":99,"life_satisfaction":91,
     "gym_quality":95,"nature_access":80,"campus_scenery":92,"city_quality":92,
     "peer_intellectual_caliber":98,"social_vibrancy":78,"peer_attractiveness":78,"dating_social_culture":70},

    {"name":"Caltech","state":"CA","type":"Private",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":65,"preparation_excellence":70,
     "median_earnings":98,"alumni_impact":96,"career_placement":96,"grad_school_quality":99,"life_satisfaction":84,
     "gym_quality":65,"nature_access":65,"campus_scenery":72,"city_quality":88,
     "peer_intellectual_caliber":99,"social_vibrancy":52,"peer_attractiveness":45,"dating_social_culture":42},

    {"name":"Duke University","state":"NC","type":"Private",
     "whole_food_emphasis":78,"meat_quality":76,"organic_sourcing":74,"preparation_excellence":82,
     "median_earnings":91,"alumni_impact":93,"career_placement":92,"grad_school_quality":96,"life_satisfaction":89,
     "gym_quality":90,"nature_access":70,"campus_scenery":88,"city_quality":72,
     "peer_intellectual_caliber":96,"social_vibrancy":85,"peer_attractiveness":86,"dating_social_culture":85},

    {"name":"Northwestern University","state":"IL","type":"Private",
     "whole_food_emphasis":74,"meat_quality":72,"organic_sourcing":70,"preparation_excellence":78,
     "median_earnings":90,"alumni_impact":91,"career_placement":91,"grad_school_quality":95,"life_satisfaction":87,
     "gym_quality":85,"nature_access":62,"campus_scenery":75,"city_quality":88,
     "peer_intellectual_caliber":95,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":65},

    {"name":"Georgetown University","state":"DC","type":"Private",
     "whole_food_emphasis":73,"meat_quality":71,"organic_sourcing":70,"preparation_excellence":77,
     "median_earnings":89,"alumni_impact":92,"career_placement":91,"grad_school_quality":94,"life_satisfaction":86,
     "gym_quality":78,"nature_access":48,"campus_scenery":75,"city_quality":92,
     "peer_intellectual_caliber":91,"social_vibrancy":75,"peer_attractiveness":76,"dating_social_culture":68},

    {"name":"Vanderbilt University","state":"TN","type":"Private",
     "whole_food_emphasis":79,"meat_quality":78,"organic_sourcing":73,"preparation_excellence":83,
     "median_earnings":88,"alumni_impact":88,"career_placement":89,"grad_school_quality":93,"life_satisfaction":90,
     "gym_quality":88,"nature_access":60,"campus_scenery":80,"city_quality":88,
     "peer_intellectual_caliber":93,"social_vibrancy":87,"peer_attractiveness":91,"dating_social_culture":87},

    {"name":"Rice University","state":"TX","type":"Private",
     "whole_food_emphasis":80,"meat_quality":79,"organic_sourcing":74,"preparation_excellence":84,
     "median_earnings":90,"alumni_impact":88,"career_placement":90,"grad_school_quality":93,"life_satisfaction":89,
     "gym_quality":85,"nature_access":55,"campus_scenery":82,"city_quality":82,
     "peer_intellectual_caliber":95,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":62},

    {"name":"Washington University in St. Louis","state":"MO","type":"Private",
     "whole_food_emphasis":85,"meat_quality":83,"organic_sourcing":80,"preparation_excellence":87,
     "median_earnings":87,"alumni_impact":88,"career_placement":88,"grad_school_quality":94,"life_satisfaction":90,
     "gym_quality":85,"nature_access":62,"campus_scenery":78,"city_quality":82,
     "peer_intellectual_caliber":93,"social_vibrancy":75,"peer_attractiveness":73,"dating_social_culture":70},

    {"name":"Emory University","state":"GA","type":"Private",
     "whole_food_emphasis":74,"meat_quality":72,"organic_sourcing":70,"preparation_excellence":76,
     "median_earnings":87,"alumni_impact":87,"career_placement":87,"grad_school_quality":93,"life_satisfaction":86,
     "gym_quality":82,"nature_access":60,"campus_scenery":68,"city_quality":85,
     "peer_intellectual_caliber":90,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Notre Dame University","state":"IN","type":"Private",
     "whole_food_emphasis":82,"meat_quality":81,"organic_sourcing":75,"preparation_excellence":85,
     "median_earnings":89,"alumni_impact":90,"career_placement":90,"grad_school_quality":92,"life_satisfaction":91,
     "gym_quality":90,"nature_access":60,"campus_scenery":82,"city_quality":52,
     "peer_intellectual_caliber":92,"social_vibrancy":82,"peer_attractiveness":74,"dating_social_culture":72},

    {"name":"Tufts University","state":"MA","type":"Private",
     "whole_food_emphasis":76,"meat_quality":74,"organic_sourcing":76,"preparation_excellence":79,
     "median_earnings":85,"alumni_impact":84,"career_placement":85,"grad_school_quality":92,"life_satisfaction":87,
     "gym_quality":72,"nature_access":60,"campus_scenery":72,"city_quality":90,
     "peer_intellectual_caliber":90,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":65},

    {"name":"Boston College","state":"MA","type":"Private",
     "whole_food_emphasis":74,"meat_quality":72,"organic_sourcing":70,"preparation_excellence":77,
     "median_earnings":84,"alumni_impact":84,"career_placement":84,"grad_school_quality":89,"life_satisfaction":87,
     "gym_quality":78,"nature_access":58,"campus_scenery":75,"city_quality":90,
     "peer_intellectual_caliber":87,"social_vibrancy":78,"peer_attractiveness":74,"dating_social_culture":70},

    {"name":"Boston University","state":"MA","type":"Private",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":66,"preparation_excellence":73,
     "median_earnings":83,"alumni_impact":82,"career_placement":82,"grad_school_quality":88,"life_satisfaction":84,
     "gym_quality":75,"nature_access":55,"campus_scenery":68,"city_quality":90,
     "peer_intellectual_caliber":83,"social_vibrancy":78,"peer_attractiveness":70,"dating_social_culture":72},

    {"name":"University of Chicago","state":"IL","type":"Private",
     "whole_food_emphasis":73,"meat_quality":71,"organic_sourcing":70,"preparation_excellence":76,
     "median_earnings":91,"alumni_impact":93,"career_placement":90,"grad_school_quality":98,"life_satisfaction":85,
     "gym_quality":75,"nature_access":50,"campus_scenery":72,"city_quality":88,
     "peer_intellectual_caliber":97,"social_vibrancy":55,"peer_attractiveness":58,"dating_social_culture":52},

    {"name":"Carnegie Mellon University","state":"PA","type":"Private",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":64,"preparation_excellence":70,
     "median_earnings":94,"alumni_impact":91,"career_placement":94,"grad_school_quality":95,"life_satisfaction":83,
     "gym_quality":75,"nature_access":55,"campus_scenery":65,"city_quality":80,
     "peer_intellectual_caliber":95,"social_vibrancy":60,"peer_attractiveness":55,"dating_social_culture":52},

    {"name":"Johns Hopkins University","state":"MD","type":"Private",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":68,"preparation_excellence":74,
     "median_earnings":90,"alumni_impact":91,"career_placement":89,"grad_school_quality":97,"life_satisfaction":84,
     "gym_quality":75,"nature_access":52,"campus_scenery":65,"city_quality":72,
     "peer_intellectual_caliber":95,"social_vibrancy":60,"peer_attractiveness":60,"dating_social_culture":52},

    {"name":"University of Southern California","state":"CA","type":"Private",
     "whole_food_emphasis":75,"meat_quality":73,"organic_sourcing":74,"preparation_excellence":78,
     "median_earnings":85,"alumni_impact":88,"career_placement":87,"grad_school_quality":89,"life_satisfaction":86,
     "gym_quality":88,"nature_access":72,"campus_scenery":78,"city_quality":88,
     "peer_intellectual_caliber":85,"social_vibrancy":92,"peer_attractiveness":92,"dating_social_culture":88},

    {"name":"New York University","state":"NY","type":"Private",
     "whole_food_emphasis":68,"meat_quality":65,"organic_sourcing":62,"preparation_excellence":70,
     "median_earnings":82,"alumni_impact":85,"career_placement":83,"grad_school_quality":87,"life_satisfaction":80,
     "gym_quality":68,"nature_access":22,"campus_scenery":68,"city_quality":98,
     "peer_intellectual_caliber":85,"social_vibrancy":80,"peer_attractiveness":76,"dating_social_culture":70},

    {"name":"Northeastern University","state":"MA","type":"Private",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":66,"preparation_excellence":72,
     "median_earnings":87,"alumni_impact":82,"career_placement":93,"grad_school_quality":85,"life_satisfaction":85,
     "gym_quality":78,"nature_access":55,"campus_scenery":62,"city_quality":90,
     "peer_intellectual_caliber":85,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"Harvey Mudd College","state":"CA","type":"Private",
     "whole_food_emphasis":75,"meat_quality":72,"organic_sourcing":73,"preparation_excellence":77,
     "median_earnings":99,"alumni_impact":90,"career_placement":97,"grad_school_quality":95,"life_satisfaction":87,
     "gym_quality":68,"nature_access":68,"campus_scenery":70,"city_quality":88,
     "peer_intellectual_caliber":97,"social_vibrancy":65,"peer_attractiveness":52,"dating_social_culture":48},

    {"name":"Case Western Reserve University","state":"OH","type":"Private",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":63,"preparation_excellence":70,
     "median_earnings":86,"alumni_impact":83,"career_placement":86,"grad_school_quality":90,"life_satisfaction":82,
     "gym_quality":72,"nature_access":52,"campus_scenery":60,"city_quality":70,
     "peer_intellectual_caliber":88,"social_vibrancy":58,"peer_attractiveness":55,"dating_social_culture":52},

    {"name":"Wake Forest University","state":"NC","type":"Private",
     "whole_food_emphasis":77,"meat_quality":76,"organic_sourcing":72,"preparation_excellence":80,
     "median_earnings":84,"alumni_impact":83,"career_placement":84,"grad_school_quality":88,"life_satisfaction":88,
     "gym_quality":85,"nature_access":65,"campus_scenery":78,"city_quality":68,
     "peer_intellectual_caliber":89,"social_vibrancy":80,"peer_attractiveness":83,"dating_social_culture":78},

    {"name":"Lehigh University","state":"PA","type":"Private",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":67,"preparation_excellence":74,
     "median_earnings":85,"alumni_impact":80,"career_placement":85,"grad_school_quality":85,"life_satisfaction":84,
     "gym_quality":78,"nature_access":68,"campus_scenery":72,"city_quality":58,
     "peer_intellectual_caliber":83,"social_vibrancy":75,"peer_attractiveness":72,"dating_social_culture":72},

    {"name":"Tulane University","state":"LA","type":"Private",
     "whole_food_emphasis":78,"meat_quality":77,"organic_sourcing":70,"preparation_excellence":82,
     "median_earnings":78,"alumni_impact":80,"career_placement":78,"grad_school_quality":85,"life_satisfaction":86,
     "gym_quality":78,"nature_access":42,"campus_scenery":72,"city_quality":88,
     "peer_intellectual_caliber":85,"social_vibrancy":95,"peer_attractiveness":78,"dating_social_culture":90},

    {"name":"University of Rochester","state":"NY","type":"Private",
     "whole_food_emphasis":71,"meat_quality":69,"organic_sourcing":66,"preparation_excellence":73,
     "median_earnings":83,"alumni_impact":80,"career_placement":82,"grad_school_quality":88,"life_satisfaction":82,
     "gym_quality":72,"nature_access":55,"campus_scenery":62,"city_quality":62,
     "peer_intellectual_caliber":88,"social_vibrancy":62,"peer_attractiveness":58,"dating_social_culture":55},

    {"name":"Rensselaer Polytechnic Institute","state":"NY","type":"Private",
     "whole_food_emphasis":66,"meat_quality":64,"organic_sourcing":60,"preparation_excellence":67,
     "median_earnings":90,"alumni_impact":82,"career_placement":91,"grad_school_quality":87,"life_satisfaction":80,
     "gym_quality":72,"nature_access":65,"campus_scenery":65,"city_quality":62,
     "peer_intellectual_caliber":86,"social_vibrancy":60,"peer_attractiveness":50,"dating_social_culture":45},

    {"name":"Stevens Institute of Technology","state":"NJ","type":"Private",
     "whole_food_emphasis":63,"meat_quality":61,"organic_sourcing":58,"preparation_excellence":65,
     "median_earnings":91,"alumni_impact":79,"career_placement":92,"grad_school_quality":83,"life_satisfaction":79,
     "gym_quality":68,"nature_access":52,"campus_scenery":72,"city_quality":88,
     "peer_intellectual_caliber":85,"social_vibrancy":58,"peer_attractiveness":58,"dating_social_culture":52},

    # ── Top Liberal Arts Colleges ────────────────────────────────────────────
    {"name":"Bowdoin College","state":"ME","type":"Private",
     "whole_food_emphasis":97,"meat_quality":96,"organic_sourcing":95,"preparation_excellence":97,
     "median_earnings":82,"alumni_impact":84,"career_placement":80,"grad_school_quality":91,"life_satisfaction":95,
     "gym_quality":78,"nature_access":85,"campus_scenery":82,"city_quality":42,
     "peer_intellectual_caliber":90,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":65},

    {"name":"Amherst College","state":"MA","type":"Private",
     "whole_food_emphasis":82,"meat_quality":80,"organic_sourcing":80,"preparation_excellence":84,
     "median_earnings":88,"alumni_impact":88,"career_placement":85,"grad_school_quality":95,"life_satisfaction":91,
     "gym_quality":78,"nature_access":80,"campus_scenery":82,"city_quality":48,
     "peer_intellectual_caliber":93,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Williams College","state":"MA","type":"Private",
     "whole_food_emphasis":83,"meat_quality":81,"organic_sourcing":80,"preparation_excellence":85,
     "median_earnings":87,"alumni_impact":88,"career_placement":84,"grad_school_quality":95,"life_satisfaction":92,
     "gym_quality":80,"nature_access":87,"campus_scenery":90,"city_quality":35,
     "peer_intellectual_caliber":93,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":65},

    {"name":"Swarthmore College","state":"PA","type":"Private",
     "whole_food_emphasis":79,"meat_quality":76,"organic_sourcing":78,"preparation_excellence":81,
     "median_earnings":85,"alumni_impact":87,"career_placement":82,"grad_school_quality":95,"life_satisfaction":90,
     "gym_quality":72,"nature_access":65,"campus_scenery":75,"city_quality":80,
     "peer_intellectual_caliber":94,"social_vibrancy":65,"peer_attractiveness":65,"dating_social_culture":62},

    {"name":"Wellesley College","state":"MA","type":"Private",
     "whole_food_emphasis":80,"meat_quality":77,"organic_sourcing":78,"preparation_excellence":82,
     "median_earnings":84,"alumni_impact":88,"career_placement":83,"grad_school_quality":94,"life_satisfaction":90,
     "gym_quality":78,"nature_access":65,"campus_scenery":82,"city_quality":88,
     "peer_intellectual_caliber":90,"social_vibrancy":68,"peer_attractiveness":70,"dating_social_culture":58},

    {"name":"Middlebury College","state":"VT","type":"Private",
     "whole_food_emphasis":90,"meat_quality":88,"organic_sourcing":91,"preparation_excellence":90,
     "median_earnings":80,"alumni_impact":83,"career_placement":78,"grad_school_quality":90,"life_satisfaction":92,
     "gym_quality":82,"nature_access":93,"campus_scenery":93,"city_quality":38,
     "peer_intellectual_caliber":88,"social_vibrancy":75,"peer_attractiveness":80,"dating_social_culture":72},

    {"name":"Colby College","state":"ME","type":"Private",
     "whole_food_emphasis":89,"meat_quality":87,"organic_sourcing":88,"preparation_excellence":90,
     "median_earnings":79,"alumni_impact":81,"career_placement":77,"grad_school_quality":88,"life_satisfaction":91,
     "gym_quality":78,"nature_access":85,"campus_scenery":82,"city_quality":38,
     "peer_intellectual_caliber":87,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Colgate University","state":"NY","type":"Private",
     "whole_food_emphasis":82,"meat_quality":80,"organic_sourcing":78,"preparation_excellence":84,
     "median_earnings":82,"alumni_impact":84,"career_placement":80,"grad_school_quality":89,"life_satisfaction":89,
     "gym_quality":80,"nature_access":72,"campus_scenery":82,"city_quality":40,
     "peer_intellectual_caliber":87,"social_vibrancy":78,"peer_attractiveness":75,"dating_social_culture":75},

    {"name":"Hamilton College","state":"NY","type":"Private",
     "whole_food_emphasis":81,"meat_quality":79,"organic_sourcing":77,"preparation_excellence":83,
     "median_earnings":80,"alumni_impact":82,"career_placement":78,"grad_school_quality":88,"life_satisfaction":88,
     "gym_quality":75,"nature_access":70,"campus_scenery":78,"city_quality":40,
     "peer_intellectual_caliber":87,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":68},

    {"name":"Davidson College","state":"NC","type":"Private",
     "whole_food_emphasis":79,"meat_quality":78,"organic_sourcing":74,"preparation_excellence":82,
     "median_earnings":78,"alumni_impact":80,"career_placement":77,"grad_school_quality":87,"life_satisfaction":89,
     "gym_quality":78,"nature_access":68,"campus_scenery":75,"city_quality":62,
     "peer_intellectual_caliber":89,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Carleton College","state":"MN","type":"Private",
     "whole_food_emphasis":83,"meat_quality":80,"organic_sourcing":82,"preparation_excellence":84,
     "median_earnings":79,"alumni_impact":83,"career_placement":77,"grad_school_quality":91,"life_satisfaction":90,
     "gym_quality":72,"nature_access":65,"campus_scenery":68,"city_quality":42,
     "peer_intellectual_caliber":91,"social_vibrancy":68,"peer_attractiveness":62,"dating_social_culture":60},

    {"name":"Kenyon College","state":"OH","type":"Private",
     "whole_food_emphasis":86,"meat_quality":85,"organic_sourcing":83,"preparation_excellence":87,
     "median_earnings":72,"alumni_impact":78,"career_placement":70,"grad_school_quality":84,"life_satisfaction":89,
     "gym_quality":70,"nature_access":65,"campus_scenery":70,"city_quality":38,
     "peer_intellectual_caliber":85,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"Oberlin College","state":"OH","type":"Private",
     "whole_food_emphasis":85,"meat_quality":81,"organic_sourcing":88,"preparation_excellence":85,
     "median_earnings":68,"alumni_impact":78,"career_placement":67,"grad_school_quality":85,"life_satisfaction":88,
     "gym_quality":68,"nature_access":60,"campus_scenery":62,"city_quality":48,
     "peer_intellectual_caliber":88,"social_vibrancy":72,"peer_attractiveness":58,"dating_social_culture":62},

    {"name":"Vassar College","state":"NY","type":"Private",
     "whole_food_emphasis":82,"meat_quality":78,"organic_sourcing":83,"preparation_excellence":83,
     "median_earnings":73,"alumni_impact":80,"career_placement":70,"grad_school_quality":87,"life_satisfaction":88,
     "gym_quality":70,"nature_access":65,"campus_scenery":75,"city_quality":62,
     "peer_intellectual_caliber":88,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"Grinnell College","state":"IA","type":"Private",
     "whole_food_emphasis":80,"meat_quality":78,"organic_sourcing":78,"preparation_excellence":82,
     "median_earnings":74,"alumni_impact":78,"career_placement":72,"grad_school_quality":88,"life_satisfaction":88,
     "gym_quality":70,"nature_access":55,"campus_scenery":58,"city_quality":35,
     "peer_intellectual_caliber":90,"social_vibrancy":68,"peer_attractiveness":60,"dating_social_culture":60},

    {"name":"Haverford College","state":"PA","type":"Private",
     "whole_food_emphasis":78,"meat_quality":75,"organic_sourcing":76,"preparation_excellence":80,
     "median_earnings":79,"alumni_impact":82,"career_placement":76,"grad_school_quality":92,"life_satisfaction":89,
     "gym_quality":72,"nature_access":62,"campus_scenery":72,"city_quality":80,
     "peer_intellectual_caliber":92,"social_vibrancy":65,"peer_attractiveness":65,"dating_social_culture":62},

    {"name":"Bryn Mawr College","state":"PA","type":"Private",
     "whole_food_emphasis":81,"meat_quality":77,"organic_sourcing":78,"preparation_excellence":82,
     "median_earnings":75,"alumni_impact":80,"career_placement":73,"grad_school_quality":90,"life_satisfaction":87,
     "gym_quality":70,"nature_access":62,"campus_scenery":78,"city_quality":80,
     "peer_intellectual_caliber":88,"social_vibrancy":62,"peer_attractiveness":65,"dating_social_culture":55},

    {"name":"Smith College","state":"MA","type":"Private",
     "whole_food_emphasis":83,"meat_quality":79,"organic_sourcing":81,"preparation_excellence":84,
     "median_earnings":73,"alumni_impact":79,"career_placement":71,"grad_school_quality":88,"life_satisfaction":87,
     "gym_quality":72,"nature_access":72,"campus_scenery":78,"city_quality":48,
     "peer_intellectual_caliber":86,"social_vibrancy":65,"peer_attractiveness":65,"dating_social_culture":55},

    {"name":"Mount Holyoke College","state":"MA","type":"Private",
     "whole_food_emphasis":82,"meat_quality":78,"organic_sourcing":80,"preparation_excellence":83,
     "median_earnings":71,"alumni_impact":77,"career_placement":70,"grad_school_quality":86,"life_satisfaction":86,
     "gym_quality":70,"nature_access":72,"campus_scenery":78,"city_quality":45,
     "peer_intellectual_caliber":84,"social_vibrancy":62,"peer_attractiveness":62,"dating_social_culture":55},

    {"name":"Barnard College","state":"NY","type":"Private",
     "whole_food_emphasis":73,"meat_quality":70,"organic_sourcing":72,"preparation_excellence":75,
     "median_earnings":79,"alumni_impact":82,"career_placement":78,"grad_school_quality":90,"life_satisfaction":85,
     "gym_quality":68,"nature_access":28,"campus_scenery":72,"city_quality":98,
     "peer_intellectual_caliber":90,"social_vibrancy":78,"peer_attractiveness":76,"dating_social_culture":70},

    {"name":"Scripps College","state":"CA","type":"Private",
     "whole_food_emphasis":84,"meat_quality":80,"organic_sourcing":83,"preparation_excellence":85,
     "median_earnings":73,"alumni_impact":77,"career_placement":72,"grad_school_quality":87,"life_satisfaction":87,
     "gym_quality":70,"nature_access":68,"campus_scenery":80,"city_quality":85,
     "peer_intellectual_caliber":88,"social_vibrancy":70,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Claremont McKenna College","state":"CA","type":"Private",
     "whole_food_emphasis":78,"meat_quality":76,"organic_sourcing":75,"preparation_excellence":80,
     "median_earnings":86,"alumni_impact":87,"career_placement":86,"grad_school_quality":91,"life_satisfaction":88,
     "gym_quality":75,"nature_access":68,"campus_scenery":78,"city_quality":85,
     "peer_intellectual_caliber":92,"social_vibrancy":75,"peer_attractiveness":76,"dating_social_culture":78},

    {"name":"Pomona College","state":"CA","type":"Private",
     "whole_food_emphasis":82,"meat_quality":79,"organic_sourcing":82,"preparation_excellence":84,
     "median_earnings":84,"alumni_impact":86,"career_placement":82,"grad_school_quality":93,"life_satisfaction":91,
     "gym_quality":75,"nature_access":70,"campus_scenery":80,"city_quality":85,
     "peer_intellectual_caliber":93,"social_vibrancy":72,"peer_attractiveness":74,"dating_social_culture":68},

    {"name":"Bates College","state":"ME","type":"Private",
     "whole_food_emphasis":87,"meat_quality":86,"organic_sourcing":86,"preparation_excellence":88,
     "median_earnings":77,"alumni_impact":79,"career_placement":75,"grad_school_quality":87,"life_satisfaction":90,
     "gym_quality":74,"nature_access":83,"campus_scenery":80,"city_quality":40,
     "peer_intellectual_caliber":85,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":65},

    {"name":"Trinity College","state":"CT","type":"Private",
     "whole_food_emphasis":76,"meat_quality":74,"organic_sourcing":72,"preparation_excellence":78,
     "median_earnings":79,"alumni_impact":80,"career_placement":77,"grad_school_quality":85,"life_satisfaction":84,
     "gym_quality":72,"nature_access":60,"campus_scenery":68,"city_quality":62,
     "peer_intellectual_caliber":82,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":70},

    {"name":"Furman University","state":"SC","type":"Private",
     "whole_food_emphasis":78,"meat_quality":77,"organic_sourcing":73,"preparation_excellence":80,
     "median_earnings":71,"alumni_impact":72,"career_placement":71,"grad_school_quality":81,"life_satisfaction":85,
     "gym_quality":80,"nature_access":72,"campus_scenery":78,"city_quality":65,
     "peer_intellectual_caliber":82,"social_vibrancy":70,"peer_attractiveness":70,"dating_social_culture":62},

    {"name":"Reed College","state":"OR","type":"Private",
     "whole_food_emphasis":80,"meat_quality":75,"organic_sourcing":82,"preparation_excellence":80,
     "median_earnings":68,"alumni_impact":78,"career_placement":64,"grad_school_quality":90,"life_satisfaction":83,
     "gym_quality":65,"nature_access":80,"campus_scenery":75,"city_quality":82,
     "peer_intellectual_caliber":90,"social_vibrancy":68,"peer_attractiveness":58,"dating_social_culture":60},

    {"name":"Macalester College","state":"MN","type":"Private",
     "whole_food_emphasis":80,"meat_quality":76,"organic_sourcing":79,"preparation_excellence":81,
     "median_earnings":70,"alumni_impact":76,"career_placement":68,"grad_school_quality":86,"life_satisfaction":86,
     "gym_quality":68,"nature_access":62,"campus_scenery":65,"city_quality":82,
     "peer_intellectual_caliber":88,"social_vibrancy":68,"peer_attractiveness":62,"dating_social_culture":60},

    # ── Top Public Universities ──────────────────────────────────────────────
    {"name":"University of California, Berkeley","state":"CA","type":"Public",
     "whole_food_emphasis":79,"meat_quality":76,"organic_sourcing":80,"preparation_excellence":81,
     "median_earnings":88,"alumni_impact":93,"career_placement":88,"grad_school_quality":97,"life_satisfaction":85,
     "gym_quality":85,"nature_access":78,"campus_scenery":82,"city_quality":92,
     "peer_intellectual_caliber":92,"social_vibrancy":80,"peer_attractiveness":78,"dating_social_culture":72},

    {"name":"UCLA","state":"CA","type":"Public",
     "whole_food_emphasis":87,"meat_quality":85,"organic_sourcing":84,"preparation_excellence":88,
     "median_earnings":85,"alumni_impact":90,"career_placement":85,"grad_school_quality":92,"life_satisfaction":87,
     "gym_quality":93,"nature_access":75,"campus_scenery":85,"city_quality":88,
     "peer_intellectual_caliber":90,"social_vibrancy":85,"peer_attractiveness":88,"dating_social_culture":80},

    {"name":"University of Michigan","state":"MI","type":"Public",
     "whole_food_emphasis":75,"meat_quality":73,"organic_sourcing":71,"preparation_excellence":77,
     "median_earnings":87,"alumni_impact":91,"career_placement":88,"grad_school_quality":94,"life_satisfaction":86,
     "gym_quality":94,"nature_access":68,"campus_scenery":72,"city_quality":75,
     "peer_intellectual_caliber":92,"social_vibrancy":85,"peer_attractiveness":80,"dating_social_culture":80},

    {"name":"University of Virginia","state":"VA","type":"Public",
     "whole_food_emphasis":77,"meat_quality":76,"organic_sourcing":73,"preparation_excellence":80,
     "median_earnings":87,"alumni_impact":89,"career_placement":87,"grad_school_quality":92,"life_satisfaction":88,
     "gym_quality":88,"nature_access":78,"campus_scenery":88,"city_quality":65,
     "peer_intellectual_caliber":90,"social_vibrancy":85,"peer_attractiveness":85,"dating_social_culture":83},

    {"name":"University of North Carolina at Chapel Hill","state":"NC","type":"Public",
     "whole_food_emphasis":76,"meat_quality":74,"organic_sourcing":72,"preparation_excellence":78,
     "median_earnings":82,"alumni_impact":86,"career_placement":82,"grad_school_quality":91,"life_satisfaction":86,
     "gym_quality":88,"nature_access":68,"campus_scenery":75,"city_quality":72,
     "peer_intellectual_caliber":88,"social_vibrancy":83,"peer_attractiveness":80,"dating_social_culture":80},

    {"name":"University of Wisconsin-Madison","state":"WI","type":"Public",
     "whole_food_emphasis":74,"meat_quality":73,"organic_sourcing":73,"preparation_excellence":76,
     "median_earnings":82,"alumni_impact":84,"career_placement":82,"grad_school_quality":90,"life_satisfaction":84,
     "gym_quality":90,"nature_access":75,"campus_scenery":75,"city_quality":78,
     "peer_intellectual_caliber":85,"social_vibrancy":88,"peer_attractiveness":80,"dating_social_culture":88},

    {"name":"Georgia Institute of Technology","state":"GA","type":"Public",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":65,"preparation_excellence":72,
     "median_earnings":92,"alumni_impact":87,"career_placement":94,"grad_school_quality":91,"life_satisfaction":82,
     "gym_quality":88,"nature_access":58,"campus_scenery":65,"city_quality":85,
     "peer_intellectual_caliber":92,"social_vibrancy":65,"peer_attractiveness":60,"dating_social_culture":58},

    {"name":"University of Illinois Urbana-Champaign","state":"IL","type":"Public",
     "whole_food_emphasis":71,"meat_quality":70,"organic_sourcing":68,"preparation_excellence":73,
     "median_earnings":87,"alumni_impact":85,"career_placement":88,"grad_school_quality":91,"life_satisfaction":82,
     "gym_quality":88,"nature_access":55,"campus_scenery":65,"city_quality":60,
     "peer_intellectual_caliber":88,"social_vibrancy":78,"peer_attractiveness":68,"dating_social_culture":70},

    {"name":"University of California, San Diego","state":"CA","type":"Public",
     "whole_food_emphasis":77,"meat_quality":74,"organic_sourcing":76,"preparation_excellence":79,
     "median_earnings":84,"alumni_impact":82,"career_placement":84,"grad_school_quality":90,"life_satisfaction":83,
     "gym_quality":88,"nature_access":85,"campus_scenery":88,"city_quality":85,
     "peer_intellectual_caliber":86,"social_vibrancy":70,"peer_attractiveness":74,"dating_social_culture":68},

    {"name":"University of California, Santa Barbara","state":"CA","type":"Public",
     "whole_food_emphasis":76,"meat_quality":73,"organic_sourcing":75,"preparation_excellence":78,
     "median_earnings":79,"alumni_impact":78,"career_placement":78,"grad_school_quality":87,"life_satisfaction":84,
     "gym_quality":85,"nature_access":93,"campus_scenery":97,"city_quality":72,
     "peer_intellectual_caliber":82,"social_vibrancy":92,"peer_attractiveness":88,"dating_social_culture":92},

    {"name":"University of California, Davis","state":"CA","type":"Public",
     "whole_food_emphasis":84,"meat_quality":83,"organic_sourcing":86,"preparation_excellence":85,
     "median_earnings":79,"alumni_impact":78,"career_placement":78,"grad_school_quality":87,"life_satisfaction":84,
     "gym_quality":85,"nature_access":68,"campus_scenery":68,"city_quality":62,
     "peer_intellectual_caliber":82,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"University of California, Irvine","state":"CA","type":"Public",
     "whole_food_emphasis":74,"meat_quality":71,"organic_sourcing":72,"preparation_excellence":75,
     "median_earnings":78,"alumni_impact":76,"career_placement":77,"grad_school_quality":85,"life_satisfaction":80,
     "gym_quality":82,"nature_access":65,"campus_scenery":68,"city_quality":78,
     "peer_intellectual_caliber":82,"social_vibrancy":68,"peer_attractiveness":66,"dating_social_culture":62},

    {"name":"University of Washington","state":"WA","type":"Public",
     "whole_food_emphasis":75,"meat_quality":73,"organic_sourcing":76,"preparation_excellence":77,
     "median_earnings":85,"alumni_impact":84,"career_placement":85,"grad_school_quality":90,"life_satisfaction":83,
     "gym_quality":88,"nature_access":88,"campus_scenery":82,"city_quality":85,
     "peer_intellectual_caliber":85,"social_vibrancy":78,"peer_attractiveness":72,"dating_social_culture":72},

    {"name":"Ohio State University","state":"OH","type":"Public",
     "whole_food_emphasis":73,"meat_quality":74,"organic_sourcing":68,"preparation_excellence":75,
     "median_earnings":81,"alumni_impact":82,"career_placement":82,"grad_school_quality":87,"life_satisfaction":82,
     "gym_quality":92,"nature_access":58,"campus_scenery":65,"city_quality":75,
     "peer_intellectual_caliber":80,"social_vibrancy":82,"peer_attractiveness":72,"dating_social_culture":80},

    {"name":"Penn State University","state":"PA","type":"Public",
     "whole_food_emphasis":72,"meat_quality":72,"organic_sourcing":67,"preparation_excellence":74,
     "median_earnings":80,"alumni_impact":82,"career_placement":82,"grad_school_quality":86,"life_satisfaction":81,
     "gym_quality":92,"nature_access":68,"campus_scenery":68,"city_quality":52,
     "peer_intellectual_caliber":80,"social_vibrancy":85,"peer_attractiveness":75,"dating_social_culture":82},

    {"name":"Purdue University","state":"IN","type":"Public",
     "whole_food_emphasis":72,"meat_quality":73,"organic_sourcing":67,"preparation_excellence":73,
     "median_earnings":85,"alumni_impact":83,"career_placement":87,"grad_school_quality":87,"life_satisfaction":80,
     "gym_quality":88,"nature_access":58,"campus_scenery":60,"city_quality":52,
     "peer_intellectual_caliber":83,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"University of Minnesota","state":"MN","type":"Public",
     "whole_food_emphasis":73,"meat_quality":72,"organic_sourcing":70,"preparation_excellence":74,
     "median_earnings":82,"alumni_impact":81,"career_placement":81,"grad_school_quality":88,"life_satisfaction":81,
     "gym_quality":88,"nature_access":65,"campus_scenery":65,"city_quality":82,
     "peer_intellectual_caliber":80,"social_vibrancy":75,"peer_attractiveness":68,"dating_social_culture":72},

    {"name":"University of Texas at Austin","state":"TX","type":"Public",
     "whole_food_emphasis":74,"meat_quality":76,"organic_sourcing":67,"preparation_excellence":76,
     "median_earnings":82,"alumni_impact":84,"career_placement":82,"grad_school_quality":88,"life_satisfaction":82,
     "gym_quality":90,"nature_access":68,"campus_scenery":70,"city_quality":88,
     "peer_intellectual_caliber":85,"social_vibrancy":85,"peer_attractiveness":80,"dating_social_culture":82},

    {"name":"Texas A&M University","state":"TX","type":"Public",
     "whole_food_emphasis":78,"meat_quality":81,"organic_sourcing":69,"preparation_excellence":78,
     "median_earnings":80,"alumni_impact":80,"career_placement":82,"grad_school_quality":83,"life_satisfaction":82,
     "gym_quality":90,"nature_access":62,"campus_scenery":62,"city_quality":62,
     "peer_intellectual_caliber":78,"social_vibrancy":82,"peer_attractiveness":72,"dating_social_culture":78},

    {"name":"Virginia Tech","state":"VA","type":"Public",
     "whole_food_emphasis":93,"meat_quality":92,"organic_sourcing":87,"preparation_excellence":93,
     "median_earnings":80,"alumni_impact":78,"career_placement":83,"grad_school_quality":82,"life_satisfaction":84,
     "gym_quality":88,"nature_access":85,"campus_scenery":85,"city_quality":52,
     "peer_intellectual_caliber":82,"social_vibrancy":75,"peer_attractiveness":68,"dating_social_culture":70},

    {"name":"James Madison University","state":"VA","type":"Public",
     "whole_food_emphasis":91,"meat_quality":90,"organic_sourcing":86,"preparation_excellence":92,
     "median_earnings":72,"alumni_impact":70,"career_placement":74,"grad_school_quality":75,"life_satisfaction":84,
     "gym_quality":85,"nature_access":80,"campus_scenery":80,"city_quality":55,
     "peer_intellectual_caliber":76,"social_vibrancy":78,"peer_attractiveness":72,"dating_social_culture":72},

    {"name":"University of Massachusetts Amherst","state":"MA","type":"Public",
     "whole_food_emphasis":90,"meat_quality":88,"organic_sourcing":85,"preparation_excellence":91,
     "median_earnings":75,"alumni_impact":74,"career_placement":75,"grad_school_quality":82,"life_satisfaction":83,
     "gym_quality":85,"nature_access":78,"campus_scenery":72,"city_quality":48,
     "peer_intellectual_caliber":78,"social_vibrancy":78,"peer_attractiveness":68,"dating_social_culture":75},

    {"name":"University of Florida","state":"FL","type":"Public",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":65,"preparation_excellence":73,
     "median_earnings":79,"alumni_impact":79,"career_placement":78,"grad_school_quality":85,"life_satisfaction":82,
     "gym_quality":88,"nature_access":60,"campus_scenery":62,"city_quality":62,
     "peer_intellectual_caliber":82,"social_vibrancy":82,"peer_attractiveness":78,"dating_social_culture":78},

    {"name":"Florida State University","state":"FL","type":"Public",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":62,"preparation_excellence":69,
     "median_earnings":72,"alumni_impact":72,"career_placement":72,"grad_school_quality":78,"life_satisfaction":78,
     "gym_quality":85,"nature_access":58,"campus_scenery":62,"city_quality":62,
     "peer_intellectual_caliber":78,"social_vibrancy":87,"peer_attractiveness":82,"dating_social_culture":85},

    {"name":"University of Georgia","state":"GA","type":"Public",
     "whole_food_emphasis":73,"meat_quality":72,"organic_sourcing":66,"preparation_excellence":74,
     "median_earnings":74,"alumni_impact":74,"career_placement":74,"grad_school_quality":80,"life_satisfaction":79,
     "gym_quality":85,"nature_access":62,"campus_scenery":65,"city_quality":65,
     "peer_intellectual_caliber":80,"social_vibrancy":82,"peer_attractiveness":78,"dating_social_culture":82},

    {"name":"University of Colorado Boulder","state":"CO","type":"Public",
     "whole_food_emphasis":76,"meat_quality":72,"organic_sourcing":76,"preparation_excellence":77,
     "median_earnings":74,"alumni_impact":74,"career_placement":73,"grad_school_quality":80,"life_satisfaction":82,
     "gym_quality":90,"nature_access":95,"campus_scenery":92,"city_quality":72,
     "peer_intellectual_caliber":78,"social_vibrancy":88,"peer_attractiveness":82,"dating_social_culture":85},

    {"name":"University of Oregon","state":"OR","type":"Public",
     "whole_food_emphasis":78,"meat_quality":74,"organic_sourcing":79,"preparation_excellence":78,
     "median_earnings":68,"alumni_impact":68,"career_placement":67,"grad_school_quality":75,"life_satisfaction":78,
     "gym_quality":82,"nature_access":88,"campus_scenery":78,"city_quality":72,
     "peer_intellectual_caliber":74,"social_vibrancy":78,"peer_attractiveness":70,"dating_social_culture":72},

    {"name":"University of Arizona","state":"AZ","type":"Public",
     "whole_food_emphasis":68,"meat_quality":67,"organic_sourcing":62,"preparation_excellence":69,
     "median_earnings":70,"alumni_impact":68,"career_placement":69,"grad_school_quality":75,"life_satisfaction":76,
     "gym_quality":82,"nature_access":70,"campus_scenery":72,"city_quality":72,
     "peer_intellectual_caliber":74,"social_vibrancy":78,"peer_attractiveness":74,"dating_social_culture":75},

    {"name":"Arizona State University","state":"AZ","type":"Public",
     "whole_food_emphasis":65,"meat_quality":63,"organic_sourcing":59,"preparation_excellence":66,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":73,"life_satisfaction":74,
     "gym_quality":88,"nature_access":65,"campus_scenery":70,"city_quality":82,
     "peer_intellectual_caliber":71,"social_vibrancy":80,"peer_attractiveness":76,"dating_social_culture":82},

    {"name":"Michigan State University","state":"MI","type":"Public",
     "whole_food_emphasis":74,"meat_quality":74,"organic_sourcing":70,"preparation_excellence":75,
     "median_earnings":78,"alumni_impact":78,"career_placement":79,"grad_school_quality":83,"life_satisfaction":79,
     "gym_quality":90,"nature_access":65,"campus_scenery":65,"city_quality":65,
     "peer_intellectual_caliber":78,"social_vibrancy":80,"peer_attractiveness":70,"dating_social_culture":78},

    {"name":"Indiana University Bloomington","state":"IN","type":"Public",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":65,"preparation_excellence":71,
     "median_earnings":74,"alumni_impact":74,"career_placement":74,"grad_school_quality":80,"life_satisfaction":78,
     "gym_quality":88,"nature_access":62,"campus_scenery":65,"city_quality":55,
     "peer_intellectual_caliber":76,"social_vibrancy":80,"peer_attractiveness":72,"dating_social_culture":78},

    {"name":"Iowa State University","state":"IA","type":"Public",
     "whole_food_emphasis":76,"meat_quality":78,"organic_sourcing":70,"preparation_excellence":76,
     "median_earnings":76,"alumni_impact":74,"career_placement":78,"grad_school_quality":79,"life_satisfaction":78,
     "gym_quality":85,"nature_access":58,"campus_scenery":60,"city_quality":52,
     "peer_intellectual_caliber":77,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":68},

    {"name":"University of Iowa","state":"IA","type":"Public",
     "whole_food_emphasis":70,"meat_quality":70,"organic_sourcing":66,"preparation_excellence":71,
     "median_earnings":74,"alumni_impact":73,"career_placement":74,"grad_school_quality":80,"life_satisfaction":77,
     "gym_quality":85,"nature_access":60,"campus_scenery":62,"city_quality":58,
     "peer_intellectual_caliber":75,"social_vibrancy":75,"peer_attractiveness":68,"dating_social_culture":72},

    {"name":"University of Maryland","state":"MD","type":"Public",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":68,"preparation_excellence":73,
     "median_earnings":82,"alumni_impact":82,"career_placement":82,"grad_school_quality":88,"life_satisfaction":80,
     "gym_quality":88,"nature_access":58,"campus_scenery":65,"city_quality":88,
     "peer_intellectual_caliber":82,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":68},

    {"name":"University of Pittsburgh","state":"PA","type":"Public",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":65,"preparation_excellence":71,
     "median_earnings":80,"alumni_impact":78,"career_placement":79,"grad_school_quality":86,"life_satisfaction":79,
     "gym_quality":80,"nature_access":60,"campus_scenery":70,"city_quality":80,
     "peer_intellectual_caliber":80,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":70},

    {"name":"Rutgers University","state":"NJ","type":"Public",
     "whole_food_emphasis":67,"meat_quality":65,"organic_sourcing":62,"preparation_excellence":68,
     "median_earnings":78,"alumni_impact":77,"career_placement":77,"grad_school_quality":83,"life_satisfaction":75,
     "gym_quality":82,"nature_access":52,"campus_scenery":58,"city_quality":80,
     "peer_intellectual_caliber":76,"social_vibrancy":72,"peer_attractiveness":62,"dating_social_culture":62},

    {"name":"University of Connecticut","state":"CT","type":"Public",
     "whole_food_emphasis":74,"meat_quality":73,"organic_sourcing":70,"preparation_excellence":76,
     "median_earnings":78,"alumni_impact":76,"career_placement":77,"grad_school_quality":82,"life_satisfaction":78,
     "gym_quality":82,"nature_access":65,"campus_scenery":65,"city_quality":55,
     "peer_intellectual_caliber":78,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":68},

    {"name":"University of Delaware","state":"DE","type":"Public",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":67,"preparation_excellence":73,
     "median_earnings":77,"alumni_impact":74,"career_placement":76,"grad_school_quality":80,"life_satisfaction":78,
     "gym_quality":80,"nature_access":60,"campus_scenery":65,"city_quality":65,
     "peer_intellectual_caliber":76,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":68},

    {"name":"Auburn University","state":"AL","type":"Public",
     "whole_food_emphasis":80,"meat_quality":82,"organic_sourcing":72,"preparation_excellence":80,
     "median_earnings":74,"alumni_impact":73,"career_placement":76,"grad_school_quality":77,"life_satisfaction":80,
     "gym_quality":88,"nature_access":62,"campus_scenery":65,"city_quality":55,
     "peer_intellectual_caliber":76,"social_vibrancy":85,"peer_attractiveness":74,"dating_social_culture":80},

    {"name":"University of Alabama","state":"AL","type":"Public",
     "whole_food_emphasis":72,"meat_quality":73,"organic_sourcing":64,"preparation_excellence":72,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":74,"life_satisfaction":76,
     "gym_quality":88,"nature_access":58,"campus_scenery":62,"city_quality":58,
     "peer_intellectual_caliber":74,"social_vibrancy":88,"peer_attractiveness":78,"dating_social_culture":85},

    {"name":"Clemson University","state":"SC","type":"Public",
     "whole_food_emphasis":74,"meat_quality":72,"organic_sourcing":67,"preparation_excellence":74,
     "median_earnings":77,"alumni_impact":74,"career_placement":78,"grad_school_quality":79,"life_satisfaction":80,
     "gym_quality":85,"nature_access":70,"campus_scenery":72,"city_quality":65,
     "peer_intellectual_caliber":80,"social_vibrancy":82,"peer_attractiveness":72,"dating_social_culture":78},

    {"name":"University of Tennessee","state":"TN","type":"Public",
     "whole_food_emphasis":71,"meat_quality":72,"organic_sourcing":64,"preparation_excellence":72,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":75,"life_satisfaction":76,
     "gym_quality":85,"nature_access":72,"campus_scenery":70,"city_quality":65,
     "peer_intellectual_caliber":74,"social_vibrancy":78,"peer_attractiveness":70,"dating_social_culture":75},

    {"name":"University of Missouri","state":"MO","type":"Public",
     "whole_food_emphasis":70,"meat_quality":70,"organic_sourcing":64,"preparation_excellence":71,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":76,"life_satisfaction":75,
     "gym_quality":82,"nature_access":60,"campus_scenery":62,"city_quality":58,
     "peer_intellectual_caliber":73,"social_vibrancy":75,"peer_attractiveness":65,"dating_social_culture":72},

    {"name":"University of Nebraska-Lincoln","state":"NE","type":"Public",
     "whole_food_emphasis":74,"meat_quality":76,"organic_sourcing":66,"preparation_excellence":74,
     "median_earnings":73,"alumni_impact":71,"career_placement":74,"grad_school_quality":76,"life_satisfaction":76,
     "gym_quality":85,"nature_access":60,"campus_scenery":60,"city_quality":62,
     "peer_intellectual_caliber":75,"social_vibrancy":75,"peer_attractiveness":65,"dating_social_culture":70},

    {"name":"Kansas State University","state":"KS","type":"Public",
     "whole_food_emphasis":73,"meat_quality":75,"organic_sourcing":65,"preparation_excellence":73,
     "median_earnings":72,"alumni_impact":70,"career_placement":73,"grad_school_quality":74,"life_satisfaction":75,
     "gym_quality":82,"nature_access":58,"campus_scenery":58,"city_quality":48,
     "peer_intellectual_caliber":73,"social_vibrancy":70,"peer_attractiveness":62,"dating_social_culture":65},

    {"name":"University of Kansas","state":"KS","type":"Public",
     "whole_food_emphasis":68,"meat_quality":68,"organic_sourcing":62,"preparation_excellence":69,
     "median_earnings":70,"alumni_impact":70,"career_placement":70,"grad_school_quality":76,"life_satisfaction":74,
     "gym_quality":82,"nature_access":58,"campus_scenery":62,"city_quality":52,
     "peer_intellectual_caliber":73,"social_vibrancy":72,"peer_attractiveness":63,"dating_social_culture":68},

    {"name":"University of Kentucky","state":"KY","type":"Public",
     "whole_food_emphasis":68,"meat_quality":68,"organic_sourcing":62,"preparation_excellence":69,
     "median_earnings":69,"alumni_impact":68,"career_placement":69,"grad_school_quality":74,"life_satisfaction":73,
     "gym_quality":85,"nature_access":65,"campus_scenery":65,"city_quality":62,
     "peer_intellectual_caliber":73,"social_vibrancy":75,"peer_attractiveness":65,"dating_social_culture":72},

    {"name":"Oklahoma State University","state":"OK","type":"Public",
     "whole_food_emphasis":72,"meat_quality":74,"organic_sourcing":63,"preparation_excellence":72,
     "median_earnings":71,"alumni_impact":69,"career_placement":72,"grad_school_quality":73,"life_satisfaction":74,
     "gym_quality":82,"nature_access":60,"campus_scenery":60,"city_quality":52,
     "peer_intellectual_caliber":73,"social_vibrancy":72,"peer_attractiveness":63,"dating_social_culture":68},

    {"name":"University of Oklahoma","state":"OK","type":"Public",
     "whole_food_emphasis":70,"meat_quality":72,"organic_sourcing":62,"preparation_excellence":70,
     "median_earnings":70,"alumni_impact":69,"career_placement":70,"grad_school_quality":74,"life_satisfaction":73,
     "gym_quality":85,"nature_access":60,"campus_scenery":62,"city_quality":55,
     "peer_intellectual_caliber":73,"social_vibrancy":75,"peer_attractiveness":65,"dating_social_culture":70},

    {"name":"University of Arkansas","state":"AR","type":"Public",
     "whole_food_emphasis":69,"meat_quality":70,"organic_sourcing":61,"preparation_excellence":70,
     "median_earnings":69,"alumni_impact":68,"career_placement":70,"grad_school_quality":72,"life_satisfaction":73,
     "gym_quality":82,"nature_access":65,"campus_scenery":65,"city_quality":55,
     "peer_intellectual_caliber":72,"social_vibrancy":72,"peer_attractiveness":63,"dating_social_culture":68},

    {"name":"Mississippi State University","state":"MS","type":"Public",
     "whole_food_emphasis":69,"meat_quality":70,"organic_sourcing":60,"preparation_excellence":69,
     "median_earnings":67,"alumni_impact":65,"career_placement":67,"grad_school_quality":69,"life_satisfaction":71,
     "gym_quality":78,"nature_access":55,"campus_scenery":55,"city_quality":42,
     "peer_intellectual_caliber":68,"social_vibrancy":68,"peer_attractiveness":58,"dating_social_culture":65},

    {"name":"Louisiana State University","state":"LA","type":"Public",
     "whole_food_emphasis":74,"meat_quality":75,"organic_sourcing":64,"preparation_excellence":76,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":75,"life_satisfaction":77,
     "gym_quality":85,"nature_access":52,"campus_scenery":62,"city_quality":65,
     "peer_intellectual_caliber":72,"social_vibrancy":85,"peer_attractiveness":76,"dating_social_culture":85},

    {"name":"University of South Carolina","state":"SC","type":"Public",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":63,"preparation_excellence":71,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":76,"life_satisfaction":75,
     "gym_quality":85,"nature_access":60,"campus_scenery":65,"city_quality":68,
     "peer_intellectual_caliber":74,"social_vibrancy":78,"peer_attractiveness":70,"dating_social_culture":72},

    {"name":"Colorado State University","state":"CO","type":"Public",
     "whole_food_emphasis":76,"meat_quality":74,"organic_sourcing":74,"preparation_excellence":76,
     "median_earnings":72,"alumni_impact":70,"career_placement":72,"grad_school_quality":76,"life_satisfaction":79,
     "gym_quality":88,"nature_access":88,"campus_scenery":80,"city_quality":65,
     "peer_intellectual_caliber":75,"social_vibrancy":78,"peer_attractiveness":72,"dating_social_culture":75},

    {"name":"North Carolina State University","state":"NC","type":"Public",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":67,"preparation_excellence":72,
     "median_earnings":80,"alumni_impact":77,"career_placement":81,"grad_school_quality":82,"life_satisfaction":79,
     "gym_quality":85,"nature_access":62,"campus_scenery":65,"city_quality":72,
     "peer_intellectual_caliber":82,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"University of New Hampshire","state":"NH","type":"Public",
     "whole_food_emphasis":80,"meat_quality":79,"organic_sourcing":78,"preparation_excellence":81,
     "median_earnings":70,"alumni_impact":68,"career_placement":70,"grad_school_quality":74,"life_satisfaction":78,
     "gym_quality":78,"nature_access":82,"campus_scenery":78,"city_quality":52,
     "peer_intellectual_caliber":74,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":68},

    {"name":"University of Vermont","state":"VT","type":"Public",
     "whole_food_emphasis":82,"meat_quality":80,"organic_sourcing":83,"preparation_excellence":83,
     "median_earnings":70,"alumni_impact":69,"career_placement":69,"grad_school_quality":76,"life_satisfaction":80,
     "gym_quality":80,"nature_access":90,"campus_scenery":88,"city_quality":58,
     "peer_intellectual_caliber":78,"social_vibrancy":75,"peer_attractiveness":68,"dating_social_culture":72},

    {"name":"University of Maine","state":"ME","type":"Public",
     "whole_food_emphasis":79,"meat_quality":78,"organic_sourcing":77,"preparation_excellence":79,
     "median_earnings":67,"alumni_impact":65,"career_placement":67,"grad_school_quality":70,"life_satisfaction":76,
     "gym_quality":72,"nature_access":85,"campus_scenery":78,"city_quality":38,
     "peer_intellectual_caliber":70,"social_vibrancy":65,"peer_attractiveness":58,"dating_social_culture":60},

    {"name":"University of Montana","state":"MT","type":"Public",
     "whole_food_emphasis":73,"meat_quality":74,"organic_sourcing":70,"preparation_excellence":73,
     "median_earnings":60,"alumni_impact":58,"career_placement":60,"grad_school_quality":63,"life_satisfaction":74,
     "gym_quality":75,"nature_access":98,"campus_scenery":96,"city_quality":40,
     "peer_intellectual_caliber":68,"social_vibrancy":68,"peer_attractiveness":65,"dating_social_culture":62},

    {"name":"University of Wyoming","state":"WY","type":"Public",
     "whole_food_emphasis":70,"meat_quality":73,"organic_sourcing":63,"preparation_excellence":70,
     "median_earnings":65,"alumni_impact":62,"career_placement":66,"grad_school_quality":66,"life_satisfaction":72,
     "gym_quality":78,"nature_access":96,"campus_scenery":90,"city_quality":38,
     "peer_intellectual_caliber":70,"social_vibrancy":65,"peer_attractiveness":60,"dating_social_culture":58},

    {"name":"University of Nevada, Reno","state":"NV","type":"Public",
     "whole_food_emphasis":65,"meat_quality":63,"organic_sourcing":59,"preparation_excellence":65,
     "median_earnings":68,"alumni_impact":65,"career_placement":68,"grad_school_quality":68,"life_satisfaction":70,
     "gym_quality":78,"nature_access":80,"campus_scenery":75,"city_quality":58,
     "peer_intellectual_caliber":68,"social_vibrancy":68,"peer_attractiveness":60,"dating_social_culture":62},

    {"name":"University of New Mexico","state":"NM","type":"Public",
     "whole_food_emphasis":63,"meat_quality":62,"organic_sourcing":59,"preparation_excellence":64,
     "median_earnings":63,"alumni_impact":61,"career_placement":63,"grad_school_quality":66,"life_satisfaction":68,
     "gym_quality":72,"nature_access":78,"campus_scenery":80,"city_quality":52,
     "peer_intellectual_caliber":67,"social_vibrancy":65,"peer_attractiveness":58,"dating_social_culture":58},

    {"name":"West Virginia University","state":"WV","type":"Public",
     "whole_food_emphasis":63,"meat_quality":63,"organic_sourcing":56,"preparation_excellence":63,
     "median_earnings":63,"alumni_impact":60,"career_placement":63,"grad_school_quality":65,"life_satisfaction":67,
     "gym_quality":82,"nature_access":75,"campus_scenery":68,"city_quality":48,
     "peer_intellectual_caliber":65,"social_vibrancy":75,"peer_attractiveness":63,"dating_social_culture":78},

    # ── Additional Strong Private Universities ───────────────────────────────
    {"name":"Brigham Young University","state":"UT","type":"Private",
     "whole_food_emphasis":72,"meat_quality":70,"organic_sourcing":64,"preparation_excellence":73,
     "median_earnings":74,"alumni_impact":76,"career_placement":74,"grad_school_quality":78,"life_satisfaction":82,
     "gym_quality":85,"nature_access":88,"campus_scenery":88,"city_quality":65,
     "peer_intellectual_caliber":80,"social_vibrancy":65,"peer_attractiveness":72,"dating_social_culture":42},

    {"name":"Baylor University","state":"TX","type":"Private",
     "whole_food_emphasis":73,"meat_quality":74,"organic_sourcing":65,"preparation_excellence":74,
     "median_earnings":72,"alumni_impact":72,"career_placement":72,"grad_school_quality":76,"life_satisfaction":80,
     "gym_quality":85,"nature_access":60,"campus_scenery":65,"city_quality":55,
     "peer_intellectual_caliber":78,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":62},

    {"name":"Southern Methodist University","state":"TX","type":"Private",
     "whole_food_emphasis":74,"meat_quality":73,"organic_sourcing":66,"preparation_excellence":76,
     "median_earnings":80,"alumni_impact":80,"career_placement":80,"grad_school_quality":82,"life_satisfaction":82,
     "gym_quality":85,"nature_access":62,"campus_scenery":72,"city_quality":85,
     "peer_intellectual_caliber":82,"social_vibrancy":82,"peer_attractiveness":85,"dating_social_culture":82},

    {"name":"Pepperdine University","state":"CA","type":"Private",
     "whole_food_emphasis":77,"meat_quality":74,"organic_sourcing":74,"preparation_excellence":79,
     "median_earnings":73,"alumni_impact":74,"career_placement":72,"grad_school_quality":77,"life_satisfaction":83,
     "gym_quality":80,"nature_access":80,"campus_scenery":97,"city_quality":85,
     "peer_intellectual_caliber":80,"social_vibrancy":72,"peer_attractiveness":84,"dating_social_culture":68},

    {"name":"Santa Clara University","state":"CA","type":"Private",
     "whole_food_emphasis":76,"meat_quality":73,"organic_sourcing":74,"preparation_excellence":77,
     "median_earnings":80,"alumni_impact":78,"career_placement":80,"grad_school_quality":80,"life_satisfaction":82,
     "gym_quality":80,"nature_access":72,"campus_scenery":75,"city_quality":92,
     "peer_intellectual_caliber":82,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"Gonzaga University","state":"WA","type":"Private",
     "whole_food_emphasis":77,"meat_quality":76,"organic_sourcing":72,"preparation_excellence":79,
     "median_earnings":71,"alumni_impact":71,"career_placement":71,"grad_school_quality":75,"life_satisfaction":81,
     "gym_quality":82,"nature_access":80,"campus_scenery":78,"city_quality":60,
     "peer_intellectual_caliber":78,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"University of Denver","state":"CO","type":"Private",
     "whole_food_emphasis":74,"meat_quality":71,"organic_sourcing":70,"preparation_excellence":75,
     "median_earnings":74,"alumni_impact":73,"career_placement":74,"grad_school_quality":77,"life_satisfaction":79,
     "gym_quality":82,"nature_access":82,"campus_scenery":80,"city_quality":82,
     "peer_intellectual_caliber":78,"social_vibrancy":75,"peer_attractiveness":72,"dating_social_culture":72},

    {"name":"Fordham University","state":"NY","type":"Private",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":63,"preparation_excellence":69,
     "median_earnings":76,"alumni_impact":77,"career_placement":75,"grad_school_quality":79,"life_satisfaction":77,
     "gym_quality":65,"nature_access":28,"campus_scenery":62,"city_quality":92,
     "peer_intellectual_caliber":80,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"Marquette University","state":"WI","type":"Private",
     "whole_food_emphasis":70,"meat_quality":69,"organic_sourcing":65,"preparation_excellence":71,
     "median_earnings":73,"alumni_impact":73,"career_placement":73,"grad_school_quality":77,"life_satisfaction":78,
     "gym_quality":75,"nature_access":55,"campus_scenery":62,"city_quality":72,
     "peer_intellectual_caliber":78,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":62},

    {"name":"Villanova University","state":"PA","type":"Private",
     "whole_food_emphasis":73,"meat_quality":71,"organic_sourcing":68,"preparation_excellence":75,
     "median_earnings":80,"alumni_impact":79,"career_placement":80,"grad_school_quality":82,"life_satisfaction":83,
     "gym_quality":80,"nature_access":58,"campus_scenery":72,"city_quality":82,
     "peer_intellectual_caliber":85,"social_vibrancy":75,"peer_attractiveness":74,"dating_social_culture":70},

    {"name":"Drexel University","state":"PA","type":"Private",
     "whole_food_emphasis":64,"meat_quality":62,"organic_sourcing":59,"preparation_excellence":65,
     "median_earnings":81,"alumni_impact":74,"career_placement":87,"grad_school_quality":78,"life_satisfaction":76,
     "gym_quality":68,"nature_access":50,"campus_scenery":60,"city_quality":85,
     "peer_intellectual_caliber":80,"social_vibrancy":65,"peer_attractiveness":58,"dating_social_culture":55},

    {"name":"American University","state":"DC","type":"Private",
     "whole_food_emphasis":70,"meat_quality":67,"organic_sourcing":68,"preparation_excellence":71,
     "median_earnings":72,"alumni_impact":77,"career_placement":72,"grad_school_quality":78,"life_satisfaction":77,
     "gym_quality":75,"nature_access":48,"campus_scenery":72,"city_quality":92,
     "peer_intellectual_caliber":80,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":68},

    # ── Military Academies ───────────────────────────────────────────────────
    {"name":"United States Military Academy (West Point)","state":"NY","type":"Military",
     "whole_food_emphasis":80,"meat_quality":82,"organic_sourcing":70,"preparation_excellence":80,
     "median_earnings":88,"alumni_impact":92,"career_placement":100,"grad_school_quality":85,"life_satisfaction":85,
     "gym_quality":95,"nature_access":85,"campus_scenery":88,"city_quality":72,
     "peer_intellectual_caliber":90,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":55},

    {"name":"United States Naval Academy","state":"MD","type":"Military",
     "whole_food_emphasis":79,"meat_quality":80,"organic_sourcing":68,"preparation_excellence":79,
     "median_earnings":87,"alumni_impact":91,"career_placement":100,"grad_school_quality":84,"life_satisfaction":84,
     "gym_quality":95,"nature_access":75,"campus_scenery":85,"city_quality":72,
     "peer_intellectual_caliber":90,"social_vibrancy":70,"peer_attractiveness":68,"dating_social_culture":52},

    {"name":"United States Air Force Academy","state":"CO","type":"Military",
     "whole_food_emphasis":80,"meat_quality":81,"organic_sourcing":69,"preparation_excellence":80,
     "median_earnings":88,"alumni_impact":90,"career_placement":100,"grad_school_quality":84,"life_satisfaction":84,
     "gym_quality":95,"nature_access":90,"campus_scenery":93,"city_quality":65,
     "peer_intellectual_caliber":90,"social_vibrancy":70,"peer_attractiveness":68,"dating_social_culture":52},

    # ── HBCUs ────────────────────────────────────────────────────────────────
    {"name":"Howard University","state":"DC","type":"HBCU",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":62,"preparation_excellence":70,
     "median_earnings":72,"alumni_impact":82,"career_placement":72,"grad_school_quality":78,"life_satisfaction":78,
     "gym_quality":68,"nature_access":45,"campus_scenery":68,"city_quality":92,
     "peer_intellectual_caliber":80,"social_vibrancy":85,"peer_attractiveness":78,"dating_social_culture":80},

    {"name":"Spelman College","state":"GA","type":"HBCU",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":64,"preparation_excellence":71,
     "median_earnings":70,"alumni_impact":80,"career_placement":70,"grad_school_quality":80,"life_satisfaction":78,
     "gym_quality":65,"nature_access":52,"campus_scenery":62,"city_quality":85,
     "peer_intellectual_caliber":82,"social_vibrancy":80,"peer_attractiveness":80,"dating_social_culture":65},

    {"name":"Morehouse College","state":"GA","type":"HBCU",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":62,"preparation_excellence":69,
     "median_earnings":70,"alumni_impact":82,"career_placement":70,"grad_school_quality":78,"life_satisfaction":77,
     "gym_quality":65,"nature_access":50,"campus_scenery":62,"city_quality":85,
     "peer_intellectual_caliber":80,"social_vibrancy":83,"peer_attractiveness":72,"dating_social_culture":72},

    {"name":"Hampton University","state":"VA","type":"HBCU",
     "whole_food_emphasis":67,"meat_quality":65,"organic_sourcing":61,"preparation_excellence":68,
     "median_earnings":66,"alumni_impact":72,"career_placement":66,"grad_school_quality":70,"life_satisfaction":73,
     "gym_quality":65,"nature_access":62,"campus_scenery":65,"city_quality":68,
     "peer_intellectual_caliber":72,"social_vibrancy":72,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"Florida A&M University","state":"FL","type":"HBCU",
     "whole_food_emphasis":65,"meat_quality":64,"organic_sourcing":59,"preparation_excellence":66,
     "median_earnings":65,"alumni_impact":70,"career_placement":66,"grad_school_quality":68,"life_satisfaction":71,
     "gym_quality":68,"nature_access":55,"campus_scenery":58,"city_quality":62,
     "peer_intellectual_caliber":68,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":68},

    {"name":"North Carolina A&T State University","state":"NC","type":"HBCU",
     "whole_food_emphasis":65,"meat_quality":64,"organic_sourcing":58,"preparation_excellence":65,
     "median_earnings":67,"alumni_impact":68,"career_placement":68,"grad_school_quality":68,"life_satisfaction":70,
     "gym_quality":65,"nature_access":58,"campus_scenery":58,"city_quality":68,
     "peer_intellectual_caliber":68,"social_vibrancy":70,"peer_attractiveness":60,"dating_social_culture":62},

    {"name":"Tuskegee University","state":"AL","type":"HBCU",
     "whole_food_emphasis":67,"meat_quality":68,"organic_sourcing":60,"preparation_excellence":67,
     "median_earnings":63,"alumni_impact":72,"career_placement":64,"grad_school_quality":67,"life_satisfaction":70,
     "gym_quality":62,"nature_access":55,"campus_scenery":55,"city_quality":42,
     "peer_intellectual_caliber":65,"social_vibrancy":68,"peer_attractiveness":58,"dating_social_culture":58},

    {"name":"Xavier University of Louisiana","state":"LA","type":"HBCU",
     "whole_food_emphasis":65,"meat_quality":64,"organic_sourcing":59,"preparation_excellence":66,
     "median_earnings":64,"alumni_impact":73,"career_placement":65,"grad_school_quality":72,"life_satisfaction":71,
     "gym_quality":62,"nature_access":40,"campus_scenery":58,"city_quality":82,
     "peer_intellectual_caliber":72,"social_vibrancy":75,"peer_attractiveness":62,"dating_social_culture":65},

    # ── Additional Notable Schools ───────────────────────────────────────────
    {"name":"Babson College","state":"MA","type":"Private",
     "whole_food_emphasis":71,"meat_quality":69,"organic_sourcing":66,"preparation_excellence":73,
     "median_earnings":88,"alumni_impact":86,"career_placement":88,"grad_school_quality":82,"life_satisfaction":83,
     "gym_quality":78,"nature_access":60,"campus_scenery":68,"city_quality":88,
     "peer_intellectual_caliber":82,"social_vibrancy":68,"peer_attractiveness":65,"dating_social_culture":62},

    {"name":"Bentley University","state":"MA","type":"Private",
     "whole_food_emphasis":68,"meat_quality":66,"organic_sourcing":63,"preparation_excellence":69,
     "median_earnings":85,"alumni_impact":78,"career_placement":87,"grad_school_quality":76,"life_satisfaction":80,
     "gym_quality":78,"nature_access":58,"campus_scenery":65,"city_quality":88,
     "peer_intellectual_caliber":78,"social_vibrancy":68,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"Bucknell University","state":"PA","type":"Private",
     "whole_food_emphasis":76,"meat_quality":75,"organic_sourcing":72,"preparation_excellence":78,
     "median_earnings":80,"alumni_impact":78,"career_placement":80,"grad_school_quality":82,"life_satisfaction":83,
     "gym_quality":80,"nature_access":68,"campus_scenery":72,"city_quality":42,
     "peer_intellectual_caliber":82,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":70},

    {"name":"Lafayette College","state":"PA","type":"Private",
     "whole_food_emphasis":74,"meat_quality":73,"organic_sourcing":70,"preparation_excellence":76,
     "median_earnings":79,"alumni_impact":77,"career_placement":79,"grad_school_quality":80,"life_satisfaction":82,
     "gym_quality":78,"nature_access":65,"campus_scenery":70,"city_quality":55,
     "peer_intellectual_caliber":80,"social_vibrancy":70,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"Gettysburg College","state":"PA","type":"Private",
     "whole_food_emphasis":75,"meat_quality":74,"organic_sourcing":71,"preparation_excellence":76,
     "median_earnings":74,"alumni_impact":73,"career_placement":73,"grad_school_quality":78,"life_satisfaction":81,
     "gym_quality":75,"nature_access":65,"campus_scenery":72,"city_quality":50,
     "peer_intellectual_caliber":78,"social_vibrancy":70,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"Muhlenberg College","state":"PA","type":"Private",
     "whole_food_emphasis":73,"meat_quality":71,"organic_sourcing":69,"preparation_excellence":74,
     "median_earnings":71,"alumni_impact":70,"career_placement":71,"grad_school_quality":76,"life_satisfaction":79,
     "gym_quality":72,"nature_access":60,"campus_scenery":65,"city_quality":60,
     "peer_intellectual_caliber":76,"social_vibrancy":68,"peer_attractiveness":62,"dating_social_culture":60},

    {"name":"Wheaton College (MA)","state":"MA","type":"Private",
     "whole_food_emphasis":83,"meat_quality":80,"organic_sourcing":82,"preparation_excellence":84,
     "median_earnings":68,"alumni_impact":68,"career_placement":66,"grad_school_quality":76,"life_satisfaction":82,
     "gym_quality":70,"nature_access":62,"campus_scenery":68,"city_quality":50,
     "peer_intellectual_caliber":78,"social_vibrancy":65,"peer_attractiveness":65,"dating_social_culture":58},

    {"name":"College of William & Mary","state":"VA","type":"Public",
     "whole_food_emphasis":76,"meat_quality":74,"organic_sourcing":72,"preparation_excellence":78,
     "median_earnings":80,"alumni_impact":82,"career_placement":79,"grad_school_quality":87,"life_satisfaction":84,
     "gym_quality":82,"nature_access":65,"campus_scenery":78,"city_quality":58,
     "peer_intellectual_caliber":88,"social_vibrancy":72,"peer_attractiveness":70,"dating_social_culture":68},

    {"name":"University of Richmond","state":"VA","type":"Private",
     "whole_food_emphasis":78,"meat_quality":77,"organic_sourcing":74,"preparation_excellence":80,
     "median_earnings":81,"alumni_impact":80,"career_placement":80,"grad_school_quality":83,"life_satisfaction":85,
     "gym_quality":85,"nature_access":70,"campus_scenery":78,"city_quality":75,
     "peer_intellectual_caliber":82,"social_vibrancy":74,"peer_attractiveness":73,"dating_social_culture":72},

    {"name":"Rhodes College","state":"TN","type":"Private",
     "whole_food_emphasis":76,"meat_quality":76,"organic_sourcing":70,"preparation_excellence":78,
     "median_earnings":70,"alumni_impact":71,"career_placement":69,"grad_school_quality":79,"life_satisfaction":81,
     "gym_quality":78,"nature_access":52,"campus_scenery":65,"city_quality":70,
     "peer_intellectual_caliber":80,"social_vibrancy":70,"peer_attractiveness":68,"dating_social_culture":65},

    {"name":"Sewanee: The University of the South","state":"TN","type":"Private",
     "whole_food_emphasis":79,"meat_quality":78,"organic_sourcing":75,"preparation_excellence":80,
     "median_earnings":67,"alumni_impact":71,"career_placement":66,"grad_school_quality":78,"life_satisfaction":82,
     "gym_quality":75,"nature_access":85,"campus_scenery":90,"city_quality":38,
     "peer_intellectual_caliber":80,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":62},

    {"name":"Centre College","state":"KY","type":"Private",
     "whole_food_emphasis":76,"meat_quality":75,"organic_sourcing":70,"preparation_excellence":77,
     "median_earnings":70,"alumni_impact":71,"career_placement":69,"grad_school_quality":78,"life_satisfaction":80,
     "gym_quality":72,"nature_access":62,"campus_scenery":65,"city_quality":45,
     "peer_intellectual_caliber":80,"social_vibrancy":68,"peer_attractiveness":62,"dating_social_culture":60},

    {"name":"Denison University","state":"OH","type":"Private",
     "whole_food_emphasis":79,"meat_quality":77,"organic_sourcing":75,"preparation_excellence":80,
     "median_earnings":72,"alumni_impact":73,"career_placement":71,"grad_school_quality":79,"life_satisfaction":82,
     "gym_quality":75,"nature_access":62,"campus_scenery":68,"city_quality":50,
     "peer_intellectual_caliber":80,"social_vibrancy":70,"peer_attractiveness":66,"dating_social_culture":65},

    {"name":"DePauw University","state":"IN","type":"Private",
     "whole_food_emphasis":74,"meat_quality":73,"organic_sourcing":69,"preparation_excellence":75,
     "median_earnings":71,"alumni_impact":73,"career_placement":70,"grad_school_quality":78,"life_satisfaction":79,
     "gym_quality":72,"nature_access":58,"campus_scenery":62,"city_quality":40,
     "peer_intellectual_caliber":78,"social_vibrancy":68,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"Whitman College","state":"WA","type":"Private",
     "whole_food_emphasis":81,"meat_quality":78,"organic_sourcing":80,"preparation_excellence":82,
     "median_earnings":68,"alumni_impact":72,"career_placement":66,"grad_school_quality":82,"life_satisfaction":84,
     "gym_quality":70,"nature_access":82,"campus_scenery":80,"city_quality":42,
     "peer_intellectual_caliber":85,"social_vibrancy":68,"peer_attractiveness":68,"dating_social_culture":62},

    {"name":"Colorado College","state":"CO","type":"Private",
     "whole_food_emphasis":79,"meat_quality":75,"organic_sourcing":79,"preparation_excellence":80,
     "median_earnings":68,"alumni_impact":71,"career_placement":66,"grad_school_quality":79,"life_satisfaction":82,
     "gym_quality":80,"nature_access":95,"campus_scenery":90,"city_quality":65,
     "peer_intellectual_caliber":82,"social_vibrancy":75,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"University of Puget Sound","state":"WA","type":"Private",
     "whole_food_emphasis":77,"meat_quality":74,"organic_sourcing":76,"preparation_excellence":78,
     "median_earnings":64,"alumni_impact":66,"career_placement":63,"grad_school_quality":73,"life_satisfaction":79,
     "gym_quality":70,"nature_access":85,"campus_scenery":80,"city_quality":68,
     "peer_intellectual_caliber":78,"social_vibrancy":65,"peer_attractiveness":63,"dating_social_culture":60},

    {"name":"Stony Brook University","state":"NY","type":"Public",
     "whole_food_emphasis":66,"meat_quality":64,"organic_sourcing":61,"preparation_excellence":66,
     "median_earnings":80,"alumni_impact":77,"career_placement":79,"grad_school_quality":86,"life_satisfaction":76,
     "gym_quality":80,"nature_access":60,"campus_scenery":62,"city_quality":72,
     "peer_intellectual_caliber":80,"social_vibrancy":62,"peer_attractiveness":58,"dating_social_culture":55},

    {"name":"University at Buffalo","state":"NY","type":"Public",
     "whole_food_emphasis":63,"meat_quality":61,"organic_sourcing":58,"preparation_excellence":63,
     "median_earnings":76,"alumni_impact":72,"career_placement":75,"grad_school_quality":80,"life_satisfaction":72,
     "gym_quality":80,"nature_access":55,"campus_scenery":55,"city_quality":65,
     "peer_intellectual_caliber":72,"social_vibrancy":65,"peer_attractiveness":58,"dating_social_culture":60},

    {"name":"George Washington University","state":"DC","type":"Private",
     "whole_food_emphasis":68,"meat_quality":65,"organic_sourcing":65,"preparation_excellence":70,
     "median_earnings":79,"alumni_impact":82,"career_placement":78,"grad_school_quality":82,"life_satisfaction":78,
     "gym_quality":72,"nature_access":45,"campus_scenery":72,"city_quality":92,
     "peer_intellectual_caliber":82,"social_vibrancy":75,"peer_attractiveness":72,"dating_social_culture":70},

    {"name":"Rollins College","state":"FL","type":"Private",
     "whole_food_emphasis":74,"meat_quality":72,"organic_sourcing":68,"preparation_excellence":75,
     "median_earnings":70,"alumni_impact":70,"career_placement":69,"grad_school_quality":73,"life_satisfaction":79,
     "gym_quality":75,"nature_access":65,"campus_scenery":75,"city_quality":72,
     "peer_intellectual_caliber":74,"social_vibrancy":72,"peer_attractiveness":72,"dating_social_culture":68},

    {"name":"University of San Diego","state":"CA","type":"Private",
     "whole_food_emphasis":74,"meat_quality":71,"organic_sourcing":71,"preparation_excellence":75,
     "median_earnings":72,"alumni_impact":72,"career_placement":71,"grad_school_quality":74,"life_satisfaction":79,
     "gym_quality":78,"nature_access":82,"campus_scenery":90,"city_quality":85,
     "peer_intellectual_caliber":76,"social_vibrancy":72,"peer_attractiveness":78,"dating_social_culture":75},

    {"name":"Loyola University Chicago","state":"IL","type":"Private",
     "whole_food_emphasis":69,"meat_quality":67,"organic_sourcing":64,"preparation_excellence":70,
     "median_earnings":71,"alumni_impact":71,"career_placement":71,"grad_school_quality":76,"life_satisfaction":76,
     "gym_quality":70,"nature_access":48,"campus_scenery":65,"city_quality":88,
     "peer_intellectual_caliber":76,"social_vibrancy":72,"peer_attractiveness":65,"dating_social_culture":65},

    {"name":"Seton Hall University","state":"NJ","type":"Private",
     "whole_food_emphasis":62,"meat_quality":60,"organic_sourcing":57,"preparation_excellence":62,
     "median_earnings":74,"alumni_impact":71,"career_placement":73,"grad_school_quality":74,"life_satisfaction":72,
     "gym_quality":68,"nature_access":42,"campus_scenery":55,"city_quality":82,
     "peer_intellectual_caliber":72,"social_vibrancy":65,"peer_attractiveness":58,"dating_social_culture":58},

    # ── New additions v2.1 ───────────────────────────────────────────────────
    {"name":"University of Miami","state":"FL","type":"Private",
     "whole_food_emphasis":70,"meat_quality":68,"organic_sourcing":64,"preparation_excellence":72,
     "median_earnings":76,"alumni_impact":80,"career_placement":76,"grad_school_quality":78,"life_satisfaction":84,
     "gym_quality":88,"nature_access":85,"campus_scenery":85,"city_quality":92,
     "peer_intellectual_caliber":78,"social_vibrancy":93,"peer_attractiveness":93,"dating_social_culture":92},

    {"name":"Texas Christian University","state":"TX","type":"Private",
     "whole_food_emphasis":72,"meat_quality":74,"organic_sourcing":63,"preparation_excellence":73,
     "median_earnings":72,"alumni_impact":74,"career_placement":73,"grad_school_quality":73,"life_satisfaction":81,
     "gym_quality":88,"nature_access":60,"campus_scenery":78,"city_quality":80,
     "peer_intellectual_caliber":78,"social_vibrancy":84,"peer_attractiveness":88,"dating_social_culture":84},

    {"name":"Loyola Marymount University","state":"CA","type":"Private",
     "whole_food_emphasis":72,"meat_quality":68,"organic_sourcing":70,"preparation_excellence":73,
     "median_earnings":74,"alumni_impact":74,"career_placement":74,"grad_school_quality":74,"life_satisfaction":82,
     "gym_quality":78,"nature_access":72,"campus_scenery":85,"city_quality":88,
     "peer_intellectual_caliber":76,"social_vibrancy":76,"peer_attractiveness":80,"dating_social_culture":76},
]


HEADER_LINE = "=" * 110


def print_section(title: str) -> None:
    print(f"\n{HEADER_LINE}\n  {title}\n{HEADER_LINE}")


def print_top_n(universities: List[University], n: int, key: str, label: str) -> None:
    print_section(f"TOP {n} — {label}")
    top = sorted(universities, key=lambda u: getattr(u, key), reverse=True)[:n]
    print(f"{'Rank':<6} {'University':<52} {'State':<6} {'Score':>7}")
    print("-" * 78)
    for i, u in enumerate(top, 1):
        print(f"{i:<6} {u.name:<52} {u.state:<6} {getattr(u, key):>7.1f}")


def print_full_rankings(universities: List[University]) -> None:
    print_section("FREMIAN INDEX — COMPLETE RANKINGS (all four pillars)")
    print(
        f"{'Rk':<4} {'University':<45} {'St':<4} {'Type':<9}"
        f" {'FQS':>5} {'LSS':>5} {'PES':>5} {'SSS':>5} {'FI':>6}"
    )
    print("-" * 95)
    for u in universities:
        print(
            f"{u.overall_rank:<4} {u.name:<45} {u.state:<4} {u.type:<9}"
            f" {u.food_quality_score:>5.1f} {u.life_success_score:>5.1f}"
            f" {u.physical_env_score:>5.1f} {u.social_scene_score:>5.1f}"
            f" {u.fremian_index:>6.1f}"
        )


def save_csv(universities: List[University], path: str) -> None:
    fields = [
        "overall_rank","name","state","type",
        "food_quality_score","food_rank",
        "whole_food_emphasis","meat_quality","organic_sourcing","preparation_excellence",
        "life_success_score","success_rank",
        "median_earnings","alumni_impact","career_placement","grad_school_quality","life_satisfaction",
        "physical_env_score","physical_rank",
        "gym_quality","nature_access","campus_scenery","city_quality","weather_climate",
        "social_scene_score","social_rank",
        "peer_intellectual_caliber","social_vibrancy","peer_attractiveness","dating_social_culture",
        "fremian_index",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for u in universities:
            row = asdict(u)
            writer.writerow({k: row[k] for k in fields})
    print(f"\nCSV saved → {path}")


def save_json(universities: List[University], path: str) -> None:
    with open(path, "w") as f:
        json.dump([asdict(u) for u in universities], f, indent=2)
    print(f"JSON saved → {path}")


def main() -> None:
    universities = [University(**d) for d in RAW_DATA]
    ranked = compute_scores(universities)

    print(f"\n{HEADER_LINE}")
    print("  FREMIAN UNIVERSITY INDEX  v3.2")
    print("  LSS 50%  |  SSS 30%  |  FQS 15%  |  PES 5%")
    print("  SSS: Peer Attractiveness 40% | Social Vibrancy 30% | Peer Intellect 20% | Dating Culture 10%")
    print(f"  Fremian Index = 0.50×LSS + 0.30×SSS + 0.15×FQS + 0.05×PES")
    print(HEADER_LINE)

    print_top_n(ranked, 25, "fremian_index",       "FREMIAN INDEX  (Overall)")
    print_top_n(ranked, 25, "food_quality_score",  "FOOD HALL QUALITY SCORE  (FQS)")
    print_top_n(ranked, 25, "life_success_score",  "LIFE PREPAREDNESS & SUCCESS  (LSS)")
    print_top_n(ranked, 25, "physical_env_score",  "PHYSICAL ENVIRONMENT  (PES)")
    print_top_n(ranked, 25, "social_scene_score",  "SOCIAL SCENE  (SSS) — attractive peers · vibrancy · genius · dating")
    print_top_n(ranked, 25, "peer_attractiveness", "PEER ATTRACTIVENESS  (raw sub-score)")

    print_full_rankings(ranked)

    save_csv(ranked, "fremian_university_rankings.csv")
    save_json(ranked, "fremian_university_rankings.json")

    print_section("METHODOLOGY")
    print("""
PILLAR WEIGHTS
     LSS  Life Success              50%  earnings + alumni network
     SSS  Social Scene              30%  beautiful people, fun, vibe, dating
     FQS  Food Hall Quality         15%  whole food, organic, grass-fed meats
     PES  Physical Environment       5%  nature, weather, campus, city

FQS  Food Hall Quality Score
     organic_sourcing       35%  certified organic, local-farm, regenerative sourcing
     whole_food_emphasis    30%  whole-food-first, unprocessed, nutrient-dense menus
     meat_quality           25%  grass-fed beef, pastured poultry, wild-caught fish
     preparation_excellence 10%  chef-led kitchens, fresh daily prep, seasonal variety

LSS  Life Success Score
     median_earnings        50%  median salary 5-10 yrs out (College Scorecard)
     alumni_impact          40%  CEOs, executives, Forbes lists — who your network becomes
     career_placement       10%  % placed at top companies within 6 months of graduation

PES  Physical Environment Score
     nature_access          25%  hiking, mountains, beaches, parks nearby
     campus_scenery         20%  breathtaking architecture, landscapes, views
     city_quality           20%  proximity to a vibrant city with jobs and culture
     weather_climate        20%  year-round livability — sunshine, warmth, outdoor days
     gym_quality            15%  rec-center quality, pools, weight rooms, courts

SSS  Social Scene Score  (DATA SOURCES: Niche.com ratings, Reddit r/college consensus,
     Greek life density, Thrillist/Complex/media "hottest campus" rankings, social media culture)
     peer_attractiveness        40%  physical appearance culture — "hot school" media rep
     social_vibrancy            30%  fun events, nightlife, energy, party scene
     peer_intellectual_caliber  20%  genius factor — admit rates & SAT/ACT ranges
     dating_social_culture      10%  hookup culture, Greek life, ease of dating
""".strip())


if __name__ == "__main__":
    main()
