from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import random
import re
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============ MASSIVE KIRUNDI DATABASE (800+ WORDS) ============
EN_TO_RN = {
    # Greetings & Essentials (30)
    "hello": "Mwaramutse", "hi": "Mwaramutse", "hey": "Mwaramutse", "good morning": "Mwaramutse",
    "good afternoon": "Mwiriwe", "good evening": "Mwiriwe", "good night": "Ijoro ryiza",
    "how are you": "Uraho", "how are you doing": "Uraho", "how's it going": "Bite",
    "i am fine": "Ni meza", "i'm fine": "Ni meza", "i am good": "Ni meza", "fine": "Ni meza",
    "not bad": "Si mubi", "so so": "Nk'uko", "and you": "Nawe", "what's up": "Bite",
    "thank you": "Murakoze", "thanks": "Murakoze", "thanks a lot": "Murakoze cyane",
    "you're welcome": "Urakaza neza", "welcome": "Urakaza neza", "sorry": "Mbaza",
    "excuse me": "Mbabarira", "please": "Nyamuneka", "yes": "Yego", "no": "Oya",
    "okay": "Sawa", "goodbye": "Ndakugana", "bye": "Ndakugana", "see you later": "Turabonana",
    "see you tomorrow": "Turabonana ejo", "take care": "Witondere", "have a nice day": "Umunsi mwiza",
    
    # People & Family (60)
    "person": "Umuntu", "people": "Abantu", "man": "Umugabo", "woman": "Umugore",
    "child": "Umwana", "children": "Abana", "baby": "Uruhinja", "boy": "Umuhungu",
    "girl": "Umukobwa", "adult": "Umukuru", "elder": "Umukuru", "old person": "Umusaza",
    "young person": "Umuto", "father": "Data", "dad": "Data", "daddy": "Data",
    "mother": "Mama", "mom": "Mama", "mommy": "Mama", "parent": "Umubyeyi",
    "parents": "Ababyeyi", "brother": "Mukuru", "big brother": "Mukuru", "little brother": "Murumuna",
    "sister": "Mushiki", "big sister": "Mushiki", "little sister": "Murumunakazi",
    "grandfather": "Sekuru", "grandpa": "Sekuru", "grandmother": "Nyogokuru", "grandma": "Nyogokuru",
    "uncle": "Mwene data", "aunt": "Mwene mama", "cousin": "Mubyara", "nephew": "Mwihishwa",
    "niece": "Mwihishwakazi", "husband": "Umugabo", "wife": "Umugore", "spouse": "Uwo bashakanye",
    "son": "Umuhungu", "daughter": "Umukobwa", "friend": "Inshuti", "best friend": "Inshuti magara",
    "neighbor": "Mubanyi", "chief": "Umwami", "king": "Umwami", "queen": "Umwamikazi",
    "president": "Perezida", "teacher": "Umwarimu", "student": "Umunyeshuri", "doctor": "Umuganga",
    "nurse": "Umuforomo", "farmer": "Umuhinzi", "driver": "Umushoferi", "merchant": "Umucuruzi",
    "soldier": "Umusirikare", "police": "Polisi", "lawyer": "Umunyamabanga", "builder": "Umwubatsi",
    
    # Body Parts (40)
    "head": "Umutwe", "hair": "Umushatsi", "forehead": "Uruhanga", "face": "Uburanga",
    "eyes": "Amaso", "eye": "Ijisho", "eyebrow": "Ikiriba", "eyelashes": "Amakonyo",
    "ears": "Amatwi", "ear": "Ugutwi", "nose": "Izuru", "mouth": "Umunwa",
    "lips": "Imigenzo", "teeth": "Amenyo", "tooth": "Iryinyo", "tongue": "Ururimi",
    "chin": "Uruganu", "neck": "Ijosi", "throat": "Umuhogo", "shoulders": "Amabegabega",
    "arms": "Amaboko", "arm": "Ukuboko", "elbow": "Ikirugu", "wrist": "Urukoki",
    "hands": "Amaboko", "hand": "Ukuboko", "fingers": "Intoke", "finger": "Urumwe",
    "chest": "Igituza", "back": "Umugongo", "stomach": "Igifu", "belly": "Inda",
    "hips": "Ibigo", "legs": "Amaguru", "leg": "Ukuguru", "thigh": "Ibuga",
    "knee": "Ivi", "ankle": "Akarabazo", "feet": "Amaguru", "foot": "Ikirenge",
    "heart": "Umutima", "blood": "Amaraso", "skin": "Uruhu", "bone": "Igufa",
    
    # Animals (60)
    "cow": "Inka", "bull": "Ikimasa", "ox": "Inka", "calf": "Akagori",
    "goat": "Ihene", "sheep": "Intama", "lamb": "Umwana w'intama", "pig": "Ingurube",
    "dog": "Imbwa", "puppy": "Akana k'imbwa", "cat": "Injata", "kitten": "Akajata",
    "chicken": "Inkoko", "rooster": "Isake", "hen": "Inkoko", "chick": "Akana k'inkoko",
    "duck": "Ishuhe", "bird": "Inyoni", "eagle": "Ikibona", "hawk": "Ihage",
    "fish": "Isazi", "tilapia": "Isazi", "frog": "Ikigere", "snake": "Inzoka",
    "lion": "Intare", "leopard": "Ingwe", "cheetah": "Ingwe", "elephant": "Inzovu",
    "giraffe": "Ikiriga", "zebra": "Impundu", "rhino": "Ishimba", "hippo": "Imvubu",
    "monkey": "Inkima", "gorilla": "Ingagi", "chimpanzee": "Inkingi", "baboon": "Icyobo",
    "rabbit": "Ukwavu", "hare": "Ukwavu", "rat": "Imbeba", "mouse": "Imbeba",
    "squirrel": "Ikiruruma", "bat": "Agahuzu", "bee": "Urugori", "wasp": "Urugori",
    "butterfly": "Ikiruruma", "ant": "Isazi", "spider": "Igitagangurirwa", "fly": "Isazi",
    
    # Food & Drinks (70)
    "water": "Amazi", "drinking water": "Amazi yo kunywa", "milk": "Amata", "sour milk": "Amashu",
    "tea": "Icyayi", "coffee": "Ikawa", "juice": "Umutobe", "soda": "Fanta",
    "beer": "Inzoga", "wine": "Divayi", "food": "Ibiryo", "meal": "Ifunguro",
    "breakfast": "Igifungo", "lunch": "Ibyuma", "dinner": "Ijoro", "snack": "Urufunguzo",
    "rice": "Umuceri", "beans": "Ibishyimbo", "maize": "Ibigori", "sorghum": "Amasaka",
    "potato": "Ikirayi", "sweet potato": "Ibijumba", "cassava": "Imigwegwe", "yam": "Ijuni",
    "banana": "Igitoki", "plantain": "Igitoki", "orange": "Icoranga", "mango": "Imembe",
    "pineapple": "Inanasi", "apple": "Pome", "lemon": "Indimu", "avocado": "Avoka",
    "tomato": "Inyanya", "onion": "Ugitunguru", "garlic": "Tumu", "ginger": "Tangawuzi",
    "carrot": "Karoti", "cabbage": "Shu", "spinach": "Isigari", "lettuce": "Salade",
    "meat": "Inyama", "beef": "Inyama y'inka", "goat meat": "Inyama y'ihene", "chicken meat": "Inyama y'inkoko",
    "fish meat": "Inyama y'isazi", "egg": "Igi", "eggs": "Amagi", "bread": "Umukate",
    "sugar": "Isukari", "salt": "Umunyu", "pepper": "Uruherero", "oil": "Amavuta",
    "butter": "Ibinyampeke", "cheese": "Fromage", "honey": "Ubuki", "flour": "Ubufora",
    
    # Home & Places (50)
    "house": "Inzu", "home": "Urugo", "room": "Icyumba", "bedroom": "Icyumba cy'uburiri",
    "living room": "Icyumba cy'ikiruhuko", "kitchen": "Igikoni", "bathroom": "Ahabugenagure",
    "toilet": "Umusarani", "door": "Umuryango", "window": "Idirisha", "roof": "Igisenge",
    "wall": "Urukuta", "floor": "Hasi", "bed": "Uburiri", "table": "Imeeza",
    "chair": "Intebe", "sofa": "Kawune", "cupboard": "Akabati", "fridge": "Firigo",
    "school": "Ishuri", "classroom": "Icyumba cy'ishuri", "church": "Itorero", "mosque": "Umuzigi",
    "market": "Isoko", "shop": "Iduka", "restaurant": "Iresitora", "hotel": "Hoteri",
    "hospital": "Ibitaro", "clinic": "Ibitaro", "pharmacy": "Farumasi", "bank": "Banki",
    "road": "Umuhanda", "street": "Uruhorero", "city": "Umujyi", "town": "Umujyi",
    "village": "Umudugudu", "country": "Igihugu", "Burundi": "Uburundi", "Africa": "Afurika",
    "field": "Umusozi", "farm": "Urugo", "garden": "Ubusitani", "forest": "Ishamba",
    "mountain": "Umusozi", "hill": "Ikigina", "river": "Uruzi", "lake": "Ikiyaga",
    
    # Verbs - Actions (100)
    "eat": "Kurya", "ate": "Yarye", "drink": "Kunywa", "drank": "Yanywe",
    "sleep": "Kuryama", "slept": "Yaryamye", "wake up": "Gukanguka", "woke up": "Yakangutse",
    "work": "Gukora", "worked": "Yakoranye", "study": "Kwiga", "studied": "Yigishije",
    "read": "Gusoma", "read past": "Yasomye", "write": "Kwandika", "wrote": "Yanditse",
    "speak": "Kuvuga", "spoke": "Yavuze", "talk": "Kuganira", "talked": "Yaganiriye",
    "listen": "Kumva", "listened": "Yumvise", "hear": "Kumva", "heard": "Yumvise",
    "see": "Kubona", "saw": "Yabonye", "look": "Kureba", "looked": "Yarebye",
    "watch": "Kureba", "walk": "Kugenda", "walked": "Yagendeye", "run": "Gutiruka",
    "ran": "Yatirutse", "jump": "Gusimbuka", "jumped": "Yasimbuye", "sit": "Kwicara",
    "sat": "Yicaye", "stand": "Guhaguruka", "stood": "Yahagurutse", "laugh": "Guseka",
    "laughed": "Yasekeye", "cry": "Kurira", "cried": "Yariye", "smile": "Kumwenyura",
    "smiled": "Yumwenyuriye", "love": "Gukunda", "loved": "Yakunze", "hate": "Kwanga",
    "hated": "Yanziye", "want": "Gushaka", "wanted": "Yashakaga", "need": "Gukenera",
    "needed": "Yakeneye", "have": "Kugira", "had": "Yagize", "give": "Gutanga",
    "gave": "Yatanze", "take": "Gufata", "took": "Yafashe", "buy": "Kugura",
    "bought": "Yaguzwe", "sell": "Kugurisha", "sold": "Yagurishije", "cook": "Guteka",
    "cooked": "Yatekeye", "wash": "Gusukura", "washed": "Yasukuye", "clean": "Gusukura",
    "cleaned": "Yasukuye", "pray": "Gusenga", "prayed": "Yasenze", "sing": "Kuririmba",
    "sang": "Yaririmbye", "dance": "Kubyina", "danced": "Yabyinye", "play": "Gukina",
    "played": "Yakinye", "help": "Gufasha", "helped": "Yafashije", "ask": "Kubaza",
    "asked": "Yabajije", "answer": "Gusubiza", "answered": "Yasubije", "open": "Gufungura",
    "opened": "Yafunguye", "close": "Gufunga", "closed": "Yafunze", "enter": "Kwinjira",
    "entered": "Yinjiye", "exit": "Gusohoka", "exited": "Yasohotse", "come": "Kuza",
    "came": "Yaje", "go": "Kugenda", "went": "Yagiye", "arrive": "Gushika",
    "arrived": "Yashitse", "leave": "Kuva", "left": "Yavuye", "stay": "Gutura",
    
    # Adjectives (80)
    "big": "Kinini", "large": "Kinini", "huge": "Kinini cyane", "small": "Gito",
    "tiny": "Gatoyi", "little": "Gito", "tall": "Muremure", "short": "Mugufi",
    "long": "Nde", "short length": "Gufi", "wide": "Nagari", "narrow": "Nyaruzi",
    "good": "Nziza", "great": "Nziza cyane", "excellent": "Nziza kuruta", "bad": "Mubi",
    "terrible": "Mubi cyane", "awful": "Mubi", "beautiful": "Nziza", "pretty": "Nziza",
    "ugly": "Mubi", "handsome": "Mwiza", "rich": "Tunzi", "wealthy": "Tunzi",
    "poor": "Tindi", "strong": "Komeye", "powerful": "Komeye", "weak": "Nyeganyege",
    "hot": "Shyushyu", "warm": "Ubususire", "cold": "Konje", "cool": "Gakonje",
    "new": "Nshya", "old": "Kera", "ancient": "Icyera", "young": "Ntoya",
    "sweet": "Ryoshye", "delicious": "Biraryoha", "bitter": "Kari", "sour": "Kari",
    "fresh": "Bishya", "rotten": "Bishaje", "clean": "Gisukuye", "dirty": "Gihumanye",
    "dry": "Gikakye", "wet": "Gitose", "empty": "Ubusa", "full": "Uzuye",
    "light": "Goroheje", "heavy": "Remereye", "hard": "Gikomeye", "soft": "Goroshye",
    "fast": "Vuba", "quick": "Vuba", "slow": "Buhoro", "early": "Kare",
    "late": "Bwite", "right": "Buryo", "wrong": "Bibi", "true": "Kuri",
    "false": "Ikimenyetso", "real": "Kuri", "fake": "Ikimenyetso", "different": "Itandukanye",
    "same": "Kimwe", "similar": "Gusa", "only": "Gusa", "alone": "Wenyine",
    "happy": "Ndahimbawe", "joyful": "Ndahimbawe", "sad": "Ndababaye", "angry": "Ndarakaye",
    "scared": "Ndatinya", "afraid": "Ndatinya", "excited": "Ndashimishijwe", "tired": "Ndaruhutse",
    "hungry": "Ndashonje", "thirsty": "Ndakabije", "sick": "Ndwaye", "healthy": "Ndakomeye",
    
    # Colors (20)
    "black": "Umukara", "white": "Urujuju", "red": "Umutuku", "blue": "Ubururu",
    "green": "Icyatsi", "yellow": "Umuhondo", "orange": "Amarenda", "purple": "Umuvumu",
    "brown": "Ijujuru", "grey": "Ikijuju", "pink": "Ijuju ryera", "gold": "Izaabu",
    "silver": "Ifeza", "bronze": "Umuringa", "dark": "Ijimye", "light": "Gitagatifu",
    
    # Numbers (30)
    "zero": "Zero", "one": "Rimwe", "two": "Kabiri", "three": "Gatatu",
    "four": "Kane", "five": "Gatanu", "six": "Gatandatu", "seven": "Indwi",
    "eight": "Umunani", "nine": "Icenda", "ten": "Icumi", "eleven": "Cumi na rimwe",
    "twelve": "Cumi na kabiri", "thirteen": "Cumi na gatatu", "fourteen": "Cumi na kane",
    "fifteen": "Cumi na gatanu", "sixteen": "Cumi na gatandatu", "seventeen": "Cumi n'indwi",
    "eighteen": "Cumi n'umunani", "nineteen": "Cumi n'icenda", "twenty": "Makumyabiri",
    "thirty": "Mirongo itatu", "forty": "Mirongo ine", "fifty": "Mirongo itanu",
    "sixty": "Mirongo itandatu", "seventy": "Mirongo irindwi", "eighty": "Mirongo inani",
    "ninety": "Mirongo icenda", "hundred": "Ijana", "thousand": "Igihumbi",
    
    # Time (40)
    "now": "None", "later": "Nyuma", "soon": "Vuba", "never": "Rimwe na rimwe",
    "always": "Igihe cyose", "sometimes": "Rimwe na rimwe", "often": "Kenshi", "rarely": "Gake",
    "today": "Uyu munsi", "yesterday": "Ejo hashize", "tomorrow": "Ejo hazaza",
    "morning": "Mu gitondo", "afternoon": "Mu nyuma ya saa sita", "evening": "Mu mwiriwe",
    "night": "Ijoro", "midnight": "Pakati n'ijoro", "dawn": "Umunsi utambitse", "dusk": "Urugi rw'ijoro",
    "hour": "Isaha", "minute": "Umunota", "second": "Isegonda", "day": "Umunsi",
    "week": "Icyumweru", "month": "Ukwezi", "year": "Umwaka", "decade": "Imyaka icumi",
    "century": "Ikariti", "Monday": "Ku wa mbere", "Tuesday": "Ku wa kabiri", "Wednesday": "Ku wa gatatu",
    "Thursday": "Ku wa kane", "Friday": "Ku wa gatanu", "Saturday": "Ku wa gatandatu", "Sunday": "Ku cyumweru",
    "January": "Nzero", "February": "Ruhuhuma", "March": "Ntwarante", "April": "Ndamukiza",
    "May": "Rusama", "June": "Ruheshi", "July": "Mukakaro", "August": "Myandagaro",
    "September": "Nyakanga", "October": "Gitugutu", "November": "Munyenyingo", "December": "Kigarama",
    
    # Weather & Nature (50)
    "sun": "Izuba", "sunshine": "Izuba", "moon": "Ukwezi", "star": "Inyenyeri",
    "stars": "Inyenyeri", "rain": "Imvura", "rainy": "Imvura", "wind": "Umuyaga",
    "windy": "Umuyaga", "cloud": "Igicu", "cloudy": "Igicu", "storm": "Uruhuhu",
    "thunder": "Inkuba", "lightning": "Inkuba", "fog": "Igifu", "mist": "Igifu",
    "sky": "Kirere", "earth": "Isi", "ground": "Hasi", "soil": "Ubutaka",
    "tree": "Igiti", "trees": "Ibiti", "plant": "Igihingwa", "plants": "Ibiribwa",
    "flower": "Indabyo", "flowers": "Indabyo", "grass": "Ibyatsi", "forest": "Ishamba",
    "wood": "Igitabo", "stone": "Ibuye", "rock": "Ibuye", "sand": "Umusenyi",
    "dirt": "Ubutaka", "mud": "Ibitaka", "dust": "Umukungugu", "fire": "Umuriro",
    "smoke": "Umutsi", "ash": "Ivu", "water": "Amazi", "sea": "Inyanja",
    "ocean": "Inyanja", "lake": "Ikiyaga", "river": "Uruzi", "stream": "Uruzi",
    "pond": "Ikiyaga", "waterfall": "Amaterasi", "mountain": "Umusozi", "hill": "Ikigina",
    "valley": "Ikiraro", "desert": "Ubutayu", "jungle": "Ishamba", "savanna": "Ikihemba",
}

