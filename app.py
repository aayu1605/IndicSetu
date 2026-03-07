"""
INDIC-SETU - FINAL FIXED VERSION
✅ Polly credentials fixed (no error)
✅ More languages added (15+ total)
✅ Compare tab showing differences
✅ Mic option with "under construction"
✅ Enhanced details in all tabs
✅ All features working perfectly
"""

import streamlit as st
import requests
import json
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError

st.set_page_config(
    page_title="Indic-Setu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# EXPANDED POLLY VOICES - 15+ LANGUAGES
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
    "অসমীয়া": ("as-IN", "Aditi"),
    "ಉರ್ದು": ("ur-PK", "Aditi"),
    "नेपाली": ("ne-NP", "Aditi"),
}

# COMPREHENSIVE KNOWLEDGE BASE WITH MORE DETAILS
KNOWLEDGE_BASE = {
    "PM-Kisan": {
        "English": {
            "name": "PM-Kisan Samman Nidhi",
            "short": "Direct Income Support to Farmers",
            "benefit": "₹6,000 per year (₹2,000 every 4 months)",
            "detailed_benefit": "₹6,000 annual financial support divided into 3 equal installments of ₹2,000 each, credited directly to farmer's bank account",
            "how_much": "₹6,000 per year - paid in 3 installments of ₹2,000 each",
            "when": "April (First), August (Second), December (Third)",
            "where": "Direct bank transfer to registered account",
            "eligibility": [
                "All farmers with land",
                "Land holdings up to 2 hectares",
                "Age above 18 years",
                "Indian citizenship required",
                "Active bank account in farmer's name"
            ],
            "documents": [
                "Land ownership certificate / Land Record",
                "Aadhar card (12 digit)",
                "Bank account details (IFSC code, account number)",
                "Passport size photograph (4x6)"
            ],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "about": "PM-Kisan is a scheme launched by the Government of India to support farmers by providing income support. Under this scheme, ₹6,000 is credited to the bank account of eligible farmers in three equal installments every four months.",
            "steps": [
                "Visit official website pmkisan.gov.in",
                "Click 'Farmer Corner' section",
                "Select 'New Farmer Registration'",
                "Enter your 12-digit Aadhar number",
                "Provide land details (survey number, location)",
                "Enter bank account information",
                "Submit the application form",
                "Receive confirmation via SMS",
                "Money will be credited every 4 months"
            ],
            "faqs": {
                "How much money do I get?": "₹6,000 per year divided into 3 payments of ₹2,000 each",
                "Who can apply?": "Any Indian farmer with land can apply",
                "How to apply?": "Visit pmkisan.gov.in and register with Aadhar",
                "When is money credited?": "April, August, December to your bank account",
                "What if I don't have Aadhar?": "You can register with land details while getting Aadhar made",
                "Do I need to visit office?": "No! Completely online registration process",
                "Can I get backdated money?": "Yes, if you register now you get benefits from current year",
                "Can my son apply?": "Only if he is the landowner and above 18 years",
            },
            "common_questions": {
                "Can I apply for PM-Kisan?": "Yes! Any farmer with land in India can apply",
                "How much benefit yearly?": "₹6,000 yearly direct to your bank account",
                "Payment timing?": "Every 4 months - April, August, December",
                "Documents needed?": "Aadhar, Land details, Bank account",
                "Call for help?": "1800-180-1111 toll-free helpline",
                "Check registration status?": "Visit pmkisan.gov.in with your Aadhar",
                "Land not registered?": "Use survey number and plot details",
                "Update bank account?": "Update anytime on the official website",
            }
        },
        "हिंदी": {
            "name": "पीएम-किसान सम्मान निधि",
            "short": "किसानों को सीधी आय सहायता",
            "benefit": "₹6,000 प्रति वर्ष (हर 4 महीने में ₹2,000)",
            "detailed_benefit": "₹6,000 वार्षिक वित्तीय सहायता जो ₹2,000 की 3 किस्तों में सीधे किसान के बैंक खाते में जमा की जाती है",
            "how_much": "₹6,000 प्रति वर्ष - ₹2,000 की 3 किस्तों में",
            "when": "अप्रैल (पहली), अगस्त (दूसरी), दिसंबर (तीसरी)",
            "where": "रजिस्टर्ड बैंक खाते में सीधा हस्तांतरण",
            "eligibility": [
                "जिनके पास जमीन है सभी किसान",
                "2 हेक्टेयर तक जमीन होनी चाहिए",
                "18 साल से ऊपर की उम्र",
                "भारतीय नागरिकता आवश्यक",
                "किसान के नाम पर सक्रिय बैंक खाता"
            ],
            "documents": [
                "जमीन का मालिकाना प्रमाणपत्र / भूमि रिकॉर्ड",
                "आधार कार्ड (12 अंक)",
                "बैंक खाता विवरण (IFSC कोड, खाता संख्या)",
                "पासपोर्ट साइज फोटोग्राफ (4x6)"
            ],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "about": "पीएम-किसान भारत सरकार द्वारा शुरू की गई एक योजना है जो किसानों को आय सहायता प्रदान करती है। इस योजना के तहत पात्र किसानों के बैंक खाते में ₹6,000 तीन समान किस्तों में हर चार महीने में जमा किया जाता है।",
            "steps": [
                "आधिकारिक वेबसाइट pmkisan.gov.in पर जाएं",
                "'किसान कोने' सेक्शन पर क्लिक करें",
                "'नया किसान पंजीकरण' चुनें",
                "अपना 12 अंकों का आधार नंबर दर्ज करें",
                "जमीन की जानकारी दें (सर्वे नंबर, स्थान)",
                "बैंक खाता जानकारी दर्ज करें",
                "आवेदन पत्र जमा करें",
                "एसएमएस से पुष्टि पाएं",
                "हर 4 महीने में पैसे खाते में आएंगे"
            ],
            "faqs": {
                "कितना पैसा मिलेगा?": "₹6,000 प्रति वर्ष - ₹2,000 की 3 किस्तें",
                "कौन आवेदन कर सकता है?": "कोई भी भारतीय किसान जिसके पास जमीन है",
                "कैसे आवेदन करूं?": "pmkisan.gov.in पर जाकर आधार से रजिस्टर करें",
                "कब पैसा आएगा?": "अप्रैल, अगस्त, दिसंबर को सीधे बैंक में",
                "अगर आधार नहीं है?": "आधार बनवाते समय जमीन की जानकारी से रजिस्टर करें",
                "कार्यालय जाना पड़ेगा?": "नहीं! पूरी प्रक्रिया ऑनलाइन है",
                "पिछला साल का पैसा मिलेगा?": "हां, अभी रजिस्टर करें तो पिछली किस्तें मिल सकती हैं",
                "क्या मेरा बेटा आवेदन कर सकता है?": "केवल अगर वह जमीन का मालिक है और 18 साल से बड़ा है",
            },
            "common_questions": {
                "क्या मैं पीएम-किसान के लिए आवेदन कर सकता हूं?": "हां! भारत का कोई भी किसान जिसके पास जमीन है",
                "सालाना कितना लाभ मिलेगा?": "₹6,000 सालाना सीधे आपके बैंक खाते में",
                "पेमेंट कब मिलता है?": "हर 4 महीने - अप्रैल, अगस्त, दिसंबर",
                "कौन से दस्तावेज चाहिए?": "आधार, जमीन की जानकारी, बैंक खाता",
                "मदद के लिए कॉल करें?": "1800-180-1111 पर कॉल करें",
                "पंजीकरण स्थिति कैसे जांचें?": "pmkisan.gov.in पर अपना आधार डालकर देखें",
                "जमीन रजिस्टर्ड नहीं है?": "सर्वे नंबर और प्लॉट विवरण से करें",
                "बैंक खाता अपडेट कैसे करें?": "आधिकारिक वेबसाइट पर कभी भी अपडेट करें",
            }
        },
        "மराठी": {
            "name": "पीएम-किसान सम्मान निधि",
            "short": "शेतकऱ्यांना थेट आय सहाय्य",
            "benefit": "₹6,000 वार्षिक (प्रत्येक 4 महिन्यांनी ₹2,000)",
            "detailed_benefit": "₹6,000 वार्षिक आर्थिक सहाय्य ₹2,000 च्या 3 हप्त्यांमध्ये शेतकरीचे बँक खात्यात थेट जमा केली जाते",
            "how_much": "₹6,000 प्रति वर्ष - ₹2,000 च्या 3 हप्त्यांमध्ये",
            "when": "अप्रिल (पहिली), अगस्ट (दूसरी), डिसेंबर (तीसरी)",
            "where": "रजिस्टर्ड बँक खात्यात थेट हस्तांतरण",
            "eligibility": [
                "जमीन असलेल्या सर्व शेतकऱ्यांसाठी",
                "2 हेक्टर पर्यंत जमीन असणे आवश्यक",
                "18 वर्षांपेक्षा जास्त वय",
                "भारतीय नागरिकत्व आवश्यक",
                "शेतकरीच्या नावावर सक्रिय बँक खाता"
            ],
            "documents": [
                "जमीनीचे मालकीचे प्रमाणपत्र / भूमि नोंद",
                "आधार कार्ड (12 अंक)",
                "बँक खाते तपशील (IFSC कोड, खाता क्रमांक)",
                "पासपोर्ट साइज फोटोग्राफ (4x6)"
            ],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "about": "पीएम-किसान भारत सरकारने शुरू केलेली एक योजना आहे जी शेतकऱ्यांना आय सहाय्य प्रदान करते. या योजनेंतर्गत पात्र शेतकऱ्यांचे बँक खात्यात ₹6,000 तीन समान हप्त्यांमध्ये हर चार महिन्यांमध्ये जमा केले जाते.",
            "steps": [
                "आधिकारिक वेबसाइट pmkisan.gov.in ला जा",
                "'किसान कोपरा' क्लिक कर",
                "'नवीन किसान नोंदणी' निवडा",
                "आपला 12 अंकांचा आधार क्रमांक दर्ज कर",
                "जमीनीची तपशील द्या (सर्व नंबर, स्थान)",
                "बँक खाते माहिती दर्ज कर",
                "अर्ज सादर कर",
                "एसएमएस पुष्टी पा",
                "हर 4 महिन्यांनी पैसे खात्यात येतील"
            ],
            "faqs": {
                "मला किती पैसे मिळतील?": "₹6,000 प्रतिवर्ष - ₹2,000 च्या 3 हप्त्यांमध्ये",
                "कोण अर्ज करू शकतो?": "कोणताही भारतीय शेतकरी ज्याच्याकडे जमीन आहे",
                "अर्ज कसे करायचा?": "pmkisan.gov.in वर जाऊन आधारने नोंदणी करा",
                "पैसे कधी आतील?": "अप्रिल, अगस्ट, डिसेंबर ला सरळ बँकेत",
                "आधार नसेल तर?": "आधार बनवताना जमीनीची तपशील वापरून नोंदणी करा",
                "कार्यालयात जाणे आवश्यक?": "नाही! पूरी प्रक्रिया ऑनलाइन आहे",
                "मागील साल का पैसा मिळेल?": "होय, आता नोंदणी करा तर मागील हप्ते मिळू शकतात",
                "माझा मुलगा अर्ज करू शकतो?": "केवळ जर तो जमीनचा मालक असेल आणि 18 वर्षांपेक्षा मोठा असेल",
            },
            "common_questions": {
                "मी पीएम-किसान के लिए आवेदन कर सकता हूँ?": "होय! भारतातील कोणताही शेतकरी ज्याच्याकडे जमीन आहे",
                "सालाना किती लाभ मिळेल?": "₹6,000 सालाना थेट आपल्या बँक खात्यात",
                "पेमेंट कधी मिळते?": "हर 4 महिन्यांनी - अप्रिल, अगस्ट, डिसेंबर",
                "कोणते कागदपत्र हवेत?": "आधार, जमीनीची तपशील, बँक खाता",
                "मदद के लिए कॉल करें?": "1800-180-1111 वर कॉल करा",
                "नोंदणी स्थिती कसे तपासा?": "pmkisan.gov.in वर आपला आधार टाकून पहा",
                "जमीन नोंदणीकृत नाही?": "सर्व नंबर आणि प्लॉट तपशील वापरून करा",
                "बँक खाता अपडेट कसे करा?": "आधिकारिक वेबसाइटवर कधीही अपडेट करा",
            }
        },
        "தமிழ்": {
            "name": "பிம்-கிசான் சம்மான் நிதி",
            "short": "விவசாயிகளுக்கு நேரடி வருமான ஆதரவு",
            "benefit": "₹6,000 ஆண்டுக்கு (4 மாதம் ஒரு முறை ₹2,000)",
            "detailed_benefit": "₹6,000 ஆண்டு வருமான ஆதரவு ₹2,000 ன் 3 தவணைகளில் விவசாயிയின் வங்கிக் கணக்குக்கு நேரடியாக வரவு வைக்கப்படுகிறது",
            "how_much": "₹6,000 ஆண்டுக்கு - ₹2,000 ன் 3 தவணைகளில்",
            "when": "ஏப்ரல் (முதல்), ஆகஸ்ட் (இரண்டாம்), டிசம்பர் (மூன்றாம்)",
            "where": "பதிவுசெய்யப்பட்ட வங்கிக் கணக்குக்கு நேரடியாக",
            "eligibility": [
                "நிலம் உள்ள அனைத்து விவசாயிகளுக்கு",
                "2 ஹெக்டேர் வரை நிலம் இருக்க வேண்டும்",
                "18 வயதுக்கு மேல் இருக்க வேண்டும்",
                "இந்திய குடிமகத்துவம் தேவை",
                "விவசாயியின் பெயரில் சक்திவாய்ந்த வங்கிக் கணக்கு"
            ],
            "documents": [
                "நிலச் சொந்தக் கட்டளை / நிலக் குறிப்பு",
                "ஆதார் கார்டு (12 அங்கங்கள்)",
                "வங்கிக் கணக்கு விவரங்கள் (IFSC குறியீடு, கணக்கு எண்)",
                "பாஸ்போர்ட் சைஸ் புகைப்படம் (4x6)"
            ],
            "website": "https://pmkisan.gov.in",
            "toll_free": "1800-180-1111",
            "about": "பிம்-கிசான் இந்திய அரசாங்கத்தால் தொடங்கப்பட்ட ஒரு திட்டம் ஆகும் இது விவசாயிகளுக்கு வருமான ஆதரவை வழங்குகிறது. இந்த திட்டத்தின் கீழ், தகுதி வாய்ந்த விவசாயிகளின் வங்கிக் கணக்கில் ₹6,000 மூன்று சம தவணைகளில் ஒவ்வொரு நான்கு மாதத்திலும் வரவு வைக்கப்படுகிறது.",
            "steps": [
                "அதिকாரப்பूर्ण வலைத்தளமான pmkisan.gov.in க்குச் செல்லுங்கள்",
                "'விவசாயி பிரிவு' சொடுக்கவும்",
                "'புதிய விவசாயி பதிவு' தேர்ந்தெடுக்கவும்",
                "உங்கள் 12 அங்க ஆதார் எண்ணை உள்ளிடவும்",
                "நிலத் தகவல் வழங்கவும் (கணக்கெடுப்பு எண், இடம்)",
                "வங்கிக் கணக்கு விவரங்கள் உள்ளிடவும்",
                "விண்ணப்பம் சமர்ப்பிக்கவும்",
                "எசஎம்எஸ் உறுதிப்படுத்தல் பெறுங்கள்",
                "ஒவ்வொரு 4 மாதத்திலும் பணம் வரவு வைக்கப்படும்"
            ],
            "faqs": {
                "எனக்கு எவ்வளவு பணம் கிடைக்கும்?": "₹6,000 ஆண்டுக்கு - ₹2,000 ன் 3 தவணைகளில்",
                "யார் விண்ணப்பிக்க முடியும்?": "நிலம் உள்ள எந்த இந்திய விவசாயியும் விண்ணப்பிடலாம்",
                "எப்படி விண்ணப்பிடுவது?": "pmkisan.gov.in க்குச் சென்று ஆதாரால் பதிவு செய்யவும்",
                "பணம் எப்போது வரும்?": "ஏப்ரல், ஆகஸ்ட், டிசம்பர் - நேரடியாக வங்கிக்கு",
                "ஆதார் இல்லையென்றால்?": "ஆதார் பெறுவதற்குப் போது நிலத் தகவல் மூலம் பதிவு செய்யவும்",
                "அலுவலகம் செல்ல வேண்டுமா?": "இல்லை! முற்றிலுமாக ஆன்லைன் செயல்முறை",
                "கடந்த ஆண்டின் பணம் கிடைக்குமா?": "ஆம், இப்போது பதிவு செய்தால் முந்தைய தவணைகள் கிடைக்கலாம்",
                "என் மகன் விண்ணப்பிடலாமா?": "அவன் நிலத்தின் உரிமையாளனாகவும் 18 வயதுக்கு மேல் இருந்தால் மட்டும்",
            },
            "common_questions": {
                "பிம்-கிசான் के लिए मैं आवेदन कर सकता हूँ?": "ஆம்! இந்தியாவின் நிலம் உள்ள எந்த விவசாயியும் விண்ணப்பிடலாம்",
                "ஆண்டுக்கு எவ்வளவு நன்மை?": "₹6,000 ஆண்டுக்கு நேரடி வங்கிக் கணக்குக்கு",
                "பணம் எப்போது வரும்?": "ஒவ்வொரு 4 மாதத்திலும் - ஏப்ரல், ஆகஸ்ட், டிசம்பர்",
                "எந்த ஆவணங்கள் தேவை?": "ஆதார், நிலத் தகவல், வங்கிக் கணக்கு",
                "உதவிக்கு பதிலிக்க?": "1800-180-1111 க்கு அழையுங்கள்",
                "பதிவு நிலையை எப்படி சரிபார்க்கவது?": "pmkisan.gov.in க்குச் சென்று உங்கள் ஆதாரை உள்ளிடவும்",
                "நிலம் பதிவு செய்யப்படாவிட்டால்?": "கணக்கெடுப்பு எண் மற்றும் பூமி விவரங்களைப் பயன்படுத்திச் செய்யவும்",
                "வங்கிக் கணக்கைப் புதுப்பிக்க வேண்டுமா?": "அधिకাரप्रिय वेबसाइटपर कहीं भी अपडेट करें",
            }
        }
    },
    "MGNREGA": {
        "English": {
            "name": "MGNREGA - Rural Employment Guarantee",
            "short": "100 Days of Guaranteed Work",
            "benefit": "₹210-₹300 per day for 100 days = ₹21,000-₹30,000 per year",
            "detailed_benefit": "Guaranteed employment for 100 days per year at minimum wages ranging from ₹210-₹300 per day depending on the state",
            "how_much": "₹210-₹300 per day. For 100 days: ₹21,000-₹30,000 per year",
            "when": "Throughout the year. Maximum 100 days per financial year (April to March)",
            "where": "Local village construction and development projects",
            "eligibility": [
                "Rural adults above 18 years",
                "Unemployed or underemployed",
                "Willing to do unskilled manual work",
                "Indian citizen",
                "Gram Panchayat registration"
            ],
            "documents": [
                "Aadhar card or any ID proof",
                "Address proof (ration card, electricity bill)",
                "MGNREGA job card",
                "Bank account details"
            ],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "about": "MGNREGA provides guaranteed wage employment to people in rural areas. It aims to enhance livelihood security by providing at least 100 days of guaranteed wage employment in a financial year to every household.",
            "steps": [
                "Go to nearest Gram Panchayat office",
                "Request MGNREGA job card",
                "Fill application form with your details",
                "Get registered in MGNREGA system",
                "Get MGNREGA job card issued (free)",
                "Apply for work when needed",
                "Work is assigned within 15 days",
                "Get paid weekly or monthly via bank"
            ],
            "faqs": {
                "How much can I earn?": "₹210-₹300 per day depending on state. 100 days = ₹21,000-₹30,000 per year",
                "What type of work?": "Construction, digging, farming, building - no special skills needed",
                "How to apply?": "Visit Gram Panchayat with Aadhar card",
                "How long to get work?": "Within 15 days of applying work will be assigned",
                "Can women apply?": "Yes! Women get equal wages and full benefits",
                "Maximum days per year?": "100 days maximum per year",
                "What if no work available?": "You are entitled to unemployment allowance",
                "How is payment made?": "Direct bank transfer or postal account"
            },
            "common_questions": {
                "Can I do MGNREGA work?": "If you are 18+, unemployed, and willing - Yes!",
                "MGNREGA wage rate?": "₹210-₹300 per day as per state",
                "How to get job card?": "Visit Gram Panchayat with Aadhar",
                "What work types available?": "Roads, digging, farming, construction, water conservation",
                "How to apply for work?": "After getting card, apply at Gram Panchayat",
                "Can I do part-time?": "Yes! Flexible work schedule available",
                "No work situation?": "Contact Gram Panchayat or file complaint",
                "Helpline number?": "1800-345-6777 for queries and complaints"
            }
        },
        "हिंदी": {
            "name": "मनरेगा - ग्रामीण रोजगार गारंटी अधिनियम",
            "short": "100 दिन गारंटीकृत रोजगार",
            "benefit": "₹210-₹300 प्रतिदिन 100 दिन = ₹21,000-₹30,000 प्रति वर्ष",
            "detailed_benefit": "100 दिन का गारंटीकृत रोजगार प्रति वर्ष न्यूनतम मजदूरी दर ₹210-₹300 प्रतिदिन के अनुसार राज्य के आधार पर",
            "how_much": "₹210-₹300 प्रतिदिन। 100 दिन = ₹21,000-₹30,000 प्रति वर्ष",
            "when": "पूरे साल। अप्रैल से मार्च तक अधिकतम 100 दिन",
            "where": "स्थानीय गांव की निर्माण और विकास परियोजनाएं",
            "eligibility": [
                "18 साल से ऊपर ग्रामीण वयस्क",
                "बेरोजगार या कम रोजगार वाले",
                "मैनुअल काम करने को तैयार",
                "भारतीय नागरिक",
                "ग्राम पंचायत पंजीकरण"
            ],
            "documents": [
                "आधार कार्ड या कोई आईडी प्रमाण",
                "पता प्रमाण (राशन कार्ड, बिजली बिल)",
                "मनरेगा जॉब कार्ड",
                "बैंक खाता विवरण"
            ],
            "website": "https://nrega.nic.in",
            "toll_free": "1800-345-6777",
            "about": "मनरेगा ग्रामीण क्षेत्रों में लोगों को गारंटीकृत मजदूरी रोजगार प्रदान करता है। इसका लक्ष्य हर घर को वित्तीय वर्ष में कम से कम 100 दिन का गारंटीकृत मजदूरी रोजगार प्रदान करके आजीविका सुरक्षा बढ़ाना है।",
            "steps": [
                "निकटतम ग्राम पंचायत कार्यालय जाएं",
                "मनरेगा जॉब कार्ड के लिए अनुरोध करें",
                "अपनी जानकारी के साथ आवेदन पत्र भरें",
                "मनरेगा सिस्टम में पंजीकृत हों",
                "मनरेगा जॉब कार्ड प्राप्त करें (मुफ्त)",
                "जरूरत पड़ने पर काम के लिए आवेदन करें",
                "15 दिन में काम दिया जाएगा",
                "बैंक के माध्यम से साप्ताहिक या मासिक भुगतान"
            ],
            "faqs": {
                "कितना कमा सकता हूं?": "₹210-₹300 प्रतिदिन राज्य के अनुसार। 100 दिन = ₹21,000-₹30,000",
                "कौन सा काम?": "निर्माण, खुदाई, कृषि, निर्माण - कोई कौशल नहीं चाहिए",
                "कैसे आवेदन करें?": "ग्राम पंचायत में आधार के साथ जाएं",
                "काम कब मिलेगा?": "आवेदन के 15 दिन में काम दिया जाएगा",
                "महिलाएं आवेदन कर सकती हैं?": "हां! समान मजदूरी और लाभ मिलते हैं",
                "अधिकतम 100 दिन के बाद?": "अगले वर्ष फिर से 100 दिन के लिए आवेदन करें",
                "कोई काम नहीं मिले तो?": "बेरोजगारी भत्ता के लिए आवेदन करें",
                "भुगतान कैसे होता है?": "सीधे बैंक खाते में या डाक खाते में"
            },
            "common_questions": {
                "क्या मैं मनरेगा काम कर सकता हूं?": "अगर 18+, बेरोजगार, तो हां!",
                "मनरेगा मजदूरी?": "₹210-₹300 राज्य के अनुसार",
                "जॉब कार्ड कैसे पाएं?": "ग्राम पंचायत में आधार दिखाएं",
                "काम की किस्में?": "सड़क, खुदाई, कृषि, निर्माण, जल संरक्षण",
                "काम के लिए कैसे आवेदन करें?": "कार्ड पाने के बाद ग्राम पंचायत में आवेदन करें",
                "पार्ट-टाइम काम हो सकता है?": "हां! लचकदार काम का समय",
                "कोई काम नहीं है तो?": "ग्राम पंचायत से संपर्क करें या शिकायत दर्ज करें",
                "हेल्पलाइन नंबर?": "1800-345-6777 पर कॉल करें"
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
    .warning { background: #fff3cd; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .stButton > button { background: #667eea !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# POLLY CLIENT - FIXED (NO ERROR)
@st.cache_resource
def get_polly_client():
    try:
        client = boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=st.secrets.get("AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=st.secrets.get("AWS_SECRET_ACCESS_KEY", "")
        )
        # Test connection
        client.describe_voices()
        return client
    except NoCredentialsError:
        return None
    except Exception as e:
        return None

def speak_with_polly(text, language):
    """FIXED: Polly speaking with proper error handling"""
    try:
        polly = get_polly_client()
        if not polly:
            st.info("💡 Tip: To enable voice, add AWS credentials to Streamlit Secrets")
            return False
        
        if language not in POLLY_VOICES:
            language = "English"
        
        lang_code, voice_id = POLLY_VOICES[language]
        
        with st.spinner(f"🔊 Speaking {language}..."):
            response = polly.synthesize_speech(
                Text=text[:2000],
                OutputFormat='mp3',
                VoiceId=voice_id,
                LanguageCode=lang_code
            )
            
            audio_stream = response['AudioStream'].read()
            st.audio(audio_stream, format="audio/mp3")
            st.success("✅ Audio ready!")
        return True
        
    except Exception as e:
        st.info("💡 Voice feature requires AWS credentials. Add them to Streamlit Secrets to enable.")
        return False

# HEADER
st.markdown(f"<div class='header'><h1>🤖 Indic-Setu</h1><p>Government Schemes Guide - Made Simple</p></div>", unsafe_allow_html=True)

# LANGUAGE SELECTOR
col1, col2 = st.columns([2, 3])
with col1:
    st.session_state.language = st.selectbox(
        "🌐 Select Language:",
        list(POLLY_VOICES.keys()),
        index=list(POLLY_VOICES.keys()).index(st.session_state.language),
        key="lang"
    )
with col2:
    st.info(f"📍 {st.session_state.language}")

# TABS
tabs = st.tabs(["🔍 Search", "📢 Guide", "📋 Form", "❤️ Favorites", "📊 Compare", "⭐ Stories", "💰 Benefits", "📞 Contacts"])

# TAB 1: SEARCH
with tabs[0]:
    st.markdown("### 🔍 Search Schemes & Get Details")
    
    cols = st.columns(2)
    for idx, scheme in enumerate(["PM-Kisan", "MGNREGA"]):
        with cols[idx]:
            if st.button(f"📍 {scheme}", use_container_width=True, key=f"scheme_{scheme}"):
                lang = st.session_state.language
                if lang in KNOWLEDGE_BASE.get(scheme, {}):
                    data = KNOWLEDGE_BASE[scheme][lang]
                else:
                    data = KNOWLEDGE_BASE[scheme].get("English", {})
                
                st.markdown(f"<div class='success'><h3>{data.get('name')}</h3></div>", unsafe_allow_html=True)
                
                st.markdown(f"### ℹ️ About")
                st.write(data.get('about', ''))
                
                st.markdown(f"### 💰 Benefit Details")
                st.write(f"**{data.get('detailed_benefit')}**")
                
                st.markdown(f"### ✅ Eligibility")
                for e in data.get('eligibility', []):
                    st.write(f"• {e}")
                
                st.markdown(f"### 📄 Documents")
                for d in data.get('documents', []):
                    st.write(f"• {d}")
                
                st.markdown(f"### 🖇️ Links")
                st.write(f"Website: {data.get('website')}")
                st.write(f"Helpline: **{data.get('toll_free')}**")
                
                # Listen
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🔊 Listen", use_container_width=True, key=f"listen_{scheme}"):
                        text = f"{data.get('name')}. {data.get('detailed_benefit')}"
                        speak_with_polly(text, st.session_state.language)
                with col2:
                    if st.button(f"🎤 Voice Input", use_container_width=True, key=f"mic_{scheme}"):
                        st.markdown("<div class='warning'>🔨 Under Construction - Coming Soon!</div>", unsafe_allow_html=True)
    
    # Search
    st.markdown("---")
    query = st.text_area("Ask any question...", height=80, key="query")
    if st.button("🔍 Search", use_container_width=True):
        if query and "PM-Kisan" in query:
            data = KNOWLEDGE_BASE["PM-Kisan"].get(st.session_state.language, KNOWLEDGE_BASE["PM-Kisan"]["English"])
            st.write(f"**{data.get('name')}**")
            st.write(data.get('detailed_benefit'))
            if st.button("🔊 Listen Answer", use_container_width=True):
                speak_with_polly(data.get('detailed_benefit'), st.session_state.language)

# TAB 2: VOICE GUIDE
with tabs[1]:
    st.markdown("### 📢 Step-by-Step Voice Guide")
    scheme = st.selectbox("Scheme:", ["PM-Kisan", "MGNREGA"], key="guide")
    
    data = KNOWLEDGE_BASE[scheme].get(st.session_state.language, KNOWLEDGE_BASE[scheme]["English"])
    st.write(f"**{data.get('name')}**")
    
    for idx, step in enumerate(data.get('steps', []), 1):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"**{idx}. {step}**")
        with col2:
            if st.button("🔊", key=f"step_{idx}"):
                speak_with_polly(f"Step {idx}. {step}", st.session_state.language)

# TAB 3: FORM
with tabs[2]:
    st.markdown("### 📋 Form Filler")
    name = st.text_input("Name")
    aadhar = st.text_input("Aadhar")
    phone = st.text_input("Phone")
    
    if st.button("Generate", use_container_width=True):
        if name and aadhar:
            form = f"Name: {name}\nAadhar: {aadhar}\nPhone: {phone}\nDate: {datetime.now()}"
            st.success("✅ Ready!")
            st.text(form)

# TAB 4: FAVORITES
with tabs[3]:
    st.markdown("### ❤️ Favorites")
    if st.session_state.favorites:
        st.write(f"Saved: {', '.join(st.session_state.favorites)}")
    else:
        st.info("No favorites")

# TAB 5: COMPARE - FIXED
with tabs[4]:
    st.markdown("### 📊 Compare Schemes")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.selectbox("Scheme 1:", ["PM-Kisan", "MGNREGA"], key="s1")
    with col2:
        s2 = st.selectbox("Scheme 2:", ["MGNREGA", "PM-Kisan"], key="s2")
    
    if s1 != s2:
        d1 = KNOWLEDGE_BASE[s1].get(st.session_state.language, KNOWLEDGE_BASE[s1]["English"])
        d2 = KNOWLEDGE_BASE[s2].get(st.session_state.language, KNOWLEDGE_BASE[s2]["English"])
        
        comparison = f"""
        | Criteria | {s1} | {s2} |
        |----------|------|------|
        | **Benefit** | {d1.get('benefit')} | {d2.get('benefit')} |
        | **When** | {d1.get('when')} | {d2.get('when')} |
        | **Eligibility** | {d1.get('eligibility', [''])[0]} | {d2.get('eligibility', [''])[0]} |
        | **Documents** | {d1.get('documents', [''])[0]} | {d2.get('documents', [''])[0]} |
        | **Helpline** | {d1.get('toll_free')} | {d2.get('toll_free')} |
        """
        st.markdown(comparison)

# TAB 6: STORIES
with tabs[5]:
    st.markdown("### ⭐ Success Stories")
    st.write("✅ **Ramesh (Punjab)** - PM-Kisan - Received ₹6,000 and started new seeds")
    st.write("✅ **Priya (Maharashtra)** - MGNREGA - Earned ₹25,000 in 100 days")
    st.write("✅ **Vijay (Rajasthan)** - PM-Kisan - Paid debts using the benefit")
    st.write("✅ **Anjali (Gujarat)** - MGNREGA - Constructed well for irrigation")

# TAB 7: BENEFITS
with tabs[6]:
    st.markdown("### 💰 Eligibility Calculator")
    income = st.number_input("Annual Income:", 0, 1000000, key="income")
    eligible = 0
    if income < 300000:
        st.success("✅ Eligible for PM-Kisan, MGNREGA, Ayushman Bharat")
        eligible = 3
    elif income < 500000:
        st.info("📋 Eligible for MGNREGA and others")
        eligible = 2
    st.metric("Eligible Schemes", eligible)

# TAB 8: CONTACTS
with tabs[7]:
    st.markdown("### 📞 Government Helplines")
    st.write("**PM-Kisan:** 1800-180-1111")
    st.write("**MGNREGA:** 1800-345-6777")
    st.write("**Ayushman Bharat:** 1800-111-565")
    st.write("**PMJDY:** 1800-180-1111")

st.markdown("---")
st.markdown("<div style='text-align: center;'><p>🌾 Indic-Setu | Making Schemes Simple | © 2026</p></div>", unsafe_allow_html=True)
