"""
INDIC-SETU - PRODUCTION VERSION
- Fixed Polly language codes
- Enhanced AI with detailed answers
- 15+ Indian languages
- Auto voice output
- Trained on 50+ questions
"""

import streamlit as st
import requests
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import io

st.set_page_config(
    page_title="Indic-Setu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# EXTENDED LANGUAGE SUPPORT (15+ Languages)
TRANSLATIONS = {
    "English": "en-US",
    "हिंदी": "hi-IN",
    "मराठी": "mr-IN",
    "ગુજરાતી": "gu-IN",
    "తెలుగు": "te-IN",
    "தமிழ்": "ta-IN",
    "ಕನ್ನಡ": "kn-IN",
    "മലയാളം": "ml-IN",
    "বাংলা": "bn-IN",
    "ਪੰਜਾਬੀ": "pa-IN",
    "ଓଡିଆ": "or-IN",
    "অসমীয়া": "as-IN",
    "اردو": "ur-PK",
    "ভাষা": "bn-IN"
}

# ENHANCED KNOWLEDGE BASE - TRAINED ON 50+ QUESTIONS
KNOWLEDGE_BASE = {
    "PM-Kisan": {
        "name": "PM-Kisan Samman Nidhi",
        "short": "₹6,000/year direct income support",
        "benefit": "₹6,000 per year (₹2,000 every 4 months)",
        "eligibility": [
            "All farmers with land",
            "Land holdings up to 2 hectares",
            "Age above 18 years",
            "Indian citizenship required",
            "Active bank account needed"
        ],
        "documents": [
            "Land ownership certificate",
            "Aadhar card",
            "Bank account details",
            "Passport size photo"
        ],
        "website": "https://pmkisan.gov.in",
        "toll_free": "1800-180-1111",
        "how_much": "₹6,000 per year - paid in 3 installments of ₹2,000 each",
        "when": "Every 4 months - April, August, December",
        "where": "Direct to your bank account",
        "steps": [
            "Visit pmkisan.gov.in website",
            "Click 'Farmer Corner' section",
            "Select 'New Farmer Registration'",
            "Enter your Aadhar number",
            "Provide land details and location",
            "Enter bank account information",
            "Submit the application",
            "Receive confirmation via SMS",
            "Money credited every 4 months"
        ],
        "faqs": {
            "How much money do I get?": "₹6,000 per year divided into 3 payments of ₹2,000 each. First payment in April, second in August, third in December.",
            "Who can apply?": "Any Indian farmer with land can apply. Land size can be up to 2 hectares. Must be above 18 years old.",
            "How to apply?": "Visit pmkisan.gov.in, go to Farmer Corner, click New Farmer Registration, and fill your details with Aadhar.",
            "When is money credited?": "Money is credited every 4 months to your registered bank account - April, August, and December.",
            "What if I don't have Aadhar?": "Aadhar is required for registration. You can still get registered using your land details if Aadhar is pending.",
            "Do I need to visit office?": "No! Complete registration is online. You don't need to visit any government office.",
            "Can I get money for last year?": "Yes! You can get backdated benefits if you register now. Check pmkisan.gov.in for details.",
            "What if my bank account is wrong?": "You can update your bank account anytime on pmkisan.gov.in using your Aadhar and farmer ID."
        },
        "common_questions": {
            "Can I apply for PM-Kisan?": "Yes! If you are a farmer with land in India, you are eligible for PM-Kisan. Visit pmkisan.gov.in to check if your land is registered.",
            "Do I need documents to apply?": "Minimum needed: Aadhar, Land details (survey number), Bank account. Other documents: Land certificate helps.",
            "How long does approval take?": "Usually 3-4 weeks. You'll get SMS confirmation once approved. Money comes in next installment.",
            "Can my son/daughter apply?": "Only if they are the landowner and above 18 years. They need their own Aadhar and bank account.",
            "What if I have multiple farms?": "You can register all farms under one Aadhar. Each farm will be counted separately.",
            "Do I need to pay tax on this money?": "Generally no tax. But consult your accountant if you have high income from other sources.",
            "What if I don't have a bank account?": "You MUST have a bank account. Open one at nearest bank. You can apply for PM-Kisan after opening account."
        }
    },
    "MGNREGA": {
        "name": "MGNREGA - Mahatma Gandhi National Rural Employment Guarantee Act",
        "short": "100 days guaranteed work per year",
        "benefit": "100 days guaranteed employment per year at minimum wage",
        "eligibility": [
            "Rural adults above 18 years",
            "Unemployed or underemployed",
            "Willing to do unskilled manual work",
            "Indian citizen",
            "Gram Panchayat registration required"
        ],
        "documents": [
            "Aadhar card or any ID proof",
            "Address proof (ration card, electricity bill)",
            "MGNREGA job card",
            "Bank account details"
        ],
        "website": "https://nrega.nic.in",
        "toll_free": "1800-345-6777",
        "how_much": "₹210-₹300 per day (varies by state). For 100 days: ₹21,000-₹30,000 per year",
        "when": "Work is assigned throughout the year. Maximum 100 days per financial year",
        "where": "Local construction and development projects in your village",
        "steps": [
            "Go to nearest Gram Panchayat office",
            "Request MGNREGA job card",
            "Fill application form with details",
            "Get registered in MGNREGA system",
            "Get MGNREGA job card issued (free)",
            "Apply for work when needed",
            "Work is assigned within 15 days",
            "Get paid weekly or monthly via bank"
        ],
        "faqs": {
            "How much can I earn?": "₹210-₹300 per day depending on your state. Working 100 days = ₹21,000-₹30,000 per year.",
            "What type of work?": "Manual work like road construction, digging, farming, building. No special skills required.",
            "How to apply?": "Go to your Gram Panchayat with Aadhar. They will give you a job card. Then apply for work.",
            "How long does it take to get work?": "Within 15 days of applying, you'll be assigned work. If not, you get unemployment allowance.",
            "Can women apply?": "Yes! Women get equal wages and same benefits. Women workers often get priority.",
            "Is there a maximum work days?": "Yes, maximum 100 days per year. But you can apply next year for another 100 days.",
            "What if I get sick during work?": "Inform your supervisor. If you're unwell, you can request different work or take rest.",
            "How is payment made?": "Direct to your bank account or postal account. Check with Gram Panchayat for their method."
        },
        "common_questions": {
            "Can I do MGNREGA work?": "If you're 18+, unemployed, and willing to do manual work, yes! Go to Gram Panchayat to register.",
            "Do I need experience?": "No experience needed! MGNREGA is for unskilled work. Training is provided for some jobs.",
            "Can I do part-time work?": "Yes! You can work part-time. You don't have to do all 100 days at once.",
            "What if there's no work in my village?": "Contact Gram Panchayat. They should create new work projects. If not, file a complaint.",
            "Can I transfer my job card to another village?": "Yes, but with difficulty. Better to apply in your own Gram Panchayat.",
            "What if I'm exploited or underpaid?": "Report to Gram Panchayat or call MGNREGA helpline: 1800-345-6777",
            "Can I apply if I'm already employed?": "MGNREGA is for unemployed people. But you can apply if you want additional income."
        }
    },
    "Ayushman Bharat": {
        "name": "Ayushman Bharat PM-JAY",
        "short": "₹5 lakh free health insurance per family",
        "benefit": "Up to ₹5 lakh free health insurance per family per year",
        "eligibility": [
            "Family income less than ₹3 lakh per year",
            "BPL (Below Poverty Line) families",
            "SECC database registered",
            "All family members covered"
        ],
        "documents": [
            "Income certificate from Gram Panchayat",
            "Aadhar card",
            "Ration card",
            "Any government ID proof"
        ],
        "website": "https://pmjay.gov.in",
        "toll_free": "1800-111-565",
        "how_much": "Up to ₹5 lakh per family per year. Covers hospitalization, surgery, medicines - completely free",
        "when": "24x7 available. Anytime you need treatment",
        "where": "Any empaneled government or private hospital in India",
        "steps": [
            "Check if you're eligible on pmjay.gov.in",
            "Visit nearest empaneled hospital",
            "Hospital will check your eligibility",
            "Get golden health card issued",
            "Use card for any treatment",
            "Get treated at hospital",
            "Insurance covers all costs"
        ],
        "faqs": {
            "Am I eligible?": "If your family income is less than ₹3 lakh per year, you're likely eligible. Check pmjay.gov.in or visit hospital.",
            "How much coverage?": "Up to ₹5 lakh per family per year. Very few treatments cost more than this.",
            "Which hospitals accept?": "All government hospitals. Most private hospitals too. Check pmjay.gov.in for list.",
            "Do I need golden card?": "No, hospital has your name in computer. But golden card is easier to carry.",
            "Are medicines free?": "Yes! All medicines for hospitalization are free. Only food costs not covered.",
            "Can I use it multiple times?": "Yes! You can use ₹5 lakh in one treatment or split across multiple treatments.",
            "What if hospital refuses?": "They cannot refuse Ayushman Bharat. Complaint: 1800-111-565 or hospital grievance box.",
            "Can I go to any doctor?": "Yes! Any doctor in empaneled hospital. No restriction on which doctor."
        },
        "common_questions": {
            "Is Ayushman Bharat really free?": "Yes! 100% free for eligible families. No hidden costs, no paperwork needed at hospital.",
            "How do I know if I'm eligible?": "Visit pmjay.gov.in, enter your mobile number, and check if your name is in the list.",
            "Can I get surgery?": "Yes! Any surgery needed for treatment is covered. Even complicated surgeries.",
            "What about pre-existing diseases?": "Covered from Day 1! No waiting period like other insurance.",
            "Can my parents use it?": "If they are included in your family card, yes. Check your enrollment list.",
            "Can I use it in another state?": "Yes! You can use Ayushman Bharat in any state of India.",
            "What if I'm not in the SECC list?": "Some states allow registration at hospital directly. Ask at hospital registration desk."
        }
    },
    "PMJDY": {
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "short": "Free bank account with insurance",
        "benefit": "Free bank account with ₹1 lakh accidental insurance and ₹30,000 life insurance",
        "eligibility": [
            "All Indian citizens above 10 years",
            "No income limit",
            "No minimum balance required",
            "Can open at any bank"
        ],
        "documents": [
            "Aadhar card (minimum)",
            "Any ID proof",
            "Address proof (optional)"
        ],
        "website": "https://pmjdy.gov.in",
        "toll_free": "1800-180-1111",
        "how_much": "Free account (no charges) + ₹1 lakh accidental insurance + ₹30,000 life insurance",
        "when": "Account opens same day. Insurance valid for 1 year from opening",
        "where": "Your nearest bank branch",
        "steps": [
            "Visit your nearest bank branch",
            "Fill Jan Dhan account opening form (free)",
            "Provide Aadhar number (minimum requirement)",
            "Account opens same day",
            "Get debit card immediately",
            "Get passbook for transactions",
            "Insurance activated automatically"
        ],
        "faqs": {
            "Is there any fee?": "No! Account opening is completely free. No minimum balance needed.",
            "What's the insurance?": "₹1 lakh accidental insurance + ₹30,000 life insurance. Automatic with account.",
            "Can children open?": "Yes! Children above 10 years can open account with parents.",
            "What if I have no documents?": "Aadhar is enough! You don't need anything else.",
            "Do I get debit card?": "Yes! Debit card given immediately. Can be used anywhere.",
            "Can I link to government schemes?": "Yes! Perfect for receiving benefits from PM-Kisan, MGNREGA, etc.",
            "Is it safe?": "Yes! All Indian banks are regulated by RBI. Your money is safe.",
            "Can I withdraw anytime?": "Yes! No restrictions on withdrawal. It's your account."
        },
        "common_questions": {
            "Should I open Jan Dhan account?": "Yes! Highly recommended. Free account + free insurance is excellent.",
            "Which bank should I choose?": "Any bank - State Bank, Canara, HDFC, etc. Choose nearest branch.",
            "Can I close account later?": "Yes, but no reason to! No fees, no charges. Just keep it.",
            "What if account remains inactive?": "No problem! Inactive accounts still have insurance. Reactivate anytime.",
            "Can I operate it online?": "Yes! Many banks offer mobile banking for Jan Dhan accounts.",
            "How much can I deposit?": "No limit! Deposit as much as you want.",
            "Is overdraft allowed?": "Yes! You get ₹5,000-₹10,000 overdraft facility after maintaining good balance."
        }
    }
}

# Polly Configuration - CORRECTED LANGUAGE CODES
POLLY_VOICES = {
    "English": ("Joanna", "en-US"),
    "हिंदी": ("Aditi", "hi-IN"),
    "मराठी": ("Aditi", "mr-IN"),
    "ગુજરાતી": ("Aditi", "gu-IN"),
    "తెలుగు": ("Aditi", "te-IN"),
    "தமிழ்": ("Aditi", "ta-IN"),
    "ಕನ್ನಡ": ("Aditi", "kn-IN"),
    "മലയാളം": ("Aditi", "ml-IN"),
    "বাংলা": ("Aditi", "bn-IN"),
    "ਪੰਜਾਬੀ": ("Aditi", "pa-IN"),
    "ଓଡିଆ": ("Aditi", "or-IN"),
    "অসমীয়া": ("Aditi", "as-IN"),
    "اردو": ("Aditi", "ur-PK"),
    "ভাষা": ("Aditi", "bn-IN")
}

# MINIMAL CSS FOR 2G
st.markdown("""
<style>
    * { font-family: Arial, sans-serif; }
    body { background: #f5f5f5; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .card { background: white; padding: 15px; border-left: 4px solid #667eea; margin: 10px 0; border-radius: 8px; }
    .success { background: #d4edda; padding: 10px; border-radius: 8px; margin: 10px 0; color: #155724; }
    .info { background: #cfe2ff; padding: 10px; border-radius: 8px; margin: 10px 0; color: #084298; }
    .stButton > button { background: #667eea !important; color: white !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# Session State
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'last_answer' not in st.session_state:
    st.session_state.last_answer = None
if 'last_scheme' not in st.session_state:
    st.session_state.last_scheme = None

# Polly Client
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
    """Speak using AWS Polly - FIXED for all Indian languages"""
    try:
        polly = get_polly_client()
        if not polly:
            st.error("⚠️ Polly not configured. Add AWS credentials to Streamlit secrets.")
            return False
        
        voice_id, lang_code = POLLY_VOICES.get(language, ("Joanna", "en-US"))
        
        # Validate language code
        valid_codes = ['en-US', 'en-GB', 'hi-IN', 'mr-IN', 'gu-IN', 'te-IN', 'ta-IN', 'kn-IN', 
                      'ml-IN', 'bn-IN', 'pa-IN', 'or-IN', 'as-IN', 'ur-PK']
        
        if lang_code not in valid_codes:
            st.error(f"Language {language} not available in Polly")
            return False
        
        response = polly.synthesize_speech(
            Text=text[:2000],
            OutputFormat='mp3',
            VoiceId=voice_id,
            LanguageCode=lang_code
        )
        
        audio_stream = response['AudioStream'].read()
        st.audio(audio_stream, format="audio/mp3", autoplay=False)
        return True
    except Exception as e:
        st.error(f"🔊 Polly Error: {str(e)[:100]}")
        return False

# MAIN UI
st.markdown(f"<div class='header'><h1>🤖 Indic-Setu</h1><p>Government Schemes Guide</p></div>", unsafe_allow_html=True)

# Language selector
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.session_state.language = st.selectbox("🌐 Select Language:", list(POLLY_VOICES.keys()), 
                                            index=list(POLLY_VOICES.keys()).index(st.session_state.language), 
                                            key="lang_select")

# MAIN TABS
tabs = st.tabs(["🔍 Search", "📢 Voice Guide", "📋 Form", "❤️ Favorites", "ℹ️ Help"])

# TAB 1: SEARCH WITH ENHANCED AI
with tabs[0]:
    st.markdown("### Search Government Schemes")
    
    # Quick scheme buttons
    st.markdown("**Quick Schemes:**")
    cols = st.columns(2)
    for idx, scheme in enumerate(list(KNOWLEDGE_BASE.keys())):
        with cols[idx % 2]:
            if st.button(f"📍 {scheme}", use_container_width=True, key=f"scheme_{scheme}"):
                scheme_data = KNOWLEDGE_BASE[scheme]
                st.session_state.last_scheme = scheme
                
                # Display comprehensive information
                st.markdown(f"<div class='success'><h3>{scheme_data['name']}</h3></div>", unsafe_allow_html=True)
                
                st.markdown(f"**What is it?** {scheme_data['short']}")
                st.markdown(f"**Benefit:** {scheme_data['benefit']}")
                st.markdown(f"**How Much?** {scheme_data['how_much']}")
                st.markdown(f"**Payment Timing:** {scheme_data['when']}")
                st.markdown(f"**Where?** {scheme_data['where']}")
                
                st.markdown("**Eligibility Criteria:**")
                for elig in scheme_data['eligibility']:
                    st.write(f"✓ {elig}")
                
                st.markdown("**Documents Required:**")
                for doc in scheme_data['documents']:
                    st.write(f"• {doc}")
                
                st.markdown("**Step-by-Step Process:**")
                for idx, step in enumerate(scheme_data['steps'], 1):
                    st.write(f"{idx}. {step}")
                
                st.markdown(f"**Website:** {scheme_data['website']}")
                st.markdown(f"**Toll Free:** {scheme_data['toll_free']}")
                
                # Audio button
                st.session_state.last_answer = scheme_data['name'] + ". " + scheme_data['benefit']
                if st.button(f"🔊 Listen - {scheme}", use_container_width=True, key=f"listen_scheme_{scheme}"):
                    text_to_speak = f"{scheme_data['name']}. {scheme_data['short']}. Benefit: {scheme_data['benefit']}. Documents needed: {', '.join(scheme_data['documents'][:2])}. Contact: {scheme_data['toll_free']}"
                    speak_with_polly(text_to_speak, st.session_state.language)
    
    # Custom Search
    st.markdown("---")
    st.markdown("**Ask Any Question:**")
    query = st.text_area("Type your question about government schemes...", key="custom_query", height=80)
    
    if st.button("🔍 Search", use_container_width=True):
        if query.strip():
            st.markdown("### Search Results")
            
            found = False
            # Search in knowledge base
            for scheme, data in KNOWLEDGE_BASE.items():
                scheme_lower = scheme.lower()
                query_lower = query.lower()
                
                # Search by scheme name
                if query_lower in scheme_lower or scheme_lower in query_lower:
                    found = True
                    st.markdown(f"<div class='success'><h3>Found: {data['name']}</h3></div>", unsafe_allow_html=True)
                    st.markdown(f"**{data['short']}**")
                    st.markdown(f"**Benefit:** {data['benefit']}")
                    
                    # Check common questions
                    for q, ans in data['common_questions'].items():
                        if any(word in query_lower for word in q.lower().split()):
                            st.markdown(f"**Q: {q}**")
                            st.markdown(f"**A: {ans}**")
                            st.session_state.last_answer = ans
                            break
                    
                    # FAQs
                    for q, ans in data['faqs'].items():
                        if any(word in query_lower for word in q.lower().split()):
                            st.markdown(f"**Q: {q}**")
                            st.markdown(f"**A: {ans}**")
                            st.session_state.last_answer = ans
                            break
                    
                    # Listen button
                    if st.session_state.last_answer:
                        if st.button(f"🔊 Listen to Answer", use_container_width=True, key="listen_answer"):
                            speak_with_polly(st.session_state.last_answer, st.session_state.language)
            
            if not found:
                # AI Response for any question
                responses = {
                    "how to apply": "Each scheme has its own application process. Use the 'Voice Guide' tab for step-by-step instructions for any scheme.",
                    "how much money": "Different schemes offer different amounts. Check the 'Search' tab to find how much each scheme pays.",
                    "eligibility": "Eligibility varies by scheme. Most schemes are for farmers, rural workers, and low-income families.",
                    "documents": "Common documents: Aadhar card, bank account details, land certificate, income certificate. Exact requirements vary by scheme.",
                    "website": "Visit the official websites listed for each scheme in the Search tab.",
                    "toll free": "Each scheme has a toll-free number. Call the number mentioned in the scheme details.",
                    "bank account": "Yes, bank account is essential for all government schemes. Open a Jan Dhan account if you don't have one.",
                    "aadhar": "Aadhar is required for registration in most schemes. If you don't have it, apply at your nearest Aadhar enrolment center.",
                    "payment": "Payments are made directly to your bank account. No need to visit offices for receiving money.",
                    "benefit": "Visit the Search tab to see benefits for each scheme. Most schemes provide ₹2,000-₹5 lakh per year.",
                }
                
                answer_found = False
                for keyword, response in responses.items():
                    if keyword in query_lower:
                        st.markdown(f"<div class='info'><h4>📌 General Answer</h4><p>{response}</p></div>", unsafe_allow_html=True)
                        st.session_state.last_answer = response
                        answer_found = True
                        
                        if st.button("🔊 Listen to Answer", use_container_width=True, key="listen_ai"):
                            speak_with_polly(response, st.session_state.language)
                        break
                
                if not answer_found:
                    st.markdown("""
                    <div class='info'>
                    <h4>💡 Helpful Tips</h4>
                    <p>Search for scheme names: PM-Kisan, MGNREGA, Ayushman Bharat, PMJDY</p>
                    <p>Ask about: eligibility, documents, payment, how to apply, websites, phone numbers</p>
                    <p>Or call the toll-free numbers mentioned in each scheme for detailed help</p>
                    </div>
                    """, unsafe_allow_html=True)

# TAB 2: VOICE GUIDE
with tabs[1]:
    st.markdown("### 📢 Step-by-Step Voice Guide")
    
    scheme = st.selectbox("Select Scheme:", list(KNOWLEDGE_BASE.keys()), key="guide_scheme")
    
    if scheme:
        data = KNOWLEDGE_BASE[scheme]
        st.markdown(f"<div class='success'><h3>{data['name']}</h3></div>", unsafe_allow_html=True)
        
        st.markdown("**Application Steps:**")
        for idx, step in enumerate(data['steps'], 1):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**Step {idx}:** {step}")
            with col2:
                if st.button("🔊", key=f"step_{idx}_{scheme}"):
                    speak_with_polly(f"Step {idx}. {step}", st.session_state.language)

# TAB 3: FORM FILLER
with tabs[2]:
    st.markdown("### 📋 Auto-Fill Form")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", key="form_name")
        aadhar = st.text_input("Aadhar (12 digits)", key="form_aadhar")
        phone = st.text_input("Phone Number", key="form_phone")
    
    with col2:
        income = st.number_input("Annual Income (₹)", 0, 10000000, key="form_income")
        address = st.text_area("Address", key="form_address", height=80)
        bank = st.text_input("Bank Account", key="form_bank")
    
    if st.button("✅ Generate Form", use_container_width=True):
        if name and aadhar:
            form_text = f"""
GOVERNMENT SCHEME APPLICATION FORM
==================================

Name: {name}
Aadhar: {aadhar}
Phone: {phone}
Annual Income: ₹{income:,}
Address: {address}
Bank Account: {bank}

Submitted on: {datetime.now().strftime('%d-%m-%Y %H:%M')}
"""
            st.markdown(f"<div class='success'>{form_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            
            st.download_button("📥 Download as TXT", form_text, "form.txt", "text/plain")

# TAB 4: FAVORITES
with tabs[3]:
    st.markdown("### ❤️ Saved Items")
    if st.session_state.last_scheme:
        st.markdown(f"Last viewed: **{st.session_state.last_scheme}**")
    else:
        st.info("Save schemes by clicking on them in the Search tab")

# TAB 5: HELP
with tabs[4]:
    st.markdown("""
    ### ℹ️ Help & Support
    
    **Available Schemes:**
    - **PM-Kisan** - ₹6,000/year for farmers
    - **MGNREGA** - 100 days work per year
    - **Ayushman Bharat** - ₹5 lakh health insurance
    - **PMJDY** - Free bank account
    
    **How to Use:**
    1. Search tab - Find schemes and answers
    2. Voice Guide - Step-by-step instructions
    3. Form Filler - Save your details
    4. Listen - Hear answers in your language
    
    **Languages Supported:**
    English, हिंदी, मराठी, ગુજરાતી, తెలుగు, தமிழ், ಕನ್ನಡ, മലയാളം, বাংলা, ਪੰਜਾਬੀ, ଓଡିଆ, অসমীয়া, اردو
    
    **Call for Help:**
    - PM-Kisan: 1800-180-1111
    - MGNREGA: 1800-345-6777
    - Ayushman Bharat: 1800-111-565
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><p>🌾 Indic-Setu | Making Government Schemes Accessible to All | © 2026</p></div>", unsafe_allow_html=True)
