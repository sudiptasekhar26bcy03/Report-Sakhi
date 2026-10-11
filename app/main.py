import os
import json
from pathlib import Path
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, Form, Request
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse, JSONResponse
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from fastapi.templating import Jinja2Templates
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Tuple

from app.config import settings
from app.agents.pipeline import ReportSakhiPipeline

# Paths setup
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="ReportSakhi: AI Health Friend explaining medical lab reports to patients in their own language by voice."
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Pipeline instance
pipeline = ReportSakhiPipeline(
    gemini_api_key=settings.gemini_api_key,
    voice_provider=settings.voice_provider
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Serves the mobile-first Home screen.
    Includes Language Picker (Malayalam, Hindi, Tamil, English),
    Large Scan Report button, and Simple Mode toggle.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
            "languages": settings.supported_languages,
            "voice_provider": settings.voice_provider
        }
    )

@app.post("/api/scan")
async def scan_report(
    files: List[UploadFile] = File(default=[]),
    file: Optional[UploadFile] = File(None),
    language: str = Form("en"),
    simple_mode: bool = Form(False),
    previous_report: Optional[str] = Form(None),
    demo_type: Optional[str] = Form(None)
):
    """
    Executes the 4-agent pipeline on submitted report PDF(s) or photo(s),
    optionally computing longitudinal trends if previous_report is passed.
    """
    try:
        documents: List[Tuple[bytes, str]] = []

        all_uploads: List[UploadFile] = list(files) if files else []
        if file and file not in all_uploads:
            all_uploads.insert(0, file)

        for up in all_uploads:
            content = await up.read()
            if content and len(content) > 0:
                ct = up.content_type or ""
                fn = up.filename or ""
                if fn.lower().endswith(".pdf") or ct.lower() == "application/pdf":
                    ct = "application/pdf"
                documents.append((content, ct))

        if not documents:
            if demo_type == "followup":
                documents.append((b"DEMO_FOLLOWUP_PAYLOAD", "image/jpeg"))
            elif demo_type == "pdf":
                documents.append((b"DEMO_PDF_REPORT_PAYLOAD", "application/pdf"))
            else:
                documents.append((b"DEMO_REPORT_PAYLOAD", "image/jpeg"))

        parsed_prev = None
        if previous_report:
            try:
                parsed_prev = json.loads(previous_report)
            except Exception:
                pass

        result = await pipeline.run(
            document_or_documents=documents,
            language=language,
            previous_report=parsed_prev
        )
        result["simple_mode"] = simple_mode
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e), "message": "Failed to process report."}
        )

from app.mcp.server import find_nearby_help

@app.post("/api/ask")
async def ask_question(
    question: str = Form(...),
    language: str = Form("en"),
    context: Optional[str] = Form(None)
):
    """
    Text follow-up question endpoint.
    Answers patient queries via ExplainerAgent and synthesizes TTS audio.
    """
    try:
        answer = await pipeline.explainer.answer_question(
            question=question,
            language=language,
            report_context=context
        )
        tts_res = await pipeline.voice.text_to_speech(answer, language_code=language)
        return JSONResponse(content={
            "success": True,
            "question": question,
            "answer": answer,
            "language": language,
            "audio_base64": tts_res.get("audio_base64"),
            "audio_format": tts_res.get("audio_format"),
            "provider": tts_res.get("provider"),
            "status": tts_res.get("status")
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e), "message": "Failed to answer question."}
        )

