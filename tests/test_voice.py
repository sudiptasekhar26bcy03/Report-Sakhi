import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import httpx
from app.agents.voice import VoiceAgent
from app.main import app


class TestVoiceAgent(unittest.TestCase):
    def setUp(self):
        self.voice = VoiceAgent(provider="bhashini")
        self.voice.google_key = ""
        self.voice.bhashini_api_key = ""
        self.voice.sarvam_key = ""
        self.voice.azure_key = ""

    def test_default_provider_is_bhashini(self):
        self.assertEqual(self.voice.provider, "bhashini")

    def test_failover_chain_order(self):
        chain = self.voice._get_failover_chain()
        self.assertEqual(chain[0], "bhashini")
        self.assertIn("sarvam", chain)
        self.assertIn("google", chain)
        self.assertIn("azure", chain)
        self.assertEqual(chain[-1], "browser")

    def test_provider_switching(self):
        for prov in ["bhashini", "sarvam", "google", "azure", "browser"]:
            agent = VoiceAgent(provider=prov)
            self.assertEqual(agent.provider, prov)
            chain = agent._get_failover_chain()
            self.assertEqual(chain[0], prov)
            self.assertEqual(chain[-1], "browser")

    def test_tts_fallback_to_browser(self):
        async def run_test():
            res = await self.voice.text_to_speech("Your hemoglobin is normal.", language_code="en")
            self.assertEqual(res["provider"], "browser")
            self.assertEqual(res["status"], "client_synthesis")
            self.assertEqual(res["client_speech_text"], "Your hemoglobin is normal.")
            self.assertEqual(res["language_code"], "en")
        asyncio.run(run_test())

    def test_stt_fallback_to_browser(self):
        async def run_test():
            res = await self.voice.speech_to_text(b"RIFF....WAVE_BYTES_TESTING_DATA_12345", language_code="hi")
            self.assertEqual(res["provider"], "browser")
            self.assertEqual(res["status"], "client_recognition")
        asyncio.run(run_test())

    def test_mock_bhashini_tts_success(self):
        async def run_test():
            agent = VoiceAgent(provider="bhashini")
            agent.bhashini_user_id = "test_user"
            agent.bhashini_api_key = "test_key"

            mock_resp = AsyncMock()
            mock_resp.status_code = 200
            # resp.json() in httpx is a synchronous method
            mock_resp.json = lambda: {
                "pipelineResponse": [{
                    "audio": [{"audioContent": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="}]
                }]
            }

            with patch("httpx.AsyncClient.post", return_value=mock_resp):
                res = await agent.text_to_speech("ഹലോ", language_code="ml")
                self.assertEqual(res["provider"], "bhashini")
                self.assertEqual(res["status"], "ready")
                self.assertIsNotNone(res["audio_base64"])
        asyncio.run(run_test())

    def test_mock_bhashini_asr_success(self):
        async def run_test():
            agent = VoiceAgent(provider="bhashini")
            agent.bhashini_user_id = "test_user"
            agent.bhashini_api_key = "test_key"

            mock_resp = AsyncMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: {
                "pipelineResponse": [{
                    "output": [{"source": "സുഖമാണോ"}]
                }]
            }

            with patch("httpx.AsyncClient.post", return_value=mock_resp):
                res = await agent.speech_to_text(b"WAVE_BYTES_HEADER_12345678901234567890", language_code="ml")
                self.assertEqual(res["provider"], "bhashini")
                self.assertEqual(res["status"], "success")
                self.assertEqual(res["transcript"], "സുഖമാണോ")
        asyncio.run(run_test())

    def test_mock_sarvam_tts_failover_to_google(self):
        async def run_test():
            agent = VoiceAgent(provider="sarvam")
            agent.sarvam_key = "bad_sarvam_key"
            agent.google_key = "good_google_key"

            # Sarvam fails (500), Google succeeds (200)
            async def side_effect(url, **kwargs):
                resp = AsyncMock()
                if "sarvam" in str(url):
                    resp.status_code = 500
                    resp.json = lambda: {"error": "Internal Error"}
                elif "googleapis" in str(url):
                    resp.status_code = 200
                    resp.json = lambda: {"audioContent": "GOOGLE_AUDIO_B64"}
                return resp

            with patch("httpx.AsyncClient.post", side_effect=side_effect):
                res = await agent.text_to_speech("Test message", language_code="en")
                self.assertEqual(res["provider"], "google")
                self.assertEqual(res["status"], "ready")
                self.assertEqual(res["audio_base64"], "GOOGLE_AUDIO_B64")
        asyncio.run(run_test())

    def test_mock_stt_failover_to_browser_on_error(self):
        async def run_test():
            agent = VoiceAgent(provider="bhashini")
            agent.bhashini_user_id = "user"
            agent.bhashini_api_key = "key"

            # Bhashini raises network timeout
            with patch("httpx.AsyncClient.post", side_effect=httpx.ConnectTimeout("Network timed out")):
                res = await agent.speech_to_text(b"WAVE_BYTES_TESTING_DATA_123456789012345", language_code="hi")
                self.assertEqual(res["provider"], "browser")
                self.assertEqual(res["status"], "client_recognition")
        asyncio.run(run_test())

    def test_voice_api_endpoints(self):
        async def run_api():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                # Test status
                status_res = await client.get("/api/voice/status")
                self.assertEqual(status_res.status_code, 200)
                data = status_res.json()
                self.assertIn("active_provider", data)
                self.assertIn("bhashini", data["supported_providers"])

                # Test TTS endpoint
                tts_res = await client.post("/api/voice/tts", data={"text": "Hello patient", "language": "en"})
                self.assertEqual(tts_res.status_code, 200)
                tts_data = tts_res.json()
                self.assertTrue(tts_data["success"])
                self.assertEqual(tts_data["status"], "client_synthesis")

                # Test STT endpoint
                stt_res = await client.post(
                    "/api/voice/stt",
                    files={"file": ("test.wav", b"0" * 64, "audio/wav")},
                    data={"language": "ml"}
                )
                self.assertEqual(stt_res.status_code, 200)
                stt_data = stt_res.json()
                self.assertTrue(stt_data["success"])
    def test_bhashini_better_audio_formats_tts(self):
        """Verifies Bhashini requests high-fidelity audio (MP3, 22.05kHz) by default."""
        async def run_test():
            agent = VoiceAgent(provider="bhashini")
            agent.bhashini_user_id = "test_user"
            agent.bhashini_api_key = "test_key"
            agent.bhashini_audio_format = "mp3"
            agent.bhashini_sampling_rate = 22050

            captured_payload = {}
            mock_resp = AsyncMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: {
                "pipelineResponse": [{
                    "audio": [{"audioContent": "MP3_HIGH_FIDELITY_B64"}]
                }]
            }

            async def mock_post(url, headers=None, json=None):
                nonlocal captured_payload
                captured_payload = json
                return mock_resp

            with patch("httpx.AsyncClient.post", side_effect=mock_post):
                res = await agent.text_to_speech("നമസ്കാരം", language_code="ml")
                self.assertEqual(res["provider"], "bhashini")
                self.assertEqual(res["audio_format"], "audio/mp3")
                self.assertEqual(res["audio_base64"], "MP3_HIGH_FIDELITY_B64")
                
                # Check task payload
                tts_task = captured_payload["pipelineTasks"][0]
                self.assertEqual(tts_task["config"]["audioFormat"], "mp3")
                self.assertEqual(tts_task["config"]["samplingRate"], 22050)
                self.assertEqual(tts_task["config"]["language"]["sourceLanguage"], "ml")

                # Test explicit WAV request
                res_wav = await agent.text_to_speech("നമസ്കാരം", language_code="ml", audio_format="wav")
                self.assertEqual(res_wav["audio_format"], "audio/wav")
                self.assertEqual(captured_payload["pipelineTasks"][0]["config"]["audioFormat"], "wav")

        asyncio.run(run_test())

    def test_bhashini_multi_audio_format_detection_asr(self):
        """Verifies Bhashini ASR detects container formats (WebM, OGG, MP3, WAV) accurately."""
        async def run_test():
            agent = VoiceAgent(provider="bhashini")
            agent.bhashini_user_id = "test_user"
            agent.bhashini_api_key = "test_key"

            captured_payload = {}
            mock_resp = AsyncMock()
            mock_resp.status_code = 200
            mock_resp.json = lambda: {
                "pipelineResponse": [{
                    "output": [{"source": "తెలుగు ప్రశ్న"}]
                }]
            }

            async def mock_post(url, headers=None, json=None):
                nonlocal captured_payload
                captured_payload = json
                return mock_resp

            with patch("httpx.AsyncClient.post", side_effect=mock_post):
                # 1. WebM Opus from modern Chrome MediaRecorder
                webm_bytes = b"\x1a\x45\xdf\xa3" + b"TEST_WEBM_CONTAINER_AUDIO_BYTES_12345"
                res_webm = await agent.speech_to_text(webm_bytes, language_code="te")
                self.assertEqual(res_webm["provider"], "bhashini")
                self.assertEqual(captured_payload["pipelineTasks"][0]["config"]["audioFormat"], "webm")
                self.assertEqual(captured_payload["pipelineTasks"][0]["config"]["language"]["sourceLanguage"], "te")

                # 2. Ogg container
                ogg_bytes = b"OggS" + b"TEST_OGG_CONTAINER_AUDIO_BYTES_12345"
                await agent.speech_to_text(ogg_bytes, language_code="ta")
                self.assertEqual(captured_payload["pipelineTasks"][0]["config"]["audioFormat"], "ogg")

                # 3. MP3 ID3 container
                mp3_bytes = b"ID3" + b"TEST_MP3_AUDIO_BYTES_123456789012345"
                await agent.speech_to_text(mp3_bytes, language_code="hi")
                self.assertEqual(captured_payload["pipelineTasks"][0]["config"]["audioFormat"], "mp3")

        asyncio.run(run_test())

    def test_all_5_native_languages_mapped(self):
        """Verifies exactly 5 native languages (Hindi, English, Malayalam, Tamil, Telugu) are configured."""
        from app.agents.voice import LANGUAGE_MAP
        from app.config import settings

        required_langs = ["hi", "en", "ml", "ta", "te"]
        self.assertEqual(len(required_langs), 5)
        self.assertEqual(len(LANGUAGE_MAP), 5)
        self.assertEqual(len(settings.supported_languages), 5)
        for code in required_langs:
            self.assertIn(code, LANGUAGE_MAP, f"Language {code} missing in LANGUAGE_MAP")
            self.assertIn(code, settings.supported_languages, f"Language {code} missing in supported_languages")
            self.assertEqual(LANGUAGE_MAP[code]["bhashini"], code)


if __name__ == "__main__":
    unittest.main()

