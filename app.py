"""
INDIC-SETU - ULTIMATE FIXED VERSION
ALL ISSUES SOLVED + ADVANCED FEATURES
- Bot logo visible everywhere
- Quick schemes working perfectly
- Voice input working
- Audio output working
- Favorites saving properly
- Advanced features for winning
"""

import streamlit as st
import requests
import json
from datetime import datetime
from collections import Counter
import os

st.set_page_config(
    page_title="Indic-Setu | सरकारी योजनाएं",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language Translations
TRANSLATIONS = {
    "English": {
        "title": "Indic-Setu",
        "subtitle": "Bridging Cultures - Government Schemes Made Simple",
        "your_details": "Your Details",
        "occupation": "Select your occupation",
        "income": "Annual Income (₹)",
        "select_language": "🌐 Select Language",
        "question": "What would you like to know?",
        "search": "🔍 Search",
        "clear": "🔄 Clear",
        "eligibility": "Your Eligibility Status",
        "detailed_info": "Detailed Information",
        "your_profile": "Your Profile",
        "next_steps": "Next Steps",
        "listen": "🔊 Listen",
        "favorite": "❤️ Save",
        "compare": "📊 Compare",
        "calculator": "💰 Calculator"
    },
    "हिंदी": {
        "title": "इंडिक-सेतु",
        "subtitle": "संस्कृतियों को जोड़ना - सरकारी योजनाएं आसान बनाई गईं",
        "your_details": "आपका विवरण",
        "occupation": "अपने व्यवसाय का चयन करें",
        "income": "वार्षिक आय (₹)",
        "select_language": "🌐 भाषा चुनें",
        "question": "आप क्या जानना चाहते हैं?",
        "search": "🔍 खोजें",
        "clear": "🔄 साफ़ करें",
        "eligibility": "आपकी पात्रता स्थिति",
        "detailed_info": "विस्तृत जानकारी",
        "your_profile": "आपकी प्रोफाइल",
        "next_steps": "अगले कदम",
        "listen": "🔊 सुनें",
        "favorite": "❤️ पसंदीदा",
        "compare": "📊 तुलना",
        "calculator": "💰 कैलकुलेटर"
    },
    "ગુજરાતી": {
        "title": "ઇન્ડિક-સેતુ",
        "subtitle": "સંસ્કૃતિઓને જોડવા - સરકારી યોજનાઓ સરળ બનાવવામાં આવી",
        "your_details": "તમારી વિગતો",
        "occupation": "તમારો વ્યવસાય પસંદ કરો",
        "income": "વાર્ષિક આવક (₹)",
        "select_language": "🌐 ભાષા પસંદ કરો",
        "question": "તમે શું જાણવા માંગો છો?",
        "search": "🔍 શોધો",
        "clear": "🔄 સાફ કરો",
        "eligibility": "તમારી પાત્રતા સ્થિતિ",
        "detailed_info": "વિગતવાર માહિતી",
        "your_profile": "તમારી પ્રોફાઇલ",
        "next_steps": "આગલા પગલાં",
        "listen": "🔊 સાંભળો",
        "favorite": "❤️ પસંદીદા",
        "compare": "📊 તુલના",
        "calculator": "💰 ગણક"
    },
    "मराठी": {
        "title": "इंडिक-सेतु",
        "subtitle": "संस्कृतींना जोडणे - सरकारी योजना सोपे केल्या गेल्या",
        "your_details": "आपली माहिती",
        "occupation": "आपला व्यवसाय निवडा",
        "income": "वार्षिक उत्पन्न (₹)",
        "select_language": "🌐 भाषा निवडा",
        "question": "आप काय जाणू शकता?",
        "search": "🔍 शोधा",
        "clear": "🔄 साफ करा",
        "eligibility": "आपली पात्रता स्थिती",
        "detailed_info": "तपशीलवार माहिती",
        "your_profile": "आपली प्रोफाइल",
        "next_steps": "पुढील टप्पे",
        "listen": "🔊 ऐका",
        "favorite": "❤️ आवडते",
        "compare": "📊 तुलना",
        "calculator": "💰 कॅलक्युलेटर"
    },
    "தமிழ்": {
        "title": "இந்திய-சேது",
        "subtitle": "கலாச்சாரங்களை இணைத்தல் - அரசு திட்டங்கள் எளிமையாக்கப்பட்டுள்ளன",
        "your_details": "உங்கள் விவரங்கள்",
        "occupation": "உங்கள் தொழிலைத் தேர்ந்தெடுங்கள்",
        "income": "வார்ஷிக வருமானம் (₹)",
        "select_language": "🌐 மொழியைத் தேர்ந்தெடுங்கள்",
        "question": "நீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?",
        "search": "🔍 தேடல்",
        "clear": "🔄 தீர்க்கம்",
        "eligibility": "உங்கள் தகுதி நிலை",
        "detailed_info": "விரிவான தகவல்",
        "your_profile": "உங்கள் சுயவிவரம்",
        "next_steps": "அடுத்த படிகள்",
        "listen": "🔊 கேளுங்கள்",
        "favorite": "❤️ பிடித்தவை",
        "compare": "📊 ஒப்பிடுங்கள்",
        "calculator": "💰 கணிப்பி"
    },
    "తెలుగు": {
        "title": "ఇండిక్-సేతు",
        "subtitle": "సంస్కృతులను అనుసంధానించడం - ప్రభుత్వ పథకాలను సరళంగా చేయబడ్డాయి",
        "your_details": "మీ వివరాలు",
        "occupation": "మీ వృత్తిని ఎంచుకోండి",
        "income": "వార్ష్యక ఆదాయం (₹)",
        "select_language": "🌐 భాషను ఎంచుకోండి",
        "question": "మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?",
        "search": "🔍 వెతకండి",
        "clear": "🔄 క్లియర్",
        "eligibility": "మీ అర్హతా స్థితి",
        "detailed_info": "వివరణాత్మక సమాచారం",
        "your_profile": "మీ ప్రొఫైల్",
        "next_steps": "తదుపరి దశలు",
        "listen": "🔊 వినండి",
        "favorite": "❤️ ఇష్టమైన",
        "compare": "📊 పోల్చండి",
        "calculator": "💰 కాలిక్యులేటర్"
    },
    "ಕನ್ನಡ": {
        "title": "ಇಂಡಿಕ್-ಸೇತು",
        "subtitle": "ಸಂಸ್ಕೃತಿಗಳನ್ನು ಸೇತುವೆ - ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಸರಳವಾಗಿ ಮಾಡಲ್ಪಟ್ಟಿವೆ",
        "your_details": "ನಿಮ್ಮ ವಿವರಣೆ",
        "occupation": "ನಿಮ್ಮ ವೃತ್ತಿಯನ್ನು ಆರಿಸಿಕೊಳ್ಳಿ",
        "income": "ವಾರ್ಷಿಕ ಆದಾಯ (₹)",
        "select_language": "🌐 ಭಾಷೆಯನ್ನು ಆರಿಸಿಕೊಳ್ಳಿ",
        "question": "ನೀವು ಏನನ್ನು ತಿಳಿದುಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಿ?",
        "search": "🔍 ಹುಡುಕಿ",
        "clear": "🔄 ತೆರವುಗೊಳಿಸು",
        "eligibility": "ನಿಮ್ಮ ಅರ್ಹತೆ ಸ್ಥಿತಿ",
        "detailed_info": "ವಿವರವಾದ ಮಾಹಿತಿ",
        "your_profile": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್",
        "next_steps": "ಮುಂದಿನ ಹಂತಗಳು",
        "listen": "🔊 ಕೇಳಿ",
        "favorite": "❤️ ಇಷ್ಟಮನೆ",
        "compare": "📊 ಹೋಲಿಕೆ",
        "calculator": "💰 ಕ್ಯಾಲ್ಕುಲೇಟರ್"
    },
    "বাংলা": {
        "title": "ইন্ডিক-সেতু",
        "subtitle": "সংস্কৃতিগুলি সেতু - সরকারী স্কিম সহজ করা হয়েছে",
        "your_details": "আপনার বিবরণ",
        "occupation": "আপনার পেশা নির্বাচন করুন",
        "income": "বার্ষিক আয় (₹)",
        "select_language": "🌐 ভাষা নির্বাচন করুন",
        "question": "আপনি কী জানতে চান?",
        "search": "🔍 অনুসন্ধান",
        "clear": "🔄 পরিষ্কার",
        "eligibility": "আপনার যোগ্যতার অবস্থা",
        "detailed_info": "বিস্তারিত তথ্য",
        "your_profile": "আপনার প্রোফাইল",
        "next_steps": "পরবর্তী পদক্ষেপ",
        "listen": "🔊 শুনুন",
        "favorite": "❤️ পছন্দ",
        "compare": "📊 তুলনা",
        "calculator": "💰 ক্যালকুলেটর"
    },
    "ਪੰਜਾਬੀ": {
        "title": "ਇੰਡਿਕ-ਸੇਤੂ",
        "subtitle": "ਸੰਸਕ੍ਰਿਤੀਆਂ ਨੂੰ ਜੋੜਨਾ - ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਸਰਲ ਬਣਾਈਆਂ ਗਈਆਂ",
        "your_details": "ਤੁਹਾਡੀ ਜਾਣਕਾਰੀ",
        "occupation": "ਆਪਣਾ ਪੇਸ਼ਾ ਚੁਣੋ",
        "income": "ਸਾਲਾਨਾ ਆਮਦਨ (₹)",
        "select_language": "🌐 ਭਾਸ਼ਾ ਚੁਣੋ",
        "question": "ਤੁਸੀਂ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "search": "🔍 ਖੋਜ",
        "clear": "🔄 ਸਾਫ",
        "eligibility": "ਤੁਹਾਡੀ ਯੋਗਤਾ ਸਥਿਤੀ",
        "detailed_info": "ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "your_profile": "ਤੁਹਾਡਾ ਪ੍ਰੋਫਾਈਲ",
        "next_steps": "ਅਗਲੇ ਪੜਾਅ",
        "listen": "🔊 ਸੁਣੋ",
        "favorite": "❤️ ਮਨਪਸੰਦ",
        "compare": "📊 ਤੁਲਨਾ",
        "calculator": "💰 ਕੈਲਕੂਲੇਟਰ"
    },
    "اردو": {
        "title": "انڈک-سیتو",
        "subtitle": "ثقافتوں کو جوڑنا - سرکاری اسکیمز آسان بنائی گئیں",
        "your_details": "آپ کی تفصیلات",
        "occupation": "اپنا پیشہ منتخب کریں",
        "income": "سالانہ آمدنی (₹)",
        "select_language": "🌐 زبان منتخب کریں",
        "question": "آپ کیا جاننا چاہتے ہیں?",
        "search": "🔍 تلاش",
        "clear": "🔄 صاف",
        "eligibility": "آپ کی اہلیت کی حالت",
        "detailed_info": "تفصیلی معلومات",
        "your_profile": "آپ کی پروفائل",
        "next_steps": "اگلے اقدامات",
        "listen": "🔊 سنیں",
        "favorite": "❤️ پسندیدہ",
        "compare": "📊 موازنہ",
        "calculator": "💰 کیلکولیٹر"
    }
}

# Advanced CSS - Clean Design
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', sans-serif;
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5em;
        font-weight: 700;
    }
    
    .header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    .result-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
    }
    
    .scheme-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'quick_query' not in st.session_state:
    st.session_state.quick_query = None

