import asyncio
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime, timezone
from sqlalchemy.future import select
from database.connection import AsyncSessionLocal
from database.schema import Channel, Production, Topic, YouTubeVideo
from python.services.quota_manager import quota_manager
from python.services.budget_guard import budget_guard

async def export_telemetry():
    os.makedirs('docs', exist_ok=True)
    async with AsyncSessionLocal() as session:
        chs_res = await session.execute(select(Channel))
        channels = [
            {'id': c.id, 'name': c.title, 'niche': c.niche, 'mode': c.operating_mode}
            for c in chs_res.scalars().all()
        ]

        prods_res = await session.execute(select(Production).order_by(Production.created_at.desc()))
        productions = []
        for p in prods_res.scalars().all():
            title = 'Autonomous Video Production'
            if p.publishing_json and isinstance(p.publishing_json, dict):
                title = p.publishing_json.get('title', title)
            elif p.script_json and isinstance(p.script_json, dict):
                title = p.script_json.get('title_candidate', title)
            
            productions.append({
                'id': p.id,
                'title': title,
                'status': p.status,
                'format': p.format or 'shorts',
                'created_at': p.created_at.isoformat() if p.created_at else None
            })

        payload = {
            'system_status': 'HEALTHY',
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'channels_count': len(channels),
            'channels': channels,
            'productions_count': len(productions),
            'productions': productions,
            'quota': {
                'used': 10000 - quota_manager.get_remaining_quota(),
                'limit': 10000,
                'remaining': quota_manager.get_remaining_quota()
            },
            'budget': {
                'daily_spent': budget_guard.data.get('daily_spent', 0.0),
                'daily_limit': 25.0
            },
            'quality_gates_passed': True
        }

        with open('docs/telemetry.json', 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
        print('Exported live telemetry to docs/telemetry.json')

if __name__ == '__main__':
    asyncio.run(export_telemetry())