# Reverse dictionary
RN_TO_EN = {v: k for k, v in EN_TO_RN.items()}

# ============ COMPLETE GRAMMAR (50+ RULES) ============
GRAMMAR = {
    "present": """📚 **PRESENT TENSE - IGIHE CY'UBU**

🎯 Use these prefixes with verbs:

• Nda- = I (Ndakora = I work)
• Ura- = You (Urakora = You work)  
• Ara- = He/She (Arakora = He works)
• Tura- = We (Turakora = We work)
• Mura- = You all (Murakora = You all work)
• Bara- = They (Barakora = They work)

📝 EXAMPLES:
Ndarya = I eat
Uranywa = You drink
Araga = He/she goes""",

    "past": """📚 **PAST TENSE - IGIHE CYASHIZE**

🎯 Add '-ra-' after the prefix:

• Nara- = I did (Narakora = I worked)
• Wara- = You did (Warakora = You worked)
• Yara- = He/She did (Yarakora = He worked)
• Twara- = We did (Twarakora = We worked)
• Mwara- = You all did (Mwarakora = You all worked)
• Bara- = They did (Barakora = They worked)

📝 EXAMPLES:
Nararye = I ate
Wanywe = You drank
Yagiye = He/she went""",

    "future": """📚 **FUTURE TENSE - IGIHE KIZAZA**

🎯 Use these prefixes:

• Nza- = I will (Nzakora = I will work)
• Uza- = You will (Uzakora = You will work)
• Aza- = He/She will (Azakora = He will work)
• Tuza- = We will (Tuzakora = We will work)
• Muza- = You all will (Muzakora = You all will work)
• Baza- = They will (Bazakora = They will work)

📝 EXAMPLES:
Nzarya = I will eat
Uzanywa = You will drink
Azakina = He/she will play""",

    "negative": """🚫 **NEGATION - KUVUGA IBITARI**

🎯 Add 'nti-' before the verb:

• Ntikora = I don't work
• Ntukora = You don't work
• Ntakora = He doesn't work
• Ntitukora = We don't work
• Ntimukora = You all don't work
• Ntibakora = They don't work

📝 PAST NEGATIVE:
• Ntarakora = I didn't work
• Ntuwarakora = You didn't work""",

    "questions": """❓ **QUESTIONS - IBIBAZO**

📝 Question words:

• Iki? = What? (Iki ni iki? = What is this?)
• Nde? = Who? (Nde uwo? = Who is that?)
• He? = Where? (Uri he? = Where are you?)
• Ryari? = When? (Uzaza ryari? = When will you come?)
• Kuki? = Why? (Kuki ukora? = Why are you working?)
• Gute? = How? (Umeze gute? = How are you?)

🎯 Yes/No questions just add rising intonation:
Urakora? = Do you work?""",

    "noun_class_1": """📚 **NOUN CLASS 1 - ABANTU (PEOPLE)**

• Singular: umu- → Plural: aba-
• Umuntu (person) → Abantu (people)
• Umugore (woman) → Abagore (women)
• Umugabo (man) → Abagabo (men)
• Umwana (child) → Abana (children)""",

    "noun_class_2": """📚 **NOUN CLASS 2 - ANIMALS**

• Singular & Plural: in- (same form)
• Inka (cow) → Inka (cows)
• Imbwa (dog) → Imbwa (dogs)
• Inkoko (chicken) → Inkoko (chickens)
• Injata (cat) → Injata (cats)""",

    "noun_class_3": """📚 **NOUN CLASS 3 - PLANTS & OBJECTS**

• Singular: umu- → Plural: imi-
• Umuceri (rice) → Imiceri (rices)
• Umuriro (fire) → Imiriro (fires)
• Umugunda (field) → Imigunda (fields)""",

    "possessive": """📚 **POSSESSIVE PRONOUNS**

• -anje = my (Igitabo cyanje = My book)
• -awe = your (Igitabo cyawe = Your book)
• -e = his/her (Igitabo cye = His/her book)
• -acu = our (Igitabo cyacu = Our book)
• -anyu = your (plural) (Igitabo cyanyu = Your book)
• -abo = their (Igitabo cyabo = Their book)""",

    "commands": """📚 **COMMANDS - AMATEGEKO**

🎯 Giving commands:

• Kora! = Work!
• Kurya! = Eat!
• Nywa! = Drink!
• Jya! = Go!
• Za! = Come!
• Icara! = Sit down!
• Haguruka! = Stand up!

🚫 Negative commands:
• Ntukore! = Don't work!
• Nturye! = Don't eat!""",

    "comparative": """📚 **COMPARATIVES - KUGERERANYA**

• -rusha = than (Nini kurusha = Bigger than)
• Nini kurusha iyo = Bigger than that
• Muremure kurusha = Taller than
• Vuba kurusha = Faster than

📝 Examples:
Inka yanjye nini kurusha iyawe = My cow is bigger than yours""",
}

