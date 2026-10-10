"""
Voice Agent: Multilingual Text-to-Speech (TTS) and Speech-to-Text (STT).
Supports one-line provider switching across:
- Bhashini (Primary - National Language Translation Mission, Govt of India)
- Sarvam AI (Generative Indian Language Voice)
- Google Cloud Speech / Text-to-Speech
- Azure Cognitive Services Speech
- Browser Web Speech API (Zero-fail client fallback)

Includes automatic cascade failover: if the primary provider fails, it seamlessly
falls back to available secondary providers down to the client browser speech.
"""

import base64
import html
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import httpx

# Ensure project root is in sys.path so 'app' package resolves whether executed directly or imported
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from app.config import settings
except ImportError:
    try:
        from config import settings  # type: ignore # pyright: ignore[reportMissingImports]  # fallback if loaded from inside app folder
    except ImportError:
        # Fallback graceful dummy settings if config cannot be loaded
        class DummySettings:
            voice_provider = "bhashini"
            bhashini_user_id = ""
            bhashini_api_key = ""
            bhashini_pipeline_id = ""
            bhashini_audio_format = "mp3"
            bhashini_sampling_rate = 22050
            sarvam_api_key = ""
            google_speech_api_key = ""
            azure_speech_key = ""
            azure_speech_region = "centralindia"
            supported_languages = {}
        settings = DummySettings()

logger = logging.getLogger(__name__)

# Language mapping matrix for speech APIs (Hindi, English, Malayalam, Tamil, Telugu)
LANGUAGE_MAP = {
    "hi": {
        "bhashini": "hi",
        "sarvam": "hi-IN",
        "google": "hi-IN",
        "google_voice_name": "hi-IN-Standard-A",
        "azure_voice": "hi-IN-SwaraNeural",
        "azure_lang": "hi-IN"
    },
    "en": {
        "bhashini": "en",
        "sarvam": "en-IN",
        "google": "en-IN",
        "google_voice_name": "en-IN-Standard-A",
        "azure_voice": "en-IN-NeerjaNeural",
        "azure_lang": "en-IN"
    },
    "ml": {
        "bhashini": "ml",
        "sarvam": "ml-IN",
        "google": "ml-IN",
        "google_voice_name": "ml-IN-Standard-A",
        "azure_voice": "ml-IN-SobhanaNeural",
        "azure_lang": "ml-IN"
    },
    "ta": {
        "bhashini": "ta",
        "sarvam": "ta-IN",
        "google": "ta-IN",
        "google_voice_name": "ta-IN-Standard-A",
        "azure_voice": "ta-IN-PallaviNeural",
        "azure_lang": "ta-IN"
    },
    "te": {
        "bhashini": "te",
        "sarvam": "te-IN",
        "google": "te-IN",
        "google_voice_name": "te-IN-Standard-A",
        "azure_voice": "te-IN-ShrutiNeural",
        "azure_lang": "te-IN"
    }
}


