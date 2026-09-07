# BRAIN.md — Autonomous YouTube Channel Operating System

**Project codename:** YT-Autopilot-X
**Document type:** Master implementation specification / engineering brain
**Target runtime:** Self-hosted, single-user first; multi-channel ready
**Primary objective:** Build an autonomous YouTube content operation that can research a niche, develop a channel identity, discover topics, generate original videos, create metadata, validate rights/quality, schedule uploads, collect analytics, and continuously improve strategy.

> **SECURITY RULE — NON-NEGOTIABLE:** Never store, print, commit, log, embed, or transmit a Gmail password. Authentication must use Google OAuth 2.0. A password that has been exposed in chat should be treated as compromised and changed immediately. This project stores OAuth tokens/refresh tokens only in an encrypted credential store.

> **ENGAGEMENT RULE:** Do not implement artificial views, likes, subscribers, comments, watch-time inflation, proxy rotation for engagement manipulation, or bot traffic. The `youtube-viewer` repository is explicitly a view-inflation project and is excluded from this architecture.

> **CONTENT RIGHTS RULE:** Never blindly download/reupload arbitrary third-party clips. Every non-owned asset must have recorded provenance and usage rights. Prefer original AI-generated media, creator-owned assets, public-domain material, or commercially licensed stock.

> **PUBLISHING RULE:** The system supports full automation, but safety and compliance gates remain configurable. Default production mode is approval-first; autonomous publishing requires all machine gates to pass and may be disabled globally.

---

## 0. Executive Summary

YT-Autopilot-X is a complete YouTube channel operating system. It combines the best architectural ideas from three inspected open-source repositories while deliberately excluding the artificial-view component.

### Source repositories inspected

1. **darkzOGx/youtube-automation-agent**
   - Strong Node.js implementation.
   - Existing agents for content strategy, script writing, thumbnail design, SEO, production, publishing/scheduling, and analytics.
   - Dashboard, database, local credentials, scheduler, production readiness checks, review studio, provenance/evidence workflows, Shorts repurposing, analytics learning, and engagement tooling.
   - The repository states an approval-first publishing model and a provider-flexible architecture.

2. **khaoss85/youtube-autopilot**
   - Strong Python layered design.
   - Separates `core`, `agents`, `services`, `pipeline`, and `io`.
   - Useful agent decomposition: TrendHunter, ScriptWriter, VisualPlanner, SeoManager, QualityReviewer.
   - Uses YouTube API, FFmpeg, scheduling, LLM clients, trend data, persistence and analytics.

3. **soumyadityac/youtube-viewer**
   - Excluded.
   - It describes automated browsing with Puppeteer/TOR to inflate YouTube views.
   - No code from this repository should be wired into the production engagement or growth system.

### End-to-end operating loop

```text
Google OAuth
    ↓
Connect YouTube channel
    ↓
Channel identity setup
    ↓
Niche discovery / niche selection
    ↓
Audience definition
    ↓
Brand kit + naming
    ↓
Content pillars
    ↓
Trend discovery
    ↓
Topic scoring
    ↓
Research + evidence collection
    ↓
Script + hook + CTA
    ↓
Scene planning
    ↓
Asset acquisition / generation
    ↓
Voice / TTS
    ↓
Captions
    ↓
FFmpeg assembly
    ↓
Thumbnail
    ↓
Title + description + hashtags + tags
    ↓
Rights / factual / safety / quality gates
    ↓
Render validation
    ↓
Upload as private
    ↓
Schedule publish time
    ↓
Analytics collection
    ↓
Retention / CTR / watch-time analysis
    ↓
Learning + strategy update
    ↓
Next production cycle
```

The system is designed to run continuously, including an hourly scheduler. “Every hour” means the scheduler wakes every hour and attempts an eligible pipeline run; it does not guarantee one successful public upload every hour. The system must stop or defer when quota, provider, rights, content quality, duplicate-content checks, or configured channel limits fail.

---

# 1. Product Definition

## 1.1 Product goal

Create a private, self-hosted control center that can operate one or more YouTube channels from a single application.

The owner supplies:
- Google account access through OAuth.
- Channel preferences.
- Optional niche constraints.
- Optional language.
- Optional visual identity.
- Provider API keys.
- Publishing cadence.
- Budget limits.

The system generates:
- Channel concept.
- Name ideas.
- Description.
- Handle ideas.
- Banner/logo prompts.
- Content pillars.
- Topic backlog.
- Scripts.
- Storyboards.
- Video clips or generated scenes.
- Voiceovers.
- Captions.
- Thumbnails.
- Titles.
- Descriptions.
- Hashtags.
- Tags.
- Upload packages.
- Schedule.
- Analytics reports.
- Learning recommendations.

## 1.2 Non-goals

- Artificially increasing views.
- Fake engagement.
- Credential harvesting.
- CAPTCHA bypass.
- Account takeover.
- Circumventing YouTube sanctions.
- Reuploading copyrighted clips without rights.
- Spam publishing when content quality is inadequate.

## 1.3 Operating modes

### Mode A — Research only

Find trends and produce topic queue.

### Mode B — Draft only

Create complete videos but never upload.

### Mode C — Approval-first

Create → validate → upload private → human review → schedule/publication.

### Mode D — Autonomous

Create → validate → upload private → schedule/publication automatically, subject to configured gates.

### Mode E — Emergency stop

Immediately stop new production and uploads while retaining already queued jobs.

---

# 2. Security and Credential Architecture

## 2.1 Never use Gmail username/password automation

The user may enter a Gmail address in the UI, but the application must not ask for or store the Gmail password.

Authentication sequence:

```text
User clicks CONNECT GOOGLE
    ↓
Google OAuth consent page
    ↓
User chooses Google account
    ↓
Google grants scopes
    ↓
Authorization code
    ↓
Backend exchanges code for tokens
    ↓
Encrypted refresh token stored
```

Google's current YouTube Data API documentation states that private-user access uses OAuth 2.0, and YouTube Data API does not support the service-account flow for YouTube accounts. A refresh token can be used to obtain access tokens after consent. [Google OAuth documentation](https://developers.google.com/youtube/v3/guides/authentication)

## 2.2 Recommended OAuth scopes

Request the minimum set required by the chosen feature set.

Typical scopes:

```text
https://www.googleapis.com/auth/youtube.upload
https://www.googleapis.com/auth/youtube.readonly
https://www.googleapis.com/auth/yt-analytics.readonly
```

Only request broader scopes such as `youtube` or `youtube.force-ssl` when a feature actually needs them.

## 2.3 Secret storage

Development:

```text
.env.local
```

Production:

```text
Docker secrets
Kubernetes secrets
HashiCorp Vault
AWS Secrets Manager
GCP Secret Manager
Azure Key Vault
```

Never commit:

```text
.env
*.pem
client_secret*.json
oauth*.json
token*.json
credentials*.json
cookies.json
session.json
```

## 2.4 Encryption

Sensitive database fields should use envelope encryption.

```text
master key
   ↓
KMS/Vault
   ↓
DEK
   ↓
encrypted OAuth refresh token
```

## 2.5 Audit logging

Log:
- login connection event
- token refresh failures
- scope changes
- channel connect/disconnect
- upload attempt
- upload result
- scheduling action
- content approval
- policy gate rejection
- emergency stop

Do not log:
- passwords
- access tokens
- refresh tokens
- authorization codes
- cookies

---

# 3. Technology Stack

The implementation intentionally uses multiple languages where each language is strongest.

## 3.1 TypeScript

Use for:
- Web dashboard.
- API gateway.
- OAuth callback endpoints.
- Admin UI.
- Job API.
- Real-time WebSocket/SSE status.
- Integration with the existing Node.js repository.

Core packages:

```text
next
react
typescript
express or fastify
zod
pino
bullmq
redis
googleapis
prisma
```

## 3.2 Python

Use for:
- AI agents.
- Research.
- Content scoring.
- NLP.
- Trend processing.
- Metadata generation.
- Analytics learning.
- Media planning.

Core packages:

```text
fastapi
pydantic
httpx
requests
google-api-python-client
google-auth-oauthlib
openai
anthropic
ffmpeg-python
Pillow
APScheduler
beautifulsoup4
trafilatura
lxml
praw
```

## 3.3 Shell

Use for:
- Docker entrypoints.
- FFmpeg orchestration scripts.
- Backups.
- CI utilities.
- Health checks.

## 3.4 SQL

Use PostgreSQL for production.

SQLite is acceptable for a single-machine prototype.

## 3.5 HTML/CSS

Use for dashboard structure/style when building a non-Next.js frontend or extending the existing dashboard.

## 3.6 YAML

Use for:
- Docker Compose.
- GitHub Actions.
- deployment manifests.
- pipeline configuration.

## 3.7 JSON

Use as service-to-service contracts.

Every agent should exchange structured JSON validated by Pydantic/Zod schemas.

## 3.8 Optional Go

Use only when needed for:
- High-volume worker service.
- Fast media pipeline workers.
- Extremely reliable scheduler daemon.

Go is optional for v1.

## 3.9 Optional Rust

Use only where profiling proves a hot path benefits from native performance.

Rust is not required for the initial system.

---

# 4. Target Repository Structure

```text
yt-autopilot-x/
│
├── apps/
│   ├── dashboard/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── styles/
│   │
│   └── api/
│       ├── routes/
│       ├── middleware/
│       ├── oauth/
│       └── websocket/
│
├── python/
│   ├── agents/
│   ├── research/
│   ├── services/
│   ├── pipelines/
│   ├── schemas/
│   ├── analytics/
│   └── workers/
│
├── packages/
│   ├── contracts/
│   ├── config/
│   ├── logger/
│   └── client/
│
├── integrations/
│   ├── youtube/
│   ├── google/
│   ├── trends/
│   ├── media/
│   ├── tts/
│   ├── llm/
│   └── image/
│
├── video/
│   ├── ffmpeg/
│   ├── captions/
│   ├── composition/
│   ├── thumbnails/
│   └── validation/
│
├── scheduler/
├── database/
├── migrations/
├── prompts/
├── policies/
├── tests/
├── scripts/
├── storage/
├── docker/
├── docs/
├── .env.example
├── docker-compose.yml
├── package.json
├── pyproject.toml
├── README.md
└── BRAIN.md
```

---

# 5. Integration Strategy for the Existing Repositories

## 5.1 Principle

Do not blindly merge repositories.

Instead:

```text
Repo A = Node product/dashboard/integration reference
Repo B = Python AI architecture reference
Repo C = excluded engagement manipulation reference
```

## 5.2 Repo A components to retain/adapt

From `youtube-automation-agent`:

- content strategy agent
- script writer agent
- thumbnail designer agent
- SEO agent
- production manager
- publishing/scheduling agent
- analytics optimization agent
- dashboard
- database abstraction
- production readiness flow
- provenance/evidence desk
- review studio
- Shorts repurposing
- growth experimentation concept
- outcome/ROI concept
- engagement drafting concept

## 5.3 Repo B components to retain/adapt

From `youtube-autopilot`:

```text
core = contracts/config
agents = pure decision logic
services = external side effects
pipeline = orchestration
io = persistence
```

Keep the rule:

> Agents think. Services act. Pipelines coordinate. Persistence stores.

## 5.4 Repo C exclusion

Do not import:

```text
Puppeteer view farm
TOR rotation
fake viewing sessions
view inflation parameters
```

No fake traffic should enter analytics or strategy metrics.

---

# 6. System Architecture

```text
                           ┌───────────────────┐
                           │   Web Dashboard   │
                           └─────────┬─────────┘
                                     │
                           ┌─────────▼─────────┐
                           │   API Gateway     │
                           └─────────┬─────────┘
                                     │
         ┌───────────────────────────┼────────────────────────────┐
         │                           │                            │
 ┌───────▼────────┐        ┌─────────▼─────────┐       ┌──────────▼───────┐
 │ Scheduler      │        │ Pipeline Manager   │       │ Credential Vault │
 └───────┬────────┘        └─────────┬─────────┘       └──────────────────┘
         │                           │
         │                  ┌────────▼────────┐
         │                  │ Research Agents │
         │                  └────────┬────────┘
         │                           │
         │                  ┌────────▼────────┐
         │                  │ Editorial Agents│
         │                  └────────┬────────┘
         │                           │
         │                  ┌────────▼────────┐
         │                  │ Media Services  │
         │                  └────────┬────────┘
         │                           │
         │                  ┌────────▼────────┐
         └─────────────────►│ QA / Policy     │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │ YouTube Service │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │ Analytics       │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │ Learning Engine │
                            └─────────────────┘
```

---

# 7. Channel Bootstrap Workflow

## 7.1 Step 1 — Connect Google

Dashboard:

```text
CONNECT GOOGLE
```

OAuth callback stores:

```text
provider
account_email
channel_id
channel_title
oauth_scopes
token_status
connected_at
```

## 7.2 Step 2 — Discover channel state

Read:
- channel title
- description
- country if available
- uploads playlist
- recent uploads
- thumbnails
- basic statistics

## 7.3 Step 3 — Select niche

Inputs:

```json
{
  "language": "en",
  "target_region": "global",
  "faceless": true,
  "shorts": true,
  "long_form": true,
  "budget": "medium",
  "risk_tolerance": "low"
}
```

## 7.4 Niche score

