from faster_whisper import WhisperModel
import os
import logging
from ..config import WHISPER_MODEL_SIZE

logger = logging.getLogger(__name__)

class STTEngine:
    def __init__(self, model_size=None, device="cuda", compute_type="float16"):
        """
        Initialize the faster-whisper model.
        :param model_size: Size of the model (tiny, base, small, medium, large-v2, etc.)
        :param device: 'cuda' or 'cpu'
        :param compute_type: 'float16' for GPU, 'int8' for CPU usually
        """
        self.model_size = model_size if model_size else WHISPER_MODEL_SIZE
        self.device = device
        self.compute_type = compute_type
        
        logger.info(f"Loading Whisper model: {self.model_size} on {self.device}...")
        try:
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            logger.info("Whisper model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            # Fallback to CPU if CUDA fails? Or just raise.
            # For now, let's try to fallback to CPU int8 if CUDA fails
            if device == "cuda":
                logger.warning("Attempting fallback to CPU (int8)...")
                self.device = "cpu"
                self.compute_type = "int8"
                self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
                logger.info("Whisper model loaded on CPU.")
            else:
                raise e

    def transcribe(self, audio_path: str, language="ja"):
        """
        Transcribe the audio file.
        :param audio_path: Path to the .wav file
        :param language: Language code (default 'ja')
        :return: Transcribed text
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return ""

        # vad_filter=True prevents hallucinations on silence
        # initial_prompt guides the context
        segments, info = self.model.transcribe(
            audio_path, 
            beam_size=5, 
            language=language,
            vad_filter=True,
            initial_prompt="これは、妹のミリアと兄の会話です。"
        )
        
        # segments is a generator, so we need to iterate to get results
        text = ""
        for segment in segments:
            text += segment.text
        
        return text.strip()

if __name__ == "__main__":
    # Simple test
    logging.basicConfig(level=logging.INFO)
    try:
        engine = STTEngine(model_size="tiny", device="cpu", compute_type="int8")
        print("Model initialized. Ready to transcribe.")
    except Exception as e:
        print(f"Error: {e}")
