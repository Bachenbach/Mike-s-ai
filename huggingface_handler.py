# core/api_integration/huggingface_handler.py
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

class HuggingFaceHandler:
    def __init__(self):
        self.initialize_pipelines()
        
    def initialize_pipelines(self):
        """Initialize various HuggingFace pipelines"""
        try:
            # Text Generation
            self.text_generator = pipeline(
                "text-generation",
                model="gpt2",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Text Classification
            self.classifier = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            # Named Entity Recognition
            self.ner = pipeline(
                "ner",
                aggregation_strategy="simple"
            )
            
            # Question Answering
            self.qa = pipeline("question-answering")
            
        except Exception as e:
            print(f"Error initializing HuggingFace pipelines: {str(e)}")

    async def process_text(self, text, task="generate"):
        """Process text using various pipelines"""
        try:
            if task == "generate":
                return await self._generate_text(text)
            elif task == "classify":
                return await self._classify_text(text)
            elif task == "ner":
                return await self._extract_entities(text)
            elif task == "qa":
                return await self._answer_question(text)
            else:
                raise ValueError(f"Unknown task: {task}")
                
        except Exception as e:
            print(f"HuggingFace processing error: {str(e)}")
            return None

    async def _generate_text(self, prompt):
        """Generate text continuation"""
        try:
            response = self.text_generator(
                prompt,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7
            )
            return response[0]['generated_text']
        except Exception as e:
            print(f"Text generation error: {str(e)}")
            return None

    async def _classify_text(self, text):
        """Classify text sentiment"""
        return self.classifier(text)

    async def _extract_entities(self, text):
        """Extract named entities"""
        return self.ner(text)

    async def _answer_question(self, context, question):
        """Answer questions based on context"""
        return self.qa(question=question, context=context)
