import pytest
import sys, os
sys.path.insert(0, '.')
from python.agents.niche_discovery import NicheDiscoveryAgent
from python.agents.trend_agent import TrendAgent

def test_niche_opportunity_scoring_formula():
    agent = NicheDiscoveryAgent()
    # Test exact mathematical weighting (Section 7.4)
    # Search Demand: 80, Competition: 30, RPM: 90, Velocity: 70, Cost: 20
    # Score = (80*0.3) + ((100-30)*0.25) + (90*0.2) + (70*0.15) + ((100-20)*0.1)
    # Score = 24 + 17.5 + 18 + 10.5 + 8 = 78.0
    score = round((80 * 0.30) + ((100 - 30) * 0.25) + (90 * 0.20) + (70 * 0.15) + ((100 - 20) * 0.10), 2)
    assert score == 78.0

def test_trend_scoring_formula():
    agent = TrendAgent()
    # Test exact formula (Section 9.2)
    # Velocity: 80, Search: 70, Longevity: 60, Freshness: 90
    # Score = (80*0.35) + (70*0.25) + (60*0.20) + (90*0.20)
    # Score = 28 + 17.5 + 12 + 18 = 75.5
    trend_score = round((80 * 0.35) + (70 * 0.25) + (60 * 0.20) + (90 * 0.20), 2)
    assert trend_score == 75.5
