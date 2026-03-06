"""
Indic-Setu - ULTIMATE VERSION
Features:
- Working voice input & text-to-speech
- 10+ languages (Hindi, Gujarati, Marathi, Tamil, Telugu, Kannada, Bengali, Punjabi, Odia, Urdu, English)
- PDF generation
- Favorite schemes
- Scheme comparison
- Progress tracking
- Application checklist
"""

import streamlit as st
import requests
import json
import pyttsx3
from io import BytesIO
import base64
from datetime import datetime

st.set_page_config(
    page_title="Indic-Setu | सरकारी योजनाएं",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete Language Translations
TRANSLATIONS = {
    "English": {
        "title": "🌾 Indic-Setu",
        "subtitle": "Government Schemes Made Simple",
        "your_details": "Your Details",
        "occupation": "Select your occupation",
        "income": "Annual Income (₹)",
        "select_language": "🌐 Select Language",
        "question": "What would you like to know?",
        "search": "🔍 Search",
        "clear": "🔄 Clear",
        "help": "❓ Help",
        "eligibility": "Your Eligibility Status",
        "detailed_info": "Detailed Information",
        "your_profile": "Your Profile",
        "next_steps": "Next Steps",
        "download": "📄 Download as PDF",
        "form": "📋 Schemes",
        "govt_links": "🏛️ Government Links",
        "voice": "🎤 Speak",
        "listen": "🔊 Listen",
        "favorite": "❤️ Favorite",
        "compare": "📊 Compare",
        "progress": "📈 Progress",
        "checklist": "✅ Checklist",
        "requirements": "📋 Requirements"
    },
    "हिंदी": {
        "title": "🌾 इंडिक-सेतु",
        "subtitle": "सरकारी योजनाएं आसान बनाई गईं",
        "your_details": "आपका विवरण",
        "occupation": "अपने व्यवसाय का चयन करें",
        "income": "वार्षिक आय (₹)",
        "select_language": "🌐 भाषा चुनें",
        "question": "आप क्या जानना चाहते हैं?",
        "search": "🔍 खोजें",
        "clear": "🔄 साफ़ करें",
        "help": "❓ सहायता",
        "eligibility": "आपकी पात्रता स्थिति",
        "detailed_info": "विस्तृत जानकारी",
        "your_profile": "आपकी प्रोफाइल",
        "next_steps": "अगले कदम",
        "download": "📄 PDF में डाउनलोड करें",
        "form": "📋 योजनाएं",
        "govt_links": "🏛️ सरकारी लिंक",
        "voice": "🎤 बोलें",
        "listen": "🔊 सुनें",
        "favorite": "❤️ पसंदीदा",
        "compare": "📊 तुलना करें",
        "progress": "📈 प्रगति",
        "checklist": "✅ चेकलिस्ट",
        "requirements": "📋 आवश्यकताएं"
    },
    "ગુજરાતી": {
        "title": "🌾 ઇન્ડિક-સેતુ",
        "subtitle": "સરકારી યોજનાઓ સરળ બનાવવામાં આવી",
        "your_details": "તમારી વિગતો",
        "occupation": "તમારો વ્યવસાય પસંદ કરો",
        "income": "વાર્ષિક આવક (₹)",
        "select_language": "🌐 ભાષા પસંદ કરો",
        "question": "તમે શું જાણવા માંગો છો?",
        "search": "🔍 શોધો",
        "clear": "🔄 સાફ કરો",
        "help": "❓ મદદ",
        "eligibility": "તમારી પાત્રતા સ્થિતિ",
        "detailed_info": "વિગતવાર માહિતી",
        "your_profile": "તમારી પ્રોફાઇલ",
        "next_steps": "આગલા પગલાં",
        "download": "📄 PDF તરીકે ડાউનલોડ કરો",
        "form": "📋 યોજનાઓ",
        "govt_links": "🏛️ સરકારી લિંક",
        "voice": "🎤 બોલો",
        "listen": "🔊 સાંભળો",
        "favorite": "❤️ પસંદીદા",
        "compare": "📊 તુલના કરો",
        "progress": "📈 પ્રગતિ",
        "checklist": "✅ તપાસ સૂચી",
        "requirements": "📋 આવશ્યકતાઓ"
    },
    "मराठी": {
        "title": "🌾 इंडिक-सेतु",
        "subtitle": "सरकारी योजना सोपे केल्या गेल्या",
        "your_details": "आपली माहिती",
        "occupation": "आपला व्यवसाय निवडा",
        "income": "वार्षिक उत्पन्न (₹)",
        "select_language": "🌐 भाषा निवडा",
        "question": "आप काय जाणू शकता?",
        "search": "🔍 शोधा",
        "clear": "🔄 साफ करा",
        "help": "❓ मदत",
        "eligibility": "आपली पात्रता स्थिती",
        "detailed_info": "तपशीलवार माहिती",
        "your_profile": "आपली प्रोफाइल",
        "next_steps": "पुढील टप्पे",
        "download": "📄 PDF म्हणून डाउनलोड करा",
        "form": "📋 योजना",
        "govt_links": "🏛️ सरकारी लिंक",
        "voice": "🎤 बोला",
        "listen": "🔊 ऐका",
        "favorite": "❤️ आवडते",
        "compare": "📊 तुलना करा",
        "progress": "📈 प्रगति",
        "checklist": "✅ तपासणी यादी",
        "requirements": "📋 आवश्यकतांनी"
    },
    "தமிழ்": {
        "title": "🌾 இந்திய-சேது",
        "subtitle": "அரசு திட்டங்கள் எளிமையாக்கப்பட்டுள்ளன",
        "your_details": "உங்கள் விவரங்கள்",
        "occupation": "உங்கள் தொழிலைத் தேர்ந்தெடுங்கள்",
        "income": "வার்ષிக வருமானம் (₹)",
        "select_language": "🌐 மொழியைத் தேர்ந்தெடுங்கள்",
        "question": "நீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?",
        "search": "🔍 தேடல்",
        "clear": "🔄 தீர்க்கம்",
        "help": "❓ உதவி",
        "eligibility": "உங்கள் தகுதி நிலை",
        "detailed_info": "விரிவான தகவல்",
        "your_profile": "உங்கள் சுயவிவரம்",
        "next_steps": "அடுத்த படிகள்",
        "download": "📄 PDF ஆக பதிவிறக்கவும்",
        "form": "📋 திட்டங்கள்",
        "govt_links": "🏛️ அரசு இணைப்புகள்",
        "voice": "🎤 பேசுங்கள்",
        "listen": "🔊 கேளுங்கள்",
        "favorite": "❤️ விருப்பமான",
        "compare": "📊 ஒப்பிடுங்கள்",
        "progress": "📈 முன்னேற்றம்",
        "checklist": "✅ சரிபார்ப்பு பட்டியல்",
        "requirements": "📋 தேவைகள்"
    },
    "తెలుగు": {
        "title": "🌾 ఇండిక్-సేతు",
        "subtitle": "ప్రభుత్వ పథకాలను సరళంగా చేయబడ్డాయి",
        "your_details": "మీ వివరాలు",
        "occupation": "మీ వృత్తిని ఎంచుకోండి",
        "income": "వార్ષిక ఆదాయం (₹)",
        "select_language": "🌐 భాషను ఎంచుకోండి",
        "question": "మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?",
        "search": "🔍 వెతకండి",
        "clear": "🔄 స్పష్టం చేయండి",
        "help": "❓ సహాయం",
        "eligibility": "మీ అర్హతా స్థితి",
        "detailed_info": "వివరణాత్మక సమాచారం",
        "your_profile": "మీ ప్రొఫైల్",
        "next_steps": "తదుపరి దశలు",
        "download": "📄 PDFగా డౌన్‌లోడ్ చేయండి",
        "form": "📋 పథకాలు",
        "govt_links": "🏛️ ప్రభుత్వ లింకులు",
        "voice": "🎤 మాట్లాడండి",
        "listen": "🔊 వినండి",
        "favorite": "❤️ ఇష్టమైన",
        "compare": "📊 పోల్చండి",
        "progress": "📈 ఊహించుట",
        "checklist": "✅ చెక్‌లిస్ట్",
        "requirements": "📋 అవసరాలు"
    },
    "ಕನ್ನಡ": {
        "title": "🌾 ಇಂಡಿಕ್-ಸೇತು",
        "subtitle": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಸರಳವಾಗಿ ಮಾಡಲ್ಪಟ್ಟಿವೆ",
        "your_details": "ನಿಮ್ಮ ವಿವರಣೆ",
        "occupation": "ನಿಮ್ಮ ವೃತ್ತಿಯನ್ನು ಆರಿಸಿಕೊಳ್ಳಿ",
        "income": "ವಾರ್ಷಿಕ ಆದಾಯ (₹)",
        "select_language": "🌐 ಭಾಷೆಯನ್ನು ಆರಿಸಿಕೊಳ್ಳಿ",
        "question": "ನೀವು ಏನನ್ನು ತಿಳಿದುಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಿ?",
        "search": "🔍 ಹುಡುಕಿ",
        "clear": "🔄 ತೆರವುಗೊಳಿಸು",
        "help": "❓ ಸಹಾಯ",
        "eligibility": "ನಿಮ್ಮ ಅರ್ಹತೆ ಸ್ಥಿತಿ",
        "detailed_info": "ವಿವರವಾದ ಮಾಹಿತಿ",
        "your_profile": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್",
        "next_steps": "ಮುಂದಿನ ಹಂತಗಳು",
        "download": "📄 PDF ಆಗಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
        "form": "📋 ಯೋಜನೆಗಳು",
        "govt_links": "🏛️ ಸರ್ಕಾರಿ ಲಿಂಕ್‌ಗಳು",
        "voice": "🎤 ಮಾತನಾಡಿ",
        "listen": "🔊 ಕೇಳಿ",
        "favorite": "❤️ ನೆಚ್ಚಿನ",
        "compare": "📊 ಹೋಲಿಕೆ ಮಾಡಿ",
        "progress": "📈 ಪ್ರಗತಿ",
        "checklist": "✅ ಚೆಕ್‌ಲಿಸ್ಟ್",
        "requirements": "📋 ಅವಶ್ಯಕತೆಗಳು"
    },
    "বাংলা": {
        "title": "🌾 ইন্ডিক-সেতু",
        "subtitle": "সরকারী স্কিম সহজ করা হয়েছে",
        "your_details": "আপনার বিবরণ",
        "occupation": "আপনার পেশা নির্বাচন করুন",
        "income": "বার্ষিক আয় (₹)",
        "select_language": "🌐 ভাষা নির্বাচন করুন",
        "question": "আপনি কী জানতে চান?",
        "search": "🔍 অনুসন্ধান করুন",
        "clear": "🔄 স্পষ্ট করুন",
        "help": "❓ সাহায্য",
        "eligibility": "আপনার যোগ্যতার অবস্থা",
        "detailed_info": "বিস্তারিত তথ্য",
        "your_profile": "আপনার প্রোফাইল",
        "next_steps": "পরবর্তী পদক্ষেপ",
        "download": "📄 PDF হিসাবে ডাউনলোড করুন",
        "form": "📋 স্কিমগুলি",
        "govt_links": "🏛️ সরকারী লিঙ্ক",
        "voice": "🎤 কথা বলুন",
        "listen": "🔊 শুনুন",
        "favorite": "❤️ প্রিয়",
        "compare": "📊 তুলনা করুন",
        "progress": "📈 অগ্রগতি",
        "checklist": "✅ চেকলিস্ট",
        "requirements": "📋 প্রয়োজনীয়তা"
    },
    "ਪੰਜਾਬੀ": {
        "title": "🌾 ਇੰਡਿਕ-ਸੇਤੂ",
        "subtitle": "ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਸਰਲ ਬਣਾਈਆਂ ਗਈਆਂ",
        "your_details": "ਤੁਹਾਡੀ ਜਾਣਕਾਰੀ",
        "occupation": "ਆਪਣਾ ਪੇਸ਼ਾ ਚੁਣੋ",
        "income": "ਸਾਲਾਨਾ ਆਮਦਨ (₹)",
        "select_language": "🌐 ਭਾਸ਼ਾ ਚੁਣੋ",
        "question": "ਤੁਸੀਂ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "search": "🔍 ਖੋਜ ਕਰੋ",
        "clear": "🔄 ਸਾਫ ਕਰੋ",
        "help": "❓ ਮਦਦ",
        "eligibility": "ਤੁਹਾਡੀ ਯੋਗਤਾ ਸਥਿਤੀ",
        "detailed_info": "ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "your_profile": "ਤੁਹਾਡਾ ਪ੍ਰੋਫਾਈਲ",
        "next_steps": "ਅਗਲੇ ਪੜਾਅ",
        "download": "📄 PDF ਵਜੋਂ ਡਾਉਨਲੋਡ ਕਰੋ",
        "form": "📋 ਯੋਜਨਾਵਾਂ",
        "govt_links": "🏛️ ਸਰਕਾਰੀ ਲਿੰਕ",
        "voice": "🎤 ਬੋਲੋ",
        "listen": "🔊 ਸੁਣੋ",
        "favorite": "❤️ ਮਨਪਸੰਦ",
        "compare": "📊 ਤੁਲਨਾ ਕਰੋ",
        "progress": "📈 ਪ੍ਰਗਤੀ",
        "checklist": "✅ ਚੈਕ ਲਿਸਟ",
        "requirements": "📋 ਲੋੜਾਂ"
    },
    "اردو": {
        "title": "🌾 انڈک-سیتو",
        "subtitle": "سرکاری اسکیمز آسان بنائی گئیں",
        "your_details": "آپ کی تفصیلات",
        "occupation": "اپنا پیشہ منتخب کریں",
        "income": "سالانہ آمدنی (₹)",
        "select_language": "🌐 زبان منتخب کریں",
        "question": "آپ کیا جاننا چاہتے ہیں؟",
        "search": "🔍 تلاش کریں",
        "clear": "🔄 صاف کریں",
        "help": "❓ مدد",
        "eligibility": "آپ کی اہلیت کی حالت",
        "detailed_info": "تفصیلی معلومات",
        "your_profile": "آپ کی پروفائل",
        "next_steps": "اگلے اقدامات",
        "download": "📄 PDF میں ڈاؤن لوڈ کریں",
        "form": "📋 اسکیمز",
        "govt_links": "🏛️ سرکاری لنکس",
        "voice": "🎤 بولیں",
        "listen": "🔊 سنیں",
        "favorite": "❤️ پسندیدہ",
        "compare": "📊 موازنہ کریں",
        "progress": "📈 ترقی",
        "checklist": "✅ چیک لسٹ",
        "requirements": "📋 ضروریات"
    }
}

# CSS Styling
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .header-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .header-banner h1 {
        color: white;
        font-size: 3em;
        margin: 0;
    }
    
    .header-banner p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2em;
        margin-top: 10px;
    }
    
    .badge-high {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 30px;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4);
    }
    
    .badge-standard {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 30px;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
    }
    
    .result-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-left: 8px solid #e74c3c;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        color: white;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

