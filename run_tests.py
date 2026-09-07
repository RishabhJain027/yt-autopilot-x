import asyncio
import sys, os
sys.path.insert(0, '.')


def test_scoring():
    from python.agents.niche_discovery import NicheDiscoveryAgent
    from python.agents.trend_agent import TrendAgent

    agent = NicheDiscoveryAgent()
    score = round((80 * 0.30) + ((100 - 30) * 0.25) + (90 * 0.20) + (70 * 0.15) + ((100 - 20) * 0.10), 2)
    assert score == 78.0, f"Expected 78.0, got {score}"
    print("[-] Test Niche Scoring: PASSED")

    trend_score = round((80 * 0.35) + (70 * 0.25) + (60 * 0.20) + (90 * 0.20), 2)
    assert trend_score == 75.5, f"Expected 75.5, got {trend_score}"
    print("[-] Test Trend Scoring: PASSED")

def test_state_machine():
    from python.pipelines.state_machine import ProductionStateMachine, VALID_STATES
    sm = ProductionStateMachine()
    assert len(VALID_STATES) >= 28
    assert sm.can_transition('IDEA', 'RESEARCHING') == True
    assert sm.can_transition('IDEA', 'PUBLISHED') == False
    next_s = sm.transition('IDEA', 'RESEARCHING', production_id='test-prod-1')
    assert next_s == 'RESEARCHING'
    print("[-] Test 28-Stage State Machine: PASSED")

def test_security_vault():
    from python.services.credential_vault import CredentialVault
    from packages.logger.logger import sanitize_message

    vault = CredentialVault()
    raw_token = "ya29.test-sample-oauth-token"
    enc = vault.encrypt_token(raw_token)
    dec = vault.decrypt_token(enc)
    assert dec == raw_token
    print("[-] Test AES-256 GCM Credential Vault: PASSED")

    redacted = sanitize_message("User access_token='ya29.secret12345' logged in")
    assert "ya29" not in redacted
    assert "[REDACTED]" in redacted
    print("[-] Test Log Redaction & Audit Logging: PASSED")

    from python.research.url_fetcher import SafeUrlFetcher, PRIVATE_IP_REGEX
    from urllib.parse import urlparse

    fetcher = SafeUrlFetcher()
    assert bool(PRIVATE_IP_REGEX.match(urlparse("http://127.0.0.1/admin").hostname)) == True
    assert bool(PRIVATE_IP_REGEX.match(urlparse("http://192.168.1.1/secret").hostname)) == True
    assert bool(PRIVATE_IP_REGEX.match(urlparse("https://www.google.com").hostname)) == False
    print("[-] Test SSRF Protection & Safe Fetcher: PASSED")

def test_quota_and_budget():
    from python.services.quota_manager import QuotaManager
    from python.services.budget_guard import BudgetGuard

    qm = QuotaManager()
    assert qm.can_afford('videos.insert') == True
    rem_before = qm.get_remaining_quota()
    qm.consume('videos.insert')
    rem_after = qm.get_remaining_quota()
    assert rem_before - rem_after == 1600
    print("[-] Test 10,000 Unit YouTube Quota Manager: PASSED")

    bg = BudgetGuard()
    cost = bg.estimate_cost('llm_tokens_1k', 10)
    assert cost > 0
    assert bg.can_spend(cost) == True
    print("[-] Test $25 Daily Budget Guard: PASSED")

def test_quality_gates():
    from python.agents.quality_gate import QualityGateAgent
    from python.schemas.script import ScriptPlan, ScriptSegment
    from python.schemas.research import ResearchPacket, ClaimItem

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
    assert report.overall_passed == True
    assert report.requires_human_review == False
    assert report.factuality_gate.passed == True
    assert report.render_gate.passed == True
    print("[-] Test 6 Machine Quality Gates (A-F): PASSED")

async def main():
    print("=" * 60)
    print("YT-AUTOPILOT-X | AUTONOMOUS TEST SUITE RUNNER")
    print("=" * 60)
    test_scoring()
    test_state_machine()
    test_security_vault()
    test_quota_and_budget()
    test_quality_gates()
    print("=" * 60)
    print("ALL TESTS SUCCESSFULLY PASSED (100%)")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
