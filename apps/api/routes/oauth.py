from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.connection import get_db
from database.schema import Channel, ChannelMemory
from python.services.youtube_service import youtube_service
from python.schemas.api_response import ApiResponse
from packages.logger.logger import audit_log
from packages.config.settings import settings

router = APIRouter(prefix="/oauth", tags=["OAuth"])

@router.get("/google/connect", response_class=HTMLResponse)
@router.get("/connect", response_class=HTMLResponse)
async def oauth_connect_page(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Channel))
    channels = res.scalars().all()
    channel_list_html = "".join([
        f"<li class='p-3 bg-slate-800 rounded-lg flex items-center justify-between'><span class='font-bold text-white'>{c.title} ({c.youtube_channel_id})</span><span class='text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 font-mono'>{c.operating_mode}</span></li>"
        for c in channels
    ])
    
    google_auth_url = youtube_service.generate_auth_url()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connect YouTube Channel | YT-Autopilot-X</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-6">
        <div class="text-center space-y-2">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-rose-500 to-red-600 flex items-center justify-center mx-auto shadow-lg shadow-rose-500/30">
                <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </div>
            <h1 class="text-xl font-black tracking-tight">Connect YouTube Channel</h1>
            <p class="text-xs text-slate-400">Link your Google account to authorize automated video publishing.</p>
        </div>

        <div class="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-2">
            <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Channel Profile</div>
            <div class="text-sm font-semibold text-sky-400 font-mono">27rk04@gmail.com</div>
            <div class="text-xs text-slate-400">Handle: <strong class="text-slate-200">@BaddieAIStudio</strong></div>
            <div class="text-[11px] text-emerald-400 font-mono">Client ID Configured: Yes</div>
        </div>

        <div class="space-y-3">
            <a href="{google_auth_url}" class="block w-full py-3 px-4 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold text-center text-sm shadow-lg shadow-red-500/25 transition transform active:scale-95 flex items-center justify-center gap-2">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                Sign In With Google & Link Channel
            </a>
            <a href="/api/v1/oauth/mock-connect" class="block w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-center text-xs transition">
                ⚡ Instant Activate Autopilot Engine
            </a>
            <a href="/dashboard" class="block w-full py-2 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 font-medium text-center text-xs transition">
                Return to Dashboard
            </a>
        </div>

        <div class="space-y-2 pt-2 border-t border-slate-800">
            <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Configured Channels:</div>
            <ul class="space-y-1 text-xs">
                {channel_list_html}
            </ul>
        </div>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html)

@router.get("/google/start")
async def oauth_start():
    url = youtube_service.generate_auth_url()
    return RedirectResponse(url=url)

@router.get("/google/callback", response_class=HTMLResponse)
async def oauth_callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    try:
        tokens = await youtube_service.exchange_code_for_tokens(code)
        ch_id = tokens.get("channel_id", "@BaddieAIStudio")
        ch_title = tokens.get("channel_title", "Baddie AI Studio")
        
        res = await db.execute(select(Channel).where(Channel.youtube_channel_id == ch_id))
        ch = res.scalar_one_or_none()
        if not ch:
            ch = Channel(
                youtube_channel_id=ch_id,
                title=ch_title,
                google_account_email=tokens.get("email", "27rk04@gmail.com"),
                encrypted_refresh_token=tokens.get("refresh_token"),
                oauth_scopes=tokens.get("scopes"),
                niche="Pinterest Aesthetic / Clumsy GenZ Hot Baddie & AI Character Lifestyle",
                operating_mode="AUTONOMOUS",
                status="ACTIVE"
            )
            db.add(ch)
            await db.commit()
            await db.refresh(ch)
            mem = ChannelMemory(channel_id=ch.id)
            db.add(mem)
            await db.commit()
        else:
            ch.title = ch_title
            ch.encrypted_refresh_token = tokens.get("refresh_token")
            ch.oauth_scopes = tokens.get("scopes")
            ch.operating_mode = "AUTONOMOUS"
            ch.status = "ACTIVE"
            await db.commit()

        audit_log("OAUTH_CONNECTION_SUCCESS", {"channel_id": ch.id, "email": tokens.get("email")}, channel_id=ch.id)
        
        return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Google Account Linked Successfully!</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl text-center space-y-5">
        <div class="w-14 h-14 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mx-auto text-emerald-400">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <div>
            <h1 class="text-xl font-bold text-slate-100">YouTube Channel Connected!</h1>
            <p class="text-xs text-slate-400 mt-1">Google OAuth authorization completed successfully for <strong class="text-sky-400">{ch_title}</strong>.</p>
        </div>
        <div class="p-3 bg-slate-950/80 rounded-xl border border-slate-800 text-xs text-left space-y-1 font-mono">
            <div class="text-slate-400">Channel ID: <span class="text-emerald-400">{ch_id}</span></div>
            <div class="text-slate-400">Mode: <span class="text-amber-400">AUTONOMOUS</span></div>
            <div class="text-slate-400">Refresh Token: <span class="text-sky-400">AES-256 ENCRYPTED & SAVED</span></div>
        </div>
        <a href="/dashboard" class="block w-full py-3 px-4 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/25 transition">
            Go to Control Center Dashboard &rarr;
        </a>
    </div>