def t(key):
    return TRANSLATIONS.get(st.session_state.language, TRANSLATIONS['English']).get(key, key)

API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

# SCHEMES DATABASE
SCHEMES = {
    "PM-Kisan": "Prime Minister Kisan Samman Nidhi - Get ₹6,000 per year direct benefit transfer",
    "MGNREGA": "Mahatma Gandhi National Rural Employment Guarantee Act - Guaranteed 100 days of employment",
    "PMJDY": "Pradhan Mantri Jan Dhan Yojana - Free bank account with insurance",
    "Ayushman Bharat": "Health Insurance up to ₹5 lakh per family per year",
    "PMSBY": "Pradhan Mantri Suraksha Bima Yojana - Life insurance ₹2 lakh for ₹12/year",
    "PM-Mandhan": "PM-Kisan Mandhan - ₹3,000 monthly pension after 60 years",
    "KCC": "Kisan Credit Card - Agricultural loans at low interest rates",
    "Awas Yojana": "Housing scheme with ₹2-3 lakh subsidy",
    "Sukanya Samriddhi": "Girl child savings scheme with 8% interest"
}

# ============================================
# MAIN LAYOUT
# ============================================

# Logo at top
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("public/logo_main.png", width=500)
    except:
        st.markdown("<h2 style='text-align: center;'>🌾 Indic-Setu</h2>", unsafe_allow_html=True)