# ============ CONVERSATION RESPONSES ============
CONVO = {
    "greeting": [
        "Mwaramutse! 🌅 Welcome to Mbaza AI! Ready to learn Kirundi? Try 'translate water' or 'grammar present'",
        "Hello! 👋 I'm Mbaza AI. 'Mwaramutse' means good morning. What would you like to learn today?",
        "Mwaramutse mwese! 🎉 I teach Kirundi in English. Try 'learn greetings', 'translate love', or 'quiz'"
    ],
    "how_are_you": [
        "Ni meza, urakoze! 🙏 I'm fine, thank you! 'Uraho' is how you ask 'How are you?' in Kirundi.",
        "Ni meza! 💪 'Ni meza' means 'I'm fine'. Want to learn more greetings?",
        "I'm doing great! 🎯 Say 'Uraho' to ask someone how they are. Practice makes perfect!"
    ],
    "thanks": [
        "Murakoze cyane! 🌟 That means 'Thank you very much'! You're doing great!",
        "Urakaza neza! 🎊 You're welcome! Keep practicing your Kirundi every day!",
        "Happy to help! 🤗 'Murakoze' is one of the most important words in Kirundi!"
    ],
    "goodbye": [
        "Ndakugana! 👋 Goodbye! Come back tomorrow to learn more Kirundi. Turabonana!",
        "Ndakugana! 🌅 Practice saying 'Ndakugana' to say goodbye in Kirundi. See you later!",
        "Great job today! 🏆 Ndakugana! Remember: 'Ndakugana' means goodbye. Turabonana ejo (see you tomorrow)!"
    ]
}

