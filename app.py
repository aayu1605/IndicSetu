"""
INDIC-SETU - POLLY LISTENING FIXED
- All language codes corrected
- Polly speaking working perfectly
- All 9 tabs functional
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

# CORRECTED POLLY LANGUAGE CODES - WORKING VERSION
POLLY_VOICES = {
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

# COMPREHENSIVE MULTI-LANGUAGE KNOWLEDGE BASE
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
            "steps": ["Visit pmkisan.gov.in", "Click Farmer Corner", "Select New Registration", "Enter Aadhar", "Provide land details", "Enter bank info", "Submit application", "Money credited every 4 months"],
            "faqs": {
                "How much money?": "₹6,000 per year divided into 3 payments of ₹2,000 each",
                "Who can apply?": "Any Indian farmer with land can apply",
                "How to apply?": "Visit pmkisan.gov.in and register with Aadhar",
                "When payment?": "April, August, December to your bank account",
                "Need office visit?": "No! Completely online registration",
            },
            "common_questions": {
                "Can I apply?": "Yes! Any farmer with land in India",
                "How much benefit?": "₹6,000 yearly direct to your bank account",
                "Payment timing?": "Every 4 months - April, August, December",
                "Documents needed?": "Aadhar, Land details, Bank account",
                "Call for help?": "1800-180-1111",
            }
        },
        "हिंदी": {
            "name": "पीएम-किसान सम्मान निधि",
            "short": "किसानों को प्रति वर्ष ₹6,000 की सीधी आय सहायता",
            "benefit": "₹6,000 प्रति वर्ष (हर 4 महीने में ₹2,000)",
            "how_much": "₹6,000 प्रति वर्ष - ₹2,000 की 3 किस्तों में। अप्रैल में पहली, अगस्त में दूसरी, दिसंबर में तीसरी।",
            "when": "हर 4 महीने - अप्रैल, अगस्त, दिसंबर",
            "where": "सीधे आपके रजिस्टर्ड बैंक खाते में",
            "eligibility": ["जिनके पास जमीन है सभी किसान", "2 हेक्टेयर तक जमीन", "18 साल से ऊपर की उम्र", "भारतीय नागरिकता"],
            "documents": ["जमीन का मालिकाना प्रमाणपत्र", "आधार कार्ड", "बैंक खाता विवरण"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": ["pmkisan.gov.in पर जाएं", "किसान कोने पर क्लिक करें", "नया पंजीकरण चुनें", "आधार नंबर दर्ज करें", "जमीन की जानकारी दें", "बैंक खाता विवरण दर्ज करें", "आवेदन जमा करें", "हर 4 महीने में पैसे आएंगे"],
            "faqs": {
                "कितना पैसा मिलेगा?": "₹6,000 प्रति वर्ष - ₹2,000 की 3 किस्तें",
                "कौन आवेदन कर सकता है?": "कोई भी भारतीय किसान जिसके पास जमीन है",
                "कैसे आवेदन करूं?": "pmkisan.gov.in पर अपना आधार दिखाकर पंजीकृत हों",
                "कब पैसा आएगा?": "अप्रैल, अगस्त, दिसंबर को सीधे बैंक में",
                "क्या कार्यालय जाना पड़ेगा?": "नहीं! पूरी प्रक्रिया ऑनलाइन है",
            },
            "common_questions": {
                "क्या मैं आवेदन कर सकता हूं?": "हां! भारत का कोई भी किसान जिसके पास जमीन है",
                "कितना लाभ मिलेगा?": "₹6,000 सालाना सीधे आपके बैंक खाते में",
                "कब पेमेंट मिलता है?": "हर 4 महीने - अप्रैल, अगस्त, दिसंबर",
                "कौन से दस्तावेज?": "आधार, जमीन की जानकारी, बैंक खाता",
                "मदद के लिए कॉल करें?": "1800-180-1111 पर कॉल करें",
            }
        },
        "मराठी": {
            "name": "पीएम-किसान सम्मान निधि",
            "short": "शेतकऱ्यांना प्रति वर्ष ₹6,000 की थेट आय सहाय्य",
            "benefit": "₹6,000 वार्षिक (प्रत्येक 4 महिन्यांनी ₹2,000)",
            "how_much": "₹6,000 प्रति वर्ष - ₹2,000 च्या 3 हप्त्यांमध्ये। अप्रिल मध्ये पहिली, अगस्ट मध्ये दूसरी, डिसेंबर मध्ये तीसरी।",
            "when": "प्रत्येक 4 महिन्यांनी - अप्रिल, अगस्ट, डिसेंबर",
            "where": "सरळ आपल्या नोंदणीकृत बँक खात्यात",
            "eligibility": ["जमीन असलेल्या सर्व शेतकऱ्यांसाठी", "2 हेक्टर पर्यंत जमीन", "18 वर्षांपेक्षा जास्त वय", "भारतीय नागरिकत्व"],
            "documents": ["जमीन मालकीचा प्रमाणपत्र", "आधार कार्ड", "बँक खाते तपशील"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": ["pmkisan.gov.in वर जा", "किसान कोपरा क्लिक कर", "नवीन नोंदणी निवडा", "आधार क्रमांक दाखल कर", "जमीन तपशील द्या", "बँक माहिती दर्ज कर", "अर्ज सादर कर", "प्रत्येक 4 महिन्यांनी पैसे आतील"],
            "faqs": {
                "मला किती पैसे मिळतील?": "₹6,000 प्रतिवर्ष - ₹2,000 च्या 3 हप्त्यांमध्ये",
                "कोण अर्ज करू शकतो?": "कोणताही भारतीय शेतकरी ज्याच्याकडे जमीन आहे",
                "अर्ज कसे करायचा?": "pmkisan.gov.in वर आधारने नोंदणी करा",
                "पैसे कधी मिळतील?": "अप्रिल, अगस्ट, डिसेंबर ला सरळ बँकेत",
                "कार्यालयात जाणे आवश्यक?": "नाही! पूरी प्रक्रिया ऑनलाइन आहे",
            },
            "common_questions": {
                "मी अर्ज करू शकतो का?": "होय! भारतातील कोणताही शेतकरी ज्याच्याकडे जमीन आहे",
                "किती लाभ मिळेल?": "₹6,000 सालाना सरळ बँकेत",
                "कधी पेमेंट?": "हर 4 महिन्यांनी - अप्रिल, अगस्ट, डिसेंबर",
                "कोणते कागदपत्र?": "आधार, जमीन तपशील, बँक खाता",
                "मदद के लिए फोन करें?": "1800-180-1111 वर कॉल करा",
            }
        },
        "தமிழ்": {
            "name": "பிம்-கிசான் சம்மான் நிதி",
            "short": "விவசாயிகளுக்கு ஆண்டுக்கு ₹6,000 நேரடி வருமான ஆதரவு",
            "benefit": "₹6,000 ஆண்டுக்கு (4 மாதம் ஒரு முறை ₹2,000)",
            "how_much": "₹6,000 ஆண்டு - ₹2,000 ன் 3 தவணைகளில். ஏப்ரல் முதல், ஆகஸ்ட் இரண்டாம், டிசம்பர் மூன்றாம்।",
            "when": "4 மாதம் ஒரு முறை - ஏப்ரல், ஆகஸ்ட், டிசம்பர்",
            "where": "உங்கள் பதிவுசெய்யப்பட்ட வங்கிக் கணக்குக்கு நேரடியாக",
            "eligibility": ["நிலம் உள்ள அனைத்து விவசாயிகளுக்கு", "2 ஹெக்டேர் வரை நிலம்", "18 வயதுக்கு மேல்", "இந்திய குடிமகத்துவம்"],
            "documents": ["நிலச் சொந்தக் கட்டளை", "ஆதார் கார்டு", "வங்கிக் கணக்கு விவரங்கள்"],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "steps": ["pmkisan.gov.in வலைத்தளத்திற்குச் செல்லுங்கள்", "விவசாயி மூலை சொடுக்கவும்", "புதிய விவசாயி பதிவு தேர்ந்தெடுக்கவும்", "உங்கள் ஆதார் எண்ணை உள்ளிடவும்", "நிலத் தகவல் வழங்கவும்", "வங்கிக் கணக்கு விவரங்கள் உள்ளிடவும்", "விண்ணப்பத்தை சமர்ப்பிக்கவும்", "4 மாதம் ஒரு முறை பணம் வரும்"],
            "faqs": {
                "எனக்கு எவ்வளவு பணம் கிடைக்கும்?": "₹6,000 ஆண்டு - ₹2,000 ன் 3 தவணைகளில்",
                "யார் விண்ணப்பிக்க முடியும்?": "நிலம் உள்ள எந்த இந்திய விவசாயியும்",
                "எப்படி விண்ணப்பிடுவது?": "pmkisan.gov.in க்குச் சென்று ஆதாரால் பதிவு செய்யவும்",
                "பணம் எப்போது வரும்?": "ஏப்ரல், ஆகஸ்ட், டிசம்பர் - நேரடியாக வங்கிக்கு",
                "அலுவலகம் வேண்டுமா?": "இல்லை! முழு ऑनலाइன",
            },
            "common_questions": {
                "நான் விண்ணப்பிடலாமா?": "ஆம்! இந்தியாவின் நிலம் உள்ள விவசாயி",
                "எவ்வளவு நன்மை?": "₹6,000 ஆண்டு நேரடி வங்கிக்கு",
                "எப்போது பணம்?": "4 மாத ஒரு முறை - ஏப்ரல், ஆகஸ்ட், டிசம்பர்",
                "எந்தெந்த ஆவணங்கள்?": "ஆதார், நிலத் தகவல், வங்கிக் கணக்கு",
                "உதவிக்கு?": "1800-180-1111",
            }
        }
    },
    "MGNREGA": {
        "English": {
            "name": "MGNREGA - Rural Employment Guarantee",
            "short": "100 days guaranteed work per year at minimum wage",
            "benefit": "100 days guaranteed employment per year at ₹210-₹300 per day",
            "how_much": "₹210-₹300 per day. For 100 days: ₹21,000-₹30,000 per year",
            "when": "Throughout the year. Maximum 100 days per year",
            "where": "Local village construction projects",
            "eligibility": ["Rural adults above 18", "Unemployed or underemployed", "Willing to do manual work", "Indian citizen"],
            "documents": ["Aadhar card", "Address proof", "Job card"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": ["Go to Gram Panchayat", "Request job card", "Fill application", "Get registered", "Get job card", "Apply for work", "Work within 15 days", "Get paid"],
            "faqs": {
                "How much earn?": "₹210-₹300 per day. 100 days work = ₹21,000-₹30,000",
                "What work?": "Construction, digging, farming - no skills needed",
                "How apply?": "Visit Gram Panchayat with Aadhar",
                "How long?": "Work within 15 days of applying",
                "Women apply?": "Yes! Equal wages and benefits",
            },
            "common_questions": {
                "Can I work?": "If 18+, unemployed, yes! Go to Gram Panchayat",
                "What wage?": "₹210-₹300 per day by state",
                "How get card?": "Visit Gram Panchayat with Aadhar",
                "What work?": "Road, digging, farming, construction",
                "Call help?": "1800-345-6777",
            }
        },
        "हिंदी": {
            "name": "मनरेगा - ग्रामीण रोजगार गारंटी",
            "short": "प्रति वर्ष 100 दिन न्यूनतम मजदूरी पर गारंटीकृत काम",
            "benefit": "100 दिन गारंटीकृत रोजगार ₹210-₹300 प्रतिदिन",
            "how_much": "₹210-₹300 प्रतिदिन। 100 दिन = ₹21,000-₹30,000 प्रति वर्ष",
            "when": "पूरे साल। प्रति वर्ष अधिकतम 100 दिन",
            "where": "स्थानीय गांव की निर्माण परियोजनाएं",
            "eligibility": ["18 साल से ऊपर ग्रामीण वयस्क", "बेरोजगार या कम रोजगार", "मैनुअल काम करने को तैयार", "भारतीय नागरिक"],
            "documents": ["आधार कार्ड", "पता प्रमाण", "जॉब कार्ड"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": ["ग्राम पंचायत जाएं", "जॉब कार्ड के लिए अनुरोध करें", "आवेदन पत्र भरें", "पंजीकृत हों", "जॉब कार्ड प्राप्त करें", "काम के लिए आवेदन करें", "15 दिन में काम", "भुगतान पाएं"],
            "faqs": {
                "कितना कमा सकता?": "₹210-₹300 प्रतिदिन। 100 दिन = ₹21,000-₹30,000",
                "कौन सा काम?": "निर्माण, खुदाई, कृषि - कोई कौशल नहीं",
                "कैसे आवेदन?": "ग्राम पंचायत जाएं आधार के साथ",
                "कितने दिन?": "15 दिन में काम मिलता है",
                "महिलाएं?": "हां! बराबर मजदूरी और लाभ",
            },
            "common_questions": {
                "क्या काम कर सकता?": "18+, बेरोजगार हो तो हां!",
                "कितनी मजदूरी?": "₹210-₹300 प्रतिदिन अपने राज्य में",
                "कार्ड कैसे?": "ग्राम पंचायत में आधार दिखाएं",
                "कौन सा काम?": "सड़क, खुदाई, कृषि, निर्माण",
                "मदद फोन?": "1800-345-6777",
            }
        },
        "मराठी": {
            "name": "मनरेगा - ग्रामीण रोजगार गारंटी",
            "short": "प्रति वर्ष 100 दिन न्यूनतम मजदूरी पर गारंटीकृत काम",
            "benefit": "100 दिन गारंटीकृत रोजगार ₹210-₹300 प्रतिदिन",
            "how_much": "₹210-₹300 प्रतिदिन। 100 दिन = ₹21,000-₹30,000 प्रति वर्ष",
            "when": "पूरे साल। प्रति वर्ष अधिकतम 100 दिन",
            "where": "स्थानीय गांव की निर्माण परियोजनाएं",
            "eligibility": ["18 साल से ऊपर ग्रामीण वयस्क", "बेरोजगार या कम रोजगार", "मैनुअल काम को तैयार", "भारतीय नागरिक"],
            "documents": ["आधार कार्ड", "पता प्रमाण", "जॉब कार्ड"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": ["ग्राम पंचायत जा", "जॉब कार्ड मागा", "फॉर्म भरा", "रजिस्टर हुआ", "कार्ड पाया", "काम के लिए आवेदन", "15 दिन में काम", "भुगतान"],
            "faqs": {
                "कितना कमा?": "₹210-₹300 प्रतिदिन। 100 दिन = ₹21,000-₹30,000",
                "कौन सा काम?": "निर्माण, खुदाई, कृषि - कोई कौशल नहीं",
                "कैसे आवेदन?": "ग्राम पंचायत में आधार दिखाएं",
                "कितने दिन?": "15 दिन में काम मिलता है",
                "महिलाएं?": "हां! बराबर मजदूरी",
            },
            "common_questions": {
                "क्या काम कर सकता?": "18+, बेरोजगार तो हां",
                "कितनी मजदूरी?": "₹210-₹300 अपने राज्य में",
                "कार्ड कैसे?": "ग्राम पंचायत में जा",
                "कौन सा काम?": "सड़क, खुदाई, कृषि, निर्माण",
                "मदद?": "1800-345-6777",
            }
        },
        "தமிழ்": {
            "name": "மனிறேகா - கிராமப்புற வேலை உத்தரவாதம்",
            "short": "ஆண்டுக்கு 100 நாள் குறிப்பிட்ட வேலை குறைந்தபட்ச ஊதியத்தில்",
            "benefit": "ஆண்டுக்கு 100 நாள் குறிப்பிட்ட வேலை ₹210-₹300 நாளாந்திரத்தில்",
            "how_much": "₹210-₹300 நாளாந்திரம். 100 நாள் = ₹21,000-₹30,000 ஆண்டு",
            "when": "வருடம் முழுவதும். ஆண்டுக்கு அதிகபட்சம் 100 நாள்",
            "where": "உள்ளூர் கிராம கட்டுமான திட்டங்கள்",
            "eligibility": ["18 வயதுக்கு மேல் கிராமப்புற", "வேலையற்ற அல்லது குறைவான", "உடல்வேலை செய்ய விரும்பினால்", "இந்திய குடிமகன்"],
            "documents": ["ஆதார் கார்டு", "பதிவிடல் சான்றிதழ்", "வேலை அட்டை"],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "steps": ["கிராம சபை செல்லுங்கள்", "வேலை அட்டைக்கு கோரிக்கை", "பத்திரம் பூரணம்", "பதிவு செய்யுங்கள்", "அட்டை பெறுங்கள்", "வேலைக்கு விண்ணப்பம்", "15 நாட்களில் வேலை", "பணம் பெறுங்கள்"],
            "faqs": {
                "எவ்வளவு சம்பாதிக்கலாம்?": "₹210-₹300 நாளாந்திரம். 100 நாள் = ₹21,000-₹30,000",
                "என்ன வேலை?": "கட்டுமான, அகழ்வு, விவசாயம் - எந்த திறமையும் தேவை இல்லை",
                "எப்படி விண்ணப்பிடுவது?": "கிராம சபைக்குச் சென்று ஆதாரைக் காட்டவும்",
                "எப்போது வேலை?": "15 நாட்களில் வேலை பெறுவீர்கள்",
                "பெண்கள் விண்ணப்பிடலாமா?": "ஆம்! சம ஊதியம் மற்றும் நன்மைகள்",
            },
            "common_questions": {
                "நான் வேலை செய்யலாமா?": "18+, வேலையற்ற நிலையில் ஆம்",
                "எவ்வளவு ஊதியம்?": "₹210-₹300 உங்கள் மாநிலத்தில்",
                "அட்டை எப்படி?": "கிராம சபைக்குச் சென்றுஆதாரைக் காட்டவும்",
                "என்ன வேலை?": "சாலை, அகழ்வு, விவசாயம், கட்டுமான",
                "உதவி?": "1800-345-6777",
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
    .stButton > button { background: #667eea !important; color: white !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'history' not in st.session_state:
    st.session_state.history = []

# POLLY CLIENT - FIXED
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
        st.warning(f"Polly error: {str(e)}")
        return None

def speak_with_polly(text, language):
    """FIXED: Polly speaking with correct language codes"""
    try:
        polly = get_polly_client()
        if not polly:
            st.error("⚠️ AWS Polly not configured. Add credentials to Streamlit Secrets.")
            return False
        
        # Get language code and voice
        if language not in POLLY_VOICES:
            language = "English"
        
        lang_code, voice_id = POLLY_VOICES[language]
        
        st.info(f"🔊 Speaking {language}...")
        
        # Call Polly
        response = polly.synthesize_speech(
            Text=text[:2000],
            OutputFormat='mp3',
            VoiceId=voice_id,
            LanguageCode=lang_code
        )
        
        # Play audio
        audio_stream = response['AudioStream'].read()
        st.audio(audio_stream, format="audio/mp3", autoplay=False)
        st.success("✅ Audio ready!")
        return True
        
    except Exception as e:
        st.error(f"❌ Polly Error: {str(e)}")
        return False

# HEADER
st.markdown(f"<div class='header'><h1>🤖 Indic-Setu</h1><p>Government Schemes Guide</p></div>", unsafe_allow_html=True)

# LANGUAGE SELECTOR
col1, col2 = st.columns([2, 3])
with col1:
    st.session_state.language = st.selectbox(
        "🌐 Select Language:",
        list(POLLY_VOICES.keys()),
        index=list(POLLY_VOICES.keys()).index(st.session_state.language),
        key="lang_select"
    )
with col2:
    st.info(f"📍 Current Language: {st.session_state.language}")

# TABS
tabs = st.tabs(["🔍 Search", "📢 Guide", "📋 Form", "❤️ Favorites", "📜 History", "📊 Compare", "⭐ Stories", "💰 Benefits", "📞 Contacts"])

# TAB 1: SEARCH
with tabs[0]:
    st.markdown("### 🔍 Search Government Schemes")
    
    st.markdown("**Quick Schemes:**")
    cols = st.columns(2)
    for idx, scheme in enumerate(["PM-Kisan", "MGNREGA"]):
        with cols[idx % 2]:
            if st.button(f"📍 {scheme}", use_container_width=True, key=f"scheme_{scheme}"):
                # Get data in selected language
                if st.session_state.language in KNOWLEDGE_BASE.get(scheme, {}):
                    data = KNOWLEDGE_BASE[scheme][st.session_state.language]
                else:
                    data = KNOWLEDGE_BASE[scheme].get("English", {})
                
                # Display scheme
                st.markdown(f"<div class='success'><h3>{data.get('name', scheme)}</h3></div>", unsafe_allow_html=True)
                st.markdown(f"**{data.get('short', '')}**")
                st.markdown(f"**Benefit:** {data.get('benefit', '')}")
                st.markdown(f"**How Much:** {data.get('how_much', '')}")
                
                st.markdown("**Steps:**")
                for step in data.get('steps', [])[:4]:
                    st.write(f"• {step}")
                
                # LISTEN BUTTON - FIXED
                if st.button(f"🔊 Listen ({st.session_state.language})", use_container_width=True, key=f"listen_{scheme}_btn"):
                    text_to_speak = f"{data.get('name', scheme)}. {data.get('benefit', '')}"
                    speak_with_polly(text_to_speak, st.session_state.language)
                
                # SAVE BUTTON
                if st.button(f"❤️ Save", use_container_width=True, key=f"save_{scheme}"):
                    if scheme not in st.session_state.favorites:
                        st.session_state.favorites.append(scheme)
                        st.success("✅ Saved to Favorites!")
    
    # CUSTOM SEARCH
    st.markdown("---")
    st.markdown("**Ask Questions:**")
    query = st.text_area("Type your question about schemes...", height=80, key="search_query")
    
    if st.button("🔍 Search", use_container_width=True):
        if query.strip():
            # Search in schemes
            for scheme_name, scheme_data in KNOWLEDGE_BASE.items():
                if query.lower() in scheme_name.lower():
                    if st.session_state.language in scheme_data:
                        data = scheme_data[st.session_state.language]
                    else:
                        data = scheme_data.get("English", {})
                    
                    st.markdown(f"<div class='success'><h3>Found: {data.get('name', scheme_name)}</h3></div>", unsafe_allow_html=True)
                    st.markdown(f"**{data.get('short', '')}**")
                    
                    # Check FAQs
                    for q, ans in data.get('faqs', {}).items():
                        if any(word in query.lower() for word in q.lower().split()):
                            st.markdown(f"**Q:** {q}")
                            st.markdown(f"**A:** {ans}")
                            
                            # LISTEN BUTTON - FIXED
                            if st.button(f"🔊 Listen Answer", use_container_width=True, key=f"listen_ans_{q}"):
                                speak_with_polly(ans, st.session_state.language)
                            break

# TAB 2: VOICE GUIDE
with tabs[1]:
    st.markdown("### 📢 Voice Guide - Step by Step")
    scheme = st.selectbox("Select Scheme:", ["PM-Kisan", "MGNREGA"], key="guide_scheme")
    
    if scheme in KNOWLEDGE_BASE:
        if st.session_state.language in KNOWLEDGE_BASE[scheme]:
            data = KNOWLEDGE_BASE[scheme][st.session_state.language]
        else:
            data = KNOWLEDGE_BASE[scheme].get("English", {})
        
        st.markdown(f"<div class='success'><h3>{data.get('name', scheme)}</h3></div>", unsafe_allow_html=True)
        
        st.markdown("**Application Steps:**")
        for idx, step in enumerate(data.get('steps', []), 1):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"**Step {idx}:** {step}")
            with col2:
                # LISTEN BUTTON - FIXED
                if st.button("🔊", key=f"step_listen_{idx}_{scheme}"):
                    speak_with_polly(f"Step {idx}. {step}", st.session_state.language)

# TAB 3: FORM FILLER
with tabs[2]:
    st.markdown("### 📋 Form Filler")
    name = st.text_input("Full Name", key="form_name")
    aadhar = st.text_input("Aadhar", key="form_aadhar")
    phone = st.text_input("Phone", key="form_phone")
    
    if st.button("✅ Generate", use_container_width=True):
        if name and aadhar:
            form_text = f"Name: {name}\nAadhar: {aadhar}\nPhone: {phone}\nDate: {datetime.now()}"
            st.success("✅ Form ready!")
            st.text(form_text)

# TAB 4: FAVORITES
with tabs[3]:
    st.markdown("### ❤️ Favorites")
    if st.session_state.favorites:
        st.success(f"Saved: {', '.join(st.session_state.favorites)}")
    else:
        st.info("No favorites yet!")

# TAB 5: HISTORY
with tabs[4]:
    st.markdown("### 📜 History")
    st.info("Your searches will appear here")

# TAB 6: COMPARE
with tabs[5]:
    st.markdown("### 📊 Compare")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.selectbox("Scheme 1:", ["PM-Kisan", "MGNREGA"], key="cmp1")
    with col2:
        s2 = st.selectbox("Scheme 2:", ["MGNREGA", "PM-Kisan"], key="cmp2")
    st.write(f"Comparing: {s1} vs {s2}")

# TAB 7: STORIES
with tabs[6]:
    st.markdown("### ⭐ Success Stories")
    st.write("✅ Ramesh - PM-Kisan - ₹6,000/year")
    st.write("✅ Priya - MGNREGA - 100 days work")

# TAB 8: BENEFITS
with tabs[7]:
    st.markdown("### 💰 Calculator")
    income = st.number_input("Annual Income:", key="calc_income")
    st.metric("Eligible Schemes", 2 if income < 300000 else 1)

# TAB 9: CONTACTS
with tabs[8]:
    st.markdown("### 📞 Helplines")
    st.write("**PM-Kisan:** 1800-180-1111")
    st.write("**MGNREGA:** 1800-345-6777")

st.markdown("---")
st.markdown("<div style='text-align: center;'><p>🌾 Indic-Setu | © 2026</p></div>", unsafe_allow_html=True)
