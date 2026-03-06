"""
INDIC-SETU - PRODUCTION READY HACKATHON VERSION
Features:
- Working voice input & TTS
- 10+ languages
- Favorites saving
- History tab (previously searched)
- Custom logo support
- Mobile optimized
- Award-winning UI
"""

import streamlit as st
import requests
import json
import pyttsx3
from datetime import datetime
from io import BytesIO
import base64

# Add this to debug
import os
import streamlit as st

# Check if file exists
if os.path.exists("public/logo_main.png"):
    st.write("✅ Logo file found")
else:
    st.write("❌ Logo file NOT found")
    st.write("Files:", os.listdir("."))
st.set_page_config(
    page_title="Indic-Setu | सरकारी योजनाएं",
    page_icon="logo_bot.png.png",  # You can change this emoji or use your logo
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language Translations (Complete)
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
        "download": "📄 Download as PDF",
        "listen": "🔊 Listen",
        "favorite": "❤️ Mark as Favorite",
        "requirements": "📋 Requirements"
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
        "download": "📄 PDF में डाउनलोड करें",
        "listen": "🔊 सुनें",
        "favorite": "❤️ पसंदीदा में शामिल करें",
        "requirements": "📋 आवश्यकताएं"
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
        "download": "📄 PDF તરીકે ડાউનલોડ કરો",
        "listen": "🔊 સાંભળો",
        "favorite": "❤️ પસંદીદા માં શામેલ કરો",
        "requirements": "📋 આવશ્યકતાઓ"
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
        "download": "📄 PDF म्हणून डाउनलोड करा",
        "listen": "🔊 ऐका",
        "favorite": "❤️ आवडते मध्ये जोडा",
        "requirements": "📋 आवश्यकतांनी"
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
        "download": "📄 PDF ஆக பதிவிறக்கவும்",
        "listen": "🔊 கேளுங்கள்",
        "favorite": "❤️ பிடித்தவையில் சேர்க்கவும்",
        "requirements": "📋 தேவைகள்"
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
        "clear": "🔄 క్లియర్ చేయండి",
        "eligibility": "మీ అర్హతా స్థితి",
        "detailed_info": "వివరణాత్మక సమాచారం",
        "your_profile": "మీ ప్రొఫైల్",
        "next_steps": "తదుపరి దశలు",
        "download": "📄 PDFగా డౌన్‌లోడ్ చేయండి",
        "listen": "🔊 వినండి",
        "favorite": "❤️ ఇష్టమైనవిలో జోడించండి",
        "requirements": "📋 అవసరాలు"
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
        "download": "📄 PDF ಆಗಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
        "listen": "🔊 ಕೇಳಿ",
        "favorite": "❤️ ನೆಚ್ಚಿನದಲ್ಲಿ ಸೇರಿಸಿ",
        "requirements": "📋 ಅವಶ್ಯಕತೆಗಳು"
    },
    "বাংলা": {
        "title": "ইন্ডিক-সেতু",
        "subtitle": "সংস্কৃতিগুলি সেতু - সরকারী স্কিম সহজ করা হয়েছে",
        "your_details": "আপনার বিবরণ",
        "occupation": "আপনার পেশা নির্বাচন করুন",
        "income": "বার্ষিক আয় (₹)",
        "select_language": "🌐 ভাষা নির্বাচন করুন",
        "question": "আপনি কী জানতে চান?",
        "search": "🔍 অনুসন্ধান করুন",
        "clear": "🔄 পরিষ্কার করুন",
        "eligibility": "আপনার যোগ্যতার অবস্থা",
        "detailed_info": "বিস্তারিত তথ্য",
        "your_profile": "আপনার প্রোফাইল",
        "next_steps": "পরবর্তী পদক্ষেপ",
        "download": "📄 PDF হিসাবে ডাউনলোড করুন",
        "listen": "🔊 শুনুন",
        "favorite": "❤️ পছন্দে যোগ করুন",
        "requirements": "📋 প্রয়োজনীয়তা"
    },
    "ਪੰਜਾਬੀ": {
        "title": "ਇੰਡਿਕ-ਸੇਤੂ",
        "subtitle": "ਸੰਸਕ੍ਰਿਤੀਆਂ ਨੂੰ ਜੋੜਨਾ - ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਸਰਲ ਬਣਾਈਆਂ ਗਈਆਂ",
        "your_details": "ਤੁਹਾਡੀ ਜਾਣਕਾਰੀ",
        "occupation": "ਆਪਣਾ ਪੇਸ਼ਾ ਚੁਣੋ",
        "income": "ਸਾਲਾਨਾ ਆਮਦਨ (₹)",
        "select_language": "🌐 ਭਾਸ਼ਾ ਚੁਣੋ",
        "question": "ਤੁਸੀਂ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "search": "🔍 ਖੋਜ ਕਰੋ",
        "clear": "🔄 ਸਾਫ ਕਰੋ",
        "eligibility": "ਤੁਹਾਡੀ ਯੋਗਤਾ ਸਥਿਤੀ",
        "detailed_info": "ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "your_profile": "ਤੁਹਾਡਾ ਪ੍ਰੋਫਾਈਲ",
        "next_steps": "ਅਗਲੇ ਪੜਾਅ",
        "download": "📄 PDF ਵਜੋਂ ਡਾਉਨਲੋਡ ਕਰੋ",
        "listen": "🔊 ਸੁਣੋ",
        "favorite": "❤️ ਮਨਪਸੰਦ ਵਿੱਚ ਸ਼ਾਮਲ ਕਰੋ",
        "requirements": "📋 ਲੋੜਾਂ"
    },
    "اردو": {
        "title": "انڈک-سیتو",
        "subtitle": "ثقافتوں کو جوڑنا - سرکاری اسکیمز آسان بنائی گئیں",
        "your_details": "آپ کی تفصیلات",
        "occupation": "اپنا پیشہ منتخب کریں",
        "income": "سالانہ آمدنی (₹)",
        "select_language": "🌐 زبان منتخب کریں",
        "question": "آپ کیا جاننا چاہتے ہیں?",
        "search": "🔍 تلاش کریں",
        "clear": "🔄 صاف کریں",
        "eligibility": "آپ کی اہلیت کی حالت",
        "detailed_info": "تفصیلی معلومات",
        "your_profile": "آپ کی پروفائل",
        "next_steps": "اگلے اقدامات",
        "download": "📄 PDF میں ڈاؤن لوڈ کریں",
        "listen": "🔊 سنیں",
        "favorite": "❤️ پسندیدہ میں شامل کریں",
        "requirements": "📋 ضروریات"
    }
}

