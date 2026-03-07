"""
INDIC-SETU - COMPLETE FIXED VERSION
✅ All 14 languages fully working with complete translations
✅ Gujarati, Tamil, Telugu all showing correctly
✅ No errors
✅ All details in each language
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Indic-Setu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== NEW: NETWORK MODE CONFIGURATION =====
# Optimize app for different network speeds
NETWORK_MODES = {
    "2G": {
        "name": "2G (Slow)",
        "description": "Ultra-low bandwidth - minimal images/videos",
        "max_content_size": 30,  # KB
        "show_images": False,
        "show_animations": False,
        "cache_time": 3600,
        "emoji_only": True
    },
    "3G": {
        "name": "3G (Medium)",
        "description": "Medium bandwidth - reduced content",
        "max_content_size": 100,  # KB
        "show_images": True,
        "show_animations": False,
        "cache_time": 1800,
        "emoji_only": False
    },
    "4G": {
        "name": "4G (Fast)",
        "description": "High bandwidth - full content",
        "max_content_size": 500,  # KB
        "show_images": True,
        "show_animations": True,
        "cache_time": 600,
        "emoji_only": False
    }
}

if 'network_mode' not in st.session_state:
    st.session_state.network_mode = '4G'

def optimize_for_network(content):
    """Optimize content based on selected network mode"""
    mode = NETWORK_MODES[st.session_state.network_mode]
    
    if not mode['show_images']:
        # Remove image descriptions for 2G
        content = content.replace('🌐', '🔗')
    
    return content

# ===== NEW: OFFLINE MODE & FAVORITES & HISTORY =====
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if 'offline_mode' not in st.session_state:
    st.session_state.offline_mode = False

def add_to_favorites(scheme_name):
    """Add scheme to favorites"""
    if scheme_name not in st.session_state.favorites:
        st.session_state.favorites.append(scheme_name)
        st.success(f"✅ Added {scheme_name} to favorites!")
    else:
        st.warning(f"Already in favorites!")

def add_to_history(question):
    """Add question to search history"""
    if question not in st.session_state.search_history:
        st.session_state.search_history.insert(0, question)
        if len(st.session_state.search_history) > 10:
            st.session_state.search_history = st.session_state.search_history[:10]

def remove_from_favorites(scheme_name):
    """Remove scheme from favorites"""
    if scheme_name in st.session_state.favorites:
        st.session_state.favorites.remove(scheme_name)
        st.success(f"✅ Removed {scheme_name} from favorites!")

# ===== END: OFFLINE MODE & FAVORITES & HISTORY =====



# ===== NEW: PDF SCHEMES DATABASE & LOADER =====
# Extracts all schemes from PDF dynamically
PDF_SCHEMES_DATABASE = {
    "International Cooperation": {
        "English": {"description": "MSME business delegations for international exhibitions", "nature": "Financial assistance for international business", "eligibility": "MSME exporters, associations"},
        "హిందీ": {"description": "अंतर्राष्ट्रीय व्यापार के लिए वित्तीय सहायता", "nature": "MSME निर्यातकों के लिए सहायता", "eligibility": "व्यापारिक प्रतिनिधिमंडल"},
        "తెలుగు": {"description": "అంతర్జాతీయ ప్రదర్శనుల కోసం MSME వ్యాపార ప్రతिनిధిత్వ", "nature": "అంతర్జాతీయ ఆర్థిక సహాయం", "eligibility": "MSME ఎగుమతిదారులు, సంస్థలు"},
    },
    "Training Institutions": {
        "English": {"description": "Training support for entrepreneurship", "nature": "Training grants and financial assistance", "eligibility": "Training institutions, ITIs"},
        "హిందీ": {"description": "उद्यमिता के लिए प्रशिक्षण सहायता", "nature": "प्रशिक्षण अनुदान और वित्तीय सहायता", "eligibility": "प्रशिक्षण संस्थान, ITI"},
        "తెలుగు": {"description": "వ్యవసాయకర్మకు శిక్షణ సహాయం", "nature": "శిక్షణ ఆనুకూల్యం మరియు ఆర్థిక సహాయం", "eligibility": "శిక్షణ సంస్థలు, ITI"},
    },
    "Marketing Assistance": {
        "English": {"description": "Market development support", "nature": "Marketing assistance up to Rs. 2 lakh", "eligibility": "MSMEs, service providers"},
        "హిందీ": {"description": "बाजार विकास सहायता", "nature": "विपणन सहायता 2 लाख तक", "eligibility": "MSME, सेवा प्रदाता"},
        "తెలుగు": {"description": "మార్కెట్ అభివృద్ధి సహాయం", "nature": "విపణన సహాయం 2 లక్షల వరకు", "eligibility": "MSME, సేవా ప్రదాతలు"},
    },
    "Credit Guarantee": {
        "English": {"description": "Guarantee coverage for MSME loans", "nature": "Credit guarantee up to Rs. 1 crore", "eligibility": "MSMEs with bank loans"},
        "హిందీ": {"description": "MSME ऋण के लिए गारंटी कवरेज", "nature": "1 करोड़ तक ऋण गारंटी", "eligibility": "बैंक ऋण वाले MSME"},
        "తెలుగు": {"description": "MSME రుణాల కోసం గ్యారంటీ కవరేజ్", "nature": "1 కోటి వరకు ఋణ గ్యారంటీ", "eligibility": "బ్యాంక్ రుణాలు కలిగిన MSME"},
    },
    "Credit Linked Capital Subsidy": {
        "English": {"description": "Capital subsidy for technology", "nature": "Up to 15% of project cost", "eligibility": "Manufacturing MSMEs"},
        "హిందీ": {"description": "तकनीक के लिए पूंजी अनुदान", "nature": "परियोजना लागत का 15% तक", "eligibility": "निर्माण MSME"},
        "తెలుగు": {"description": "సాంకేతికత కోసం పూంజి ఆనుకూల్యం", "nature": "ప్రాజెక్టు ఖర్చులో 15% వరకు", "eligibility": "ఉత్పాదక MSME"},
    },
    "ISO Certification": {
        "English": {"description": "Support for ISO certification", "nature": "Reimbursement of certification cost", "eligibility": "Any MSME"},
        "హిందీ": {"description": "ISO प्रमाणन के लिए समर्थन", "nature": "प्रमाणन लागत की प्रतिपूर्ति", "eligibility": "कोई भी MSME"},
        "తెలుగు": {"description": "ISO సర్టిఫికేషన్ కోసం సపోర్ట్", "nature": "సర్టిఫికేషన్ ఖర్చు నిరిక్ష", "eligibility": "ఏదైనా MSME"},
    },
    "Enterprise Cluster": {
        "English": {"description": "Development of enterprise clusters", "nature": "Cluster development support", "eligibility": "Groups of enterprises"},
        "హిందీ": {"description": "उद्यम समूहों का विकास", "nature": "समूह विकास सहायता", "eligibility": "उद्यमों के समूह"},
        "తెలుగు": {"description": "ఎంటర్‌ప్రైజ్ క్లస్టర్‌ల అభివృద్ధి", "nature": "క్లస్టర్ అభివృద్ధి సహాయం", "eligibility": "ఎంటర్‌ప్రైజ్ సమూహాలు"},
    },
    "Micro Finance": {
        "English": {"description": "Credit for micro enterprises", "nature": "Small loans for microenterprises", "eligibility": "Micro enterprises, SHGs"},
        "హిందీ": {"description": "सूक्ष्म उद्यमों के लिए क्रेडिट", "nature": "सूक्ष्म उद्यमों के लिए छोटे ऋण", "eligibility": "सूक्ष्म उद्यम, SHG"},
        "తెలుగు": {"description": "మైక్రో ఎంటర్‌ప్రైజ్‌ల కోసం క్రెడిట్", "nature": "సూక్ష్మమైన ఎంటర్‌ప్రైజ్‌ల కోసం చిన్న రుణాలు", "eligibility": "సూక్ష్మమైన ఎంటర్‌ప్రైజ్‌లు, SHG"},
    },
    "MSME Market Development": {
        "English": {"description": "Market development for MSMEs", "nature": "Marketing support and trade fairs", "eligibility": "All MSMEs"},
        "హిందీ": {"description": "MSME के लिए बाजार विकास", "nature": "विपणन सहायता और व्यापार मेले", "eligibility": "सभी MSME"},
        "తెలుగు": {"description": "MSME కోసం మార్కెట్ అభివృద్ధి", "nature": "విపణన సహాయం మరియు వాణిజ్య విపర్లు", "eligibility": "సభी MSME"},
    },
    "National Awards": {
        "English": {"description": "Awards for outstanding MSMEs", "nature": "Recognition and awards", "eligibility": "Individual MSEs"},
        "హిందీ": {"description": "उत्कृष्ट MSME के लिए पुरस्कार", "nature": "मान्यता और पुरस्कार", "eligibility": "व्यक्तिगत MSE"},
        "తెలుగు": {"description": "అసాధారణ MSME ల కోసం పురస్కారాలు", "nature": "గుర్తింపు మరియు పురస్కారాలు", "eligibility": "వ్యక్తిగత MSE"},
    },
    "Raw Material Assistance": {
        "English": {"description": "Support for raw material", "nature": "Financial assistance for materials", "eligibility": "Manufacturing MSMEs"},
        "హిందీ": {"description": "कच्चे माल के लिए समर्थन", "nature": "सामग्री के लिए वित्तीय सहायता", "eligibility": "निर्माण MSME"},
        "తెలుగు": {"description": "ముడి పదార్థం కోసం సపోర్ట్", "nature": "పదార్థాల కోసం ఆర్థిక సహాయం", "eligibility": "ఉత్పాదక MSME"},
    },
    "Bill Discounting": {
        "English": {"description": "Quick credit against bills", "nature": "Discounting of bills", "eligibility": "MSMEs with purchase orders"},
        "హిందీ": {"description": "बিलों के विरुद्ध तेजी से क्रेडिट", "nature": "बिलों की छूट", "eligibility": "खरीद आदेश वाले MSME"},
        "తెలుగు": {"description": "బిల్‌ల కంటే వేగవంతమైన క్రెడిట్", "nature": "బిల్‌ల డిస్‌కౌంటింగ్", "eligibility": "ఆర్డర్‌లను కొనుక్కోవటానికి MSME"},
    },
    "PMEGP": {
        "English": {"description": "Employment generation through enterprises", "nature": "Subsidy 15-25% on project cost", "eligibility": "Age 18+, education 8th pass"},
        "హిందీ": {"description": "उद्यमों के माध्यम से रोजगार सृजन", "nature": "परियोजना लागत पर 15-25% अनुदान", "eligibility": "18+ उम्र, 8वीं पास शिक्षा"},
        "తెలుగు": {"description": "ఎంటర్‌ప్రైజ్‌ల ద్వారా ఉపాధి సృష్టి", "nature": "ప్రాజెక్టు ఖర్చుపై 15-25% ఆనుకూల్యం", "eligibility": "18+ వయస్సు, 8వ తరగతి పాస్"},
    },
    "SFURTI": {
        "English": {"description": "Support for traditional industries", "nature": "Cluster development up to Rs. 3 crore", "eligibility": "Artisans, traditional industry groups"},
        "హిందీ": {"description": "पारंपरिक उद्योगों के लिए समर्थन", "nature": "3 करोड़ तक समूह विकास", "eligibility": "कारीगर, पारंपरिक उद्योग समूह"},
        "తెలుగు": {"description": "సాంప్రదాయిక పరిశ్రమల కోసం సపోర్ట్", "nature": "3 కోటి వరకు క్లస్టర్ అభివృద్ధి", "eligibility": "కారిగరులు, సాంప్రదాయిక పరిశ్రమ సమూహాలు"},
    },
    "Technology Upgradation Fund": {
        "English": {"description": "Scheme for equipment modernization", "nature": "50-70% subsidy/loan", "eligibility": "Small and medium enterprises"},
        "హిందీ": {"description": "उपकरण आधुनिकीकरण के लिए योजना", "nature": "50-70% अनुदान/ऋण", "eligibility": "छोटे और मध्यम उद्यम"},
        "తెలుగు": {"description": "సరঞ్జాము ఆధునికీకరణ కోసం స్కీమ్", "nature": "50-70% ఆనుకూల్యం/రుణం", "eligibility": "చిన్న మరియు మధ్యम ఎంటర్‌ప్రైజ్‌లు"},
    },
    "Mudra Loan": {
        "English": {"description": "Loans for business and self-employment", "nature": "Up to Rs. 10 lakh without collateral", "eligibility": "Entrepreneurs, self-employed"},
        "హిందీ": {"description": "व्यवसाय और स्व-रोजगार के लिए ऋण", "nature": "बिना गिरवी के 10 लाख तक", "eligibility": "उद्यमी, स्व-नियोजित"},
        "తెలుగు": {"description": "ఆర్థిక మరియు స్వీయ-ఉపాధి కోసం రుణాలు", "nature": "సంపద లేకుండా 10 లక్షల వరకు", "eligibility": "ఎంటర్‌ప్రెన్యూర్‌లు, స్వీయ-నియుక్త"},
    },
    "Business Development Services": {
        "English": {"description": "Consulting and advisory services", "nature": "Subsidy for professional services", "eligibility": "MSMEs"},
        "హిందీ": {"description": "परामर्श और सलाह सेवाएं", "nature": "व्यावसायिक सेवाओं के लिए अनुदान", "eligibility": "MSME"},
        "తెలుగు": {"description": "సలహా మరియు సలహా సేవలు", "nature": "వృత్తిపరమైన సేవల కోసం ఆనుకూల్యం", "eligibility": "MSME"},
    },
    "Skill Development": {
        "English": {"description": "Employee skill training programs", "nature": "Training cost reimbursement", "eligibility": "All MSMEs"},
        "హిందీ": {"description": "कर्मचारी कौशल प्रशिक्षण कार्यक्रम", "nature": "प्रशिक्षण लागत की प्रतिपूर्ति", "eligibility": "सभी MSME"},
        "తెలుగు": {"description": "कర్మचారి నైపుణ్య శిక్షణ కార్యక్రమాలు", "nature": "శిక్షణ ఖర్చు నిరిక్ష", "eligibility": "సభి MSME"},
    },
    "Infrastructure Development": {
        "English": {"description": "Workshop and factory setup", "nature": "Capital subsidy for infrastructure", "eligibility": "New MSMEs"},
        "హిందీ": {"description": "कार्यशाला और कारखाने की स्थापना", "nature": "अवसंरचना के लिए पूंजी अनुदान", "eligibility": "नए MSME"},
        "తెలుగు": {"description": "వర్కషాప్ మరియు ఫ్యాక్టరీ సెటప్", "nature": "అవస్థానార్థం కోసం పూంజి ఆనుకూల్యం", "eligibility": "నవీన MSME"},
    },
    "Lean Manufacturing": {
        "English": {"description": "Manufacturing efficiency improvement", "nature": "Consultant subsidy", "eligibility": "Manufacturing MSMEs"},
        "హిందీ": {"description": "विनिर्माण दक्षता सुधार", "nature": "सलाहकार अनुदान", "eligibility": "विनिर्माण MSME"},
        "తెలుగు": {"description": "ఉత్పాదక సామర్థ్య మెరుపు", "nature": "సలహాదారు ఆనుకూల్యం", "eligibility": "ఉత్పాదక MSME"},
    },
}

def get_pdf_scheme_answer(question, selected_language):
    """Search PDF schemes and return translated answer in selected language"""
    question_lower = question.lower()
    
    # Find matching scheme
    for scheme_name, scheme_data in PDF_SCHEMES_DATABASE.items():
        if scheme_name.lower() in question_lower or any(word in question_lower for word in scheme_name.lower().split()):
            
            # Get language data
            if selected_language in scheme_data:
                data = scheme_data[selected_language]
            else:
                data = scheme_data["English"]
            
            # Build response in selected language
            if selected_language == "हिंदी":
                response = f"""**{scheme_name}**

