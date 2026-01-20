import time
import wave
import audioop
import os
import uuid
import logging

logger = logging.getLogger(__name__)

class AudioRecorder:
    def __init__(self, user_id, save_dir="./data/temp"):
        self.user_id = user_id
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            
        self.buffer = bytearray()
        self.last_packet_time = time.time()
        self.silence_start_time = None
        self.is_speaking = False
        
        # Audio params
        self.CHANNELS = 2
        self.SAMPLE_WIDTH = 2 # 16-bit
        self.RATE = 48000
        self.BYTES_PER_SEC = self.RATE * self.CHANNELS * self.SAMPLE_WIDTH
        
        # VAD Config
        # RMS threshold is tricky. 300-500 is usually background noise.
        # This might need tuning.
        self.SILENCE_THRESHOLD = 500 
        self.SILENCE_DURATION = 1.0 # Seconds of silence to trigger 'End of Sentence'
        self.MIN_DURATION = 1.0 # Minimum seconds to consider valid speech
        self.MAX_DURATION = 20.0 # Force flush if too long (20s)

    def write(self, pcm_data):
        """
        Write raw PCM data to buffer.
        Returns a file path if a complete utterance is detected and saved.
        """
        self.buffer.extend(pcm_data)
        self.last_packet_time = time.time()
        
        # Calculate RMS for VAD
        try:
            rms = audioop.rms(pcm_data, self.SAMPLE_WIDTH)
        except Exception:
            rms = 0
        
        if rms > self.SILENCE_THRESHOLD:
            if not self.is_speaking:
                # Speech started
                self.is_speaking = True
                # logger.debug(f"User {self.user_id} started speaking.")
            self.silence_start_time = None
        else:
            if self.is_speaking:
                if self.silence_start_time is None:
                    self.silence_start_time = time.time()
        
        return self.check_flush()

    def check_flush(self):
        """
        Check if we should flush the buffer to a file.
        Returns path if flushed, None otherwise.
        """
        current_time = time.time()
        
        # Check max duration
        buffer_duration = len(self.buffer) / self.BYTES_PER_SEC
        if buffer_duration > self.MAX_DURATION:
            return self._flush()

        if not self.is_speaking:
             # Cleanup old buffer if valid timeout
             if len(self.buffer) > 0 and (current_time - self.last_packet_time > 5.0):
                 self.buffer.clear()
             return None

        # Logic: Speaking started, checking for silence closure
        if self.silence_start_time and (current_time - self.silence_start_time > self.SILENCE_DURATION):
            # Silence detected long enough
            if buffer_duration < self.MIN_DURATION:
                # Too short, discard (probably cough or click)
                self.buffer.clear()
                self.is_speaking = False
                self.silence_start_time = None
                return None
            
            # Valid utterance
            return self._flush()
            
        return None

    def _flush(self):
        filename = f"{self.user_id}_{int(time.time()*1000)}_{str(uuid.uuid4())[:4]}.wav"
        path = os.path.join(self.save_dir, filename)
        
        try:
            # Create a mono version for Whisper if possible, but for raw PCM dump we might just dump stereo.
            # Audioop.tomono requires width, left_factor, right_factor.
            # Simple averaging: 0.5, 0.5
            mono_data = audioop.tomono(self.buffer, self.SAMPLE_WIDTH, 0.5, 0.5)

            with wave.open(path, 'wb') as wf:
                wf.setnchannels(1) # Saving as Mono
                wf.setsampwidth(self.SAMPLE_WIDTH)
                wf.setframerate(self.RATE)
                wf.writeframes(mono_data)
            
            logger.info(f"Saved audio: {path} (Duration: {len(self.buffer)/self.BYTES_PER_SEC:.2f}s, Mono)")
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            path = None

        self.cleanup()
        return path

    def cleanup(self):
        """
        Release resources/reset state.
        """
        self.buffer.clear()
        self.is_speaking = False
        self.silence_start_time = None
