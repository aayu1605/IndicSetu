"""
INDIC-SETU - ADVANCED VERSION v5
1. 2G/Low Bandwidth Optimized
2. Voice Guider (step-by-step guidance)
3. Form Filler (auto-fill government forms)
4. Enhanced AI Knowledge Base
"""

import streamlit as st
import requests
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import io

# PAGE CONFIG - MINIMAL FOR 2G
st.set_page_config(
    page_title="Indic-Setu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LANGUAGE TRANSLATIONS - MINIMAL SIZE
TRANSLATIONS = {
    "English": {
        "title": "Indic-Setu",
        "subtitle": "Government Schemes Guide",
        "search": "🔍 Search",
        "listen": "🔊 Listen",
        "voice_guide": "📢 Step-by-Step Guide",
        "form_fill": "📋 Auto-Fill Forms",
        "eligibility": "Eligibility Status",
        "details": "Details",
        "save": "❤️ Save",
        "income": "Income (₹)",
        "occupation": "Job Type"
    },
    "हिंदी": {
        "title": "इंडिक-सेतु",
        "subtitle": "सरकारी योजना गाइड",
        "search": "🔍 खोजें",
        "listen": "🔊 सुनें",
        "voice_guide": "📢 चरण-दर-चरण गाइड",
        "form_fill": "📋 फॉर्म स्वतः भरें",
        "eligibility": "पात्रता स्थिति",
        "details": "विवरण",
        "save": "❤️ सहेजें",
        "income": "आय (₹)",
        "occupation": "व्यवसाय"
    },
    "मराठी": {
        "title": "इंडिक-सेतु",
        "subtitle": "सरकारी योजना गाइड",
        "search": "🔍 शोधा",
        "listen": "🔊 ऐका",
        "voice_guide": "📢 चरण-दर-चरण मार्गदर्शन",
        "form_fill": "📋 फॉर्म स्वयंपूर्ण करा",
        "eligibility": "पात्रता स्थिती",
        "details": "तपशील",
        "save": "❤️ सहेजा",
        "income": "आय (₹)",
        "occupation": "व्यवसाय"
    },
    "தமிழ்": {
        "title": "இந்திய-சேது",
        "subtitle": "அரசு திட்டம் வழிகாட்டி",
        "search": "🔍 தேடல்",
        "listen": "🔊 கேளுங்கள்",
        "voice_guide": "📢 படிப்படியான வழிகாட்டி",
        "form_fill": "📋 படிவங்களை தானாக நிரப்பவும்",
        "eligibility": "தகுதி நிலை",
        "details": "விவரங்கள்",
        "save": "❤️ சேமிக்கவும்",
        "income": "வருமானம் (₹)",
        "occupation": "வேலை வகை"
    }
}

# ENHANCED AI KNOWLEDGE BASE
KNOWLEDGE_BASE = {
    "PM-Kisan": {
        "name": "PM-Kisan Samman Nidhi",
        "benefit": "₹6,000/year",
        "eligibility": ["All farmers with land", "Land holdings up to 2 hectares", "Age above 18"],
        "documents": ["Land certificate", "Aadhar", "Bank account"],
        "website": "https://pmkisan.gov.in",
        "toll_free": "1800-180-1111",
        "steps": [
            "Visit pmkisan.gov.in",
            "Click 'Farmer Corner'",
            "Select 'New Farmer Registration'",
            "Enter Aadhar and Land details",
            "Submit application",
            "Receive confirmation",
            "Benefits credited to bank every 4 months"
        ],
        "faqs": {
            "How much money?": "₹6,000 per year (₹2,000 every 4 months)",
            "Who can apply?": "All farmers with land",
            "How to apply?": "Visit pmkisan.gov.in and register",
            "When is money credited?": "Every 4 months to bank account"
        }
    },
    "MGNREGA": {
        "name": "Mahatma Gandhi National Rural Employment Guarantee Act",
        "benefit": "100 days guaranteed employment/year",
        "eligibility": ["Rural adults", "Unemployed", "Willing to do manual work"],
        "documents": ["Aadhar", "Address proof", "Job card"],
        "website": "https://nrega.nic.in",
        "toll_free": "1800-345-6777",
        "steps": [
            "Go to nearest Gram Panchayat",
            "Request job card",
            "Fill application form",
            "Get registered",
            "Apply for work",
            "Work assigned within 15 days",
            "Get paid weekly or monthly"
        ],
        "faqs": {
            "How many days work?": "Minimum 100 days per year",
            "What is the wage?": "₹210-300 per day (varies by state)",
            "How to register?": "Go to Gram Panchayat with Aadhar",
            "How is payment made?": "Through bank transfer or cheque"
        }
    },
    "Ayushman Bharat": {
        "name": "Ayushman Bharat - PM-JAY",
        "benefit": "₹5 lakh health insurance/family/year",
        "eligibility": ["Income less than ₹3 lakh/year", "BPL families", "OBC families"],
        "documents": ["Income certificate", "Aadhar", "Ration card"],
        "website": "https://pmjay.gov.in",
        "toll_free": "1800-111-565",
        "steps": [
            "Check if eligible (income <3L)",
            "Register on pmjay.gov.in or visit hospital",
            "Get golden card issued",
            "Use card for free treatment",
            "Get treated at empaneled hospitals",
            "Insurance covers up to ₹5 lakh"
        ],
        "faqs": {
            "Coverage amount?": "Up to ₹5 lakh per family per year",
            "Who is eligible?": "Families with income less than ₹3 lakh",
            "Which hospitals?": "All empaneled government and private hospitals",
            "Documents needed?": "Aadhar and income certificate"
        }
    },
    "PMJDY": {
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "benefit": "Free bank account with insurance",
        "eligibility": ["All Indian citizens above 10 years", "No income limit"],
        "documents": ["Aadhar", "Any ID proof"],
        "website": "https://pmjdy.gov.in",
        "toll_free": "1800-180-1111",
        "steps": [
            "Visit nearest bank",
            "Fill account opening form",
            "Submit Aadhar copy",
            "Get account opened same day",
            "Receive debit card",
            "Get ₹1 lakh accidental insurance"
        ],
        "faqs": {
            "Account opening fee?": "Completely free",
            "Minimum balance?": "No minimum balance required",
            "Insurance coverage?": "₹1 lakh accidental insurance",
            "Documents needed?": "Only Aadhar is enough"
        }
    }
}

# Polly Configuration
POLLY_VOICES = {
    "English": "Joanna",
    "हिंदी": "Aditi",
    "मराठी": "Aditi",
    "தமிழ்": "Aditi"
}

POLLY_LANG_CODES = {
    "English": "en-US",
    "हिंदी": "hi-IN",
    "मराठी": "mr-IN",
    "தமிழ்": "ta-IN"
}

# MINIMAL CSS FOR 2G
st.markdown("""
<style>
    * { font-family: Arial, sans-serif; }
    body { background: #f5f5f5; }
    .header { background: #667eea; padding: 20px; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .card { background: white; padding: 15px; border-left: 4px solid #667eea; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .success { background: #d4edda; padding: 10px; border-radius: 8px; margin: 10px 0; }
    .info { background: #cfe2ff; padding: 10px; border-radius: 8px; margin: 10px 0; }
    .stButton > button { background: #667eea !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 10px 20px !important; }
</style>
""", unsafe_allow_html=True)

# Session State
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'guide_step' not in st.session_state:
    st.session_state.guide_step = 0

def t(key):
    return TRANSLATIONS.get(st.session_state.language, TRANSLATIONS['English']).get(key, key)

@st.cache_resource
def get_polly_client():
    try:
        return boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=st.secrets.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=st.secrets.get("AWS_SECRET_ACCESS_KEY")
        )
    except:
        return None

