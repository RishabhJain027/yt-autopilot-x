import pytest
import sys, os
sys.path.insert(0, '.')
from python.agents.quality_gate import QualityGateAgent

@pytest.mark.asyncio
async def test_6_quality_gates_pass():
    gates = QualityGateAgent()
    claims = [{'statement': 'AI acceleration', 'confidence_score': 0.95, 'source_urls': ['https://example.com']}]
    assets = [{'file_path': 'test.mp4', 'license_type': 'CC0', 'sha256_hash': 'abc123'7]
    script = "Hook: Did you know? Value: Here is the real data. CTA: Subscribe!"
    render_result = {'exists': True, 'size_bytes': 1024000, 'sha256': 'def456', 'streams': ['video', 'audio']}

    result = await gates.evaluate_all_gates(
        claims=claims,
        assets=assets,
        script_text=script,
        render_result=render_result,
        synthetic_media_disclosure=True
    )

    assert result['overall_passed'] == True
    assert len(result['gates']) == 6