class VoiceAgent:
    def __init__(self, provider: Optional[str] = None):
        cfg_provider = getattr(settings, "voice_provider", "google")
        self.provider = (provider or cfg_provider or "google").lower().strip()
        
        # Credentials & audio quality settings from config / environment
        self.bhashini_user_id = getattr(settings, "bhashini_user_id", "") or os.getenv("BHASHINI_USER_ID", "")
        self.bhashini_api_key = getattr(settings, "bhashini_api_key", "") or os.getenv("BHASHINI_API_KEY", "")
        self.bhashini_pipeline_id = getattr(settings, "bhashini_pipeline_id", "") or os.getenv("BHASHINI_PIPELINE_ID", "")
        self.bhashini_audio_format = getattr(settings, "bhashini_audio_format", "mp3") or os.getenv("BHASHINI_AUDIO_FORMAT", "mp3")
        try:
            raw_rate = getattr(settings, "bhashini_sampling_rate", 22050) or os.getenv("BHASHINI_SAMPLING_RATE", "22050")
            self.bhashini_sampling_rate = int(raw_rate)
        except (ValueError, TypeError):
            self.bhashini_sampling_rate = 22050

        self.sarvam_key = getattr(settings, "sarvam_api_key", "") or os.getenv("SARVAM_API_KEY", "")
        self.google_key = getattr(settings, "google_speech_api_key", "") or os.getenv("GOOGLE_SPEECH_API_KEY", "") or getattr(settings, "gemini_api_key", "") or os.getenv("GEMINI_API_KEY", "")
        self.azure_key = getattr(settings, "azure_speech_key", "") or os.getenv("AZURE_SPEECH_KEY", "")
        self.azure_region = getattr(settings, "azure_speech_region", "") or os.getenv("AZURE_SPEECH_REGION", "centralindia")

    @staticmethod
    def detect_audio_format(audio_bytes: bytes) -> str:
        """Detects audio container/format from binary magic bytes."""
        if not audio_bytes or len(audio_bytes) < 4:
            return "wav"
        # WebM / Matroska EBML header: 1A 45 DF A3
        if audio_bytes.startswith(b"\x1a\x45\xdf\xa3"):
            return "webm"
        # Ogg Vorbis/Opus container: OggS
        if audio_bytes.startswith(b"OggS"):
            return "ogg"
        # RIFF WAVE
        if audio_bytes.startswith(b"RIFF") and len(audio_bytes) >= 12 and audio_bytes[8:12] == b"WAVE":
            return "wav"
        # FLAC: fLaC
        if audio_bytes.startswith(b"fLaC"):
            return "flac"
        # MP3: ID3 or sync frame
        if audio_bytes.startswith(b"ID3") or (len(audio_bytes) > 2 and audio_bytes[0] == 0xFF and (audio_bytes[1] & 0xE0) == 0xE0):
            return "mp3"
        # MP4 / M4A / AAC: ftyp
        if len(audio_bytes) >= 12 and audio_bytes[4:8] == b"ftyp":
            return "mp4"
        return "wav"

    def _get_failover_chain(self) -> List[str]:
        """Constructs priority provider order starting with the selected VOICE_PROVIDER."""
        if self.provider == "browser":
            return ["browser"]

        all_remote = ["google", "bhashini", "sarvam", "azure"]
        primary = self.provider if self.provider in all_remote else "google"

        # Primary first, then remaining remote providers, ending with browser
        chain = [primary] + [p for p in all_remote if p != primary] + ["browser"]
        return chain

    # -------------------------------------------------------------------------
    # Text-to-Speech (TTS)
    # -------------------------------------------------------------------------

    async def text_to_speech(
        self,
        text: str,
        language_code: str = "en",
        audio_format: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes speech for the patient.
        Attempts the configured VOICE_PROVIDER with automatic cascade failover.
        Supports high-fidelity Bhashini audio formats (MP3, WAV, FLAC, OGG, AAC) with 22.05kHz/44.1kHz sampling.
        Returns:
        {
            "provider": str,
            "language_code": str,
            "audio_base64": Optional[str],
            "audio_format": Optional[str],
            "client_speech_text": str,
            "status": "ready" | "client_synthesis"
        }
        """
        lang = language_code if language_code in LANGUAGE_MAP else "en"
        failover_chain = self._get_failover_chain()

        for provider in failover_chain:
            try:
                if provider == "bhashini" and self.bhashini_api_key:
                    result = await self._synthesize_bhashini(text, lang, audio_format=audio_format)
                    if result:
                        return result

                elif provider == "sarvam" and self.sarvam_key:
                    result = await self._synthesize_sarvam(text, lang)
                    if result:
                        return result

                elif provider == "google" and self.google_key:
                    result = await self._synthesize_google(text, lang)
                    if result:
                        return result

                elif provider == "azure" and self.azure_key:
                    result = await self._synthesize_azure(text, lang)
                    if result:
                        return result

                elif provider == "browser":
                    # Guaranteed client-side browser Web Speech API
                    return {
                        "provider": "browser",
                        "language_code": lang,
                        "audio_base64": None,
                        "audio_format": None,
                        "client_speech_text": text,
                        "status": "client_synthesis"
                    }

            except Exception as e:
                logger.warning(f"Voice provider '{provider}' TTS failed: {e}. Cascading to next provider...")

        # Final safety fallback
        return {
            "provider": "browser",
            "language_code": lang,
            "audio_base64": None,
            "audio_format": None,
            "client_speech_text": text,
            "status": "client_synthesis"
        }

    async def _synthesize_bhashini(
        self,
        text: str,
        lang: str,
        audio_format: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Synthesizes high-fidelity speech using Government of India Bhashini ULCA API.
        Supports crystal-clear compressed MP3, lossless WAV, FLAC, and OGG formats with configurable sampling rate.
        """
        if not self.bhashini_user_id or not self.bhashini_api_key:
            return None

        url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
        headers = {
            "userID": self.bhashini_user_id,
            "ulcaApiKey": self.bhashini_api_key,
            "Content-Type": "application/json"
        }
        if self.bhashini_pipeline_id:
            headers["pipelineId"] = self.bhashini_pipeline_id

        target_lang = LANGUAGE_MAP.get(lang, {}).get("bhashini", "en")
        target_format = (audio_format or self.bhashini_audio_format or "mp3").lower().strip()
        if target_format not in ["mp3", "wav", "flac", "ogg", "aac"]:
            target_format = "mp3"

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": target_lang},
                        "gender": "female",
                        "samplingRate": self.bhashini_sampling_rate,
                        "audioFormat": target_format
                    }
                }
            ],
            "inputData": {
                "input": [{"source": text}]
            }
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                pipeline_resp = data.get("pipelineResponse", [])
                for task_res in pipeline_resp:
                    audio_list = task_res.get("audio", [])
                    if audio_list:
                        audio_content = audio_list[0].get("audioContent") or audio_list[0].get("audioUri")
                        if audio_content:
                            return {
                                "provider": "bhashini",
                                "language_code": lang,
                                "audio_base64": audio_content,
                                "audio_format": f"audio/{target_format}",
                                "sampling_rate": self.bhashini_sampling_rate,
                                "client_speech_text": text,
                                "status": "ready"
                            }
        return None

    async def _synthesize_sarvam(self, text: str, lang: str) -> Optional[Dict[str, Any]]:
        """Synthesizes speech using Sarvam AI Bulbul TTS API."""
        if not self.sarvam_key:
            return None

        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "api-subscription-key": self.sarvam_key,
            "Content-Type": "application/json"
        }
        target_lang = LANGUAGE_MAP.get(lang, {}).get("sarvam", "en-IN")

        payload = {
            "inputs": [text],
            "target_language_code": target_lang,
            "speaker": "meera",
            "model": "bulbul:v1"
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                audios = data.get("audios", [])
                if audios:
                    return {
                        "provider": "sarvam",
                        "language_code": lang,
                        "audio_base64": audios[0],
                        "audio_format": "audio/wav",
                        "client_speech_text": text,
                        "status": "ready"
                    }
        return None

    async def _synthesize_google(self, text: str, lang: str) -> Optional[Dict[str, Any]]:
        """Synthesizes speech using Google Cloud Text-to-Speech API or Gemini TTS model."""
        if not self.google_key:
            return None

        # 1. Try Google Cloud Text-to-Speech REST API
        try:
            url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.google_key}"
            target_lang = LANGUAGE_MAP.get(lang, {}).get("google", "en-IN")
            voice_name = LANGUAGE_MAP.get(lang, {}).get("google_voice_name", f"{target_lang}-Standard-A")

            payload = {
                "input": {"text": text},
                "voice": {"languageCode": target_lang, "name": voice_name, "ssmlGender": "FEMALE"},
                "audioConfig": {"audioEncoding": "MP3"}
            }

            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    audio_content = data.get("audioContent")
                    if audio_content:
                        return {
                            "provider": "google",
                            "language_code": lang,
                            "audio_base64": audio_content,
                            "audio_format": "audio/mp3",
                            "client_speech_text": text,
                            "status": "ready"
                        }
                else:
                    logger.debug(f"Google Cloud TTS REST returned status {resp.status_code}. Falling back to Google GenAI TTS...")
        except Exception as e:
            logger.debug(f"Google Cloud TTS REST attempt failed: {e}. Falling back to Google GenAI TTS...")

        # 2. Try Google GenAI TTS (gemini-3.8-flash-tts)
        try:
            import asyncio
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.google_key)
            lang_names = {
                "hi": "Hindi", "en": "English", "ml": "Malayalam", "ta": "Tamil", "te": "Telugu"
            }
            lang_label = lang_names.get(lang, "English")
            prompt = f"Read this text clearly and warmly aloud in {lang_label}: {text}"

            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-3.8-flash-tts",
                contents=prompt,
                config=types.GenerateContentConfig(response_modalities=["AUDIO"])
            )
            if response and response.candidates and response.candidates[0].content:
                parts = response.candidates[0].content.parts or []
                for part in parts:
                    if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
                        b64_audio = base64.b64encode(part.inline_data.data).decode("utf-8")
                        mime = part.inline_data.mime_type or "audio/wav"
                        return {
                            "provider": "google",
                            "language_code": lang,
                            "audio_base64": b64_audio,
                            "audio_format": mime,
                            "client_speech_text": text,
                            "status": "ready"
                        }
        except Exception as e:
            logger.warning(f"Google GenAI TTS error: {e}")

        return None

    async def _synthesize_azure(self, text: str, lang: str) -> Optional[Dict[str, Any]]:
        """Synthesizes speech using Azure Cognitive Services Speech REST API."""
        if not self.azure_key:
            return None

        url = f"https://{self.azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
        azure_voice = LANGUAGE_MAP.get(lang, {}).get("azure_voice", "en-IN-NeerjaNeural")
        azure_lang = LANGUAGE_MAP.get(lang, {}).get("azure_lang", "en-IN")

        escaped_text = html.escape(text)
        ssml = (
            f"<speak version='1.0' xml:lang='{azure_lang}'>"
            f"<voice name='{azure_voice}'>{escaped_text}</voice>"
            f"</speak>"
        )

        headers = {
            "Ocp-Apim-Subscription-Key": self.azure_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "ReportSakhi"
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, content=ssml.encode("utf-8"))
            if resp.status_code == 200 and resp.content:
                audio_b64 = base64.b64encode(resp.content).decode("utf-8")
                return {
                    "provider": "azure",
                    "language_code": lang,
                    "audio_base64": audio_b64,
                    "audio_format": "audio/mp3",
                    "client_speech_text": text,
                    "status": "ready"
                }
        return None

    # -------------------------------------------------------------------------
    # Speech-to-Text (STT / ASR)
    # -------------------------------------------------------------------------

    async def speech_to_text(
        self,
        audio_bytes: bytes,
        language_code: str = "en",
        audio_format: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribes patient spoken voice question into text.
        Executes cascade failover starting with the configured VOICE_PROVIDER.
        Accepts WebM, OGG, WAV, MP3, FLAC with automatic format auto-detection.
        Returns:
        {
            "provider": str,
            "transcript": str,
            "confidence": float,
            "status": "success" | "client_recognition"
        }
        """
        if not audio_bytes or len(audio_bytes) < 32:
            return {
                "provider": "browser",
                "transcript": "",
                "confidence": 0.0,
                "status": "client_recognition"
            }

        lang = language_code if language_code in LANGUAGE_MAP else "en"
        failover_chain = self._get_failover_chain()

        for provider in failover_chain:
            try:
                if provider == "bhashini" and self.bhashini_api_key:
                    res = await self._transcribe_bhashini(audio_bytes, lang, audio_format=audio_format)
                    if res:
                        return res

                elif provider == "sarvam" and self.sarvam_key:
                    res = await self._transcribe_sarvam(audio_bytes, lang)
                    if res:
                        return res

                elif provider == "google" and self.google_key:
                    res = await self._transcribe_google(audio_bytes, lang)
                    if res:
                        return res

                elif provider == "azure" and self.azure_key:
                    res = await self._transcribe_azure(audio_bytes, lang)
                    if res:
                        return res

                elif provider == "browser":
                    return {
                        "provider": "browser",
                        "transcript": "",
                        "confidence": 1.0,
                        "status": "client_recognition"
                    }

            except Exception as e:
                logger.warning(f"Voice provider '{provider}' STT failed: {e}. Cascading to next provider...")

        # Final safety fallback to client-side browser speech recognition
        return {
            "provider": "browser",
            "transcript": "",
            "confidence": 1.0,
            "status": "client_recognition"
        }

    async def _transcribe_bhashini(
        self,
        audio_bytes: bytes,
        lang: str,
        audio_format: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Transcribes speech using Bhashini ULCA ASR inference API.
        Dynamically detects and passes audio container format (webm, ogg, wav, mp3, flac).
        """
        if not self.bhashini_user_id or not self.bhashini_api_key:
            return None

        url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
        headers = {
            "userID": self.bhashini_user_id,
            "ulcaApiKey": self.bhashini_api_key,
            "Content-Type": "application/json"
        }
        if self.bhashini_pipeline_id:
            headers["pipelineId"] = self.bhashini_pipeline_id

        target_lang = LANGUAGE_MAP.get(lang, {}).get("bhashini", "en")
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

        detected = (audio_format or self.detect_audio_format(audio_bytes)).lower().strip()
        if "webm" in detected:
            asr_format = "webm"
        elif "ogg" in detected:
            asr_format = "ogg"
        elif "mp3" in detected or "mpeg" in detected:
            asr_format = "mp3"
        elif "flac" in detected:
            asr_format = "flac"
        elif "mp4" in detected or "m4a" in detected or "aac" in detected:
            asr_format = "mp4"
        else:
            asr_format = "wav"

        asr_config: Dict[str, Any] = {
            "language": {"sourceLanguage": target_lang},
            "audioFormat": asr_format
        }
        if asr_format in ["wav", "mp3"]:
            asr_config["samplingRate"] = self.bhashini_sampling_rate

        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": asr_config
                }
            ],
            "inputData": {
                "audio": [{"audioContent": b64_audio}]
            }
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                pipeline_resp = data.get("pipelineResponse", [])
                for task_res in pipeline_resp:
                    output = task_res.get("output", [])
                    if output:
                        transcript = (
                            output[0].get("source")
                            or output[0].get("transcript")
                            or output[0].get("target")
                            or output[0].get("text")
                            or ""
                        ).strip()
                        if transcript:
                            return {
                                "provider": "bhashini",
                                "transcript": transcript,
                                "confidence": 0.95,
                                "status": "success"
                            }
        return None

    async def _transcribe_sarvam(self, audio_bytes: bytes, lang: str) -> Optional[Dict[str, Any]]:
        """Transcribes speech using Sarvam AI Saaras STT API."""
        if not self.sarvam_key:
            return None

        url = "https://api.sarvam.ai/speech-to-text"
        headers = {"api-subscription-key": self.sarvam_key}
        target_lang = LANGUAGE_MAP.get(lang, {}).get("sarvam", "en-IN")
        detected = (self.detect_audio_format(audio_bytes) or "wav").lower().strip()
        files = {"file": (f"audio.{detected}", audio_bytes, f"audio/{detected}")}
        data = {"model": "saaras:v1", "language_code": target_lang}

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, files=files, data=data)
            if resp.status_code == 200:
                transcript = resp.json().get("transcript", "").strip()
                if transcript:
                    return {
                        "provider": "sarvam",
                        "transcript": transcript,
                        "confidence": 0.95,
                        "status": "success"
                    }
        return None

    async def _transcribe_google(self, audio_bytes: bytes, lang: str) -> Optional[Dict[str, Any]]:
        """Transcribes speech using Google Cloud Speech-to-Text REST API."""
        if not self.google_key:
            return None

        url = f"https://speech.googleapis.com/v1/speech:recognize?key={self.google_key}"
        target_lang = LANGUAGE_MAP.get(lang, {}).get("google", "en-IN")
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

        detected = self.detect_audio_format(audio_bytes).lower()
        encoding_map = {
            "webm": "WEBM_OPUS",
            "ogg": "OGG_OPUS",
            "mp3": "MP3",
            "flac": "FLAC",
            "wav": "LINEAR16"
        }
        encoding = encoding_map.get(detected, "ENCODING_UNSPECIFIED")

        config = {
            "languageCode": target_lang,
            "enableAutomaticPunctuation": True
        }
        if encoding != "ENCODING_UNSPECIFIED":
            config["encoding"] = encoding

        payload = {
            "config": config,
            "audio": {
                "content": b64_audio
            }
        }

        # 1. Try Google Cloud Speech REST API
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    if results:
                        alternatives = results[0].get("alternatives", [])
                        if alternatives:
                            transcript = alternatives[0].get("transcript", "").strip()
                            confidence = float(alternatives[0].get("confidence", 0.90))
                            if transcript:
                                return {
                                    "provider": "google",
                                    "transcript": transcript,
                                    "confidence": confidence,
                                    "status": "success"
                                }
        except Exception as e:
            logger.debug(f"Google Cloud Speech REST attempt failed: {e}. Falling back to Google GenAI STT...")

        # 2. Try Google GenAI Multimodal Audio STT (gemini-3.5-flash)
        try:
            import asyncio
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.google_key)
            detected_format = self.detect_audio_format(audio_bytes).lower()
            mime_map = {
                "wav": "audio/wav",
                "mp3": "audio/mp3",
                "ogg": "audio/ogg",
                "webm": "audio/webm",
                "flac": "audio/flac"
            }
            mime = mime_map.get(detected_format, "audio/wav")

            lang_names = {
                "hi": "Hindi", "en": "English", "ml": "Malayalam", "ta": "Tamil", "te": "Telugu"
            }
            lang_label = lang_names.get(lang, "English")

            stt_models = ["gemini-flash-latest", "gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-3.5-flash"]
            response = None
            for stt_model in stt_models:
                try:
                    response = await asyncio.to_thread(
                        client.models.generate_content,
                        model=stt_model,
                        contents=[
                            types.Part.from_bytes(data=audio_bytes, mime_type=mime),
                            f"Transcribe the patient's spoken words verbatim in {lang_label}. Return ONLY the transcribed text without commentary."
                        ]
                    )
                    if response and response.text:
                        break
                except Exception:
                    continue
            if response and response.text:
                transcript = response.text.strip()
                if transcript:
                    return {
                        "provider": "google",
                        "transcript": transcript,
                        "confidence": 0.95,
                        "status": "success"
                    }
        except Exception as e:
            logger.warning(f"Google GenAI STT error: {e}")

        return None

    async def _transcribe_azure(self, audio_bytes: bytes, lang: str) -> Optional[Dict[str, Any]]:
        """Transcribes speech using Azure Cognitive Services Speech REST API."""
        if not self.azure_key:
            return None

        azure_lang = LANGUAGE_MAP.get(lang, {}).get("azure_lang", "en-IN")
        url = f"https://{self.azure_region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language={azure_lang}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure_key,
            "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
            "Accept": "application/json"
        }

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, headers=headers, content=audio_bytes)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("RecognitionStatus") == "Success":
                    transcript = data.get("DisplayText", "").strip()
                    if transcript:
                        return {
                            "provider": "azure",
                            "transcript": transcript,
                            "confidence": 0.92,
                            "status": "success"
                        }
        return None


if __name__ == "__main__":
    # Smoke-test CLI execution: python app/agents/voice.py
    import asyncio
    print(f"ReportSakhi VoiceAgent Initialized successfully.")
    print(f"Supported languages ({len(LANGUAGE_MAP)}): {list(LANGUAGE_MAP.keys())}")
    agent = VoiceAgent()
    print(f"Active Voice Provider: {agent.provider}")
    print(f"Failover Chain: {agent._get_failover_chain()}")
    res = asyncio.run(agent.text_to_speech("ReportSakhi voice agent initialized.", language_code="en"))
    print(f"Text-to-Speech test status: {res.get('status')} (Provider: {res.get('provider')})")