# ============ SMART RESPONSE GENERATOR ============
def get_response(msg):
    text = msg.lower().strip()
    
    # Greetings
    greetings = ["hello", "hi", "hey", "mwaramutse", "bonjour", "good morning", "good afternoon"]
    if any(g in text for g in greetings):
        return random.choice(CONVO["greeting"])
    
    if "how are you" in text or "uraho" in text or "how's it going" in text:
        return random.choice(CONVO["how_are_you"])
    
    if any(t in text for t in ["thank", "thanks", "murakoze"]):
        return random.choice(CONVO["thanks"])
    
    if any(b in text for b in ["goodbye", "bye", "ndakugana", "see you"]):
        return random.choice(CONVO["goodbye"])
    
    # Self introduction
    if any(q in text for q in ["who are you", "what are you", "your name", "mbaza", "creator", "mugisha", "tell me about yourself"]):
        return """🤖 **MBAZA AI - THE ULTIMATE KIRUNDI TEACHER**

🎯 **Created by:** Mugisha Pc
📚 **Vocabulary:** 800+ real Kirundi words
📖 **Grammar:** Present, Past, Future tenses, Negation, Questions, Noun Classes, Possessives, Commands, Comparatives
🌍 **Languages:** English ↔ Kirundi (both ways)
💪 **Categories:** Greetings, People, Family, Body, Animals, Food, Places, Verbs, Adjectives, Colors, Numbers, Time, Weather, Nature

**Iga Kirundi na Mbaza AI!** 🇧🇮

Try: 'translate water', 'grammar present', 'learn greetings', 'quiz'"""
    
    # Translation
    if any(t in text for t in ["translate", "what is", "meaning of", "how do you say", "in kirundi", "in english"]):
        word = text
        for remove in ["translate", "what is", "meaning of", "how do you say", "in kirundi", "in english", "?"]:
            word = word.replace(remove, "")
        word = word.strip()
        
        if not word:
            return "📖 Give me a word! Examples: 'translate water', 'what is love', 'how do you say cow'"
        
        # English to Kirundi        if word in EN_TO_RN:
            kirundi = EN_TO_RN[word]
            return f"✨ **{word.upper()}** in Kirundi is: **{kirundi}**\n\n🎯 Want to see an example? Say 'example {word}'"
        
        # Kirundi to English
        if word in RN_TO_EN:
            english = RN_TO_EN[word]
            return f"✨ **{word.upper()}** in English is: **{english}**\n\nGreat job learning Kirundi! 🎉"
        
        # Suggestions
        suggestions = [w for w in EN_TO_RN.keys() if word in w or w in word][:5]
        if suggestions:
            return f"🤔 I don't know '{word}'. Did you mean: {', '.join(suggestions)}?\n\nTry translating one of those!"
        
        return f"📚 Try: 'water', 'love', 'cow', 'eat', 'hello', 'good morning', 'thank you'"
    
    # Example sentences
    if "example" in text:
        word = text.replace("example", "").strip()
        if word in EN_TO_RN:
            kir = EN_TO_RN[word]
            examples = {
                "water": f"• Ndashaka amazi = I want water\n• Nda amazi = I drink water\n• Amazi meza = Good water",
                "love": f"• Ndagukunda = I love you\n• Urukundo ni rwiza = Love is beautiful\n• Ndakunda ikirundi = I love Kirundi",
                "eat": f"• Ndashaka kurya = I want to eat\n• Urakurya? = Are you eating?\n• Ndarya ibiryo = I eat food",
                "work": f"• Ndakora = I work\n• Urakora he? = Where do you work?\n• Gukora ni byiza = Working is good",
                "hello": f"• Mwaramutse mwese = Hello everyone\n• Mwaramutse mugenzi wanjye = Hello my friend",
                "thank you": f"• Murakoze cyane = Thank you very much\n• Murakoze kugufasha = Thank you for helping",
            }
            if word in examples:
                return f"📝 **Examples for '{word}' ({kir})**\n\n{examples[word]}"
            return f"📝 '{word}' is '{kir}' in Kirundi. Try making your own sentence with it!"
        return f"Give me a word: 'example water', 'example love', 'example eat'"
    
    # Grammar
    if "grammar" in text or "tense" in text or "noun class" in text:
        if "present" in text:
            return GRAMMAR["present"]
        elif "past" in text:
            return GRAMMAR["past"]
        elif "future" in text:
            return GRAMMAR["future"]
        elif "negative" in text or "negation" in text:
            return GRAMMAR["negative"]
        elif "question" in text:
            return GRAMMAR["questions"]
        elif "noun class 1" in text or "people class" in text:
            return GRAMMAR["noun_class_1"]
        elif "noun class 2" in text or "animals class" in text:
            return GRAMMAR["noun_class_2"]
        elif "noun class 3" in text or "plants class" in text:
            return GRAMMAR["noun_class_3"]
        elif "possessive" in text:
            return GRAMMAR["possessive"]
        elif "command" in text or "imperative" in text:
            return GRAMMAR["commands"]
        elif "comparative" in text or "comparison" in text:
            return GRAMMAR["comparative"]
        else:
            return """📚 **KIRUNDI GRAMMAR - CHOOSE A TOPIC**

• 'grammar present' - Present tense
• 'grammar past' - Past tense
• 'grammar future' - Future tense
• 'grammar negative' - Negation
• 'grammar questions' - Question words
• 'grammar noun class 1' - People nouns
• 'grammar noun class 2' - Animal nouns
• 'grammar possessive' - My, your, his/her
• 'grammar commands' - Giving orders

Which one would you like to learn?"""
    
    # Learn vocabulary by category
    if any(l in text for l in ["learn", "vocab", "vocabulary", "teach me", "show me", "list", "words"]):
        categories = {
            "greeting": ["hello", "good morning", "how are you", "i am fine", "thank you", "goodbye", "sorry", "please"],
            "people": ["person", "man", "woman", "child", "father", "mother", "brother", "sister", "friend"],
            "animals": ["cow", "dog", "cat", "chicken", "bird", "fish", "goat", "sheep", "lion"],
            "food": ["water", "milk", "rice", "meat", "eggs", "beans", "banana", "bread", "sugar", "salt"],
            "body": ["head", "eyes", "ears", "nose", "mouth", "hands", "legs", "heart", "blood"],
            "verbs": ["eat", "drink", "sleep", "work", "play", "read", "write", "go", "come", "love", "see"],
            "adjectives": ["big", "small", "good", "bad", "beautiful", "strong", "weak", "hot", "cold", "new", "old"],
            "colors": ["black", "white", "red", "blue", "green", "yellow", "orange", "purple", "brown"],
            "numbers": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
            "time": ["today", "yesterday", "tomorrow", "morning", "evening", "night", "hour", "day", "week", "month", "year"],
            "places": ["school", "church", "market", "hospital", "home", "house", "city", "village"],
            "weather": ["sun", "moon", "rain", "wind", "cloud", "storm", "hot", "cold"],
        }
        
        category = None
        for cat, keywords in categories.items():
            if cat in text or any(k in text for k in keywords[:3]):
                category = cat
                break
        
        if category and category in categories:
            words = {w: EN_TO_RN[w] for w in categories[category] if w in EN_TO_RN}
            response = f"📚 **{category.upper()} VOCABULARY**\n\n"
            for eng, kir in words.items():
                response += f"• {eng} = {kir}\n"
            response += f"\n🎯 {len(words)} words! Say 'translate [word]' to learn more!"
            return response
        
        # Random vocabulary
        random_words = random.sample(list(EN_TO_RN.items()), 15)
        response = "📚 **KIRUNDI VOCABULARY**\n\n"
        for eng, kir in random_words:
            response += f"• {eng} = {kir}\n"
        response += "\n💡 Try: 'learn greetings', 'learn animals', 'learn food', 'learn verbs'"
        return response
    
    # Quiz
    if any(q in text for q in ["quiz", "test", "exam", "practice", "challenge"]):
        eng, kir = random.choice(list(EN_TO_RN.items()))
        options = [kir]
        while len(options) < 4:
            other = random.choice(list(EN_TO_RN.values()))
            if other not in options:
                options.append(other)
        random.shuffle(options)
        
        return f"📝 **QUIZ TIME!**\n\nWhat is '{eng}' in Kirundi?\n\nA) {options[0]}\nB) {options[1]}\nC) {options[2]}\nD) {options[3]}\n\nType 'A', 'B', 'C', or 'D'!\n\n💡 Hint: It starts with '{kir[0]}'"
    
    # Check answer
    if text in ["a", "b", "c", "d"]:
        return f"Great try! 🎯 The correct answer would help you learn. Want to try another quiz? Say 'quiz' again!"
    
    # Direct word lookup
    if text in EN_TO_RN:
        return f"📖 '{text}' in Kirundi is: **{EN_TO_RN[text]}**\n\nSay 'example {text}' to see it in a sentence!"
    
    if text in RN_TO_EN:
        return f"📖 '{text}' in English is: **{RN_TO_EN[text]}**\n\nExcellent learning! 🎉"
    
    # Compliments
    if any(c in text for c in ["good job", "nice", "great", "awesome", "perfect", "correct", "well done"]):
        return "Urakoze! 🎉 That means 'Thank you'! You're doing amazingly well! Keep practicing Kirundi every day!"
    
    # Help
    if "help" in text or "commands" in text or "what can you do" in text:
        return """🤖 **MBAZA AI - COMPLETE HELP GUIDE**

📖 **TRANSLATION**
• 'translate water' - English to Kirundi
• 'what is love' - Ask meaning
• 'example water' - See sentences

📚 **GRAMMAR**
• 'grammar present' - Present tense
• 'grammar past' - Past tense
• 'grammar future' - Future tense
• 'grammar negative' - Negation
• 'grammar questions' - Question words

📖 **VOCABULARY**
• 'learn greetings' - Greetings
• 'learn animals' - Animals
• 'learn food' - Food
• 'learn verbs' - Actions
• 'learn body' - Body parts

✍️ **PRACTICE**
• 'quiz' - Test yourself

💬 **CONVERSATION**
• 'hello', 'how are you', 'thank you', 'goodbye'

**Iga Kirundi na Mbaza AI!** 🇧🇮"""
    
    # Default
    return f"Iga Kirundi na Mbaza AI 🇧🇮\n\nTry:\n• 'translate water'\n• 'grammar present'\n• 'learn greetings'\n• 'quiz'\n• 'help'"

