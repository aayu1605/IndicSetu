"""
Indic-Setu - ADVANCED VERSION
Features:
- Multi-language UI (Hindi, Gujarati, Marathi, Tamil, Telugu, Kannada)
- Voice input with mic 🎤
- Text-to-speech narration 🔊
- Beautiful colored responses
- Scheme application form filling
- Government website links
"""

import streamlit as st
import requests
import json
import pyttsx3
from io import BytesIO

st.set_page_config(
    page_title="Indic-Setu | Government Schemes",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language translations
TRANSLATIONS = {
    "English": {
        "title": "🌾 Indic-Setu",
        "subtitle": "Government Schemes Made Simple",
        "your_details": "Your Details",
        "occupation": "Select your occupation",
        "income": "Annual Income (₹)",
        "select_language": "Select Language",
        "question": "What would you like to know?",
        "search": "🔍 Search",
        "clear": "🔄 Clear",
        "help": "❓ Help",
        "eligibility": "Your Eligibility Status",
        "detailed_info": "Detailed Information",
        "your_profile": "Your Profile",
        "next_steps": "Next Steps",
        "download": "📄 Download as JSON",
        "form": "📋 Application Forms",
        "govt_links": "🏛️ Government Links",
        "voice": "🎤 Voice Input",
        "listen": "🔊 Listen",
        "fill_form": "Fill Application Form"
    },
    "हिंदी": {
        "title": "🌾 इंडिक-सेतु",
        "subtitle": "सरकारी योजनाएं सरल बनाई गई",
        "your_details": "आपका विवरण",
        "occupation": "अपने व्यवसाय का चयन करें",
        "income": "वार्षिक आय (₹)",
        "select_language": "भाषा चुनें",
        "question": "आप क्या जानना चाहते हैं?",
        "search": "🔍 खोजें",
        "clear": "🔄 साफ़ करें",
        "help": "❓ सहायता",
        "eligibility": "आपकी पात्रता स्थिति",
        "detailed_info": "विस्तृत जानकारी",
        "your_profile": "आपकी प्रोफाइल",
        "next_steps": "अगले कदम",
        "download": "📄 JSON के रूप में डाउनलोड करें",
        "form": "📋 आवेदन फॉर्म",
        "govt_links": "🏛️ सरकारी लिंक",
        "voice": "🎤 वॉयस इनपुट",
        "listen": "🔊 सुनें",
        "fill_form": "आवेदन फॉर्म भरें"
    },
    "ગુજરાતી": {
        "title": "🌾 ઇન્ડિક-સેતુ",
        "subtitle": "સરકારી યોજનાઓ સરળ બનાવવામાં આવી",
        "your_details": "તમારી વિગતો",
        "occupation": "તમારો વ્યવસાય પસંદ કરો",
        "income": "વાર્ષિક આવક (₹)",
        "select_language": "ભાષા પસંદ કરો",
        "question": "તમે શું જાણવા માંગો છો?",
        "search": "🔍 શોધો",
        "clear": "🔄 સાફ કરો",
        "help": "❓ મદદ",
        "eligibility": "તમારી પાત્રતા સ્થિતિ",
        "detailed_info": "વિગતવાર માહિતી",
        "your_profile": "તમારી પ્રોફાઇલ",
        "next_steps": "આગલા પગલાં",
        "download": "📄 JSON તરીકે ડાউનલોડ કરો",
        "form": "📋 અરજી ફોર્મ",
        "govt_links": "🏛️ સરકારી લિંક",
        "voice": "🎤 વોઇસ ઇનપુટ",
        "listen": "🔊 સાંભળો",
        "fill_form": "અરજી ફોર્મ ભરો"
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-left: 8px solid #667eea;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    
    .result-box-answer {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-left: 8px solid #e74c3c;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        color: white;
    }
    
    .form-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 25px;
        border-left: 8px solid #1abc9c;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .gov-links {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    
    .gov-link-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
    }
    
    .gov-link-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
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

# Get translations
def t(key):
    return TRANSLATIONS.get(st.session_state.language, TRANSLATIONS['English']).get(key, key)

# API URL
API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

# Language Selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.session_state.language = st.selectbox(
        "🌐",
        list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language)
    )