```text
NicheScore =
  0.20 * TrendDemand
+ 0.15 * AudienceSize
+ 0.15 * ProductionFeasibility
+ 0.15 * EvergreenPotential
+ 0.10 * MonetizationPotential
+ 0.10 * Differentiation
+ 0.05 * SearchIntent
+ 0.10 * BrandFit
- 0.20 * CopyrightRisk
- 0.10 * Saturation
```

Weights must be configurable.

## 7.5 Niche proposal output

```json
{
  "niche": "AI tools and productivity",
  "audience": "18-34 tech/productivity learners",
  "primary_format": "shorts",
  "secondary_format": "long_form",
  "content_pillars": [
    "AI tools",
    "productivity workflows",
    "automation tutorials",
    "tool comparisons"
  ],
  "risk_notes": [],
  "evidence": []
}
```

---

# 8. Channel Naming and Branding Agent

Generate:
- 50 name ideas.
- 10 shortlist names.
- handle ideas.
- tagline.
- channel description.
- profile image prompt.
- banner prompt.
- visual identity.

Avoid:
- impersonation.
- trademark misuse.
- deceptive official-sounding names.

Brand memory:

```json
{
  "name": "FutureStack AI",
  "tone": ["smart", "fast", "practical"],
  "colors": [],
  "fonts": [],
  "logo_style": "minimal geometric",
  "thumbnail_style": "high contrast, one focal object, 3-5 words max"
}
```

---

# 9. Trend Discovery System

Trend sources should be modular.

Potential sources:

```text
YouTube search / public metadata
YouTube Analytics for owned channel
Google Trends where available
Reddit public API sources
News RSS / approved news APIs
Industry feeds
Official product announcements
Developer blogs
```

Do not depend on undocumented private endpoints when a supported API exists.

## 9.1 Trend normalization

```json
{
  "topic": "new AI coding agent",
  "source": "official_blog",
  "source_url": "...",
  "published_at": "...",
  "detected_at": "...",
  "momentum": 0.82,
  "competition": 0.51,
  "channel_fit": 0.94
}
```

## 9.2 Trend score

```text
TrendScore =
  0.30 * momentum
+ 0.20 * recency
+ 0.20 * audience_fit
+ 0.15 * differentiation
+ 0.15 * production_feasibility
- 0.20 * rights_risk
```

---

# 10. Research Agent

Research must produce evidence, not just a generated answer.

For every factual claim:

```text
claim_id
claim_text
source_url
source_title
source_publisher
retrieved_at
confidence
supports_claim
```

Research output:

```json
{
  "topic": "...",
  "facts": [],
  "sources": [],
  "contradictions": [],
  "uncertainties": [],
  "claims_requiring_human_review": []
}
```

The script writer must not silently convert uncertainty into certainty.

---

# 11. Topic Selection

The topic agent chooses based on:

```text
Trend score
Audience fit
Historical channel performance
Pillar balance
Recency
Production cost
Rights risk
Duplicate risk
Novelty
Expected retention
```

Maintain a topic cooldown table so near-identical topics do not recur within a configurable window.

---

# 12. Script Agent

Every script has:

```text
Hook
Context
Core value
Proof/examples
Pattern interruption
Payoff
CTA
```

For Shorts:

```text
0-2s     Hook
2-8s     Context
8-35s    Main content
35-50s   Payoff
50-60s   CTA
```

Durations must adapt to the spoken word count and desired format.

## 12.1 Script JSON

```json
{
  "title_candidate": "...",
  "hook": "...",
  "segments": [
    {
      "id": "scene_001",
      "voiceover": "...",
      "duration": 5.5,
      "claims": ["claim_1"]
    }
  ],
  "cta": "..."
}
```

---

# 13. Visual Planner

Map every script beat to a visual.

Priority order:

```text
1. Original footage
2. Licensed stock
3. Public domain
4. AI-generated scene
5. Screen recording of owned/demo environment
6. Abstract motion graphics
```

For each scene:

```json
{
  "scene_id": "scene_001",
  "duration": 4.2,
  "visual_type": "ai_video",
  "prompt": "...",
  "aspect_ratio": "9:16",
  "rights_status": "generated"
}
```

---

# 14. Asset Acquisition and Rights System

This is one of the most important modules.

Every asset gets a provenance record.

```text
asset_id
source_type
source_url
creator
license_name
license_url
commercial_use
modification_allowed
attribution_required
retrieved_at
checksum_sha256
used_in_video
rights_verified_by
```

Rights states:

```text
UNKNOWN
PENDING
VERIFIED
REJECTED
EXPIRED
```

The pipeline cannot publish when required assets are UNKNOWN or REJECTED.

YouTube's monetization guidance says monetizable content should be original/non-repetitious and that creators need the necessary rights to commercially use visual and audio elements. See current YouTube Help guidance. 

---

# 15. TTS / Voice Agent

Provider abstraction:

```python
class TTSProvider:
    def synthesize(self, text: str, voice_id: str, language: str) -> AudioArtifact:
        ...
```

Store:

```text
provider
model
voice_id
language
duration
cost
created_at
checksum
```

Support:

```text
Google TTS
ElevenLabs
Microsoft Azure Speech
OpenAI-compatible TTS where available
Local TTS as fallback
```

---

# 16. Caption Engine

Produce:

```text
SRT
VTT
burned-in captions
```

Pipeline:

```text
script
 ↓
TTS audio
 ↓
word/segment timing
 ↓
caption segmentation
 ↓
line-length validator
 ↓
SRT/VTT
 ↓
FFmpeg burn-in option
```

Rules:
- Keep captions readable.
- Avoid covering faces/product UI.
- Use safe margins.
- Match spoken content.

---

# 17. Thumbnail Agent

Inputs:

```text
video topic
channel brand kit
winning historical thumbnails
video transcript
```

Outputs:

```text
thumbnail prompt
background concept
foreground subject
text concept
layout
negative prompt
```

A/B experiment support should prepare variants for human/controlled experimentation rather than silently rewriting live metadata.

---

# 18. SEO / Publishing Package

Generate:

```text
primary title
alternate titles
description
hashtags
tags
category
language
thumbnail
playlist
```

Title rules:
- truthful.
- relevant.
- concise.
- curiosity without deceptive promise.

Description structure:

```text
1. Two-line hook/value proposition
2. Main summary
3. Useful links
4. Sources when appropriate
5. CTA
6. Hashtags
7. Disclosure section when required
```

Tags are secondary metadata, not the primary growth strategy.

---

# 19. Quality and Policy Gate

Every production must run multiple validators.

## Gate A — Factuality

```text
claims resolved
sources available
contradictions handled
```

## Gate B — Rights

```text
all assets verified
music rights verified
voice rights verified
```

## Gate C — Duplicate / repetitive content

Compare embeddings and metadata against recent content.

## Gate D — Safety

Check:

```text
hate
harassment
sexual content
violent graphic content
dangerous instructions
misinformation-sensitive claims
medical claims
legal claims
financial claims
impersonation
```

## Gate E — Synthetic media disclosure

The YouTube API video resource supports a `status.containsSyntheticMedia` field. The upload contract must expose this flag and the dashboard must let the operator review it where applicable. [YouTube videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)

## Gate F — Render quality

Check:

```text
MP4 decodes
video stream exists
audio stream exists when expected
resolution correct
frame rate valid
duration valid
captions valid
no black frames above threshold
no audio clipping above threshold
```

---

# 20. FFmpeg Production Pipeline

Canonical pipeline:

```text
scene clips
    +
voiceover
    +
music
    +
sfx
    +
captions
    +
logo/overlay
    ↓
FFmpeg composition
    ↓
normalization
    ↓
encoding
    ↓
thumbnail extraction
    ↓
validation
```

Preferred intermediate format:

```text
H.264 video
AAC audio
MP4 container
```

The exact preset, bitrate and CRF remain configurable per format.

---

# 21. Media Validation

Run:

```bash
ffprobe -v error -show_entries format=duration -show_streams final.mp4
```

Validate:

```text
duration > 0
video stream exists
audio stream exists if expected
codec acceptable
resolution acceptable
rotation metadata consistent
file size reasonable
```

Compute:

```text
sha256
```

for artifact identity.

---

# 22. Upload Architecture

Google's current documentation defines `videos.insert` for uploads and allows setting title, description, tags, category, privacy state, publish time and synthetic-media disclosure fields. Uploads require OAuth scopes. [YouTube Data API](https://developers.google.com/youtube/v3/docs/videos/insert)

### Upload lifecycle

```text
LOCAL_READY
   ↓
PRE_UPLOAD_VALIDATION
   ↓
UPLOAD_PRIVATE
   ↓
YOUTUBE_PROCESSING
   ↓
PROCESSING_VALIDATED
   ↓
SCHEDULED
   ↓
PUBLISHED
```

Never mark a video as published merely because the upload request returned HTTP 200.

Poll YouTube processing status where needed.

---

# 23. Scheduling

Use an internal scheduler with a persistent database.

Recommended:

```text
APScheduler (Python)
```

or:

```text
BullMQ + Redis (Node)
```

For v1 single-machine implementation, APScheduler is sufficient. For distributed workers, BullMQ/Redis is preferred.

## 23.1 Hourly cadence

Default scheduler:

```text
minute = 00
frequency = hourly
```

At each wake-up:

```text
check channel status
check global stop switch
check provider budgets
check quota
check pending jobs
check content backlog
check upload slots
run eligible workflow
```

### Important interpretation

The hourly scheduler is **not** a promise that exactly one public video will appear every hour.

Example:

```text
20:00  research
21:00  video generation
22:00  rendering
23:00  upload
00:00  upload next
```

A job may span multiple hours.

An optional “one completed upload per hour” policy can be configured only when the production backlog is ready and quota is available.

---

# 24. YouTube Scheduling Constraints

YouTube's current help documentation supports scheduling a private video to become public at a specified date/time. [YouTube Help — schedule video publish time](https://support.google.com/youtube/answer/1270709)

