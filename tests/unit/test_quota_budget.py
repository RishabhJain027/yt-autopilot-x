import pytest
import sys, os
sys.path.insert(0, '.')
from python.services.quota_manager import QuotaManager
from python.services.budget_guard import BudgetGuard

def test_quota_deduction_and_limit():
    mgr = QuotaManager(daily_limit=10000)
    assert mgr.get_usage()['remaining'] == 10000
    
    # Upload deducts 1600 units
    assert mgr.check_and_deduct("videos.insert") == True
    assert mgr.get_usage()['used'] == 1600
    assert mgr.get_usage()['usage_percent'] == 16.0

    # Search deducts 100 units
    mgr.check_and_deduct("search.list")
    assert mgr.get_usage()['used'] == 1700

def test_budget_guard_daily_limit():
    guard = BudgetGuard(daily_limit=25.0)
    assert guard.check_budget(additional_cost=1.5) == True
    guard.record_expense(cost=24.0, category="LLM")
    assert guard.get_status()['daily_used'] == 24.0
    
    # Exceeding budget
    assert guard.check_budget(additional_cost=2.0) == False
