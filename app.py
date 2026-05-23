from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# ============ SPEAKING-FOCUSED KIRUNDI DATABASE ============
# English to Kirundi - Common spoken phrases
EN_TO_RN = {
    # Basic Greetings - Most Important for Speaking
    "hello": "Mwaramutse",
    "hi": "Mwaramutse", 
    "good morning": "Mwaramutse",
    "good afternoon": "Mwiriwe",
    "good evening": "Mwiriwe",
    "good night": "Ijoro ryiza",
    "how are you": "Uraho",
    "how are you doing": "Uraho",
    "how's it going": "Bite",
    "i am fine": "Ni meza",
    "i'm fine": "Ni meza",
    "i am good": "Ni meza",
    "fine": "Ni meza",
    "not bad": "Si mubi",
    "and you": "Nawe",
    "what's up": "Bite",
    "thank you": "Murakoze",
    "thanks": "Murakoze",
    "thanks a lot": "Murakoze cyane",
    "you're welcome": "Urakaza neza",
    "welcome": "Urakaza neza",
    "sorry": "Mbaza",
    "excuse me": "Mbabarira",
    "please": "Nyamuneka",
    "yes": "Yego",
    "no": "Oya",
    "okay": "Sawa",
    "goodbye": "Ndakugana",
    "bye": "Ndakugana",
    "see you later": "Turabonana",
    "see you tomorrow": "Turabonana ejo",
    "take care": "Witondere",
    "have a nice day": "Umunsi mwiza",
    
    # Common Daily Phrases - Speaking Focus
    "what is your name": "Witwa nde",
    "my name is": "Nitwa",
    "nice to meet you": "Mbaye umunezero wo kuguhuza",
    "where are you from": "Uturuka he",
    "i am from": "Nturuka",
    "how old are you": "Ufite imyaka ingahe",
    "i am": "Mfite imyaka",
    "what do you do": "Ukora iki",
    "i work": "Nkora",
    "i study": "Niga",
    "where do you live": "Utuye he",
    "i live in": "Ntuye i",
    "do you speak english": "Uvuga icyongereza",
    "i speak a little kirundi": "Nvuga gito ikirundi",
    "can you help me": "Uramfasha",
    "i need help": "Nkeneye ubufasha",
    "how much": "Angahe",
    "how many": "Angahe",
    "i want": "Ndashaka",
    "i don't want": "Sindashaka",
    "i like": "Ndagukunda",
    "i don't like": "Ntabikunda",
    "it's good": "Ni byiza",
    "it's bad": "Ni bibi",
    "it's beautiful": "Ni nziza",
    "it's expensive": "Birahenze",
    "it's cheap": "Birahendutse",
    "come here": "Uze hano",
    "go there": "Jya hariya",
    "wait": "Tegereza",
    "listen": "Jya kumva",
    "look": "Reba",
    "stop": "Hagarara",
    "go": "Genda",
    "eat": "Kurya",
    "drink": "Kunywa",
    "sleep": "Kuryama",
    "wake up": "Kanguka",
    
    # People - Speaking
    "person": "Umuntu",
    "people": "Abantu",
    "man": "Umugabo",
    "woman": "Umugore",
    "child": "Umwana",
    "children": "Abana",
    "boy": "Umuhungu",
    "girl": "Umukobwa",
    "friend": "Inshuti",
    "teacher": "Umwarimu",
    "student": "Umunyeshuri",
    "doctor": "Umuganga",
    
    # Family - Speaking
    "father": "Data",
    "dad": "Data",
    "mother": "Mama",
    "mom": "Mama",
    "brother": "Mukuru",
    "sister": "Mushiki",
    "grandfather": "Sekuru",
    "grandmother": "Nyogokuru",
    "uncle": "Mwene data",
    "aunt": "Mwene mama",
    "husband": "Umugabo wanjye",
    "wife": "Umugore wanjye",
    "son": "Umuhungu wanjye",
    "daughter": "Umukobwa wanjye",
    
    # Animals - Speaking
    "cow": "Inka",
    "dog": "Imbwa",
    "cat": "Injata",
    "chicken": "Inkoko",
    "bird": "Inyoni",
    "fish": "Isazi",
    "goat": "Ihene",
    "sheep": "Intama",
    
    # Food & Drink - Speaking
    "water": "Amazi",
    "milk": "Amata",
    "rice": "Umuceri",
    "meat": "Inyama",
    "eggs": "Amagi",
    "bread": "Umukate",
    "beans": "Ibishyimbo",
    "banana": "Igitoki",
    "food": "Ibiryo",
    "eat": "Kurya",
    "drink": "Kunywa",
    "hungry": "Ndashonje",
    "thirsty": "Ndakabije",
    "full": "Nahagaze",
    
    # Shopping - Speaking
    "market": "Isoko",
    "shop": "Iduka",
    "buy": "Kugura",
    "sell": "Kugurisha",
    "money": "Amafaranga",
    "cheap": "Birahendutse",
    "expensive": "Birahenze",
    "how much is this": "Iki ni angahe",
    
    # Directions - Speaking
    "where": "He",
    "here": "Hano",
    "there": "Hariya",
    "left": "Ibumoso",
    "right": "Iburyo",
    "straight": "Imbere",
    "near": "Hafi",
    "far": "Kure",
    "school": "Ishuri",
    "church": "Itorero",
    "hospital": "Ibitaro",
    "home": "Urugo",
    "house": "Inzu",
    
    # Time - Speaking
    "today": "Uyu munsi",
    "yesterday": "Ejo hashize",
    "tomorrow": "Ejo hazaza",
    "morning": "Mu gitondo",
    "afternoon": "Saa sita",
    "evening": "Mu mwiriwe",
    "night": "Ijoro",
    "now": "None",
    "later": "Nyuma",
    "soon": "Vuba",
    
    # Emotions - Speaking
    "happy": "Ndahimbawe",
    "sad": "Ndababaye",
    "angry": "Ndarakaye",
    "scared": "Ndatinya",
    "tired": "Ndaruhutse",
    "sick": "Ndwaye",
    
    # Love & Relationships - Speaking
    "love": "Urukundo",
    "i love you": "Ndagukunda",
    "i love kirundi": "Ndagukunda ikirundi",
    "beautiful": "Nziza",
    "handsome": "Mwiza",
    
    # Numbers - Speaking
    "one": "Rimwe",
    "two": "Kabiri",
    "three": "Gatatu",
    "four": "Kane",
    "five": "Gatanu",
    "six": "Gatandatu",
    "seven": "Indwi",
    "eight": "Umunani",
    "nine": "Icenda",
    "ten": "Icumi",
    
    # Question Words - Speaking
    "what": "Iki",
    "who": "Nde",
    "where": "He",
    "when": "Ryari",
    "why": "Kuki",
    "how": "Gute",
}