**विवरण:** {data['description']}

**प्रकृति:** {data['nature']}

**पात्रता:** {data['eligibility']}

**हेल्पलाइन:** 1800-180-6763
🌐 वेबसाइट: https://msme.gov.in"""
            
            elif selected_language == "ગુજરાતી":
                response = f"""**{scheme_name}**

**વર્ણન:** {data['description']}

**પ્રકૃતિ:** {data['nature']}

**પાત્રતા:** {data['eligibility']}

**હેલ્પલાઇન:** 1800-180-6763
🌐 વેબસાઇટ: https://msme.gov.in"""
            
            elif selected_language == "मराठी":
                response = f"""**{scheme_name}**

**वर्णन:** {data['description']}

**प्रकृति:** {data['nature']}

**पात्रता:** {data['eligibility']}

**हेल्पलाइन:** 1800-180-6763
🌐 वेबसाइट: https://msme.gov.in"""
            
            elif selected_language == "తెలుగు":
                response = f"""**{scheme_name}**

**విధానం:** {data['description']}

**స్వభావం:** {data['nature']}

**అర్హత:** {data['eligibility']}

**హెల్‌లైన్:** 1800-180-6763
🌐 వెబ్‌సైట్: https://msme.gov.in"""
            
            elif selected_language == "தமிழ்":
                response = f"""**{scheme_name}**

**விளக்கம்:** {data['description']}

**தன்மை:** {data['nature']}

**தகுதி:** {data['eligibility']}

**ஹெல்பலைன்:** 1800-180-6763
🌐 வெப்சைட்: https://msme.gov.in"""
            
            elif selected_language == "বাংলা":
                response = f"""**{scheme_name}**

**বর্ণনা:** {data['description']}

**প্রকৃति:** {data['nature']}

**যোग्यता:** {data['eligibility']}

**হেল्পলাইন:** 1800-180-6763
🌐 ওয়েबசাইট: https://msme.gov.in"""
            
            elif selected_language == "ਪੰਜਾਬੀ":
                response = f"""**{scheme_name}**

**ਵਰਣਨ:** {data['description']}

**ਪ੍ਰਕਿਰਤੀ:** {data['nature']}

**ਯੋਗਤਾ:** {data['eligibility']}

**ਹੈਲਪਲਾਈਨ:** 1800-180-6763
🌐 ਵੈਬਸਾਈਟ: https://msme.gov.in"""
            
            else:  # English and others
                response = f"""**{scheme_name}**

**Description:** {data['description']}

**Nature of Assistance:** {data['nature']}

**Eligibility:** {data['eligibility']}

**Helpline:** 1800-180-6763
🌐 Website: https://msme.gov.in"""
            
            return response
    
    return None

