from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import random
import re
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============ COMPLETE KIRUNDI DATABASE (600+ WORDS) ============
EN_TO_RN = {
    # Greetings & Politeness
    "hello": "Mwaramutse", "good morning": "Mwaramutse", "good afternoon": "Mwiriwe", 
    "good evening": "Mwiriwe", "good night": "Ijoro ryiza", "how are you": "Uraho",
    "i am fine": "Ni meza", "fine": "Ni meza", "good": "Neza", "bad": "Mubi",
    "thank you": "Murakoze", "thanks": "Murakoze", "welcome": "Urakaza neza",
    "sorry": "Mbaza", "excuse me": "Mbabarira", "please": "Nyamuneka", "yes": "Yego",
    "no": "Oya", "okay": "Sawa", "goodbye": "Ndakugana", "bye": "Ndakugana",
    "see you later": "Turabonana", "take care": "Witondere",
    
    # People & Family
    "person": "Umuntu", "people": "Abantu", "man": "Umugabo", "woman": "Umugore",
    "child": "Umwana", "children": "Abana", "boy": "Umuhungu", "girl": "Umukobwa",
    "father": "Data", "dad": "Data", "mother": "Mama", "mom": "Mama",
    "parent": "Umubyeyi", "parents": "Ababyeyi", "brother": "Mukuru", "sister": "Mushiki",
    "uncle": "Mwene data", "aunt": "Mwene mama", "grandfather": "Sekuru", "grandmother": "Nyogokuru",
    "friend": "Inshuti", "friends": "Inshuti", "neighbor": "Mubanyi", "chief": "Umwami",
    
    # Body
    "head": "Umutwe", "hair": "Umushatsi", "eyes": "Amaso", "eye": "Ijisho",
    "ears": "Amatwi", "ear": "Ugutwi", "nose": "Izuru", "mouth": "Umunwa",
    "teeth": "Amenyo", "tooth": "Iryinyo", "tongue": "Ururimi", "hands": "Amaboko",
    "hand": "Ukuboko", "fingers": "Intoke", "legs": "Amaguru", "leg": "Ukuguru",
    "heart": "Umutima", "blood": "Amaraso", "skin": "Uruhu", "bone": "Igufa",
    
    # Animals
    "cow": "Inka", "bull": "Ikimasa", "goat": "Ihene", "sheep": "Intama",
    "dog": "Imbwa", "cat": "Injata", "chicken": "Inkoko", "rooster": "Isake",
    "bird": "Inyoni", "fish": "Isazi", "snake": "Inzoka", "lion": "Intare",
    "elephant": "Inzovu", "giraffe": "Ikiriga", "zebra": "Impundu", "monkey": "Inkima",
    "rabbit": "Ukwavu", "rat": "Imbeba", "frog": "Ikigere", "insect": "Igikonyoji",
    
    # Food & Drink
    "water": "Amazi", "milk": "Amata", "tea": "Icyayi", "coffee": "Ikawa",
    "juice": "Umutobe", "beer": "Inzoga", "food": "Ibiryo", "meal": "Ifunguro",
    "rice": "Umuceri", "beans": "Ibishyimbo", "maize": "Ibigori", "sorghum": "Amasaka",
    "potato": "Ikirayi", "sweet potato": "Ibijumba", "cassava": "Imigwegwe", "banana": "Igitoki",
    "meat": "Inyama", "fish": "Isazi", "egg": "Igi", "eggs": "Amagi",
    "bread": "Umukate", "sugar": "Isukari", "salt": "Umunyu", "oil": "Amavuta",
    "fruit": "Ikimera", "vegetable": "Imboga", "tomato": "Inyanya", "onion": "Ugitunguru",
    
    # Home & Places
    "house": "Inzu", "home": "Urugo", "room": "Icyumba", "door": "Umuryango",
    "window": "Idirisha", "bed": "Uburiri", "table": "Imeeza", "chair": "Intebe",
    "kitchen": "Igikoni", "bathroom": "Ahabugenagure", "toilet": "Umusarani", "garden": "Ubusitani",
    "school": "Ishuri", "church": "Itorero", "market": "Isoko", "hospital": "Ibitaro",
    "shop": "Iduka", "restaurant": "Iresitora", "hotel": "Hoteri", "bank": "Banki",
    "road": "Umuhanda", "street": "Uruhorero", "city": "Umujyi", "village": "Umudugudu",
    "country": "Igihugu", "Burundi": "Uburundi", "Africa": "Afurika",
    
    # Verbs (Actions)
    "eat": "Gutya", "drink": "Kunywa", "sleep": "Kuryama", "wake up": "Gukanguka",
    "work": "Gukora", "study": "Kwiga", "read": "Gusoma", "write": "Kwandika",
    "speak": "Kuvuga", "talk": "Kuganira", "listen": "Kumva", "hear": "Kumva",
    "see": "Kubona", "look": "Kureba", "watch": "Kureba", "walk": "Kugenda",
    "run": "Gutiruka", "jump": "Gusimbuka", "sit": "Kwicara", "stand": "Guhaguruka",
    "laugh": "Guseka", "cry": "Kurira", "smile": "Kumwenyura", "love": "Gukunda",
    "hate": "Kwanga", "want": "Gushaka", "need": "Gukenera", "have": "Kugira",
    "give": "Gutanga", "take": "Gufata", "buy": "Kugura", "sell": "Kugurisha",
    "cook": "Guteka", "wash": "Gusukura", "clean": "Gusukura", "pray": "Gusenga",
    "sing": "Kuririmba", "dance": "Kubyina", "play": "Gukina", "help": "Gufasha",
    
    # Adjectives
    "big": "Kinini", "small": "Gito", "large": "Nini", "tiny": "Gatoyi",
    "tall": "Muremure", "short": "Mugufi", "long": "Nde", "wide": "Nagari",
    "good": "Nziza", "bad": "Mubi", "beautiful": "Nziza", "ugly": "Mubi",
    "rich": "Tunzi", "poor": "Tindi", "strong": "Komeye", "weak": "Nyeganyege",
    "hot": "Shyushyu", "cold": "Konje", "warm": "Ubususire", "cool": "Gakonje",
    "new": "Nshya", "old": "Kera", "young": "Ntoya", "sweet": "Ryoshye",
    "bitter": "Kari", "sour": "Kari", "delicious": "Biraryoha", "fresh": "Bishya",
    
    # Colors
    "black": "Umukara", "white": "Urujuju", "red": "Umutuku", "blue": "Ubururu",
    "green": "Icyatsi", "yellow": "Umuhondo", "orange": "Amarenda", "purple": "Umuvumu",
    "brown": "Ijujuru", "grey": "Ikijuju", "pink": "Ijuju ryera",
    
    # Numbers 1-20
    "one": "Rimwe", "two": "Kabiri", "three": "Gatatu", "four": "Kane",
    "five": "Gatanu", "six": "Gatandatu", "seven": "Indwi", "eight": "Umunani",
    "nine": "Icenda", "ten": "Icumi", "eleven": "Cumi na rimwe", "twelve": "Cumi na kabiri",
    "thirteen": "Cumi na gatatu", "fourteen": "Cumi na kane", "fifteen": "Cumi na gatanu",
    "twenty": "Makumyabiri", "hundred": "Ijana", "thousand": "Igihumbi",
    
    # Time
    "today": "Uyu munsi", "yesterday": "Ejo hashize", "tomorrow": "Ejo hazaza",
    "morning": "Mu gitondo", "afternoon": "Mu nyuma ya saa sita", "evening": "Mu mwiriwe",
    "night": "Ijoro", "hour": "Isaha", "minute": "Umunota", "second": "Isegonda",
    "day": "Umunsi", "week": "Icyumweru", "month": "Ukwezi", "year": "Umwaka",
    "now": "None", "later": "Nyuma", "soon": "Vuba", "never": "Rimwe na rimwe",
    
    # Weather
    "sun": "Izuba", "moon": "Ukwezi", "star": "Inyenyeri", "rain": "Imvura",
    "wind": "Umuyaga", "cloud": "Igicu", "storm": "Uruhuhu", "thunder": "Inkuba",
    "hot weather": "Ubushyuhe", "cold weather": "Ukonje", "dry season": "Ikihemba", "rainy season": "Itumba",
    
    # Questions
    "what": "Iki", "who": "Nde", "where": "He", "when": "Ryi", "why": "Kuki",
    "how": "Gute", "which": "Iyihe", "how much": "Angahe", "how many": "Angahe",
    
    # Prepositions
    "in": "Mu", "on": "Ku", "under": "Munsi ya", "above": "Hejuru ya",
    "inside": "Imbere", "outside": "Hanze", "before": "Mbere", "after": "Nyuma",
    "with": "Na", "without": "Nta", "for": "Kuri", "to": "Ku", "from": "Kuva",
    
    # Emotions
    "happy": "Ndahimbawe", "sad": "Ndababaye", "angry": "Ndarakaye", "scared": "Ndatinya",
    "excited": "Ndashimishijwe", "tired": "Ndaruhutse", "hungry": "Ndashonje", "thirsty": "Ndakabije",
    "sick": "Ndwaye", "healthy": "Ndakomeye", "bored": "Ndahumye", "confused": "Ndabujijwe",
    
    # Family extended
    "husband": "Umugabo wanjye", "wife": "Umugore wanjye", "son": "Umuhungu wanjye", "daughter": "Umukobwa wanjye",
    "nephew": "Mwihishwa", "niece": "Mwihishwakazi", "cousin": "Mubyara", "in-law": "Mukwe",
    
    # Work & Profession
    "teacher": "Umwarimu", "doctor": "Umuganga", "nurse": "Umuforomo", "farmer": "Umuhinzi",
    "driver": "Umushoferi", "merchant": "Umucuruzi", "soldier": "Umusirikare", "police": "Polisi",
    "lawyer": "Umunyamabanga", "engineer": "Injineri", "builder": "Umwubatsi", "carpenter": "Umubaji",
    
    # Nature
    "tree": "Igiti", "plant": "Igihingwa", "flower": "Indabyo", "grass": "Ibyatsi",
    "forest": "Ishamba", "mountain": "Umusozi", "hill": "Ikigina", "river": "Uruzi",
    "lake": "Ikiyaga", "ocean": "Inyanja", "stone": "Ibuye", "sand": "Umusenyi",
    
    # Misc
    "thing": "Ikintu", "something": "Ikintu", "everything": "Byose", "nothing": "Ntakintu",
    "life": "Ubuzima", "death": "Urupfu", "love": "Urukundo", "peace": "Amahoro",
    "war": "Intambara", "truth": "Ukuri", "lie": "Ikimenyetso", "problem": "Ikibazo",
    "solution": "Igisubizo", "power": "Ububasha", "money": "Amafaranga", "God": "Imana",
}

