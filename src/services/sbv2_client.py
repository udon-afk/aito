import requests
import logging
import os
import uuid
from ..config import SBV2_URL

logger = logging.getLogger(__name__)

class SBV2Client:
    def __init__(self):
        self.base_url = SBV2_URL
        # Model ID or Style ID might be needed depending on SBV2 setup.
        # Assuming defaults or a specific model loaded in the server.
        self.model_id = 0 
        self.speaker_id = 0
    
    def tts(self, text: str, save_dir="./data/temp") -> str:
        """
        Convert text to speech.
        Returns path to saved .wav file.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        params = {
            "text": text,
            "model_id": self.model_id,
            "speaker_id": self.speaker_id,
            "sdp_ratio": 0.2,
            "noise": 0.6,
            "noise_w": 0.8,
            "length": 1.0,
            "language": "JP",
            "auto_split": "true",
            "split_interval": 0.5,
            "assist_text_weight": 1.0,
            "style": "Neutral",
            "style_weight": 5.0
        }

            # Note: The endpoint depends on the implementation of Style-Bert-VITS2 API.
            # Common one is /voice
            resp = requests.get(f"{self.base_url}/voice", params=params)
             # If it returns audio bytes directly
            if resp.status_code == 200:
                filename = f"tts_{uuid.uuid4().hex}.wav"
                path = os.path.join(save_dir, filename)
                with open(path, "wb") as f:
                    f.write(resp.content)
                return path
            else:
                logger.error(f"SBV2 TTS failed: {resp.status_code} {resp.text}")
                return None
        except Exception as e:
            logger.error(f"SBV2 connection failed: {e}")
            return None