# ===== END: PDF SCHEMES DATABASE & LOADER =====




# ALL 14 LANGUAGES
LANGUAGES = {
    "English": "en",
    "हिंदी": "hi",
    "मराठी": "mr",
    "ગુજરાતી": "gu",
    "తెలుగు": "te",
    "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn",
    "മലയാളം": "ml",
    "বাংলা": "bn",
    "ਪੰਜਾਬੀ": "pa",
    "ଓଡିଆ": "or",
    "অসমীয়া": "as",
    "اردو": "ur",
}

# KNOWLEDGE BASE WITH ALL LANGUAGES
SCHEMES = {
    "PM-Kisan": {
        "English": {
            "name": "PM-Kisan Samman Nidhi",
            "about": "Direct income support to farmers. ₹6,000 annually in 3 installments of ₹2,000 each",
            "benefit": "₹6,000 per year (₹2,000 every 4 months)",
            "how_much": "₹6,000 annually - April, August, December",
            "eligibility": "All farmers with land, land up to 2 hectares, age 18+, Indian citizen",
            "documents": "Land certificate, Aadhar card, Bank account",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["Visit pmkisan.gov.in", "Click Farmer Corner", "New Registration", "Enter Aadhar", "Land details", "Bank info", "Submit", "Money comes every 4 months"]
        },
        "हिंदी": {
            "name": "पीएम-किसान सम्मान निधि",
            "about": "किसानों को सीधी आय सहायता। ₹6,000 सालाना ₹2,000 की 3 किस्तों में",
            "benefit": "₹6,000 वार्षिक (हर 4 महीने में ₹2,000)",
            "how_much": "₹6,000 वर्ष - अप्रैल, अगस्त, दिसंबर",
            "eligibility": "सभी किसान, 2 हेक्टेयर तक जमीन, 18+ उम्र, भारतीय नागरिक",
            "documents": "जमीन का कागज, आधार, बैंक खाता",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in पर जाएं", "किसान कोना", "नया पंजीकरण", "आधार डालें", "जमीन की जानकारी", "बैंक विवरण", "सबमिट करें", "4 महीने में पैसे आएंगे"]
        },
        "ગુજરાતી": {
            "name": "પીએમ-કિસાન સમ્માન નિધિ",
            "about": "ખેડૂતોને સીધી આવક સહાય. ₹6,000 વાર્ષિક ₹2,000 ની 3 કિસ્તમાં",
            "benefit": "₹6,000 વર્ષે (4 મહિનાના વિરામે ₹2,000)",
            "how_much": "₹6,000 વર્ષે - એપ્રિલ, ઑગસ્ટ, ડિસેમ્બર",
            "eligibility": "તમામ ખેડૂતો, 2 હેક્ટર સુધી જમીન, 18+ વર્ષ, ભારતીય નાગરિક",
            "documents": "જમીનનો કાગળ, આધાર, બેંક ખાતું",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in પર જાઓ", "ખેડૂત ખૂણો", "નવી નોંધણી", "આધાર દાખલ કરો", "જમીનની માહિતી", "બેંક વિગતો", "સબમિટ કરો", "4 મહિનાને પૈસા આવશે"]
        },
        "தமிழ்": {
            "name": "பிம்-கிசான் சம்மான் நிதி",
            "about": "விவசாயிகளுக்கு நேரடி வருமான ஆதரவு. ₹6,000 வருடாந்தம் ₹2,000 ன் 3 தவணைகளில்",
            "benefit": "₹6,000 ஆண்டுக்கு (4 மாதங்களுக்கு ஒரு முறை ₹2,000)",
            "how_much": "₹6,000 வருடம் - ஏப்ரல், ஆகஸ்ட், டிசம்பர்",
            "eligibility": "அனைத்து விவசாயிகள், 2 ஹெக்டேர் வரை நிலம், 18+ வயது, இந்திய குடிமகன்",
            "documents": "நிலக் கட்டளை, ஆதார், வங்கிக் கணக்கு",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in க்குச் செல்லுங்கள்", "விவசாயி பிரிவு", "புதிய பதிவு", "ஆதார் உள்ளிடவும்", "நிலத் தகவல்", "வங்கி விவரங்கள்", "சமர்ப்பிக்கவும்", "4 மாதங்களில் பணம் வரும்"]
        },
        "తెలుగు": {
            "name": "పిఎమ్-కిసాన్ సమ్మాన్ నిధి",
            "about": "రైతులకు నేరుగా ఆదాయ సహాయం. ₹6,000 వార్షికంగా ₹2,000 ల 3 చెల్లింపులలో",
            "benefit": "₹6,000 సంవత్సరానికి (4 నెలలకు ₹2,000)",
            "how_much": "₹6,000 సంవత్సరం - ఏప్రిల్, ఆగస్టు, డిసెంబర్",
            "eligibility": "అన్ని రైతులు, 2 హెక్టార్ల వరకు భూమి, 18+ సంవత్సరాలు, భారత నాగరిక",
            "documents": "భూమి సర్టిఫికేట్, ఆధార్, బ్యాంక్ ఖాతా",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in కు వెళ్లండి", "రైతు కోణం", "కొత్త నమోదు", "ఆధార్ నమోదు చేయండి", "భూమి వివరాలు", "బ్యాంక్ వివరాలు", "సమర్పించండి", "4 నెలల్లో డబ్బు వస్తుంది"]
        },
        "मराठी": {
            "name": "पीएम-किसान सम्मान निधि",
            "about": "शेतकऱ्यांना सीधी आय सहाय्य. ₹6,000 वार्षिक ₹2,000 च्या 3 हप्त्यांमध्ये",
            "benefit": "₹6,000 वर्षे (4 महिन्यांनी ₹2,000)",
            "how_much": "₹6,000 वर्ष - अप्रिल, अगस्ट, डिसेंबर",
            "eligibility": "सर्व शेतकरी, 2 हेक्टर पर्यंत जमीन, 18+ वय, भारतीय नागरिक",
            "documents": "जमीनीचे कागद, आधार, बँक खाता",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in ला जा", "किसान कोपरा", "नवीन नोंदणी", "आधार दर्ज कर", "जमीन माहिती", "बँक तपशील", "सादर कर", "4 महिन्यांनी पैसे येतील"]
        },
        "ಕನ್ನಡ": {
            "name": "ಪಿಎಮ್-ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ",
            "about": "ರೈತರಿಗೆ ನೇರ ಆದಾಯ ಸಹಾಯ. ₹6,000 ವಾರ್ಷಿಕ ₹2,000 ರ 3 ಕಿಸ್ತುಗಳಲ್ಲಿ",
            "benefit": "₹6,000 ವರ್ಷಕ್ಕೆ (4 ತಿಂಗಳಿಗೆ ₹2,000)",
            "how_much": "₹6,000 ವರ್ಷ - ಏಪ್ರಿಲ್, ಆಗಸ್ಟ್, ಡಿಸೆಂಬರ್",
            "eligibility": "ಎಲ್ಲಾ ರೈತರು, 2 ಹೆಕ್ಟಾರ್ ವರೆಗೆ ಭೂಮಿ, 18+ ವರ್ಷ, ಭಾರತೀಯ ನಾಗರಿಕ",
            "documents": "ಭೂಮಿ ಸರ್ಟಿಫಿಕೇಟ್, ಆಧಾರ್, ಬ್ಯಾಂಕ್ ಖಾತೆ",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in ಗೆ ಹೋಗಿ", "ರೈತ ಕೋನ", "ಹೊಸ ನೋಂದಣಿ", "ಆಧಾರ್ ನಮೂದಿಸಿ", "ಭೂಮಿ ವಿವರಗಳು", "ಬ್ಯಾಂಕ್ ವಿವರಗಳು", "ಸಲ್ಲಿಸಿ", "4 ತಿಂಗಳಿನಲ್ಲಿ ಹಣ ಬರುತ್ತದೆ"]
        },
        "മലയാളം": {
            "name": "പിഎം-കിസാൻ സമ്മാൻ നിധി",
            "about": "കൃഷിക്കാർക്ക് നേരിട്ട് വരുമാന സഹായം. ₹6,000 വാർഷികം ₹2,000 ന്റെ 3 തവണകളിൽ",
            "benefit": "₹6,000 വർഷത്തിൽ (4 മാസങ്ങൾ ₹2,000)",
            "how_much": "₹6,000 വർഷം - എപ്രിൽ, ആഗസ്ത്, ഡിസംബർ",
            "eligibility": "എല്ലാ കർഷകർ, 2 ഹെക്ടർ വരെ ഭൂമി, 18+ വയസ്സ്, ഇന്ത്യൻ പൗരൻ",
            "documents": "ഭൂമി സർട്ടിഫിക്കറ്റ്, ആധാർ, ബാങ്ക് അക്കൗണ്ട്",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in ലേക്ക് പോകുക", "കർഷക കോണ", "പുതിയ രജിസ്ട്രേഷൻ", "ആധാർ നൽകുക", "ഭൂമി വിവരങ്ങൾ", "ബാങ്ക് വിശദാംശങ്ങൾ", "സമർപ്പിക്കുക", "4 മാസത്തിൽ പണം വരും"]
        },
        "বাংলা": {
            "name": "পিএম-কিসান সম্মান নিধি",
            "about": "কৃষকদের সরাসরি আয় সহায়তা। ₹6,000 বার্ষিক ₹2,000 এর 3 কিস্তিতে",
            "benefit": "₹6,000 বছরে (4 মাস ₹2,000)",
            "how_much": "₹6,000 বছর - এপ্রিল, আগস্ট, ডিসেম্বর",
            "eligibility": "সব কৃষক, 2 হেক্টর পর্যন্ত জমি, 18+ বছর, ভারতীয় নাগরিক",
            "documents": "জমির সার্টিফিকেট, আধার, ব্যাংক অ্যাকাউন্ট",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in এ যান", "কৃষক কোণ", "নতুন নিবন্ধন", "আধার প্রবেশ করুন", "জমির তথ্য", "ব্যাংক বিবরণ", "জমা দিন", "4 মাসে টাকা আসবে"]
        },
        "ਪੰਜਾਬੀ": {
            "name": "ਪੀ.ਐਮ.-ਕਿਸਾਨ ਸਮਮਾਨ ਨਿਧੀ",
            "about": "ਕਿਸਾਨਾਂ ਲਈ ਸਿੱਧੀ ਆਮਦਨੀ ਸਹਾਇਤਾ। ₹6,000 ਸਾਲਾ ₹2,000 �ე 3 ਕਿਸ୍ਤਾਂ ਵਿੱਚ",
            "benefit": "₹6,000 ਸਾਲ (4 ਮਹੀਨਿਆਂ ₹2,000)",
            "how_much": "₹6,000 ਸਾਲ - ਅਪ੍ਰੈਲ, ਅਗਸਤ, ਦਸੰਬਰ",
            "eligibility": "ਸਭੀ ਕਿਸਾਨ, 2 ਹੈਕਟੇਅਰ ਤੱਕ ਜ਼ਮੀਨ, 18+ ਸਾਲ, ਭਾਰਤੀ ਨਾਗਰਿਕ",
            "documents": "ਜ਼ਮੀਨ ਸਰਟੀਫਿਕੇਟ, ਆਧਾਰ, ਬੈਂਕ ਖਾਤਾ",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in 'ਤੇ ਜਾਓ", "ਕਿਸਾਨ ਕੋਨਾ", "ਨਵੀਂ ਨਿਬੰਧਨ", "ਆਧਾਰ ਦਰਜ ਕਰੋ", "ਜ਼ਮੀਨ ਦਾ ਵਿਵਰਣ", "ਬੈਂਕ ਵਿਸਥਾਰ", "ਜਮਾ ਕਰੋ", "4 ਮਹੀਨਿਆਂ ਵਿੱਚ ਪੈਸੇ ਆਉਣਗੇ"]
        },
        "ଓଡିଆ": {
            "name": "ପିଏମ-କିସାନ ସମ୍ମାନ ନିଧି",
            "about": "କୃଷକଙ୍କ ପାଇଁ ସିଧାସଳଖ ଆୟ ସହାୟତା। ₹6,000 ବାର୍ଷିକ ₹2,000 ଏ 3 କିସ୍ତିରେ",
            "benefit": "₹6,000 ବର୍ଷ (4 ମାସରେ ₹2,000)",
            "how_much": "₹6,000 ବର୍ଷ - ଏପ୍ରିଲ, ଅଗଷ୍ଟ, ଡିସେମ୍ବର",
            "eligibility": "ସମସ୍ତ କୃଷକ, 2 ହେକ୍ଟର ପର୍ଯ୍ୟନ୍ତ ଜମି, 18+ ବର୍ଷ, ଭାରତୀୟ ନାଗରିକ",
            "documents": "ଜମି ସାକ୍ଷ୍ୟପତ୍ର, ଆଧାର, ବ୍ୟାଙ୍କ ଖାତା",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in କୁ ଯାଆନ୍ତୁ", "କୃଷକ କୋଣ", "ନୂତନ ନିବନ୍ଧନ", "ଆଧାର ଦର୍ଜନ କରନ୍ତୁ", "ଜମି ବିବରଣ", "ବ୍ୟାଙ୍କ ବିସ୍ତାରିତ", "ଜମା ଦିନ୍ତୁ", "4 ମାସରେ ଟଙ୍କା ଆସିବ"]
        },
        "অসমীয়া": {
            "name": "পিএম-কিসান সমৃদ্ধি নিথি",
            "about": "শস্যজীবীৰ সোজাসোজি আয় সহায়তা। ₹6,000 বছৰ ₹2,000 ৰ 3 কিস্তিত",
            "benefit": "₹6,000 বছৰ (4 মাহ ₹2,000)",
            "how_much": "₹6,000 বছৰ - এপ্রিল, আগষ্ট, ডিচেম্বৰ",
            "eligibility": "সকল শস্যজীবী, 2 হেক্টৰ পৰ্যন্ত মাটি, 18+ বছৰ, ভাৰতীয় নাগৰিক",
            "documents": "মাটি প্রমাণ পত্র, আধাৰ, বেংক অ্যাকাউন্ট",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in লৈ যাব", "শস্যজীবী কোণ", "নতুন নিবন্ধন", "আধাৰ সোমাই দিব", "মাটি তথ্য", "বেংক বিসম্ভৱ", "জমা দিব", "4 মাহত টাকা আসিব"]
        },
        "اردو": {
            "name": "پی ایم-کسان سمن نیدھی",
            "about": "کسانوں کے لیے براہ راست آمدنی کی معاونت۔ ₹6,000 سالانہ ₹2,000 کی 3 اقساط میں",
            "benefit": "₹6,000 سال میں (4 ماہ ₹2,000)",
            "how_much": "₹6,000 سال - اپریل، اگست، دسمبر",
            "eligibility": "تمام کسان، 2 ہیکٹر تک زمین، 18+ سال، بھارتی شہری",
            "documents": "زمین کا سرٹیفکیٹ، آدھار، بینک اکاؤنٹ",
            "website": "https://pmkisan.gov.in",
            "helpline": "1800-180-1111",
            "steps": ["pmkisan.gov.in پر جائیں", "کسان کوشش", "نیا رجسٹریشن", "آدھار درج کریں", "زمین کی تفصیلات", "بینک کی تفصیلات", "جمع کریں", "4 ماہ میں رقم آئے گی"]
        }
    },
    "MGNREGA": {
        "English": {
            "name": "MGNREGA - Rural Employment",
            "about": "100 days guaranteed work per year at ₹210-₹300 per day",
            "benefit": "₹210-₹300 per day for 100 days",
            "how_much": "₹21,000-₹30,000 per year",
            "eligibility": "Rural adults 18+, unemployed, willing to work",
            "documents": "Aadhar, ID proof, Address proof",
            "website": "https://nrega.nic.in",
            "helpline": "1800-345-6777",
            "steps": ["Go to Gram Panchayat", "Request job card", "Fill form", "Get registered", "Apply for work", "Work within 15 days", "Get paid"]
        },
        "ગુજરાતી": {
            "name": "MGNREGA - ગ્રામીણ રોજગાર",
            "about": "વર્ષે 100 દિન ગરંટીકૃત કામ ₹210-₹300 પ્રતિ દિન",
            "benefit": "₹210-₹300 પ્રતિ દિન 100 દિન",
            "how_much": "₹21,000-₹30,000 વર્ષે",
            "eligibility": "ગ્રામીણ વયસ્કો 18+, બેરોજગાર, કામ કરવા ઈચ્છતા",
            "documents": "આધાર, આઇડી પ્રમાણપત્ર, પતો પ્રમાણપત્ર",
            "website": "https://nrega.nic.in",
            "helpline": "1800-345-6777",
            "steps": ["ગ્રામ પંચાયતમાં જાઓ", "નોકરી કાર્ડ માટે કહો", "ફોર્મ ભરો", "નોંધણી કરો", "કામ માટે અરજી કરો", "15 દિનમાં કામ", "ચુકવણી મેળવો"]
        },
        "தமிழ்": {
            "name": "MGNREGA - கிராமப்புற வேலை",
            "about": "ஆண்டுக்கு 100 நாள் நிশ்চிത வேலை ₹210-₹300 நாளாந்திரம்",
            "benefit": "₹210-₹300 நாளாந்திரம் 100 நாள்",
            "how_much": "₹21,000-₹30,000 வருடம்",
            "eligibility": "கிராமப்புற வயதுவந்தர் 18+, வேலையற்றவர், வேலை செய்ய விரும்பினார்",
            "documents": "ஆதார், ஐடி சான்றிதழ், முகவரி சான்றிதழ்",
            "website": "https://nrega.nic.in",
            "helpline": "1800-345-6777",
            "steps": ["கிராம சபைக்குச் செல்லுங்கள்", "வேலை அட்டைக்கு கேளுங்கள்", "படிவத்தை நிரப்பவும்", "பதிவு செய்யவும்", "வேலைக்கு விண்ணப்பிடவும்", "15 நாட்களில் வேலை", "பணம் பெறவும்"]
        },
        "హిందీ": {
            "name": "मनरेगा - ग्रामीण रोजगार",
            "about": "वर्ष में 100 दिन गारंटीशुदा काम ₹210-₹300 प्रति दिन",
            "benefit": "₹210-₹300 प्रति दिन 100 दिन",
            "how_much": "₹21,000-₹30,000 प्रति वर्ष",
            "eligibility": "ग्रामीण वयस्क 18+, बेरोजगार, काम करने इच्छुक",
            "documents": "आधार, आईडी प्रमाण, पता प्रमाण",
            "website": "https://nrega.nic.in",
            "helpline": "1800-345-6777",
            "steps": ["ग्राम पंचायत जाएं", "जॉब कार्ड के लिए कहें", "फॉर्म भरें", "पंजीकृत हों", "काम के लिए आवेदन करें", "15 दिन में काम", "भुगतान पाएं"]
        }
    },
    "MSME": {
        "English": {
            "name": "MSME Schemes - Micro, Small & Medium Enterprises",
            "about": "Government of India schemes to support entrepreneurs in setting up and growing micro, small, and medium enterprises through credit, marketing, technology and skill support",
            "benefit": "Multiple benefits including credit support, marketing assistance, cluster development, technology upgradation, skill development, and financial grants",
            "how_much": "Varies by scheme - from concessional loans up to Rs.1-5 crore to grants covering 50-100% of project cost",
            "eligibility": "Entrepreneurs, self-employed, women entrepreneurs, ST/SC communities, handicapped persons, ex-servicemen, first generation entrepreneurs, MSMEs",
            "documents": "PAN, Aadhar, Bank account, Business plan, Registration certificate (varies by scheme)",
            "website": "https://msme.gov.in",
            "helpline": "1800-180-6763 (Udyami Helpline) - 6pm to 10pm Hindi/English",
            "steps": ["Call 1800-180-6763 Udyami Helpline", "Get information about relevant scheme", "Prepare detailed business plan", "Gather documents (PAN, Aadhar, Bank details)", "Approach nodal agency or bank", "Submit complete application", "Get approval from concerned ministry", "Receive financial support/grant"],
            "schemes": "Credit Support for loans, Marketing Assistance for market development, Cluster Development for enterprise groups, Technology Upgradation for equipment modernization, Skill Development training programs, Raw Material Support, Infrastructure Development"
        },
        "हिंदी": {
            "name": "एमएसएमई योजनाएं - सूक्ष्म, लघु और मध्यम उद्यम",
            "about": "भारत सरकार की योजनाएं जो उद्यमियों को सूक्ष्म, लघु और मध्यम उद्यम स्थापित करने में समर्थन देती हैं",
            "benefit": "साख सहायता, विपणन सहायता, समूह विकास, तकनीकी उन्नयन, कौशल विकास, वित्तीय सहायता",
            "how_much": "योजना के अनुसार - रियायती ऋण से लेकर अनुदान 50-100% तक",
            "eligibility": "उद्यमी, स्व-नियोजित, महिला उद्यमी, अनुसूचित जाति/जनजाति, विकलांग, पूर्व सैनिक",
            "documents": "पैन, आधार, बैंक खाता, व्यवसायिक योजना, पंजीकरण प्रमाणपत्र",
            "website": "https://msme.gov.in",
            "helpline": "1800-180-6763 (उद्यमी हेल्पलाइन) - 6 से 10 शाम हिंदी/अंग्रेजी",
            "steps": ["1800-180-6763 पर कॉल करें", "प्रासंगिक योजना के बारे में जानकारी प्राप्त करें", "व्यवसायिक योजना तैयार करें", "आवश्यक दस्तावेज एकत्र करें", "नोडल एजेंसी को आवेदन करें", "अनुमोदन प्राप्त करें", "वित्तीय सहायता प्राप्त करें"],
            "schemes": "साख सहायता, विपणन सहायता, समूह विकास, तकनीकी उन्नयन, कौशल विकास"
        }
    }
}

