"""
Indic-Setu - DEBUG VERSION
Shows EXACTLY what Lambda is returning
"""

import streamlit as st
import requests
import json

st.set_page_config(page_title="Indic-Setu DEBUG", layout="wide")

st.title("🔧 Indic-Setu DEBUG MODE")
st.write("This shows exactly what your Lambda is returning")

API_URL = "https://i66i3hu9a4.execute-api.us-east-1.amazonaws.com/prod/query"

st.markdown("---")
st.write("### 1. Test Lambda Connection")

# Sidebar
occupation = st.sidebar.text_input("Occupation:", "Farmer (किसान)")
income = st.sidebar.number_input("Income:", 0, 1000000, 80000)

col1, col2 = st.columns(2)

with col1:
    query = st.text_area("Question:", "How do I apply for PM-Kisan?", height=100)

with col2:
    if st.button("🧪 TEST LAMBDA", use_container_width=True):
        st.write(f"**API URL:** {API_URL}")
        st.write(f"**Payload:**")
        
        payload = {
            "query": query,
            "income": int(income),
            "occupation": occupation
        }
        
        st.json(payload)
        
        st.write("---")
        st.write("**Sending request...**")
        
        try:
            response = requests.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            st.write(f"**Status Code:** `{response.status_code}`")
            
            st.write("**Raw Response Text:**")
            st.code(response.text)
            
            st.write("**Parsed JSON:**")
            try:
                result = response.json()
                st.json(result)
                
                st.write("---")
                st.write("### Response Fields:")
                
                for key, value in result.items():
                    st.write(f"- **{key}**: {type(value).__name__}")
                    if key == 'body' and isinstance(value, str):
                        st.write("  (This is a STRING, not JSON!)")
                        st.write("  Trying to parse...")
                        try:
                            parsed_body = json.loads(value)
                            st.json(parsed_body)
                        except:
                            st.write("  Could not parse body as JSON")
                
                # Check for 'answer' field
                st.write("---")
                st.write("### Checking 'answer' field:")
                if 'answer' in result:
                    st.write("✅ 'answer' field found!")
                    st.write(f"Content: {result['answer'][:200]}...")
                else:
                    st.write("❌ 'answer' field NOT found!")
                    st.write("Available fields:", list(result.keys()))
                    
            except json.JSONDecodeError as e:
                st.error(f"Could not parse response as JSON: {e}")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.write("### 2. What to Look For")

st.info("""
**Good Response** should have:
- Status Code: 200
- JSON with 'answer' field
- 'answer' contains actual text (not "No information available")
- 'eligibility_status' field
- 'income' and 'occupation' fields

**Bad Response** might have:
- Status Code: 500
- 'answer' = "No information available"
- Missing fields
- Empty strings
""")

st.markdown("---")
st.write("### 3. Troubleshooting")

if st.checkbox("Show Lambda Code Check"):
    st.write("""
**If 'answer' field is missing or empty:**
- Lambda code was NOT updated
- Go to AWS Lambda console
- Replace code with LAMBDA_ULTRA_SIMPLE.py
- Click Deploy
- Wait 30 seconds
- Try again

**If status is 500:**
- Lambda has an error
- Check CloudWatch logs
- Share the error message
    """)

if st.checkbox("Show Streamlit App Code Issues"):
    st.write("""
**If response looks good but Streamlit doesn't show it:**
- The Streamlit app might be looking for wrong field name
- Check if response has 'answer' field
- Check if it's being displayed correctly
    """)