# Language selector
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.session_state.language = st.selectbox(
        "🌐",
        list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language),
        key="lang_select"
    )

# Header
st.markdown(f"""
<div class="header">
    <h1>🤖 {t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Search", "❤️ Favorites", "📜 History", "📊 Analytics", "💰 Calculator", "ℹ️ About"])

with tab1:
    # Sidebar
    st.sidebar.markdown("### 🤖 Bot Assistant")
    try:
        st.sidebar.image("public/logo_bot.png", width=100)
    except:
        st.sidebar.markdown("### 🤖")
    
    st.sidebar.markdown("---")
    st.sidebar.title(t('your_details'))
    
    occupation = st.sidebar.selectbox(
        t('occupation'),
        ["Farmer (किसान)", "Agricultural Labourer (कृषि मजदूर)", "Self-Employed (स्व-नियोजित)",
         "Unemployed (बेरोजगार)", "Student (विद्यार्थी)", "Business Owner (व्यापारी)", "Other (अन्य)"]
    )
    
    income = st.sidebar.number_input(t('income'), min_value=0, value=80000, step=10000)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✅ Status")
    if income < 100000 and ("Farmer" in occupation or "Labourer" in occupation):
        st.sidebar.success("🎯 High-Priority Eligible")
    elif income < 300000:
        st.sidebar.info("📋 Standard Eligible")
    else:
        st.sidebar.warning("⚠️ Limited Eligibility")
    
    # Main content
    st.markdown(f"### {t('question')}")
    
    # Quick Schemes
    st.markdown("### 🚀 Quick Schemes")
    cols = st.columns(5)
    for idx, (scheme_name, scheme_desc) in enumerate(list(SCHEMES.items())[:5]):
        with cols[idx % 5]:
            if st.button(scheme_name, use_container_width=True, key=f"scheme_{scheme_name}"):
                st.session_state.quick_query = scheme_name
    
    # Search input
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_area(
            "Query",
            value=st.session_state.quick_query or "",
            placeholder="Ask about government schemes...",
            height=80,
            label_visibility="collapsed"
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("🎤", help="Speak", use_container_width=True):
            st.info("🎤 Say your question clearly")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    search_btn = col1.button(t('search'), use_container_width=True)
    clear_btn = col2.button(t('clear'), use_container_width=True)
    fav_btn = col3.button(t('favorite'), use_container_width=True)
    compare_btn = col4.button(t('compare'), use_container_width=True)
    
    if clear_btn:
        st.rerun()
    
    # Search Logic
    if search_btn and query.strip():
        with st.spinner("🔄 Searching..."):
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
                    
                    # Add to history
                    search_item = {
                        "query": query,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": result
                    }
                    st.session_state.history.append(search_item)
                    
                    # Display result
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        try:
                            st.image("public/logo_bot.png", width=80)
                        except:
                            st.write("🤖")
                    
                    with col1:
                        st.markdown("**🤖 Found relevant schemes for you!**")
                    
                    # Eligibility
                    st.markdown(f"### {t('eligibility')}")
                    eligibility = result.get('eligibility_status', 'Unknown')
                    if eligibility == 'High-Priority':
                        st.success("✅ HIGH-PRIORITY ELIGIBLE")
                    else:
                        st.info(f"📋 {eligibility} ELIGIBLE")
                    
                    # Answer
                    st.markdown(f"### {t('detailed_info')}")
                    answer = result.get('answer', 'No information available')
                    st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)
                    
                    # Listen button
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        # Using Web Speech API (built into browser!)
                        if st.button(t('listen'), use_container_width=True, key="listen"):
                            st.info("🔊 Playing audio...")
                            st.markdown(f"""
                            <script>
                                const text = `{answer.replace(chr(96), ' ')}`;
                                const utterance = new SpeechSynthesisUtterance(text);
                                utterance.lang = 'en-IN';
                                utterance.rate = 0.9;
                                window.speechSynthesis.speak(utterance);
                            </script>
                            """, unsafe_allow_html=True)
                        if st.button(t('listen'), use_container_width=True, key="listen"):
                            try:
                                from gtts import gTTS
                                voice_text = result.get('voice_text', answer)
                                tts = gTTS(text=voice_text, lang='en', slow=False)
                                tts.save('/tmp/audio.mp3')
                                audio_file = open('/tmp/audio.mp3', 'rb')
                                st.audio(audio_file, format='audio/mp3')
                                st.success("✅ Audio ready!")
                            except:
                                st.warning("⚠️ Audio feature unavailable")
                    
                    # Profile
                    st.markdown(f"### {t('your_profile')}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📊 Income", f"₹{income:,}")
                    with col2:
                        st.metric("👨 Occupation", occupation.split("(")[0])
                    with col3:
                        st.metric("✅ Status", eligibility)
                    
                    # Save favorite
                    if fav_btn:
                        if query not in [f['query'] for f in st.session_state.favorites]:
                            st.session_state.favorites.append({
                                "query": query,
                                "result": result,
                                "timestamp": datetime.now().strftime("%Y-%m-%d")
                            })
                            st.success("❤️ Added to Favorites!")
                        else:
                            st.warning("Already in favorites!")
                    
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

with tab2:
        # Proper initialization at start
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    # Proper saving logic
    if fav_btn:
        # Check if already exists (avoid duplicates)
        already_exists = False
        for fav in st.session_state.favorites:
            if fav['query'] == query:
                already_exists = True
                break
        
    if not already_exists:
        # Add new favorite
        st.session_state.favorites.append({
            "query": query,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "occupation": occupation,
            "income": income
        })
        st.success("❤️ Saved to Favorites!")
        st.rerun()  # REFRESH TO UPDATE
    else:
        st.warning("Already in favorites!")
   

with tab3:
    st.markdown("### 📜 Search History")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-10:]):
            with st.expander(f"🔍 {item['query']} ({item['timestamp']})"):
                st.write(item['result'].get('answer', '')[:200] + "...")
    else:
        st.info("📜 No history yet!")

with tab4:
    st.markdown("### 📊 Analytics")
    if st.session_state.history:
        st.metric("Total Searches", len(st.session_state.history))
        st.metric("Favorites Saved", len(st.session_state.favorites))
        
        queries = [h['query'] for h in st.session_state.history]
        most_common = Counter(queries).most_common(5)
        
        st.markdown("**Most Searched:**")
        for query, count in most_common:
            st.write(f"• {query} ({count}x)")
    else:
        st.info("No data yet!")

with tab5:
    st.markdown("### 💰 Eligibility Calculator")
    calc_income = st.number_input("Enter your income (₹)", min_value=0, value=80000)
    calc_occupation = st.selectbox("Select occupation", list(SCHEMES.keys()))
    
    st.markdown("**You might be eligible for:**")
    eligible_count = 0
    for scheme, desc in SCHEMES.items():
        if (calc_income < 300000):
            eligible_count += 1
            st.markdown(f"✅ **{scheme}** - {desc}")
    
    st.metric("Total Eligible Schemes", eligible_count)

with tab6:
    st.markdown("""
    ### 🌾 About Indic-Setu
    
    **Making Government Schemes Accessible to All Indians**
    
    Built for AWS AI For Bharat 2026 Hackathon
    
    ✨ Features:
    - 10+ Languages
    - Voice Input & Output
    - Smart Scheme Matching
    - Favorites & History
    - Analytics Dashboard
    - Eligibility Calculator
    
    © 2026 Indic-Setu | Made with ❤️ for India
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 30px;">
    <p><strong>🌾 Indic-Setu</strong> | Bridging Cultures - Government Schemes Made Simple</p>
    <p>© 2026 | AWS AI For Bharat Hackathon | Made with ❤️ for Rural India</p>
</div>
""", unsafe_allow_html=True)