# Kirundi to English
RN_TO_EN = {v: k for k, v in EN_TO_RN.items()}

# ============ SPOKEN PHRASES & CONVERSATIONS ============
SPOKEN_PHRASES = {
    "greeting": [
        "Mwaramutse! 👋 Say 'Uraho' to ask 'How are you?' in Kirundi!",
        "Hello! 🌅 'Mwaramutse' means good morning. Try saying it out loud!",
        "Mwaramutse mwenza! That means 'Hello my friend!' in Kirundi."
    ],
    "how_are_you": [
        "Ni meza! 🙏 That's 'I'm fine' in Kirundi. Now you say 'Uraho' to ask someone how they are!",
        "I'm good! 💪 In Kirundi, say 'Ni meza' when someone asks 'Uraho' (How are you).",
        "Ni meza, urakoze! That means 'I'm fine, thank you!' Practice saying it!"
    ],
    "thanks": [
        "Murakoze! 🎉 That's 'Thank you' in Kirundi. You're welcome is 'Urakaza neza'.",
        "Urakaza neza! 🌟 Keep practicing! Say 'Murakoze' when someone helps you.",
        "Murakoze cyane! That means 'Thank you very much'. You're doing great!"
    ],
    "goodbye": [
        "Ndakugana! 👋 Say this when leaving. 'Turabonana' means 'See you later'!",
        "Ndakugana, mugenzi wanjye! That means 'Goodbye, my friend!' Come back tomorrow!",
        "Turabonana ejo! That's 'See you tomorrow!' Keep practicing every day!"
    ],
    "love": [
        "Ndagukunda! ❤️ That's how you say 'I love you' in Kirundi!",
        "Urukundo means 'Love' in Kirundi. Say 'Ndagukunda' to someone special!",
        "In Kirundi, 'I love you' is 'Ndagukunda'. Beautiful, right?"
    ],
    "help": [
        "To ask for help in Kirundi, say 'Uramfasha?' (Can you help me?)",
        "If you need help, say 'Nkeneye ubufasha' (I need help). I'm always here for you!",
        "Want to learn Kirundi fast? Practice saying common phrases every day!"
    ]
}