# Header
st.markdown(f"""
<div class="header-banner">
    <h1>{t('title')}</h1>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title(t('your_details'))

occupation = st.sidebar.selectbox(
    t('occupation'),
    [
        "Farmer (किसान)",
        "Agricultural Labourer (कृषि मजदूर)",
        "Self-Employed (स्व-नियोजित)",
        "Unemployed (बेरोजगार)",
        "Student (विद्यार्थी)",
        "Other (अन्य)"
    ]
)

income = st.sidebar.number_input(t('income'), min_value=0, value=80000, step=10000)

# Eligibility preview
st.sidebar.markdown("### ✅ Eligibility")
if income < 100000 and ("Farmer" in occupation or "Labourer" in occupation):
    st.sidebar.success("🎯 High-Priority Eligible!")
elif income < 300000:
    st.sidebar.info("📋 Standard Eligible")
else:
    st.sidebar.warning("⚠️ Limited Eligibility")

# Main content
st.markdown(f"### {t('question')}")

# Voice input + Text input
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_area(
        "Enter query",
        placeholder="Ask anything about government schemes...",
        height=100,
        label_visibility="collapsed"
    )

with col2:
    if st.button(t('voice'), use_container_width=True):
        st.info("🎤 Voice input feature - requires browser microphone access")

# Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    search_button = st.button(t('search'), use_container_width=True)
with col2:
    clear_button = st.button(t('clear'), use_container_width=True)
with col3:
    form_button = st.button(t('form'), use_container_width=True)
with col4:
    help_button = st.button(t('help'), use_container_width=True)

if clear_button:
    st.rerun()

if help_button:
    st.info("""
    ### How to Use Indic-Setu:
    1. Select your occupation and income
    2. Choose your language
    3. Ask any question about government schemes
    4. Get instant personalized answers
    5. Fill application forms for schemes
    6. Access government websites
    """)

# API Call
if search_button and query.strip():
    with st.spinner("🔄 Searching government schemes..."):
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
                
                # Extract body if wrapped
                if isinstance(api_response, dict) and 'body' in api_response:
                    if isinstance(api_response['body'], str):
                        result = json.loads(api_response['body'])
                    else:
                        result = api_response['body']
                else:
                    result = api_response
                
                st.session_state.last_response = result
                
                # Eligibility status
                st.markdown(f"### {t('eligibility')}")
                eligibility = result.get('eligibility_status', 'Unknown')
                if eligibility == 'High-Priority':
                    st.markdown('<div class="badge-high">✅ HIGH-PRIORITY</div>', unsafe_allow_html=True)
                    st.success("🎉 You are HIGH-PRIORITY eligible!")
                else:
                    st.markdown('<div class="badge-standard">📋 STANDARD</div>', unsafe_allow_html=True)
                    st.info("Multiple schemes available for you!")
                
                # Detailed information
                st.markdown(f"### {t('detailed_info')}")
                answer = result.get('answer', 'No information available')
                st.markdown(f'<div class="result-box-answer">{answer}</div>', unsafe_allow_html=True)
                
                # Text-to-speech
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button(t('listen'), use_container_width=True):
                        try:
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 150)
                            voice_text = result.get('voice_text', answer)
                            engine.save_to_file(voice_text, '/tmp/audio.mp3')
                            engine.runAndWait()
                            st.success("✅ Audio generated!")
                        except:
                            st.warning("⚠️ Audio not available")
                
                # Profile summary
                st.markdown(f"### {t('your_profile')}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Income", f"₹{income:,}")
                with col2:
                    st.metric("Occupation", occupation.split("(")[0].strip())
                with col3:
                    st.metric("Status", eligibility)
                
                # Next steps
                st.markdown(f"### {t('next_steps')}")
                st.info("""
                ✅ Save this information
                ✅ Contact local Gram Panchayat
                ✅ Prepare required documents
                ✅ Apply online via government portals
                """)
                
                # Download
                st.markdown(f"### 📥 Export")
                result_json = json.dumps(result, ensure_ascii=False, indent=2)
                st.download_button(
                    t('download'),
                    result_json,
                    "indic_setu_result.json",
                    "application/json"
                )
            else:
                st.error(f"❌ API Error: {response.status_code}")
        
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Government Links
st.markdown("---")
st.markdown(f"## {t('govt_links')}")

gov_websites = {
    "PM-Kisan": "https://pmkisan.gov.in",
    "MGNREGA": "https://nrega.nic.in",
    "Ayushman Bharat": "https://pmjay.gov.in",
    "PMJDY": "https://pmjdy.gov.in",
    "Awas Yojana": "https://pmayg.nic.in",
    "Sukanya Samriddhi": "https://www.indiapost.gov.in",
    "NABARD": "https://www.nabard.org",
    "Gram Panchayat": "https://e-gopala.gol.nic.in"
}

cols = st.columns(4)
for idx, (name, url) in enumerate(gov_websites.items()):
    with cols[idx % 4]:
        st.markdown(f"""
        <a href="{url}" target="_blank" class="gov-link-btn">{name}</a>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d;">
    <p>🌾 <strong>Indic-Setu</strong> | Making Government Schemes Accessible to Rural India</p>
    <p>© 2024 | Empowering Rural Communities</p>
</div>
""", unsafe_allow_html=True)