The Data API `status.publishAt` field is for a private, never-published video and uses ISO 8601 time. [YouTube Data API videos](https://developers.google.com/youtube/v3/docs/videos)

Current Google documentation also notes that uploads using `videos.insert` from unverified API projects created after 28 July 2020 can be restricted to private viewing mode until the API project passes Google's compliance audit. Design around this from day one.

Therefore the robust sequence is:

```text
API upload
 ↓
private
 ↓
processing
 ↓
set/confirm publishAt
 ↓
scheduled publication
```

---

# 25. Quota Management

YouTube API quota must be treated as a first-class resource.

Track:

```text
quota_budget_daily
quota_consumed
quota_estimated_next_job
quota_reset_time
```

Every service call records:

```text
endpoint
cost_estimate
actual_response
timestamp
```

Scheduler behavior:

```text
if quota < minimum_required:
    defer upload
```

Never retry blindly on quota errors.

---

# 26. Database Design

Use PostgreSQL in production.

## 26.1 channels

```sql
CREATE TABLE channels (
  id UUID PRIMARY KEY,
  google_account_email TEXT,
  youtube_channel_id TEXT UNIQUE NOT NULL,
  title TEXT,
  description TEXT,
  niche TEXT,
  language_code TEXT,
  timezone TEXT,
  operating_mode TEXT,
  status TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
```

## 26.2 channel_memory

```sql
CREATE TABLE channel_memory (
  channel_id UUID PRIMARY KEY REFERENCES channels(id),
  brand_json JSONB,
  audience_json JSONB,
  pillars_json JSONB,
  banned_topics_json JSONB,
  recent_titles_json JSONB,
  approved_learnings_json JSONB,
  updated_at TIMESTAMPTZ NOT NULL
);
```

## 26.3 topics

```sql
CREATE TABLE topics (
  id UUID PRIMARY KEY,
  channel_id UUID REFERENCES channels(id),
  topic TEXT NOT NULL,
  score NUMERIC,
  trend_score NUMERIC,
  competition_score NUMERIC,
  rights_risk NUMERIC,
  status TEXT,
  evidence_json JSONB,
  created_at TIMESTAMPTZ NOT NULL
);
```

## 26.4 productions

```sql
CREATE TABLE productions (
  id UUID PRIMARY KEY,
  channel_id UUID REFERENCES channels(id),
  topic_id UUID REFERENCES topics(id),
  status TEXT NOT NULL,
  format TEXT,
  script_json JSONB,
  publishing_json JSONB,
  review_json JSONB,
  final_video_path TEXT,
  thumbnail_path TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
```

## 26.5 assets

```sql
CREATE TABLE assets (
  id UUID PRIMARY KEY,
  production_id UUID REFERENCES productions(id),
  source_url TEXT,
  local_path TEXT,
  checksum_sha256 TEXT,
  rights_status TEXT,
  license_json JSONB,
  created_at TIMESTAMPTZ NOT NULL
);
```

## 26.6 youtube_videos

```sql
CREATE TABLE youtube_videos (
  id UUID PRIMARY KEY,
  production_id UUID REFERENCES productions(id),
  youtube_video_id TEXT UNIQUE,
  upload_status TEXT,
  privacy_status TEXT,
  publish_at TIMESTAMPTZ,
  published_at TIMESTAMPTZ,
  contains_synthetic_media BOOLEAN,
  response_json JSONB,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
```

## 26.7 analytics_snapshots

```sql
CREATE TABLE analytics_snapshots (
  id UUID PRIMARY KEY,
  youtube_video_id TEXT,
  captured_at TIMESTAMPTZ,
  views BIGINT,
  likes BIGINT,
  comments BIGINT,
  watch_time_minutes NUMERIC,
  average_view_duration_seconds NUMERIC,
  ctr NUMERIC,
  retention_json JSONB
);
```

---

# 27. Production State Machine

States:

```text
IDEA
RESEARCHING
RESEARCH_READY
SCRIPTING
SCRIPT_READY
VISUAL_PLANNING
ASSET_COLLECTION
ASSET_READY
VOICE_GENERATION
CAPTIONS_GENERATED
RENDERING
RENDERED
QA_PENDING
QA_FAILED
RIGHTS_PENDING
REVIEW_PENDING
APPROVED
UPLOAD_PENDING
UPLOADING
PROCESSING
SCHEDULED
PUBLISHED
ANALYTICS_PENDING
LEARNING_READY
ARCHIVED
FAILED
CANCELLED
```

Every state transition must be transactional.

---

# 28. Retry Strategy

Every job gets:

```text
attempt_count
max_attempts
last_error
next_retry_at
```

Retryable:

```text
network timeout
rate limit
provider temporary failure
YouTube 5xx
temporary render filesystem error
```

Non-retryable until human/config change:

```text
invalid OAuth scope
copyright rights rejected
policy violation
missing required API key
permanent malformed request
```

Exponential backoff:

```text
30s
2m
10m
30m
2h
```

Jitter is recommended.

---

# 29. Idempotency

Every external side effect must be idempotent where possible.

Upload job key:

```text
channel_id + production_id
```

Before upload:

```text
query local database
query YouTube reconciliation where required
if upload already has video ID:
    do not upload again
```

This protects against the worst failure:

```text
YouTube accepts upload
network dies
our application sees timeout
application retries
duplicate video appears
```

---

# 30. Autonomous Hourly Orchestrator

Pseudo-code:

```python
def hourly_tick():
    acquire_distributed_lock("hourly-channel-cycle")

    channels = get_active_channels()

    for channel in channels:
        if emergency_stop(channel):
            continue

        health = get_channel_health(channel)
        if not health.ok:
            create_incident(channel, health.reason)
            continue

        reconcile_youtube_state(channel)
        collect_recent_analytics(channel)

        backlog = get_pipeline_backlog(channel)

        if backlog.needs_topic:
            topic = discover_and_select_topic(channel)
            enqueue(topic)

        if backlog.needs_script:
            enqueue_script(backlog.next_eligible())

        if backlog.needs_assets:
            enqueue_assets(backlog.asset_jobs())

        if backlog.needs_render:
            enqueue_render(backlog.render_jobs())

        if backlog.needs_upload:
            enforce_all_publish_gates()
            enqueue_upload(backlog.upload_jobs())

        update_learning_models(channel)

    release_lock()
```

---

# 31. Parallel Workers

Recommended queues:

```text
research
script
visual
asset
voice
caption
thumbnail
render
qa
upload
analytics
learning
```

Concurrency defaults:

```text
research = 4
script = 4
asset = 2
voice = 4
render = 2
upload = 1 per channel
analytics = 2
```

Make all limits configurable.

GPU-heavy video generation must be independently rate-limited.

---

# 32. Dashboard Design

Main pages:

```text
Dashboard
Channel Setup
Niche Lab
Trend Radar
Content Calendar
Production Queue
Review Studio
Upload Queue
Analytics
Experiments
Audience
Assets / Rights
Providers
Scheduler
Logs
System Health
Settings
```

## Dashboard metrics

```text
Videos today
Scheduled
Published
Views 24h
Views 7d
Watch time
CTR
Retention
Subscribers gained
Production cost
Provider spend
Pending reviews
Pipeline failures
Quota remaining
```

---

# 33. System Health Page

Show:

```text
Google OAuth       CONNECTED
YouTube API        HEALTHY
YouTube quota      71%
OpenAI              HEALTHY
Gemini              HEALTHY
TTS                  HEALTHY
Video provider      HEALTHY
FFmpeg               HEALTHY
Database             HEALTHY
Scheduler            RUNNING
Storage              HEALTHY
```

Red states:

```text
BLOCKED
DEGRADED
NEEDS ACTION
```

---

# 34. Content Calendar

Calendar should show:

```text
research
script
render
review
upload
scheduled
published
```

Example:

```text
MON 09:00  Topic #101
MON 10:00  Script #101
MON 12:00  Render #101
MON 13:00  Upload #101
MON 14:00  Publish #101
MON 15:00  Topic #102
```

The actual publish time must be configurable and timezone-aware.

---

# 35. Review Studio

Even autonomous mode should expose a full review record.

Display:

```text
Video preview
Title
Description
Hashtags
Tags
Thumbnail
Sources
Rights
Synthetic-media flag
Safety checks
Factual checks
Estimated cost
Estimated publish time
```

Buttons:

```text
APPROVE
REJECT
REGENERATE SCRIPT
REGENERATE SCENE
REGENERATE THUMBNAIL
EDIT METADATA
PAUSE
```

---

# 36. Analytics Engine

Collect at minimum:

```text
views
likes
comments
watch time
average view duration
CTR
subscriber change
retention curve where available
traffic source where available
```

Compare:

```text
24h
48h
7d
28d
```

Normalize performance by:

```text
format
length
pillar
topic type
hook type
thumbnail style
upload time
```

---

# 37. Learning Engine

Do not train blindly on noisy metrics.

For each learning:

```json
{
  "finding": "Problem-solving hooks outperform list hooks",
  "evidence_count": 18,
  "confidence": 0.81,
  "metric": "relative watch retention",
  "recommended_action": "Increase problem-solving hooks",
  "status": "PENDING_APPROVAL"
}
```

Only approved learnings influence the next planning cycle in approval-first mode.

---

# 38. Controlled Experiments

Potential experiments:

```text
title structure
thumbnail composition
hook style
video length
CTA position
caption style
upload hour
```

Do not modify multiple variables at once unless explicitly designed as a multivariate experiment.

Record:

```text
baseline
variant
time window
sample size
metric
confidence
```

Stop experiments that cause material retention degradation or policy concerns.

---

# 39. Cost Management

Every external provider call records:

```text
provider
model
units
estimated_cost
actual_cost
currency
job_id
timestamp
```

Per-channel budget:

```text
hourly budget
 daily budget
weekly budget
monthly budget
```

Budget policy:

```text
if projected_cost > available_budget:
    do not start job
```

Use cheaper fallback providers for noncritical tasks.

---

# 40. Provider Abstraction

All providers must share common contracts.

Example:

```python
class LLMProvider(Protocol):
    async def generate(self, prompt: str, schema: dict) -> dict:
        ...
```

Video:

```python
class VideoProvider(Protocol):
    async def generate_scene(self, prompt: str, duration: float, aspect_ratio: str):
        ...
```

Image:

```python
class ImageProvider(Protocol):
    async def generate(self, prompt: str, size: str):
        ...
```

This avoids vendor lock-in.

---

# 41. Prompt Management

All agent prompts live in:

```text
prompts/
```

Example:

```text
prompts/
├── niche_discovery.md
├── trend_research.md
├── script_writer.md
├── visual_planner.md
├── seo.md
├── thumbnail.md
├── quality.md
└── learning.md
```

Prompts are versioned.

Every production stores:

```text
prompt_version
model
temperature
provider
```

This enables reproducibility.

---

# 42. API Design

## GET /api/health

Returns system health.

## GET /api/channels

List connected channels.

## POST /api/oauth/google/start

Start OAuth.

## GET /api/oauth/google/callback

OAuth callback.

## POST /api/channels/{id}/bootstrap

Discover channel state.

## POST /api/channels/{id}/niche/discover

Run niche research.

## POST /api/channels/{id}/topics/discover

Run trend research.

## POST /api/productions

Create production.

## POST /api/productions/{id}/render

Render video.

## POST /api/productions/{id}/approve

Approve.

## POST /api/productions/{id}/reject

Reject.

## POST /api/productions/{id}/upload

Upload/schedule.

## GET /api/analytics/{videoId}

Get analytics.

## POST /api/scheduler/pause

Pause scheduler.

## POST /api/scheduler/resume

Resume.

## POST /api/system/emergency-stop

Emergency stop all publishing.

---

# 43. Event Model

Events:

```text
CHANNEL_CONNECTED
NICHE_SELECTED
TOPIC_DISCOVERED
TOPIC_SELECTED
SCRIPT_GENERATED
ASSET_CREATED
VOICE_GENERATED
CAPTIONS_GENERATED
VIDEO_RENDERED
QA_PASSED
QA_FAILED
RIGHTS_VERIFIED
REVIEW_APPROVED
UPLOAD_STARTED
UPLOAD_COMPLETED
SCHEDULED
PUBLISHED
ANALYTICS_CAPTURED
LEARNING_CREATED
```

Use an append-only event log for debugging.

---

# 44. Notifications

Notify the owner when:

```text
OAuth expired
critical provider unavailable
quota exhausted
rights review blocked
upload failed repeatedly
scheduler stopped
video published
analytics anomaly detected
budget exceeded
```

Channels:

```text
web dashboard
email
Telegram/Discord optional
```

Never include secrets in notifications.

---

# 45. Content Deduplication

Use:

```text
title similarity
script embedding similarity
topic entity overlap
thumbnail similarity
source overlap
```

Reject or rework content exceeding configured thresholds.

Example:

```text
title_similarity > 0.88 => regenerate
script_similarity > 0.85 => regenerate
```

Thresholds must be validated empirically.

---

# 46. Language Support

The system should support a `language_code` per channel.

Initial language layer:

```text
English — en
Hindi — hi
Hinglish — custom `hi-Latn` style profile
Spanish — es
French — fr
German — de
Portuguese — pt
Japanese — ja
Korean — ko
Arabic — ar
```

Do not pretend every provider supports every language equally. Provider capability discovery is required.

## Localization pipeline

```text
master research
   ↓
master script
   ↓
localized script
   ↓
language QA
   ↓
localized TTS
   ↓
localized captions
   ↓
localized metadata
```

---

# 47. Shorts vs Long-form

## Shorts

Target:

```text
9:16
short duration
fast hook
burned captions
```

## Long-form

Target:

```text
16:9
structured chapters
deeper research
more scenes
higher production budget
```

The channel strategy can mix both formats.

Do not blindly convert every long-form video into a Short; choose self-contained segments.

---

# 48. Shorts Repurposing

Input:

```text
approved long-form video
scene timeline
captions
```

Generate:

```text
Short candidate A
Short candidate B
Short candidate C
```

Reuse source assets where rights allow.

Maintain parent-child relationship:

```text
long_form_production_id
    ↓
short_production_id
```

---

# 49. Audience Feedback Engine

Sync comments from owned channel where permitted.

Classify:

```text
question
request
praise
criticism
spam
scam
abuse
off-topic
```

Generate draft responses but default to approval-first for posting replies.

Mine recurring questions into topic candidates.

---

# 50. Error Handling Playbook

## OAuth error

```text
mark channel AUTH_REQUIRED
stop upload jobs
notify owner
```

## API quota error

```text
defer upload
continue local research/production if budget permits
```

## LLM failure

```text
retry
fallback provider
if all fail → queue
```

## TTS failure

```text
retry
alternate voice/provider
```

## Video provider failure

```text
retry scene only
fallback to stock or motion graphics
```

## FFmpeg failure

```text
collect stderr
mark render failed
retry if transient
```

## Upload timeout

```text
reconcile before retry
```

## YouTube processing failure

```text
keep video private
mark PROCESSING_FAILED
attempt remediation
```

---

# 51. Recovery After Restart

On startup:

```text
load incomplete jobs
validate artifacts
reconcile YouTube uploads
rebuild scheduler
resume eligible jobs
```

Every job has a checkpoint.

Example:

```json
{
  "production_id": "...",
  "stage": "RENDERING",
  "completed": [
    "research",
    "script",
    "assets",
    "voice",
    "captions"
  ],
  "remaining": ["render", "qa", "upload"]
}
```

---

# 52. Backup and Restore

Back up:

```text
PostgreSQL
channel memory
production metadata
rights/provenance records
prompt versions
configuration
```

Do not place OAuth secrets in ordinary database backups unless encrypted using a dedicated key-management approach.

Daily backup:

```text
pg_dump
```

Retention:

```text
7 daily
4 weekly
3 monthly
```

---

# 53. Docker Architecture

Services:

```text
frontend
api
python-worker
scheduler
postgres
redis
ffmpeg-worker
minio (optional)
```

Example:

```yaml
services:
  api:
    build: ./apps/api
    env_file: .env
    depends_on:
      - postgres
      - redis

  worker:
    build: ./python
    env_file: .env
    depends_on:
      - postgres
      - redis

  scheduler:
    build: ./scheduler
    env_file: .env
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:latest

  redis:
    image: redis:latest
```

Pin production image versions rather than using floating `latest` tags.

---

# 54. Environment Variables

Use a template:

```text
APP_ENV=development
APP_PORT=3456
APP_BASE_URL=http://localhost:3456

DATABASE_URL=...
REDIS_URL=...
STORAGE_ROOT=./storage

GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=...

OPENAI_API_KEY=...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=...

TTS_PROVIDER=...
TTS_API_KEY=...

VIDEO_PROVIDER=...
VIDEO_API_KEY=...

DAILY_BUDGET_USD=...
HOURLY_UPLOAD_POLICY=true
AUTONOMOUS_PUBLISHING=false

LOG_LEVEL=info
```

Never put personal Gmail passwords here.

---

# 55. Development Setup

```bash
git clone <your-fork>
cd yt-autopilot-x

npm install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env

docker compose up -d postgres redis

npm run dev
python -m python.worker
python -m scheduler
```

---

# 56. Google Cloud Setup

Create a Google Cloud project.

Enable:

```text
YouTube Data API v3
YouTube Analytics API
```

Create OAuth client credentials appropriate for the application type.

Configure authorized redirect URI.

The official YouTube authentication documentation should be treated as the source of truth for OAuth implementation details.

---

# 57. Channel Bootstrap First Run

On first run:

```text
1. Connect Google
2. Detect channel
3. Confirm channel
4. Load current metadata
5. Choose niche mode
6. Run niche research
7. Choose channel strategy
8. Generate brand kit
9. Generate 30-day topic backlog
10. Generate first video
11. Render
12. QA
13. Upload private
14. Schedule
15. Track analytics
```

Never silently change an existing channel's identity.

---

# 58. Daily Operating Plan

Even with an hourly scheduler, the agents should understand larger planning windows.

### Daily

```text
refresh trends
review yesterday's analytics
select today's topics
produce scheduled content
collect failures
```

### Weekly

```text
review pillar performance
review retention
review CTR
review subscriber conversion
reallocate topic mix
```

### Monthly

```text
review niche health
review monetization readiness
review production cost
review experiments
refresh channel strategy
```

---

# 59. One-Hour Cycle Example

At 10:00:

```text
Trend scan
```

At 11:00:

```text
Research + topic selection
```

At 12:00:

```text
Script + visual plan
```

At 13:00:

```text
Asset generation
```

At 14:00:

```text
TTS + captions
```

At 15:00:

```text
FFmpeg render
```

At 16:00:

```text
QA + rights validation
```

At 17:00:

```text
YouTube upload
```

At 18:00:

```text
Schedule and start next job
```

The scheduler should allow overlapping jobs when resources permit.

---

# 60. Throughput Policy

Do not configure “one upload every hour” as an unconditional command.

Use:

```text
max_publishes_per_24h
max_concurrent_renders
max_provider_spend_per_day
minimum_quality_score
minimum_rights_score
minimum_originality_score
```

Recommended initial values:

```text
max_publishes_per_24h = 8
max_concurrent_renders = 2
AUTONOMOUS_PUBLISHING = false
```

Tune based on real channel performance and API/project limits.

---

# 61. Content Quality Score

```text
QualityScore =
  0.20 * factuality
+ 0.15 * originality
+ 0.15 * retention_potential
+ 0.10 * audio_quality
+ 0.10 * visual_quality
+ 0.10 * metadata_quality
+ 0.10 * audience_fit
+ 0.05 * rights_confidence
+ 0.05 * brand_fit
```

Publish threshold:

```text
>= configurable minimum
```

Any hard-block policy failure overrides the score.

---

# 62. Originality Model

Originality is not simply “different wording.”

Measure:

```text
new angle
new research synthesis
new narration
new visuals
new structure
new examples
```

Avoid template spam such as:

```text
same script skeleton
same visual sequence
same title formula
same generic voiceover
same footage
```

YouTube's monetization guidance emphasizes original and non-repetitious content.

---

# 63. Copyright and Content Rights

Hard rule:

```text
No license evidence = not publishable
```

For music:

```text
source
license
commercial use
attribution
```

For images:

```text
source
license
modification
commercial use
```

For video clips:

```text
creator/source
license
commercial use
transformation rights
```

Do not rely on the phrase “fair use” as an automatic permission system.

---

# 64. Synthetic Media Handling

Maintain:

```text
synthetic_media_present
synthetic_media_type
provider
model
human_reviewed
youtube_disclosure_required
```

Where the YouTube API field is supported, set `status.containsSyntheticMedia` correctly based on the actual content and current API behavior.

---

# 65. Scheduler Database Jobs

Example table:

```sql
CREATE TABLE scheduled_jobs (
  id UUID PRIMARY KEY,
  channel_id UUID NOT NULL,
  job_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  status TEXT NOT NULL,
  run_at TIMESTAMPTZ NOT NULL,
  attempts INT NOT NULL DEFAULT 0,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
```

Use a lock around workers to prevent duplicate execution.

---

# 66. Observability

Metrics:

```text
jobs_started
jobs_completed
jobs_failed
render_seconds
upload_seconds
provider_latency
provider_error_rate
queue_depth
quota_remaining
cost_per_video
videos_published
analytics_refresh_age
```

Logs use structured JSON.

Example:

```json
{
  "level": "info",
  "event": "video_uploaded",
  "channel_id": "...",
  "production_id": "...",
  "youtube_video_id": "...",
  "duration_ms": 18342
}
```

---

# 67. Testing Strategy

## Unit tests

Test:

```text
scoring
metadata validation
rights gates
state transitions
scheduler calculations
caption segmentation
quota checks
```

## Integration tests

Test:

```text
OAuth token refresh
YouTube metadata calls
upload to test/private target
analytics read
FFmpeg render
storage
```

## End-to-end tests

```text
topic → script → asset → render → private upload → reconciliation
```

Use a test channel where possible.

---

# 68. Security Test Plan

Verify:

```text
password never stored
access token never logged
refresh token encrypted
CSRF protection
OAuth state validation
secure cookies
rate limiting
admin auth
path traversal blocked
SSRF controls for remote asset fetch
```

Asset downloaders must allowlist protocols:

```text
https
```

Do not permit:

```text
file://
ftp://
gopher://
```

without a compelling and isolated use case.

---

# 69. Content Safety Test Plan

Create a fixture suite for:

```text
unsafe medical claim
financial promise
hate content
copyrighted music
unlicensed movie clip
misleading title
synthetic media
spam
repetitive script
```

Expected result for each test:

```text
BLOCK
```

---

# 70. Deployment

Recommended deployment tiers.

### Tier 1 — Local

```text
Docker Compose
Postgres
Redis
Local storage
```

### Tier 2 — VPS

```text
Ubuntu
Docker
Caddy/Nginx
Postgres
Redis
object storage
```

### Tier 3 — Cloud

```text
managed Postgres
managed Redis
container workers
object storage
secrets manager
monitoring
```

---

# 71. CI/CD

Pipeline:

```text
lint
 ↓
typecheck
 ↓
unit tests
 ↓
integration tests
 ↓
build
 ↓
container scan
 ↓
deploy
```

Never deploy with failing quality gates.

---

# 72. Git Branching

```text
main
 ├── develop
 ├── feature/*
 ├── fix/*
 └── release/*
```

Commit examples:

```text
feat: add hourly pipeline scheduler
feat: add YouTube OAuth flow
feat: add rights provenance model
fix: reconcile interrupted uploads
```

---

# 73. Implementation Order

## Phase 1

```text
repository skeleton
config
logging
Postgres
Redis
```

## Phase 2

```text
Google OAuth
channel discovery
```

## Phase 3

```text
niche agent
trend agent
research agent
```

## Phase 4

```text
script
SEO
thumbnail
```

## Phase 5

```text
TTS
captions
FFmpeg
```

## Phase 6

```text
rights system
QA
review studio
```

## Phase 7

```text
YouTube upload
scheduling
```

## Phase 8

```text
analytics
learning
```

## Phase 9

```text
hourly autonomous scheduler
```

## Phase 10

```text
hardening
observability
cost control
multi-channel
```

---

# 74. Acceptance Criteria

Project is considered v1 complete when all are true:

```text
[ ] Google OAuth works
[ ] Channel is discovered
[ ] Niche recommendation works
[ ] Channel strategy stored
[ ] Topic discovery works
[ ] Research evidence stored
[ ] Script generation works
[ ] TTS works
[ ] Captions work
[ ] Thumbnail generated
[ ] FFmpeg render works
[ ] Rights records exist
[ ] QA blocks invalid video
[ ] Video uploads privately
[ ] Scheduling works
[ ] Analytics collected
[ ] Learning created
[ ] Hourly scheduler runs
[ ] Jobs survive restart
[ ] Duplicate upload protection works
[ ] Secrets never logged
[ ] No fake-view system exists
```

---

# 75. Autonomous Mode Activation Gate

Autonomous publishing must stay OFF until:

```text
OAuth verified
API project configured
quota understood
private test upload successful
processing reconciliation tested
scheduling tested
rights workflow tested
QA tested
emergency stop tested
backup tested
logging audited
```

Then:

```text
AUTONOMOUS_PUBLISHING=true
```

should be a deliberate operator action.

---

# 76. First Video Dry Run

Required first run:

```text
Topic = manually selected
AI research = enabled
Script = generated
Voice = generated
Assets = original/licensed
Render = generated
QA = generated
Upload = PRIVATE
Schedule = disabled
```

Owner watches the final private video.

Only after a successful dry run should autonomous scheduling be activated.

---

# 77. First 24-Hour Automation Run

Expected sequence:

```text
Hour 1
trend + topic

Hour 2
research + script

Hour 3
visual plan + asset generation

Hour 4
voice + captions

Hour 5
render

Hour 6
QA

Hour 7
private upload

Hour 8
processing validation

Hour 9
scheduled publication

Hour 10
new topic
```

Workers may overlap when resources permit.

---

# 78. 7-Day Learning Cycle

At the end of week 1:

```text
collect all videos
calculate baseline metrics
identify top hooks
identify weak topics
identify thumbnail patterns
review retention
review costs
```

Do not change the entire strategy from one outlier video.

---

# 79. 30-Day Optimization Cycle

Evaluate:

```text
niche health
content pillar ROI
watch-time contribution
subscriber conversion
cost per published video
provider cost
production failure rate
average QA score
```

Generate:

```text
keep
increase
reduce
stop
experiment
```

Only approved strategic changes should alter the production planner in controlled mode.

---

# 80. Future Features

Possible later additions:

```text
multi-channel management
multiple Google accounts
brand accounts
affiliate link management
sponsor-read agent
podcast-to-video
blog-to-video
live stream preparation
community post drafting
Instagram/Reels repurposing
TikTok repurposing
advanced retention forecasting
voice cloning with explicit rights
local LLM mode
GPU cluster
```

Any future integration must preserve the same security, rights and anti-manipulation rules.

---

# 81. Operator Prompt for the AI

Use this as the top-level system instruction for the channel operator:

```text
You are the Autonomous YouTube Channel Operating Agent.

Your job is to operate a YouTube content pipeline while respecting channel configuration,
content rights, factual accuracy, platform rules, provider budgets, and quality thresholds.

You may research topics, rank opportunities, create editorial plans, write original scripts,
plan visuals, generate original media, prepare metadata, run QA, schedule eligible uploads,
and analyze performance.

You must never fabricate evidence, invent rights, upload unlicensed assets, create fake
engagement, manipulate views, bypass authentication controls, or conceal failures.

Every irreversible external action must be represented by a durable job and must be
idempotent. Before uploading, verify the complete production gate. If a gate fails, do not
publish; record the reason and continue with other eligible work.

Use analytics as evidence. Do not overreact to single outliers. Approved learnings may
influence future content planning.
```

---

# 82. OpenCode / Codex Implementation Prompt

Use this prompt after placing `BRAIN.md` in the repository:

```text
Read BRAIN.md completely before changing code.

Build the system exactly according to the architecture and contracts in BRAIN.md.

First inspect the existing repository and the three referenced source repositories.
Reuse components where architecture and licensing permit, but do not blindly merge projects.
Use the Node repository as the dashboard/integration reference and the Python repository as
the agent/pipeline reference.

Do not implement or import artificial YouTube engagement, view inflation, proxy-based
viewing, fake likes, fake subscribers, or fake watch time.

Do not ask for or store Gmail passwords. Implement Google OAuth 2.0 and encrypted token
storage instead.

Implement in phases and keep the project runnable after each phase:
1. config + database + logging
2. OAuth + YouTube channel discovery
3. niche/trend/research agents
4. script/visual/SEO/thumbnail agents
5. TTS/captions/FFmpeg
6. rights + QA gates
7. private upload + reconciliation + scheduling
8. analytics + learning
9. hourly scheduler
10. tests + observability + deployment

Before enabling autonomous publishing, prove a private test upload, processing
reconciliation, scheduling, recovery after restart, duplicate-upload protection, and
emergency stop.

Never hardcode API keys or credentials.

Use typed contracts and validate all agent outputs.

At every stage, update the implementation notes and tests.
```

---

# 83. Example Topic-to-Video Contract

```json
{
  "channel_id": "channel-001",
  "topic": {
    "title": "5 AI tools that automate boring work",
    "score": 0.91,
    "sources": []
  },
  "script": {
    "hook": "...",
    "sections": [],
    "cta": "..."
  },
  "visuals": {
    "aspect_ratio": "9:16",
    "scenes": []
  },
  "publishing": {
    "title": "...",
    "description": "...",
    "hashtags": [],
    "tags": []
  },
  "policy": {
    "rights": "VERIFIED",
    "factuality": "PASSED",
    "safety": "PASSED",
    "originality": "PASSED",
    "synthetic_media": false
  }
}
```

---

# 84. Example Scheduler Configuration

```yaml
scheduler:
  enabled: true
  tick: "0 * * * *"
  timezone: "Asia/Kolkata"

production:
  shorts:
    enabled: true
    max_per_day: 6
  long_form:
    enabled: true
    max_per_day: 2

publishing:
  autonomous: false
  upload_privacy: private
  schedule_enabled: true
  require_all_gates: true

budgets:
  daily_usd: 25
  monthly_usd: 500
```

Switch timezone according to the channel's chosen publishing region.

---

# 85. Example Niche Strategy

Example only:

```text
Niche: AI tools / productivity
Audience: students, creators, developers, knowledge workers
Pillars:
  1. tool discoveries
  2. comparisons
  3. tutorials
  4. workflow automation
Formats:
  70% Shorts
  30% long-form
Tone:
  practical
  energetic
  evidence-led
```

The system should choose the real niche dynamically; this is only the shape of the configuration.

---

# 86. Channel Memory Rules

Remember:

```text
recent topics
recent titles
recent hooks
winning thumbnail patterns
approved learnings
banned topics
provider performance
average production time
rights preferences
```

Forget or expire:

```text
stale trends
expired licenses
old low-confidence learnings
```

Never store unnecessary personal data.

---

# 87. Source Attribution

Every generated production stores a source bundle.

```json
{
  "sources": [
    {
      "url": "...",
      "publisher": "...",
      "published_at": "...",
      "retrieved_at": "...",
      "claims_supported": ["claim_1"]
    }
  ]
}
```

For factual videos, descriptions can include human-readable source links where appropriate.

---

# 88. Content Calendar Generation

The planner receives:

```text
30-day horizon
content pillars
weekly cadence
current backlog
historical winners
new trends
```

Returns:

```text
Day 1 topic A
Day 1 topic B
Day 2 topic C
...
```

Hourly scheduler selects from the approved queue rather than inventing an entirely new strategy every hour.

---

# 89. Backpressure Rules

If rendering queue exceeds:

```text
MAX_RENDER_QUEUE
```

stop creating new render jobs.

If upload queue exceeds:

```text
MAX_UPLOAD_QUEUE
```

stop generating unnecessary additional videos.

This prevents the system from spending money faster than it can publish.

---

# 90. Resource Governor

Control:

```text
CPU
RAM
GPU
storage
API quota
provider spend
```

Example:

```python
if gpu_utilization > 90:
    do_not_start_video_job()
```

The goal is stable throughput, not maximum parallelism.

---

# 91. Storage Lifecycle

Directories:

```text
storage/
├── raw/
├── research/
├── audio/
├── captions/
├── scenes/
├── renders/
├── thumbnails/
├── uploads/
├── published/
└── archive/
```

Use checksums and production IDs.

Example:

```text
storage/renders/<production_id>/final.mp4
```

---

# 92. Data Retention

Default:

```text
raw generated scenes: 30 days
intermediate render files: 14 days
final published assets: 1 year or configurable
analytics: long-term
rights evidence: long-term
logs: 30-90 days
```

Never delete evidence needed to establish content rights.

---

# 93. Privacy

Minimize personal information.

Channel-level data is operational data.

Do not collect unrelated Gmail mail or contacts.

This application should request only YouTube/Google scopes necessary for its functions.

---

# 94. Emergency Stop

Global switch:

```text
EMERGENCY_STOP=true
```

Behavior:

```text
stop new uploads
stop new scheduling
allow read-only analytics
allow in-progress render completion or terminate safely
show red banner
```

Reset requires an explicit operator action.

---

# 95. Disaster Recovery Scenarios

### Scenario A: Database lost

Restore backup → reconcile YouTube by channel/video IDs.

### Scenario B: VPS dies

New machine → restore secrets → restore DB → restore object storage → run reconciliation.

### Scenario C: upload succeeded but client timed out

Reconciliation must find existing video before retrying.

### Scenario D: provider API unavailable

Pause affected jobs, switch provider where safe.

### Scenario E: YouTube API unavailable

Continue local generation within cost budget; hold uploads.

---

# 96. Performance Targets

Target v1:

```text
Dashboard response p95 < 500 ms for standard reads
Job enqueue < 1 s
Scheduler tick < 10 s
Database queries indexed
No duplicate upload under retry
```

Actual video rendering time depends on provider and hardware.

---

# 97. Engineering Principles

1. Secure by default.
2. Typed contracts.
3. Idempotent side effects.
4. Evidence before claims.
5. Rights before publication.
6. Originality before scale.
7. Analytics before optimization.
8. Backpressure before overload.
9. Human override at every important boundary.
10. Every external side effect is observable.

---

# 98. Definition of “Done” for Each Video

A video is DONE only when:

```text
[✓] topic selected
[✓] research complete
[✓] claims supported or intentionally marked
[✓] script generated
[✓] scenes generated
[✓] rights verified
[✓] voice generated
[✓] captions generated
[✓] thumbnail generated
[✓] final render validated
[✓] metadata validated
[✓] safety gate passed
[✓] originality gate passed
[✓] private upload reconciled
[✓] schedule stored
[✓] publication confirmed
[✓] analytics tracking registered
```

---

# 99. Final Repository Checklist

```text
[ ] README explains architecture
[ ] BRAIN.md present
[ ] .env.example present
[ ] .gitignore secure
[ ] OAuth implementation documented
[ ] YouTube upload implementation documented
[ ] scheduler tested
[ ] Docker Compose works
[ ] PostgreSQL migration works
[ ] Redis works
[ ] Python worker starts
[ ] Node dashboard starts
[ ] FFmpeg installed/verified
[ ] test channel configured
[ ] private upload test complete
[ ] emergency stop tested
```

---

# 100. Final Master Workflow

```text
                    ┌─────────────────────┐
                    │  Google OAuth       │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  YouTube Channel    │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Niche Intelligence │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Channel Strategy   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Trend Radar        │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Topic Selector     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Research + Claims  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Script Agent       │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Visual Planner     │
                    └──────────┬──────────┘
                               ↓
               ┌───────────────┼────────────────┐
               ↓               ↓                ↓
          AI Video        Licensed Media   Owned Assets
               └───────────────┼────────────────┘
                               ↓
                    ┌─────────────────────┐
                    │  TTS + Captions     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  FFmpeg Render      │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  QA / Rights Gate  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Private Upload     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Processing Check   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Scheduled Publish  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Analytics Engine   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Learning Engine    │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Next Hour / Topic  │
                    └─────────────────────┘
```

---

# 101. Final Security Note

The Gmail address supplied during the design process must not be written into source code or BRAIN.md. The Gmail password must not be written anywhere in the application. Replace any password that has been exposed and use OAuth.

For actual deployment, create a Google Cloud OAuth application, connect the account through the dashboard, and store only the resulting encrypted OAuth credentials.

---

# 102. Current External References

- Google OAuth 2.0 for YouTube: https://developers.google.com/youtube/v3/guides/authentication
- YouTube Data API reference: https://developers.google.com/youtube/v3/docs
- YouTube `videos.insert`: https://developers.google.com/youtube/v3/docs/videos/insert
- YouTube upload guide: https://developers.google.com/youtube/v3/guides/uploading_a_video
- YouTube scheduled publishing help: https://support.google.com/youtube/answer/1270709
- YouTube monetization/originality guidance: https://support.google.com/youtube/answer/2490020

Treat the official Google/YouTube documentation as authoritative when API behavior changes.

---

# 103. Build Directive

Implement the system as an original integration project inspired by the inspected repositories, not as a blind copy.

Start with a safe private-upload proof of concept. Then enable the complete production workflow.

The intended outcome is:

```text
ONE DASHBOARD
      ↓
ONE CHANNEL MEMORY
      ↓
ONE AUTONOMOUS CONTENT BRAIN
      ↓
HOURLY ELIGIBILITY CHECKS
      ↓
ORIGINAL / LICENSED CONTENT
      ↓
AUTOMATED PRODUCTION
      ↓
YOUTUBE SCHEDULING
      ↓
ANALYTICS
      ↓
CONTINUOUS IMPROVEMENT
```

**End of BRAIN.md**

# 87. DETAILED STATE-TRANSITION CONTRACTS

The workflow engine is the single source of truth for content state. UI labels, API responses, worker queues, and database records must reflect the same state machine.

## 87.1 State transition table

| Current | Event | Required checks | Next state | Side effect |
|---|---|---|---|---|
| IDEA | START_RESEARCH | channel active | RESEARCHING | enqueue research |
| RESEARCHING | RESEARCH_SUCCESS | sources >= minimum | RESEARCH_READY | persist packet |
| RESEARCHING | RESEARCH_FAILURE | retryable? | FAILED/RESEARCHING | retry/backoff |
| RESEARCH_READY | START_SCRIPT | evidence valid | SCRIPTING | enqueue script |
| SCRIPTING | SCRIPT_SUCCESS | schema valid | SCRIPT_READY | persist script |
| SCRIPTING | SCRIPT_FAILURE | retryable? | FAILED/SCRIPTING | retry |
| SCRIPT_READY | PLAN_VISUALS | script valid | ASSET_PLANNING | enqueue visual plan |
| ASSET_PLANNING | PLAN_SUCCESS | scene timings valid | ASSETS_PENDING | enqueue assets |
| ASSETS_PENDING | ASSETS_COMPLETE | rights complete | RENDERING | enqueue render |
| RENDERING | RENDER_SUCCESS | ffprobe valid | QUALITY_REVIEW | enqueue review |
| QUALITY_REVIEW | PASS | all gates pass | HUMAN_REVIEW or APPROVED | policy-dependent |
| QUALITY_REVIEW | FAIL | revision possible | REVISION_REQUIRED | store findings |
| REVISION_REQUIRED | REVISE | remaining attempts | SCRIPTING/ASSET_PLANNING | targeted invalidation |
| HUMAN_REVIEW | APPROVE | operator authorized | APPROVED | audit approval |
| HUMAN_REVIEW | REJECT | reason present | REJECTED | audit rejection |
| APPROVED | SCHEDULE | publish policy permits | SCHEDULED | enqueue publish |
| SCHEDULED | START_UPLOAD | auth+quota+preflight | UPLOADING | upload request |
| UPLOADING | SUCCESS | ID returned | PUBLISHED | persist video ID |
| UPLOADING | TIMEOUT | possible side effect | UNKNOWN_UPLOAD | reconciliation job |
| UNKNOWN_UPLOAD | RECONCILE_FOUND | matching video | PUBLISHED | link remote ID |
| UNKNOWN_UPLOAD | RECONCILE_NOT_FOUND | safe retry | SCHEDULED | retry upload |
| PUBLISHED | ANALYTICS_SYNC | auth valid | ANALYTICS_ACTIVE | store snapshot |
| ANALYTICS_ACTIVE | LEARNING_READY | sufficient evidence | LEARNING_READY | recommendation |

Illegal transitions must raise `StateTransitionError` and create an audit event. Do not mutate the database first and validate later.

# 88. WORKFLOW ORCHESTRATOR DESIGN

The orchestrator manages workflow execution but does not contain provider-specific implementation details.

```python
class WorkflowOrchestrator:
    async def execute(self, run_id: UUID) -> WorkflowResult:
        run = await repository.load_run(run_id)
        definition = registry.get(run.workflow_type)
        await state_machine.assert_executable(run)

        for step in definition.steps:
            if await checkpoint_store.is_complete(run_id, step.name):
                continue

            result = await worker_dispatcher.dispatch(step, run)
            await checkpoint_store.commit(run_id, step.name, result)

        return await repository.complete_run(run_id)
```

## 88.1 Workflow requirements

Every workflow must have:

```text
workflow_id
workflow_type
entity_id
version
started_at
heartbeat_at
status
current_step
attempt_count
correlation_id
error_code
error_message
```

## 88.2 Workflow invariants

- Only one active execution may own a given workflow lock.
- A completed step is immutable unless explicitly invalidated.
- Every step input and output is hashable.
- Every external side effect is idempotent or reconciliable.
- Retry count is bounded.
- Workflow cancellation is cooperative.

# 89. JOB QUEUE SEMANTICS

Use separate queues to prevent heavy video jobs from starving lightweight tasks.

```text
queue.research
queue.editorial
queue.media
queue.render
queue.publish
queue.analytics
queue.maintenance
```

Each job contains:

```json
{
  "job_id": "uuid",
  "workflow_id": "uuid",
  "type": "render_video",
  "priority": 3,
  "attempt": 1,
  "max_attempts": 2,
  "scheduled_at": "timestamp",
  "deadline_at": "timestamp",
  "idempotency_key": "render:video:uuid",
  "payload_version": 1
}
```

## 89.1 Queue guarantees

Required behaviors:
- at-least-once delivery;
- idempotent workers;
- visibility timeout;
- dead-letter queue;
- retry delay;
- queue metrics;
- graceful shutdown.

Never assume exactly-once delivery.

# 90. DISTRIBUTED LOCKING

The scheduler must not run twice for the same channel during the same interval.

Lock key:

```text
scheduler:{channel_id}:hourly
```

Acquire with TTL.
Renew for long runs.
Release in `finally`.

If lock acquisition fails:

```text
log INFO: another scheduler owns run
exit normally
```

Do not create duplicate jobs merely because a lock could not be acquired.

# 91. CRON AND TIMEZONE RULES

All persisted timestamps are UTC.

Channel-facing schedules are evaluated in the channel timezone.

```text
UTC database
   ↓
channel.timezone
   ↓
local publish_at
```

Daylight saving transitions must be handled by a timezone-aware library; never manually add/subtract hours.

For the initial India deployment:

```text
CHANNEL_TIMEZONE=Asia/Kolkata
```

An hourly scheduler should run continuously in UTC while interpreting publishing windows in channel-local time.

# 92. HOURLY TICK DETAILED ALGORITHM

```python
def hourly_tick(channel_id, now_utc):
    with scheduler_lock(channel_id):
        run_id = create_run("HOURLY_CHANNEL_TICK")

        ensure_database_ready()
        ensure_storage_ready()
        ensure_queue_ready()

        reconcile_unknown_uploads(channel_id)
        recover_expired_jobs(channel_id)
        retry_due_jobs(channel_id)

        channel = get_channel(channel_id)
        policy = get_publish_policy(channel_id)
        budget = calculate_budget(channel_id)
        capacity = calculate_capacity(channel_id)

        if analytics_window_due(channel_id, now_utc):
            enqueue_unique("ANALYTICS_REFRESH", channel_id)

        if research_window_due(channel_id, now_utc):
            enqueue_unique("TOPIC_RESEARCH", channel_id)

        backlog = calculate_backlog(channel_id)

        while capacity.has_generation_slot() and backlog.needs_content():
            topic = choose_next_topic(channel_id)
            if not topic:
                break

            if budget.insufficient_for(topic):
                mark_topic_deferred(topic, "BUDGET")
                break

            create_content_workflow(topic)
            capacity.consume_generation_slot()
            backlog.increment()

        dispatch_due_publish_jobs(channel_id, policy)
        persist_tick_metrics(run_id)
        complete_run(run_id)
```

## 92.1 Backlog target algorithm

```text
TARGET_READY_BACKLOG = 3
TARGET_SCHEDULED_BACKLOG = 7
```

If scheduled backlog exceeds target, stop generating production assets and focus on analytics/research.

If backlog is below target, increase generation within cost and capacity bounds.

# 93. TOPIC SELECTION PIPELINE

```text
Raw Signals
    ↓
Normalize
    ↓
Language Filter
    ↓
Age/Recency Filter
    ↓
Category Classifier
    ↓
Duplicate Detector
    ↓
Risk Classifier
    ↓
Audience Match
    ↓
Trend Scoring
    ↓
Historical Performance Prior
    ↓
Diversity Penalty
    ↓
Final Rank
```

## 93.1 Topic candidate schema

```json
{
  "candidate_id": "uuid",
  "canonical_topic": "...",
  "source_signals": [],
  "detected_at": "timestamp",
  "momentum": 0.0,
  "audience_fit": 0.0,
  "novelty": 0.0,
  "competition": 0.0,
  "risk": 0.0,
  "confidence": 0.0
}
```

# 94. COMPETITOR/REFERENCE ANALYSIS

Reference channels are used for structural analysis only.

Allowed analysis:
- topic frequency;
- title patterns;
- upload cadence;
- publicly observable video metadata;
- public engagement patterns;
- topic gaps.

Do not clone scripts, thumbnails, branding, or footage.

## 94.1 Content gap algorithm

```text
competitor_topics
       ↓
cluster topics
       ↓
compare with own channel coverage
       ↓
identify underserved clusters
       ↓
score audience fit
       ↓
generate original angle
```

# 95. ORIGINALITY ENGINE

Before final script approval, calculate similarity against the channel archive.

Signals:
- title similarity;
- paragraph similarity;
- hook similarity;
- sequence similarity;
- visual-plan similarity.

If similarity exceeds configured threshold:

```text
REJECT DUPLICATE
    ↓
GENERATE DIFFERENT ANGLE
```

Do not simply change adjectives in a copied script.

# 96. SCRIPT REVISION ALGORITHM

When QualityReviewer returns a failure:

```python
def revise_script(package, findings):
    allowed = findings.allowed_revision_scope

    if "FACTUAL" in findings:
        return rewrite_with_sources(package, findings)

    if "HOOK" in findings:
        return revise_hook_only(package)

    if "DUPLICATE" in findings:
        return regenerate_angle(package)

    return targeted_revision(package, findings)
```

Never regenerate the whole production if the failure is isolated to metadata or one scene.

# 97. SCENE REPAIR ALGORITHM

```text
Identify failed scene
       ↓
Check dependency graph
       ↓
Invalidate scene output
       ↓
Preserve unaffected scenes
       ↓
Regenerate scene
       ↓
Recalculate timeline
       ↓
Rebuild captions if timing changed
       ↓
Re-render final MP4
       ↓
Re-run quality gates
```

## 97.1 Dependency graph

```text
Script paragraph
    ├── narration
    ├── scene
    │    ├── visual asset
    │    └── caption timing
    └── metadata claim
```

# 98. VIDEO HASHING AND ARTIFACT IDENTITY

Every final artifact receives SHA-256.

```text
content_hash = SHA256(final_file_bytes)
```

Also store logical identity:

```text
artifact_key = hash(video_id + stage + provider + version)
```

This enables safe cache reuse.

# 99. STORAGE LAYOUT CONTRACT

```text
storage/
└── channels/{channel_id}/
    ├── research/{run_id}/
    ├── scripts/{video_id}/
    ├── assets/{video_id}/
    ├── narration/{video_id}/
    ├── captions/{video_id}/
    ├── thumbnails/{video_id}/
    ├── renders/{video_id}/
    ├── manifests/{video_id}/
    └── logs/{run_id}/
```

Do not use user-visible titles as primary filesystem paths. Titles can contain unsafe characters and can change.

# 100. MANIFEST FORMAT

Each production must contain a manifest:

```json
{
  "schema_version": 1,
  "video_id": "uuid",
  "strategy_version": 3,
  "prompt_versions": {
    "script": "v1",
    "visual": "v1",
    "seo": "v1"
  },
  "scenes": [],
  "assets": [],
  "audio": {},
  "captions": {},
  "thumbnail": {},
  "quality": {},
  "provenance": {},
  "cost": {},
  "created_at": "timestamp"
}
```

The manifest is the canonical reproducibility record for the video.

# 101. PROVIDER HEALTH MODEL

Each provider has:

```text
availability
latency_p50
latency_p95
error_rate
cost_estimate
quota_remaining
last_success
last_failure
```

Provider selection score:

```text
ProviderScore =
  reliability * 0.35
+ quality * 0.30
+ cost_efficiency * 0.20
+ latency * 0.15
```

Only providers explicitly enabled by the operator may be selected.

# 102. CIRCUIT BREAKER

When a provider repeatedly fails:

```text
CLOSED
  ↓ repeated failures
OPEN
  ↓ cooldown
HALF_OPEN
  ↓ successful probe
CLOSED
```

Do not continue hammering an unhealthy endpoint.

# 103. RATE LIMITING

Implement rate limits at:
- external provider client;
- API routes;
- publishing worker;
- research collector;
- scheduler enqueue layer.

Use token-bucket or provider-specific rate-limit logic where appropriate.

# 104. COST ESTIMATION BEFORE EXECUTION

Every paid job should estimate cost before execution.

```python
estimate = provider.estimate_cost(request)

if estimate > remaining_budget:
    raise BudgetExceeded()
```

For uncertain costs, store:

```text
estimated_min
estimated_max
actual_cost
```

Do not represent an unknown cost as zero.

# 105. AUTONOMY POLICY ENGINE

Autonomy is a policy object, not a collection of booleans spread through code.

```json
{
  "generate": true,
  "render": true,
  "upload": false,
  "publish": false,
  "max_videos_per_day": 5,
  "max_spend_per_day": 20,
  "require_human_for_sensitive_topics": true,
  "require_human_for_unknown_rights": true
}
```

Policy evaluation:

```python
def can_publish(video, channel_policy):
    checks = [
        video.quality_passed,
        video.rights_passed,
        video.metadata_passed,
        video.oauth_ready,
        video.cost_within_budget,
        channel_policy.upload_enabled,
        channel_policy.publish_enabled,
    ]
    return all(checks)
```

# 106. SENSITIVE-TOPIC ROUTING

Topic sensitivity may require an additional review state.

```text
NORMAL
  ↓
SENSITIVE
  ↓
ENHANCED_REVIEW
```

The classifier must be deterministic for known policy rules where possible and must record why enhanced review was triggered.

# 107. HUMAN REVIEW SLA

The system should track:

```text
review_requested_at
first_viewed_at
decision_at
reviewer_id
revision_count
```

Dashboard metrics:
- queue age;
- average decision time;
- rejected percentage;
- common rejection reasons.

# 108. NOTIFICATION ROUTING

Notification severity:

```text
INFO       dashboard only
WARNING    dashboard + optional webhook
ERROR      dashboard + webhook
CRITICAL   dashboard + webhook + persistent alert
```

Never put OAuth tokens or sensitive payloads in notifications.

# 109. API RESPONSE CONTRACT

Standard response envelope:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "request_id": "uuid"
}
```

Error:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VIDEO_NOT_APPROVABLE",
    "message": "Rights evidence is incomplete",
    "details": {}
  },
  "request_id": "uuid"
}
```