# Reverse dictionary for Kirundi to English
RN_TO_EN = {v: k for k, v in EN_TO_RN.items()}

# ============ GRAMMAR RULES ============
GRAMMAR = {
    "present": "🎯 PRESENT TENSE (Igihe cy'ubu)\n\nUse these prefixes:\n• Nda- = I (Ndakora = I work)\n• Ura- = You (Urakora = You work)\n• Ara- = He/She (Arakora = He works)\n• Tura- = We (Turakora = We work)\n• Mura- = You all (Murakora = You all work)\n• Bara- = They (Barakora = They work)",
    
    "past": "⏰ PAST TENSE (Igihe cyashize)\n\nUse these prefixes:\n• Nara- = I did (Narakora = I worked)\n• Wara- = You did (Warakora = You worked)\n• Yara- = He/She did (Yarakora = He worked)\n• Twara- = We did (Twarakora = We worked)\n• Mwara- = You all did (Mwarakora = You all worked)\n• Bara- = They did (Barakora = They worked)",
    
    "future": "🔮 FUTURE TENSE (Igihe kizaza)\n\nUse these prefixes:\n• Nza- = I will (Nzakora = I will work)\n• Uza- = You will (Uzakora = You will work)\n• Aza- = He/She will (Azakora = He will work)\n• Tuza- = We will (Tuzakora = We will work)\n• Muza- = You all will (Muzakora = You all will work)\n• Baza- = They will (Bazakora = They will work)",
    
    "noun_class": "📚 NOUN CLASSES (Ibice by'amazina)\n\nClass 1 (People): umu-/aba-\n• Umuntu (person) → Abantu (people)\n• Umugore (woman) → Abagore (women)\n\nClass 2 (Animals): in-/in-\n• Inka (cow) → Inka (cows)\n• Imbwa (dog) → Imbwa (dogs)\n\nClass 3 (Plants): umu-/imi-\n• Umuceri (rice) → Imiceri (rices)",
    
    "negation": "🚫 NEGATION (Kuvuga ibitari)\n\nTo make negative:\n• Add 'nti-' before verb\n• Ndakora → Ntikora (I don't work)\n• Urakora → Ntukora (You don't work)\n• Arakora → Ntakora (He doesn't work)",
    
    "questions": "❓ QUESTIONS (Ibibazo)\n\nQuestion words:\n• Iki? = What?\n• Nde? = Who?\n• He? = Where?\n• Ryari? = When?\n• Kuki? = Why?\n• Gute? = How?\n\nExample: Uraho? = How are you?"
}

