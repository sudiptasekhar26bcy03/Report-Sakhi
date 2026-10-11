import unittest
from app.agents.checker import CheckerAgent


class TestCheckerFuzzyAndNormalization(unittest.TestCase):
    def setUp(self):
        self.checker = CheckerAgent()

    def test_fuzzy_creatinine_variations(self):
        """Tests that various lab formats, prefixes, and misspellings for Creatinine match accurately."""
        variations = [
            "S.Creatinine",
            "Serum Creat.",
            "Creatinine Serum",
            "S. Creat",
            "Serum Creatnine",  # common typo
            "Creatinine, Serum"
        ]
        for name in variations:
            res = self.checker.find_matching_rule(name)
            self.assertIsNotNone(res, f"Failed to match variation: {name}")
            test_key, test_def = res
            self.assertEqual(test_key, "serum_creatinine", f"Variation {name} mapped to {test_key} instead of serum_creatinine")

    def test_fuzzy_cholesterol_and_hemoglobin(self):
        """Tests typos in longer descriptive lab test names."""
        res_chol = self.checker.find_matching_rule("Total Cholestrol")  # missing 'e'
        self.assertIsNotNone(res_chol)
        self.assertEqual(res_chol[0], "total_cholesterol")

        res_hb1 = self.checker.find_matching_rule("Haemoglobin")
        self.assertIsNotNone(res_hb1)
        self.assertEqual(res_hb1[0], "hemoglobin")

        res_hb2 = self.checker.find_matching_rule("Hemogloblin")  # typo with extra 'l'
        self.assertIsNotNone(res_hb2)
        self.assertEqual(res_hb2[0], "hemoglobin")

    def test_clinical_acronym_collision_guardrails(self):
        """Tests that short acronyms (<= 4 chars) NEVER falsely cross-match."""
        # MCH vs MCHC
        mch_res = self.checker.find_matching_rule("MCH")
        self.assertIsNotNone(mch_res)
        self.assertEqual(mch_res[0], "mch")

        mchc_res = self.checker.find_matching_rule("MCHC")
        self.assertIsNotNone(mchc_res)
        self.assertEqual(mchc_res[0], "mchc")

        # T3 vs T4
        t3_res = self.checker.find_matching_rule("T3")
        self.assertIsNotNone(t3_res)
        self.assertEqual(t3_res[0], "total_t3")

        t4_res = self.checker.find_matching_rule("T4")
        self.assertIsNotNone(t4_res)
        self.assertEqual(t4_res[0], "total_t4")

        # SGOT vs SGPT
        sgot_res = self.checker.find_matching_rule("SGOT")
        self.assertIsNotNone(sgot_res)
        self.assertEqual(sgot_res[0], "sgot_ast")

        sgpt_res = self.checker.find_matching_rule("SGPT")
        self.assertIsNotNone(sgpt_res)
        self.assertEqual(sgpt_res[0], "sgpt_alt")

    def test_safe_skip_and_needs_human_review_flag(self):
        """Tests that unrecognizable tests are safely skipped and flagged under needs_human_review."""
        batch = [
            {"test_name": "S.Creatinine", "value": 1.1, "unit": "mg/dL"},
            {"test_name": "Mysterious Enzyme XYZ-999", "value": 42.0, "unit": "U/L"},
            {"test_name": "Unrecognized Marker 123", "value": "15.5", "unit": "ng/mL"}
        ]
        res = self.checker.check_results(batch)

        # Only S.Creatinine should be evaluated in items
        self.assertEqual(res["total_tests"], 1)
        self.assertEqual(len(res["items"]), 1)
        self.assertEqual(res["items"][0]["canonical_name"], "Serum Creatinine")
        self.assertEqual(res["items"][0]["color"], "green")

        # The 2 unrecognized tests must be in needs_human_review & skipped_tests
        self.assertIn("needs_human_review", res)
        self.assertEqual(len(res["needs_human_review"]), 2)
        self.assertEqual(res["skipped_count"], 2)

        flagged_names = [item["test_name"] for item in res["needs_human_review"]]
        self.assertIn("Mysterious Enzyme XYZ-999", flagged_names)
        self.assertIn("Unrecognized Marker 123", flagged_names)

        # Check that reasons are clearly given
        for item in res["needs_human_review"]:
            self.assertIn("reason", item)
            self.assertIn("manual review", item["reason"].lower())


if __name__ == "__main__":
    unittest.main()
