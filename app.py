"""
INDIC-SETU - COMPLETE FINAL VERSION WITH POLLY
- Polly for multilingual voice output
- Quick schemes fixed and working
- Custom questions working perfectly
- All features complete
"""

import streamlit as st
import requests
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import io

st.set_page_config(
    page_title="Indic-Setu | सरकारी योजनाएं",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language Translations (UI ONLY)
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
        "listen": "🔊 Speak Answer",
        "favorite": "❤️ Save",
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
        "listen": "🔊 जवाब सुनें",
        "favorite": "❤️ सहेजें",
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
        "listen": "🔊 જવાબ સાંભળો",
        "favorite": "❤️ સહેજો",
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
        "listen": "🔊 उत्तर ऐका",
        "favorite": "❤️ सहेजा",
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
        "listen": "🔊 பதிலைக் கேளுங்கள்",
        "favorite": "❤️ சேமிக்கவும்",
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
        "listen": "🔊 సమాధానం వినండి",
        "favorite": "❤️ సేవ్ చేయండి",
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
        "listen": "🔊 ಉತ್ತರ ಕೇಳಿ",
        "favorite": "❤️ ಉಳಿಸಿ",
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
        "listen": "🔊 উত্তর শুনুন",
        "favorite": "❤️ সংরক্ষণ করুন",
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
        "listen": "🔊 ਜਵਾਬ ਸੁਣੋ",
        "favorite": "❤️ ਸੇਵ ਕਰੋ",
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
        "listen": "🔊 جواب سنیں",
        "favorite": "❤️ محفوظ کریں",
    }
}

# Polly Voice IDs for each language
POLLY_VOICES = {
    "English": "Joanna",
    "हिंदी": "Aditi",
    "ગુજરાતી": "Aditi",
    "मराठी": "Aditi",
    "தமிழ்": "Aditi",
    "తెలుగు": "Aditi",
    "ಕನ್ನಡ": "Aditi",
    "বাংলা": "Aditi",
    "ਪੰਜਾਬੀ": "Aditi",
    "اردو": "Aditi"
}

# Polly Language Codes
POLLY_LANG_CODES = {
    "English": "en-US",
    "हिंदी": "hi-IN",
    "ગુજરાતી": "gu-IN",
    "मराठी": "mr-IN",
    "தமிழ்": "ta-IN",
    "తెలుగు": "te-IN",
    "ಕನ್ನಡ": "kn-IN",
    "বাংলা": "bn-IN",
    "ਪੰਜਾਬੀ": "pa-IN",
    "اردو": "ur-PK"
}

