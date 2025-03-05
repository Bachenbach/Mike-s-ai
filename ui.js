// js/ui.js
class UI {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.userInput = document.getElementById('userInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.loadingSpinner = document.getElementById('loadingSpinner');
        
        this.setupEventListeners();
        this.setupTheme();
    }

    setupEventListeners() {
        // Auto-resize textarea
        this.userInput.addEventListener('input', () => {
            this.userInput.style.height = 'auto';
            this.userInput.style.height = this.userInput.scrollHeight + 'px';
        });

        // Settings modal
        document.getElementById('settingsBtn').addEventListener('click', () => {
            document.getElementById('settingsModal').style.display = 'block';
        });

        document.querySelector('.close-btn').addEventListener('click', () => {
            document.getElementById('settingsModal').style.display = 'none';
        });

        // Theme selection
        document.getElementById('themeSelect').addEventListener('change', (e) => {
            this.setTheme(e.target.value);
        });
    }

    setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    addMessage(message, isAi = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isAi ? 'ai-message' : 'user-message'}`;
        
        // Process markdown and code blocks
        const formattedMessage = this.formatMessage(message);
        messageDiv.innerHTML = formattedMessage;
        
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(message) {
        // Basic markdown processing
        let formatted = message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');

        // Code block processing
        formatted = formatted.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, language, code) => {
            return `<pre><code class="language-${language || 'plaintext'}">${this.escapeHtml(code.trim())}</code></pre>`;
        });

        return formatted;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    showLoading() {
        this.loadingSpinner.classList.remove('hidden');
    }

    hideLoading() {
        this.loadingSpinner.classList.add('hidden');
    }

    clearInput() {
        this.userInput.value = '';
        this.userInput.style.height = 'auto';
    }
}