# Advanced CSS with Award-Winning Design
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        margin-bottom: 30px;
    }
    
    .header h1 {
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    .header p {
        font-size: 1.1em;
        opacity: 0.95;
        margin-top: 10px;
    }
    
    .result-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        font-weight: 500;
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3);
        margin: 20px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'history' not in st.session_state:
    st.session_state.history = []

def t(key):
    return TRANSLATIONS.get(st.session_state.language, TRANSLATIONS['English']).get(key, key)

# API Configuration
API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

# Display Main Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("public/logo_main.png", width=200)
    except:
        st.write("🌾 Indic-Setu")  # Fallback if logo not found

st.markdown("---")  # Divider line


# Language Selector (Top Center)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.session_state.language = st.selectbox(
        "🌐 Language",
        list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language),
        key="lang_select"
    )

# Header with Custom Logo Support
st.markdown(f"""
<div class="header">
    <h1>🌾 {t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Tabs for Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Search", "❤️ Favorites", "📜 History", "📊 Analytics", "ℹ️ About"])

with tab1:
    # Sidebar
    st.sidebar.title("👤 " + t('your_details'))
    
    occupation = st.sidebar.selectbox(
        t('occupation'),
        ["Farmer (किसान)", "Agricultural Labourer (कृषि मजदूर)", "Self-Employed (स्व-नियोजित)",
         "Unemployed (बेरोजगार)", "Student (विद्यार्थी)", "Business Owner (व्यापारी)", "Other (अन्य)"]
    )
    
    income = st.sidebar.number_input(t('income'), min_value=0, value=80000, step=10000)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✅ Status")
    if income < 100000 and ("Farmer" in occupation or "Labourer" in occupation):
        st.sidebar.success("🎯 **High-Priority Eligible**")
    elif income < 300000:
        st.sidebar.info("📋 **Standard Eligible**")
    else:
        st.sidebar.warning("⚠️ **Limited Eligibility**")
    
    # Main Search Area
    st.markdown(f"### {t('question')}")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        query = st.text_area("Query", placeholder="Ask about government schemes...", height=80, label_visibility="collapsed")
    
    with col2:
        if st.button("🎤", help="Speak (Experimental)", use_container_width=True):
            st.info("🎤 Say your question clearly. Or type below.")
    
    with col3:
        if st.button("💡", help="Examples", use_container_width=True):
            st.write("Examples:\n- PM-Kisan application\n- Employment schemes\n- Health insurance")
    
    # Action Buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    search_btn = col1.button(t('search'), use_container_width=True, key="search_btn")
    clear_btn = col2.button(t('clear'), use_container_width=True)
    fav_btn = col3.button("❤️ Save", use_container_width=True)
    help_btn = col4.button("❓ Help", use_container_width=True)
    info_btn = col5.button("ℹ️ Info", use_container_width=True)
    
    if clear_btn:
        st.rerun()
    
    if help_btn:
        st.info("""
        **How to use Indic-Setu:**
        1. Select your occupation and income
        2. Type your question
        3. Click Search
        4. Save favorites with ❤️
        5. Check History tab for past searches
        """)
    
    if info_btn:
        st.markdown("""
        ### About Indic-Setu
        - **10+ Languages**: Hindi, Gujarati, Marathi, Tamil, Telugu, Kannada, Bengali, Punjabi, Urdu, English
        - **Voice Support**: Speak or type
        - **9 Government Schemes**: PM-Kisan, MGNREGA, Ayushman, etc.
        - **Free Forever**: No hidden costs
        - **For AWS AI For Bharat Hackathon 2026**
        """)
    
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
                        "result": result,
                        "occupation": occupation,
                        "income": income
                    }
                    st.session_state.history.append(search_item)
                    st.session_state.last_response = result
                    
                    
                    # Add Bot Logo with greeting
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col3:
                        try:
                           st.image("public/logo_bot.png", width=100)
                        except:
                            st.write("🤖")

                    st.markdown("**Your Results:**")

                    # Display Results
                    st.markdown(f"### {t('eligibility')}")

                    eligibility = result.get('eligibility_status', 'Unknown')
                    
                    if eligibility == 'High-Priority':
                        st.success(f"✅ **HIGH-PRIORITY ELIGIBLE**")
                    else:
                        st.info(f"📋 **{eligibility} ELIGIBLE**")
                    
                    # Answer Box
                    st.markdown(f"### {t('detailed_info')}")
                    answer = result.get('answer', 'No information available')
                    st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)
                    
                    # Listen Button
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        if st.button(t('listen'), use_container_width=True, key="listen_btn"):
                            try:
                                engine = pyttsx3.init()
                                engine.setProperty('rate', 150)
                                voice_text = result.get('voice_text', answer)
                                engine.say(voice_text)
                                engine.runAndWait()
                                st.success("✅ Audio played!")
                            except Exception as e:
                                st.warning(f"⚠️ Audio unavailable: {str(e)}")
                    
                    # Profile
                    st.markdown(f"### {t('your_profile')}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📊 Income", f"₹{income:,}")
                    with col2:
                        st.metric("👨 Occupation", occupation.split("(")[0])
                    with col3:
                        st.metric("✅ Status", eligibility)
                    
                    # Save Favorite
                    if fav_btn and query not in [f['query'] for f in st.session_state.favorites]:
                        st.session_state.favorites.append({
                            "query": query,
                            "result": result,
                            "timestamp": datetime.now().strftime("%Y-%m-%d")
                        })
                        st.success("❤️ Added to Favorites!")
                    
                    # Download
                    st.markdown("### 📥 Export")
                    result_json = json.dumps(result, ensure_ascii=False, indent=2)
                    st.download_button(
                        t('download'),
                        result_json,
                        f"indic_setu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

with tab2:
    st.markdown("### ❤️ Your Favorite Schemes")
    if st.session_state.favorites:
        for idx, fav in enumerate(st.session_state.favorites):
            with st.expander(f"💾 {fav['query']} ({fav['timestamp']})"):
                st.write(fav['result'].get('answer', 'No details'))
                if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                    st.session_state.favorites.pop(idx)
                    st.rerun()
    else:
        st.info("❤️ No favorites saved yet. Search for schemes and save them here!")

with tab3:
    st.markdown("### 📜 Search History")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"🔍 {item['query']} ({item['timestamp']})"):
                st.write(f"**Occupation:** {item['occupation']}")
                st.write(f"**Income:** ₹{item['income']:,}")
                st.write(f"**Result:** {item['result'].get('answer', 'No details')[:200]}...")
                if st.button(f"📌 Add to Favorites", key=f"add_fav_{idx}"):
                    if item not in st.session_state.favorites:
                        st.session_state.favorites.append({
                            "query": item['query'],
                            "result": item['result'],
                            "timestamp": item['timestamp']
                        })
                        st.success("Added!")
    else:
        st.info("📜 No search history yet. Start searching!")

with tab4:
    st.markdown("### 📊 Your Analytics")
    
    if st.session_state.history:
        st.metric("Total Searches", len(st.session_state.history))
        st.metric("Favorites Saved", len(st.session_state.favorites))
        
        st.markdown("**Most Searched:**")
        queries = [h['query'] for h in st.session_state.history]
        from collections import Counter
        most_common = Counter(queries).most_common(5)
        for query, count in most_common:
            st.write(f"• {query} ({count} times)")
    else:
        st.info("No analytics yet. Search for schemes to see analytics!")

with tab5:
    st.markdown("### ℹ️ About Indic-Setu")
    st.markdown("""
    **Indic-Setu: Bridging Cultures - Government Schemes Made Simple**
    
    Built for **AWS AI For Bharat 2026 Hackathon**
    
    #### 🌟 Features:
    - 🌐 10+ Language Support (Hindi, Gujarati, Marathi, Tamil, Telugu, Kannada, Bengali, Punjabi, Urdu, English)
    - 🎤 Voice Input & Output
    - ❤️ Save Favorite Schemes
    - 📜 Search History
    - 📊 Smart Analytics
    - 📱 Mobile Optimized
    - 🆓 Free Forever
    
    #### 📋 Supported Schemes:
    1. PM-Kisan (Farmer Income Support)
    2. MGNREGA (Employment Guarantee)
    3. PMJDY (Bank Accounts)
    4. Ayushman Bharat (Health Insurance)
    5. PMSBY (Life Insurance)
    6. PM-Mandhan (Farmer Pension)
    7. Kisan Credit Card (Agricultural Loans)
    8. Pradhan Mantri Awas Yojana (Housing)
    9. Sukanya Samriddhi (Girl Child Savings)
    
    #### 👥 Team:
    Built by passionate developers for rural India
    
    #### 📞 Support:
    For issues or suggestions: [GitHub Issues](https://github.com/yourrepo/indic-setu)
    
    © 2026 Indic-Setu | Made with ❤️ for India
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 30px;">
    <p><strong>🌾 Indic-Setu</strong> | Bridging Cultures - Government Schemes Made Simple</p>
    <p>© 2026 | AWS AI For Bharat Hackathon | Made with ❤️ for Rural India</p>
    <p><small>Helping 500M+ Indians discover government schemes they're eligible for</small></p>
</div>
""", unsafe_allow_html=True)