# ============ SMART SPEAKING RESPONSE ============
def get_response(user_input):
    text = user_input.lower().strip()
    
    # ===== GREETINGS =====
    if text in ["hello", "hi", "hey", "good morning", "mwaramutse"]:
        return random.choice(SPOKEN_PHRASES["greeting"])
    
    if "how are you" in text or "uraho" in text:
        return random.choice(SPOKEN_PHRASES["how_are_you"])
    
    if text in ["thank you", "thanks", "murakoze"]:
        return random.choice(SPOKEN_PHRASES["thanks"])
    
    if text in ["goodbye", "bye", "ndakugana", "see you"]:
        return random.choice(SPOKEN_PHRASES["goodbye"])
    
    # ===== LOVE PHRASES =====
    if "love" in text or "i love you" in text or "ndagukunda" in text:
        return random.choice(SPOKEN_PHRASES["love"])
    
    # ===== WHO AM I =====
    if any(q in text for q in ["who are you", "what is mbaza", "creator", "mugisha", "your name"]):
        return """🤖 **MBAZA AI** - Your Kirundi Speaking Partner!

🎯 Created by: **Mugisha Pc**
🗣️ **I TEACH SPEAKING KIRUNDI** - Not just grammar!
📚 I know 500+ common phrases and words
💬 Practice real conversations with me

**Try these:**
• Say 'hello' - Learn greetings
• Say 'how are you' - Daily phrases
• Say 'i love you' - Romantic phrases
• Ask 'translate water' - Learn words

**Iga Kirundi na Mbaza AI!** 🇧🇮"""
    
    # ===== TRANSLATION =====
    if "translate" in text or "what is" in text or "meaning of" in text:
        # Extract word
        word = text.replace("translate", "").replace("what is", "").replace("meaning of", "").strip()
        
        if not word:
            return "📖 Give me a word! Example: 'translate water' or 'what is love'"
        
        # Check exact match first
        if word in EN_TO_RN:
            kirundi = EN_TO_RN[word]
            return f"📖 **{word}** in Kirundi is: **{kirundi}**\n\n🗣️ Try saying it out loud! Want to hear it in a sentence? Say 'example {word}'"
        
        # Check partial match
        matches = [w for w in EN_TO_RN.keys() if word in w or w in word]
        if matches:
            match = matches[0]
            kirundi = EN_TO_RN[match]
            return f"📖 Did you mean **{match}**? That is **{kirundi}** in Kirundi.\n\n🗣️ Practice saying '{kirundi}'!"
        
        # Common words suggestion
        common = ["water", "love", "hello", "thank you", "goodbye", "cow", "eat", "drink", "person", "friend"]
        return f"📚 I don't know '{word}' yet. Try one of these common words:\n\n• " + "\n• ".join(common[:8])
    
    # ===== EXAMPLE SENTENCES =====
    if "example" in text:
        word = text.replace("example", "").strip()
        if word in EN_TO_RN:
            kir = EN_TO_RN[word]
            examples = {
                "water": f"🗣️ 'Nda amazi' = I drink water\n🗣️ 'Ndashaka amazi' = I want water",
                "love": f"🗣️ 'Ndagukunda' = I love you\n🗣️ 'Urukundo ni rwiza' = Love is beautiful",
                "hello": f"🗣️ 'Mwaramutse mwese' = Hello everyone\n🗣️ 'Mwaramutse mugenzi wanjye' = Hello my friend",
                "thank you": f"🗣️ 'Murakoze cyane' = Thank you very much\n🗣️ 'Murakoze kugufasha' = Thank you for helping",
                "eat": f"🗣️ 'Ndashaka kurya' = I want to eat\n🗣️ 'Urakurya?' = Are you eating?",
                "drink": f"🗣️ 'Ndashaka kunywa' = I want to drink\n🗣️ 'Nda amazi' = I drink water",
            }
            if word in examples:
                return examples[word] + f"\n\n🗣️ '{kir}' is how you say '{word}' in Kirundi!"
            return f"🗣️ '{kir}' means '{word}' in Kirundi. Try using it in a sentence!"
        return f"Give me a word: 'example water', 'example love', 'example hello'"
    
    # ===== LEARN SPOKEN PHRASES =====
    if any(l in text for l in ["learn", "teach me", "show me", "phrases"]):
        category = None
        if "greeting" in text:
            category = "GREETINGS"
            phrases = {
                "Hello": "Mwaramutse",
                "Good morning": "Mwaramutse",
                "Good evening": "Mwiriwe",
                "How are you": "Uraho",
                "I am fine": "Ni meza",
                "Thank you": "Murakoze",
                "Goodbye": "Ndakugana",
            }
        elif "love" in text:
            category = "LOVE PHRASES"
            phrases = {
                "I love you": "Ndagukunda",
                "Love": "Urukundo",
                "You are beautiful": "Uri mwiza",
                "My heart": "Umutima wanjye",
            }
        elif "question" in text:
            category = "QUESTIONS"
            phrases = {
                "What": "Iki",
                "Who": "Nde",
                "Where": "He",
                "When": "Ryari",
                "Why": "Kuki",
                "How": "Gute",
            }
        else:
            category = "DAILY PHRASES"
            phrases = {
                "Yes": "Yego",
                "No": "Oya",
                "Please": "Nyamuneka",
                "Sorry": "Mbaza",
                "Excuse me": "Mbabarira",
                "Wait": "Tegereza",
                "Listen": "Jya kumva",
                "Look": "Reba",
            }
        
        response = f"🗣️ **{category} TO SPEAK IN KIRUNDI**\n\n"
        for eng, kir in phrases.items():
            response += f"• {eng} = {kir}\n"
        response += "\n💡 Practice saying these out loud every day!"
        return response
    
    # ===== QUIZ =====
    if any(q in text for q in ["quiz", "test", "practice"]):
        eng, kir = random.choice(list(EN_TO_RN.items()))
        return f"📝 **SPEAKING QUIZ!**\n\nHow do you say '{eng}' in Kirundi?\n\n🗣️ Type 'translate {eng}' for help, or type your answer!\n\n💡 Hint: Starts with '{kir[0]}'"
    
    # ===== CONVERSATION PRACTICE =====
    if "conversation" in text or "talk" in text:
        return """🗣️ **LET'S PRACTICE CONVERSATION!**

I'll be your Kirundi speaking partner. Try:

• Say 'hello' to me in Kirundi
• Ask me 'how are you' in Kirundi
• Tell me 'thank you' in Kirundi
• Say 'goodbye' in Kirundi

Start now! Say 'Mwaramutse' to me!"""
    
    # ===== HELP =====
    if "help" in text:
        return """🗣️ **MBAZA AI - SPEAKING KIRUNDI**

📖 **TRANSLATE WORDS:**
'translate water', 'what is love'

🗣️ **LEARN PHRASES:**
'learn greetings', 'learn love phrases'

💬 **CONVERSATION:**
'hello', 'how are you', 'thank you', 'i love you'

📝 **PRACTICE:**
'quiz', 'conversation'

**Iga Kirundi na Mbaza AI!** 🇧🇮
Start by saying 'hello' to me!"""
    
    # ===== DIRECT WORD LOOKUP =====
    if text in EN_TO_RN:
        return f"🗣️ '{text}' in Kirundi is: **{EN_TO_RN[text]}**\n\nTry saying it! Say 'example {text}' to see it in a sentence."
    
    if text in RN_TO_EN:
        return f"🗣️ '{text}' in English is: **{RN_TO_EN[text]}**\n\nGreat job! Keep practicing!"
    
    # ===== DEFAULT - ENCOURAGE SPEAKING =====
    return f"""🗣️ **Iga Kirundi na Mbaza AI!**

Try these speaking exercises:

📖 'translate water' - Learn a word
🗣️ 'learn greetings' - Learn phrases
💬 'hello' - Start a conversation
📝 'quiz' - Test yourself

What would you like to learn to say in Kirundi?"""

