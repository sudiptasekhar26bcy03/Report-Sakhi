"""
Pipeline Orchestrator: Chains the four agents together.
Flow: Image -> Reader -> Checker -> Explainer -> Voice
"""

import logging
from typing import Dict, Any, Optional

from app.agents.reader import ReaderAgent
from app.agents.checker import CheckerAgent
from app.agents.explainer import ExplainerAgent
from app.agents.voice import VoiceAgent

logger = logging.getLogger(__name__)

class ReportSakhiPipeline:
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        voice_provider: Optional[str] = None,
        ranges_path: Optional[str] = None
    ):
        self.reader = ReaderAgent(api_key=gemini_api_key)
        self.checker = CheckerAgent(ranges_path=ranges_path)
        self.explainer = ExplainerAgent(api_key=gemini_api_key)
        self.voice = VoiceAgent(provider=voice_provider)

    async def run(
        self,
        document_or_documents: Any = None,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg",
        language: str = "en",
        previous_report: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes the full 4-agent pipeline with longitudinal comparison if previous report is provided.
        Accepts a single PDF/image (bytes) or a collection of documents/pages.
        """
        input_data = document_or_documents if document_or_documents is not None else (image_bytes or b"")

        # Step 1: Reader Agent extracts test names and numbers
        reader_output = await self.reader.extract_tests(input_data, mime_type=mime_type)
        if reader_output.get("status") == "retake_required" or not reader_output.get("is_clear", True):
            return {
                "success": False,
                "status": "retake_required",
                "message": reader_output.get("message", "The report seems unclear. Please upload a clear PDF or take a well-lit photo of the report instead of guessing."),
                "reader": reader_output,
                "checker": None,
                "comparison": None,
                "explainer": None,
                "voice": None,
                "show_hospital_finder": False
            }

        extracted_tests = reader_output.get("tests", [])
        if not extracted_tests:
            return {
                "success": False,
                "status": "retake_required",
                "message": "No measurable lab test values could be clearly read from this report. Please upload a clear PDF or well-lit photo.",
                "reader": reader_output,
                "checker": None,
                "comparison": None,
                "explainer": None,
                "voice": None,
                "show_hospital_finder": False
            }

        # Step 2: Checker Agent (deterministic rule-based System One layer)
        checker_output = self.checker.check_results(extracted_tests)

        # Step 2b: Longitudinal Comparison against previous report if provided
        comparison = None
        if previous_report and isinstance(previous_report, dict):
            prev_items = previous_report.get("items", []) or previous_report.get("checker", {}).get("items", [])
            if prev_items:
                comparison = self.checker.compare_with_previous(checker_output.get("items", []), prev_items)

        # Step 3: Explainer Agent (Class 5 reading level + longitudinal progress + safety line)
        explainer_output = await self.explainer.generate_explanation(
            checker_output,
            language=language,
            comparison=comparison
        )

        # Step 4: Voice Agent (TTS audio or client speech directive)
        voice_output = await self.voice.text_to_speech(
            explainer_output.get("full_speech_script", explainer_output.get("summary_text", "")),
            language_code=language
        )

        # Determine if Hospital/Lab finder should be actively presented
        show_hospital_finder = checker_output.get("needs_attention", False)

        return {
            "success": True,
            "status": "completed",
            "language": language,
            "reader": reader_output,
            "checker": checker_output,
            "comparison": comparison,
            "explainer": explainer_output,
            "voice": voice_output,
            "show_hospital_finder": show_hospital_finder
        }
