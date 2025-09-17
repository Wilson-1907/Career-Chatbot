/**
 * Chat API Client for CBE Career Guide
 * Handles communication with the FastAPI backend
 */

class ChatAPI {
    constructor(baseURL = 'http://127.0.0.1:8000', authToken = null) {
        this.baseURL = baseURL;
        this.authToken = authToken;
    }

    /**
     * Set authentication token
     */
    setAuthToken(token) {
        this.authToken = token;
    }

    /**
     * Get headers for API requests
     */
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        return headers;
    }

    /**
     * Send a single chat message
     */
    async sendMessage(message, language = 'en', userContext = null) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    message: message,
                    language: language,
                    user_context: userContext
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    /**
     * Send a message with conversation history
     */
    async sendMessageWithHistory(messages, language = 'en') {
        try {
            const response = await fetch(`${this.baseURL}/chat/history`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    messages: messages,
                    language: language
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending message with history:', error);
            throw error;
        }
    }

    /**
     * Get CBE pathways information
     */
    async getPathways() {
        try {
            const response = await fetch(`${this.baseURL}/pathways`, {
                method: 'GET',
                headers: this.getHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting pathways:', error);
            throw error;
        }
    }

    /**
     * Get careers for a specific pathway
     */
    async getCareers(pathway) {
        try {
            const response = await fetch(`${this.baseURL}/careers/${pathway}`, {
                method: 'GET',
                headers: this.getHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting careers:', error);
            throw error;
        }
    }

    /**
     * Check API health
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/health`, {
                method: 'GET',
                headers: this.getHeaders()
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error checking health:', error);
            throw error;
        }
    }
}

/**
 * Chat Manager - Handles chat UI and conversation flow
 */
class ChatManager {
    constructor(apiBaseURL = 'http://127.0.0.1:8000') {
        this.api = new ChatAPI(apiBaseURL);
        this.conversationHistory = [];
        this.currentLanguage = 'en';
        this.userContext = null;
        this.isTyping = false;
    }

    /**
     * Initialize chat manager
     */
    async initialize(authToken = null) {
        if (authToken) {
            this.api.setAuthToken(authToken);
        }

        // Check if backend is available
        try {
            await this.api.checkHealth();
            console.log('Chat API is healthy');
        } catch (error) {
            console.warn('Chat API is not available:', error);
            this.showError('Chat service is currently unavailable. Please try again later.');
        }
    }

    /**
     * Set user context for personalized responses
     */
    setUserContext(context) {
        this.userContext = context;
    }

    /**
     * Set language for responses
     */
    setLanguage(language) {
        this.currentLanguage = language;
    }

    /**
     * Send a message and handle the response
     */
    async sendMessage(message) {
        if (this.isTyping) {
            return;
        }

        this.isTyping = true;
        this.addMessageToUI(message, 'user');
        this.showTypingIndicator();

        try {
            let response;

            if (this.conversationHistory.length > 0) {
                // Send with history for context
                const messages = [
                    ...this.conversationHistory,
                    { role: 'user', content: message }
                ];
                response = await this.api.sendMessageWithHistory(messages, this.currentLanguage);
            } else {
                // Send single message
                response = await this.api.sendMessage(message, this.currentLanguage, this.userContext);
            }

            // Add to conversation history
            this.conversationHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: response.response }
            );

            // Keep only last 20 messages for performance
            if (this.conversationHistory.length > 20) {
                this.conversationHistory = this.conversationHistory.slice(-20);
            }

            this.hideTypingIndicator();
            this.addMessageToUI(response.response, 'assistant');

        } catch (error) {
            this.hideTypingIndicator();
            this.showError('Sorry, I encountered an error. Please try again.');
            console.error('Chat error:', error);
        } finally {
            this.isTyping = false;
        }
    }

    /**
     * Add message to UI (implement based on your UI framework)
     */
    addMessageToUI(message, role) {
        // This should be implemented based on your specific UI
        console.log(`${role}: ${message}`);

        // Example implementation for a chat container
        const chatContainer = document.getElementById('chatMessages');
        if (chatContainer) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p>${this.formatMessage(message)}</p>
                    <small class="timestamp">${new Date().toLocaleTimeString()}</small>
                </div>
            `;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.style.display = 'block';
        }
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        this.addMessageToUI(`Error: ${message}`, 'system');
    }

    /**
     * Format message for display
     */
    formatMessage(message) {
        // Basic formatting - convert line breaks to <br>
        return message.replace(/\n/g, '<br>');
    }

    /**
     * Clear conversation
     */
    clearConversation() {
        this.conversationHistory = [];
        const chatContainer = document.getElementById('chatMessages');
        if (chatContainer) {
            chatContainer.innerHTML = '';
        }
    }

    /**
     * Get pathway information
     */
    async getPathwayInfo() {
        try {
            return await this.api.getPathways();
        } catch (error) {
            console.error('Error getting pathway info:', error);
            return null;
        }
    }

    /**
     * Get career information for a pathway
     */
    async getCareerInfo(pathway) {
        try {
            return await this.api.getCareers(pathway);
        } catch (error) {
            console.error('Error getting career info:', error);
            return null;
        }
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChatAPI, ChatManager };
} else {
    window.ChatAPI = ChatAPI;
    window.ChatManager = ChatManager;
}