"""
Indic-Setu - DEBUG VERSION
Shows exactly what's happening with API URL configuration
"""

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Indic-Setu | DEBUG",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Indic-Setu DEBUG MODE")
st.write("This shows what's actually happening with your configuration")

# ===== DEBUG SECTION =====
st.markdown("---")
st.markdown("## 🔍 DEBUG INFORMATION")

# Check 1: Can we access secrets at all?
st.write("### 1. Checking Streamlit Secrets Access")
try:
    all_secrets = dict(st.secrets)
    st.write("✅ Secrets dictionary is accessible")
    st.write("**Available secret keys:**", list(all_secrets.keys()))
except Exception as e:
    st.write("❌ Cannot access secrets:", str(e))
    all_secrets = {}

# Check 2: Can we get the API URL specifically?
st.write("### 2. Checking API URL Secret")
try:
    api_url_from_secrets = st.secrets.get("api_url")
    if api_url_from_secrets:
        st.write("✅ Found api_url in secrets")
        st.write("**Value:**", api_url_from_secrets)
        api_url = api_url_from_secrets
    else:
        st.write("⚠️ api_url key exists but is empty or None")
        api_url = None
except Exception as e:
    st.write("❌ Error reading api_url:", str(e))
    api_url = None

# Check 3: Try different ways to access it
st.write("### 3. Alternative Secret Access Methods")

try:
    method1 = st.secrets["api_url"]
    st.write("✅ Method 1 (direct access): Success")
    st.write("   Value:", method1)
except:
    st.write("❌ Method 1 (direct access): Failed")
    method1 = None

try:
    method2 = st.secrets.get("api_url", "NOT_FOUND")
    st.write("✅ Method 2 (.get()): Success")
    st.write("   Value:", method2)
except:
    st.write("❌ Method 2 (.get()): Failed")
    method2 = None

# Final API URL determination
st.write("### 4. Final API URL Determination")
if api_url:
    st.success(f"✅ Using: {api_url}")
    use_api_url = api_url
else:
    default_url = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"
    st.warning(f"⚠️ Using default: {default_url}")
    use_api_url = default_url

# ===== END DEBUG SECTION =====
st.markdown("---")

# Allow manual override
st.write("### 5. Manual Override")
st.info("If the above shows errors, you can manually paste your API URL below:")
manual_api_url = st.text_input(
    "Manual API URL (leave empty to use auto-detected):",
    value="",
    placeholder="https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"
)

if manual_api_url:
    final_api_url = manual_api_url
    st.success(f"Using manual URL: {final_api_url}")
else:
    final_api_url = use_api_url
    st.info(f"Using auto-detected URL: {final_api_url}")

# ===== TEST API CALL =====
st.markdown("---")
st.markdown("## 🧪 Test API Call")

if st.button("Click to test API connection"):
    st.write(f"Testing with URL: {final_api_url}")
    
    try:
        payload = {
            "query": "test",
            "income": 50000,
            "occupation": "Farmer"
        }
        
        with st.spinner("Sending request..."):
            response = requests.post(
                final_api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        
        st.write(f"**Status Code:** {response.status_code}")
        
        if response.status_code == 200:
            st.success("✅ API CALL SUCCESSFUL!")
            result = response.json()
            st.write("**Response:**")
            st.json(result)
        else:
            st.error(f"❌ API returned status {response.status_code}")
            st.write("**Response:**")
            st.write(response.text)
    
    except requests.exceptions.ConnectionError as e:
        st.error(f"❌ Connection Error: Cannot reach {final_api_url}")
        st.write("Check if:")
        st.write("1. URL is correct")
        st.write("2. AWS API Gateway is deployed")
        st.write("3. POST /query method exists")
    
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out - API took too long to respond")
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# ===== INSTRUCTIONS =====
st.markdown("---")
st.markdown("## 📋 What to Do Next")

st.info("""
**If debug shows ✅ for everything:**
- Secrets are configured correctly
- Use the app_streamlit_cloud.py code (it should work)
- Test the API call button above

**If debug shows ❌ for secrets:**
- Go to Streamlit Cloud Settings → Secrets
- Add this line: `api_url = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"`
- Save and redeploy

**If API test fails:**
- Check AWS Lambda CloudWatch logs
- Verify POST /query method exists in API Gateway
- Verify Lambda is working
""")
