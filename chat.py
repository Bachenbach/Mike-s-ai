# app/routes/chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process the message
            response = await process_message(data, client_id)
            
            # Send response back to client
            await manager.send_message(json.dumps(response), client_id)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)

async def process_message(data: str, client_id: str):
    """Process incoming message and generate response"""
    try:
        # Parse incoming data
        message_data = json.loads(data)
        user_input = message_data.get('message', '')
        
        # Process with NLP
        nlp_analysis = await language_processor.process_text(user_input)
        
        # Get AI response
        ai_response = await api_orchestrator.process_query(user_input)
        
        # Update context
        context = await context_manager.update_context(
            user_input, 
            ai_response, 
            nlp_analysis
        )
        
        return {
            'status': 'success',
            'response': ai_response,
            'nlp_analysis': nlp_analysis,
            'context': context
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
