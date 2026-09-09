import pytest
import sys, os
sys.path.insert(0, '.')
from python.services.quota_manager import QuotaManager
from python.services.budget_guard import BudgetGuard

def test_quota_deduction_and_limit():
    mgr = QuotaManager()
    assert mgr.can_afford('videos.insert') is True
    rem_before = mgr.get_remaining_quota()
    mgr.consume('videos.insert')
    rem_after = mgr.get_remaining_quota()
    assert rem_before - rem_after == 1600

def test_budget_guard_daily_limit():
    guard = BudgetGuard()
    cost = guard.estimate_cost('llm_tokens_1k', 10)
    assert cost > 0
    assert guard.can_spend(cost) is True
