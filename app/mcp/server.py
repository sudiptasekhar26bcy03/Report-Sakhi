"""
MCP Server: Provides tools to assist healthcare patients in India.
Includes the 'find_nearby_help' tool linking patients to nearby hospitals,
clinics, diagnostic labs, and emergency helplines based on Red/Yellow report status.
"""

from typing import Dict, Any, Optional, List
import logging
from mcp.server.mcpserver import MCPServer

logger = logging.getLogger(__name__)

# Initialize MCP Server instance
server = MCPServer("report-sakhi-help")


LOCALIZED_HELP_ADVICE = {
    "ml": {
        "red_title": "അടിയന്തിര സഹായം തേടുക",
        "red_advice": "ചില പരിശോധനാ ഫലങ്ങൾ സാധാരണ പരിധിക്ക് പുറത്താണ്. റിപ്പോർട്ടുമായി ഉടൻ അടുത്തുള്ള ആശുപത്രിയിലോ കാഷ്വാലിറ്റിയിലോ പോകുക.",
        "yellow_title": "ഡോക്ടറെ സമീപിക്കുക",
        "yellow_advice": "ചില അളവുകളിൽ വ്യത്യാസമുണ്ട്. അടുത്ത ദിവസങ്ങളിൽ ഒരു ഡോക്ടറെ കണ്ട് റിപ്പോർട്ട് കാണിക്കുക."
    },
    "hi": {
        "red_title": "तुरंत डॉक्टर की सलाह लें",
        "red_advice": "कुछ जांच परिणाम सामान्य सीमा से काफी बाहर हैं। तुरंत नजदीकी अस्पताल या आपातकालीन केंद्र में डॉक्टर से संपर्क करें।",
        "yellow_title": "डॉक्टर से परामर्श लें",
        "yellow_advice": "कुछ मान सामान्य सीमा से थोड़े अलग हैं। अगले कुछ दिनों में नजदीकी क्लिनिक या डॉक्टर से परामर्श लें।"
    },
    "ta": {
        "red_title": "உடனடி மருத்துவ உதவி",
        "red_advice": "சில முடிவுகள் இயல்பான வரம்பை விட வேறுபட்டுள்ளன. உடனடியாக அருகிலுள்ள மருத்துவமனை அல்லது அவசர சிகிச்சை மையத்தை அணுகவும்.",
        "yellow_title": "மருத்துவரை அணுகவும்",
        "yellow_advice": "சில அளவுகளில் மாற்றம் உள்ளது. அடுத்த சில நாட்களில் அருகிலுள்ள மருத்துவரிடம் ஆலோசிக்கவும்."
    },
    "te": {
        "red_title": "తక్షణ వైద్య సహాయం",
        "red_advice": "కొన్ని పరీక్షల ఫలితాలు సాధారణ పరిమితి కంటే చాలా భిన్నంగా ఉన్నాయి. వెంటనే దగ్గరలోని ఆసుపత్రిని సంప్రదించండి.",
        "yellow_title": "వైద్యుడిని సంప్రదించండి",
        "yellow_advice": "కొన్ని విలువల్లో తేడాలు ఉన్నాయి. రాబోయే కొద్ది రోజుల్లో సమీపంలోని వైద్యుడిని సంప్రదించండి."
    },
    "kn": {
        "red_title": "ತುರ್ತು ವೈದ್ಯಕೀಯ ನೆರವು",
        "red_advice": "ಕೆಲವು ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳು ಸಾಮಾನ್ಯ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿವೆ. ತಕ್ಷಣ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ.",
        "yellow_title": "ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ",
        "yellow_advice": "ಕೆಲವು ಮೌಲ್ಯಗಳಲ್ಲಿ ವ್ಯತ್ಯಾಸವಿದೆ. ಮುಂದಿನ ಕೆಲವೇ ದಿನಗಳಲ್ಲಿ ಹತ್ತಿರದ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ."
    },
    "bn": {
        "red_title": "জরুরি চিকিৎসা সহায়তা",
        "red_advice": "কিছু পরীক্ষার ফলাফল স্বাভাবিক সীমার অনেক বাইরে। অবিলম্বে নিকটস্থ হাসপাতালে যোগাযোগ করুন।",
        "yellow_title": "ডাক্তারের পরামর্শ নিন",
        "yellow_advice": "কিছু মান স্বাভাবিকের চেয়ে আলাদা। আগামী কয়েক দিনের মধ্যে চিকিৎসকের পরামর্শ নিন।"
    },
    "mr": {
        "red_title": "तातडीची वैद्यकीय मदत",
        "red_advice": "काही चाचण्यांचे निकाल सामान्य मर्यादेपेक्षा खूप वेगळे आहेत. लगेच जवळच्या रुग्णालयात जा.",
        "yellow_title": "डॉक्टरांचा सल्ला घ्या",
        "yellow_advice": "काही मूल्यांमध्ये फरक आहे. पुढील काही दिवसांत डॉक्टरांशी संपर्क साधा."
    },
    "gu": {
        "red_title": "તાત્કાલિક તબીબી સહાય",
        "red_advice": "કેટલાક પરિણામો સામાન્ય મર્યાદાથી ઘણા બહાર છે. તાત્કાલિક નજીકની હોસ્પિટલનો સંપર્ક કરો.",
        "yellow_title": "ડૉક્ટરની સલાહ લો",
        "yellow_advice": "કેટલાક મૂલ્યોમાં તફાવત છે. આગામી દિવસોમાં ડૉક્ટરની સલાહ લો."
    },
    "pa": {
        "red_title": "ਤੁਰੰਤ ਡਾਕਟਰੀ ਸਹਾਇਤਾ",
        "red_advice": "ਕੁਝ ਟੈਸਟ ਨਤੀਜੇ ਆਮ ਸੀਮਾ ਤੋਂ ਕਾਫ਼ੀ ਬਾਹਰ ਹਨ। ਤੁਰੰਤ ਨਜ਼ਦੀਕੀ ਹਸਪਤਾਲ ਜਾਓ।",
        "yellow_title": "ਡਾਕਟਰ ਦੀ ਸਲਾਹ ਲਵੋ",
        "yellow_advice": "ਕੁਝ ਮੁੱਲਾਂ ਵਿੱਚ ਫਰਕ ਹੈ। ਅਗਲੇ ਕੁਝ ਦਿਨਾਂ ਵਿੱਚ ਡਾਕਟਰ ਨਾਲ ਸੰਪਰਕ ਕਰੋ।"
    },
    "or": {
        "red_title": "ଜରୁରୀକାଳୀନ ଚିକିତ୍ସା",
        "red_advice": "କିଛି ପରୀକ୍ଷା ଫଳାଫଳ ସାଧାରଣ ସୀମାରୁ ବହୁତ ବାହାରେ ଅଛି। ତୁରନ୍ତ ଡାକ୍ତରଖାନା ଯାଆନ୍ତୁ।",
        "yellow_title": "ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ",
        "yellow_advice": "କିଛି ମୂଲ୍ୟରେ ପରିବର୍ତ୍ତନ ଅଛି। ଶୀଘ୍ର ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ।"
    },
    "as": {
        "red_title": "জৰুৰী চিকিৎসা সাহায্য",
        "red_advice": "কিছুমান ফলাফল স্বাভাৱিক সীমাৰ বাহিৰত আছে। অবিলম্বে ওচৰৰ চিকিৎসালয়লৈ যাওক।",
        "yellow_title": "চিকিৎসকৰ পৰামৰ্শ লওক",
        "yellow_advice": "কিছুমান মানত পাৰ্থক্য আছে। সোনকালে চিকিৎসকৰ পৰামৰ্শ লওক।"
    },
    "ur": {
        "red_title": "فوری طبی امداد",
        "red_advice": "کچھ ٹیسٹ کے نتائج معمول کی حد سے باہر ہیں۔ فوری طور پر قریبی ہسپتال سے رجوع کریں۔",
        "yellow_title": "ڈاکٹر سے مشورہ کریں",
        "yellow_advice": "کچھ اقدار میں فرق ہے۔ اگلے چند دنوں میں قریبی ڈاکٹر سے مشورہ کریں۔"
    },
    "en": {
        "red_title": "Urgent Medical Attention",
        "red_advice": "Certain test values are significantly outside normal limits. Please visit the nearest hospital or emergency center promptly with this report.",
        "yellow_title": "Consult a Doctor",
        "yellow_advice": "Certain test values differ from usual ranges. Please schedule a visit to a nearby doctor or health clinic in the next few days."
    }
}