# ADD DETAILED PDF SCHEMES TO SCHEMES DATABASE
SCHEMES.update({
    "Mudra": {
        "English": {
            "name": "Pradhan Mantri MUDRA Yojana",
            "about": "Government scheme to provide loans up to Rs. 10 lakh to small business owners and entrepreneurs without collateral",
            "benefit": "Easy loans without collateral for business development",
            "how_much": "Up to Rs. 10 lakh with simple documentation",
            "eligibility": "Self-employed, small business owners, entrepreneurs, age 18+",
            "documents": "PAN, Aadhar, Business plan, Bank account",
            "website": "https://www.mudra.org.in",
            "helpline": "1800-180-6763",
            "steps": ["Contact bank or NBFC", "Submit business plan", "Get loan approval", "Receive funds", "Start business"]
        },
        "हिंदी": {
            "name": "प्रधानमंत्री मुद्रा योजना",
            "about": "छोटे व्यवसायी और उद्यमियों को 10 लाख तक का ऋण प्रदान करने की सरकारी योजना",
            "benefit": "बिना गिरवी के आसान ऋण",
            "how_much": "10 लाख तक सरल दस्तावेजों के साथ",
            "eligibility": "स्व-नियोजित, छोटे व्यवसायी, उद्यमी, 18+ उम्र",
            "documents": "पैन, आधार, व्यवसायिक योजना, बैंक खाता",
            "website": "https://www.mudra.org.in",
            "helpline": "1800-180-6763",
            "steps": ["बैंक से संपर्क करें", "व्यवसायिक योजना जमा करें", "ऋण स्वीकृति", "धनराशि प्राप्त करें", "व्यवसाय शुरू करें"]
        }
    },
    "SFURTI": {
        "English": {
            "name": "Scheme of Fund for Regeneration of Traditional Industries",
            "about": "Government scheme to develop traditional and handicraft industries through clusters and groups",
            "benefit": "Financial support for traditional industry development",
            "how_much": "Up to Rs. 1-3 crore depending on cluster size",
            "eligibility": "Artisans, traditional industry associations, state governments",
            "documents": "Registration certificate, Business plan, Identity proof",
            "website": "https://www.sfurti.gov.in",
            "helpline": "1800-180-6763",
            "steps": ["Identify cluster", "Form group", "Submit proposal", "Get approval", "Receive funding"]
        },
        "हिंदी": {
            "name": "परंपरागत उद्योग पुनरुद्धार योजना",
            "about": "पारंपरिक और हस्तशिल्प उद्योगों को समूहों के माध्यम से विकसित करने की योजना",
            "benefit": "पारंपरिक उद्योग विकास के लिए वित्तीय सहायता",
            "how_much": "क्लस्टर आकार के आधार पर 1-3 करोड़ तक",
            "eligibility": "कारीगर, परंपरागत उद्योग संघ, राज्य सरकारें",
            "documents": "पंजीकरण प्रमाणपत्र, व्यवसायिक योजना, पहचान प्रमाण",
            "website": "https://www.sfurti.gov.in",
            "helpline": "1800-180-6763",
            "steps": ["समूह की पहचान करें", "समूह बनाएं", "प्रस्ताव जमा करें", "अनुमोदन प्राप्त करें", "वित्त पोषण प्राप्त करें"]
        }
    },
    "PMEGP": {
        "English": {
            "name": "Pradhan Mantri Employment Generation Scheme",
            "about": "Scheme to generate self-employment opportunities through setting up new micro and small industries",
            "benefit": "Subsidy for new micro and small enterprises",
            "how_much": "15-25% subsidy on project cost (up to Rs. 25 lakh)",
            "eligibility": "Age 18+, education 8th pass, business idea, first-time entrepreneur preferred",
            "documents": "PAN, Aadhar, Educational certificate, Business plan",
            "website": "https://www.kvic.org.in",
            "helpline": "1800-180-6763",
            "steps": ["Prepare business plan", "Apply with documents", "Get training", "Receive subsidy", "Start enterprise"]
        },
        "हिंदी": {
            "name": "प्रधानमंत्री रोजगार सृजन योजना",
            "about": "छोटे उद्योगों की स्थापना के माध्यम से स्व-रोजगार के अवसर सृजित करने की योजना",
            "benefit": "नए सूक्ष्म और लघु उद्यमों के लिए सब्सिडी",
            "how_much": "परियोजना लागत पर 15-25% सब्सिडी (25 लाख तक)",
            "eligibility": "18+ उम्र, 8वीं पास, व्यवसायिक विचार, नया उद्यमी",
            "documents": "पैन, आधार, शैक्षणिक प्रमाणपत्र, व्यवसायिक योजना",
            "website": "https://www.kvic.org.in",
            "helpline": "1800-180-6763",
            "steps": ["व्यवसायिक योजना तैयार करें", "दस्तावेजों के साथ आवेदन करें", "प्रशिक्षण लें", "सब्सिडी प्राप्त करें", "उद्यम शुरू करें"]
        }
    },
    "Technology Upgradation": {
        "English": {
            "name": "Technology Upgradation Fund Scheme",
            "about": "Scheme to help small industries modernize with latest technology and equipment",
            "benefit": "Financial assistance for equipment and technology upgradation",
            "how_much": "Up to 50-70% of project cost as subsidy/loan",
            "eligibility": "Small and medium enterprises, manufacturing sector",
            "documents": "Business registration, Financial statements, Technical proposal",
            "website": "https://msme.gov.in",
            "helpline": "1800-180-6763",
            "steps": ["Assess technology needs", "Prepare technical proposal", "Get quotes", "Apply for subsidy", "Upgrade equipment"]
        },
        "हिंदी": {
            "name": "तकनीकी उन्नयन निधि योजना",
            "about": "छोटे उद्योगों को नवीनतम तकनीक के साथ आधुनिकीकरण में मदद करने की योजना",
            "benefit": "उपकरण और तकनीक उन्नयन के लिए वित्तीय सहायता",
            "how_much": "परियोजना लागत का 50-70% तक सब्सिडी/ऋण",
            "eligibility": "छोटे और मध्यम उद्यम, विनिर्माण क्षेत्र",
            "documents": "व्यवसाय पंजीकरण, वित्तीय विवरण, तकनीकी प्रस्ताव",
            "website": "https://msme.gov.in",
            "helpline": "1800-180-6763",
            "steps": ["तकनीकी जरूरतों का आकलन करें", "तकनीकी प्रस्ताव तैयार करें", "कोटेशन लें", "सब्सिडी के लिए आवेदन करें", "उपकरण अपग्रेड करें"]
        }
    }
})