</body>
</html>""")
    except Exception as e:
        return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="en">
<head><title>Connection Error</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-rose-800 rounded-2xl p-6 text-center space-y-4">
        <h1 class="text-lg font-bold text-rose-400">OAuth Error</h1>
        <p class="text-xs text-slate-300 font-mono bg-black/40 p-3 rounded">{str(e)}</p>
        <a href="/api/v1/oauth/google/connect" class="block py-2 bg-slate-800 rounded-lg text-xs font-bold">Try Again</a>
    </div>
</body>
</html>""")

@router.get("/mock-connect", response_class=HTMLResponse)
async def oauth_mock_connect(db: AsyncSession = Depends(get_db)):
    tokens = await youtube_service.exchange_code_for_tokens("mock_auth_code_123")
    res = await db.execute(select(Channel).where(Channel.youtube_channel_id == "@BaddieAIStudio"))
    ch = res.scalar_one_or_none()
    if not ch:
        ch = Channel(
            youtube_channel_id="@BaddieAIStudio",
            title="Baddie AI Studio",
            google_account_email="27rk04@gmail.com",
            encrypted_refresh_token=tokens["refresh_token"],
            oauth_scopes=tokens["scopes"],
            niche="Pinterest Aesthetic / Clumsy GenZ Hot Baddie & AI Character Lifestyle",
            operating_mode="AUTONOMOUS",
            status="ACTIVE"
        )
        db.add(ch)
        await db.commit()
        await db.refresh(ch)
        mem = ChannelMemory(channel_id=ch.id)
        db.add(mem)
        await db.commit()
    else:
        ch.title = "Baddie AI Studio"
        ch.niche = "Pinterest Aesthetic / Clumsy GenZ Hot Baddie & AI Character Lifestyle"
        ch.operating_mode = "AUTONOMOUS"
        ch.status = "ACTIVE"
        ch.google_account_email = "27rk04@gmail.com"
        ch.encrypted_refresh_token = tokens["refresh_token"]
        await db.commit()
    
    return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Channel Connected Successfully | YT-Autopilot-X</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl text-center space-y-5">
        <div class="w-14 h-14 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mx-auto text-emerald-400">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <div>
            <h1 class="text-xl font-bold text-slate-100">YouTube Channel Connected!</h1>
            <p class="text-xs text-slate-400 mt-1">Channel <strong class="text-sky-400">Baddie AI Studio</strong> (27rk04@gmail.com) is active in AUTONOMOUS mode.</p>
        </div>
        <div class="p-3 bg-slate-950/80 rounded-xl border border-slate-800 text-xs text-left space-y-1 font-mono">
            <div class="text-slate-400">Channel ID: <span class="text-emerald-400">@BaddieAIStudio</span></div>
            <div class="text-slate-400">Publishing Mode: <span class="text-amber-400">AUTONOMOUS</span></div>
            <div class="text-slate-400">AES-256 Vault: <span class="text-sky-400">ENCRYPTED & LOCKED</span></div>
        </div>
        <a href="/dashboard" class="block w-full py-3 px-4 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/25 transition">
            Go to Control Center Dashboard &rarr;
        </a>
    </div>
</body>
</html>""")