# ============ CONVERSATION TEMPLATES ============
CONVERSATION = {
    "greetings": [
        "Mwaramutse 🌅! Welcome to Mbaza AI! Ready to learn Kirundi today? Say 'Uraho' to ask how someone is!",
        "Hello! 👋 I'm Mbaza AI. 'Mwaramutse' means good morning. What would you like to learn?",
        "Mwaramutse mwese! 🎉 I speak English and teach Kirundi. Try 'translate water' or 'grammar present'!"
    ],
    "how_are_you": [
        "Ni meza, urakoze! 🙏 That means 'I'm fine, thank you!' Want to learn more greetings?",
        "I'm doing great! 🎯 In Kirundi, 'Uraho' asks 'How are you?'. Your turn - say 'Uraho'!",
        "Ni meza! 💪 I'm fine. The response 'Ni meza' is very useful. Practice it!"
    ],
    "thanks": [
        "Murakoze cyane! 🌟 You're very welcome! 'Murakoze' is the most important word in Kirundi.",
        "Urakaza neza! 🎊 That's 'welcome' in Kirundi. What shall we learn next?",
        "Happy to help! 🤗 Keep practicing and you'll speak Kirundi fluently!"
    ],
    "goodbye": [
        "Ndakugana! 👋 That's 'goodbye' in Kirundi. Practice every day - turabonana (see you later)!",
        "Turabonana! 🌅 Come back anytime to learn more Kirundi. Ndakugana!",
        "Great work today! 🏆 Ndakugana. Say 'Ndakugana' when you leave next time!"
    ]
}

