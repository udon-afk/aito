import requests
import logging
import json
from ..config import OLLAMA_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.system_prompt = "あなたは「ミリア」という名前の妹キャラクターです。兄（ユーザー）と仲良く会話してください。返答は短めに、感情豊かに。"
        # Initialize history with system prompt
        self.history = [{"role": "system", "content": self.system_prompt}]

    def generate(self, prompt: str, user_id=None, context_docs=None) -> str:
        """
        Generate a response from Ollama (Chat API).
        :param prompt: User input text
        :param user_id: Ideally maintain history per user (Currently simple global history for demo)
        :param context_docs: RAG context strings
        """
        
        # Add context to the prompt if available
        user_content = prompt
        if context_docs:
            user_content = f"Context:\n{context_docs}\n\nUser: {prompt}"

        # Append user message
        self.history.append({"role": "user", "content": user_content})

        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": False
        }
        
        try:
            resp = requests.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            # Extract response
            ai_message = data.get("message", {})
            ai_text = ai_message.get("content", "")
            
            # Append AI response to history
            if ai_text:
                self.history.append({"role": "assistant", "content": ai_text})
                
            return ai_text
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "ごめんね、ちょっと頭が回らないみたい..."

    def clear_history(self):
        self.history = [{"role": "system", "content": self.system_prompt}]
