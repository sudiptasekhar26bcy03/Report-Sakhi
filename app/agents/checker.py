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
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

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
    def _normalize_name(name: str) -> str:
        """Strip punctuation, spaces, and lowercase for matching."""
        return re.sub(r"[^a-z0-9]", "", str(name).lower())

    def find_matching_rule(self, test_name: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Matches an extracted test name against canonical keys and aliases in ranges.json.
        Returns (rule_key, rule_dict) or None if not recognized.
        """
        if not test_name:
            return None

        clean_target = self._normalize_name(test_name)
        if not clean_target:
            return None

        tests_catalog = self.ranges_data.get("tests", {})

        # 1. Exact match on rule key
        for test_key, test_def in tests_catalog.items():
            if self._normalize_name(test_key) == clean_target:
                return test_key, test_def

        # 2. Exact match on aliases or canonical name
        for test_key, test_def in tests_catalog.items():
            canonical = test_def.get("canonical_name", "")
            if self._normalize_name(canonical) == clean_target:
                return test_key, test_def

            for alias in test_def.get("aliases", []):
                if self._normalize_name(alias) == clean_target:
                    return test_key, test_def

        # 3. Substring / token matching (e.g., 'blood sugar fasting' matches 'fasting blood sugar')
        for test_key, test_def in tests_catalog.items():
            for alias in test_def.get("aliases", []):
                alias_norm = self._normalize_name(alias)
                if alias_norm and (alias_norm in clean_target or clean_target in alias_norm):
                    return test_key, test_def

        return None

    def evaluate_test(self, test_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Evaluates a single extracted test against deterministic reference ranges.
        Labels test as:
          - 'green' for normal
          - 'yellow' for watch
          - 'red' for urgent
        Returns None for unknown tests or unmeasurable values (skipping them).
        """
        raw_name = str(test_item.get("test_name", "")).strip()
        raw_val = test_item.get("value")
        raw_unit = str(test_item.get("unit", "")).strip()

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
            # Unparseable value -> skip
            return None

        # Look up rule in ranges.json
        matched = self.find_matching_rule(raw_name)
        if not matched:
            # Unknown test -> skip
            return None

        rule_key, rule = matched

        canonical_name = rule.get("canonical_name", raw_name)
        unit = rule.get("unit", raw_unit)
        normal = rule.get("normal", {})
        min_norm = normal.get("min")
        max_norm = normal.get("max")
        crit_low = rule.get("critical_low")
        crit_high = rule.get("critical_high")

        # Smart unit normalization for Platelets:
        # If reported as absolute count (e.g., 220000 /cumm) and rule uses lakhs/cumm (1.5 - 4.5)
        if (rule_key == "platelets" or "platelet" in rule_key) and val > 1000:
            val = round(val / 100000.0, 2)

        # 1. Critical Urgent Check (RED)
        if (crit_low is not None and val < crit_low) or (crit_high is not None and val > crit_high):
            color = "red"
            status_code = "urgent"
            status_label = "Urgent (Immediate Attention)"
            direction = "very_low" if (crit_low is not None and val < crit_low) else "very_high"

        # 2. Outside Normal Range Check (YELLOW - Watch)
        elif (min_norm is not None and val < min_norm) or (max_norm is not None and val > max_norm):
            color = "yellow"
            status_code = "watch"
            status_label = "Watch (Consult Doctor)"
            direction = "low" if (min_norm is not None and val < min_norm) else "high"

        # 3. Normal Range Check (GREEN - Normal)
        else:
            color = "green"
            status_code = "normal"
            status_label = "Normal Range"
            direction = "optimal"

        norm_formatted = f"{min_norm} - {max_norm} {unit}".strip() if (min_norm is not None and max_norm is not None) else ""

        return {
            "test_name": raw_name,
            "canonical_name": canonical_name,
            "rule_key": rule_key,
            "value": val,
            "unit": unit,
            "color": color,           # "green" | "yellow" | "red"
            "status_code": status_code, # "normal" | "watch" | "urgent"
            "status_label": status_label,
            "direction": direction,   # "optimal" | "low" | "high" | "very_low" | "very_high"
            "normal_range": {
                "min": min_norm,
                "max": max_norm,
                "formatted": norm_formatted
            },
            "description": rule.get("description", {})
        }

    def check_results(self, raw_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs batch evaluation against ranges.json.
        Labels known tests as green, yellow, or red while skipping unknown or unmeasurable tests.
        """
        evaluated_items: List[Dict[str, Any]] = []
        skipped_tests: List[Dict[str, Any]] = []

        for item in raw_tests:
            evaluated = self.evaluate_test(item)
            if evaluated is None:
                skipped_tests.append({
                    "test_name": item.get("test_name", "Unknown"),
                    "value": item.get("value"),
                    "unit": item.get("unit")
                })
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
            "items": evaluated_items
        }