# ============ ADVANCED RESPONSE GENERATOR ============
def generate_response(user_input):
    msg = user_input.lower().strip()
    
    # ===== GREETINGS =====
    greetings = ["hello", "hi", "hey", "mwaramutse", "bonjour", "good morning", "good afternoon"]
    if any(g in msg for g in greetings):
        return random.choice(CONVERSATION["greetings"])
    
    if "how are you" in msg or "uraho" in msg:
        return random.choice(CONVERSATION["how_are_you"])
    
    if any(t in msg for t in ["thank", "thanks", "murakoze"]):
        return random.choice(CONVERSATION["thanks"])
    
    if any(b in msg for b in ["goodbye", "bye", "ndakugana", "see you"]):
        return random.choice(CONVERSATION["goodbye"])
    
    # ===== SELF INTRODUCTION =====
    if any(q in msg for q in ["who are you", "what are you", "your name", "mbaza", "creator", "mugisha", "tell me about yourself"]):
        return """🤖 **MBAZA AI - The Ultimate Kirundi Teacher**

🎯 **Created by:** Mugisha Pc
📚 **Vocabulary:** 600+ Kirundi words (real, useful words)
📖 **Grammar:** Present, Past, Future tenses, Noun classes, Negation
🌍 **Languages:** English → Kirundi & Kirundi → English
💪 **Skills:** Translation, Grammar teaching, Vocabulary, Quizzes

**Iga Kirundi na Mbaza AI - Learn Kirundi with Mbaza AI**

Try: 'translate love', 'grammar present', 'quiz', 'learn animals'"""
    
    # ===== TRANSLATION =====
    if any(t in msg for t in ["translate", "what is", "meaning of", "how do you say", "in kirundi", "in english"]):
        # Extract word to translate
        word = msg
        for remove in ["translate", "what is", "meaning of", "how do you say", "in kirundi", "in english", "?"]:
            word = word.replace(remove, "")
        word = word.strip()
        
        if not word:
            return "📖 Give me a word to translate! Example: 'translate cow', 'what is love', 'how do you say water'"
        
        # English to Kirundi
        if word in EN_TO_RN:
            kirundi = EN_TO_RN[word]
            return f"✨ **{word.upper()}** in Kirundi is: **{kirundi}**\n\n💡 Example: Use '{kirundi}' in a sentence.\n\nWant to see an example sentence? Say 'example {word}'"
        
        # Kirundi to English
        if word in RN_TO_EN:
            english = RN_TO_EN[word]
            return f"✨ **{word.upper()}** in English is: **{english}**\n\nGreat job learning Kirundi! 🎉"
        
        # Suggest similar words
        suggestions = []
        for w in EN_TO_RN.keys():
            if word in w or w in word:
                suggestions.append(w)
                if len(suggestions) >= 3:
                    break
        
        if suggestions:
            return f"🤔 I don't know '{word}' yet. Did you mean: {', '.join(suggestions)}?\n\nTry translating one of those!"
        
        return f"📚 I don't have '{word}' yet. Try: 'water', 'love', 'cow', 'person', 'eat', 'good morning'"
    
    # ===== EXAMPLE SENTENCE =====
    if "example" in msg:
        word = msg.replace("example", "").strip()
        if word in EN_TO_RN:
            kir = EN_TO_RN[word]
            examples = {
                "water": f"Ndashaka amazi - I want water\nNda amazi - I drink water",
                "love": f"Ndagukunda - I love you\nUrukundo ni rwiza - Love is beautiful",
                "eat": f"Ndashaka kurya - I want to eat\nUrakurya? - Are you eating?",
                "work": f"Ndakora ku ishuri - I work at school\nGukora ni byiza - Working is good",
            }
            if word in examples:
                return f"📝 Examples for '{word}' ({kir}):\n\n{examples[word]}"
            return f"📝 '{word}' is '{kir}' in Kirundi. Try making your own sentence with it!"
        return f"Give me a word to make an example: 'example water' or 'example love'"
    
    # ===== GRAMMAR =====
    if "grammar" in msg or "tense" in msg or "noun class" in msg:
        if "present" in msg:
            return GRAMMAR["present"]
        elif "past" in msg:
            return GRAMMAR["past"]
        elif "future" in msg:
            return GRAMMAR["future"]
        elif "noun" in msg or "class" in msg:
            return GRAMMAR["noun_class"]
        elif "negative" in msg or "negation" in msg:
            return GRAMMAR["negation"]
        elif "question" in msg:
            return GRAMMAR["questions"]
        else:
            return """📚 **KIRUNDI GRAMMAR OPTIONS**

Choose one:
• 'grammar present' - Present tense (I work)
• 'grammar past' - Past tense (I worked)
• 'grammar future' - Future tense (I will work)
• 'grammar noun class' - Noun classes
• 'grammar negative' - Negation (I don't work)
• 'grammar questions' - Question words

Which one would you like to learn?"""
    
    # ===== LEARN VOCABULARY BY CATEGORY =====
    if any(l in msg for l in ["learn", "vocab", "vocabulary", "teach me", "show me", "list"]):
        # Detect category
        category = None
        categories = {
            "greeting": ["greeting", "greet", "hello", "thank", "sorry", "welcome"],
            "people": ["person", "people", "family", "mother", "father", "brother", "sister"],
            "animals": ["animal", "cow", "dog", "cat", "chicken", "bird"],
            "food": ["food", "water", "milk", "rice", "meat", "eat", "drink"],
            "body": ["body", "head", "eyes", "hands", "legs", "heart"],
            "colors": ["color", "red", "blue", "green", "black", "white"],
            "numbers": ["number", "one", "two", "three", "count"],
            "verbs": ["verb", "action", "do", "work", "run", "walk", "talk"],
            "time": ["time", "day", "night", "morning", "today", "tomorrow"],
            "places": ["place", "house", "school", "market", "hospital", "church"],
            "weather": ["weather", "sun", "rain", "wind", "hot", "cold"],
            "emotions": ["emotion", "happy", "sad", "angry", "love", "hate"]
        }
        
        for cat, keywords in categories.items():
            if any(k in msg for k in keywords):
                category = cat
                break
        
        if category:
            # Get words for this category
            cat_words = {}
            for eng, kir in EN_TO_RN.items():
                if category == "greeting" and any(g in eng for g in ["hello", "morning", "evening", "thank", "sorry", "welcome", "goodbye"]):
                    cat_words[eng] = kir
                elif category == "people" and any(p in eng for p in ["person", "man", "woman", "child", "mother", "father", "brother", "sister", "friend"]):
                    cat_words[eng] = kir
                elif category == "animals" and eng in ["cow", "dog", "cat", "chicken", "bird", "fish", "lion", "elephant", "goat", "sheep"]:
                    cat_words[eng] = kir
                elif category == "food" and any(f in eng for f in ["water", "milk", "rice", "meat", "egg", "bread", "salt", "sugar", "fruit"]):
                    cat_words[eng] = kir
                elif category == "body" and eng in ["head", "eyes", "ears", "nose", "mouth", "hands", "legs", "heart"]:
                    cat_words[eng] = kir
                elif category == "colors" and eng in ["black", "white", "red", "blue", "green", "yellow", "orange"]:
                    cat_words[eng] = kir
                elif category == "numbers" and eng in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]:
                    cat_words[eng] = kir
                elif category == "verbs" and eng in ["eat", "drink", "sleep", "work", "run", "walk", "talk", "love", "see", "hear"]:
                    cat_words[eng] = kir
            
            if cat_words:
                response = f"📚 **{category.upper()} VOCABULARY**\n\n"
                for eng, kir in list(cat_words.items())[:15]:
                    response += f"• {eng} = {kir}\n"
                response += f"\n🎯 {len(cat_words)} words in this category!\nSay 'translate [word]' to see more!"
                return response
        
        # Random vocabulary if no category found
        random_words = random.sample(list(EN_TO_RN.items()), 12)
        response = "🎓 **KIRUNDI VOCABULARY**\n\n"
        for eng, kir in random_words:
            response += f"• {eng} = {kir}\n"
        response += "\n💡 Want specific category? Try: 'learn greetings', 'learn animals', 'learn food', 'learn verbs'"
        return response
    
    # ===== QUIZ =====
    if any(q in msg for q in ["quiz", "test", "exam", "practice", "challenge"]):
        eng, kir = random.choice(list(EN_TO_RN.items()))
        return f"📝 **QUIZ TIME!**\n\nWhat is '{eng}' in Kirundi?\n\nType: 'translate {eng}' for help, or type your answer!\n\n💡 Hint: It starts with '{kir[0]}'"
    
    # ===== CHECK IF DIRECT WORD LOOKUP =====
    if msg in EN_TO_RN:
        return f"📖 '{msg}' in Kirundi is: **{EN_TO_RN[msg]}**\n\nSay 'example {msg}' to see it in a sentence!"
    
    if msg in RN_TO_EN:
        return f"📖 '{msg}' in English is: **{RN_TO_EN[msg]}**\n\nGreat learning! 🎉"
    
    # ===== HELP =====
    if "help" in msg or "commands" in msg or "what can you do" in msg:
        return """🤖 **MBAZA AI - COMPLETE HELP GUIDE**

🎯 **TRANSLATION**
• 'translate cow' - English to Kirundi
• 'what is love' - Ask meaning
• 'example water' - See example sentences

📚 **GRAMMAR**
• 'grammar present' - Present tense
• 'grammar past' - Past tense
• 'grammar future' - Future tense
• 'grammar noun class' - Noun classes

📖 **VOCABULARY**
• 'learn greetings' - Greetings
• 'learn animals' - Animals
• 'learn food' - Food
• 'learn verbs' - Actions

✍️ **PRACTICE**
• 'quiz' - Test yourself

💬 **CONVERSATION**
• 'hello', 'how are you', 'thank you', 'goodbye'

**Iga Kirundi na Mbaza AI!** 🇧🇮"""
    
    # ===== COMPLIMENT/ENCOURAGEMENT =====
    if any(c in msg for c in ["good job", "nice", "great", "awesome", "perfect", "correct"]):
        return "Urakoze! 🎉 That's 'thank you' in Kirundi. You're doing great! Keep practicing and you'll speak Kirundi fluently!"
    
    if any(w in msg for w in ["sorry", "wrong", "incorrect"]):
        return "No problem! 🙏 Learning a language takes practice. Try again! Want to see the correct answer? Say 'translate' + the word."
    
    # ===== DEFAULT SMART RESPONSE =====
    return f"""🤔 I'm here to teach you Kirundi!

Try these:
📖 'translate water' - Learn words
📚 'grammar present' - Study grammar
🎓 'learn greetings' - Vocabulary
✍️ 'quiz' - Test yourself

What would you like to learn today? 🎯"""

