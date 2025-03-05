// js/api.js
class API {
    constructor(config) {
        this.config = config;
        this.ws = null;
        this.messageQueue = [];
        this.isConnected = false;
    }

    async connect() {
        try {
            this.ws = new WebSocket(this.config.wsUrl);
            
            this.ws.onopen = () => {
                this.isConnected = true;
                this.processQueue();
            };

            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleResponse(data);
            };

            this.ws.onclose = () => {
                this.isConnected = false;
                setTimeout(() => this.connect(), 5000); // Reconnect after 5 seconds
            };

        } catch (error) {
            console.error('WebSocket connection error:', error);
        }
    }

    async sendMessage(message) {
        try {
            if (!this.isConnected) {
                this.messageQueue.push(message);
                return;
            }

            const data = {
                message: message,
                timestamp: new Date().toISOString()
            };

            this.ws.send(JSON.stringify(data));

        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    async processQueue() {
        while (this.messageQueue.length > 0 && this.isConnected) {
            const message = this.messageQueue.shift();
            await this.sendMessage(message);
        }
    }

    handleResponse(data) {
        // Dispatch custom event with response
        const event = new CustomEvent('ai-response', { detail: data });
        document.dispatchEvent(event);
    }

    async fallbackHttpRequest(message) {
        try {
            const response = await fetch(`${this.config.apiUrl}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: message })
            });

            if (!response.ok) {
                throw new Error('HTTP request failed');
            }

            return await response.json();

        } catch (error) {
            console.error('HTTP request error:', error);
            throw error;
        }
    }
}
