# core/api_integration/api_orchestrator.py
from .openai_handler import OpenAIHandler
from .huggingface_handler import HuggingFaceHandler
from core.database.mongodb_handler import MongoDBHandler
from core.search.google_search import GoogleSearchEngine

class APIOrchestrator:
    def __init__(self):
        self.openai = OpenAIHandler()
        self.huggingface = HuggingFaceHandler()
        self.db = MongoDBHandler()
        self.search = GoogleSearchEngine()

    async def process_query(self, user_input):
        try:
            # 1. Search for relevant information
            search_results = await self.search.search(user_input)
            
            # 2. Get context from database
            db_context = self.db.get_relevant_context(user_input)
            
            # 3. Combine context
            context = {
                "search_results": search_results,
                "database_context": db_context
            }
            
            # 4. Generate main response using OpenAI
            main_response = await self.openai.generate_response(
                user_input,
                context=context
            )
            
            # 5. Enhance with HuggingFace processing
            enhancements = await self._enhance_response(user_input, main_response)
            
            # 6. Store interaction
            self._store_interaction(user_input, main_response, enhancements)
            
            return {
                "main_response": main_response,
                "enhancements": enhancements,
                "context": context
            }
            
        except Exception as e:
            print(f"Orchestration error: {str(e)}")
            return None

    async def _enhance_response(self, user_input, main_response):
        """Enhance the main response with additional processing"""
        return {
            "sentiment": await self.huggingface.process_text(user_input, "classify"),
            "entities": await self.huggingface.process_text(user_input, "ner"),
            "generated_continuation": await self.huggingface.process_text(
                main_response['response'], 
                "generate"
            )
        }

    def _store_interaction(self, user_input, response, enhancements):
        """Store the interaction in the database"""
        interaction_data = {
            "user_input": user_input,
            "response": response,
            "enhancements": enhancements,
            "timestamp": datetime.now()
        }
        self.db.store_conversation(interaction_data)