Do not return stack traces in production.

# 110. PAGINATION

All potentially large list APIs must paginate.

Use cursor pagination for analytics/events where practical.

Example:

```http
GET /api/videos?cursor=abc&limit=50
```

Maximum server-side page size must be enforced.

# 111. API VERSIONING

Breaking changes require:

```text
/api/v1/...
/api/v2/...
```

Do not silently redefine `/api/v1` semantics.

# 112. DATABASE INDEXING STRATEGY

Index:

```text
channels.youtube_channel_id
videos.channel_id,status
videos.publish_at,status
topics.channel_id,score
jobs.status,scheduled_at
analytics_snapshots.video_id,captured_at
assets.video_id,rights_status
```

Add indexes only with measured workload justification.

# 113. DATABASE TRANSACTION RULES

Use transactions for coupled changes.

Example publish state transition:

```text
BEGIN
  mark UPLOADING
  create audit event
COMMIT

external upload

BEGIN
  persist youtube_video_id
  mark PUBLISHED
  create audit event
COMMIT
```

Never hold a long database transaction open during a multi-minute video upload.

# 114. CONCURRENCY RULES

Safe concurrency:
- multiple research jobs for independent channels;
- multiple analytics refreshes subject to quota;
- limited rendering workers.

Unsafe without locking:
- two publishes of same video;
- two strategy activations;
- two hourly scheduler runs for same channel;
- two edits of same review record.