# ============ HTML WITH WORKING INPUT ON PHONES ============
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
    <meta name="theme-color" content="#667eea">
    <title>Mbaza AI - Speak Kirundi</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            height: 100%;
            width: 100%;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            overflow: hidden;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }

        .app {
            width: 100%;
            height: 100%;
            background: white;
            display: flex;
            flex-direction: column;
            position: relative;
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            flex-shrink: 0;
        }

        .header h1 {
            font-size: 22px;
            font-weight: 700;
        }

        .header p {
            font-size: 13px;
            opacity: 0.9;
            margin-top: 4px;
        }

        /* Quick Buttons */
        .quick-buttons {
            display: flex;
            gap: 10px;
            padding: 12px;
            background: #f8f9fa;
            overflow-x: auto;
            border-bottom: 1px solid #e9ecef;
            flex-shrink: 0;
            -webkit-overflow-scrolling: touch;
        }

        .quick-btn {
            padding: 8px 18px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
            color: #495057;
        }

        .quick-btn:active {
            background: #667eea;
            color: white;
            transform: scale(0.96);
            border-color: #667eea;
        }

        /* Messages - Scrollable */
        .messages {
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

        .bubble {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 20px;
            font-size: 15px;
            line-height: 1.45;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message.user .bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message.bot .bubble {
            background: white;
            color: #2d3748;
            border-bottom-left-radius: 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        }

        .message.bot .bubble strong {
            color: #667eea;
        }

        /* Typing Indicator */
        .typing {
            display: none;
            padding: 10px 16px;
            background: white;
            border-radius: 20px;
            width: fit-content;
            margin-left: 16px;
            margin-bottom: 12px;
        }

        .typing span {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #cbd5e0;
            margin: 0 3px;
            animation: typingAnim 1.4s infinite;
        }

        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingAnim {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-8px); opacity: 1; }
        }

        /* Input Area - FIXED AT BOTTOM, ALWAYS VISIBLE */
        .input-container {
            flex-shrink: 0;
            background: white;
            border-top: 1px solid #e9ecef;
            padding: 12px;
        }

        .input-wrapper {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .input-field {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid #e9ecef;
            border-radius: 30px;
            font-size: 16px;
            outline: none;
            font-family: inherit;
            background: white;
            width: 100%;
        }

        .input-field:focus {
            border-color: #667eea;
        }

        .send-btn {
            padding: 14px 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s;
            white-space: nowrap;
        }

        .send-btn:active {
            transform: scale(0.95);
        }

        /* Scrollbar */
        .messages::-webkit-scrollbar {
            width: 4px;
        }

        .messages::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        .messages::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }

        /* Mobile Specific */
        @media (max-width: 480px) {
            .bubble {
                max-width: 85%;
                font-size: 14px;
                padding: 10px 14px;
            }
            .quick-btn {
                font-size: 13px;
                padding: 7px 15px;
            }
            .header h1 {
                font-size: 20px;
            }
            .input-field {
                padding: 12px 16px;
                font-size: 15px;
            }
            .send-btn {
                padding: 12px 22px;
                font-size: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="app">
        <div class="header">
            <h1>🤖 MBAZA AI</h1>
            <p>Iga Kirundi na Mbaza AI</p>
        </div>

        <div class="quick-buttons">
            <button class="quick-btn" onclick="sendQuick('translate water')">💧 Water</button>
            <button class="quick-btn" onclick="sendQuick('translate love')">❤️ Love</button>
            <button class="quick-btn" onclick="sendQuick('learn greetings')">🗣️ Greetings</button>
            <button class="quick-btn" onclick="sendQuick('conversation')">💬 Talk</button>
            <button class="quick-btn" onclick="sendQuick('quiz')">✍️ Quiz</button>
            <button class="quick-btn" onclick="sendQuick('help')">ℹ️ Help</button>
        </div>

        <div class="messages" id="messages">
            <div class="message bot">
                <div class="bubble">
                    <strong>🤖 Mbaza AI</strong><br><br>
                    Iga Kirundi na Mbaza AI! 🗣️🇧🇮<br><br>
                    I'll teach you to SPEAK Kirundi! Try:<br>
                    • "hello" - Greetings<br>
                    • "translate love" - Learn words<br>
                    • "learn greetings" - Phrases<br>
                    • "conversation" - Practice talking
                </div>
            </div>
        </div>

        <div class="typing" id="typing">
            <span></span><span></span><span></span>
        </div>

        <div class="input-container">
            <div class="input-wrapper">
                <input type="text" id="messageInput" class="input-field" placeholder="Type your message here..." autofocus>
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('messages');
        const inputField = document.getElementById('messageInput');
        const typingDiv = document.getElementById('typing');

        function scrollToBottom() {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function sendQuick(text) {
            inputField.value = text;
            sendMessage();
        }

        async function sendMessage() {
            const message = inputField.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            inputField.value = '';
            scrollToBottom();

            typingDiv.style.display = 'block';
            scrollToBottom();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                typingDiv.style.display = 'none';
                addMessage(data.response, 'bot');
                scrollToBottom();
            } catch (error) {
                typingDiv.style.display = 'none';
                addMessage("🗣️ Iga Kirundi na Mbaza AI! Try 'translate hello'", 'bot');
                scrollToBottom();
            }
        }

        function addMessage(text, sender) {
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            const bubble = document.createElement('div');
            bubble.className = 'bubble';
            
            if (sender === 'bot') {
                bubble.innerHTML = '<strong>🤖 Mbaza AI</strong><br><br>' + text.replace(/\\n/g, '<br>');
            } else {
                bubble.innerHTML = '<strong>🧑 You</strong><br><br>' + text;
            }
            
            div.appendChild(bubble);
            messagesDiv.appendChild(div);
            scrollToBottom();
        }

        inputField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Focus on input when page loads
        setTimeout(() => {
            inputField.focus();
        }, 100);
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
            return jsonify({'response': "🗣️ Iga Kirundi na Mbaza AI! Type 'hello' to start!"})
        
        response = get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': "🗣️ Iga Kirundi na Mbaza AI! Try 'translate water' or 'hello'"})

@app.route('/health')
def health():
    return jsonify({'status': 'active', 'ai': 'Mbaza AI', 'creator': 'Mugisha Pc'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
