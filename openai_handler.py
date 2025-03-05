# core/api_integration/openai_handler.py
import openai
from core.config import Config
import asyncio
import json

class OpenAIHandler:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"  # or "gpt-4" if you have access

    async def generate_response(self, user_input, context=None):
        try:
            # Prepare conversation history
            messages = self._prepare_messages(user_input, context)
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                presence_penalty=0.6,
                frequency_penalty=0.0
            )
            
            # Store conversation
            self._update_conversation_history(user_input, response.choices[0].message['content'])
            
            return {
                'response': response.choices[0].message['content'],
                'usage': response.usage,
                'model': self.model
            }
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return None

    def _prepare_messages(self, user_input, context):
        messages = [
            {"role": "system", "content": "You are an advanced AI assistant with access to multiple AI services and real-time information."}
        ]
        
        # Add context if available
        if context:
            messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
        
        # Add conversation history
        for conv in self.conversation_history[-5:]:  # Last 5 conversations
            messages.append({"role": "user", "content": conv["user"]})
            messages.append({"role": "assistant", "content": conv["assistant"]})
            
        # Add current input
        messages.append({"role": "user", "content": user_input})
        
        return messages

    def _update_conversation_history(self, user_input, response):
        self.conversation_history.append({
            "user": user_input,
            "assistant": response
        })
        if len(self.conversation_history) > 20:  # Keep last 20 conversations
            self.conversation_history.pop(0)
