import pytest
import sys, os
sys.path.insert(0, '.')
from python.agents.quality_gate import QualityGateAgent
from python.schemas.script import ScriptPlan, ScriptSegment
from python.schemas.research import ResearchPacket, ClaimItem

def test_6_quality_gates_pass():
    gates = QualityGateAgent()
    script = ScriptPlan(
        title_candidate="AI Breakthrough",
        hook="Hook test",
        context="Context test",
        core_value="Proof test",
        proof="Verified proof",
        payoff="Payoff test",
        cta="Subscribe now",
        segments=[ScriptSegment(id="1", voiceover="Test voiceover", duration=5.0)],
        format="shorts",
        estimated_duration_seconds=45.0
    )
    research = ResearchPacket(
        topic="AI Breakthrough",
        facts=["Fact 1"],
        claims=[ClaimItem(claim_id="c1", claim_text="Test claim", confidence=0.98, requires_human_review=False)],
        sources=[]
    )
    report = gates.validate_production(script=script, research=research, video_exists=True)
    assert report.overall_passed is True
    assert report.requires_human_review is False
    assert report.factuality_gate.passed is True
    assert report.render_gate.passed is True