Use optimistic versioning where possible:

```text
UPDATE ... WHERE id=? AND version=?
```

# 115. EVENTUAL CONSISTENCY RULES

External systems are authoritative for remote state.

Example:

```text
Local DB says SCHEDULED
YouTube says PRIVATE
```

Reconciliation must resolve the discrepancy based on fresh API state and record the decision.

# 116. YOUTUBE REMOTE RECONCILIATION

Periodic reconciliation should inspect:
- scheduled videos;
- upload status;
- privacy status;
- publish time;
- thumbnail status where available;
- deleted/missing remote videos.

Local database should never assume a remote operation succeeded solely because a request was sent.

# 117. PUBLISH WINDOW SELECTION

Given a desired local-time window:

```text
candidate times
   ↓
filter conflicts
   ↓
apply channel history
   ↓
avoid excessive clustering
   ↓
select next valid time
```

Analytics may later learn preferred publishing windows, but learning recommendations must not override a hard operator schedule.

# 118. CONTENT CALENDAR CONFLICT RESOLUTION

Priority:

```text
manual fixed schedule
    > approved campaign
    > experiment
    > normal scheduled content
    > exploratory content
```

When conflicts occur, lower-priority content moves to the next open slot.

# 119. CAMPAIGN MODEL

A campaign groups related videos:

```text
campaign
 ├── objective
 ├── start/end
 ├── audience
 ├── pillar
 ├── creative constraints
 └── video_ids
```

Campaign-level analytics should compare performance against campaign objective.

# 120. SHORTS REPURPOSING ALGORITHM

```text
approved long-form video
        ↓
scene timeline
        ↓
identify self-contained segments
        ↓
score hook completeness
        ↓
score payoff completeness
        ↓
score context independence
        ↓
select top N
        ↓
9:16 layout
        ↓
captions
        ↓
review
        ↓
schedule
```

Never create a Short that misleadingly removes context from the source.

# 121. AUDIO/VIDEO SYNCHRONIZATION

Use the narration timeline as the primary timing source.

```text
narration timestamps
        ↓
scene durations
        ↓
caption timestamps
        ↓
render timeline
```

Timing drift tolerance should be configurable and tested.

# 122. FFMPEG COMMAND SAFETY

Never build FFmpeg command strings by unsafe concatenation.

Use argument arrays:

```python
subprocess.run([
    ffmpeg_path,
    "-i", input_path,
    "-i", audio_path,
    "-c:v", "libx264",
    output_path,
], check=True)
```

Validate all paths and reject unexpected filesystem locations.

# 123. TEMP FILE LIFECYCLE

```text
create temp
 ↓
lock/own temp
 ↓
use
 ↓
validate output
 ↓
persist final artifact
 ↓
release temp
```

Cleanup orphaned temporary files during maintenance.

