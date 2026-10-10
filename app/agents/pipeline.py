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
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Executes the full 4-agent pipeline.
        """
        # Step 1: Reader Agent extracts test names and numbers
        reader_output = await self.reader.extract_tests(image_bytes, mime_type=mime_type)
        if reader_output.get("status") == "retake_required" or not reader_output.get("is_clear", True):
            return {
                "success": False,
                "status": "retake_required",
                "message": reader_output.get("message", "The photo seems unclear. Please retake the photo with better lighting instead of guessing."),
                "reader": reader_output,
                "checker": None,
                "explainer": None,
                "voice": None,
                "show_hospital_finder": False
            }

        extracted_tests = reader_output.get("tests", [])
        if not extracted_tests:
            return {
                "success": False,
                "status": "retake_required",
                "message": "No measurable lab test values could be clearly read from this photo. Please retake the photo of the report.",
                "reader": reader_output,
                "checker": None,
                "explainer": None,
                "voice": None,
                "show_hospital_finder": False
            }

        # Step 2: Checker Agent (deterministic rule-based System One layer)
        checker_output = self.checker.check_results(extracted_tests)

        # Step 3: Explainer Agent (Class 5 reading level + safety line)
        explainer_output = await self.explainer.generate_explanation(checker_output, language=language)

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
            "explainer": explainer_output,
            "voice": voice_output,
            "show_hospital_finder": show_hospital_finder
        }
