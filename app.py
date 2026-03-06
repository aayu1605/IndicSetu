"""
Indic-Setu Frontend - FIXED VERSION
Correctly parses Lambda response with body field
"""

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Indic-Setu | Sarkari Yojnayen",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .header-banner {
        background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .header-banner h1 {
        color: white;
        margin: 0;
    }
    .badge-high {
        background: #2ecc71;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
    }
    .badge-standard {
        background: #3498db;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
    }
    .result-box {
        background: white;
        padding: 20px;
        border-left: 6px solid #2ecc71;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-banner">
    <h1>🌾 Indic-Setu</h1>
    <p>Sarkari Yojnaon ke Liye Aasaan Pataptar</p>
    <p style="opacity: 0.9;">Government Schemes Made Simple</p>
</div>
""", unsafe_allow_html=True)

# API URL
API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

# Sidebar
st.sidebar.title("⚙️ Your Details")

occupation = st.sidebar.selectbox(
    "Select your occupation",
    [
        "Farmer (किसान)",
        "Agricultural Labourer (कृषि मजदूर)",
        "Weaver (बुनकर)",
        "Artisan (शिल्पकार)",
        "Self-Employed (स्व-नियोजित)",
        "Unemployed (बेरोजगार)",
        "Student (विद्यार्थी)",
        "Other (अन्य)"
    ]
)

income = st.sidebar.number_input(
    "Annual Income (₹)",
    min_value=0,
    value=80000,
    step=10000
)

# Check eligibility
st.sidebar.markdown("### ✅ Eligibility Preview")
if income < 100000 and ("Farmer" in occupation or "Labourer" in occupation):
    st.sidebar.success("🎯 High-Priority Eligible!")
elif income < 300000:
    st.sidebar.info("📋 Standard Eligible")
else:
    st.sidebar.warning("⚠️ Limited Eligibility")

# Main content
st.markdown("### 🤔 What would you like to know?")

query = st.text_area(
    "Ask about government schemes...",
    placeholder="उदाहरण: मुझे PM-Kisan के लिए आवेदन कैसे करना है?",
    height=100,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_button = st.button("🔍 खोजें | Search", use_container_width=True)

with col2:
    clear_button = st.button("🔄 Clear", use_container_width=True)

with col3:
    help_button = st.button("❓ Help", use_container_width=True)

if clear_button:
    st.rerun()

if help_button:
    st.info("""
    ### How to Use Indic-Setu:
    
    1. **Select your occupation** from the sidebar
    2. **Enter your annual income**
    3. **Ask any question** about government schemes
    4. **Click Search** to get personalized information
    5. **Check your eligibility status** and available schemes
    """)

# API Call
if search_button and query.strip():
    with st.spinner("🔄 Searching government schemes..."):
        try:
            payload = {
                "query": query,
                "income": int(income),
                "occupation": occupation
            }
            
            response = requests.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                # Parse the response - Lambda wraps it in statusCode, headers, body
                api_response = response.json()
                
                # Extract the body (which contains the actual data as a string)
                if isinstance(api_response, dict) and 'body' in api_response:
                    # Body is a string, parse it as JSON
                    if isinstance(api_response['body'], str):
                        result = json.loads(api_response['body'])
                    else:
                        result = api_response['body']
                else:
                    # Response doesn't have body wrapper, use as-is
                    result = api_response
                
                # Display eligibility badge
                st.markdown("### ✨ Your Eligibility Status")
                
                eligibility = result.get('eligibility_status', 'Unknown')
                if eligibility == 'High-Priority':
                    st.markdown(f'<div class="badge-high">✅ {eligibility}</div>', unsafe_allow_html=True)
                    st.success("🎉 You are HIGH-PRIORITY eligible!")
                else:
                    st.markdown(f'<div class="badge-standard">📋 {eligibility}</div>', unsafe_allow_html=True)
                    st.info("Multiple schemes are available for you!")
                
                # Display answer
                st.markdown("### 📝 Detailed Information")
                answer = result.get('answer', 'No information available')
                st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)
                
                # Profile summary
                st.markdown("### 📋 Your Profile")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Annual Income", f"₹{income:,}")
                
                with col2:
                    st.metric("Occupation", occupation.split("(")[0].strip())
                
                with col3:
                    st.metric("Status", eligibility)
                
                # Next steps
                st.markdown("### 🎯 Next Steps")
                st.info("""
                ✅ Save this information for reference
                ✅ Contact your local Gram Panchayat or government office
                ✅ Prepare required documents (Aadhar, Land Records, Bank Account)
                ✅ Apply online via official government portals
                ✅ Track your application status
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
                st.error(f"❌ API Error (Status {response.status_code})")
                st.error(f"Response: {response.text}")
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to API. Check your internet connection.")
        
        except json.JSONDecodeError as e:
            st.error(f"❌ Error parsing response: {str(e)}")
        
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
    <p>🌾 <strong>Indic-Setu</strong> | Making Government Schemes Accessible to Rural India</p>
    <p>सरकारी योजनाओं को आसान और सुलभ बनाना</p>
    <p style="font-size: 0.85em; opacity: 0.7;">© 2024 | Empowering Rural Communities</p>
</div>
""", unsafe_allow_html=True)
