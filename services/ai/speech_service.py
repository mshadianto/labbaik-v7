"""
LABBAIK AI - Speech Services
=============================
- Speech-to-Text: Groq Whisper API
- Text-to-Speech: Edge TTS (Microsoft)
"""

import os
import io
import asyncio
import logging
import tempfile
from typing import Optional
from groq import Groq

logger = logging.getLogger(__name__)

# Try to import edge-tts
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False
    logger.warning("edge-tts not installed. TTS will be disabled.")

# Indonesian voice options (Edge TTS - Microsoft Neural Voices)
TTS_VOICES = {
    "id_female": "id-ID-GadisNeural",      # Indonesian Female (recommended)
    "id_male": "id-ID-ArdiNeural",         # Indonesian Male
    "ar_female": "ar-SA-ZariyahNeural",    # Arabic Female
    "ar_male": "ar-SA-HamedNeural",        # Arabic Male
}

DEFAULT_TTS_VOICE = "id_female"


class SpeechService:
    """Speech-to-text service using Groq Whisper API."""

    DEFAULT_MODEL = "whisper-large-v3-turbo"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize speech service.

        Args:
            api_key: Groq API key (uses GROQ_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self._client = None

    @property
    def client(self) -> Groq:
        """Lazy-initialize Groq client."""
        if self._client is None:
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not configured")
            self._client = Groq(api_key=self.api_key)
        return self._client

    def transcribe(
        self,
        audio_bytes: bytes,
        language: str = "id",
        filename: str = "audio.wav"
    ) -> str:
        """Transcribe audio to text.

        Args:
            audio_bytes: Raw audio data
            language: Language code (id=Indonesian, ar=Arabic, en=English)
            filename: Filename hint for format detection

        Returns:
            Transcribed text
        """
        if not audio_bytes:
            return ""

        try:
            # Write audio to temp file (Groq requires file path)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_bytes)
                temp_path = f.name

            # Transcribe using Groq Whisper
            with open(temp_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=(filename, audio_file.read()),
                    model=self.DEFAULT_MODEL,
                    language=language,
                    response_format="text",
                )

            # Cleanup temp file
            try:
                os.unlink(temp_path)
            except Exception:
                pass

            result = transcription.strip() if isinstance(transcription, str) else str(transcription).strip()
            logger.info(f"Transcribed {len(audio_bytes)} bytes -> {len(result)} chars")
            return result

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise


# Singleton instance
_speech_service: Optional[SpeechService] = None


def get_speech_service() -> SpeechService:
    """Get singleton speech service instance."""
    global _speech_service
    if _speech_service is None:
        _speech_service = SpeechService()
    return _speech_service


def transcribe_audio(audio_bytes: bytes, language: str = "id") -> str:
    """Convenience function to transcribe audio.

    Args:
        audio_bytes: Raw audio data
        language: Language code (id=Indonesian, ar=Arabic, en=English)

    Returns:
        Transcribed text
    """
    service = get_speech_service()
    return service.transcribe(audio_bytes, language=language)


# =============================================================================
# TEXT-TO-SPEECH (TTS)
# =============================================================================

def text_to_speech(
    text: str,
    voice: str = DEFAULT_TTS_VOICE,
    rate: str = "+0%"
) -> Optional[bytes]:
    """Convert text to speech audio.

    Args:
        text: Text to convert to speech
        voice: Voice ID (id_female, id_male, ar_female, ar_male)
        rate: Speech rate adjustment (e.g., "-10%", "+10%")

    Returns:
        Audio bytes (MP3 format) or None if TTS unavailable
    """
    if not HAS_EDGE_TTS:
        logger.warning("edge-tts not available")
        return None

    if not text or not text.strip():
        return None

    # Clean text for TTS (remove markdown, emojis that might cause issues)
    clean_text = _clean_text_for_tts(text)
    if not clean_text:
        return None

    voice_id = TTS_VOICES.get(voice, TTS_VOICES[DEFAULT_TTS_VOICE])

    try:
        # Run async TTS in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            audio_bytes = loop.run_until_complete(
                _generate_tts_audio(clean_text, voice_id, rate)
            )
            return audio_bytes
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        return None


async def _generate_tts_audio(text: str, voice_id: str, rate: str) -> bytes:
    """Generate TTS audio using edge-tts (async)."""
    communicate = edge_tts.Communicate(text, voice_id, rate=rate)
    audio_buffer = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])

    audio_buffer.seek(0)
    return audio_buffer.read()


def _clean_text_for_tts(text: str) -> str:
    """Clean text for TTS (remove markdown, code blocks, etc.)."""
    import re

    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)

    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)

    # Remove markdown links [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Remove bullet points
    text = re.sub(r'^[\-\*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Remove extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    # Limit length for TTS (avoid very long audio)
    max_chars = 2000
    if len(text) > max_chars:
        text = text[:max_chars] + "..."

    return text


def is_tts_available() -> bool:
    """Check if TTS is available."""
    return HAS_EDGE_TTS
