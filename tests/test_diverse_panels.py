import unittest
from app.agents.checker import CheckerAgent
from app.agents.reader import ReaderAgent


class TestDiverseLabPanels(unittest.TestCase):
    def setUp(self):
        self.checker = CheckerAgent()
        self.reader = ReaderAgent()

    def test_lipid_panel_evaluation(self):
        tests = [
            {"test_name": "Total Cholesterol", "value": 240.0, "unit": "mg/dL"},
            {"test_name": "HDL Cholesterol", "value": 35.0, "unit": "mg/dL"},
            {"test_name": "LDL Cholesterol", "value": 165.0, "unit": "mg/dL"},
            {"test_name": "Triglycerides", "value": 220.0, "unit": "mg/dL"},
        ]
        res = self.checker.check_results(tests)
        self.assertEqual(res["overall_status"], "yellow")
        for item in res["items"]:
            self.assertEqual(item.get("panel"), "lipids")
            self.assertIn(item.get("color"), ["yellow", "red"])

    def test_liver_function_evaluation(self):
        tests = [
            {"test_name": "SGPT (ALT)", "value": 110.0, "unit": "U/L"},
            {"test_name": "SGOT (AST)", "value": 85.0, "unit": "U/L"},
            {"test_name": "Total Bilirubin", "value": 1.1, "unit": "mg/dL"},
            {"test_name": "Serum Albumin", "value": 4.2, "unit": "g/dL"},
        ]
        res = self.checker.check_results(tests)
        self.assertIn(res["overall_status"], ["yellow", "red"])
        for item in res["items"]:
            self.assertEqual(item.get("panel"), "liver")

    def test_thyroid_panel_evaluation(self):
        tests = [
            {"test_name": "TSH", "value": 8.5, "unit": "uIU/mL"},
            {"test_name": "Free T4", "value": 1.2, "unit": "ng/dL"},
        ]
        res = self.checker.check_results(tests)
        self.assertEqual(res["overall_status"], "yellow")
        for item in res["items"]:
            self.assertEqual(item.get("panel"), "thyroid")

    def test_kidney_panel_evaluation(self):
        tests = [
            {"test_name": "Serum Creatinine", "value": 4.5, "unit": "mg/dL"},
            {"test_name": "Blood Urea", "value": 45.0, "unit": "mg/dL"},
        ]
        res = self.checker.check_results(tests)
        self.assertEqual(res["overall_status"], "red")
        for item in res["items"]:
            self.assertEqual(item.get("panel"), "kidney")

    def test_reader_digital_text_diverse_extraction(self):
        sample_report_text = """
        METROPOLIS HEALTHCARE LAB REPORT
        PATIENT: Rahul Sharma  AGE: 45 Y / M

        LIPID PROFILE:
        Total Cholesterol: 210 mg/dL (Desirable: <200)
        HDL Cholesterol: 42 mg/dL (Normal: >40)
        LDL Cholesterol: 135 mg/dL (Optimal: <100)
        Triglycerides: 180 mg/dL (Normal: <150)

        LIVER FUNCTION TESTS:
        SGPT (ALT): 45 U/L (Normal: 10-40)
        SGOT (AST): 38 U/L (Normal: 10-40)
        Total Bilirubin: 0.9 mg/dL (Normal: 0.2-1.2)
        Serum Albumin: 4.1 g/dL (Normal: 3.5-5.2)

        THYROID PROFILE:
        TSH: 6.2 uIU/mL (Normal: 0.4 - 4.5)
        """
        extracted = self.reader._extract_tests_from_digital_text(sample_report_text)
        names = [t["test_name"].lower() for t in extracted]

        # Check presence of extracted items
        self.assertTrue(any("cholesterol" in n for n in names))
        self.assertTrue(any("hdl" in n for n in names))
        self.assertTrue(any("triglyceride" in n for n in names))
        self.assertTrue(any("sgpt" in n or "alt" in n for n in names))
        self.assertTrue(any("bilirubin" in n for n in names))
        self.assertTrue(any("tsh" in n for n in names))

        # Check evaluation assigns correct panels
        eval_res = self.checker.check_results(extracted)
        panels = {item["panel"] for item in eval_res["items"]}
        self.assertIn("lipids", panels)
        self.assertIn("liver", panels)
        self.assertIn("thyroid", panels)


if __name__ == "__main__":
    unittest.main()
