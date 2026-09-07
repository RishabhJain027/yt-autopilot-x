import pytest
import sys, os
sys.path.insert(0, '.')
from python.pipelines.state_machine import StateEngine, ProductionState

def test_state_machine_stages_count():
    states = list(ProductionState)
    assert len(states) == 28, f"ProductionState must have exactly 28 stages, found {len(states)}"

def test_valid_transition():
    engine = StateEngine()
    next_state = engine.validate_transition(ProductionState.DISCOVERY_QUEUED, ProductionState.NICHE_ANALYZING)
    assert next_state == ProductionState.NICHE_ANALYZING

def test_invalid_transition_raises():
    engine = StateEngine()
    with pytest.raises(ValueError):
        engine.validate_transition(ProductionState.DISCOVERY_QUEUED, ProductionState.PUBLISHED_PUBLIC)

def test_quality_gate_transitions():
    engine = StateEngine()
    next_s = engine.validate_transition(ProductionState.QUALITY_GATE_CHECKING, ProductionState.QUALITY_GATE_PASSED)
    assert next_s == ProductionState.QUALITY_GATE_PASSED

