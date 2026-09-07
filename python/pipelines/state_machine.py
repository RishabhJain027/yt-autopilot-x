from typing import Set, Dict
from packages.logger.logger import logger, audit_log

# All 28 States from Section 27 of BRAIN.md
VALID_STATES: Set[str] = {
    'DISCOVERY_QUEUED',
    'IDEA',
    'RESEARCHING',
    'RESEARCH_READY',
    'SCRIPTING',
    'SCRIPT_READY',
    'VISUAL_PLANNING',
    'ASSET_COLLECTION',
    'ASSET_READY',
    'VOICE_GENERATION',
    'CAPTIONS_GENERATED',
    'RENDERING',
    'RENDERED',
    'QA_PENDING',
    'QA_FAILED',
    'RIGHTS_PENDING',
    'REVIEW_PENDING',
    'APPROVED',
    'UPLOAD_PENDING',
    'UPLOADING',
    'PROCESSING',
    'SCHEDULED',
    'PUBLISHED',
    'ANALYTICS_PENDING',
    'LEARNING_READY',
    'ARCHIVED',
    'FAILED',
    'CANCELLED'
}

TRANSITIONS: Dict[str, Set[str]] = {
    'DISCOVERY_QUEUED': {'IDEA', 'RESEARCHING', 'FAILED', 'CANCELLED'},
    'IDEA': {'RESEARCHING', 'CANCELLED', 'FAILED'},
    'RESEARCHING': {'RESEARCH_READY', 'FAILED', 'CANCELLED'},
    'RESEARCH_READY': {'SCRIPTING', 'FAILED', 'CANCELLED'},
    'SCRIPTING': {'SCRIPT_READY', 'FAILED', 'CANCELLED'},
    'SCRIPT_READY': {'VISUAL_PLANNING', 'VOICE_GENERATION', 'FAILED', 'CANCELLED'},
    'VISUAL_PLANNING': {'ASSET_COLLECTION', 'ASSET_READY', 'FAILED', 'CANCELLED'},
    'ASSET_COLLECTION': {'ASSET_READY', 'RIGHTS_PENDING', 'FAILED', 'CANCELLED'},
    'ASSET_READY': {'VOICE_GENERATION', 'RENDERING', 'FAILED', 'CANCELLED'},
    'VOICE_GENERATION': {'CAPTIONS_GENERATED', 'RENDERING', 'FAILED', 'CANCELLED'},
    'CAPTIONS_GENERATED': {'RENDERING', 'FAILED', 'CANCELLED'},
    'RENDERING': {'RENDERED', 'FAILED', 'CANCELLED'},
    'RENDERED': {'QA_PENDING', 'FAILED', 'CANCELLED'},
    'QA_PENDING': {'REVIEW_PENDING', 'APPROVED', 'QA_FAILED', 'FAILED', 'CANCELLED'},
    'QA_FAILED': {'SCRIPTING', 'VISUAL_PLANNING', 'RENDERING', 'CANCELLED', 'FAILED'},
    'RIGHTS_PENDING': {'ASSET_READY', 'QA_FAILED', 'CANCELLED', 'FAILED'},
    'REVIEW_PENDING': {'APPROVED', 'SCRIPTING', 'VISUAL_PLANNING', 'RENDERING', 'QA_FAILED', 'CANCELLED'},
    'APPROVED': {'UPLOAD_PENDING', 'UPLOADING', 'SCHEDULED', 'CANCELLED'},
    'UPLOAD_PENDING': {'UPLOADING', 'CANCELLED', 'FAILED'},
    'UPLOADING': {'PROCESSING', 'SCHEDULED', 'FAILED'},
    'PROCESSING': {'SCHEDULED', 'PUBLISHED', 'FAILED'},
    'SCHEDULED': {'PUBLISHED', 'CANCELLED', 'FAILED'},
    'PUBLISHED': {'ANALYTICS_PENDING', 'LEARNING_READY', 'ARCHIVED'},
    'ANALYTICS_PENDING': {'LEARNING_READY', 'ARCHIVED'},
    'LEARNING_READY': {'ARCHIVED', 'IDEA'},
    'ARCHIVED': set(),
    'FAILED': {'IDEA', 'RESEARCHING', 'SCRIPTING', 'RENDERING', 'UPLOAD_PENDING'},
    'CANCELLED': set()
}

class ProductionStateMachine:
    def can_transition(self, current_state: str, next_state: str) -> bool:
        if next_state not in VALID_STATES:
            return False
        return next_state in TRANSITIONS.get(current_state, set())

    def transition(self, current_state: str, next_state: str, production_id: str, channel_id: str = None) -> str:
        if not self.can_transition(current_state, next_state):
            err = f"Illegal state transition from {current_state} to {next_state} for production {production_id}"
            logger.error(err)
            raise ValueError(err)

        audit_log("STATE_TRANSITION", {
            "production_id": production_id,
            "from_state": current_state,
            "to_state": next_state
        }, channel_id=channel_id)

        logger.info(f"[STATE] Production {production_id}: {current_state} -> {next_state}")
        return next_state

state_machine = ProductionStateMachine()
