import tensorflow as tf
import numpy as np
from transformers import pipeline
from core.config import Config

class KnowledgeBase:
    def __init__(self):
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        self.qa_pipeline = pipeline('question-answering')
        self.summarizer = pipeline('summarization')
        self.initialize_local_model()

    def initialize_local_model(self):
        # Create a simple neural network for local processing
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='softmax')
        ])
        
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(Config.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

    async def learn_from_interaction(self, user_input, response, context):
        """Process and learn from each interaction"""
        try:
            # Analyze sentiment
            sentiment = self.sentiment_analyzer(user_input)
            
            # Generate summary
            summary = self.summarizer(user_input, max_length=50, min_length=10)
            
            # Store learning data
            learning_data = {
                'input': user_input,
                'response': response,
                'context': context,
                'sentiment': sentiment,
                'summary': summary
            }
            
            return learning_data
            
        except Exception as e:
            print(f"Learning error: {str(e)}")
            return None