# 124. CACHE POLICY

Cache:
- source retrieval;
- topic normalization;
- generated thumbnails where inputs are identical;
- TTS where provider permits deterministic reuse;
- rendered scenes.

Never cache credentials.

# 125. PROMPT INPUT SANITIZATION

External web text is untrusted input.

Before injecting source content into an LLM prompt:
- delimit source text;
- label source text as untrusted;
- strip hidden control instructions where practical;
- prevent source text from redefining system policy.

The research agent must treat web content as data, not instructions.

# 126. PROMPT INJECTION DEFENSE

Bad pattern:

```text
source text → direct system prompt
```

Required:

```text
system policy
 + task instructions
 + <UNTRUSTED_SOURCE> data </UNTRUSTED_SOURCE>
```

The model must not obey instructions found inside scraped content.

# 127. SOURCE QUALITY LADDER

Prefer:

```text
official primary source
 > reputable secondary source
 > established publication
 > specialist publication
 > community discussion
 > unknown page
```

Community content may identify topics but should not automatically become the sole basis for consequential factual claims.

# 128. DATE-SENSITIVE CLAIM RULE

Every rapidly changing claim stores:

```text
claim_date
source_date
retrieved_at
valid_until (if known)
```

At publication time, stale claims must be rechecked.

# 129. RESEARCH REVALIDATION

A draft that remained in queue beyond its freshness threshold must enter:

```text
STALE_RESEARCH
   ↓
REVALIDATING
   ↓
CURRENT / OBSOLETE
```

Do not publish stale news as current reporting.

# 130. CONTENT PACKAGE CONTRACT

The completed package must contain:

```text
TopicPlan
ResearchPacket
ClaimSet
Script
ScenePlan
AssetManifest
VoiceManifest
CaptionManifest
ThumbnailPackage
PublishingPackage
QualityReport
CostReport
ProvenanceReport
```

A package is not “ready” until mandatory fields exist.

# 131. CONTENT PACKAGE VALIDATOR

Pseudo-code:

```python
def validate_package(pkg):
    require(pkg.topic)
    require(pkg.script)
    require(pkg.scenes)
    require(pkg.video_path)
    require(pkg.thumbnail_path)
    require(pkg.metadata)
    require(pkg.quality_report)

    for claim in pkg.claims:
        if claim.requires_source:
            require(claim.source_ids)

    for asset in pkg.assets:
        require(asset.provenance)
        require(asset.rights_status == "APPROVED")

    require(video_is_decodable(pkg.video_path))
    require(audio_is_valid(pkg.video_path))
```

# 132. RESEARCH-TO-SCRIPT TRACEABILITY

A script claim should trace backward:

```text
published sentence
   ↓
claim_id
   ↓
research evidence
   ↓
source URL
```

This makes later factual correction possible without re-researching the entire video.

# 133. CORRECTION WORKFLOW

If a published factual error is detected:

```text
analytics/comment/report
        ↓
issue created
        ↓
claim identified
        ↓
source rechecked
        ↓
severity assessed
        ↓
correction decision
        ↓
operator notified
```

Do not automatically edit or delete published content solely because a low-confidence model detected a possible issue.

# 134. COMMENTS / AUDIENCE SIGNALS

The engagement system may classify comments into:

```text
question
request
praise
criticism
spam
scam
off-topic
```

Only approved workflows may produce replies.

Audience-requested topics can become future topic candidates with evidence links to comments.

# 135. COMMENT SAFETY

Never automatically reply to:
- obvious scams;
- requests for passwords/credentials;
- dangerous instructions;
- abusive content;
- malicious links.

Flag for review instead.

# 136. MODEL SELECTION ROUTER

Select model based on task class rather than one model for everything.

```text
simple classification → cheap/fast model
research synthesis → capable reasoning model
script generation → high-quality writing model
thumbnail prompt → visual-capable model
analytics summary → cheap structured model
```

Model choice must remain configurable.

# 137. LLM BUDGET GUARD

Track tokens:

```text
prompt_tokens
completion_tokens
cached_tokens
estimated_cost
actual_cost
```

If token budget is exceeded:

```text
reduce context
 ↓
summarize memory
 ↓
retry
```

Do not silently omit critical evidence merely to fit a context window.

# 138. CONTEXT MEMORY COMPRESSION

When memory becomes large:

```text
raw history
  ↓
structured facts
  ↓
rolling summary
  ↓
recent exact examples
```

Keep canonical structured data in the database; summaries must not become the only source of truth.

# 139. PROMPT VERSION EXPERIMENTS

Prompt changes are experiments when behavior changes materially.

Store:

```text
prompt_version
model
temperature/settings if applicable
input schema version
output schema version
```

Compare quality outcomes before promoting a new prompt.

# 140. FEATURE DEVELOPMENT WORKFLOW FOR AI CODING AGENTS

```text
READ brain.md
     ↓
READ target module
     ↓
READ tests
     ↓
SEARCH for existing behavior
     ↓
DEFINE change
     ↓
CHECK state/schema/API impact
     ↓
IMPLEMENT
     ↓
TEST
     ↓
LINT / TYPECHECK
     ↓
RUN targeted integration tests
     ↓
UPDATE docs
     ↓
REPORT exact changes
```

# 141. AI AGENT CHANGE RISK CLASSIFICATION

### LOW
- UI copy;
- isolated component styling;
- pure helper;
- non-behavioral documentation.

### MEDIUM
- provider adapter;
- new API endpoint;
- analytics query;
- non-breaking schema addition.

### HIGH
- database migration;
- state transition;
- publishing logic;
- OAuth changes;
- scheduler behavior;
- autonomy defaults.

High-risk changes require explicit tests and a migration/rollback plan.

# 142. ROLLBACK STRATEGY

For every high-risk deployment:

```text
new version
    ↓
health checks
    ↓
shadow/staging validation
    ↓
limited rollout
    ↓
monitor
    ↓
full rollout
```

Database migrations must have a safe forward compatibility strategy even when rollback is not directly possible.

# 143. STAGING ENVIRONMENT

Staging must never publish to the production channel.

Use:

```text
YOUTUBE_CHANNEL_MODE=STAGING
PUBLISH_AUTOMATION_ENABLED=false
```

Where possible use a dedicated test channel.

# 144. DRY-RUN MODE

Support:

```text
DRY_RUN=true
```

In dry run:
- research may execute;
- scripts may generate;
- rendering may execute if enabled;
- upload API is never called;
- scheduler simulates decisions;
- all intended actions are logged.

# 145. SANDBOX PUBLISH TEST

Before production activation:

```text
OAuth test
 ↓
channel identity
 ↓
small media validation
 ↓
private upload if permitted
 ↓
remote ID reconciliation
 ↓
thumbnail validation
 ↓
analytics read test
```

The system should not use public publishing as its first connectivity test.

# 146. READINESS CHECK

Return a structured readiness report:

```json
{
  "oauth": "PASS",
  "youtube_read": "PASS",
  "youtube_upload": "UNKNOWN",
  "llm": "PASS",
  "tts": "PASS",
  "ffmpeg": "PASS",
  "storage": "PASS",
  "database": "PASS",
  "scheduler": "PASS",
  "budget": "PASS"
}
```

A failed required dependency blocks autonomous execution.

# 147. MAINTENANCE JOBS

Scheduled maintenance:

```text
hourly:
  queue recovery
  readiness check

6-hourly:
  analytics refresh
  remote reconciliation

nightly:
  temp cleanup
  database maintenance
  storage accounting
  error aggregation

weekly:
  learning report
  provider performance
  budget review
```

# 148. DATABASE CLEANUP

Never delete records merely because a file was deleted.

Use soft deletion for business objects where audit history matters.

```text
deleted_at
deleted_by
```

# 149. PRIVACY

Only collect data required for operation.

Do not store Gmail inbox contents as part of YouTube automation unless a separately authorized feature requires it.

OAuth scopes should be minimal.

# 150. SECRET ROTATION

Support replacing:
- Google client secret;
- OAuth refresh tokens;
- provider API keys;
- webhook secrets.

Rotation must not require deleting channel history.

# 151. API KEY MANAGEMENT

Keys should have:

```text
provider
created_at
last_used_at
status
rotation_due_at
```

Do not expose them in frontend JavaScript.

# 152. BACKUP VERIFICATION

A backup is not considered successful merely because the database produced a dump.

Nightly process:

```text
backup
 ↓
checksum
 ↓
restore test
 ↓
verify row counts
 ↓
verify critical tables
 ↓
record result
```

# 153. RECOVERY TIME OBJECTIVES

Initial targets:

```text
API recovery: < 30 min
Scheduler recovery: < 30 min
Database recovery: < 60 min
Media recovery: < 4 hr
```

These are engineering targets, not guarantees, and should be revised after deployment measurements.

# 154. RELEASE CHECKLIST

Before release:

```text
[ ] tests pass
[ ] typecheck pass
[ ] lint pass
[ ] database migrations reviewed
[ ] security scan pass
[ ] OAuth flow checked
[ ] scheduler checked
[ ] upload reconciliation checked
[ ] no secrets in diff
[ ] feature flags reviewed
[ ] changelog updated
[ ] brain.md updated
```

# 155. INCIDENT RESPONSE

When an automated publish behaves unexpectedly:

```text
1. Disable publishing feature flag.
2. Preserve logs and audit records.
3. Reconcile remote YouTube state.
4. Identify workflow/run IDs.
5. Freeze affected jobs.
6. Patch root cause.
7. Test staging.
8. Resume only after readiness check.
```

# 156. OBSERVABILITY DASHBOARD

Main panels:

```text
System Health
Queue Depth
Active Jobs
Failed Jobs
OAuth Status
Provider Health
Daily Spend
Uploads Today
Published Today
Review Backlog
Analytics Freshness
Disk Usage
```

# 157. TRACE CORRELATION

Every request/job/workflow should share:

```text
request_id
correlation_id
workflow_id
job_id
entity_id
```

This makes it possible to reconstruct a failure across API → worker → provider → database.

# 158. PERFORMANCE BUDGETS

Initial operational targets:

```text
dashboard initial data response: < 1 sec locally
API typical metadata endpoint: < 500 ms excluding providers
queue dispatch: < 2 sec
analytics persistence: batch writes preferred
```

Video-generation latency is provider-dependent and should not be forced into API request/response paths.

# 159. ASYNCHRONOUS API PATTERN

Long operations must return:

```http
202 Accepted
```

with:

```json
{
  "job_id": "uuid",
  "status": "QUEUED",
  "status_url": "/api/jobs/uuid"
}
```

Never hold an HTTP request open for a multi-minute render.

# 160. JOB STATUS API

```http
GET /api/jobs/:job_id
```

Response:

```json
{
  "job_id": "...",
  "status": "RUNNING",
  "progress": 0.62,
  "current_step": "RENDER_AUDIO",
  "started_at": "...",
  "updated_at": "..."
}
```

# 161. PROGRESS MODEL

Progress must represent meaningful workflow stages rather than arbitrary fake percentages.

Example:

```text
research      10%
script        20%
visual plan   30%
assets        45%
voice         55%
render        75%
quality       90%
publish       100%
```

If a stage is indeterminate, show `indeterminate` rather than pretending.

# 162. DATABASE + QUEUE CONSISTENCY

When creating a job and its queue message:

Preferred pattern:

```text
DB transaction
   ↓
outbox event
   ↓
outbox dispatcher
   ↓
queue
```

This prevents the database from saying a job exists while the queue message was lost.

# 163. OUTBOX PATTERN

```sql
outbox_events (
  id UUID PRIMARY KEY,
  aggregate_type TEXT,
  aggregate_id UUID,
  event_type TEXT,
  payload JSONB,
  created_at TIMESTAMP,
  published_at TIMESTAMP NULL
)
```

Dispatcher retries unpublished events safely.

# 164. DEAD-LETTER QUEUE

A job enters DLQ after bounded retries.

DLQ payload must contain:

```text
original_job_id
failure_code
attempts
last_error
stack_hash
created_at
```

Operators can inspect and requeue after diagnosis.

# 165. REQUEUE POLICY

Requeue only after classifying:

```text
TRANSIENT → retry
CONFIGURATION → fix config then retry
DATA → fix data then retry
POLICY → manual decision
PERMANENT → abandon
```

# 166. DATABASE SCHEMA EXPANSION

Additional tables recommended:

```text
workflow_runs
workflow_steps
jobs
outbox_events
audit_events
provider_usage
provider_health
reviews
approvals
research_sources
research_claims
voice_profiles
caption_tracks
experiments
learning_recommendations
notifications
cost_records
```

Each should use UUID primary keys and timestamps.

# 167. CLAIM TABLE

```sql
research_claims (
  id UUID PRIMARY KEY,
  research_packet_id UUID NOT NULL,
  text TEXT NOT NULL,
  claim_type TEXT NOT NULL,
  confidence NUMERIC NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
)
```

# 168. CLAIM-SOURCE JOIN

```sql
claim_sources (
  claim_id UUID NOT NULL,
  source_id UUID NOT NULL,
  support_strength NUMERIC,
  PRIMARY KEY (claim_id, source_id)
)
```

# 169. REVIEW RECORD

```sql
reviews (
  id UUID PRIMARY KEY,
  video_id UUID NOT NULL,
  review_type TEXT NOT NULL,
  result TEXT NOT NULL,
  findings JSONB,
  reviewer_id UUID NULL,
  reviewed_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL
)
```

