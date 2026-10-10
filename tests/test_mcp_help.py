import asyncio
import unittest
import httpx
from app.mcp.server import find_nearby_help, server
from app.agents.explainer import ExplainerAgent, EXACT_SAFETY_DISCLAIMER
from app.main import app


class TestMCPHelpAndVoiceQA(unittest.TestCase):
    def test_mcp_find_nearby_help_red(self):
        res = find_nearby_help(urgency="red", language="en")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["urgency"], "red")
        self.assertIn("hospital", res["map_url"].lower())
        self.assertIn("108", [h["code"] for h in res["helplines"]])
        self.assertIn("Urgent", res["title"])

    def test_mcp_find_nearby_help_yellow(self):
        res = find_nearby_help(urgency="yellow", language="hi")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["urgency"], "yellow")
        self.assertIn("104", [h["code"] for h in res["helplines"]])
        self.assertIn("डॉक्टर", res["title"])

    def test_mcp_find_nearby_help_with_gps(self):
        res = find_nearby_help(urgency="red", latitude=9.9312, longitude=76.2673, language="ml")
        self.assertTrue(res["has_gps"])
        self.assertIn("@9.9312,76.2673", res["map_url"])
        self.assertIn("അടിയന്തിര", res["title"])

    def test_explainer_answer_question_safety(self):
        async def run_test():
            explainer = ExplainerAgent(api_key="")
            # Ask sugar question
            ans = await explainer.answer_question("Is my fasting blood sugar high?", language="en")
            self.assertTrue(ans.endswith(EXACT_SAFETY_DISCLAIMER))
            # Must not diagnose
            self.assertNotIn("you have diabetes", ans.lower())

            # Ask in Malayalam
            ans_ml = await explainer.answer_question("എന്റെ ഷുഗർ അളവ് എത്രയാണ്?", language="ml")
            self.assertTrue(ans_ml.endswith(EXACT_SAFETY_DISCLAIMER))
        asyncio.run(run_test())

    def test_api_nearby_help_endpoint(self):
        async def run_test():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                res = await client.get("/api/help/nearby?urgency=red&language=ml")
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertEqual(data["status"], "success")
                self.assertEqual(data["urgency"], "red")
                self.assertIn("map_url", data)
                self.assertIn("helplines", data)
        asyncio.run(run_test())

    def test_api_voice_ask_loop(self):
        async def run_test():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                # 1. Text question through /api/ask
                res_ask = await client.post("/api/ask", data={"question": "What does my hemoglobin mean?", "language": "en"})
                self.assertEqual(res_ask.status_code, 200)
                data_ask = res_ask.json()
                self.assertTrue(data_ask["success"])
                self.assertIn("answer", data_ask)
                self.assertIn("provider", data_ask)
                self.assertTrue(data_ask["answer"].endswith(EXACT_SAFETY_DISCLAIMER))

                # 2. Audio question through /api/voice/ask
                # Send mock wave audio
                mock_wav = b"RIFF" + b"\x00" * 36 + b"WAVEfmt " + b"\x00" * 20 + b"data" + b"\x00" * 64
                res_voice_ask = await client.post(
                    "/api/voice/ask",
                    files={"file": ("question.wav", mock_wav, "audio/wav")},
                    data={"question": "Is my blood sugar normal?", "language": "hi"}
                )
                self.assertEqual(res_voice_ask.status_code, 200)
                data_voice = res_voice_ask.json()
                self.assertTrue(data_voice["success"])
                self.assertIn("answer", data_voice)
                self.assertIn("provider", data_voice)
        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
