from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "dev"

    wakeword_model_path: str = ""
    wakeword_threshold: float = 0.55

    vad_primary: str = "silero"
    vad_fallback: str = "webrtc"
    vad_energy_threshold: int = 500

    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_stt_model: str = "whisper-large-v3-turbo"
    stt_local_model: str = "base"

    edge_tts_voice: str = "en-US-AndrewMultilingualNeural"
    piper_exe: str = ""
    piper_model_path: str = ""


settings = Settings()

