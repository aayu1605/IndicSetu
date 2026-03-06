"""
Indic-Setu Frontend - Streamlit App
Beautiful interface for rural India government scheme eligibility checker
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pyttsx3
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Indic-Setu | Sarkari Yojnayen",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful rural-focused design
st.markdown("""
<style>
    /* Root theme */
    :root {
        --primary: #2ecc71;
        --dark-green: #27ae60;
        --gold: #f39c12;
        --earth: #8b7355;
        --sky: #3498db;
        --danger: #e74c3c;
    }
    
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Lora:wght@400;600&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Lora', serif;
        color: #1a472a;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    /* Header styling */
    .header-banner {
        background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(46, 204, 113, 0.3);
        text-align: center;
    }
    
    .header-banner h1 {
        color: white;
        font-size: 2.5em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-banner p {
        color: rgba(255,255,255,0.9);
        margin-top: 10px;
        font-size: 1.1em;
    }
    
    /* Badge styling */
    .badge-container {
        text-align: center;
        margin: 20px 0;
    }
    
    .badge-high-priority {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 20px 40px;
        border-radius: 50px;
        font-size: 1.5em;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(46, 204, 113, 0.4);
        display: inline-block;
        animation: pulse-badge 2s ease-in-out infinite;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-standard {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 20px 40px;
        border-radius: 50px;
        font-size: 1.5em;
        font-weight: 700;
        box-shadow: 0 10px 30px rgba(52, 152, 219, 0.4);
        display: inline-block;
        animation: float-badge 3s ease-in-out infinite;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    @keyframes pulse-badge {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes float-badge {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Input cards */
    .input-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #2ecc71;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        border-radius: 25px !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(46, 204, 113, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(46, 204, 113, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Result box */
    .result-box {
        background: white;
        padding: 25px;
        border-radius: 10px;
        border-left: 6px solid #2ecc71;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #ecf0f1 0%, #bdc3c7 100%);
    }
    
    .sidebar-info {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #f39c12;
    }
    
    /* Voice button */
    .voice-button {
        background: linear-gradient(90deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 12px 25px;
        border-radius: 25px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        box-shadow: 0 6px 15px rgba(243, 156, 18, 0.3);
        margin-top: 10px;
    }
    
    /* Low data mode */
    .low-data-warning {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-banner h1 {
            font-size: 1.8em;
        }
        .badge-high-priority, .badge-standard {
            font-size: 1.1em;
            padding: 15px 30px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_url' not in st.session_state:
    st.session_state.api_url = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'low_data_mode' not in st.session_state:
    st.session_state.low_data_mode = False

# Header Banner
st.markdown("""
<div class="header-banner">
    <h1>🌾 Indic-Setu</h1>
    <p>Sarkari Yojnaon ke Liye Aasaan Pataptar</p>
    <p style="font-size: 0.9em; opacity: 0.9;">Government Schemes Made Simple</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ Settings & Input")

# Low Data Mode Toggle
st.sidebar.markdown("### 📊 User Preferences")
low_data_mode = st.sidebar.checkbox(
    "🌐 Low-Data Mode (2G Network)",
    value=st.session_state.low_data_mode,
    help="Disable images and reduce animations for slower networks"
)
st.session_state.low_data_mode = low_data_mode

if low_data_mode:
    st.sidebar.markdown("""
    <div class="low-data-warning">
    💡 Low-Data Mode: Images disabled, minimal animations enabled
    </div>
    """, unsafe_allow_html=True)

# API Configuration
st.sidebar.markdown("### 🔌 API Configuration")
api_url = st.sidebar.text_input(
    "AWS API Gateway URL",
    value=st.session_state.api_url,
    help="Enter your Lambda API Gateway endpoint",
    placeholder="https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"
)
st.session_state.api_url = api_url

# Language Selection
st.sidebar.markdown("### 🗣️ Language Preference")
language = st.sidebar.selectbox(
    "Select Language",
    ["Hindi-English Mix (सर्वोत्तम) 🇮🇳", "English", "Hindi (हिंदी)"],
    help="Choose your preferred language"
)

# Occupation Selection
st.sidebar.markdown("### 👨‍🌾 Occupation")
occupation = st.sidebar.selectbox(
    "Your Main Occupation",
    [
        "Farmer (किसान)",
        "Agricultural Labourer (कृषि मजदूर)",
        "Weaver (बुनकर)",
        "Artisan (शिल्पकार)",
        "Self-Employed (स्व-नियोजित)",
        "Unemployed (बेरोजगार)",
        "Student (विद्यार्थी)",
        "Other (अन्य)"
    ],
    help="Select your occupation for accurate scheme matching"
)

# Income Input
st.sidebar.markdown("### 💰 Annual Income")
income = st.sidebar.number_input(
    "Your Annual Income (₹)",
    min_value=0,
    value=0,
    step=10000,
    help="Enter your total annual household income"
)

# Display eligibility info
st.sidebar.markdown("### ✅ Eligibility Check")
if income < 100000 and "Farmer" in occupation or "Labourer" in occupation:
    st.sidebar.success("🎯 **High-Priority** - You may qualify for premium schemes!")
elif income < 300000:
    st.sidebar.info("📋 **Standard** - Multiple schemes available for you")
else:
    st.sidebar.warning("⚠️ **Limited** - Some schemes may not be available")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📞 Support
**Toll-Free:** 1800-180-1111  
**Website:** indic-setu.gov.in  
**Email:** help@indicsetu.in
""")

# Main Content Area
st.markdown("### 🤔 What would you like to know?")

# Query Input
query = st.text_area(
    "Ask about government schemes...",
    placeholder="उदाहरण: मुझे PM-Kisan के लिए आवेदन कैसे करना है?\nExample: How do I apply for PM-Kisan?",
    height=100,
    label_visibility="collapsed"
)

# Submit Button
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    submit_button = st.button("🔍 खोजें | Search", use_container_width=True)

with col2:
    clear_button = st.button("🔄 Clear", use_container_width=True)

with col3:
    help_button = st.button("❓ Help", use_container_width=True)

# Clear functionality
if clear_button:
    st.rerun()

# Help modal
if help_button:
    st.info("""
    ### How to use Indic-Setu:
    
    1. **Set Your Details** (Sidebar):
       - Select your occupation
       - Enter your annual income
       - Choose your language
    
    2. **Ask Your Question**:
       - Type any question about government schemes
       - Examples: "How to apply for PM-Kisan?", "What is my eligibility?"
    
    3. **Get Your Answer**:
       - View detailed, personalized information
       - Check your eligibility status
       - Listen to the answer in Hindi-English
    
    4. **Take Action**:
       - Follow the next steps provided
       - Contact local government office
       - Apply online via official portals
    """)

# API Call and Response Handling
if submit_button and query.strip():
    if not api_url or "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query" in api_url:
        st.error("⚠️ Please configure your AWS API Gateway URL in Settings (Sidebar)")
    else:
        with st.spinner("🔄 Searching government schemes for you..."):
            try:
                # Prepare request payload
                payload = {
                    "query": query,
                    "income": int(income),
                    "occupation": occupation
                }
                
                # Make API request
                response = requests.post(
                    api_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.last_response = result
                    
                    # Display eligibility badge
                    st.markdown("### ✨ Your Eligibility Status")
                    
                    if result.get('eligibility_status') == 'High-Priority':
                        st.markdown("""
                        <div class="badge-container">
                            <div class="badge-high-priority">
                                ✅ HIGH-PRIORITY ELIGIBLE
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.success("🎉 आप उच्च प्राथमिकता के लिए योग्य हैं! You are HIGH-PRIORITY eligible!")
                    else:
                        st.markdown("""
                        <div class="badge-container">
                            <div class="badge-standard">
                                📋 STANDARD ELIGIBLE
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("कई योजनाएं आपके लिए उपलब्ध हैं। Multiple schemes available for you.")
                    
                    # Display main answer
                    st.markdown("### 📝 Detailed Information")
                    st.markdown(f"""
                    <div class="result-box">
                        {result.get('answer', 'No information available')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Voice TTS Section
                    st.markdown("### 🎧 Awaaz mein Suniye (Listen in Hindi-English)")
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        voice_text = result.get('voice_text', '')
                        st.text_area(
                            "Voice Text",
                            value=voice_text,
                            height=80,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        if st.button("🔊 Play", use_container_width=True):
                            try:
                                # Initialize text-to-speech
                                engine = pyttsx3.init()
                                engine.setProperty('rate', 150)  # Slow speech for clarity
                                
                                # Generate speech
                                audio_buffer = BytesIO()
                                engine.save_to_file(
                                    voice_text,
                                    '/tmp/indic_setu_audio.mp3'
                                )
                                engine.runAndWait()
                                
                                # Display audio player
                                with open('/tmp/indic_setu_audio.mp3', 'rb') as f:
                                    st.audio(f.read(), format='audio/mp3')
                                
                                st.success("🎵 Audio generated successfully!")
                            
                            except Exception as e:
                                st.warning(f"⚠️ Text-to-speech not available: {str(e)}")
                                st.info("Try using browser developer tools or install pyttsx3")
                    
                    # Additional Information Section
                    st.markdown("### 📋 Your Profile Summary")
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    
                    with summary_col1:
                        st.metric("Annual Income", f"₹{income:,}", delta="High Priority" if income < 100000 else "Standard")
                    
                    with summary_col2:
                        st.metric("Occupation", occupation.split("(")[0].strip())
                    
                    with summary_col3:
                        st.metric("Status", result.get('eligibility_status', 'Unknown'))
                    
                    # Next Steps
                    st.markdown("### 🎯 Next Steps")
                    st.info("""
                    ✅ Save this information for reference  
                    ✅ Contact your local Gram Panchayat or government office  
                    ✅ Prepare required documents (Aadhar, Land Records, Bank Account)  
                    ✅ Apply online via official government portals  
                    ✅ Keep tracking your application status  
                    """)
                    
                    # Download option
                    st.markdown("### 📥 Export Information")
                    result_json = json.dumps(result, ensure_ascii=False, indent=2)
                    st.download_button(
                        "📄 Download as JSON",
                        result_json,
                        "indic_setu_result.json",
                        "application/json"
                    )
                
                else:
                    st.error(f"❌ API Error (Status {response.status_code}): {response.text}")
            
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please check your internet connection and API URL.")
            
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to the API. Please verify your AWS API Gateway URL.")
            
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
    <p>🌾 <strong>Indic-Setu</strong> | Making Government Schemes Accessible to Rural India</p>
    <p>सरकारी योजनाओं को आसान और सुलभ बनाना | Built for the Hackathon with ❤️</p>
    <p style="font-size: 0.85em; opacity: 0.7;">© 2024 | Empowering Rural Communities | Version 1.0</p>
</div>
""", unsafe_allow_html=True)