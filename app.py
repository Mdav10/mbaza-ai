from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# ============ KIRUNDI VOCABULARY (English -> Kirundi) ============
WORDS = {
    # Greetings
    "good morning": "Mwaramutse",
    "good evening": "Mwiriwe",
    "how are you": "Uraho",
    "i am fine": "Ni meza",
    "goodbye": "Ndakugana",
    "thank you": "Murakoze",
    "welcome": "Urakaza neza",
    "hello": "Mwaramutse",
    "bye": "Ndakugana",
    "thanks": "Murakoze",
    
    # People
    "person": "umuntu",
    "people": "abantu",
    "woman": "umugore",
    "man": "umugabo",
    "child": "umwana",
    "girl": "umukobwa",
    "boy": "umuhungu",
    
    # Family
    "father": "data",
    "mother": "mama",
    "uncle": "mwene data",
    "aunt": "mwene mama",
    "sister": "mushiki",
    "brother": "mukuru",
    
    # Animals
    "cow": "inka",
    "dog": "imbwa",
    "cat": "injata",
    "chicken": "inkoko",
    "horse": "ifarashi",
    
    # Food
    "milk": "amata",
    "rice": "umuceri",
    "meat": "inyama",
    "eggs": "amagi",
    "water": "amazi",
    "bananas": "ibitoki",
    
    # Places
    "school": "ishuri",
    "church": "itorero",
    "market": "isoko",
    "hospital": "ibitaro",
    "home": "urugo",
    
    # Verbs
    "eat": "kurya",
    "drink": "kunywa",
    "sleep": "kuryama",
    "work": "gukora",
    "play": "gukina",
    "read": "gusoma",
    "write": "kwandika",
    "go": "kugenda",
    "come": "kuza",
    "see": "kubona",
    "love": "gukunda",
    
    # Adjectives
    "big": "nini",
    "small": "to",
    "tall": "muremure",
    "short": "gufi",
    "bad": "mubi",
    "good": "neza",
    "fast": "vuba",
    "slow": "buhoro",
    
    # Numbers
    "one": "rimwe",
    "two": "kabiri",
    "three": "gatatu",
    "four": "kane",
    "five": "gatanu",
    "ten": "icumi",
    
    # Time
    "day": "umunsi",
    "night": "ijoro",
    "hour": "isaha",
    "week": "icyumweru",
    "month": "ukwezi",
    "year": "umwaka",
    
    # Body
    "head": "umutwe",
    "eyes": "amaso",
    "ears": "amatwi",
    "nose": "izuru",
    "mouth": "umunwa",
}

# ============ KIRUNDI TO ENGLISH ============
WORDS_REVERSE = {v: k for k, v in WORDS.items()}

# ============ GRAMMAR RULES ============
GRAMMAR_RULES = {
    "present tense": "Use 'nda' for I, 'ura' for you, 'ara' for he/she. Example: Ndakora = I work",
    "past tense": "Use 'nara' for I, 'wara' for you, 'yara' for he/she. Example: Narakora = I worked",
    "future tense": "Use 'nza' for I, 'uza' for you, 'aza' for he/she. Example: Nzakora = I will work",
    "noun class 1": "People: umu- (singular) becomes aba- (plural). Umuntu = person, Abantu = people",
    "negative": "Add 'nti' before the verb. Example: Ntikora = I don't work",
}

# ============ CONVERSATION RESPONSES ============
RESPONSES = {
    "greeting": [
        "Mwaramutse! Good morning! How can I help you learn Kirundi?",
        "Hello! Welcome to Mbaza AI. Say 'how are you' in Kirundi?",
        "Mwaramutse! Are you ready to learn Kirundi today?"
    ],
    "how_are_you": [
        "Ni meza! I am fine. Thank you for asking. Say 'Uraho' to ask someone how they are.",
        "I am good! 'Ni meza' means I am fine. Would you like to learn more greetings?"
    ],
    "thanks": [
        "Murakoze! You're welcome! Keep learning Kirundi with me.",
        "Urakaza neza! That means welcome. Let's continue learning!"
    ],
    "goodbye": [
        "Ndakugana! Goodbye! Come back to learn more Kirundi.",
        "Turabonana! See you later! Practice your Kirundi every day!"
    ]
}