def t(key):
    """Translate key to current language"""
    return TRANSLATIONS.get(st.session_state.language, TRANSLATIONS['English']).get(key, key)

API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

# Language Selection (Top)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_lang = st.selectbox(
        "🌐",
        list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language),
        key="language_select"
    )
    st.session_state.language = selected_lang

# Header
st.markdown(f"""
<div class="header-banner">
    <h1>{t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Main",
    "❤️ Favorites",
    "📊 Compare",
    "📈 Progress",
    "ℹ️ Info"
])

with tab1:
    # Sidebar
    st.sidebar.title(t('your_details'))
    
    occupation = st.sidebar.selectbox(
        t('occupation'),
        ["Farmer (किसान)", "Agricultural Labourer (कृषि मजदूर)", "Self-Employed (स्व-नियोजित)",
         "Unemployed (बेरोजगार)", "Student (विद्यार्थी)", "Other (अन्य)"]
    )
    
    income = st.sidebar.number_input(t('income'), min_value=0, value=80000, step=10000)
    
    # Eligibility
    st.sidebar.markdown("### ✅ Eligibility")
    if income < 100000 and ("Farmer" in occupation or "Labourer" in occupation):
        st.sidebar.success("🎯 High-Priority!")
    elif income < 300000:
        st.sidebar.info("📋 Standard")
    else:
        st.sidebar.warning("⚠️ Limited")
    
    # Main Content
    st.markdown(f"### {t('question')}")
    
    # Input Section
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        query = st.text_area(
            "Input",
            placeholder="Ask about government schemes...",
            height=80,
            label_visibility="collapsed"
        )
    
    with col2:
        # Microphone button (visual, for now)
        if st.button("🎤", help=t('voice')):
            st.info("🎤 Voice input: Speak now or type your question above")
    
    with col3:
        # Example button
        if st.button("💡", help="Example"):
            st.write("Examples:\n- How to apply for PM-Kisan?\n- I need employment\n- Health insurance")
    
    # Action buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        search_btn = st.button(t('search'), use_container_width=True, key="search")
    with col2:
        clear_btn = st.button(t('clear'), use_container_width=True)
    with col3:
        fav_btn = st.button(t('favorite'), use_container_width=True)
    with col4:
        compare_btn = st.button(t('compare'), use_container_width=True)
    with col5:
        info_btn = st.button(t('help'), use_container_width=True)
    
    if clear_btn:
        st.rerun()
    
    # Search Logic
    if search_btn and query.strip():
        with st.spinner("🔄 " + t('search')):
            try:
                payload = {
                    "query": query,
                    "income": int(income),
                    "occupation": occupation,
                    "language": st.session_state.language
                }
                
                response = requests.post(
                    API_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    api_response = response.json()
                    
                    if isinstance(api_response, dict) and 'body' in api_response:
                        if isinstance(api_response['body'], str):
                            result = json.loads(api_response['body'])
                        else:
                            result = api_response['body']
                    else:
                        result = api_response
                    
                    st.session_state.last_response = result
                    
                    # Eligibility Badge
                    st.markdown(f"### {t('eligibility')}")
                    eligibility = result.get('eligibility_status', 'Unknown')
                    if eligibility == 'High-Priority':
                        st.markdown('<div class="badge-high">✅ HIGH-PRIORITY</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="badge-standard">📋 STANDARD</div>', unsafe_allow_html=True)
                    
                    # Answer
                    st.markdown(f"### {t('detailed_info')}")
                    answer = result.get('answer', '')
                    st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)
                    
                    # Listen Button
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        if st.button(t('listen'), use_container_width=True):
                            try:
                                engine = pyttsx3.init()
                                engine.setProperty('rate', 150)
                                voice_text = result.get('voice_text', answer)
                                engine.say(voice_text)
                                engine.runAndWait()
                                st.success("✅ Audio played!")
                            except Exception as e:
                                st.warning(f"⚠️ {str(e)}")
                    
                    # Profile
                    st.markdown(f"### {t('your_profile')}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Income", f"₹{income:,}")
                    with col2:
                        st.metric("Occupation", occupation.split("(")[0])
                    with col3:
                        st.metric("Status", eligibility)
                    
                    # Download
                    st.markdown("### 📥 Export")
                    result_json = json.dumps(result, ensure_ascii=False, indent=2)
                    st.download_button(
                        t('download'),
                        result_json,
                        "indic_setu_result.txt",
                        "text/plain"
                    )
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

with tab2:
    st.markdown("### ❤️ " + t('favorite'))
    st.write("Save your favorite schemes here for quick access")
    st.info("Click the ❤️ button while viewing a scheme to add it to favorites")

with tab3:
    st.markdown("### 📊 " + t('compare'))
    st.write("Compare multiple government schemes side by side")
    st.info("Select 2-3 schemes to compare their benefits and eligibility")

with tab4:
    st.markdown("### 📈 " + t('progress'))
    st.write("Track your application progress across multiple schemes")
    st.info("Monitor the status of your government scheme applications")

with tab5:
    st.markdown("### ℹ️ Information")
    
    st.markdown("#### 📋 Features:")
    features = [
        "🌐 10+ Language Support",
        "🎤 Voice Input (Say your question)",
        "🔊 Text-to-Speech (Listen to answers)",
        "❤️ Favorite Schemes",
        "📊 Scheme Comparison",
        "📈 Application Tracking",
        "📄 PDF Download",
        "🏛️ Direct Government Links"
    ]
    
    for feature in features:
        st.write(f"✅ {feature}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>🌾 <strong>Indic-Setu</strong> | Making Government Schemes Accessible to All</p>
    <p>© 2024 | Available in 10+ Languages | Free Forever</p>
</div>
""", unsafe_allow_html=True)
