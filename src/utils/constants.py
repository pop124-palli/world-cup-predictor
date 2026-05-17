"""
All magic numbers live here. Change once — affects the whole project.
"""

# ELO K-factors per tournament importance
K_FACTORS = {
    "FIFA World Cup": 40,
    "FIFA World Cup qualification": 30,
    "UEFA Euro": 35,
    "UEFA Euro qualification": 28,
    "Copa América": 35,
    "AFC Asian Cup": 30,
    "Africa Cup of Nations": 30,
    "Friendly": 15,
    "default": 20,
}

# Home ground advantage (added to home team ELO before expected score calc)
HOME_ELO_BONUS = 100

# Starting ELO for every team
DEFAULT_ELO = 1500

# How many recent matches to use for form
FORM_WINDOW = 5

# Weighted decay for recent matches (most recent first)
FORM_DECAY_WEIGHTS = [0.35, 0.25, 0.20, 0.12, 0.08]

# Position importance weights (must sum to 1.0)
POSITION_WEIGHTS = {
    "GK":  0.15,
    "CB":  0.12,
    "LB":  0.08,
    "RB":  0.08,
    "CDM": 0.10,
    "CM":  0.09,
    "CAM": 0.10,
    "LW":  0.07,
    "RW":  0.07,
    "ST":  0.14,
}

# Squad selection weights
STARTER_WEIGHT = 0.85
BENCH_WEIGHT   = 0.15

# Average squad strength and form (used to normalise deltas)
AVG_SQUAD_STRENGTH = 70.0
AVG_FORM_SCORE     = 6.5

# ELO boost per squad-strength point above average
SQUAD_ELO_SCALE = 3.0

# ELO boost per form point above average
FORM_ELO_SCALE = 10.0

# Known star players per national team
STAR_PLAYERS = {
    "Brazil":      ["Vinicius Jr", "Rodrygo"],
    "France":      ["Kylian Mbappe", "Antoine Griezmann"],
    "Argentina":   ["Lionel Messi", "Julian Alvarez"],
    "England":     ["Jude Bellingham", "Harry Kane"],
    "Spain":       ["Pedri", "Lamine Yamal"],
    "Germany":     ["Florian Wirtz", "Jamal Musiala"],
    "Portugal":    ["Cristiano Ronaldo", "Bruno Fernandes"],
    "Netherlands": ["Virgil van Dijk", "Cody Gakpo"],
    "Belgium":     ["Kevin De Bruyne", "Romelu Lukaku"],
    "Italy":       ["Federico Chiesa", "Nicolo Barella"],
}