def get_response(message):
    """Generate response based on user message"""
    msg = message.lower().strip()
    
    # ===== GREETINGS =====
    if any(word in msg for word in ["hello", "hi", "hey", "mwaramutse", "bonjour"]):
        return random.choice(RESPONSES["greeting"])
    
    if "how are you" in msg or "uraho" in msg:
        return random.choice(RESPONSES["how_are_you"])
    
    if any(word in msg for word in ["thank", "thanks", "murakoze"]):
        return random.choice(RESPONSES["thanks"])
    
    if any(word in msg for word in ["goodbye", "bye", "ndakugana"]):
        return random.choice(RESPONSES["goodbye"])
    
    # ===== WHO IS MBAZA =====
    if any(word in msg for word in ["who are you", "what is mbaza", "creator", "mugisha"]):
        return """🤖 I am Mbaza AI!
        
Created by Mugisha Pc
I teach Kirundi language
I know greetings, vocabulary, grammar
Say 'help' to see what I can do!
Iga Kirundi na Mbaza AI - Learn Kirundi with Mbaza AI"""
    
    # ===== TRANSLATION =====
    if "translate" in msg or "what is" in msg or "meaning of" in msg:
        # Extract word to translate
        word = msg.replace("translate", "").replace("what is", "").replace("meaning of", "").strip()
        
        # English to Kirundi
        if word in WORDS:
            return f"📖 {word} in Kirundi is: {WORDS[word]}\n\nExample: Use it in a sentence!"
        
        # Kirundi to English
        if word in WORDS_REVERSE:
            return f"📖 {word} in English is: {WORDS_REVERSE[word]}"
        
        return f"Sorry, I don't know '{word}' yet. Try another word like 'hello', 'good morning', 'cow', 'water'"
    
    # ===== GRAMMAR =====
    if "grammar" in msg or "tense" in msg:
        if "present" in msg:
            return f"📚 PRESENT TENSE\n\n{GRAMMAR_RULES['present tense']}"
        elif "past" in msg:
            return f"📚 PAST TENSE\n\n{GRAMMAR_RULES['past tense']}"
        elif "future" in msg:
            return f"📚 FUTURE TENSE\n\n{GRAMMAR_RULES['future tense']}"
        elif "noun" in msg or "class" in msg:
            return f"📚 NOUN CLASSES\n\n{GRAMMAR_RULES['noun class 1']}"
        else:
            return """📚 KIRUNDI GRAMMAR
        
Say:
'grammar present' - Present tense
'grammar past' - Past tense  
'grammar future' - Future tense
'grammar noun class' - Noun classes"""
    
    # ===== LEARN VOCABULARY =====
    if any(word in msg for word in ["learn", "vocab", "words", "teach me"]):
        category = None
        categories = ["greeting", "people", "animals", "food", "verbs", "numbers"]
        
        for cat in categories:
            if cat in msg:
                category = cat
                break
        
        if category == "greeting":
            words_found = {k: v for k, v in WORDS.items() if k in ["good morning", "good evening", "how are you", "i am fine", "goodbye", "thank you"]}
        elif category == "people":
            words_found = {k: v for k, v in WORDS.items() if k in ["person", "woman", "man", "child", "girl", "boy"]}
        elif category == "animals":
            words_found = {k: v for k, v in WORDS.items() if k in ["cow", "dog", "cat", "chicken", "horse"]}
        elif category == "food":
            words_found = {k: v for k, v in WORDS.items() if k in ["milk", "rice", "meat", "eggs", "water"]}
        elif category == "verbs":
            words_found = {k: v for k, v in WORDS.items() if k in ["eat", "drink", "sleep", "work", "play", "read", "write", "go", "come", "love"]}
        elif category == "numbers":
            words_found = {k: v for k, v in WORDS.items() if k in ["one", "two", "three", "four", "five", "ten"]}
        else:
            # Random words
            import random
            items = list(WORDS.items())
            random.shuffle(items)
            words_found = dict(items[:8])
            category = "random"
        
        response = f"📚 {category.upper()} VOCABULARY\n\n"
        for eng, kir in list(words_found.items())[:10]:
            response += f"{eng} = {kir}\n"
        response += "\nSay 'translate [word]' to see more!"
        return response
    
    # ===== QUIZ =====
    if "quiz" in msg or "test" in msg:
        eng, kir = random.choice(list(WORDS.items()))
        return f"📝 QUIZ TIME!\n\nWhat is '{eng}' in Kirundi?\n\nType your answer! (Say 'translate {eng}' for help)"
    
    # ===== HELP =====
    if "help" in msg or "what can you do" in msg:
        return """🤖 MBAZA AI HELP
        
1. TRANSLATE: 'translate hello', 'what is cow'
2. GRAMMAR: 'grammar present', 'grammar past'
3. LEARN: 'learn greetings', 'learn animals', 'learn verbs'
4. QUIZ: 'quiz', 'test me'
5. GREETINGS: 'hello', 'how are you', 'thank you', 'goodbye'
6. ABOUT: 'who are you', 'creator'

Iga Kirundi na Mbaza AI! 🇧🇮"""
    
    # ===== CHECK IF SINGLE WORD IN DICTIONARY =====
    if msg in WORDS:
        return f"📖 {msg} in Kirundi is: {WORDS[msg]}"
    
    if msg in WORDS_REVERSE:
        return f"📖 {msg} in English is: {WORDS_REVERSE[msg]}"
    
    # ===== DEFAULT RESPONSE =====
    return f"""Iga Kirundi na Mbaza AI! 🇧🇮

Try these:
• 'translate hello' - Learn words
• 'grammar present' - Learn grammar
• 'learn greetings' - Study vocabulary
• 'quiz' - Test yourself
• 'help' - See all features

What would you like to learn today?"""