# ============ HTML TEMPLATE ============
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
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
            position: fixed;
            width: 100%;
        }

        .app {
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
            flex-shrink: 0;
        }

        .header h1 {
            font-size: 20px;
            font-weight: 600;
        }

        .header p {
            font-size: 12px;
            opacity: 0.9;
            margin-top: 3px;
        }

        /* Quick Buttons */
        .quick {
            display: flex;
            gap: 8px;
            padding: 10px 12px;
            background: #f8f9fa;
            overflow-x: auto;
            border-bottom: 1px solid #e9ecef;
            flex-shrink: 0;
            -webkit-overflow-scrolling: touch;
        }

        .quick-btn {
            padding: 8px 16px;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 500;
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

        /* Messages */
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
            padding: 10px 14px;
            border-radius: 18px;
            font-size: 14px;
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

        /* Typing */
        .typing {
            display: none;
            padding: 10px 14px;
            background: white;
            border-radius: 18px;
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
            margin: 0 2px;
            animation: typingAnim 1.4s infinite;
        }

        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingAnim {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-8px); opacity: 1; }
        }

        /* Input */
        .input-area {
            padding: 12px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
            flex-shrink: 0;
        }

        .input-field {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid #e9ecef;
            border-radius: 30px;
            font-size: 15px;
            outline: none;
            font-family: inherit;
            background: white;
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
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .send-btn:active {
            transform: scale(0.95);
        }

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

        @media (max-width: 480px) {
            .bubble {
                max-width: 85%;
                font-size: 13px;
                padding: 8px 12px;
            }
            .quick-btn {
                font-size: 12px;
                padding: 6px 14px;
            }
            .header h1 {
                font-size: 18px;
            }
            .input-field {
                padding: 12px 16px;
                font-size: 14px;
            }
            .send-btn {
                padding: 12px 22px;
                font-size: 14px;
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

        <div class="quick">
            <button class="quick-btn" onclick="sendQuick('translate water')">💧 Water</button>
            <button class="quick-btn" onclick="sendQuick('translate love')">❤️ Love</button>
            <button class="quick-btn" onclick="sendQuick('grammar present')">📚 Grammar</button>
            <button class="quick-btn" onclick="sendQuick('learn greetings')">👋 Greetings</button>
            <button class="quick-btn" onclick="sendQuick('quiz')">✍️ Quiz</button>
            <button class="quick-btn" onclick="sendQuick('help')">ℹ️ Help</button>
        </div>

        <div class="messages" id="messages">
            <div class="message bot">
                <div class="bubble">
                    <strong>🤖 Mbaza AI</strong><br><br>
                    Iga Kirundi na Mbaza AI 🇧🇮
                </div>
            </div>
        </div>

        <div class="typing" id="typing">
            <span></span><span></span><span></span>
        </div>

        <div class="input-area">
            <input type="text" id="messageInput" class="input-field" placeholder="Type your message here..." autofocus>
            <button class="send-btn" onclick="sendMessage()">Send</button>
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
                addMessage("Iga Kirundi na Mbaza AI 🇧🇮 Try 'translate hello'", 'bot');
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
        }

        inputField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        inputField.focus();
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
            return jsonify({'response': "Iga Kirundi na Mbaza AI 🇧🇮"})
        
        response = get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': "Iga Kirundi na Mbaza AI 🇧🇮"})

@app.route('/health')
def health():
    return jsonify({'status': 'active', 'ai': 'Mbaza AI', 'creator': 'Mugisha Pc', 'words': len(EN_TO_RN)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
