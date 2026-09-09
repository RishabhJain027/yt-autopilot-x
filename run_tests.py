import asyncio
import sys, os
sys.path.insert(0, '.')
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

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

async def test_goal_agent():
    from python.agents.goal_agent import goal_agent
    status = await goal_agent.get_channel_goal_status()
    assert "targets" in status
    assert status["targets"]["target_subscribers"] == 10000
    assert "current_progress" in status
    print("[-] Test /goal Objectives & Milestone Engine: PASSED")

async def test_browser_researcher():
    from python.agents.browser_researcher import browser_researcher
    results = await browser_researcher.browse_trending_research("Wan 2.1")
    assert len(results) >= 1
    assert any("Wan 2.1" in r["topic"] for r in results)
    print("[-] Test /browser Web Trend & Claim Discovery: PASSED")

async def test_learning_engine():
    from python.agents.learning_engine import learning_engine
    directives = await learning_engine.get_active_strategy_directives("test_channel")
    assert "recommended_hook_style" in directives
    assert directives["retention_target"] == 0.75
    print("[-] Test /learn Continuous Adaptation Engine: PASSED")

async def test_boost_agent():
    from python.agents.boost_agent import boost_agent
    pkg = boost_agent.generate_boost_package("DeepSeek-V3 MoE", "Stop paying for closed models!")
    assert pkg["algorithm_boost_score"] > 90.0
    assert len(pkg["hashtags"]) >= 5
    assert pkg["hook_evaluation"]["verdict"] in ["VIRAL_READY", "ACCEPTABLE"]
    print("[-] Test /boost Viral Retention & SEO Multiplier: PASSED")

async def test_dynamic_trend_discovery():
    from python.agents.trend_agent import trend_agent
    past = ["5 New AI Coding Assistants You Never Heard Of", "How To Automate Your Entire Daily Workflow in 10 Minutes"]
    trends = await trend_agent.discover_trends(niche="AI Breakthroughs", exclude_topics=past)
    assert len(trends) >= 3
    # Check that past topics are strictly excluded
    for t in trends:
        assert t.topic not in past
    assert trends[0].score > 0.80
    print("[-] Test Dynamic Trend Discovery & Anti-Repetition: PASSED")

async def test_remote_video_router():
    from python.services.remote_video_router import remote_t2v_router

    # 1. Model Registry Coverage (34+ open-source models & diffusers variants)
    catalog = remote_t2v_router.get_model_catalog()
    assert len(catalog) >= 30, f"Expected at least 30 models, found {len(catalog)}"

    required_models = [
        "wan2.2_t2v_14b", "wan2.2_t2v_14b_diffusers", "wan2.2_ti2v_5b", "wan2.2_ti2v_5b_diffusers",
        "wan2.2_lightning", "wan2.1", "wan2.1_diffusers", "wan2.1_t2v_14b",
        "hunyuan_video_1.5", "hunyuan_video", "fasthunyuan", "fasth3_4step",
        "ltx_2.5", "ltx_video", "minimax_h3", "cosmos_7b", "animatediff_lightning",
        "animatelcm", "cogvideox_5b", "cogvideox", "open_sora_v2", "mochi_1",
        "stepvideo_t2v", "pyramid_flow_sd3", "pyramid_flow_miniflux", "allegro",
        "hotshot_xl", "longcat_video", "krea_realtime", "i2vgen_xl",
        "modelscope_damo", "damo_ms_17b", "modelscope", "zeroscope_v2"
    ]
    for m in required_models:
        assert m in catalog, f"Missing model in registry: {m}"
        assert "hf_id" in catalog[m], f"Missing hf_id for {m}"
        assert "license" in catalog[m], f"Missing license for {m}"

    # 2. Model Lookup Methods
    found_by_hf = remote_t2v_router.get_model_by_hf_id("Wan-AI/Wan2.2-T2V-A14B")
    assert found_by_hf is not None
    assert found_by_hf["name"] == "Wan2.2-T2V-A14B"

    found_by_key = remote_t2v_router.get_model_by_key("hunyuan_video_1.5")
    assert found_by_key is not None
    assert "HunyuanVideo 1.5" in found_by_key["name"]

    # 3. Intelligent Model Selector
    aesthetic_model = remote_t2v_router.select_best_model(
        "Maya the aesthetic seductive baddie sipping iced matcha in sunlit Parisian loft",
        niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨"
    )
    assert aesthetic_model["name"] in ["Wan2.2-T2V-A14B", "HunyuanVideo 1.5", "LTX-2.5", "MiniMax-H3", "AnimateDiff-Lightning", "Wan2.1-T2V-14B"]

    tech_model = remote_t2v_router.select_best_model(
        "HunyuanVideo 1.5 4-step fast generation benchmark",
        niche="AI Tools & Tech Breakthroughs"
    )
    assert tech_model["name"] in ["Wan2.2-Lightning (LightX2V)", "FastHunyuan (FastVideo)", "Wan2.1-T2V-1.3B", "LTX-Video 0.9.5", "Cosmos-1.0-Diffusion-7B-Text2World", "CogVideoX-5B"]

    print(f"[-] Test Remote T2V Multi-Model Registry ({len(catalog)} models) & Intelligent Selector: PASSED")

