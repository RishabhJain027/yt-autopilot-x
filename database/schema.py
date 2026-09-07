import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Numeric, BigInteger, Boolean, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def gen_uuid() -> str:
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    google_account_email = Column(String(255), nullable=True)
    youtube_channel_id = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    niche = Column(String(255), nullable=True)
    language_code = Column(String(10), default='en')
    timezone = Column(String(50), default='Asia/Kolkata')
    operating_mode = Column(String(50), default='APPROVAL_FIRST')
    status = Column(String(50), default='ACTIVE')
    encrypted_refresh_token = Column(Text, nullable=True)
    oauth_scopes = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    memory = relationship('ChannelMemory', back_populates='channel', uselist=False, cascade='all, delete-orphan')
    topics = relationship('Topic', back_populates='channel', cascade='all, delete-orphan')
    productions = relationship('Production', back_populates='channel', cascade='all, delete-orphan')

class ChannelMemory(Base):
    __tablename__ = 'channel_memory'

    channel_id = Column(String(36), ForeignKey('channels.id'), primary_key=True)
    brand_json = Column(JSON, default=dict)
    audience_json = Column(JSON, default=dict)
    pillars_json = Column(JSON, default=list)
    banned_topics_json = Column(JSON, default=list)
    recent_titles_json = Column(JSON, default=list)
    approved_learnings_json = Column(JSON, default=list)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    channel = relationship('Channel', back_populates='memory')

class Topic(Base):
    __tablename__ = 'topics'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    channel_id = Column(String(36), ForeignKey('channels.id'), index=True)
    topic = Column(Text, nullable=False)
    score = Column(Numeric(5, 2), default=0.0)
    trend_score = Column(Numeric(5, 2), default=0.0)
    competition_score = Column(Numeric(5, 2), default=0.0)
    rights_risk = Column(Numeric(5, 2), default=0.0)
    status = Column(String(50), default='DISCOVERED')
    evidence_json = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    channel = relationship('Channel', back_populates='topics')
    productions = relationship('Production', back_populates='topic')

class Production(Base):
    __tablename__ = 'productions'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    channel_id = Column(String(36), ForeignKey('channels.id'), index=True)
    topic_id = Column(String(36), ForeignKey('topics.id'), nullable=True)
    status = Column(String(50), nullable=False, default='IDEA', index=True)
    format = Column(String(20), default='shorts')
    script_json = Column(JSON, default=dict)
    visual_json = Column(JSON, default=dict)
    publishing_json = Column(JSON, default=dict)
    review_json = Column(JSON, default=dict)
    final_video_path = Column(Text, nullable=True)
    thumbnail_path = Column(Text, nullable=True)
    audio_path = Column(Text, nullable=True)
    caption_path = Column(Text, nullable=True)
    video_hash_sha256 = Column(String(64), nullable=True)
    render_duration_seconds = Column(Numeric(8, 2), default=0.0)
    estimated_cost_usd = Column(Numeric(8, 4), default=0.0)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    channel = relationship('Channel', back_populates='productions')
    topic = relationship('Topic', back_populates='productions')
    assets = relationship('Asset', back_populates='production', cascade='all, delete-orphan')
    claims = relationship('Claim', back_populates='production', cascade='all, delete-orphan')
    youtube_video = relationship('YouTubeVideo', back_populates='production', uselist=False, cascade='all, delete-orphan')
    reviews = relationship('ReviewRecord', back_populates='production', cascade='all, delete-orphan')

class Claim(Base):
    __tablename__ = 'claims'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    production_id = Column(String(36), ForeignKey('productions.id'), index=True)
    claim_text = Column(Text, nullable=False)
    source_url = Column(Text, nullable=True)
    source_title = Column(Text, nullable=True)
    source_publisher = Column(Text, nullable=True)
    confidence = Column(Numeric(4, 2), default=1.0)
    supports_claim = Column(Boolean, default=True)
    requires_human_review = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    production = relationship('Production', back_populates='claims')

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    production_id = Column(String(36), ForeignKey('productions.id'), index=True)
    source_type = Column(String(50), default='generated')
    source_url = Column(Text, nullable=True)
    local_path = Column(Text, nullable=True)
    checksum_sha256 = Column(String(64), nullable=True)
    rights_status = Column(String(50), default='VERIFIED')
    license_json = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    production = relationship('Production', back_populates='assets')

class YouTubeVideo(Base):
    __tablename__ = 'youtube_videos'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    production_id = Column(String(36), ForeignKey('productions.id'), unique=True, index=True)
    youtube_video_id = Column(String(255), unique=True, nullable=True, index=True)
    upload_status = Column(String(50), default='PENDING')
    privacy_status = Column(String(50), default='private')
    publish_at = Column(DateTime(timezone=True), nullable=True, index=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    contains_synthetic_media = Column(Boolean, default=True)
    response_json = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    production = relationship('Production', back_populates='youtube_video')

class AnalyticsSnapshot(Base):
    __tablename__ = 'analytics_snapshots'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    youtube_video_id = Column(String(255), index=True)
    channel_id = Column(String(36), index=True)
    captured_at = Column(DateTime(timezone=True), default=utc_now)
    views = Column(BigInteger, default=0)
    likes = Column(BigInteger, default=0)
    comments = Column(BigInteger, default=0)
    watch_time_minutes = Column(Numeric(10, 2), default=0.0)
    average_view_duration_seconds = Column(Numeric(8, 2), default=0.0)
    ctr = Column(Numeric(5, 4), default=0.0)
    retention_json = Column(JSON, default=dict)

class ReviewRecord(Base):
    __tablename__ = 'review_records'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    production_id = Column(String(36), ForeignKey('productions.id'), index=True)
    review_requested_at = Column(DateTime(timezone=True), default=utc_now)
    decision_at = Column(DateTime(timezone=True), nullable=True)
    reviewer_id = Column(String(100), default='operator')
    decision = Column(String(50), nullable=True)
    feedback_notes = Column(Text, nullable=True)
    revision_count = Column(BigInteger, default=0)

    production = relationship('Production', back_populates='reviews')

class LearningRecommendation(Base):
    __tablename__ = 'learning_recommendations'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    channel_id = Column(String(36), index=True)
    finding = Column(Text, nullable=False)
    evidence_count = Column(BigInteger, default=1)
    confidence = Column(Numeric(4, 2), default=0.5)
    metric = Column(String(100), nullable=False)
    recommended_action = Column(Text, nullable=False)
    status = Column(String(50), default='PENDING_APPROVAL')
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class OutboxEvent(Base):
    __tablename__ = 'outbox_events'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    event_type = Column(String(100), nullable=False, index=True)
    payload_json = Column(JSON, nullable=False)
    status = Column(String(50), default='PENDING')
    retry_count = Column(BigInteger, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    processed_at = Column(DateTime(timezone=True), nullable=True)

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(String(36), primary_key=True, default=gen_uuid)
    channel_id = Column(String(36), nullable=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    details_json = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)