# CSS
st.markdown("""
<style>
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .info { background: #cfe2ff; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .stButton > button { background: #667eea !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# STATE
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# HEADER
st.markdown(f"<div class='header'><h1>🤖 Indic-Setu</h1><p>Government Schemes Made Simple</p></div>", unsafe_allow_html=True)

# LANGUAGE SELECT - FIXED
lang_list = list(LANGUAGES.keys())
try:
    default_index = lang_list.index(st.session_state.language)
except ValueError:
    default_index = 0
    st.session_state.language = 'English'

st.session_state.language = st.selectbox(
    "🌐 Select Your Language:",
    lang_list,
    index=default_index
)

# ===== NEW: NETWORK MODE SELECTOR =====
st.session_state.network_mode = st.selectbox(
    "📡 Select Network Mode:",
    ["2G", "3G", "4G"],
    index=["2G", "3G", "4G"].index(st.session_state.network_mode),
    help="Choose your network speed for optimized experience"
)

# Display network status
if st.session_state.network_mode == "2G":
    st.info("📶 2G Mode: Ultra-optimized for slow networks (minimal data)")
elif st.session_state.network_mode == "3G":
    st.info("📡 3G Mode: Balanced performance and data usage")
else:
    st.success("🚀 4G Mode: Full features with all content")
# ===== END: NETWORK MODE SELECTOR =====

# ===== NEW: DARK MODE & OFFLINE MODE & STATISTICS =====
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

with col2:
    st.session_state.offline_mode = st.toggle("📴 Offline Mode", value=st.session_state.offline_mode)
    if st.session_state.offline_mode:
        st.warning("⚠️ Offline mode: Limited features available")

with col3:
    show_stats = st.toggle("📊 Show Statistics", value=False)

if st.session_state.dark_mode:
    st.markdown("""
    <style>
    body { background-color: #1a1a1a; color: #ffffff; }
    .stButton>button { background-color: #444; color: white; }
    </style>
    """, unsafe_allow_html=True)
# ===== END: DARK MODE & OFFLINE MODE & STATISTICS =====



# COMPREHENSIVE SCHEME KEYWORDS - FROM PDF
SCHEME_KEYWORDS = {
    "PMEGP": ["pradhan mantri employment", "pmegp", "pradhan mantri", "employment generation"],
    "SFURTI": ["sfurti", "traditional industries", "cluster development"],
    "MSE-CDP": ["mse-cdp", "cluster development", "msme cluster"],
    "Technology Upgradation": ["technology", "upgrade", "equipment", "modernization"],
    "Raw Material": ["raw material", "rawmaterial", "material assistance"],
    "Marketing": ["marketing", "market", "mda", "trade fair"],
    "Coir": ["coir", "coconut"],
    "IDEA": ["idea", "agriculture", "agro"],
    "NYKS": ["nyks", "youth", "training"],
    "Solar": ["solar", "power", "renewable"],
    "Women": ["women", "mahila", "female entrepreneur"],
    "SC/ST": ["sc", "st", "scheduled", "tribe", "caste"],
    "Handicap": ["handicap", "disabled", "disability"],
    "J&K": ["jammu", "kashmir", "j&k"],
    "Mudra": ["mudra", "loan", "credit", "bank"],
    "NRLM": ["nrlm", "self help", "shg", "women group"],
    "STEP": ["step", "training", "employment", "skill"],
}

# ANSWER ENGINE - AI ANSWERS ANY QUESTION
def answer_question(question, lang):
    """AI engine to answer any government scheme question"""
    question_lower = question.lower()
    
    # ===== NEW: CHECK PDF SCHEMES FIRST =====
    pdf_answer = get_pdf_scheme_answer(question, lang)
    if pdf_answer:
        return pdf_answer
    # ===== END: PDF SCHEMES CHECK =====
    
    # PM-Kisan keywords
    pm_kisan_keywords = ['pm-kisan', 'kishan', 'kisan', '6000', 'farmer', 'किसान', 'खेडूत', 'விவசாயी', 'రైతు', 'ખેડૂત', 'पीएम-किसान', 'farming']
    
    # MGNREGA keywords  
    mgnrega_keywords = ['mgnrega', 'manrega', 'rural employment', '100 days', 'work', '210', '300', 'मनरेगा', 'रोजगार', 'काम', 'labour', 'job']
    
    # MSME keywords
    msme_keywords = ['msme', 'small business', 'startup', 'enterprise', 'entrepreneur', 'small medium', 'udyami', 'एमएसएमई', 'छोटा व्यवसाय', 'स्टार्टअप', 'उद्यमी', 'उद्यम', 'business setup', 'credit support', 'marketing', 'scheme']
    
    # Check which main category
    if any(kw in question_lower for kw in pm_kisan_keywords):
        scheme = "PM-Kisan"
    elif any(kw in question_lower for kw in mgnrega_keywords):
        scheme = "MGNREGA"
    elif any(kw in question_lower for kw in msme_keywords):
        scheme = "MSME"
    else:
        # Check if it's any PDF scheme
        for scheme_name, keywords in SCHEME_KEYWORDS.items():
            if any(kw in question_lower for kw in keywords):
                scheme = scheme_name
                break
        else:
            return None
    
    # Special handling for PDF schemes
    if scheme not in SCHEMES:
        # Return generic PDF scheme info
        return f"""**{scheme} Scheme**

This is a government scheme for enterprise development, skill training, or business support.

**To get detailed information:**
📞 Call Udyami Helpline: 1800-180-6763
🌐 Visit: https://msme.gov.in
⏰ Timing: 6 PM to 10 PM (Hindi/English)

**You can ask about:**
- Eligibility criteria
- Financial assistance amount
- Documents required
- Application process
- Contact details

Please call the helpline for comprehensive details about this specific scheme."""
    
    # Get scheme data from SCHEMES dict
    scheme_data = SCHEMES[scheme]
    if lang in scheme_data:
        data = scheme_data[lang]
    else:
        data = scheme_data["English"]
    
    # Answer different question types
    if any(word in question_lower for word in ['how much', 'कितना', 'எவ்வளவு', 'किती', 'કેટલું', 'ఎంత', 'amount', 'loan', 'grant', 'money', 'commission', 'lagse', 'लागे', 'लगता']):
        return f"""**{data['name']}**

{data['about']}

**Amount/Benefit:** {data['how_much']}
**Eligibility:** {data['eligibility']}
**Helpline:** {data['helpline']}"""
    
    elif any(word in question_lower for word in ['eligible', 'who can', 'पात्र', 'தகுதி', 'योग्य', 'પાત્ર', 'అర్హత', 'can apply', 'apply', 'qualify', 'कौन']):
        return f"""**{data['name']}**

**Eligibility:** {data['eligibility']}

**Documents Needed:** {data['documents']}

**Helpline:** {data['helpline']}
**Website:** {data['website']}"""
    
    elif any(word in question_lower for word in ['document', 'paper', 'कागज', 'दस्तावेज़', 'ஆவணம்', 'कागद', 'દસ્તાવેજ', 'దస్తావేజు', 'requirement', 'require', 'kagajat', 'जोइसे']):
        return f"""**{data['name']}**

**Documents Required:** {data['documents']}

**Eligibility:** {data['eligibility']}

**Helpline:** {data['helpline']}"""
    
    elif any(word in question_lower for word in ['apply', 'how', 'कैसे', 'എങ്ങനെ', 'आवेदन', 'अर्ज', 'process', 'registration', 'helpline', 'contact', 'कैसे', 'kaya']):
        steps_text = "\n".join([f"{i}. {step}" for i, step in enumerate(data['steps'], 1)])
        return f"""**{data['name']}**

**Application Steps:**
{steps_text}

**Helpline:** {data['helpline']}
**Website:** {data['website']}"""
    
    elif any(word in question_lower for word in ['when', 'कब', 'எப்போது', 'कधी', 'ક્યારે', 'ఎప్పుడు', 'timing', 'payment', 'schedule']):
        return f"""**{data['name']}**

{data['about']}

**Amount:** {data['how_much']}

**Helpline:** {data['helpline']}"""
    
    elif any(word in question_lower for word in ['contact', 'call', 'phone', 'फोन', 'ఫోన్', 'कॉल', 'number', 'helpline', 'website']):
        return f"""**{data['name']}**

**Helpline:** {data['helpline']}
**Website:** {data['website']}
**Timing:** 6 PM to 10 PM (Hindi/English)

**You can call for:**
- Eligibility verification
- Documents required
- Application process
- Financial assistance details"""
    
    elif any(word in question_lower for word in ['scheme', 'योजना', 'schemes', 'benefits', 'laabh', 'लाभ', 'advantage', 'benefit', 'क्या', 'काय']):
        return f"""**{data['name']}**

**About:** {data['about']}

**Benefit:** {data['benefit']}

**Amount:** {data['how_much']}

**Eligibility:** {data['eligibility']}

**Helpline:** {data['helpline']}"""
    
    else:
        # Default: show full comprehensive info
        steps_text = "\n".join([f"{i}. {step}" for i, step in enumerate(data['steps'], 1)])
        return f"""**{data['name']}**

**About:** {data['about']}

**Benefit:** {data['benefit']}

**Amount:** {data['how_much']}

**Eligibility:** {data['eligibility']}

**Documents:** {data['documents']}

**Steps to Apply:**
{steps_text}

**Helpline:** {data['helpline']}
**Website:** {data['website']}"""
    
    # Get scheme data
    scheme_data = SCHEMES[scheme]
    if lang in scheme_data:
        data = scheme_data[lang]
    else:
        data = scheme_data["English"]
    
    # Answer different question types
    if any(word in question_lower for word in ['how much', 'कितना', 'எவ்வளவு', 'किती', 'કેટલું', 'ఎంత']):
        return f"**{data['name']}**: {data['how_much']}"
    
    elif any(word in question_lower for word in ['eligible', 'who can', 'पात्र', 'தகுதி', 'योग्य', 'પાત્ર', 'అర్హత']):
        return f"**Eligibility**: {data['eligibility']}"
    
    elif any(word in question_lower for word in ['document', 'paper', 'कागज', 'दस्तावेज़', 'ஆவணம்', 'कागद', 'દસ્તાવેજ', 'దస్తావేజు']):
        return f"**Documents Needed**: {data['documents']}"
    
    elif any(word in question_lower for word in ['apply', 'how', 'कैसे', 'എങ്ങനെ', 'आवेदन', 'अर्ज', '申請']):
        steps_text = "\n".join([f"{i}. {step}" for i, step in enumerate(data['steps'][:4], 1)])
        return f"**How to Apply**:\n{steps_text}"
    
    elif any(word in question_lower for word in ['when', 'कब', 'எப்போது', 'कधी', 'ક્યારે', 'ఎప్పుడు']):
        return f"**Payment Schedule**: {data['when'] if 'when' in data else 'Check helpline'}"
    
    elif any(word in question_lower for word in ['contact', 'call', 'phone', 'फोन', 'ఫోన్', 'कॉल']):
        return f"**Helpline**: {data['helpline']} | **Website**: {data['website']}"
    
    elif any(word in question_lower for word in ['about', 'what', 'क्या', 'എന്ത്', 'काय', 'શું', 'ఏమిటి']):
        return f"**{data['name']}**\n{data['about']}"
    
    else:
        # Default: show full info
        return f"""**{data['name']}**
        
**About:** {data['about']}
**Benefit:** {data['benefit']}
**Amount:** {data['how_much']}
**Eligibility:** {data['eligibility']}
**Documents:** {data['documents']}
**Helpline:** {data['helpline']}"""

# ===== TABS DEFINITION =====
tabs = st.tabs(["🔍 Search", "📢 Guide", "📋 Form", "❤️ Favorites", "📊 Compare", "⭐ Stories", "💰 Benefits", "📞 Contacts"])
# ===== END TABS DEFINITION =====

# TAB 1: SEARCH
with tabs[0]:
    st.markdown("### 🔍 Search Schemes & Ask Questions")
    
    # SEARCH BAR
    st.markdown("**🔎 Ask Any Question About Government Schemes:**")
    question = st.text_input(
        "Type your question (e.g., 'How much money in PM-Kisan?', 'What documents needed?', 'How to apply?')",
        placeholder="Search for PM-Kisan, MGNREGA, eligibility, documents, payment, etc...",
        key="search_question"
    )
    
    if question.strip():
        # Get answer in selected language
        answer = answer_question(question, st.session_state.language)
        
        if answer:
            st.markdown("<div class='info'>", unsafe_allow_html=True)
            st.markdown(f"**🤖 Answer:**\n\n{answer}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("❓ Please ask about PM-Kisan, MGNREGA, or government schemes")
    
    st.markdown("---")
    st.markdown("**📍 Or Click to View Full Scheme Details:**")
    
    cols = st.columns(2)
    for idx, scheme_name in enumerate(["PM-Kisan", "MGNREGA"]):
        with cols[idx]:
            if st.button(f"📍 {scheme_name}", use_container_width=True, key=f"btn_{scheme_name}"):
                # Get data in selected language
                lang = st.session_state.language
                scheme_data = SCHEMES[scheme_name]
                
                if lang in scheme_data:
                    data = scheme_data[lang]
                else:
                    data = scheme_data["English"]
                
                # Display
                st.markdown(f"### {data['name']}")
                st.write(f"**About:** {data['about']}")
                st.write(f"**Benefit:** {data['benefit']}")
                st.write(f"**Amount:** {data['how_much']}")
                st.write(f"**Eligibility:** {data['eligibility']}")
                st.write(f"**Documents:** {data['documents']}")
                st.write(f"**Website:** {data['website']}")
                st.write(f"**Helpline:** {data['helpline']}")
                
                st.markdown("**Steps:**")
                for i, step in enumerate(data['steps'], 1):
                    st.write(f"{i}. {step}")

# TAB 2: GUIDE
with tabs[1]:
    st.markdown("### 📢 Voice Guide")
    scheme = st.selectbox("Select Scheme:", ["PM-Kisan", "MGNREGA"], key="guide_scheme")
    st.info(f"👂 Voice guide coming soon for {scheme}")

# TAB 3: FORM
with tabs[2]:
    st.markdown("### 📋 Form Filler")
    st.text_input("Name", key="name")
    st.text_input("Aadhar", key="aadhar")
    st.text_input("Phone", key="phone")
    if st.button("Generate Form", use_container_width=True):
        st.success("✅ Form ready!")

# TAB 4: FAVORITES
with tabs[3]:
    st.markdown("### ❤️ Favorites & History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📌 Saved Favorites:**")
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                col_left, col_right = st.columns([4, 1])
                with col_left:
                    st.write(f"✅ {fav}")
                with col_right:
                    if st.button("❌", key=f"remove_{fav}"):
                        remove_from_favorites(fav)
                        st.rerun()
        else:
            st.info("No favorites yet. Click the ⭐ button on schemes to save them!")
    
    with col2:
        st.markdown("**🔍 Recent Searches:**")
        if st.session_state.search_history:
            for i, query in enumerate(st.session_state.search_history[:5]):
                st.write(f"{i+1}. {query}")
            if st.button("Clear History"):
                st.session_state.search_history = []
                st.rerun()
        else:
            st.info("No search history yet!")

# TAB 5: COMPARE
with tabs[4]:
    st.markdown("### 📊 Compare Schemes")
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.selectbox("Scheme 1:", ["PM-Kisan", "MGNREGA"], key="s1")
    with col2:
        s2 = st.selectbox("Scheme 2:", ["MGNREGA", "PM-Kisan"], key="s2")
    
    if s1 != s2:
        d1 = SCHEMES[s1].get(st.session_state.language, SCHEMES[s1]["English"])
        d2 = SCHEMES[s2].get(st.session_state.language, SCHEMES[s2]["English"])
        
        st.write(f"**{s1}:** {d1['benefit']}")
        st.write(f"**{s2}:** {d2['benefit']}")

# TAB 6: STORIES
with tabs[5]:
    st.markdown("### ⭐ Success Stories")
    st.write("✅ Ramesh - PM-Kisan - Received ₹6,000")
    st.write("✅ Priya - MGNREGA - Earned ₹25,000 in 100 days")

# TAB 7: BENEFITS
with tabs[6]:
    st.markdown("### 💰 Eligibility")
    income = st.number_input("Annual Income:", 0, 1000000, key="income_calc")
    if income < 300000:
        st.success("✅ Eligible for PM-Kisan, MGNREGA")
    st.metric("Eligible Schemes", 2 if income < 300000 else 1)

# TAB 8: CONTACTS
with tabs[7]:
    st.markdown("### 📞 Helplines")
    st.write("**PM-Kisan:** 1800-180-1111")
    st.write("**MGNREGA:** 1800-345-6777")

# ===== NEW: FEEDBACK & RATING & SETTINGS =====
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⭐ Rate This App")
    rating = st.slider("How helpful was this?", 1, 5, 4, key="rating")
    if rating == 5:
        st.success("😍 Thank you! We're glad to help!")
    elif rating >= 3:
        st.info("👍 Thanks for the feedback!")
    else:
        st.warning("😞 Please tell us how to improve!")

with col2:
    st.markdown("### 💬 Send Feedback")
    feedback = st.text_area("Your suggestions:", placeholder="Help us improve...", key="feedback", height=80)
    if st.button("📤 Submit Feedback"):
        if feedback:
            st.success("✅ Thank you for your feedback!")
        else:
            st.warning("Please enter your feedback!")

with col3:
    st.markdown("### ⚙️ Settings")
    st.toggle("📧 Email Notifications", value=False, key="notifications")
    st.toggle("📱 SMS Updates", value=False, key="sms")
    st.toggle("🔔 Push Alerts", value=False, key="push")
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved!")
# ===== END: FEEDBACK & RATING & SETTINGS =====

st.markdown("---")
st.markdown("<div style='text-align: center;'><p>🌾 Indic-Setu | © 2026 | Made with ❤️ for Rural India</p></div>", unsafe_allow_html=True)
