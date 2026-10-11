"""
Checker Agent: Fast, deterministic, non-AI rule-based decision layer (System One).
Deliberately NOT an LLM for medical precision and safety.

Compares extracted lab test values against clinical limits in ranges.json:
- Normal range: GREEN (normal)
- Outside normal: YELLOW (watch / consult doctor)
- Beyond critical limits: RED (urgent / immediate attention)
- Unknown or unmeasurable tests: Skipped
"""

import json
import logging
import os
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Common pathology & diagnostic abbreviations mapped to standardized clinical terms
CLINICAL_ABBREVIATIONS: Dict[str, str] = {
    "creat": "creatinine",
    "chol": "cholesterol",
    "bili": "bilirubin",
    "trig": "triglycerides",
    "trigl": "triglycerides",
    "tg": "triglycerides",
    "hb": "hemoglobin",
    "haem": "hemoglobin",
    "plt": "platelets",
    "glu": "glucose",
    "leuko": "leukocytes",
    "lympho": "lymphocytes",
    "neutro": "neutrophils",
    "eosino": "eosinophils",
    "mono": "monocytes",
    "baso": "basophils",
    "alk": "alkaline",
    "phos": "phosphatase",
    "alp": "alkaline phosphatase"
}

class CheckerAgent:
    def __init__(self, ranges_path: Optional[str] = None):
        if ranges_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            ranges_path = str(base_dir / "data" / "ranges.json")
        
        self.ranges_path = ranges_path
        self.ranges_data = self._load_ranges()

    def _load_ranges(self) -> Dict[str, Any]:
        """Loads reference ranges from local JSON configuration."""
        try:
            with open(self.ranges_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load ranges from {self.ranges_path}: {e}")
            return {"tests": {}}

    @staticmethod
    def _normalize_name(name: Optional[str]) -> str:
        """Strip punctuation, spaces, and lowercase for matching."""
        if not name:
            return ""
        return re.sub(r"[^a-z0-9]", "", name.lower())

    @classmethod
    def _normalize_medical_text(cls, text: Optional[str]) -> Tuple[str, str, str]:
        """
        Normalizes medical test names by:
        1. Converting to lowercase.
        2. Standardizing common clinical prefixes (e.g. 's.', 'serum', 'b.', 'blood', 'total', 'plasma').
        3. Stripping non-alphanumeric punctuation.
        4. Expanding common clinical abbreviations (e.g. 'creat' -> 'creatinine').
        Returns:
            (norm_str, sorted_str, clean_nospace)
        """
        if not text:
            return "", "", ""
        s = text.lower().strip()
        s = re.sub(r"\b(s|serum|plasma|blood|b|total|t)\b[\s\.]*", " ", s)
        s = re.sub(r"^s[\.\s]+", " ", s)
        s = re.sub(r"^b[\.\s]+", " ", s)
        s = re.sub(r"[^a-z0-9\s]", " ", s)
        tokens = []
        for t in s.split():
            clean_t = t.strip()
            if clean_t:
                expanded = CLINICAL_ABBREVIATIONS.get(clean_t, clean_t)
                tokens.append(expanded)
        norm_str = " ".join(tokens)
        sorted_str = " ".join(sorted(tokens))
        clean_nospace = re.sub(r"[^a-z0-9]", "", text.lower())
        return norm_str, sorted_str, clean_nospace

    @staticmethod
    def _parse_reference_range(range_str: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Parses min and max from lab report interval strings like:
        '13 - 17', '4,800 - 10,800', '20 - 40', '31.5 - 34.5', '< 2', '> 10'
        """
        if not range_str:
            return None, None
        s = range_str.replace(",", "").strip()
        # Pattern for "min - max" or "min to max"
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(?:-|to)\s*([0-9]+(?:\.[0-9]+)?)", s, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1)), float(m.group(2))
            except ValueError:
                pass
        # Pattern for "< max" or "<= max"
        m = re.search(r"(?:<|<=)\s*([0-9]+(?:\.[0-9]+)?)", s)
        if m:
            try:
                return 0.0, float(m.group(1))
            except ValueError:
                pass
        # Pattern for "> min" or ">= min"
        m = re.search(r"(?:>|>=)\s*([0-9]+(?:\.[0-9]+)?)", s)
        if m:
            try:
                return float(m.group(1)), None
            except ValueError:
                pass
        return None, None

    def find_matching_rule_with_score(
        self,
        test_name: str,
        similarity_threshold: float = 0.80
    ) -> Optional[Tuple[str, Dict[str, Any], float]]:
        """
        Matches an extracted test name against canonical keys and aliases in ranges.json
        using exact, normalized, token-sorted, and fuzzy string matching.
        Returns:
            (test_key, test_def, confidence_score) or None
        """
        if not test_name:
            return None

        t_norm, t_sort, t_clean = self._normalize_medical_text(test_name)
        if not t_norm and not t_clean:
            return None

        tests_catalog = self.ranges_data.get("tests", {})

        # 1. Exact match on raw clean key, canonical name, or aliases (Score = 1.0)
        for test_key, test_def in tests_catalog.items():
            if re.sub(r"[^a-z0-9]", "", test_key.lower()) == t_clean:
                return test_key, test_def, 1.0
            if re.sub(r"[^a-z0-9]", "", test_def.get("canonical_name", "").lower()) == t_clean:
                return test_key, test_def, 1.0
            for alias in test_def.get("aliases", []):
                if re.sub(r"[^a-z0-9]", "", alias.lower()) == t_clean:
                    return test_key, test_def, 1.0

        # 2. Exact match on medical normalized & abbreviation-expanded string (Score = 1.0)
        for test_key, test_def in tests_catalog.items():
            k_norm, k_sort, _ = self._normalize_medical_text(test_key)
            c_norm, c_sort, _ = self._normalize_medical_text(test_def.get("canonical_name", ""))
            if t_norm and (t_norm == k_norm or t_norm == c_norm):
                return test_key, test_def, 1.0
            if t_sort and (t_sort == k_sort or t_sort == c_sort):
                return test_key, test_def, 1.0
            for alias in test_def.get("aliases", []):
                a_norm, a_sort, _ = self._normalize_medical_text(alias)
                if t_norm and t_norm == a_norm:
                    return test_key, test_def, 1.0
                if t_sort and t_sort == a_sort:
                    return test_key, test_def, 1.0

        # 3. Substring matching prioritized by longest matching alias (minimum 4 chars)
        best_sub = None
        best_sub_len = 0
        for test_key, test_def in tests_catalog.items():
            for alias in test_def.get("aliases", []):
                _, _, a_clean = self._normalize_medical_text(alias)
                if len(a_clean) >= 4 and len(t_clean) >= 4:
                    if a_clean in t_clean and len(a_clean) > best_sub_len:
                        best_sub_len = len(a_clean)
                        best_sub = (test_key, test_def)
                    elif t_clean in a_clean and len(t_clean) > best_sub_len:
                        best_sub_len = len(t_clean)
                        best_sub = (test_key, test_def)

        if best_sub:
            return best_sub[0], best_sub[1], 0.95

        # 4. Fuzzy SequenceMatcher comparison against keys, canonical names, and aliases
        best_fuzzy_match = None
        best_fuzzy_score = 0.0

        for test_key, test_def in tests_catalog.items():
            candidate_strings = [test_key, test_def.get("canonical_name", "")] + test_def.get("aliases", [])
            for cand in candidate_strings:
                c_norm, c_sort, c_clean = self._normalize_medical_text(cand)

                # Safety guardrail: Do NOT loosely fuzzy-match short acronyms (<= 4 chars)
                # to prevent catastrophic medical collisions (e.g. MCH vs MCHC, T3 vs T4)
                if len(t_clean) <= 4 or len(c_clean) <= 4:
                    continue

                r_norm = SequenceMatcher(None, t_norm, c_norm).ratio()
                r_sort = SequenceMatcher(None, t_sort, c_sort).ratio()
                r_clean = SequenceMatcher(None, t_clean, c_clean).ratio()
                score = max(r_norm, r_sort, r_clean)

                if score > best_fuzzy_score:
                    best_fuzzy_score = score
                    best_fuzzy_match = (test_key, test_def)

        if best_fuzzy_match and best_fuzzy_score >= similarity_threshold:
            return best_fuzzy_match[0], best_fuzzy_match[1], round(best_fuzzy_score, 3)

        return None

    def find_matching_rule(self, test_name: str, similarity_threshold: float = 0.80) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Matches an extracted test name against canonical keys and aliases in ranges.json.
        Preserves 2-tuple return format (test_key, test_def) for backward compatibility.
        """
        res = self.find_matching_rule_with_score(test_name, similarity_threshold=similarity_threshold)
        if res:
            return res[0], res[1]
        return None

    def evaluate_test(self, test_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Evaluates a single extracted test against deterministic reference ranges.
        Labels test as:
          - 'green' for normal
          - 'yellow' for watch
          - 'red' for urgent
        Accurately respects the lab report's printed biological reference interval and flags.
        """
        raw_name = str(test_item.get("test_name", "")).strip()
        raw_val = test_item.get("value")
        raw_unit = str(test_item.get("unit", "")).strip()
        raw_range = str(test_item.get("reference_range", "") or "").strip()
        raw_flag = str(test_item.get("flag", "") or "").strip().upper()

        # Parse numerical value
        if raw_val is None:
            return None

        try:
            if isinstance(raw_val, str):
                cleaned_val = raw_val.replace(",", "").strip()
                val = float(cleaned_val)
            else:
                val = float(raw_val)
        except (TypeError, ValueError):
            return None

        # Look up rule in ranges.json with fuzzy and normalized matching
        matched_result = self.find_matching_rule_with_score(raw_name)

        # Parse report's printed biological reference interval if available
        rep_min, rep_max = self._parse_reference_range(raw_range)

        # Safe Skip Guardrail: If rule was not found, safely skip rather than guessing a medical range
        if not matched_result:
            return None

        rule_key, rule, match_score = matched_result

        canonical_name = rule.get("canonical_name", raw_name)
        unit = raw_unit or rule.get("unit", "")

        normal = rule.get("normal", {})
        min_norm = rep_min if rep_min is not None else normal.get("min")
        max_norm = rep_max if rep_max is not None else normal.get("max")
        crit_low = rule.get("critical_low")
        crit_high = rule.get("critical_high")

        # Smart unit normalization for Platelets:
        # If reported as absolute count (e.g., 220000 /cumm) and rule uses lakhs/cumm (1.5 - 4.5)
        if (rule_key == "platelets" or "platelet" in rule_key.lower()) and val > 1000:
            val = round(val / 100000.0, 2)
            unit = "lakhs/cumm"

        # 1. Critical Urgent Check (RED)
        if (crit_low is not None and val < crit_low) or (crit_high is not None and val > crit_high):
            color = "red"
            status_code = "urgent"
            status_label = "Urgent (Immediate Attention)"
            direction = "very_low" if (crit_low is not None and val < crit_low) else "very_high"

        # 2. Outside Normal Range Check (YELLOW - Watch)
        elif (min_norm is not None and val < min_norm) or (max_norm is not None and val > max_norm) or raw_flag in ("L", "LOW", "H", "HIGH", "*"):
            color = "yellow"
            status_code = "watch"
            status_label = "Watch (Consult Doctor)"
            if (min_norm is not None and val < min_norm) or raw_flag in ("L", "LOW"):
                direction = "low"
            elif (max_norm is not None and val > max_norm) or raw_flag in ("H", "HIGH"):
                direction = "high"
            else:
                direction = "abnormal"

        # 3. Normal Range Check (GREEN - Normal)
        else:
            color = "green"
            status_code = "normal"
            status_label = "Normal Range"
            direction = "optimal"

        if raw_range:
            norm_formatted = f"{raw_range} {unit}".strip()
        elif min_norm is not None and max_norm is not None:
            norm_formatted = f"{min_norm} - {max_norm} {unit}".strip()
        elif max_norm is not None:
            norm_formatted = f"< {max_norm} {unit}".strip()
        else:
            norm_formatted = ""

        description = rule.get("description", {})
        if not description:
            description = {
                "en": f"Lab parameter: {canonical_name}",
                "hi": f"लैब परीक्षण: {canonical_name}",
                "ml": f"ലാബ് പരിശോധന: {canonical_name}",
                "ta": f"ஆய்வக சோதனை: {canonical_name}"
            }

        # Determine panel category (cbc, diabetes, lipids, liver, kidney, thyroid, general)
        panel = rule.get("panel")
        if not panel:
            combined_name = f"{raw_name} {canonical_name}".lower()
            if any(k in combined_name for k in ["wbc", "rbc", "hemoglobin", "haemoglobin", "platelet", "hct", "mcv", "mch", "neutrophil", "lymphocyte", "monocyte", "eosinophil", "basophil", "esr", "pcv"]):
                panel = "cbc"
            elif any(k in combined_name for k in ["sugar", "glucose", "fbs", "ppbs", "rbs", "hba1c"]):
                panel = "diabetes"
            elif any(k in combined_name for k in ["cholesterol", "lipid", "triglyceride", "hdl", "ldl", "vldl"]):
                panel = "lipids"
            elif any(k in combined_name for k in ["bilirubin", "sgpt", "sgot", "alt", "ast", "alkaline phosphatase", "alp", "albumin", "globulin", "protein", "ggt", "lft"]):
                panel = "liver"
            elif any(k in combined_name for k in ["creatinine", "urea", "bun", "uric acid", "kft", "rft"]):
                panel = "kidney"
            elif any(k in combined_name for k in ["tsh", "t3", "t4", "ft3", "ft4", "thyroid"]):
                panel = "thyroid"
            else:
                panel = "general"

        return {
            "test_name": raw_name,
            "canonical_name": canonical_name,
            "rule_key": rule_key,
            "panel": panel,
            "value": val,
            "unit": unit,
            "match_confidence": match_score,
            "color": color,           # "green" | "yellow" | "red"
            "status_code": status_code, # "normal" | "watch" | "urgent"
            "status_label": status_label,
            "direction": direction,   # "optimal" | "low" | "high" | "very_low" | "very_high"
            "normal_range": {
                "min": min_norm,
                "max": max_norm,
                "formatted": norm_formatted
            },
            "description": description
        }

    def check_results(self, raw_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs batch evaluation against ranges.json.
        Labels known tests as green, yellow, or red while skipping unknown or unmeasurable tests.
        Flags unrecognized tests under 'needs_human_review' for safety.
        """
        evaluated_items: List[Dict[str, Any]] = []
        skipped_tests: List[Dict[str, Any]] = []
        needs_human_review: List[Dict[str, Any]] = []

        for item in raw_tests:
            raw_name = str(item.get("test_name", "")).strip()
            raw_val = item.get("value")
            is_valid_num = False
            if raw_val is not None:
                try:
                    float(str(raw_val).replace(",", "").strip())
                    is_valid_num = True
                except (TypeError, ValueError):
                    pass

            evaluated = self.evaluate_test(item)
            if evaluated is None:
                if not is_valid_num:
                    reason = "Unreadable or non-numeric test value (requires manual review)"
                else:
                    reason = "Unrecognized parameter: falls below similarity threshold (requires physician/manual review)"

                review_entry = {
                    "test_name": raw_name or "Unknown",
                    "value": raw_val,
                    "unit": item.get("unit"),
                    "reference_range": item.get("reference_range"),
                    "flag": item.get("flag"),
                    "reason": reason
                }
                skipped_tests.append({
                    "test_name": raw_name or "Unknown",
                    "value": raw_val,
                    "unit": item.get("unit")
                })
                needs_human_review.append(review_entry)
                continue
            evaluated_items.append(evaluated)

        red_count = sum(1 for item in evaluated_items if item["color"] == "red")
        yellow_count = sum(1 for item in evaluated_items if item["color"] == "yellow")
        green_count = sum(1 for item in evaluated_items if item["color"] == "green")

        has_red = red_count > 0
        has_yellow = yellow_count > 0

        overall_status = "red" if has_red else ("yellow" if has_yellow else "green")

        return {
            "overall_status": overall_status,
            "is_urgent": has_red,
            "needs_attention": has_red or has_yellow,
            "total_tests": len(evaluated_items),
            "green_count": green_count,
            "yellow_count": yellow_count,
            "red_count": red_count,
            "skipped_count": len(skipped_tests),
            "skipped_tests": skipped_tests,
            "needs_human_review": needs_human_review,
            "unrecognized_tests": needs_human_review,
            "needs_review_count": len(needs_human_review),
            "items": evaluated_items
        }

    def compare_with_previous(
        self,
        current_items: List[Dict[str, Any]],
        previous_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Longitudinal Trend Tracker: Compares current test values against the previous report.
        Calculates:
          - Numerical difference (delta = current - previous)
          - Percentage change
          - Trajectory direction (up, down, same)
          - Health impact (improved, worsened, stable)
          - Multilingual spoken explanations for patient voice delivery.
        """
        if not current_items or not previous_items:
            return {
                "has_comparison": False,
                "total_compared": 0,
                "improved_count": 0,
                "worsened_count": 0,
                "stable_count": 0,
                "overall_trajectory": "stable",
                "comparisons": [],
                "spoken_summary": {
                    "en": "",
                    "hi": "",
                    "ml": "",
                    "ta": "",
                    "te": ""
                }
            }

        # Build index of previous tests
        prev_by_key: Dict[str, Dict[str, Any]] = {}
        prev_by_norm: Dict[str, Dict[str, Any]] = {}

        for item in previous_items:
            rkey = item.get("rule_key")
            if rkey and rkey != "custom_lab_test":
                prev_by_key[rkey] = item
            cname = item.get("canonical_name") or item.get("test_name", "")
            if cname:
                prev_by_norm[self._normalize_name(cname)] = item
            tname = item.get("test_name", "")
            if tname:
                prev_by_norm[self._normalize_name(tname)] = item

        comparisons: List[Dict[str, Any]] = []

        for curr in current_items:
            rkey = curr.get("rule_key")
            matched_prev = None
            if rkey and rkey in prev_by_key:
                matched_prev = prev_by_key[rkey]
            else:
                cname_norm = self._normalize_name(curr.get("canonical_name", ""))
                tname_norm = self._normalize_name(curr.get("test_name", ""))
                if cname_norm in prev_by_norm:
                    matched_prev = prev_by_norm[cname_norm]
                elif tname_norm in prev_by_norm:
                    matched_prev = prev_by_norm[tname_norm]

            if not matched_prev:
                continue

            curr_raw = curr.get("value")
            prev_raw = matched_prev.get("value")
            if curr_raw is None or prev_raw is None:
                continue

            try:
                curr_val = float(curr_raw)
                prev_val = float(prev_raw)
            except (TypeError, ValueError):
                continue

            delta = round(curr_val - prev_val, 2)
            pct_change = round(((curr_val - prev_val) / prev_val) * 100.0, 1) if prev_val != 0 else 0.0

            if delta > 0.0001:
                trend_dir = "up"
            elif delta < -0.0001:
                trend_dir = "down"
            else:
                trend_dir = "same"

            # Determine clinical normal limits
            normal_data = curr.get("normal_range") or matched_prev.get("normal_range") or {}
            min_norm = normal_data.get("min")
            max_norm = normal_data.get("max")

            if min_norm is None and max_norm is None and rkey:
                candidate_name = curr.get("canonical_name") or curr.get("test_name")
                if isinstance(candidate_name, str) and candidate_name:
                    rule_match = self.find_matching_rule(candidate_name)
                    if rule_match:
                        rule_def = rule_match[1].get("normal", {})
                        min_norm = rule_def.get("min")
                        max_norm = rule_def.get("max")

            # Distance from normal bounds
            def _dist(val: float, mn: Optional[float], mx: Optional[float]) -> float:
                if mn is not None and val < mn:
                    return round(mn - val, 3)
                if mx is not None and val > mx:
                    return round(val - mx, 3)
                return 0.0

            d_prev = _dist(prev_val, min_norm, max_norm)
            d_curr = _dist(curr_val, min_norm, max_norm)

            # Determine health impact
            if min_norm is None and max_norm is None:
                if abs(delta) < 0.001:
                    health_impact = "stable"
                else:
                    health_impact = "changed"
            else:
                if d_curr == 0.0 and d_prev == 0.0:
                    health_impact = "stable"
                elif d_curr < d_prev:
                    health_impact = "improved"
                elif d_curr > d_prev:
                    health_impact = "worsened"
                else:
                    health_impact = "stable"

            canonical = curr.get("canonical_name") or curr.get("test_name")
            unit = curr.get("unit") or matched_prev.get("unit") or ""
            abs_delta = abs(delta)

            # Multilingual friendly explanation per test
            if health_impact == "improved":
                if trend_dir == "down":
                    en_msg = f"{canonical} is lower by {abs_delta:g} {unit} since last time, which is good progress."
                    ml_msg = f"{canonical} കഴിഞ്ഞ തവണത്തേക്കാൾ {abs_delta:g} {unit} കുറഞ്ഞു, ഇത് നല്ല മാറ്റമാണ്."
                    hi_msg = f"{canonical} पिछली बार से {abs_delta:g} {unit} कम हुआ है, यह एक अच्छा सुधार है।"
                    ta_msg = f"{canonical} கடந்த முறையை விட {abs_delta:g} {unit} குறைந்துள்ளது, இது நல்ல முன்னேற்றம்."
                    te_msg = f"{canonical} గత పరీక్ష కంటే {abs_delta:g} {unit} తగ్గింది, ఇది మంచి మెరుగుదల."
                else:
                    en_msg = f"{canonical} increased by {abs_delta:g} {unit} into a healthier range."
                    ml_msg = f"{canonical} കഴിഞ്ഞ തവണത്തേക്കാൾ {abs_delta:g} {unit} വർദ്ധിച്ച് കൂടുതൽ ആരോഗ്യകരമായ നിലയിലായി."
                    hi_msg = f"{canonical} में {abs_delta:g} {unit} की बढ़ोतरी होकर सुरक्षित स्तर पर आ गया है।"
                    ta_msg = f"{canonical} {abs_delta:g} {unit} அதிகரித்து பாதுகாப்பான நிலைக்கு வந்துள்ளது."
                    te_msg = f"{canonical} {abs_delta:g} {unit} పెరిగి సురక్షిత స్థాయికి చేరుకుంది."
            elif health_impact == "worsened":
                if trend_dir == "up":
                    en_msg = f"{canonical} increased by {abs_delta:g} {unit} compared to last time and needs review."
                    ml_msg = f"{canonical} കഴിഞ്ഞ തവണത്തേക്കാൾ {abs_delta:g} {unit} കൂടിയിട്ടുണ്ട്, ഡോക്ടറെ കാണിക്കുന്നത് നന്നായിരിക്കും."
                    hi_msg = f"{canonical} पिछली बार से {abs_delta:g} {unit} बढ़ गया है, डॉक्टर से परामर्श आवश्यक है।"
                    ta_msg = f"{canonical} கடந்த முறையை விட {abs_delta:g} {unit} அதிகரித்துள்ளது, மருத்துவரிடம் காட்டுங்கள்."
                    te_msg = f"{canonical} గత పరీక్ష కంటే {abs_delta:g} {unit} పెరిగింది, వైద్యుడిని సంప్రదించడం మంచిది."
                else:
                    en_msg = f"{canonical} dropped by {abs_delta:g} {unit} below optimal level since last time."
                    ml_msg = f"{canonical} കഴിഞ്ഞ തവണത്തേക്കാൾ {abs_delta:g} {unit} കുറഞ്ഞിട്ടുണ്ട്, ശ്രദ്ധിക്കുക."
                    hi_msg = f"{canonical} पिछली बार की तुलना में {abs_delta:g} {unit} कम हुआ है, ध्यान देना जरूरी है।"
                    ta_msg = f"{canonical} கடந்த முறையை விட {abs_delta:g} {unit} குறைந்துள்ளது, கவனம் தேவை."
                    te_msg = f"{canonical} గత పరీక్ష కంటే {abs_delta:g} {unit} తగ్గింది, శ్రద్ధ వహించండి."
            else:
                en_msg = f"{canonical} is steady with little change ({delta:+g} {unit})."
                ml_msg = f"{canonical} കാര്യമായ മാറ്റമില്ലാതെ സ്ഥിരമായി തുടരുന്നു."
                hi_msg = f"{canonical} बिना किसी बड़े बदलाव के स्थिर बना हुआ है।"
                ta_msg = f"{canonical} பெரிய மாற்றமின்றி சீராக உள்ளது."
                te_msg = f"{canonical} పెద్ద మార్పు లేకుండా స్థిరంగా ఉంది."

            comparisons.append({
                "test_name": curr.get("test_name"),
                "canonical_name": canonical,
                "rule_key": rkey or curr.get("canonical_name"),
                "previous_value": prev_val,
                "current_value": curr_val,
                "unit": unit,
                "delta": delta,
                "delta_formatted": f"{'+' if delta > 0 else ''}{delta:g}",
                "percent_change": pct_change,
                "trend_direction": trend_dir,
                "health_impact": health_impact,
                "previous_color": matched_prev.get("color", "green"),
                "current_color": curr.get("color", "green"),
                "normal_range": normal_data,
                "message": {
                    "en": en_msg,
                    "ml": ml_msg,
                    "hi": hi_msg,
                    "ta": ta_msg,
                    "te": te_msg
                }
            })

        improved_count = sum(1 for c in comparisons if c["health_impact"] == "improved")
        worsened_count = sum(1 for c in comparisons if c["health_impact"] == "worsened")
        stable_count = sum(1 for c in comparisons if c["health_impact"] == "stable")

        if improved_count > worsened_count:
            overall_trajectory = "improving"
        elif worsened_count > improved_count:
            overall_trajectory = "worsening"
        else:
            overall_trajectory = "stable"

        # Build composite spoken summary lines
        top_improved = [c for c in comparisons if c["health_impact"] == "improved"]
        top_worsened = [c for c in comparisons if c["health_impact"] == "worsened"]

        spoken_en_parts = []
        spoken_ml_parts = []
        spoken_hi_parts = []
        spoken_ta_parts = []
        spoken_te_parts = []

        if top_improved:
            item = top_improved[0]
            spoken_en_parts.append(item["message"]["en"])
            spoken_ml_parts.append(item["message"]["ml"])
            spoken_hi_parts.append(item["message"]["hi"])
            spoken_ta_parts.append(item["message"]["ta"])
            spoken_te_parts.append(item["message"]["te"])

        if top_worsened:
            item = top_worsened[0]
            spoken_en_parts.append(item["message"]["en"])
            spoken_ml_parts.append(item["message"]["ml"])
            spoken_hi_parts.append(item["message"]["hi"])
            spoken_ta_parts.append(item["message"]["ta"])
            spoken_te_parts.append(item["message"]["te"])

        if not top_improved and not top_worsened and comparisons:
            spoken_en_parts.append("Your test numbers are steady compared to your previous report.")
            spoken_ml_parts.append("കഴിഞ്ഞ റിപ്പോർട്ടുമായി താരതമ്യം ചെയ്യുമ്പോൾ പരിശോധനാ ഫലങ്ങൾ സ്ഥിരതയുള്ളതാണ്.")
            spoken_hi_parts.append("आपकी पिछली रिपोर्ट की तुलना में जांच के परिणाम स्थिर बने हुए हैं।")
            spoken_ta_parts.append("உங்கள் முந்தைய அறிக்கையுடன் ஒப்பிடுகையில் பரிசோதனை முடிவுகள் சீராக உள்ளன.")
            spoken_te_parts.append("మీ మునుపటి నివేదికతో పోలిస్తే పరీక్ష ఫలితాలు స్థిరంగా ఉన్నాయి.")

        return {
            "has_comparison": len(comparisons) > 0,
            "total_compared": len(comparisons),
            "improved_count": improved_count,
            "worsened_count": worsened_count,
            "stable_count": stable_count,
            "overall_trajectory": overall_trajectory,
            "comparisons": comparisons,
            "spoken_summary": {
                "en": " ".join(spoken_en_parts),
                "ml": " ".join(spoken_ml_parts),
                "hi": " ".join(spoken_hi_parts),
                "ta": " ".join(spoken_ta_parts),
                "te": " ".join(spoken_te_parts)
            }
        }