@server.tool()
def find_nearby_help(
    query_type: str = "hospital",
    urgency: str = "red",
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    language: str = "en"
) -> Dict[str, Any]:
    """
    Finds nearby hospitals, clinics, or diagnostic labs based on patient urgency (red/yellow).
    Generates turn-by-turn map search links and includes Indian emergency helplines (108, 104, 112).
    
    Args:
        query_type: 'hospital', 'clinic', 'lab', or 'all'
        urgency: 'red' (emergency/urgent) or 'yellow' (consult doctor/routine attention)
        latitude: Optional patient GPS latitude
        longitude: Optional patient GPS longitude
        language: Language code ('ml', 'hi', 'ta', 'en')
    """
    urgency_norm = urgency.lower().strip() if urgency else "red"
    is_urgent = (urgency_norm == "red")
    lang = language if language in LOCALIZED_HELP_ADVICE else "en"
    lang_info = LOCALIZED_HELP_ADVICE[lang]

    # 1. Build Direct Turn-by-Turn Map URL
    if latitude is not None and longitude is not None:
        if is_urgent or query_type == "hospital":
            query_str = "hospitals+or+emergency+trauma+centers"
        elif query_type == "lab":
            query_str = "diagnostic+labs+and+pathology+centres"
        else:
            query_str = "doctors+clinics+or+primary+health+centres"
        map_url = f"https://www.google.com/maps/search/{query_str}/@{latitude},{longitude},14z"
    else:
        if is_urgent or query_type == "hospital":
            map_url = "https://www.google.com/maps/search/nearest+hospital+or+emergency+clinic+near+me"
        elif query_type == "lab":
            map_url = "https://www.google.com/maps/search/nearest+diagnostic+lab+or+pathology+near+me"
        else:
            map_url = "https://www.google.com/maps/search/nearest+doctor+clinic+or+health+centre+near+me"

    # 2. Curated Facility Recommendations for Bharat Healthcare
    if is_urgent:
        facilities = [
            {"type": "Government District Hospital", "desc": "24/7 Casualty & Critical Care"},
            {"type": "Community Health Centre (CHC)", "desc": "Specialist Doctors & Emergency Inpatient"},
            {"type": "Private Multi-specialty Hospital", "desc": "Immediate Clinical Attention"}
        ]
        title = lang_info["red_title"]
        advice = lang_info["red_advice"]
    else:
        facilities = [
            {"type": "Primary Health Centre (PHC)", "desc": "Local Government Doctor & Essential Medicines"},
            {"type": "Family Physician / General Practitioner", "desc": "Routine Health Consultation"},
            {"type": "NABL Accredited Diagnostic Lab", "desc": "Repeat / Follow-up Blood Tests"}
        ]
        title = lang_info["yellow_title"]
        advice = lang_info["yellow_advice"]

    # 3. National Emergency & Health Helplines for India
    helplines = [
        {
            "code": "108",
            "name": "108 Ambulance",
            "desc": "Toll-Free Emergency Medical Response",
            "tel": "tel:108"
        },
        {
            "code": "104",
            "name": "104 Health Helpline",
            "desc": "24/7 Free Medical Advice & Guidance",
            "tel": "tel:104"
        },
        {
            "code": "112",
            "name": "112 National Emergency",
            "desc": "All-in-One Emergency Services",
            "tel": "tel:112"
        }
    ]

    return {
        "status": "success",
        "urgency": urgency_norm,
        "query_type": query_type,
        "title": title,
        "advice": advice,
        "map_url": map_url,
        "has_gps": (latitude is not None and longitude is not None),
        "facilities": facilities,
        "helplines": helplines
    }


if __name__ == "__main__":
    # Allows running as a standalone MCP server via stdio
    server.run(transport="stdio")
