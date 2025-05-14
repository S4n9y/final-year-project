    function sendMessage() {
      const userMessage = document.getElementById('userMessage').value;
      if (userMessage.trim() !== "") {
        const chatbotResponse = getChatbotResponse(userMessage);
        displayMessage(userMessage, 'user');
        displayMessage(chatbotResponse, 'bot');
      }
      document.getElementById('userMessage').value = "";
    }

    function displayMessage(message, sender) {
      const chatboxBody = document.querySelector('.chatbox-body');
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('chatbot-message');
      if (sender === 'user') {
        messageDiv.classList.add('user-message');
        messageDiv.textContent = `You: ${message}`;
      } else {
        messageDiv.classList.add('bot-message');
        messageDiv.textContent = `Bot: ${message}`;
      }
      chatboxBody.appendChild(messageDiv);
      chatboxBody.scrollTop = chatboxBody.scrollHeight; // Scroll to bottom
    }

    function getChatbotResponse(message) {
      const lowerMessage = message.toLowerCase();

      // Basic responses
      if (lowerMessage.includes("weather")) {
        return "I can fetch the latest weather updates for your farm location. 🌤️";
      } else if (lowerMessage.includes("pests")) {
        return "For pests, use natural remedies like neem oil or consult your local agricultural extension officer. 🐜";
      } else if (lowerMessage.includes("market price")) {
        return "I can provide the latest market prices for your crops. 📊";
      } else {
        return "Sorry, I didn't quite get that. Can you ask something else about farming? 🌱";
      }
    } 