def speak_with_polly(text, language):
    try:
        polly = get_polly_client()
        if not polly:
            st.warning("Polly not configured")
            return
        
        voice = POLLY_VOICES.get(language, "Joanna")
        lang_code = POLLY_LANG_CODES.get(language, "en-US")
        
        response = polly.synthesize_speech(
            Text=text[:1500],
            OutputFormat='mp3',
            VoiceId=voice,
            LanguageCode=lang_code
        )
        
        audio_stream = response['AudioStream'].read()
        st.audio(audio_stream, format="audio/mp3")
    except Exception as e:
        st.error(f"Audio error: {str(e)}")

# MAIN UI
st.markdown(f"<div class='header'><h1>{t('title')}</h1><p>{t('subtitle')}</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.session_state.language = st.selectbox("🌐", list(TRANSLATIONS.keys()), index=list(TRANSLATIONS.keys()).index(st.session_state.language), key="lang")
with col2:
    st.write("")

# MAIN TABS
tabs = st.tabs(["🔍 Search", "📢 Voice Guide", "📋 Form Filler", "❤️ Favorites", "📞 Help"])

# TAB 1: SEARCH
with tabs[0]:
    st.markdown("### Search Schemes")
    
    # Sidebar
    st.sidebar.markdown("### Your Info")
    occupation = st.sidebar.selectbox("Job", ["Farmer", "Laborer", "Self-Employed", "Unemployed", "Other"], key="occ")
    income = st.sidebar.number_input("Income (₹)", 0, 1000000, 50000, key="inc")
    
    # Quick buttons - OPTIMIZED FOR 2G
    st.markdown("**Quick Schemes:**")
    cols = st.columns(2)
    for idx, scheme in enumerate(list(KNOWLEDGE_BASE.keys())[:4]):
        with cols[idx % 2]:
            if st.button(scheme, use_container_width=True, key=f"scheme_{scheme}"):
                scheme_data = KNOWLEDGE_BASE[scheme]
                
                # Display info
                st.markdown(f"<div class='success'><h4>{scheme_data['name']}</h4></div>", unsafe_allow_html=True)
                st.markdown(f"**Benefit:** {scheme_data['benefit']}")
                
                st.markdown("**Eligibility:**")
                for elig in scheme_data['eligibility']:
                    st.write(f"✓ {elig}")
                
                st.markdown("**Documents Needed:**")
                for doc in scheme_data['documents']:
                    st.write(f"• {doc}")
                
                # Voice play
                if st.button(f"{t('listen')} - {scheme}", key=f"listen_{scheme}"):
                    text = f"{scheme_data['name']}. Benefit: {scheme_data['benefit']}. Eligibility: {', '.join(scheme_data['eligibility'])}. Contact: {scheme_data['toll_free']}"
                    speak_with_polly(text, st.session_state.language)
                
                # Save favorite
                if st.button(f"{t('save')} - {scheme}", key=f"save_{scheme}"):
                    if scheme not in st.session_state.favorites:
                        st.session_state.favorites.append(scheme)
                        st.success("Saved!")
    
    # Search custom
    st.markdown("---")
    st.markdown("**Custom Search:**")
    query = st.text_input("Ask anything about schemes...", key="search_query")
    
    if st.button(t('search'), use_container_width=True):
        if query.strip():
            # Search in knowledge base
            found = False
            for scheme, data in KNOWLEDGE_BASE.items():
                if query.lower() in scheme.lower() or query.lower() in data['name'].lower():
                    st.markdown(f"<div class='success'><h4>Found: {data['name']}</h4></div>", unsafe_allow_html=True)
                    st.markdown(f"**Benefit:** {data['benefit']}")
                    st.markdown(f"**Website:** {data['website']}")
                    st.markdown(f"**Toll Free:** {data['toll_free']}")
                    found = True
            
            if not found:
                st.info("Scheme not found. Try another search.")

# TAB 2: VOICE GUIDE (STEP-BY-STEP)
with tabs[1]:
    st.markdown("### 📢 Step-by-Step Voice Guide")
    
    scheme = st.selectbox("Select Scheme for Guide:", list(KNOWLEDGE_BASE.keys()), key="guide_scheme")
    
    if scheme:
        scheme_data = KNOWLEDGE_BASE[scheme]
        
        st.markdown(f"<div class='info'><h3>{scheme_data['name']}</h3></div>", unsafe_allow_html=True)
        st.markdown(f"**Benefit:** {scheme_data['benefit']}")
        
        st.markdown("### Application Steps:")
        
        for idx, step in enumerate(scheme_data['steps'], 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**Step {idx}:** {step}")
            with col2:
                if st.button(f"🔊", key=f"step_voice_{idx}"):
                    speak_with_polly(f"Step {idx}. {step}", st.session_state.language)
        
        # FAQs
        st.markdown("### FAQs:")
        for question, answer in scheme_data['faqs'].items():
            with st.expander(question):
                st.write(answer)
                if st.button(f"Listen", key=f"faq_listen_{question}"):
                    speak_with_polly(f"{question}. Answer: {answer}", st.session_state.language)

# TAB 3: AUTO FORM FILLER
with tabs[2]:
    st.markdown("### 📋 Auto-Fill Government Forms")
    
    st.markdown("**Fill your details once, use for all forms:**")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        aadhar = st.text_input("Aadhar Number (12 digits)")
        phone = st.text_input("Phone Number")
    
    with col2:
        dob = st.date_input("Date of Birth")
        address = st.text_area("Address")
        bank_account = st.text_input("Bank Account Number")
    
    if st.button("Generate Form Details", use_container_width=True):
        if name and aadhar:
            form_data = {
                "Name": name,
                "Aadhar": aadhar,
                "Phone": phone,
                "DOB": str(dob),
                "Address": address,
                "Bank Account": bank_account,
                "Occupation": occupation,
                "Income": f"₹{income:,}"
            }
            
            st.markdown("### Your Form Details:")
            st.json(form_data)
            
            # Download as text
            form_text = "\n".join([f"{k}: {v}" for k, v in form_data.items()])
            st.download_button(
                label="Download Form Details (TXT)",
                data=form_text,
                file_name="indicsetu_form_details.txt",
                mime="text/plain"
            )
            
            # Download as JSON
            st.download_button(
                label="Download as JSON",
                data=json.dumps(form_data, indent=2),
                file_name="indicsetu_form_details.json",
                mime="application/json"
            )
            
            st.success("✅ Print or take screenshot for government offices!")

# TAB 4: FAVORITES
with tabs[3]:
    st.markdown("### ❤️ Saved Schemes")
    
    if st.session_state.favorites:
        st.success(f"You have {len(st.session_state.favorites)} saved scheme(s)")
        
        for scheme in st.session_state.favorites:
            if scheme in KNOWLEDGE_BASE:
                data = KNOWLEDGE_BASE[scheme]
                with st.expander(f"💾 {scheme}"):
                    st.markdown(f"**Name:** {data['name']}")
                    st.markdown(f"**Benefit:** {data['benefit']}")
                    st.markdown(f"**Website:** {data['website']}")
                    
                    if st.button(f"Remove", key=f"remove_{scheme}"):
                        st.session_state.favorites.remove(scheme)
                        st.rerun()
    else:
        st.info("No favorites yet! Save schemes from the Search tab.")

# TAB 5: HELP
with tabs[4]:
    st.markdown("### 📞 Help & Support")
    
    st.markdown("""
    **Toll Free Numbers:**
    - PM-Kisan: 1800-180-1111
    - MGNREGA: 1800-345-6777
    - Ayushman Bharat: 1800-111-565
    - PMJDY: 1800-180-1111
    
    **How to Use Indic-Setu:**
    1. **Search Tab:** Find schemes by name or question
    2. **Voice Guide:** Get step-by-step spoken instructions
    3. **Form Filler:** Save your details for all forms
    4. **Favorites:** Save schemes you like
    
    **2G Compatible:**
    ✅ Works on slow internet
    ✅ Minimal data usage
    ✅ Voice output available
    ✅ No large images or videos
    
    **Tips:**
    - Use voice guide for step-by-step help
    - Save your info in form filler for quick access
    - Call toll-free numbers for more help
    - Visit official websites for updates
    """)
    
    # Feedback
    st.markdown("---")
    feedback = st.text_area("Send us feedback:")
    if st.button("Send Feedback"):
        if feedback:
            st.success("✅ Thank you for your feedback!")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><p>🌾 Indic-Setu | Making Government Schemes Accessible | © 2026</p></div>", unsafe_allow_html=True)