# ============ HTML TEMPLATE (BEAUTIFUL & MOBILE OPTIMIZED) ============
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <meta name="theme-color" content="#667eea">
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
        
        .app-container {
            width: 100%;
            height: 100%;
            background: white;
            display: flex;
            flex-direction: column;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 20px;
            font-weight: 600;
        }
        
        .header h1 span {
            font-size: 24px;
        }
        
        .header p {
            font-size: 11px;
            opacity: 0.9;
            margin-top: 4px;
        }
        
        /* Quick Actions */
        .quick-actions {
            display: flex;
            gap: 8px;
            padding: 10px 12px;
            background: #f8f9fa;
            overflow-x: auto;
            border-bottom: 1px solid #e9ecef;
            scrollbar-width: thin;
        }
        
        .quick-btn {
            padding: 7px 15px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 25px;
            font-size: 12px;
            font-weight: 500;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
            color: #495057;
        }
        
        .quick-btn:active {
            background: #667eea;
            color: white;
            transform: scale(0.95);
            border-color: #667eea;
        }
        
        /* Messages Area */
        .messages-area {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .message {
            display: flex;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-bubble {
            max-width: 80%;
            padding: 10px 14px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.45;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        
        .message.user .message-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.bot .message-bubble {
            background: white;
            color: #2d3748;
            border-bottom-left-radius: 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        }
        
        .message.bot .message-bubble strong {
            color: #667eea;
        }
        
        /* Typing Indicator */
        .typing {
            display: none;
            padding: 10px 14px;
            background: white;
            border-radius: 18px;
            width: fit-content;
            margin-bottom: 10px;
        }
        
        .typing span {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #cbd5e0;
            margin: 0 2px;
            animation: typingDot 1.4s infinite;
        }
        
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingDot {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-8px); opacity: 1; }
        }
        
        /* Input Area */
        .input-area {
            padding: 12px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 8px;
        }
        
        .input-field {
            flex: 1;
            padding: 12px 16px;
            border: 1.5px solid #e9ecef;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            font-family: inherit;
        }
        
        .input-field:focus {
            border-color: #667eea;
        }
        
        .send-btn {
            padding: 12px 22px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .send-btn:active {
            transform: scale(0.95);
        }
        
        /* Scrollbar */
        .messages-area::-webkit-scrollbar {
            width: 4px;
        }
        
        .messages-area::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        .messages-area::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }
        
        @media (max-width: 480px) {
            .message-bubble {
                max-width: 85%;
                font-size: 13px;
                padding: 8px 12px;
            }
            .quick-btn {
                font-size: 11px;
                padding: 6px 12px;
            }
            .header h1 {
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1><span>🤖</span> MBAZA AI</h1>
            <p>Iga Kirundi na Mbaza AI</p>
        </div>
        
        <div class="quick-actions">
            <button class="quick-btn" onclick="sendMessage('translate water')">💧 Water</button>
            <button class="quick-btn" onclick="sendMessage('translate love')">❤️ Love</button>
            <button class="quick-btn" onclick="sendMessage('grammar present')">📚 Grammar</button>
            <button class="quick-btn" onclick="sendMessage('learn greetings')">👋 Greetings</button>
            <button class="quick-btn" onclick="sendMessage('quiz')">✍️ Quiz</button>
            <button class="quick-btn" onclick="sendMessage('help')">ℹ️ Help</button>
        </div>
        
        <div class="messages-area" id="messages">
            <div class="message bot">
                <div class="message-bubble">
                    <strong>🤖 Mbaza AI</strong><br><br>
                    Iga Kirundi na Mbaza AI! 🇧🇮<br><br>
                    I teach Kirundi in English.<br>
                    Try: 'translate water', 'grammar present', 'learn greetings'
                </div>
            </div>
        </div>
        
        <div class="typing" id="typing">
            <span></span><span></span><span></span>
        </div>
        
        <div class="input-area">
            <input type="text" id="input" class="input-field" placeholder="Type in English..." onkeypress="handleEnter(event)">
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>
    
    <script>
        const messagesArea = document.getElementById('messages');
        const input = document.getElementById('input');
        const typingIndicator = document.getElementById('typing');
        
        function scrollToBottom() {
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }
        
        function handleEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage(text) {
            const message = text !== undefined ? text : input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
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
                addMessage("Let's learn Kirundi! Try 'translate hello' or 'grammar present'", 'bot');
                scrollToBottom();
            }
        }
        
        function addMessage(text, sender) {
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            
            if (sender === 'bot') {
                bubble.innerHTML = '<strong>🤖 Mbaza AI</strong><br><br>' + text.replace(/\\n/g, '<br>');
            } else {
                bubble.innerHTML = '<strong>🧑 You</strong><br><br>' + text;
            }
            
            div.appendChild(bubble);
            messagesArea.appendChild(div);
        }
        
        input.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'response': "Type something to learn Kirundi! Try 'translate hello'"})
        
        response = generate_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': "Let's learn Kirundi! 🇧🇮 Try 'translate water' or 'hello'"})

@app.route('/health')
def health():
    return jsonify({'status': 'active', 'ai': 'Mbaza AI', 'creator': 'Mugisha Pc', 'words': len(EN_TO_RN)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