@app.post("/api/voice/ask")
async def voice_ask_question(
    file: Optional[UploadFile] = File(None),
    question: Optional[str] = Form(None),
    language: str = Form("en"),
    context: Optional[str] = Form(None)
):
    """
    Voice Q&A loop:
    1. Transcribes incoming patient audio via Voice Agent.
    2. Answers question via Explainer Agent (Class 5, non-diagnostic).
    3. Synthesizes voice audio response via Voice Agent TTS.
    """
    try:
        transcribed_text = (question or "").strip()

        # Step 1: Transcribe audio if provided
        if file:
            audio_bytes = await file.read()
            if len(audio_bytes) > 64:
                stt_res = await pipeline.voice.speech_to_text(
                    audio_bytes,
                    language_code=language,
                    audio_format=file.content_type
                )
                audio_transcript = stt_res.get("transcript", "").strip()
                if audio_transcript:
                    transcribed_text = audio_transcript

        if not transcribed_text:
            not_heard_msgs = {
                "hi": "माफ़ कीजिए, आपकी आवाज़ साफ़ सुनाई नहीं दी। कृपया दोबारा बोलें।",
                "en": "I could not hear your question clearly. Please tap the mic and try asking again.",
                "ml": "ക്ഷമിക്കണം, നിങ്ങളുടെ ചോദ്യം വ്യക്തമായി കേൾക്കാനായില്ല. ദയവായി വീണ്ടും ചോദിക്കാമോ?",
                "ta": "மன்னிக்கவும், உங்கள் கேள்வி தெளிவாகக் கேட்கவில்லை. தயவுசெய்து மீண்டும் பேசவும்.",
                "te": "క్షమించండి, మీ ప్రశ్న స్పష్టంగా వినబడలేదు. దయచేసి మళ్లీ మాట్లాడండి."
            }
            fallback_msg = not_heard_msgs.get(language, not_heard_msgs["en"])
            tts_fallback = await pipeline.voice.text_to_speech(fallback_msg, language_code=language)
            return JSONResponse(content={
                "success": False,
                "question": "",
                "answer": fallback_msg,
                "language": language,
                "audio_base64": tts_fallback.get("audio_base64"),
                "audio_format": tts_fallback.get("audio_format"),
                "provider": tts_fallback.get("provider")
            })

        # Step 2: Answer via Explainer Agent
        answer = await pipeline.explainer.answer_question(
            question=transcribed_text,
            language=language,
            report_context=context
        )

        # Step 3: Synthesize voice response
        tts_res = await pipeline.voice.text_to_speech(answer, language_code=language)

        return JSONResponse(content={
            "success": True,
            "question": transcribed_text,
            "answer": answer,
            "language": language,
            "audio_base64": tts_res.get("audio_base64"),
            "audio_format": tts_res.get("audio_format"),
            "provider": tts_res.get("provider"),
            "status": tts_res.get("status")
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e), "message": "Failed to process voice question."}
        )

@app.get("/api/help/nearby")
@app.post("/api/help/nearby")
async def get_nearby_help(
    urgency: str = "red",
    query_type: str = "hospital",
    conditions: str = "",
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    language: str = "en"
):
    """
    Executes the MCP 'find_nearby_help' tool.
    Returns dynamic turn-by-turn map links, emergency facilities, and helplines.
    """
    help_data = find_nearby_help(
        query_type=query_type,
        urgency=urgency,
        conditions=conditions,
        latitude=latitude,
        longitude=longitude,
        language=language
    )
    return JSONResponse(content=help_data)

@app.post("/api/voice/tts")
async def voice_tts(
    text: str = Form(...),
    language: str = Form("en")
):
    """
    Text-to-Speech synthesis endpoint with Bhashini primary and cascade failover.
    """
    try:
        tts_res = await pipeline.voice.text_to_speech(text, language_code=language)
        return JSONResponse(content={"success": True, **tts_res})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e), "provider": "browser", "client_speech_text": text}
        )

@app.post("/api/voice/stt")
async def voice_stt(
    file: UploadFile = File(...),
    language: str = Form("en")
):
    """
    Speech-to-Text transcription endpoint.
    """
    try:
        audio_bytes = await file.read()
        stt_res = await pipeline.voice.speech_to_text(audio_bytes, language_code=language)
        return JSONResponse(content={"success": True, **stt_res})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e), "transcript": "", "provider": "browser"}
        )

@app.get("/api/voice/status")
async def voice_status():
    """
    Returns configured Voice Provider and supported failover options.
    """
    return JSONResponse(content=settings.get_voice_info())

@app.get("/api/ranges")
async def get_ranges():
    """
    Returns reference ranges rule set.
    """
    return JSONResponse(content=pipeline.checker.ranges_data)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
        "voice_provider": settings.voice_provider
    }