# 170. LEARNING RECOMMENDATION RECORD

```sql
learning_recommendations (
  id UUID PRIMARY KEY,
  channel_id UUID NOT NULL,
  type TEXT NOT NULL,
  evidence JSONB NOT NULL,
  confidence NUMERIC NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  decided_at TIMESTAMP NULL
)
```

# 171. LEARNING LIFECYCLE

```text
OBSERVED
 ↓
ANALYZED
 ↓
PROPOSED
 ↓
PENDING_APPROVAL
 ↓
APPROVED / REJECTED
 ↓
APPLIED
 ↓
MEASURED
```

This creates an evidence loop instead of untracked model behavior changes.

# 172. STRATEGY VERSIONING

Every generated video must point to the exact strategy version used at planning time.

A later strategy update does not retroactively rewrite old production decisions.

# 173. CONTENT PILLAR BALANCING

Maintain rolling representation:

```text
pillar_share = videos_in_pillar / total_recent_videos
```

If a pillar exceeds its maximum or falls below minimum, apply a ranking adjustment.

```text
adjusted_score = topic_score + balance_bonus - saturation_penalty
```

# 174. FORMAT MIX OPTIMIZATION

Track:

```text
short
long
series
one-off
```

Optimize mix only with sufficient sample size. Never draw strategy conclusions from one video.

# 175. MINIMUM SAMPLE SIZE RULE

A learning engine should not make strong recommendations until configured minimum observations are available.

Example:

```text
minimum comparable videos = 5
minimum analytics snapshots = 3
```

These thresholds are configuration, not hard-coded facts.

# 176. STATISTICAL CAUTION

The system should distinguish:

```text
correlation
causal evidence
insufficient evidence
```

A recommendation should never claim causation solely because two metrics moved together.

# 177. TITLE/THUMBNAIL EXPERIMENT DATA MODEL

```text
experiment
 ├── control_variant
 ├── variants[]
 ├── metric
 ├── start
 ├── end
 ├── sample_threshold
 ├── results
 └── decision
```

# 178. EXPERIMENT SAFETY

Do not modify live metadata more frequently than the platform/workflow policy allows.

Every experiment must have a restore/control state.

# 179. ANALYTICS DATA QUALITY

Analytics records are tagged:

```text
REAL
ESTIMATED
SIMULATED
MISSING
```

Only `REAL` data is eligible for production learning by default.

# 180. DATA QUALITY FLAGS

```text
LOW_SAMPLE
STALE
INCOMPLETE
SIMULATED
CONFLICTING
```

These flags must be visible to the recommendation engine.

# 181. REPORTING

Generate:

```text
Daily Operations Report
Weekly Content Report
Monthly Strategy Report
Provider Cost Report
Failure Report
Experiment Report
```

# 182. DAILY REPORT FORMAT

```text
Videos created
Videos published
Views
Watch time
CTR
Retention highlights
Subscriber change
Top topics
Weak topics
Costs
Failures
Pending actions
```

# 183. WEEKLY STRATEGY REPORT

```text
Top performing pillars
Top performing hooks
Best publishing windows
Topic clusters
Audience requests
Cost efficiency
Content gaps
Learning recommendations
```

# 184. AUTOMATED CHANNEL STARTUP PROCEDURE

On first activation:

```text
1. Validate OAuth.
2. Fetch channel identity.
3. Run API readiness.
4. Create strategy draft.
5. Discover niche.
6. Generate channel branding package.
7. Generate first 10 topic candidates.
8. Generate first 3 production drafts.
9. Render drafts.
10. Review.
11. Schedule according to policy.
12. Enable recurring scheduler.
```

Do not jump directly from OAuth to mass publishing.

# 185. FIRST 24-HOUR BOOTSTRAP PLAN

```text
Hour 0  → connection/readiness
Hour 1  → niche/strategy
Hour 2  → topic research
Hour 3  → first script
Hour 4  → first production
Hour 5  → review/repair
Hour 6  → second production
Hour 7  → analytics/readiness
Hour 8+ → steady state
```

These are workflow phases, not guaranteed provider completion times.

# 186. STEADY-STATE OPERATING MODEL

At steady state:

```text
RESEARCH BACKLOG → enough topics for next 24–72 hours
PRODUCTION BACKLOG → enough drafts for target cadence
SCHEDULED BACKLOG → enough approved videos for near-term slots
ANALYTICS → continuously refreshed
LEARNING → weekly evidence loop
```

# 187. AUTONOMY LEVELS

Expose levels rather than one dangerous master switch.

```text
LEVEL 0: Observe
LEVEL 1: Research
LEVEL 2: Generate drafts
LEVEL 3: Render drafts
LEVEL 4: Upload private/unlisted according to policy
LEVEL 5: Schedule approved content
LEVEL 6: Fully configured automation
```

Promotion between levels requires readiness checks.

# 188. AUTOMATION KILL SWITCH

Global emergency switch:

```text
AUTOMATION_KILL_SWITCH=true
```

Behavior:
- stop new generation jobs;
- stop new publish jobs;
- allow reconciliation;
- allow currently safe cleanup;
- preserve existing drafts.

The kill switch must be checked before any publish side effect.

# 189. LICENSE AND ATTRIBUTION EXPORT

For each published video, generate an internal rights report:

```text
video
assets
licenses
attributions
source links
AI-generated media flags
operator confirmations
```

# 190. CONTENT PROVENANCE REPORT

A production should answer:

```text
Why was this topic selected?
Where did the facts come from?
Which model generated the script?
Which provider created the audio?
Where did each visual come from?
Which prompt versions were used?
Who approved it?
When was it uploaded?
What did analytics show?
```

# 191. AUDITABILITY PRINCIPLE

Every important output must have enough metadata to reproduce or explain the decision without relying on hidden model state.

# 192. NO HIDDEN SIDE EFFECTS

Functions named like:

```text
analyze()
score()
validate()
```

must not upload files, mutate remote accounts, send messages, or update unrelated tables.

Side effects belong in explicit service methods.

# 193. PURE AGENT CONTRACT

Agents should prefer:

```python
result = agent(input_model)
```

over:

```python
agent.read_database()
agent.call_youtube()
agent.modify_files()
agent.send_email()
```

The second pattern makes testing and safety significantly harder.

# 194. DEPENDENCY INJECTION

Services are injected:

```python
pipeline = PublishPipeline(
    youtube=youtube_service,
    storage=storage_service,
    audit=audit_service,
    repository=video_repository,
)
```

This allows mocks in tests.

# 195. MOCK PROVIDERS

Every external provider must have a deterministic mock for CI.

```text
MockLLM
MockTTS
MockVideo
MockYouTube
MockStorage
```

Mocks must mimic error conditions too.

# 196. CONTRACT TESTS

Provider adapters should pass the same contract test suite:

```text
valid request
invalid request
timeout
rate limit
provider error
malformed response
success response
```

# 197. SECURITY TESTS

Test for:
- secret leakage;
- path traversal;
- command injection;
- SSRF in URL fetchers;
- webhook spoofing;
- unauthorized publish;
- broken access control;
- malformed provider payloads.

# 198. URL FETCHER SAFETY

Research fetchers must:
- restrict protocols to HTTP/HTTPS;
- reject local file URLs;
- enforce response size limits;
- enforce timeout;
- limit redirects;
- validate content type;
- prevent access to internal network ranges where applicable.

# 199. WEB SCRAPING SAFETY

Use official APIs or permitted sources where possible. Respect source terms, robots directives where applicable, rate limits, and copyright constraints. Do not build the platform around bypassing technical access controls.

# 200. FINAL IMPLEMENTATION CONTRACT

The implementation is complete only when the following system can operate as one coherent machine:

```text
                     USER / OPERATOR
                            │
                            ▼
                     DASHBOARD / API
                            │
                            ▼
                     CHANNEL STRATEGY
                            │
                            ▼
                     TOPIC DISCOVERY
                            │
                            ▼
                        RESEARCH
                            │
                            ▼
                   CLAIM VERIFICATION
                            │
                            ▼
                         SCRIPT
                            │
                            ▼
                      VISUAL PLAN
                            │
                            ▼
                     ASSET PIPELINE
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
           VIDEO           AUDIO        CAPTIONS
             └──────────────┼──────────────┘
                            ▼
                          RENDER
                            │
                            ▼
                     QUALITY GATES
                            │
               ┌────────────┴─────────────┐
               ▼                          ▼
          HUMAN REVIEW             AUTO POLICY
               │                          │
               └────────────┬─────────────┘
                            ▼
                       PUBLISH QUEUE
                            │
                            ▼
                    YOUTUBE SCHEDULE
                            │
                            ▼
                         PUBLISHED
                            │
                            ▼
                        ANALYTICS
                            │
                            ▼
                         LEARNING
                            │
                            ▼
                     NEW STRATEGY INPUT
                            │
                            └──────────────→ NEXT VIDEO
```

The system must remain bounded by explicit permissions, budgets, quality gates, provenance, reproducible state, and observable workflows. Continuous automation is a scheduler property; it is never permission to remove validation, fabricate engagement, bypass security, or ignore remote-platform state.

# 201. AI ASSISTANT QUICK-START CARD

When any AI assistant opens this repository, execute these exact steps:

```text
STEP 1
Read brain.md.

STEP 2
Inspect the existing tree.

STEP 3
Identify whether the requested feature already exists.

STEP 4
Locate the authoritative contract/schema/state machine.

STEP 5
Modify the smallest possible set of modules.

STEP 6
Do not introduce a parallel architecture.

STEP 7
Run unit + targeted integration tests.

STEP 8
Check logs/error paths.

STEP 9
Check security/secrets.

STEP 10
Update brain.md only when architecture or operational rules materially change.

STEP 11
Update CHANGELOG.md.

STEP 12
Report files changed, tests run, known limitations, and next safe action.
```

# 202. DO NOT HALLUCINATE THE CODEBASE

When a symbol, endpoint, database table, provider method, environment variable, or file is not present, the AI assistant must first search the repository.

Never state “already implemented” without inspecting code.

Never invent an endpoint merely because a similar endpoint seems logical.

Never assume a repository’s latest README reflects every implementation detail; inspect source code and tests before modifying it.

# 203. REFERENCE IMPLEMENTATION MAPPING

Initial mapping from the studied repositories:

```text
AgentTube / youtube-automation-agent
    ↓
Node dashboard
Node publishing
Node analytics
Node strategy
Node scheduler patterns
Scene/provenance/review concepts

khaoss85/youtube-autopilot
    ↓
Python agent architecture
Pydantic contracts
Provider abstraction
Trend research patterns
Quality review patterns
Pipeline orchestration

soumyadityac/youtube-viewer
    ↓
EXCLUDED
```

# 204. REFACTORING RULE FOR IMPORTED CODE

Copied/reference code must be normalized into this project’s:

```text
naming conventions
state machine
logging
error taxonomy
contracts
security model
configuration system
```

Do not retain duplicated configuration formats without an adapter or migration plan.

# 205. MIGRATION ORDER FOR EXISTING REPOSITORY CODE

```text
1. inventory files
2. classify reusable modules
3. classify unsafe/out-of-scope modules
4. define internal contracts
5. migrate core schemas
6. migrate agents
7. migrate services
8. migrate orchestration
9. migrate UI
10. run integration tests
11. remove duplicated legacy paths
12. freeze architecture
```

# 206. SOURCE CODE INVENTORY REQUIREMENT

Before a large merge, maintain an inventory:

```text
path
purpose
source repo
license
status
replacement
owner
```

This prevents accidental license/provenance confusion during repository fusion.

# 207. LICENSE REVIEW

Before distributing combined code:
- inspect each source repository license;
- retain required notices;
- document copied files;
- do not assume all repositories have compatible licenses.

# 208. OBSERVABLE AUTONOMY

The operator dashboard must always answer:

```text
What is the system doing now?
Why is it doing it?
What is waiting?
What failed?
What will happen next?
How much will it cost?
What remote side effect occurred?
```

# 209. FINAL GOLDEN RULES

```text
1. OAuth, never Gmail passwords.
2. Official APIs/services for legitimate platform interaction.
3. No fake engagement.
4. No blind content copying.
5. Provenance for third-party media.
6. Evidence for factual claims.
7. State machine before side effect.
8. Idempotency before retries.
9. Reconciliation after uncertain remote operations.
10. Bounded concurrency.
11. Bounded spending.
12. Observable automation.
13. Versioned strategy and prompts.
14. Real analytics only for learning by default.
15. Human review remains available at every autonomy level.
16. Never let an AI assistant invent architecture.
17. Read the code before changing the code.
18. Update this document when the architecture materially changes.
```

# 210. PROJECT HANDOFF STATUS

This `brain.md` is intended to be the durable handoff artifact between the project owner and future AI engineering assistants.

The next coding session should begin with repository inspection and an implementation-delta report, not with wholesale file generation.

The expected first implementation target is a safe local/staging vertical slice:

```text
OAuth
 → channel discovery
 → strategy
 → one topic
 → one research packet
 → one script
 → one rendered draft
 → review record
 → dry-run publish
 → mocked analytics
```

Once that vertical slice passes end-to-end tests, expand throughput and autonomous scheduling incrementally.
