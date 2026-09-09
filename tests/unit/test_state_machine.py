import pytest
import sys, os
sys.path.insert(0, '.')
from python.pipelines.state_machine import ProductionStateMachine, VALID_STATES

def test_state_machine_stages_count():
    assert len(VALID_STATES) >= 28, f"VALID_STATES must have at least 28 stages, found {len(VALID_STATES)}"

def test_valid_transition():
    sm = ProductionStateMachine()
    assert sm.can_transition('IDEA', 'RESEARCHING') is True
    next_state = sm.transition('IDEA', 'RESEARCHING', production_id='test-prod-1')
    assert next_state == 'RESEARCHING'

def test_invalid_transition_raises():
    sm = ProductionStateMachine()
    assert sm.can_transition('IDEA', 'PUBLISHED') is False
    with pytest.raises(ValueError):
        sm.transition('IDEA', 'PUBLISHED', production_id='test-prod-1')

