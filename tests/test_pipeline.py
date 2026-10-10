import asyncio
import unittest
from app.agents.checker import CheckerAgent
from app.agents.reader import ReaderAgent
from app.agents.explainer import ExplainerAgent, EXACT_SAFETY_DISCLAIMER
from app.agents.pipeline import ReportSakhiPipeline


class TestReportSakhi(unittest.TestCase):
    def setUp(self):
        self.checker = CheckerAgent()
        self.reader = ReaderAgent()
        self.explainer = ExplainerAgent()

    def test_checker_normal(self):
        res = self.checker.check_results([
            {"test_name": "Hemoglobin", "value": 14.5, "unit": "g/dL"}
        ])
        self.assertEqual(res["overall_status"], "green")
        self.assertFalse(res["is_urgent"])
        self.assertFalse(res["needs_attention"])
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["color"], "green")
        self.assertEqual(res["items"][0]["status_code"], "normal")

    def test_checker_yellow_watch(self):
        res = self.checker.check_results([
            {"test_name": "Fasting Blood Sugar", "value": 130.0, "unit": "mg/dL"}
        ])
        self.assertEqual(res["overall_status"], "yellow")
        self.assertTrue(res["needs_attention"])
        self.assertFalse(res["is_urgent"])
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["color"], "yellow")
        self.assertEqual(res["items"][0]["status_code"], "watch")

    def test_checker_critical_red_urgent(self):
        res = self.checker.check_results([
            {"test_name": "Hemoglobin", "value": 5.8, "unit": "g/dL"}
        ])
        self.assertEqual(res["overall_status"], "red")
        self.assertTrue(res["is_urgent"])
        self.assertTrue(res["needs_attention"])
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["color"], "red")
        self.assertEqual(res["items"][0]["status_code"], "urgent")

    def test_checker_skips_unknown_tests(self):
        """Checker must skip tests not present in ranges.json while labeling known ones."""
        res = self.checker.check_results([
            {"test_name": "Hemoglobin", "value": 13.5, "unit": "g/dL"},
            {"test_name": "Random Unknown Enzyme XYZ", "value": 85.0, "unit": "U/L"},
            {"test_name": "NonExistentPanel_123", "value": 1.2, "unit": "mg/dL"}
        ])
        # Only Hemoglobin should be in items
        self.assertEqual(res["total_tests"], 1)
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["canonical_name"], "Hemoglobin (Hb)")
        self.assertEqual(res["items"][0]["color"], "green")
        # Skipped tests should be tracked
        self.assertEqual(res["skipped_count"], 2)
        self.assertEqual(len(res["skipped_tests"]), 2)

    def test_checker_skips_unmeasurable_values(self):
        """Checker must skip tests with non-numeric or unreadable values."""
        res = self.checker.check_results([
            {"test_name": "Hemoglobin", "value": "Unreadable", "unit": "g/dL"},
            {"test_name": "Fasting Blood Sugar", "value": None, "unit": "mg/dL"},
            {"test_name": "Total WBC Count", "value": 6500.0, "unit": "/cumm"}
        ])
        self.assertEqual(res["total_tests"], 1)
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["canonical_name"], "Total WBC Count")
        self.assertEqual(res["skipped_count"], 2)

    def test_checker_platelet_unit_normalization(self):
        """Checker should normalize platelet counts from absolute /cumm (e.g. 220,000) to lakhs/cumm."""
        res = self.checker.check_results([
            {"test_name": "Platelets", "value": 220000, "unit": "/cumm"}
        ])
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["value"], 2.2)
        self.assertEqual(res["items"][0]["color"], "green")

    def test_reader_empty_or_blurry_image(self):
        async def run_test():
            # Empty bytes
            res = await self.reader.extract_tests(b"")
            self.assertEqual(res["status"], "retake_required")
            self.assertFalse(res["is_clear"])
            self.assertEqual(len(res["tests"]), 0)

            # Tiny unclear bytes
            res2 = await self.reader.extract_tests(b"tiny")
            self.assertEqual(res2["status"], "retake_required")
            self.assertFalse(res2["is_clear"])
        asyncio.run(run_test())

    def test_reader_clean_json_extraction(self):
        async def run_test():
            res = await self.reader.extract_tests(b"DEMO_SAMPLE_REPORT_PAYLOAD_IMAGE")
            self.assertEqual(res["status"], "success")
            self.assertTrue(res["is_clear"])
            self.assertTrue(len(res["tests"]) > 0)
            for item in res["tests"]:
                self.assertIn("test_name", item)
                self.assertIn("value", item)
                self.assertIn("unit", item)
                self.assertIsInstance(item["value"], float)
        asyncio.run(run_test())

    def test_explainer_mandatory_safety_disclaimer(self):
        """Explainer must append the exact safety text to every result."""
        async def run_test():
            checked_data = self.checker.check_results([
                {"test_name": "Hemoglobin", "value": 14.0, "unit": "g/dL"}
            ])
            for lang in ["en", "hi", "ml", "ta"]:
                explanation = await self.explainer.generate_explanation(checked_data, language=lang)
                self.assertEqual(explanation["safety_line"], EXACT_SAFETY_DISCLAIMER)
                self.assertTrue(explanation["summary_text"].endswith(EXACT_SAFETY_DISCLAIMER))
                self.assertTrue(explanation["full_speech_script"].endswith(EXACT_SAFETY_DISCLAIMER))
        asyncio.run(run_test())

    def test_explainer_never_diagnoses(self):
        """Explainer must never produce forbidden medical diagnostic claims."""
        async def run_test():
            checked_data = self.checker.check_results([
                {"test_name": "Fasting Blood Sugar", "value": 180.0, "unit": "mg/dL"}
            ])
            explanation = await self.explainer.generate_explanation(checked_data, language="en")
            summary_lower = explanation["summary_text"].lower()
            forbidden = ["you have diabetes", "you are diagnosed with", "you are a diabetic"]
            for term in forbidden:
                self.assertNotIn(term, summary_lower)
        asyncio.run(run_test())

    def test_multilingual_pipeline(self):
        async def run_pipeline():
            pipeline = ReportSakhiPipeline()
            for lang in ["ml", "hi", "ta", "en"]:
                output = await pipeline.run(b"DEMO_SAMPLE_REPORT_IMAGE", language=lang)
                self.assertTrue(output["success"])
                self.assertTrue(len(output["checker"]["items"]) > 0)
                self.assertEqual(output["explainer"]["safety_line"], EXACT_SAFETY_DISCLAIMER)
                self.assertTrue(output["explainer"]["summary_text"].endswith(EXACT_SAFETY_DISCLAIMER))
                self.assertIn(output["checker"]["overall_status"], ["green", "yellow", "red"])
        asyncio.run(run_pipeline())


if __name__ == "__main__":
    unittest.main()
