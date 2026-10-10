import os
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "ReportSakhi"
    version: str = "1.0.0"
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY", "")

    # Single VOICE_PROVIDER setting for one-line failover switching:
    # "bhashini", "sarvam", "google", "azure", "browser"
    voice_provider: str = os.getenv("VOICE_PROVIDER", "bhashini")

    # 1. Bhashini Credentials (Primary)
    bhashini_user_id: Optional[str] = os.getenv("BHASHINI_USER_ID", "")
    bhashini_api_key: Optional[str] = os.getenv("BHASHINI_API_KEY", "")
    bhashini_pipeline_id: Optional[str] = os.getenv("BHASHINI_PIPELINE_ID", "")

    # 2. Sarvam AI Credentials
    sarvam_api_key: Optional[str] = os.getenv("SARVAM_API_KEY", "")

    # 3. Google Cloud Credentials
    google_speech_api_key: Optional[str] = os.getenv("GOOGLE_SPEECH_API_KEY", "")

    # 4. Azure Cognitive Services Speech Credentials
    azure_speech_key: Optional[str] = os.getenv("AZURE_SPEECH_KEY", "")
    azure_speech_region: Optional[str] = os.getenv("AZURE_SPEECH_REGION", "centralindia")

    # Supported Indian Languages
    supported_languages: dict = {
        "ml": {"name": "മലയാളം", "code": "ml-IN", "english_name": "Malayalam"},
        "hi": {"name": "हिन्दी", "code": "hi-IN", "english_name": "Hindi"},
        "ta": {"name": "தமிழ்", "code": "ta-IN", "english_name": "Tamil"},
        "en": {"name": "English", "code": "en-IN", "english_name": "English"}
    }

    def get_voice_info(self) -> dict:
        return {
            "active_provider": self.voice_provider.lower().strip(),
            "supported_providers": ["bhashini", "sarvam", "google", "azure", "browser"],
            "has_bhashini_credentials": bool(self.bhashini_user_id and self.bhashini_api_key),
            "has_sarvam_credentials": bool(self.sarvam_api_key),
            "has_google_credentials": bool(self.google_speech_api_key),
            "has_azure_credentials": bool(self.azure_speech_key),
        }

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