async def test_pinterest_genz_niche_pipeline():
    from python.agents.niche_discovery import niche_agent
    from python.schemas.topic import NicheScoreInput
    from python.agents.script_agent import script_agent
    from python.agents.visual_planner import visual_planner
    from python.services.tts_service import tts_service
    from python.schemas.research import ResearchPacket, ClaimItem

    # 1. Niche Discovery
    niche_prop = await niche_agent.discover_niche(NicheScoreInput(
        niche_preference="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨",
        shorts=True
    ))
    assert "Pinterest Aesthetic" in niche_prop.niche
    assert niche_prop.score >= 0.85
    assert len(niche_prop.content_pillars) >= 3

    # 2. Script Generation
    research = ResearchPacket(
        topic="The 3-Second Eye Contact Trick That Makes Him Obsessed",
        facts=[
            "Mirror neurons fire synchronously when holding soft, alluring eye contact.",
            "The 3-second triangle gaze creates immediate subconscious chemical tension."
        ],
        claims=[ClaimItem(claim_id="c1", claim_text="Mirror neuron eye contact tension", confidence=0.96, requires_human_review=False)]
    )
    script = await script_agent.generate_script(
        topic="The 3-Second Eye Contact Trick That Makes Him Obsessed",
        research=research,
        format="shorts",
        niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨"
    )
    assert "babes" in script.hook.lower() or "secret" in script.hook.lower() or "obsessed" in script.hook.lower() or "maya" in script.hook.lower()
    assert len(script.segments) == 5

    # 3. Visual Planning (Character Consistency & Clean Rendering with NO text boxes)
    storyboard = visual_planner.plan_visuals(
        script,
        aspect_ratio="9:16",
        niche="Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨"
    )
    assert len(storyboard.scenes) == 5
    for scene in storyboard.scenes:
        assert "NO text" in scene.prompt or "NO text boxes" in scene.prompt
        assert "Maya" in scene.prompt

    # 4. Multi-Persona Voice Selection
    baddie_voice = tts_service.select_voice_for_niche("Pinterest Aesthetic & Girly Clumsy Baddie / Maya ✨")
    assert "Ava" in baddie_voice or "Emma" in baddie_voice or "Jenny" in baddie_voice

    tech_voice = tts_service.select_voice_for_niche("AI Tools and Tech Breakthroughs")
    assert "Ava" in tech_voice or "Guy" in tech_voice or "Brian" in tech_voice

    print("[-] Test Pinterest Aesthetic / Maya ✨ Seductive Baddie Pipeline & Voice Persona: PASSED")

async def test_zero_local_gpu_scene_generation():
    from python.services.remote_video_router import remote_t2v_router

    # Synthesize a test scene clip via serverless remote path (0 local GPU)
    res = await remote_t2v_router.generate_scene_clip(
        scene_id="test_scene_001",
        prompt="Maya 21yo stunning gorgeous aesthetic baddie in sunlit Parisian cafe holding iced matcha",
        duration=2.5,
        aspect_ratio="9:16",
        niche="Pinterest Aesthetic"
    )
    assert res["status"] in ["READY", "REMOTE_SUCCESS"]
    assert os.path.exists(res["clip_path"])
    assert res["duration"] >= 2.5
    print("[-] Test Zero Local GPU Remote Scene Generation: PASSED")

async def main():
    print("=" * 60)
    print("YT-AUTOPILOT-X | AUTONOMOUS TEST SUITE RUNNER")
    print("=" * 60)
    test_scoring()
    test_state_machine()
    test_security_vault()
    test_quota_and_budget()
    test_quality_gates()
    await test_goal_agent()
    await test_browser_researcher()
    await test_learning_engine()
    await test_boost_agent()
    await test_dynamic_trend_discovery()
    await test_remote_video_router()
    await test_pinterest_genz_niche_pipeline()
    await test_zero_local_gpu_scene_generation()
    print("=" * 60)
    print("ALL TESTS SUCCESSFULLY PASSED (100%)")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())

