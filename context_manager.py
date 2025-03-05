# core/nlp/context_manager.py
from collections import deque
import numpy as np
from datetime import datetime, timedelta

class ContextManager:
    def __init__(self, max_history=10):
        self.context_history = deque(maxlen=max_history)
        self.topic_tracking = {}
        self.user_preferences = {}
        self.conversation_state = {
            'current_topic': None,
            'open_questions': [],
            'last_update': datetime.now()
        }

    async def update_context(self, user_input, ai_response, nlp_analysis):
        """Update conversation context with new interaction"""
        context_entry = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'ai_response': ai_response,
            'nlp_analysis': nlp_analysis,
            'topic': self._extract_topic(nlp_analysis)
        }
        
        self.context_history.append(context_entry)
        self._update_topic_tracking(context_entry)
        self._update_conversation_state(context_entry)
        
        return self.get_current_context()

    def get_current_context(self):
        """Get relevant context for current conversation"""
        return {
            'recent_history': list(self.context_history),
            'current_topic': self.conversation_state['current_topic'],
            'topic_history': self.topic_tracking,
            'open_questions': self.conversation_state['open_questions']
        }

    def _extract_topic(self, nlp_analysis):
        """Extract main topic from NLP analysis"""
        if 'entities' in nlp_analysis:
            # Prioritize named entities
            entities = nlp_analysis['entities']
            if entities:
                return max(entities, key=lambda x: len(x['text']))['text']
                
        if 'semantics' in nlp_analysis:
            # Fall back to key phrases
            phrases = nlp_analysis['semantics'].get('key_phrases', [])
            if phrases:
                return max(phrases, key=lambda x: x['importance_score'])['text']
                
        return None

    def _update_topic_tracking(self, context_entry):
        """Track topic evolution and persistence"""
        topic = context_entry['topic']
        if topic:
            if topic not in self.topic_tracking:
                self.topic_tracking[topic] = {
                    'first_mention': context_entry['timestamp'],
                    'last_mention': context_entry['timestamp'],
                    'mention_count': 1
                }
            else:
                self.topic_tracking[topic]['last_mention'] = context_entry['timestamp']
                self.topic_tracking[topic]['mention_count'] += 1

    def _update_conversation_state(self, context_entry):
        """Update current conversation state"""
        self.conversation_state['last_update'] = context_entry['timestamp']
        
        # Update current topic if it's significant
        if context_entry['topic']:
            self.conversation_state['current_topic'] = context_entry['topic']
            
        # Track questions
        if '?' in context_entry['user_input']:
            self.conversation_state['open_questions'].append({
                'question': context_entry['user_input'],
                'timestamp': context_entry['timestamp']
            })
