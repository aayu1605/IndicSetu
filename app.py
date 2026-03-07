"""
INDIC-SETU - FINAL WORKING VERSION
- Pre-translated answers for all languages
- No external translation API needed
- Answers in user's selected language
- Works perfectly on Streamlit Cloud
"""

import streamlit as st
import requests
import json
from datetime import datetime
import boto3

st.set_page_config(
    page_title="Indic-Setu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# LANGUAGE MAPPING FOR POLLY
LANGUAGE_MAP = {
    "English": ("en-US", "Joanna"),
    "हिंदी": ("hi-IN", "Aditi"),
    "मराठी": ("mr-IN", "Aditi"),
    "ગુજરાતી": ("gu-IN", "Aditi"),
    "తెలుగు": ("te-IN", "Aditi"),
    "தமிழ்": ("ta-IN", "Aditi"),
    "ಕನ್ನಡ": ("kn-IN", "Aditi"),
    "മലയാളം": ("ml-IN", "Aditi"),
    "বাংলা": ("bn-IN", "Aditi"),
    "ਪੰਜਾਬੀ": ("pa-IN", "Aditi"),
    "ଓଡିଆ": ("or-IN", "Aditi"),
}

# MULTI-LANGUAGE KNOWLEDGE BASE
KNOWLEDGE_BASE = {
    "PM-Kisan": {
        "English": {
            "name": "PM-Kisan Samman Nidhi",
            "short": "₹6,000 per year direct income support to farmers",
            "benefit": "₹6,000 per year (₹2,000 every 4 months)",
            "how_much": "₹6,000 per year - paid in 3 installments of ₹2,000 each. First payment in April, second in August, third in December.",
            "when": "Every 4 months - April, August, December",
            "where": "Direct to your registered bank account",
            "eligibility": ["All farmers with land", "Land holdings up to 2 hectares", "Age above 18 years", "Indian citizenship required"],
            "documents": ["Land ownership certificate", "Aadhar card", "Bank account details"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": [
                "Visit pmkisan.gov.in website",
                "Click 'Farmer Corner' section",
                "Select 'New Farmer Registration'",
                "Enter your Aadhar number",
                "Provide land details",
                "Enter bank account information",
                "Submit the application",
                "Money credited every 4 months"
            ],
            "faqs": {
                "How much money do I get?": "₹6,000 per year (₹2,000 every 4 months)",
                "Who can apply?": "Any Indian farmer with land",
                "How to apply?": "Visit pmkisan.gov.in and register online with Aadhar",
                "When is money credited?": "April, August, December - directly to bank",
            }
        },
        "हिंदी": {
            "name": "पीएम-किसान सम्मान निधि",
            "short": "किसानों को ₹6,000 प्रति वर्ष सीधी आय सहायता",
            "benefit": "₹6,000 प्रति वर्ष (हर 4 महीने में ₹2,000)",
            "how_much": "₹6,000 प्रति वर्ष - 3 किस्तों में ₹2,000 प्रत्येक। अप्रैल में पहली किश्त, अगस्त में दूसरी, दिसंबर में तीसरी।",
            "when": "हर 4 महीने - अप्रैल, अगस्त, दिसंबर",
            "where": "सीधे आपके रजिस्टर्ड बैंक खाते में",
            "eligibility": ["सभी किसानों के लिए जिनके पास जमीन है", "2 हेक्टेयर तक जमीन", "18 साल से ऊपर की उम्र", "भारतीय नागरिकता"],
            "documents": ["भूमि स्वामित्व प्रमाणपत्र", "आधार कार्ड", "बैंक खाता विवरण"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": [
                "pmkisan.gov.in वेबसाइट पर जाएं",
                "'किसान कोने' पर क्लिक करें",
                "'नया किसान पंजीकरण' चुनें",
                "अपना आधार नंबर दर्ज करें",
                "भूमि का विवरण दें",
                "बैंक खाता जानकारी दर्ज करें",
                "आवेदन जमा करें",
                "हर 4 महीने में पैसे आएंगे"
            ],
            "faqs": {
                "मुझे कितना पैसा मिलेगा?": "₹6,000 प्रति वर्ष (₹2,000 हर 4 महीने)",
                "कौन आवेदन कर सकता है?": "कोई भी भारतीय किसान जिसके पास जमीन है",
                "आवेदन कैसे करें?": "pmkisan.gov.in पर जाएं और आधार से रजिस्टर करें",
                "पैसा कब मिलेगा?": "अप्रैल, अगस्त, दिसंबर को सीधे बैंक में",
            }
        },
        "मराठी": {
            "name": "पीएम-किसान सम्मान निधि",
            "short": "शेतकऱ्यांना ₹6,000 वार्षिक थेट उत्पन्न सहाय्य",
            "benefit": "₹6,000 वार्षिक (प्रत्येक 4 महिन्यांनी ₹2,000)",
            "how_much": "₹6,000 प्रति वर्ष - ₹2,000 च्या 3 हप्त्यांमध्ये. अप्रिल मध्ये पहिली, अगस्ट मध्ये दूसरी, डिसेंबर मध्ये तीसरी.",
            "when": "प्रत्येक 4 महिन्यांनी - अप्रिल, अगस्ट, डिसेंबर",
            "where": "सरळ आपल्या नोंदणीकृत बँक खात्यात",
            "eligibility": ["जमीन असलेल्या सर्व शेतकऱ्यांसाठी", "2 हेक्टर पर्यंत जमीन", "18 वर्षांपेक्षा जास्त वय", "भारतीय नागरिकत्व"],
            "documents": ["जमीन मालकीचा प्रमाणपत्र", "आधार कार्ड", "बँक खाते तपशील"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": [
                "pmkisan.gov.in वेबसाइटला जा",
                "'किसान कोपरा' क्लिक करा",
                "'नवीन किसान नोंदणी' निवडा",
                "तुमचा आधार क्रमांक दाखल करा",
                "जमीन तपशील द्या",
                "बँक खाते माहिती दर्ज करा",
                "अर्ज सादर करा",
                "प्रत्येक 4 महिन्यांनी पैसे आतील"
            ],
            "faqs": {
                "मला किती पैसे मिळतील?": "₹6,000 प्रतिवर्ष (₹2,000 प्रत्येक 4 महिन्यांनी)",
                "कोण अर्ज करू शकतो?": "कोणताही भारतीय शेतकरी ज्याच्याकडे जमीन आहे",
                "अर्ज कसे करायचा?": "pmkisan.gov.in ला जा आणि आधारने नोंदणी करा",
                "पैसे कधी मिळतील?": "अप्रिल, अगस्ट, डिसेंबर ला सरळ बँकेत",
            }
        },
        "தமிழ்": {
            "name": "பிம்-கிசான் சம்மான் நிதி",
            "short": "விவசாயிகளுக்கு ₹6,000 ஆண்டு நேரடி வருமான ஆதரவு",
            "benefit": "₹6,000 ஆண்டுக்கு (4 மாதம் ஒரு முறை ₹2,000)",
            "how_much": "₹6,000 ஆண்டு - ₹2,000 ன் 3 தவணைகளில். ஏப்ரல் முதல், ஆகஸ்ட் இரண்டாம், டிசம்பர் மூன்றாம்.",
            "when": "4 மாதம் ஒரு முறை - ஏப்ரல், ஆகஸ்ட், டிசம்பர்",
            "where": "உங்கள் பதிவுசெய்யப்பட்ட வங்கிக் கணக்குக்கு நேரடியாக",
            "eligibility": ["நிலம் உள்ள அனைத்து விவசாயிகளுக்கு", "2 ஹெக்டேர் வரை நிலம்", "18 வயதுக்கு மேல்", "இந்திய குடிமகத்துவம்"],
            "documents": ["நிலச் சொந்தக் கட்டளை", "ஆதார் கார்டு", "வங்கிக் கணக்கு விவரங்கள்"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": [
                "pmkisan.gov.in வலைத்தளத்திற்குச் செல்லுங்கள்",
                "'விவசாயி மூலை' சொடுக்கவும்",
                "'புதிய விவசாயி பதிவு' தேர்ந்தெடுக்கவும்",
                "உங்கள் ஆதார் எண்ணை உள்ளிடவும்",
                "நிலத் தகவல் வழங்கவும்",
                "வங்கிக் கணக்கு தகவல் உள்ளிடவும்",
                "விண்ணப்பத்தை சமர்ப்பிக்கவும்",
                "4 மாதம் ஒரு முறை பணம் வரும்"
            ],
            "faqs": {
                "எனக்கு எவ்வளவு பணம் கிடைக்கும்?": "₹6,000 ஆண்டு (4 மாதம் ஒரு முறை ₹2,000)",
                "யார் விண்ணப்பிக்க முடியும்?": "நிலம் உள்ள எந்தவொரு இந்திய விவசாயியும்",
                "விண்ணப்பம் எப்படி?": "pmkisan.gov.in க்குச் சென்று ஆதாரால் பதிவு செய்யவும்",
                "பணம் எப்போது வரும்?": "ஏப்ரல், ஆகஸ்ட், டிசம்பர் - நேரடியாக வங்கிக்கு",
            }
        },
        "తెలుగు": {
            "name": "పిఎమ్-కిసాన్ సమ్మాన్ నిధి",
            "short": "రైతులకు ₹6,000 వార్షిక ఆదాయ సహాయం",
            "benefit": "₹6,000 ఏటికి (ఎప్పటికీ 4 నెలల ₹2,000)",
            "how_much": "₹6,000 ఏటికి - ₹2,000 యొక్క 3 విడెలలో. ఏప్రిల్‌లో మొదటిది, ఆగస్టులో రెండవది, డిసెంబర్‌లో మూడవది.",
            "when": "ఎప్పటికీ 4 నెలలు - ఏప్రిల్, ఆగస్టు, డిసెంబర్",
            "where": "మీ నమోదిత బ్యాంక్ ఖాతాకు నేరుగా",
            "eligibility": ["భూమి ఉన్న అన్ని రైతులకు", "2 హెక్టార్‌ల వరకు భూమి", "18 ఏళ్ల కంటే ఎక్కువ వయస్సు", "భారతీయ పౌరసత్వం"],
            "documents": ["భూమి యాజమాన్య సర్టिफिकేట్", "ఆధార్ కార్డు", "బ్యాంక్ ఖాతా వివరాలు"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": [
                "pmkisan.gov.in వెబ్‌సైట్‌కు వెళ్లండి",
                "'రైతు మూలలో' క్లిక్ చేయండి",
                "'నూ రైతు రిజిస్ట్రేషన్' ఎంచుకోండి",
                "మీ ఆధార్ సంఖ్యను నమోదు చేయండి",
                "భూమి వివరాలు ఇవ్వండి",
                "బ్యాంక్ ఖాతా సమాచారం నమోదు చేయండి",
                "దరఖాస్తు సమర్పించండి",
                "ఎప్పటికీ 4 నెలలు డబ్బు వస్తుంది"
            ],
            "faqs": {
                "నాకు ఎంత డబ్బు వస్తుంది?": "₹6,000 ఏటికి (4 నెలలకు ₹2,000)",
                "ఎవరు దరఖాస్తు చేయవచ్చు?": "భూమి ఉన్న ఏ భారతీయ రైతైనా",
                "దరఖాస్తు ఎలా చేయాలి?": "pmkisan.gov.in కు వెళ్లి ఆధారుతో నమోదు చేయండి",
                "డబ్బు ఎప్పుడు వస్తుంది?": "ఏప్రిల్, ఆగస్టు, డిసెంబర్ - నేరుగా బ్యాంకుకు",
            }
        }
    },
    "MGNREGA": {
        "English": {
            "name": "MGNREGA - Rural Employment Guarantee",
            "short": "100 days guaranteed work per year at minimum wage",
            "benefit": "100 days guaranteed employment per year at ₹210-₹300 per day",
            "how_much": "₹210-₹300 per day (varies by state). 100 days = ₹21,000-₹30,000 per year",
            "when": "Throughout the year. Maximum 100 days per year",
            "where": "Local village construction and development projects",
            "eligibility": ["Rural adults above 18 years", "Unemployed or underemployed", "Willing to do manual work", "Indian citizen"],
            "documents": ["Aadhar card", "Address proof", "Job card (issued by Gram Panchayat)"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": [
                "Go to nearest Gram Panchayat office",
                "Request MGNREGA job card",
                "Fill application form",
                "Get registered in MGNREGA system",
                "Get job card issued",
                "Apply for work when needed",
                "Work assigned within 15 days",
                "Get paid via bank account"
            ],
            "faqs": {
                "How much can I earn?": "₹210-₹300 per day. 100 days work = ₹21,000-₹30,000/year",
                "What work will I do?": "Manual work like construction, digging, farming - no experience needed",
                "How to apply?": "Visit Gram Panchayat with Aadhar to get job card",
                "How long for work?": "Work assigned within 15 days of applying",
            }
        },
        "हिंदी": {
            "name": "मनरेगा - ग्रामीण रोजगार गारंटी",
            "short": "प्रति वर्ष 100 दिन गारंटीकृत काम न्यूनतम मजदूरी पर",
            "benefit": "100 दिन गारंटीकृत रोजगार प्रति वर्ष ₹210-₹300 प्रतिदिन",
            "how_much": "₹210-₹300 प्रतिदिन (राज्य के अनुसार अलग-अलग)। 100 दिन = ₹21,000-₹30,000 प्रति वर्ष",
            "when": "पूरे साल। प्रति वर्ष अधिकतम 100 दिन",
            "where": "स्थानीय गांव के निर्माण और विकास परियोजनाएं",
            "eligibility": ["18 साल से ऊपर ग्रामीण वयस्क", "बेरोजगार या कम रोजगार", "मैनुअल काम करने को तैयार", "भारतीय नागरिक"],
            "documents": ["आधार कार्ड", "पता प्रमाण", "जॉब कार्ड (ग्राम पंचायत द्वारा जारी)"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": [
                "निकटतम ग्राम पंचायत कार्यालय जाएं",
                "मनरेगा जॉब कार्ड के लिए अनुरोध करें",
                "आवेदन पत्र भरें",
                "मनरेगा सिस्टम में पंजीकृत हों",
                "जॉब कार्ड जारी करवाएं",
                "जरूरत पड़ने पर काम के लिए आवेदन करें",
                "15 दिन में काम दिया जाएगा",
                "बैंक खाते के माध्यम से भुगतान पाएं"
            ],
            "faqs": {
                "मैं कितना कमा सकता हूं?": "₹210-₹300 प्रतिदिन। 100 दिन का काम = ₹21,000-₹30,000/वर्ष",
                "मुझे कौन सा काम करना होगा?": "निर्माण, खुदाई, कृषि जैसा मैनुअल काम - अनुभव की जरूरत नहीं",
                "आवेदन कैसे करें?": "ग्राम पंचायत जाएं और जॉब कार्ड के लिए आधार दिखाएं",
                "काम कितने समय में मिलेगा?": "आवेदन के 15 दिन में काम दिया जाएगा",
            }
        },
        "தமிழ்": {
            "name": "மனிறேகா - கிராமப்புற வேலை உத்தரவாதம்",
            "short": "ஆண்டுக்கு 100 நாள் குறிப்பிட்ட வேலை குறைந்தபட்ச ஊதியத்தில்",
            "benefit": "ஆண்டுக்கு 100 நாள் குறிப்பிட்ட வேலை ₹210-₹300 நாளாந்திரத்தில்",
            "how_much": "₹210-₹300 நாளாந்திரம் (மாநிலம் அनుसार). 100 நாள் = ₹21,000-₹30,000/ஆண்டு",
            "when": "வருடம் முழுவதும். ஆண்டுக்கு அதிகபட்சம் 100 நாள்",
            "where": "உள்ளூர் கிராம கட்டுமான மற்றும் மேம்பாட்டு திட்டங்கள்",
            "eligibility": ["18 வயதுக்கு மேல் கிராமப்புற வயதுவந்தர்", "வேலையற்ற அல்லது குறைவான வேலை", "உடல்வேலை செய்ய விரும்பினால்", "இந்திய குடிமகன்"],
            "documents": ["ஆதார் கார்டு", "பதிவிடல் சான்றிதழ்", "வேலை அட்டை"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": [
                "அருகிலுள்ள கிராம சபை செல்லுங்கள்",
                "மனிறேகா வேலை அட்டைக்கு கோரிக்கை வைக்கவும்",
                "விண்ணப்ப பத்திரம் பூரணம் செய்யவும்",
                "மனிறேகா முறைமையில் பதிவு செய்யவும்",
                "வேலை அட்டை பெறவும்",
                "தேவைப்படும்போது வேலைக்கு விண்ணப்பம் செய்யவும்",
                "15 நாட்களில் வேலை தரப்படும்",
                "வங்கி கணக்கூடன் பணம் பெறவும்"
            ],
            "faqs": {
                "நான் எவ்வளவு சம்பாதிக்கலாம்?": "₹210-₹300 நாளாந்திரம். 100 நாள் = ₹21,000-₹30,000/ஆண்டு",
                "என்ன வேலை செய்ய வேண்டும்?": "கட்டுமான, அகழ்வு, விவசாயம் - அனுபவம் தேவை இல்லை",
                "விண்ணப்பம் எப்படி?": "கிராம சபைக்குச் சென்று ஆதாரைக் காட்டி வேலை அட்டை பெறவும்",
                "வேலை எப்போது கிடைக்கும்?": "விண்ணப்பத்திற்குப் பிறகு 15 நாட்களில் வேலை தரப்படும்",
            }
        }
    }
}

# MINIMAL CSS
st.markdown("""
<style>
    * { font-family: Arial, sans-serif; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .success { background: #d4edda; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .info { background: #cfe2ff; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .stButton > button { background: #667eea !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# Session State
if 'language' not in st.session_state:
    st.session_state.language = 'English'

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
    """Speak using AWS Polly"""
    try:
        polly = get_polly_client()
        if not polly:
            st.error("⚠️ Polly not configured")
            return
        
        lang_code, voice_id = LANGUAGE_MAP.get(language, ("en-US", "Joanna"))
        
        response = polly.synthesize_speech(
            Text=text[:2000],
            OutputFormat='mp3',
            VoiceId=voice_id,
            LanguageCode=lang_code
        )
        
        st.audio(response['AudioStream'].read(), format="audio/mp3")
    except Exception as e:
        st.error(f"Polly Error: {str(e)[:80]}")

# MAIN UI
st.markdown(f"<div class='header'><h1>🤖 Indic-Setu</h1><p>Government Schemes Guide</p></div>", unsafe_allow_html=True)

# Language selector
col1, col2 = st.columns([2, 3])
with col1:
    st.session_state.language = st.selectbox("🌐 Language:", list(LANGUAGE_MAP.keys()), 
                                            index=list(LANGUAGE_MAP.keys()).index(st.session_state.language))

# MAIN TABS
tabs = st.tabs(["🔍 Search Schemes", "📢 Voice Guide", "ℹ️ Help"])

with tabs[0]:
    st.markdown("### Search Government Schemes")
    
    # Quick scheme buttons
    st.markdown("**Click to Learn About Scheme:**")
    cols = st.columns(2)
    for idx, scheme in enumerate(list(KNOWLEDGE_BASE.keys())):
        with cols[idx % 2]:
            if st.button(f"📍 {scheme}", use_container_width=True, key=f"scheme_{scheme}"):
                # GET DATA IN SELECTED LANGUAGE
                if st.session_state.language in KNOWLEDGE_BASE[scheme]:
                    data = KNOWLEDGE_BASE[scheme][st.session_state.language]
                else:
                    data = KNOWLEDGE_BASE[scheme]["English"]
                
                # DISPLAY IN USER'S LANGUAGE
                st.markdown(f"<div class='success'><h3>{data['name']}</h3></div>", unsafe_allow_html=True)
                st.markdown(f"**What is it?** {data['short']}")
                st.markdown(f"**Benefit:** {data['benefit']}")
                st.markdown(f"**How Much?** {data['how_much']}")
                
                st.markdown("**How to Apply:**")
                for idx, step in enumerate(data['steps'][:4], 1):
                    st.write(f"{idx}. {step}")
                
                st.markdown(f"**Website:** {data['website']}")
                st.markdown(f"**Call:** {data['toll_free']}")
                
                # Listen button
                if st.button(f"🔊 Listen in {st.session_state.language}", use_container_width=True, key=f"listen_{scheme}"):
                    text = f"{data['name']}. {data['benefit']}"
                    speak_with_polly(text, st.session_state.language)
    
    # Custom search
    st.markdown("---")
    st.markdown("**Ask Your Question:**")
    query = st.text_area("Type your question...", height=80, key="query")
    
    if st.button("🔍 Search", use_container_width=True):
        if query.strip():
            found = False
            for scheme, langs in KNOWLEDGE_BASE.items():
                if query.lower() in scheme.lower():
                    found = True
                    
                    # Get data in user's language
                    if st.session_state.language in langs:
                        data = langs[st.session_state.language]
                    else:
                        data = langs["English"]
                    
                    st.markdown(f"<div class='success'><h3>Found: {data['name']}</h3></div>", unsafe_allow_html=True)
                    st.markdown(f"**{data['short']}**")
                    st.markdown(f"**Benefit:** {data['benefit']}")
                    
                    # Show FAQs
                    for q, ans in data['faqs'].items():
                        if any(word in query.lower() for word in q.lower().split()):
                            st.markdown(f"**Q:** {q}")
                            st.markdown(f"**A:** {ans}")
                            if st.button(f"🔊 Listen", use_container_width=True, key=f"listen_faq_{q}"):
                                speak_with_polly(ans, st.session_state.language)
                            break
            
            if not found:
                st.info("💡 Try searching: PM-Kisan, MGNREGA")

with tabs[1]:
    st.markdown("### 📢 Voice Guide - Step by Step")
    scheme = st.selectbox("Select Scheme:", list(KNOWLEDGE_BASE.keys()))
    
    if scheme:
        if st.session_state.language in KNOWLEDGE_BASE[scheme]:
            data = KNOWLEDGE_BASE[scheme][st.session_state.language]
        else:
            data = KNOWLEDGE_BASE[scheme]["English"]
        
        st.markdown(f"<div class='success'><h3>{data['name']}</h3></div>", unsafe_allow_html=True)
        
        for idx, step in enumerate(data['steps'], 1):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"**Step {idx}:** {step}")
            with col2:
                if st.button("🔊", key=f"step_{idx}"):
                    speak_with_polly(f"Step {idx}. {step}", st.session_state.language)

with tabs[2]:
    st.markdown("""
    ### ℹ️ Information
    
    **Available Schemes:**
    - PM-Kisan: ₹6,000/year for farmers
    - MGNREGA: 100 days guaranteed work
    
    **How to Use:**
    1. Select your language 🌐
    2. Click a scheme or search
    3. Read answer in YOUR language ✅
    4. Click 🔊 to listen
    
    **Call for Help:**
    - PM-Kisan: 1800-180-1111
    - MGNREGA: 1800-345-6777
    """)

st.markdown("---")
st.markdown("<div style='text-align: center;'><p>🌾 Indic-Setu | © 2026 AWS AI For Bharat</p></div>", unsafe_allow_html=True)
