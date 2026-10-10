import os
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "ReportSakhi"
    version: str = "1.0.0"
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY", "")

    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

    # Single VOICE_PROVIDER setting for one-line failover switching:
    # "google", "browser", "bhashini", "sarvam", "azure"
    voice_provider: str = os.getenv("VOICE_PROVIDER", "google")

    # 1. Bhashini Credentials & Audio Quality (Primary)
    bhashini_user_id: Optional[str] = os.getenv("BHASHINI_USER_ID", "")
    bhashini_api_key: Optional[str] = os.getenv("BHASHINI_API_KEY", "")
    bhashini_pipeline_id: Optional[str] = os.getenv("BHASHINI_PIPELINE_ID", "")
    bhashini_audio_format: str = os.getenv("BHASHINI_AUDIO_FORMAT", "mp3")  # "mp3", "wav", "flac", "ogg", "aac"
    bhashini_sampling_rate: int = int(os.getenv("BHASHINI_SAMPLING_RATE", "22050"))  # 22050, 44100, 16000

    # 2. Sarvam AI Credentials
    sarvam_api_key: Optional[str] = os.getenv("SARVAM_API_KEY", "")

    # 3. Google Cloud Credentials
    google_speech_api_key: Optional[str] = os.getenv("GOOGLE_SPEECH_API_KEY", "")

    # 4. Azure Cognitive Services Speech Credentials
    azure_speech_key: Optional[str] = os.getenv("AZURE_SPEECH_KEY", "")
    azure_speech_region: Optional[str] = os.getenv("AZURE_SPEECH_REGION", "centralindia")

    # Supported Native Indian Languages (Bhashini National Language Mission)
    supported_languages: dict = {
        "ml": {"name": "മലയാളം", "code": "ml-IN", "english_name": "Malayalam"},
        "hi": {"name": "हिन्दी", "code": "hi-IN", "english_name": "Hindi"},
        "ta": {"name": "தமிழ்", "code": "ta-IN", "english_name": "Tamil"},
        "te": {"name": "తెలుగు", "code": "te-IN", "english_name": "Telugu"},
        "kn": {"name": "ಕನ್ನಡ", "code": "kn-IN", "english_name": "Kannada"},
        "bn": {"name": "বাংলা", "code": "bn-IN", "english_name": "Bengali"},
        "mr": {"name": "मराठी", "code": "mr-IN", "english_name": "Marathi"},
        "gu": {"name": "ગુજરાતી", "code": "gu-IN", "english_name": "Gujarati"},
        "pa": {"name": "ਪੰਜਾਬੀ", "code": "pa-IN", "english_name": "Punjabi"},
        "or": {"name": "ଓଡ଼ିଆ", "code": "or-IN", "english_name": "Odia"},
        "as": {"name": "অসমীয়া", "code": "as-IN", "english_name": "Assamese"},
        "ur": {"name": "اردو", "code": "ur-IN", "english_name": "Urdu"},
        "en": {"name": "English", "code": "en-IN", "english_name": "English"}
    }

    def get_voice_info(self) -> dict:
        return {
            "active_provider": self.voice_provider.lower().strip(),
            "supported_providers": ["bhashini", "sarvam", "google", "azure", "browser"],
            "bhashini_audio_format": self.bhashini_audio_format,
            "bhashini_sampling_rate": self.bhashini_sampling_rate,
            "has_bhashini_credentials": bool(self.bhashini_user_id and self.bhashini_api_key),
            "has_sarvam_credentials": bool(self.sarvam_api_key),
            "has_google_credentials": bool(self.google_speech_api_key),
            "has_azure_credentials": bool(self.azure_speech_key),
            "supported_languages_count": len(self.supported_languages)
        }

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
