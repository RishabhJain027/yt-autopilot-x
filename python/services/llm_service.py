import json
import re
from typing import Dict, Any, Optional
from packages.config.settings import settings
from packages.logger.logger import logger
from python.services.budget_guard import budget_guard

# Prompt Injection Defense: Delimit external inputs safely
def sanitize_prompt_input(raw_input: str) -> str:
    cleaned = raw_input.replace('<|im_start|>', '').replace('<|im_end|>', '')
    return f'<<<UNTRUSTED_EXTERNAL_DATA_START>>>\n{cleaned}\n<<<UNTRUSTED_EXTERNAL_DATA_END>>>'

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PRIMARY_PROVIDER

    async def generate_json(self, system_prompt: str, user_prompt: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        # Estimate cost
        est = budget_guard.estimate_cost('llm_tokens_1k', 2)
        if not budget_guard.can_spend(est):
            logger.warning('LLM generation deferred due to budget limit, using fallback structured response')
            return fallback_data

        try:
            if self.provider == 'gemini' and settings.GEMINI_API_KEY:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
                resp = await model.generate_content_async(user_prompt, generation_config={'response_mime_type': 'application/json'})
                data = json.loads(resp.text)
                budget_guard.record_spend('gemini', 'llm_tokens_1k', est)
                return data

            elif self.provider == 'openai' and settings.OPENAI_API_KEY:
                import httpx
                headers = {'Authorization': f'Bearer {settings.OPENAI_API_KEY}', 'Content-Type': 'application/json'}
                payload = {
                    'model': 'gpt-4o-mini',
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_prompt}
                    ],
                    'response_format': {'type': 'json_object'}
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    res = await client.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
                    if res.status_code == 200:
                        content = res.json()['choices'][0]['message']['content']
                        budget_guard.record_spend('openai', 'llm_tokens_1k', est)
                        return json.loads(content)
        except Exception as e:
            logger.error(f'LLM API call failed: {e}. Falling back to structured response generator.')

        # Mock / Rule-based local fallback
        budget_guard.record_spend('mock_local', 'llm_tokens_1k', 0.0)
        return fallback_data

llm_service = LLMService()