# ============ HTML TEMPLATE ============
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Mbaza AI - Learn Kirundi</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
        }
        
        .chat-container {
            width: 100%;
            height: 100%;
            background: white;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .chat-header h1 {
            font-size: 22px;
            font-weight: 600;
        }
        
        .chat-header p {
            font-size: 12px;
            opacity: 0.9;
            margin-top: 4px;
        }
        
        .quick-buttons {
            display: flex;
            gap: 8px;
            padding: 10px 12px;
            background: #f8f9fa;
            overflow-x: auto;
            border-bottom: 1px solid #e9ecef;
        }
        
        .quick-btn {
            padding: 8px 16px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 25px;
            font-size: 13px;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }
        
        .quick-btn:active {
            background: #667eea;
            color: white;
            transform: scale(0.95);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .message {
            display: flex;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 20px;
            font-size: 15px;
            line-height: 1.4;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.bot .message-content {
            background: white;
            color: #2d3748;
            border-bottom-left-radius: 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        }
        
        .message.bot .message-content strong {
            color: #667eea;
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border-radius: 20px;
            width: fit-content;
            margin-bottom: 12px;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #cbd5e0;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-8px); opacity: 1; }
        }
        
        .chat-input-container {
            padding: 12px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 8px;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 1.5px solid #e9ecef;
            border-radius: 25px;
            font-size: 15px;
            outline: none;
            font-family: inherit;
        }
        
        .chat-input:focus {
            border-color: #667eea;
        }
        
        .send-button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .send-button:active {
            transform: scale(0.95);
        }
        
        @media (max-width: 480px) {
            .message-content {
                max-width: 85%;
                font-size: 14px;
                padding: 10px 14px;
            }
            .quick-btn {
                font-size: 12px;
                padding: 6px 14px;
            }
            .chat-header h1 {
                font-size: 18px;
            }
            .send-button {
                padding: 10px 18px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🤖 MBAZA AI</h1>
            <p>Iga Kirundi na Mbaza AI | Learn Kirundi with Mbaza AI</p>
        </div>
        
        <div class="quick-buttons">
            <button class="quick-btn" onclick="sendQuick('hello')">👋 Hello</button>
            <button class="quick-btn" onclick="sendQuick('how are you')">❓ How are you</button>
            <button class="quick-btn" onclick="sendQuick('translate cow')">📖 Translate</button>
            <button class="quick-btn" onclick="sendQuick('grammar present')">📚 Grammar</button>
            <button class="quick-btn" onclick="sendQuick('learn greetings')">🎓 Learn</button>
            <button class="quick-btn" onclick="sendQuick('quiz')">✍️ Quiz</button>
            <button class="quick-btn" onclick="sendQuick('help')">ℹ️ Help</button>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    <strong>🤖 Mbaza AI</strong><br><br>
                    Iga Kirundi na Mbaza AI! 🇧🇮<br><br>
                    I teach Kirundi language. Try:<br>
                    • "translate hello"<br>
                    • "grammar present"<br>
                    • "learn greetings"<br>
                    • "quiz"<br><br>
                    What would you like to learn?
                </div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            <span></span><span></span><span></span>
        </div>
        
        <div class="chat-input-container">
            <input type="text" id="messageInput" class="chat-input" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
            <button class="send-button" onclick="sendMessage()">Send</button>
        </div>
    </div>
    
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const typingIndicator = document.getElementById('typingIndicator');
        
        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function sendQuick(text) {
            messageInput.value = text;
            sendMessage();
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            messageInput.value = '';
            scrollToBottom();
            
            typingIndicator.style.display = 'block';
            scrollToBottom();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                typingIndicator.style.display = 'none';
                addMessage(data.response, 'bot');
                scrollToBottom();
            } catch (error) {
                typingIndicator.style.display = 'none';
                addMessage('Sorry, something went wrong. Please try again.', 'bot');
                scrollToBottom();
            }
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            if (sender === 'bot') {
                contentDiv.innerHTML = '<strong>🤖 Mbaza AI</strong><br><br>' + text.replace(/\\n/g, '<br>');
            } else {
                contentDiv.innerHTML = '<strong>🧑 You</strong><br><br>' + text;
            }
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }
        
        messageInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'response': 'Please type something to learn Kirundi!'})
        
        response = get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': 'Sorry, something went wrong. Please try again!'})

@app.route('/health')
def health():
    return jsonify({'status': 'active', 'ai': 'Mbaza AI', 'creator': 'Mugisha Pc'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