# Advanced CSS
st.markdown("""
<style>
    * { font-family: 'Segoe UI', sans-serif; }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px; border-radius: 15px; color: white;
        text-align: center; margin-bottom: 30px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .header h1 { margin: 0; font-size: 2.5em; font-weight: 700; }
    .header p { margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.9; }
    
    .result-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px; border-radius: 12px; color: white;
        margin: 20px 0; box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
    }
    
    .card {
        background: white; padding: 15px; border-radius: 12px;
        border-left: 4px solid #667eea; margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 15px; border-radius: 12px; margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important; padding: 10px 20px !important;
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
if 'last_query' not in st.session_state:
    st.session_state.last_query = None

def t(key):
    return TRANSLATIONS.get(st.session_state.language, TRANSLATIONS['English']).get(key, key)

# AWS Polly Client
@st.cache_resource
def get_polly_client():
    try:
        return boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=st.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=st.secrets.get("AWS_SECRET_ACCESS_KEY")
        )
    except Exception as e:
        st.warning(f"⚠️ Polly not configured. Check AWS credentials in Streamlit secrets.")
        return None

def speak_with_polly(text, language):
    """Speak text using AWS Polly"""
    try:
        polly_client = get_polly_client()
        if not polly_client:
            st.warning("⚠️ Polly not available. Audio feature disabled.")
            return False
        
        voice_id = POLLY_VOICES.get(language, "Joanna")
        lang_code = POLLY_LANG_CODES.get(language, "en-US")
        
        # Get speech from Polly
        response = polly_client.synthesize_speech(
            Text=text[:1000],  # Limit text length
            OutputFormat='mp3',
            VoiceId=voice_id,
            LanguageCode=lang_code
        )
        
        # Play audio
        audio_stream = response['AudioStream'].read()
        st.audio(audio_stream, format="audio/mp3")
        return True
    except Exception as e:
        st.warning(f"⚠️ Polly error: {str(e)}")
        return False

API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

# SCHEMES DATABASE
SCHEMES = {
    "PM-Kisan": {"benefit": "₹6,000/year", "eligibility": "All farmers", "contact": "1800-180-1111"},
    "MGNREGA": {"benefit": "100 days work/year", "eligibility": "Rural workers", "contact": "State office"},
    "PMJDY": {"benefit": "Free bank account", "eligibility": "All citizens", "contact": "Nearest bank"},
    "Ayushman Bharat": {"benefit": "₹5L health insurance", "eligibility": "Income <3L", "contact": "Hospital"},
    "PMSBY": {"benefit": "₹2L insurance/₹12", "eligibility": "18-70 with account", "contact": "Bank"},
    "PM-Mandhan": {"benefit": "₹3,000/month pension", "eligibility": "Farmers 18-40", "contact": "CSC/Bank"},
    "KCC": {"benefit": "Agri loans 4%", "eligibility": "Farmers", "contact": "Bank"},
    "Awas Yojana": {"benefit": "₹2-3L subsidy", "eligibility": "BPL families", "contact": "Gram Panchayat"},
    "Sukanya": {"benefit": "8% interest for girls", "eligibility": "Girls <10yrs", "contact": "Post office"}
}

# SUCCESS STORIES
STORIES = [
    {"name": "Ramesh", "state": "Punjab", "scheme": "PM-Kisan", "benefit": "₹6,000", "story": "Got ₹6,000 for farming!"},
    {"name": "Priya", "state": "Maharashtra", "scheme": "MGNREGA", "benefit": "100 days", "story": "Earned ₹20,000!"},
    {"name": "Vijay", "state": "Rajasthan", "scheme": "Ayushman", "benefit": "₹5L", "story": "Free surgery!"},
    {"name": "Anjali", "state": "Gujarat", "scheme": "PMJDY", "benefit": "Free account", "story": "Free account!"},
]

# ============================================
# MAIN UI START
# ============================================

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.session_state.language = st.selectbox(
        "🌐", 
        list(TRANSLATIONS.keys()), 
        index=list(TRANSLATIONS.keys()).index(st.session_state.language), 
        key="lang_select"
    )

st.markdown(f"<div class='header'><h1>🤖 {t('title')}</h1><p>{t('subtitle')}</p></div>", unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Search", 
    "❤️ Favorites", 
    "📜 History", 
    "📊 Compare", 
    "⭐ Stories", 
    "💰 Benefits", 
    "📞 Contacts"
])

# ============================================
# TAB 1: SEARCH
# ============================================
with tab1:
    # Sidebar
    st.sidebar.markdown("### 🤖 Your Profile")
    try:
        st.sidebar.image("public/logo_bot.png", width=100)
    except:
        st.sidebar.markdown("### 🤖 Bot")
    
    st.sidebar.markdown("---")
    
    occupation = st.sidebar.selectbox(
        t('occupation'),
        ["Farmer (किसान)", "Agricultural Labourer (कृषि मजदूर)", "Self-Employed", "Unemployed", "Student", "Business Owner", "Other"],
        key="occ"
    )
    
    income = st.sidebar.number_input(t('income'), min_value=0, value=80000, step=10000, key="inc")
    
    st.sidebar.markdown("---")
    if income < 100000 and ("Farmer" in occupation or "Labourer" in occupation):
        st.sidebar.success("🎯 High-Priority")
    elif income < 300000:
        st.sidebar.info("📋 Standard")
    else:
        st.sidebar.warning("⚠️ Limited")
    
    # Main Content
    st.markdown(f"### {t('question')}")
    
    # Quick Schemes - FIXED
    st.markdown("### 🚀 Quick Schemes (Click to Search)")
    cols = st.columns(5)
    for idx, scheme in enumerate(list(SCHEMES.keys())[:5]):
        with cols[idx]:
            if st.button(scheme, use_container_width=True, key=f"q_scheme_{scheme}_{idx}"):
                st.session_state.last_query = f"Tell me about {scheme}"
    
    # Input Area
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_area(
            "Query", 
            value=st.session_state.last_query or "",
            placeholder="Ask about schemes or type your question...", 
            height=80, 
            label_visibility="collapsed",
            key="query_input"
        )
        # Clear the quick query after display
        if st.session_state.last_query:
            st.session_state.last_query = None
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🎤", use_container_width=True, key="voice_input_btn"):
            st.info("🎤 Mic feature coming soon")
    
    # Action Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_btn = st.button(t('search'), use_container_width=True, key="search_main")
    with col2:
        clear_btn = st.button(t('clear'), use_container_width=True, key="clear_main")
    with col3:
        fav_btn = st.button(t('favorite'), use_container_width=True, key="fav_main")
    with col4:
        st.button("📊 Compare", use_container_width=True, key="comp_main")
    
    if clear_btn:
        st.rerun()
    
    # SEARCH LOGIC - WORKS FOR QUICK SCHEMES AND CUSTOM QUESTIONS
    if search_btn and query.strip():
        with st.spinner("🔄 Searching & Generating Audio..."):
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
                    
                    # Handle response
                    if isinstance(api_response, dict) and 'body' in api_response:
                        if isinstance(api_response['body'], str):
                            result = json.loads(api_response['body'])
                        else:
                            result = api_response['body']
                    else:
                        result = api_response
                    
                    # GET ANSWER
                    answer = result.get('answer', 'No information available')
                    
                    # Add to history
                    st.session_state.history.append({
                        "query": query,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": result,
                        "answer": answer
                    })
                    
                    # Display Results
                    st.markdown(f"### {t('eligibility')}")
                    eligibility = result.get('eligibility_status', 'Unknown')
                    
                    if eligibility == 'High-Priority':
                        st.success("✅ HIGH-PRIORITY ELIGIBLE")
                    else:
                        st.info(f"📋 {eligibility} ELIGIBLE")
                    
                    st.markdown(f"### {t('detailed_info')}")
                    st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)
                    
                    # Voice Output - USING POLLY
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        if st.button(t('listen'), use_container_width=True, key="listen_btn"):
                            speak_with_polly(answer, st.session_state.language)
                    
                    # Profile
                    st.markdown(f"### {t('your_profile')}")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("💰 Income", f"₹{income:,}")
                    col2.metric("👨 Job", occupation.split("(")[0])
                    col3.metric("✅ Status", eligibility)
                    
                    # Save Favorite
                    if fav_btn:
                        already_exists = False
                        for fav in st.session_state.favorites:
                            if fav['query'] == query:
                                already_exists = True
                                break
                        
                        if not already_exists:
                            st.session_state.favorites.append({
                                "query": query,
                                "result": result,
                                "answer": answer,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "occupation": occupation,
                                "income": income
                            })
                            st.success("❤️ Saved to Favorites!")
                        else:
                            st.warning("Already in favorites!")
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================
# TAB 2: FAVORITES
# ============================================
with tab2:
    st.markdown("### ❤️ Your Favorites")
    if st.session_state.favorites:
        st.success(f"You have {len(st.session_state.favorites)} favorite(s) saved!")
        for idx, fav in enumerate(st.session_state.favorites):
            with st.expander(f"💾 {fav['query']} ({fav['timestamp']})"):
                st.write(f"**Occupation:** {fav['occupation']}")
                st.write(f"**Income:** ₹{fav['income']:,}")
                st.markdown(f'<div class="result-box">{fav.get("answer", "No details")[:400]}</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🗑️ Remove", key=f"remove_{idx}"):
                        st.session_state.favorites.pop(idx)
                        st.success("Removed!")
                        st.rerun()
                with col2:
                    if st.button("📋 Full", key=f"full_{idx}"):
                        st.write(fav.get("answer", "No details"))
                with col3:
                    if st.button("🔊 Listen", key=f"listen_fav_{idx}"):
                        speak_with_polly(fav.get("answer", ""), st.session_state.language)
    else:
        st.info("❤️ No favorites saved yet! Save one above.")

# ============================================
# TAB 3: HISTORY
# ============================================
with tab3:
    st.markdown("### 📜 Search History")
    if st.session_state.history:
        st.info(f"You have {len(st.session_state.history)} search(es)")
        for hist_idx, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"🔍 {item['query']} ({item['timestamp']})"):
                st.markdown(f'<div class="result-box">{item.get("answer", "No details")[:300]}...</div>', unsafe_allow_html=True)
                if st.button("🔊 Listen", key=f"listen_hist_{hist_idx}_{item['timestamp']}"):
                    speak_with_polly(item.get("answer", ""), st.session_state.language)
    else:
        st.info("📜 No history yet!")

# ============================================
# TAB 4: COMPARE
# ============================================
with tab4:
    st.markdown("### 📊 Compare Schemes")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.selectbox("Scheme 1", list(SCHEMES.keys()), key="s1_comp")
    with col2:
        s2 = st.selectbox("Scheme 2", list(SCHEMES.keys()), key="s2_comp")
    
    if s1 != s2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Criteria**\n\nBenefit\n\nEligibility\n\nContact")
        with col2:
            st.markdown(f"**{s1}**\n\n{SCHEMES[s1]['benefit']}\n\n{SCHEMES[s1]['eligibility']}\n\n{SCHEMES[s1]['contact']}")
        with col3:
            st.markdown(f"**{s2}**\n\n{SCHEMES[s2]['benefit']}\n\n{SCHEMES[s2]['eligibility']}\n\n{SCHEMES[s2]['contact']}")

# ============================================
# TAB 5: SUCCESS STORIES
# ============================================
with tab5:
    st.markdown("### ⭐ Success Stories")
    for story in STORIES:
        st.markdown(f"""
        <div class="success-card">
            <h4>{story['name']} - {story['state']}</h4>
            <p><strong>Scheme:</strong> {story['scheme']} | <strong>Benefit:</strong> {story['benefit']}</p>
            <p><em>"{story['story']}"</em></p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 6: BENEFITS CALCULATOR
# ============================================
with tab6:
    st.markdown("### 💰 Calculate Benefits")
    calc_income = st.number_input("Your income (₹)", 0, 10000000, 80000, key="calc_inc")
    st.markdown("**You might be eligible for:**")
    count = 0
    for scheme, info in SCHEMES.items():
        if calc_income < 300000:
            count += 1
            st.markdown(f'<div class="card">✅ <strong>{scheme}</strong><br>{info["benefit"]}</div>', unsafe_allow_html=True)
    st.metric("Total Eligible Schemes", count)

# ============================================
# TAB 7: GOVERNMENT CONTACTS
# ============================================
with tab7:
    st.markdown("### 📞 Government Contacts")
    for scheme, info in SCHEMES.items():
        with st.expander(f"📞 {scheme}"):
            st.write(f"📱 Contact: {info['contact']}")
            st.write(f"☎️ Toll Free: 1800-180-1111")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><p><strong>🌾 Indic-Setu</strong> | © 2026 AWS AI For Bharat</p></div>", unsafe_allow_html=True)
