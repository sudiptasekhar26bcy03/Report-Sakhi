/* -------------------------------------------------------------
   ReportSakhi - Interactive Frontend Logic
   Handles Language Switching, Camera Scan, Simple Mode,
   Multi-Provider Voice Audio (Bhashini/Sarvam/Google/Azure/Browser),
   Attached Result Cards Listen Bar, Hero Mic Voice Q/A,
   and MCP-powered find_nearby_help for Red/Yellow results.
   ------------------------------------------------------------- */

// Localized UI Dictionary
const I18N = {
    ml: {
        brandTagline: "നിങ്ങളുടെ ആരോഗ്യ സുഹൃത്ത്",
        simpleModeText: "ലളിത രൂപം",
        simpleModeSub: "വലിയ അക്ഷരങ്ങളും ശബ്ദവും",
        langSectionTitle: "ഭാഷ തിരഞ്ഞെടുക്കുക",
        langSectionHint: "നിങ്ങളുടെ മാതൃഭാഷയിൽ ഫലങ്ങൾ കേൾക്കൂ",
        scanHeading: "ലാബ് റിപ്പോർട്ട് സ്കാൻ ചെയ്യുക",
        scanSubheading: "രക്തം, പഞ്ചസാര അല്ലെങ്കിൽ തൈറോയ്ഡ് റിപ്പോർട്ടിന്റെ വ്യക്തമായ ഫോട്ടോ എടുക്കൂ",
        scanBtnLabel: "റിപ്പോർട്ട് സ്കാൻ ചെയ്യുക",
        scanBtnSub: "ക്യാമറ അല്ലെങ്കിൽ ഗാലറി",
        demoSampleText: "സാമ്പിൾ റിപ്പോർട്ട് കാണുക (CBC + Sugar)",
        hl1: "സുരക്ഷിത റഫറൻസ് പരിധികൾ",
        hl2: "ശബ്ദ വിശദീകരണം",
        hl3: "അടുത്തുള്ള ആശുപത്രി",
        loadingTitle: "റിപ്പോർട്ട് വായിക്കുന്നു...",
        loadingStep: "റീഡർ ഏജന്റ് ഫലങ്ങൾ കണ്ടെത്തുന്നു",
        backBtnText: "പുതിയ സ്കാൻ",
        listenButtonLabel: "വിശദീകരണം കേൾക്കുക",
        listenButtonHint: "മലയാളത്തിൽ ഉച്ചരിക്കുന്നു",
        attachedListenMain: "റിപ്പോർട്ട് കേൾക്കുക",
        attachedListenSub: "എല്ലാ പരിശോധനാ ഫലങ്ങളും ശബ്ദത്തിൽ കേൾക്കൂ",
        testsSectionHeading: "പരിശോധനാ ഫലങ്ങൾ",
        hospitalTitle: "ഡോക്ടറെ സമീപിക്കുക",
        hospitalAdvice: "അടുത്തുള്ള ആരോഗ്യ കേന്ദ്രങ്ങൾ കാണാൻ മാപ്പ് തുറക്കുക",
        hospitalActionText: "അടുത്തുള്ള ആശുപത്രി കണ്ടെത്തുക",
        askSectionTitle: "ചോദ്യങ്ങൾ ചോദിക്കാം",
        askSectionSub: "റിപ്പോർട്ടിനെക്കുറിച്ച് ചോദിക്കാൻ മൈക്കിൽ തൊടുക",
        heroMicCaption: "സ്വരത്തിൽ ചോദിക്കുക",
        heroMicHint: "മാതൃഭാഷയിൽ മറുപടി കേൾക്കാം",
        heroMicRecording: "കേൾക്കുന്നു... ചോദിക്കൂ",
        heroMicThinking: "സഖി ചിന്തിക്കുന്നു...",
        replayBtnLabel: "കേൾക്കുക",
        retakeTitle: "ചിത്രം വ്യക്തമല്ല",
        retakeDesc: "ലാബ് റിപ്പോർട്ടിലെ അക്കങ്ങൾ വ്യക്തമായി വായിക്കാൻ സാധിക്കുന്നില്ല. സുരക്ഷിതത്വത്തിനായി ഞങ്ങൾ വിവരങ്ങൾ ഊഹിക്കാറില്ല. ദയവായി നല്ല വെളിച്ചത്തിൽ വ്യക്തമായ ഒരു ഫോട്ടോ വീണ്ടും എടുക്കുക.",
        btnRetakeLabel: "വീണ്ടും ഫോട്ടോ എടുക്കുക",
        btnCancelRetakeLabel: "വേണ്ട",
        askPlaceholder: "ഉദാ: എന്റെ ഷുഗർ കൂടുതലാണോ?",
        sendBtnText: "ചോദിക്കൂ"
    },
    hi: {
        brandTagline: "आपकी सेहत की सच्ची सखी",
        simpleModeText: "सरल मोड",
        simpleModeSub: "बड़े अक्षर और आवाज़",
        langSectionTitle: "अपनी भाषा चुनें",
        langSectionHint: "अपनी भाषा में रिपोर्ट की व्याख्या सुनें",
        scanHeading: "लैब रिपोर्ट स्कैन करें",
        scanSubheading: "ब्लड टेस्ट, शुगर या थायराइड रिपोर्ट का साफ़ फोटो लें",
        scanBtnLabel: "रिपोर्ट स्कैन करें",
        scanBtnSub: "कैमरा या गैलरी",
        demoSampleText: "सैंपल रिपोर्ट देखें (CBC + Sugar)",
        hl1: "सुरक्षित मेडिकल सीमाएं",
        hl2: "आवाज़ में जानकारी",
        hl3: "नजदीकी अस्पताल",
        loadingTitle: "रिपोर्ट पढ़ी जा रही है...",
        loadingStep: "रीडर एजेंट जांच के आंकड़े निकाल रहा है",
        backBtnText: "नया स्कैन",
        listenButtonLabel: "रिपोर्ट की आवाज़ सुनें",
        listenButtonHint: "हिंदी में सरल व्याख्या",
        attachedListenMain: "रिपोर्ट सुनें",
        attachedListenSub: "सभी परिणामों को आवाज़ में सुनने के लिए दबाएं",
        testsSectionHeading: "जांच परिणाम और स्थिति",
        hospitalTitle: "डॉक्टर से परामर्श लें",
        hospitalAdvice: "नजदीकी स्वास्थ्य केंद्र के लिए मैप खोलें",
        hospitalActionText: "नजदीकी अस्पताल खोजें",
        askSectionTitle: "कोई सवाल है?",
        askSectionSub: "माइक दबाकर अपनी रिपोर्ट के बारे में पूछें",
        heroMicCaption: "बोलकर सवाल पूछें",
        heroMicHint: "मातृभाषा में उत्तर सुनें",
        heroMicRecording: "सुन रहे हैं... बोलिए",
        heroMicThinking: "सखी सोच रही है...",
        replayBtnLabel: "सुनें",
        retakeTitle: "फ़ोटो साफ़ नहीं है",
        retakeDesc: "रिपोर्ट के आंकड़े साफ़ नहीं दिख रहे हैं। आपकी सुरक्षा के लिए हम परिणामों का अंदाज़ा नहीं लगाते। कृपया अच्छी रोशनी में दोबारा साफ़ फ़ोटो लें।",
        btnRetakeLabel: "दोबारा फ़ोटो लें",
        btnCancelRetakeLabel: "रद्द करें",
        askPlaceholder: "जैसे: क्या मेरी शुगर ज्यादा है?",
        sendBtnText: "पूछें"
    },
    ta: {
        brandTagline: "உங்கள் மருத்துவத் தோழி",
        simpleModeText: "எளிய முறை",
        simpleModeSub: "பெரிய எழுத்துகள் & குரல்",
        langSectionTitle: "மொழியைத் தேர்ந்தெடுக்கவும்",
        langSectionHint: "உங்கள் சொந்த மொழியில் விளக்கத்தைக் கேளுங்கள்",
        scanHeading: "ஆய்வக அறிக்கையை ஸ்கேன் செய்க",
        scanSubheading: "இரத்தப் பரிசோதனை அல்லது சர்க்கரை அறிக்கையை தெளிவாகப் படம் எடுக்கவும்",
        scanBtnLabel: "ஸ்கேன் செய்க",
        scanBtnSub: "கேமரா அல்லது கேலரி",
        demoSampleText: "மாதிரி அறிக்கை காண்க (CBC + Sugar)",
        hl1: "பாதுகாப்பான மருத்துவ வரம்புகள்",
        hl2: "குரல் விளக்கம்",
        hl3: "அருகிலுள்ள மருத்துவமனை",
        loadingTitle: "அறிக்கை படிக்கப்படுகிறது...",
        loadingStep: "மதிப்புகளைப் பிரித்தெடுக்கிறது",
        backBtnText: "புதிய ஸ்கேன்",
        listenButtonLabel: "விளக்கத்தைக் கேளுங்கள்",
        listenButtonHint: "தமிழில் பேசப்படும்",
        attachedListenMain: "அறிக்கையைக் கேட்கவும்",
        attachedListenSub: "அனைத்து முடிவுகளையும் குரலில் கேட்கத் தட்டவும்",
        testsSectionHeading: "சோதனை முடிவுகள்",
        hospitalTitle: "மருத்துவரை அணுகவும்",
        hospitalAdvice: "அருகிலுள்ள மையங்களைக் காண வரைபடத்தைத் திறக்கவும்",
        hospitalActionText: "அருகிலுள்ள மருத்துவமனை",
        askSectionTitle: "கேள்வி கேட்கவா?",
        askSectionSub: "மைக் பொத்தானைத் தட்டவும்",
        heroMicCaption: "குரலில் கேள்வி கேட்கவும்",
        heroMicHint: "தாய்மொழியில் பதில் கேளுங்கள்",
        heroMicRecording: "கேட்கிறது... பேசுங்கள்",
        heroMicThinking: "சகி சிந்திக்கிறது...",
        replayBtnLabel: "கேட்க",
        retakeTitle: "படம் தெளிவாக இல்லை",
        retakeDesc: "அறிக்கையின் எண்களை தெளிவாகப் படிக்க முடியவில்லை. மருத்துவப் பாதுகாப்பிற்காக நாங்கள் எண்களை ஊகிப்பதில்லை. தயவுசெய்து நல்ல வெளிச்சத்தில் மீண்டும் படம் எடுக்கவும்.",
        btnRetakeLabel: "மீண்டும் படம் எடுக்கவும்",
        btnCancelRetakeLabel: "மூடுக",
        askPlaceholder: "எ.கா: சர்க்கரை அளவு அதிகமா?",
        sendBtnText: "கேட்க"
    },
    te: {
        brandTagline: "మీ ఆరోగ్య స్నేహితురాలు",
        simpleModeText: "సులభ మోడ్",
        simpleModeSub: "పెద్ద అక్షరాలు & ఆడియో",
        langSectionTitle: "భాషను ఎంచుకోండి",
        langSectionHint: "మీ మాతృభాషలో వివరణ వినండి",
        scanHeading: "ల్యాబ్ రిపోర్టును స్కాన్ చేయండి",
        scanSubheading: "రక్తం, షుగర్ రిపోర్టుల స్పష్టమైన ఫోటో తీయండి",
        scanBtnLabel: "రిపోర్టు స్కాన్ చేయండి",
        scanBtnSub: "కెమెరా లేదా గ్యాలరీ",
        demoSampleText: "నమూనా నివేదికను చూడండి (CBC + Sugar)",
        hl1: "సురక్షిత వైద్య పరిమితులు",
        hl2: "వాయిస్ వివరణ",
        hl3: "సమీప ఆసుపత్రి",
        loadingTitle: "నివేదిక చదువుతోంది...",
        loadingStep: "ఫలితాలను సేకరిస్తోంది",
        backBtnText: "కొత్త స్కాన్",
        listenButtonLabel: "వివరణ వినండి",
        listenButtonHint: "తెలుగులో స్పష్టంగా",
        attachedListenMain: "రిపోర్టు వినండి",
        attachedListenSub: "అన్ని ఫలితాలను వాయిస్‌లో వినడానికి నొక్కండి",
        testsSectionHeading: "పరీక్ష ఫలితాలు & స్థితి",
        hospitalTitle: "వైద్యుడిని సంప్రదించండి",
        hospitalAdvice: "సమీప ఆరోగ్య కేంద్రాల కోసం మ్యాప్ తెరవండి",
        hospitalActionText: "సమీప ఆసుపత్రిని కనుగొనండి",
        askSectionTitle: "ప్రశ్న ఉందా?",
        askSectionSub: "మైక్ నొక్కి ప్రశ్న అడగండి",
        heroMicCaption: "నోటితో మాట్లాడి అడగండి",
        heroMicHint: "మాతృభాషలో సమాధానం వినండి",
        heroMicRecording: "వింటోంది... మాట్లాడండి",
        heroMicThinking: "సఖి ఆలోచిస్తోంది...",
        replayBtnLabel: "వినండి",
        retakeTitle: "ఫోటో అస్పష్టంగా ఉంది",
        retakeDesc: "రిపోర్టు వివరాలు స్పష్టంగా కనిపించడం లేదు. మీ భద్రత కోసం మేము అంచనాలు వేయము. దయచేసి స్పష్టమైన ఫోటో తీయండి.",
        btnRetakeLabel: "మళ్ళీ ఫోటో తీయండి",
        btnCancelRetakeLabel: "రద్దు",
        askPlaceholder: "ఉదా: నా షుగర్ ఎక్కువగా ఉందా?",
        sendBtnText: "అడగండి"
    },
    kn: {
        brandTagline: "ನಿಮ್ಮ ಆರೋಗ್ಯದ ಗೆಳತಿ",
        simpleModeText: "ಸರಳ ಮೋಡ್",
        simpleModeSub: "ದೊಡ್ಡ ಅಕ್ಷರಗಳು ಮತ್ತು ಧ್ವನಿ",
        langSectionTitle: "ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
        langSectionHint: "ನಿಮ್ಮ ಮಾತೃಭಾಷೆಯಲ್ಲಿ ವಿವರಣೆ ಕೇಳಿ",
        scanHeading: "ಲ್ಯಾಬ್ ವರದಿ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ",
        scanSubheading: "ರಕ್ತ, ಸಕ್ಕರೆ ವರದಿಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ",
        scanBtnLabel: "ವರದಿ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ",
        scanBtnSub: "ಕ್ಯಾಮೆರಾ ಅಥವಾ ಗ್ಯಾಲರಿ",
        demoSampleText: "ಮಾದರಿ ವರದಿ ನೋಡಿ (CBC + Sugar)",
        hl1: "ಸುರಕ್ಷಿತ ವೈದ್ಯಕೀಯ ಮಿತಿಗಳು",
        hl2: "ಧ್ವನಿ ವಿವರಣೆ",
        hl3: "ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆ",
        loadingTitle: "ವರದಿ ಓದಲಾಗುತ್ತಿದೆ...",
        loadingStep: "ಫಲಿತಾಂಶಗಳನ್ನು ಹೊರತೆಗೆಯಲಾಗುತ್ತಿದೆ",
        backBtnText: "ಹೊಸ ಸ್ಕ್ಯಾನ್",
        listenButtonLabel: "ವಿವರಣೆ ಕೇಳಿ",
        listenButtonHint: "ಕನ್ನಡದಲ್ಲಿ ಧ್ವನಿ",
        attachedListenMain: "ವರದಿ ಕೇಳಿ",
        attachedListenSub: "ಎಲ್ಲಾ ಫಲಿತಾಂಶಗಳನ್ನು ಧ್ವನಿಯಲ್ಲಿ ಕೇಳಲು ಒತ್ತಿರಿ",
        testsSectionHeading: "ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳು",
        hospitalTitle: "ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ",
        hospitalAdvice: "ಆಸ್ಪತ್ರೆಗಳಿಗಾಗಿ ನಕ್ಷೆಯನ್ನು ತೆರೆಯಿರಿ",
        hospitalActionText: "ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆ ಹುಡುಕಿ",
        askSectionTitle: "ಪ್ರಶ್ನೆ ಇದೆಯೇ?",
        askSectionSub: "ಮೈಕ್ ಒತ್ತಿ ಪ್ರಶ್ನೆ ಕೇಳಿ",
        heroMicCaption: "ಧ್ವನಿಯಲ್ಲಿ ಪ್ರಶ್ನೆ ಕೇಳಿ",
        heroMicHint: "ಮಾತೃಭಾಷೆಯಲ್ಲಿ ಉತ್ತರ ಕೇಳಿ",
        heroMicRecording: "ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದೆ... ಮಾತನಾಡಿ",
        heroMicThinking: "ಸಖಿ ಯೋಚಿಸುತ್ತಿದೆ...",
        replayBtnLabel: "ಕೇಳಿ",
        retakeTitle: "ಫೋಟೋ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ",
        retakeDesc: "ವರದಿಯ ಅಂಕಿಅಂಶಗಳು ಸ್ಪಷ್ಟವಾಗಿ ಕಾಣುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಬೆಳಕಿನಲ್ಲಿ ಸ್ಪಷ್ಟವಾದ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ.",
        btnRetakeLabel: "ಮತ್ತೆ ಫೋಟೋ ತೆಗೆಯಿರಿ",
        btnCancelRetakeLabel: "ಮುಚ್ಚಿ",
        askPlaceholder: "ಉದಾ: ನನ್ನ ಸಕ್ಕರೆ ಮಟ್ಟ ಹೆಚ್ಚಿದೆಯೇ?",
        sendBtnText: "ಕೇಳಿ"
    },
    bn: {
        brandTagline: "আপনার স্বাস্থ্য বন্ধু",
        simpleModeText: "সহজ মোড",
        simpleModeSub: "বড় লেখা ও ভয়েস",
        langSectionTitle: "ভাষা নির্বাচন করুন",
        langSectionHint: "মাতৃভাষায় রিপোর্টের ব্যাখ্যা শুনুন",
        scanHeading: "ল্যাব রিপোর্ট স্ক্যান করুন",
        scanSubheading: "রক্ত বা সুগার রিপোর্টের পরিষ্কার ছবি তুলুন",
        scanBtnLabel: "রিপোর্ট স্ক্যান করুন",
        scanBtnSub: "ক্যামেরা বা গ্যালারি",
        demoSampleText: "নমুনা রিপোর্ট দেখুন (CBC + Sugar)",
        hl1: "নিরাপদ চিকিৎসা সীমা",
        hl2: "ভয়েস ব্যাখ্যা",
        hl3: "নিকটস্থ হাসপাতাল",
        loadingTitle: "রিপোর্ট পড়া হচ্ছে...",
        loadingStep: "তথ্য বের করা হচ্ছে",
        backBtnText: "নতুন স্ক্যান",
        listenButtonLabel: "ব্যাখ্যা শুনুন",
        listenButtonHint: "বাংলায় শুনুন",
        attachedListenMain: "রিপোর্ট শুনুন",
        attachedListenSub: "সব ফলাফল ভয়েসে শুনতে চাপুন",
        testsSectionHeading: "পরীক্ষার ফলাফল ও অবস্থা",
        hospitalTitle: "ডাক্তারের পরামর্শ নিন",
        hospitalAdvice: "নিকটস্থ স্বাস্থ্যকেন্দ্রের মানচিত্র দেখুন",
        hospitalActionText: "নিকটস্থ হাসপাতাল খুঁজুন",
        askSectionTitle: "কোনো প্রশ্ন আছে?",
        askSectionSub: "মাইকে ট্যাপ করে প্রশ্ন করুন",
        heroMicCaption: "কথা বলে প্রশ্ন করুন",
        heroMicHint: "মাতৃভাষায় উত্তর শুনুন",
        heroMicRecording: "শুনছি... কথা বলুন",
        heroMicThinking: "সখী ভাবছে...",
        replayBtnLabel: "শুনুন",
        retakeTitle: "ছবি স্পষ্ট নয়",
        retakeDesc: "রিপোর্টের লেখা স্পষ্ট পড়া যাচ্ছে না। অনুমানের বদলে দয়া করে ভালো আলোতে আবার ছবি তুলুন।",
        btnRetakeLabel: "আবার ছবি তুলুন",
        btnCancelRetakeLabel: "বন্ধ করুন",
        askPlaceholder: "যেমন: আমার সুগার কি বেশি?",
        sendBtnText: "জিজ্ঞেস করুন"
    },
    mr: {
        brandTagline: "तुमची आरोग्य सखी",
        simpleModeText: "सोपा मोड",
        simpleModeSub: "मोठे फॉन्ट आणि आवाज",
        langSectionTitle: "भाषा निवडा",
        langSectionHint: "मातृभाषेत रिपोर्ट ऐका",
        scanHeading: "लॅब रिपोर्ट स्कॅन करा",
        scanSubheading: "रक्त किंवा शुगर रिपोर्टचा स्पष्ट फोटो घ्या",
        scanBtnLabel: "रिपोर्ट स्कॅन करा",
        scanBtnSub: "कॅमेरा किंवा गॅलरी",
        demoSampleText: "नमुना रिपोर्ट पहा (CBC + Sugar)",
        hl1: "सुरक्षित वैद्यकीय मर्यादा",
        hl2: "व्हॉइस स्पष्टीकरण",
        hl3: "जवळचे रुग्णालय",
        loadingTitle: "रिपोर्ट वाचत आहे...",
        loadingStep: "तपासणी आकडे काढत आहे",
        backBtnText: "नवीन स्कॅन",
        listenButtonLabel: "स्पष्टीकरण ऐका",
        listenButtonHint: "मराठीत ऐका",
        attachedListenMain: "रिपोर्ट ऐका",
        attachedListenSub: "सर्व निकाल आवाजात ऐकण्यासाठी दाबा",
        testsSectionHeading: "तपासणी निकाल आणि स्थिती",
        hospitalTitle: "डॉक्टरांचा सल्ला घ्या",
        hospitalAdvice: "जवळच्या केंद्रांसाठी नकाशा उघडा",
        hospitalActionText: "जवळचे रुग्णालय शोधा",
        askSectionTitle: "काही प्रश्न आहे?",
        askSectionSub: "माईक दाबून प्रश्न विचारा",
        heroMicCaption: "बोलून प्रश्न विचारा",
        heroMicHint: "मातृभाषेत उत्तर ऐका",
        heroMicRecording: "ऐकत आहे... बोला",
        heroMicThinking: "सखी विचार करत आहे...",
        replayBtnLabel: "ऐका",
        retakeTitle: "फोटो स्पष्ट नाही",
        retakeDesc: "रिपोर्टचे आकडे स्पष्ट दिसत नाहीत. कृपया योग्य प्रकाशात पुन्हा फोटो घ्या.",
        btnRetakeLabel: "पुन्हा फोटो घ्या",
        btnCancelRetakeLabel: "बंद करा",
        askPlaceholder: "उदा: माझी शुगर जास्त आहे का?",
        sendBtnText: "विचारा"
    },
    gu: {
        brandTagline: "તમારી સ્વાસ્થ્ય સખી",
        simpleModeText: "સરળ મોડ",
        simpleModeSub: "મોટા અક્ષરો અને અવાજ",
        langSectionTitle: "ભાષા પસંદ કરો",
        langSectionHint: "તમારી માતૃભાષામાં રિપોર્ટ સાંભળો",
        scanHeading: "લેબ રિપોર્ટ સ્કેન કરો",
        scanSubheading: "બ્લડ અથવા સુગર રિપોર્ટનો સ્પષ્ટ ફોટો લો",
        scanBtnLabel: "રિપોર્ટ સ્કેન કરો",
        scanBtnSub: "કેમેરા અથવા ગેલેરી",
        demoSampleText: "નમૂના રિપોર્ટ જુઓ (CBC + Sugar)",
        hl1: "સુરક્ષિત તબીબી મર્યાદા",
        hl2: "વોઇસ સમજૂતી",
        hl3: "નજીકની હોસ્પિટલ",
        loadingTitle: "રિપોર્ટ વાંચી રહ્યું છે...",
        loadingStep: "આંકડા ચકાસી રહ્યું છે",
        backBtnText: "નવું સ્કેન",
        listenButtonLabel: "સમજૂતી સાંભળો",
        listenButtonHint: "ગુજરાતીમાં સાંભળો",
        attachedListenMain: "રિપોર્ટ સાંભળો",
        attachedListenSub: "પરિણામો અવાજમાં સાંભળવા માટે દબાવો",
        testsSectionHeading: "પરીક્ષણ પરિણામો",
        hospitalTitle: "ડૉક્ટરની સલાહ લો",
        hospitalAdvice: "નજીકના આરોગ્ય કેન્દ્રો માટે મેપ ખોલો",
        hospitalActionText: "નજીકની હોસ્પિટલ શોધો",
        askSectionTitle: "કોઈ પ્રશ્ન છે?",
        askSectionSub: "માઇક દબાવીને પ્રશ્ન પૂછો",
        heroMicCaption: "બોલીને પ્રશ્ન પૂછો",
        heroMicHint: "માતૃભાષામાં જવાબ સાંભળો",
        heroMicRecording: "સાંભળી રહ્યું છે... બોલો",
        heroMicThinking: "સખી વિચારી રહી છે...",
        replayBtnLabel: "સાંભળો",
        retakeTitle: "ફોટો સ્પષ્ટ નથી",
        retakeDesc: "રિપોર્ટના આંકડા સ્પષ્ટ દેખાતા નથી. કૃપા કરીને સારો ફોટો ફરીથી લો.",
        btnRetakeLabel: "ફરી ફોટો લો",
        btnCancelRetakeLabel: "બંધ કરો",
        askPlaceholder: "દા.ત.: શું મારું સુગર વધારે છે?",
        sendBtnText: "પૂછો"
    },
    pa: {
        brandTagline: "ਤੁਹਾਡੀ ਸਿਹਤ ਸਖੀ",
        simpleModeText: "ਸਰਲ ਮੋਡ",
        simpleModeSub: "ਵੱਡੇ ਅੱਖਰ ਅਤੇ ਆਵਾਜ਼",
        langSectionTitle: "ਭਾਸ਼ਾ ਚੁਣੋ",
        langSectionHint: "ਆਪਣੀ ਮਾਂ-ਬੋਲੀ ਵਿੱਚ ਰਿਪੋਰਟ ਸੁਣੋ",
        scanHeading: "ਲੈਬ ਰਿਪੋਰਟ ਸਕੈਨ ਕਰੋ",
        scanSubheading: "ਬਲੱਡ ਜਾਂ ਸ਼ੂਗਰ ਰਿਪੋਰਟ ਦੀ ਸਾਫ਼ ਫ਼ੋਟੋ ਲਵੋ",
        scanBtnLabel: "ਰਿਪੋਰਟ ਸਕੈਨ ਕਰੋ",
        scanBtnSub: "ਕੈਮਰਾ ਜਾਂ ਗੈਲਰੀ",
        demoSampleText: "ਨਮੂਨਾ ਰਿਪੋਰਟ ਵੇਖੋ (CBC + Sugar)",
        hl1: "ਸੁਰੱਖਿਅਤ ਡਾਕਟਰੀ ਸੀਮਾਵਾਂ",
        hl2: "ਆਵਾਜ਼ ਵਿੱਚ ਜਾਣਕਾਰੀ",
        hl3: "ਨੇੜਲਾ ਹਸਪਤਾਲ",
        loadingTitle: "ਰਿਪੋਰਟ ਪੜ੍ਹੀ ਜਾ ਰਹੀ ਹੈ...",
        loadingStep: "ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ ਜਾ ਰਹੇ ਹਨ",
        backBtnText: "ਨਵਾਂ ਸਕੈਨ",
        listenButtonLabel: "ਵਿਆਖਿਆ ਸੁਣੋ",
        listenButtonHint: "ਪੰਜਾਬੀ ਵਿੱਚ ਸੁਣੋ",
        attachedListenMain: "ਰਿਪੋਰਟ ਸੁਣੋ",
        attachedListenSub: "ਸਾਰੇ ਨਤੀਜੇ ਆਵਾਜ਼ ਵਿੱਚ ਸੁਣਨ ਲਈ ਦਬਾਓ",
        testsSectionHeading: "ਟੈਸਟ ਨਤੀਜੇ ਅਤੇ ਸਥਿਤੀ",
        hospitalTitle: "ਡਾਕਟਰ ਦੀ ਸਲਾਹ ਲਵੋ",
        hospitalAdvice: "ਨੇੜਲੇ ਕੇਂਦਰਾਂ ਲਈ ਨਕਸ਼ਾ ਖੋਲ੍ਹੋ",
        hospitalActionText: "ਨੇੜਲਾ ਹਸਪਤਾਲ ਲੱਭੋ",
        askSectionTitle: "ਕੋਈ ਸਵਾਲ ਹੈ?",
        askSectionSub: "ਮਾਈਕ ਦਬਾ ਕੇ ਸਵਾਲ ਪੁੱਛੋ",
        heroMicCaption: "ਬੋਲ ਕੇ ਸਵਾਲ ਪੁੱਛੋ",
        heroMicHint: "ਮਾਂ-ਬੋਲੀ ਵਿੱਚ ਜਵਾਬ ਸੁਣੋ",
        heroMicRecording: "ਸੁਣ ਰਹੇ ਹਾਂ... ਬੋਲੋ",
        heroMicThinking: "ਸਖੀ ਸੋਚ ਰਹੀ ਹੈ...",
        replayBtnLabel: "ਸੁਣੋ",
        retakeTitle: "ਫ਼ੋਟੋ ਸਾਫ਼ ਨਹੀਂ ਹੈ",
        retakeDesc: "ਰਿਪੋਰਟ ਦੇ ਅੰਕੜੇ ਸਾਫ਼ ਨਹੀਂ ਪੜ੍ਹੇ ਜਾ ਰਹੇ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਸਾਫ਼ ਫ਼ੋਟੋ ਲਵੋ।",
        btnRetakeLabel: "ਦੁਬਾਰਾ ਫ਼ੋਟੋ ਲਵੋ",
        btnCancelRetakeLabel: "ਬੰਦ ਕਰੋ",
        askPlaceholder: "ਜਿਵੇਂ: ਕੀ ਮੇਰੀ ਸ਼ੂਗਰ ਵੱਧ ਹੈ?",
        sendBtnText: "ਪੁੱਛੋ"
    },
    or: {
        brandTagline: "ଆପଣଙ୍କ ସ୍ୱାସ୍ଥ୍ୟ ବନ୍ଧୁ",
        simpleModeText: "ସରଳ ମୋଡ୍",
        simpleModeSub: "ବଡ଼ ଅକ୍ଷର ଏବଂ ସ୍ୱର",
        langSectionTitle: "ଭାଷା ବାଛନ୍ତୁ",
        langSectionHint: "ମାତୃଭାଷାରେ ବୁଝନ୍ତୁ",
        scanHeading: "ଲ୍ୟାବ୍ ରିପୋର୍ଟ ସ୍କାନ୍ କରନ୍ତୁ",
        scanSubheading: "ରକ୍ତ କିମ୍ବା ଶର୍କରା ରିପୋର୍ଟର ସ୍ପଷ୍ଟ ଫଟୋ ଉଠାନ୍ତୁ",
        scanBtnLabel: "ରିପୋର୍ଟ ସ୍କାନ୍ କରନ୍ତୁ",
        scanBtnSub: "କ୍ୟାମେରା କିମ୍ବା ଗ୍ୟାଲେରୀ",
        demoSampleText: "ନମୁନା ରିପୋର୍ଟ ଦେଖନ୍ତୁ (CBC + Sugar)",
        hl1: "ସୁରକ୍ଷିତ ଡାକ୍ତରୀ ସୀମା",
        hl2: "ସ୍ୱର ବିବରଣୀ",
        hl3: "ନିକଟସ୍ଥ ଡାକ୍ତରଖାନା",
        loadingTitle: "ରିପୋର୍ଟ ପଢ଼ାଯାଉଛି...",
        loadingStep: "ଫଳାଫଳ ବାହାର କରାଯାଉଛି",
        backBtnText: "ନୂତନ ସ୍କାନ୍",
        listenButtonLabel: "ବିବରଣୀ ଶୁଣନ୍ତୁ",
        listenButtonHint: "ଓଡ଼ିଆରେ ଶୁଣନ୍ତୁ",
        attachedListenMain: "ରିପୋର୍ଟ ଶୁଣନ୍ତୁ",
        attachedListenSub: "ଫଳାଫଳ ଶୁଣିବା ପାଇଁ ଦବାନ୍ତୁ",
        testsSectionHeading: "ପରୀକ୍ଷା ଫଳାଫଳ",
        hospitalTitle: "ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ",
        hospitalAdvice: "ନିକଟସ୍ଥ ସ୍ୱାସ୍ଥ୍ୟକେନ୍ଦ୍ର ମାନଚିତ୍ର ଦେଖନ୍ତୁ",
        hospitalActionText: "ନିକଟସ୍ଥ ଡାକ୍ତରଖାନା ଖୋଜନ୍ତୁ",
        askSectionTitle: "କୌଣସି ପ୍ରଶ୍ନ ଅଛି?",
        askSectionSub: "ମାଇକ୍ ଦବାଇ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ",
        heroMicCaption: "କହି ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ",
        heroMicHint: "ମାତୃଭାଷାରେ ଉତ୍ତର ଶୁଣନ୍ତୁ",
        heroMicRecording: "ଶୁଣୁଛି... କୁହନ୍ତୁ",
        heroMicThinking: "ସଖୀ ଭାବୁଛି...",
        replayBtnLabel: "ଶୁଣନ୍ତୁ",
        retakeTitle: "ଫଟୋ ସ୍ପଷ୍ଟ ନୁହେଁ",
        retakeDesc: "ରିପୋର୍ଟ ସ୍ପଷ୍ଟ ପଢ଼ାଯାଉନାହିଁ। ଦୟାକରି ପୁଣି ଥରେ ସ୍ପଷ୍ଟ ଫଟୋ ଉଠାନ୍ତୁ।",
        btnRetakeLabel: "ପୁଣି ଫଟୋ ଉଠାନ୍ତୁ",
        btnCancelRetakeLabel: "ବନ୍ଦ କରନ୍ତୁ",
        askPlaceholder: "ଯଥା: ମୋର ଶୁଗାର୍ ଅଧିକ ଅଛି କି?",
        sendBtnText: "ପଚାରନ୍ତୁ"
    },
    as: {
        brandTagline: "আপোনাৰ স্বাস্থ্য সখী",
        simpleModeText: "সহজ মোড",
        simpleModeSub: "ডাঙৰ আখৰ আৰু কণ্ঠ",
        langSectionTitle: "ভাষা বাছক",
        langSectionHint: "মাতৃভাষাত ৰিপ'ৰ্ট শুনক",
        scanHeading: "লেব ৰিপ'ৰ্ট স্কেন কৰক",
        scanSubheading: "তেজ বা চেনিৰ ৰিপ'ৰ্টৰ স্পষ্ট ফটো তোলক",
        scanBtnLabel: "ৰিপ'ৰ্ট স্কেন কৰক",
        scanBtnSub: "কেমেৰা বা গেলেৰী",
        demoSampleText: "নমুনা ৰিপ'ৰ্ট চাওক (CBC + Sugar)",
        hl1: "সুৰক্ষিত চিকিৎসা সীমা",
        hl2: "ভয়েচ ব্যাখ্যা",
        hl3: "ওচৰৰ চিকিৎসালয়",
        loadingTitle: "ৰিপ'ৰ্ট পঢ়া হৈছে...",
        loadingStep: "তথ্য আহৰণ কৰা হৈছে",
        backBtnText: "নতুন স্কেন",
        listenButtonLabel: "ব্যাখ্যা শুনক",
        listenButtonHint: "অসমীয়াত শুনক",
        attachedListenMain: "ৰিপ'ৰ্ট শুনক",
        attachedListenSub: "সকলো ফলাফল কণ্ঠত শুনিবলৈ টিপক",
        testsSectionHeading: "পৰীক্ষাৰ ফলাফল",
        hospitalTitle: "চিকিৎসকৰ পৰামৰ্শ লওক",
        hospitalAdvice: "ওচৰৰ কেন্দ্ৰৰ মানচিত্ৰ চাওক",
        hospitalActionText: "ওচৰৰ চিকিৎসালয় বিচাৰক",
        askSectionTitle: "কিবা প্ৰশ্ন আছে নেকি?",
        askSectionSub: "মাইকত টিপি প্ৰশ্ন সোধক",
        heroMicCaption: "কৈ প্ৰশ্ন সোধক",
        heroMicHint: "মাতৃভাষাত উত্তৰ শুনক",
        heroMicRecording: "শুনি আছোঁ... কওক",
        heroMicThinking: "সখীয়ে চিন্তা কৰিছে...",
        replayBtnLabel: "শুনক",
        retakeTitle: "ফটো স্পষ্ট নহয়",
        retakeDesc: "ৰিপ'ৰ্টৰ তথ্য স্পষ্টকৈ পঢ়িব পৰা নাই। অনুগ্ৰহ কৰি আকৌ স্পষ্ট ফটো তোলক।",
        btnRetakeLabel: "আকৌ ফটো তোলক",
        btnCancelRetakeLabel: "বন্ধ কৰক",
        askPlaceholder: "উদাহৰণ: মোৰ চেনিৰ মাত্ৰা বেছি নেকি?",
        sendBtnText: "সোধক"
    },
    ur: {
        brandTagline: "آپ کی صحت کی سہیلی",
        simpleModeText: "آسان موڈ",
        simpleModeSub: "بڑے حروف اور آواز",
        langSectionTitle: "اپنی زبان منتخب کریں",
        langSectionHint: "اپنی مادری زبان میں رپورٹ سنیں",
        scanHeading: "لیب رپورٹ اسکین کریں",
        scanSubheading: "بلڈ یا شوگر رپورٹ کی صاف تصویر لیں",
        scanBtnLabel: "رپورٹ اسکین کریں",
        scanBtnSub: "کیمرہ یا گیلری",
        demoSampleText: "نمونہ رپورٹ دیکھیں (CBC + Sugar)",
        hl1: "محفوظ طبی حدود",
        hl2: "صوتی وضاحت",
        hl3: "قریبی ہسپتال",
        loadingTitle: "رپورٹ پڑھی جا رہی ہے...",
        loadingStep: "نتائج نکالے جا رہے ہیں",
        backBtnText: "نیا اسکین",
        listenButtonLabel: "وضاحت سنیں",
        listenButtonHint: "اردو میں سنیں",
        attachedListenMain: "رپورٹ سنیں",
        attachedListenSub: "تمام نتائج آواز میں سننے کے لیے دبائیں",
        testsSectionHeading: "ٹیسٹ کے نتائج اور صورتحال",
        hospitalTitle: "ڈاکٹر سے مشورہ کریں",
        hospitalAdvice: "قریبی مراکز کے لیے نقشہ کھولیں",
        hospitalActionText: "قریبی ہسپتال تلاش کریں",
        askSectionTitle: "کوئی سوال ہے؟",
        askSectionSub: "مائیک دبا کر سوال پوچھیں",
        heroMicCaption: "بول کر سوال پوچھیں",
        heroMicHint: "مادری زبان میں جواب سنیں",
        heroMicRecording: "سن رہے ہیں... بولیں",
        heroMicThinking: "سخی سوچ رہی ہے...",
        replayBtnLabel: "سنیں",
        retakeTitle: "تصویر صاف نہیں ہے",
        retakeDesc: "رپورٹ کے اعداد و شمار واضح نہیں ہیں۔ برائے مہربانی دوبارہ صاف تصویر لیں۔",
        btnRetakeLabel: "دوبارہ تصویر لیں",
        btnCancelRetakeLabel: "بند کریں",
        askPlaceholder: "مثلاً: کیا میری شوگر زیادہ ہے؟",
        sendBtnText: "پوچھیں"
    },
    en: {
        brandTagline: "Your AI health friend",
        simpleModeText: "Simple Mode",
        simpleModeSub: "Large icons & audio",
        langSectionTitle: "Choose Your Language",
        langSectionHint: "Tap to hear explanations in your mother tongue",
        scanHeading: "Scan Your Lab Report",
        scanSubheading: "Take a clear photo of blood, sugar, or urine test results",
        scanBtnLabel: "SCAN REPORT",
        scanBtnSub: "Camera or Gallery",
        demoSampleText: "Or Try Sample Report (CBC + Sugar)",
        hl1: "Safe Medical Ranges",
        hl2: "Spoken Voice Advice",
        hl3: "Nearest Hospital Finder",
        loadingTitle: "Reading Lab Report...",
        loadingStep: "Reader Agent extracting values",
        backBtnText: "New Scan",
        listenButtonLabel: "Listen to Explanation",
        listenButtonHint: "Spoken in your language",
        attachedListenMain: "LISTEN TO RESULTS",
        attachedListenSub: "Tap to hear all results explained by voice",
        testsSectionHeading: "Report Values & Safety Check",
        hospitalTitle: "Consult a Doctor Nearby",
        hospitalAdvice: "One tap opens map directions to health centers",
        hospitalActionText: "Find Nearest Clinic or Hospital",
        askSectionTitle: "Have a question?",
        askSectionSub: "Tap the mic to ask anything about your report",
        heroMicCaption: "Tap to Speak Your Question",
        heroMicHint: "Spoken answers in your mother tongue",
        heroMicRecording: "Listening... Speak now",
        heroMicThinking: "Sakhi is thinking...",
        replayBtnLabel: "Listen",
        retakeTitle: "Photo Is Blurry",
        retakeDesc: "We cannot clearly read the numbers on this report. For your medical safety, we do not guess lab test results. Please retake the photo with good lighting and steady focus.",
        btnRetakeLabel: "Retake Photo",
        btnCancelRetakeLabel: "Close",
        askPlaceholder: "e.g. Is my sugar high?",
        sendBtnText: "Ask"
    }
};

class ReportSakhiApp {
    constructor() {
        this.currentLang = localStorage.getItem("reportSakhi_lang") || "ml";
        this.simpleMode = localStorage.getItem("reportSakhi_simple") === "true";
        this.isSpeaking = false;
        this.isRecordingAudio = false;
        this.currentSpeechScript = "";
        this.currentAudioBase64 = null;
        this.currentAudioFormat = "audio/wav";
        this.currentReportContext = "";
        this.lastAnswerText = "";
        this.lastAnswerAudioBase64 = null;
        this.lastAnswerAudioFormat = "audio/wav";
        this.audioElement = null;
        this.mediaRecorder = null;
        this.audioChunks = [];

        this.initElements();
        this.bindEvents();
        this.applyLanguage(this.currentLang);
        this.applySimpleMode(this.simpleMode);
    }

    initElements() {
        // Views
        this.mainHomeView = document.getElementById("mainHomeView");
        this.loadingOverlay = document.getElementById("loadingOverlay");
        this.resultsContainer = document.getElementById("resultsContainer");

        // Controls
        this.simpleModeToggle = document.getElementById("simpleModeToggle");
        this.langButtons = document.querySelectorAll(".lang-btn");
        this.fileInput = document.getElementById("reportFileInput");
        this.btnScanMain = document.getElementById("btnScanMain");
        this.btnDemoSample = document.getElementById("btnDemoSample");
        this.btnBackHome = document.getElementById("btnBackHome");

        // Audio Listen Buttons
        this.btnListenAudio = document.getElementById("btnListenAudio");
        this.listenIcon = document.getElementById("listenIcon");
        this.btnAttachedListen = document.getElementById("btnAttachedListen");
        this.attachedListenIcon = document.getElementById("attachedListenIcon");
        this.attachedAudioWaves = document.getElementById("attachedAudioWaves");

        // Results Content
        this.testsGrid = document.getElementById("testsGrid");
        this.hospitalFinderSection = document.getElementById("hospitalFinderSection");
        this.helpUrgencyBadge = document.getElementById("helpUrgencyBadge");
        this.hospitalTitle = document.getElementById("hospitalTitle");
        this.hospitalAdvice = document.getElementById("hospitalAdvice");
        this.btnOpenHospitalMap = document.getElementById("btnOpenHospitalMap");
        this.hospitalActionText = document.getElementById("hospitalActionText");

        this.explanationHeadline = document.getElementById("explanationHeadline");
        this.explanationText = document.getElementById("explanationText");
        this.safetyLineText = document.getElementById("safetyLineText");
        this.urgencyPill = document.getElementById("urgencyPill");
        this.urgencyPillText = document.getElementById("urgencyPillText");

        // Hero Voice Mic Elements
        this.btnHeroMic = document.getElementById("btnHeroMic");
        this.heroMicIcon = document.getElementById("heroMicIcon");
        this.heroMicCaption = document.getElementById("heroMicCaption");
        this.heroMicHint = document.getElementById("heroMicHint");

        // Fallback Q&A Elements
        this.askTextInput = document.getElementById("askTextInput");
        this.btnSendQuestion = document.getElementById("btnSendQuestion");
        this.askReplyBox = document.getElementById("askReplyBox");
        this.userQuestionEcho = document.getElementById("userQuestionEcho");
        this.echoText = document.getElementById("echoText");
        this.askReplyText = document.getElementById("askReplyText");
        this.btnReplayAudio = document.getElementById("btnReplayAudio");
        this.replayBtnLabel = document.getElementById("replayBtnLabel");

        // Retake Modal Elements
        this.retakeModal = document.getElementById("retakeModal");
        this.retakeModalTitle = document.getElementById("retakeModalTitle");
        this.retakeModalDesc = document.getElementById("retakeModalDesc");
        this.btnRetakePhoto = document.getElementById("btnRetakePhoto");
        this.btnDismissRetake = document.getElementById("btnDismissRetake");
        this.btnRetakeLabel = document.getElementById("btnRetakeLabel");
        this.btnCancelRetakeLabel = document.getElementById("btnCancelRetakeLabel");
    }

    bindEvents() {
        // Language Buttons
        this.langButtons.forEach(btn => {
            btn.addEventListener("click", () => {
                const lang = btn.dataset.lang;
                this.setLanguage(lang);
            });
        });

        // Simple Mode Toggle
        this.simpleModeToggle.addEventListener("change", (e) => {
            this.setSimpleMode(e.target.checked);
        });

        // Scan Buttons
        this.btnScanMain.addEventListener("click", () => {
            this.fileInput.click();
        });

        this.fileInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                this.fileInput.value = "";
                this.processScan(file);
            }
        });

        this.btnDemoSample.addEventListener("click", () => {
            this.processScan(null); // Runs demo payload
        });

        // Navigation
        this.btnBackHome.addEventListener("click", () => {
            this.stopSpeaking();
            this.stopAudioRecording();
            this.resultsContainer.style.display = "none";
            this.mainHomeView.style.display = "flex";
        });

        // Audio Listen Buttons
        this.btnListenAudio.addEventListener("click", () => {
            this.toggleListenAudio();
        });

        if (this.btnAttachedListen) {
            this.btnAttachedListen.addEventListener("click", () => {
                this.toggleListenAudio();
            });
        }

        // Hero Voice Mic Button
        if (this.btnHeroMic) {
            this.btnHeroMic.addEventListener("click", () => {
                this.toggleHeroMic();
            });
        }

        // Replay Answer Audio Button
        if (this.btnReplayAudio) {
            this.btnReplayAudio.addEventListener("click", () => {
                this.replayLastAnswer();
            });
        }

        // Text Ask Q&A
        this.btnSendQuestion.addEventListener("click", () => {
            const query = this.askTextInput.value.trim();
            if (query) this.submitQuestion(query);
        });

        this.askTextInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                const query = this.askTextInput.value.trim();
                if (query) this.submitQuestion(query);
            }
        });

        // Retake Modal Actions
        if (this.btnRetakePhoto) {
            this.btnRetakePhoto.addEventListener("click", () => {
                if (this.retakeModal) this.retakeModal.style.display = "none";
                this.mainHomeView.style.display = "flex";
                this.fileInput.click();
            });
        }

        if (this.btnDismissRetake) {
            this.btnDismissRetake.addEventListener("click", () => {
                if (this.retakeModal) this.retakeModal.style.display = "none";
                this.mainHomeView.style.display = "flex";
            });
        }
    }

    getTestIcon(test) {
        const key = (test.rule_key || "").toLowerCase();
        const name = (test.canonical_name || test.test_name || "").toLowerCase();
        if (key.includes("hemoglobin") || name.includes("hemoglobin") || name.includes("haemoglobin") || name.includes("hb")) return "🩸";
        if (key.includes("fasting") || name.includes("fasting") || name.includes("fbs")) return "🍬";
        if (key.includes("post_prandial") || name.includes("ppbs") || name.includes("post prandial") || name.includes("pp")) return "🍚";
        if (key.includes("hba1c") || name.includes("hba1c")) return "📊";
        if (key.includes("wbc") || name.includes("wbc") || name.includes("leukocyte") || name.includes("tlc")) return "🛡️";
        if (key.includes("platelet") || name.includes("platelet") || name.includes("plt")) return "🩹";
        if (key.includes("tsh") || name.includes("thyroid") || name.includes("tsh")) return "⚡";
        if (key.includes("creatinine") || name.includes("creatinine")) return "💧";
        if (key.includes("cholesterol") || name.includes("cholesterol") || name.includes("lipid")) return "🫀";
        return "🧪";
    }

    getStatusIcon(color) {
        if (color === "red") return "🚨";
        if (color === "yellow") return "⚠️";
        return "✅";
    }

    setLanguage(lang) {
        this.currentLang = lang;
        localStorage.setItem("reportSakhi_lang", lang);
        this.applyLanguage(lang);
    }

    applyLanguage(lang) {
        this.langButtons.forEach(b => {
            const isActive = b.dataset.lang === lang;
            b.classList.toggle("active", isActive);
            b.setAttribute("aria-checked", isActive);
        });

        const dict = I18N[lang] || I18N.en;
        for (const [id, text] of Object.entries(dict)) {
            const el = document.getElementById(id);
            if (el) {
                if (el.tagName === "INPUT") {
                    el.placeholder = text;
                } else {
                    el.innerText = text;
                }
            }
        }
    }

    setSimpleMode(enabled) {
        this.simpleMode = enabled;
        localStorage.setItem("reportSakhi_simple", enabled);
        this.applySimpleMode(enabled);
    }

    applySimpleMode(enabled) {
        this.simpleModeToggle.checked = enabled;
        this.simpleModeToggle.setAttribute("aria-checked", enabled ? "true" : "false");
        if (enabled) {
            document.body.classList.add("simple-mode");
            if (this.resultsContainer.style.display === "flex" && this.currentSpeechScript && !this.isSpeaking) {
                setTimeout(() => {
                    this.speakText(this.currentSpeechScript, this.currentAudioBase64, this.currentAudioFormat);
                }, 300);
            }
        } else {
            document.body.classList.remove("simple-mode");
        }
    }

    async processScan(file) {
        this.mainHomeView.style.display = "none";
        this.loadingOverlay.style.display = "flex";
        this.resultsContainer.style.display = "none";

        const formData = new FormData();
        if (file) {
            formData.append("file", file);
        }
        formData.append("language", this.currentLang);
        formData.append("simple_mode", this.simpleMode);

        try {
            const response = await fetch("/api/scan", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            this.loadingOverlay.style.display = "none";

            if (data.status === "retake_required") {
                this.showRetakeModal(data.message);
                return;
            }

            this.renderResults(data);
        } catch (error) {
            console.error("Scan error:", error);
            this.loadingOverlay.style.display = "none";
            this.showRetakeModal("Could not read report clearly. Please retake a well-lit photo of the lab report.");
        }
    }

    showRetakeModal(customMessage) {
        const dict = I18N[this.currentLang] || I18N.en;
        this.loadingOverlay.style.display = "none";
        this.resultsContainer.style.display = "none";
        this.mainHomeView.style.display = "flex";

        if (this.retakeModal) {
            this.retakeModal.style.display = "flex";
            if (this.retakeModalTitle) {
                this.retakeModalTitle.innerText = dict.retakeTitle || "Photo Is Blurry";
            }
            if (this.retakeModalDesc) {
                this.retakeModalDesc.innerText = customMessage || dict.retakeDesc || "We cannot clearly read the numbers on this report. For your medical safety, we do not guess lab test results. Please retake the photo with good lighting and steady focus.";
            }
            if (this.btnRetakeLabel && dict.btnRetakeLabel) {
                this.btnRetakeLabel.innerText = dict.btnRetakeLabel;
            }
            if (this.btnCancelRetakeLabel && dict.btnCancelRetakeLabel) {
                this.btnCancelRetakeLabel.innerText = dict.btnCancelRetakeLabel;
            }
        }
    }

    renderResults(data) {
        this.resultsContainer.style.display = "flex";

        const checker = data.checker || {};
        const explainer = data.explainer || {};
        const voice = data.voice || {};
        const overallStatus = checker.overall_status || "green";

        // Store context for Explainer Agent Q&A
        this.currentReportContext = JSON.stringify(checker.items || []);

        // Store synthesized audio
        this.currentAudioBase64 = voice.audio_base64 || null;
        this.currentAudioFormat = voice.audio_format || "audio/wav";

        // Urgency pill
        this.urgencyPill.className = `urgency-pill urgency-${overallStatus}`;
        const statusMap = {
            green: { en: "Normal", hi: "सामान्य", ml: "സാധാരണ", ta: "இயல்பானது" },
            yellow: { en: "Consult Doctor", hi: "डॉक्टर से मिलें", ml: "ഡോക്ടറെ കാണുക", ta: "ஆலோசனை பெறுக" },
            red: { en: "Needs Attention", hi: "तुरंत ध्यान दें", ml: "അടിയന്തിരം", ta: "கவனம் தேவை" }
        };
        this.urgencyPillText.innerText = (statusMap[overallStatus] && statusMap[overallStatus][this.currentLang]) || overallStatus.toUpperCase();

        // Summary and Safety Line
        this.explanationHeadline.innerText = explainer.headline || "Report Overview";
        this.explanationText.innerText = explainer.summary_text || "";
        this.safetyLineText.innerText = explainer.safety_line || I18N[this.currentLang]?.safetyLineText || "This explains your report. It is not a diagnosis. Please consult a doctor.";
        this.currentSpeechScript = explainer.full_speech_script || explainer.summary_text || "";

        // Tests Grid
        this.testsGrid.innerHTML = "";
        const items = checker.items || [];
        items.forEach((test, idx) => {
            const card = document.createElement("div");
            const color = test.color || "green";
            card.className = `test-item-card color-${color}`;
            
            const desc = (test.description && test.description[this.currentLang]) || "";
            const normFormatted = test.normal_range ? test.normal_range.formatted : "";
            const testIcon = this.getTestIcon(test);
            const statusIcon = this.getStatusIcon(color);
            const statusLabel = test.status_label || (color === "red" ? "URGENT" : (color === "yellow" ? "WATCH" : "NORMAL"));

            card.innerHTML = `
                <div class="test-card-main">
                    <div class="test-icon-badge" aria-hidden="true">${testIcon}</div>
                    <div class="test-meta">
                        <span class="test-title">${test.canonical_name || test.test_name}</span>
                        <div class="test-status-pill pill-${color}">
                            <span class="status-symbol" aria-hidden="true">${statusIcon}</span>
                            <span class="status-name">${statusLabel}</span>
                        </div>
                    </div>
                    <div class="test-val-container">
                        <span class="test-val-badge">${test.value}</span>
                        <span class="test-unit-badge">${test.unit}</span>
                    </div>
                    <button type="button" class="btn-card-listen" data-card-idx="${idx}" aria-label="Listen to this test">🔊</button>
                </div>
                <div class="test-row-details">
                    ${desc ? `<p class="test-desc">${desc}</p>` : ''}
                    <div class="test-row-sub">
                        <span class="test-normal-range">Normal: ${normFormatted}</span>
                    </div>
                </div>
            `;

            const miniBtn = card.querySelector(".btn-card-listen");
            if (miniBtn) {
                miniBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    this.speakTestCard(test, miniBtn);
                });
            }

            this.testsGrid.appendChild(card);
        });

        // Hospital / Nearby Help: Triggered if ANY result is Red or Yellow via MCP tool
        if (overallStatus === "red" || overallStatus === "yellow") {
            this.hospitalFinderSection.style.display = "block";
            this.hospitalFinderSection.className = `card hospital-finder-card urgency-${overallStatus}`;
            this.fetchNearbyHelp(overallStatus);
        } else {
            this.hospitalFinderSection.style.display = "none";
        }

        // Auto-play audio if Simple Mode is active
        if (this.simpleMode) {
            setTimeout(() => {
                this.speakText(this.currentSpeechScript, this.currentAudioBase64, this.currentAudioFormat);
            }, 400);
        }
    }

    // -------------------------------------------------------------
    // MCP Server: find_nearby_help Integration
    // -------------------------------------------------------------
    async fetchNearbyHelp(urgency) {
        const executeFetch = async (lat = null, lng = null) => {
            try {
                let url = `/api/help/nearby?urgency=${encodeURIComponent(urgency)}&language=${encodeURIComponent(this.currentLang)}`;
                if (lat !== null && lng !== null) {
                    url += `&latitude=${lat}&longitude=${lng}`;
                }
                const res = await fetch(url);
                const data = await res.json();

                if (this.btnOpenHospitalMap) {
                    this.btnOpenHospitalMap.href = data.map_url || "https://www.google.com/maps/search/hospitals+near+me";
                }
                if (this.hospitalTitle && data.title) {
                    this.hospitalTitle.innerText = data.title;
                }
                if (this.hospitalAdvice && data.advice) {
                    this.hospitalAdvice.innerText = data.advice;
                }
                if (this.helpUrgencyBadge) {
                    this.helpUrgencyBadge.innerText = (data.urgency === "red") ? "URGENT ATTENTION" : "CONSULT DOCTOR";
                }
            } catch (err) {
                console.warn("Failed to fetch nearby help from MCP tool:", err);
            }
        };

        // Try getting geolocation for accurate turn-by-turn map directions
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => executeFetch(pos.coords.latitude, pos.coords.longitude),
                () => executeFetch(),
                { timeout: 3500 }
            );
        } else {
            executeFetch();
        }
    }

    // -------------------------------------------------------------
    // Voice Audio Playback
    // -------------------------------------------------------------
    toggleListenAudio() {
        if (this.isSpeaking) {
            this.stopSpeaking();
        } else {
            this.speakText(this.currentSpeechScript, this.currentAudioBase64, this.currentAudioFormat);
        }
    }

    setSpeakingState(speaking) {
        this.isSpeaking = speaking;
        const iconChar = speaking ? "⏸️" : "🔊";

        if (this.listenIcon) this.listenIcon.innerText = iconChar;
        if (this.attachedListenIcon) this.attachedListenIcon.innerText = iconChar;

        if (this.btnAttachedListen) {
            this.btnAttachedListen.classList.toggle("speaking", speaking);
            this.btnAttachedListen.setAttribute("aria-pressed", speaking ? "true" : "false");
        }
        if (this.btnListenAudio) {
            this.btnListenAudio.classList.toggle("speaking", speaking);
            this.btnListenAudio.setAttribute("aria-pressed", speaking ? "true" : "false");
        }
    }

    speakText(text, audioBase64 = null, format = "audio/wav") {
        if (!text && !audioBase64) return;
        this.stopSpeaking();

        // 1. Play server audio if provided (Bhashini / Sarvam / Google / Azure)
        if (audioBase64) {
            try {
                this.audioElement = new Audio(`data:${format};base64,${audioBase64}`);
                this.audioElement.onplay = () => this.setSpeakingState(true);
                this.audioElement.onended = () => this.setSpeakingState(false);
                this.audioElement.onerror = () => {
                    console.warn("Server audio playback failed, falling back to Web Speech synthesis.");
                    this.speakViaWebSpeech(text);
                };
                this.audioElement.play();
                return;
            } catch (err) {
                console.warn("Audio element error:", err);
            }
        }

        // 2. Client Web Speech API fallback
        this.speakViaWebSpeech(text);
    }

    speakViaWebSpeech(text) {
        if (!('speechSynthesis' in window)) return;

        const utterance = new SpeechSynthesisUtterance(text);
        const langCodes = {
            ml: "ml-IN", hi: "hi-IN", ta: "ta-IN", te: "te-IN",
            kn: "kn-IN", bn: "bn-IN", mr: "mr-IN", gu: "gu-IN",
            pa: "pa-IN", or: "or-IN", as: "as-IN", ur: "ur-IN", en: "en-IN"
        };
        utterance.lang = langCodes[this.currentLang] || "en-IN";
        utterance.rate = 0.95;

        utterance.onstart = () => this.setSpeakingState(true);
        utterance.onend = utterance.onerror = () => this.setSpeakingState(false);

        window.speechSynthesis.speak(utterance);
    }

    speakTestCard(test, btnElement) {
        const name = test.canonical_name || test.test_name;
        const val = `${test.value} ${test.unit}`;
        const status = test.status_label || test.color;

        let script = "";
        if (this.currentLang === "ml") {
            script = `${name}: അളവ് ${val}. നില: ${status}.`;
        } else if (this.currentLang === "hi") {
            script = `${name}: मान ${val}. स्थिति: ${status}.`;
        } else if (this.currentLang === "ta") {
            script = `${name}: அளவு ${val}. நிலை: ${status}.`;
        } else {
            script = `${name} is ${val}. Status is ${status}.`;
        }

        if (btnElement) {
            btnElement.classList.add("speaking");
            setTimeout(() => btnElement.classList.remove("speaking"), 2500);
        }

        this.speakText(script);
    }

    stopSpeaking() {
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement = null;
        }
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        this.setSpeakingState(false);
        document.querySelectorAll(".btn-card-listen.speaking").forEach(b => b.classList.remove("speaking"));
    }

    // -------------------------------------------------------------
    // Hero Microphone Voice Q&A Loop
    // -------------------------------------------------------------
    toggleHeroMic() {
        if (this.isRecordingAudio) {
            this.stopAudioRecording();
        } else {
            this.startAudioRecording();
        }
    }

    async startAudioRecording() {
        const dict = I18N[this.currentLang] || I18N.en;

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            // Older browser fallback: Web Speech API recognition
            this.toggleSpeechRecognition();
            return;
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.audioChunks = [];
            
            // Choose supported audio mime type
            let mimeType = "audio/webm";
            if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
                mimeType = "audio/webm;codecs=opus";
            } else if (MediaRecorder.isTypeSupported("audio/mp4")) {
                mimeType = "audio/mp4";
            } else if (MediaRecorder.isTypeSupported("audio/wav")) {
                mimeType = "audio/wav";
            }

            this.mediaRecorder = new MediaRecorder(stream, { mimeType });
            this.mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) {
                    this.audioChunks.push(e.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: mimeType });
                // Stop audio tracks
                stream.getTracks().forEach(track => track.stop());
                this.submitVoiceQuestion(audioBlob);
            };

            this.mediaRecorder.start();
            this.isRecordingAudio = true;

            // UI Recording State
            this.btnHeroMic.classList.add("recording");
            this.heroMicIcon.innerText = "⏹️";
            this.heroMicCaption.innerText = dict.heroMicRecording || "Listening... Speak now";
        } catch (err) {
            console.warn("Microphone access failed, falling back to Web Speech recognition:", err);
            this.toggleSpeechRecognition();
        }
    }

    stopAudioRecording() {
        if (this.mediaRecorder && this.isRecordingAudio) {
            this.isRecordingAudio = false;
            const dict = I18N[this.currentLang] || I18N.en;

            this.btnHeroMic.classList.remove("recording");
            this.btnHeroMic.classList.add("thinking");
            this.heroMicIcon.innerText = "⏳";
            this.heroMicCaption.innerText = dict.heroMicThinking || "Sakhi is thinking...";

            this.mediaRecorder.stop();
        }
    }

    async submitVoiceQuestion(audioBlob) {
        const dict = I18N[this.currentLang] || I18N.en;
        const formData = new FormData();
        formData.append("file", audioBlob, "question_audio.webm");
        formData.append("language", this.currentLang);
        if (this.currentReportContext) {
            formData.append("context", this.currentReportContext);
        }

        this.askReplyBox.style.display = "block";
        this.askReplyText.innerText = dict.heroMicThinking || "Thinking...";

        try {
            const res = await fetch("/api/voice/ask", {
                method: "POST",
                body: formData
            });
            const data = await res.json();

            // Reset Hero Mic State
            this.btnHeroMic.classList.remove("thinking");
            this.heroMicIcon.innerText = "🎙️";
            this.heroMicCaption.innerText = dict.heroMicCaption || "Tap to Speak Your Question";

            // Show Question Echo & Answer
            if (data.question) {
                this.userQuestionEcho.style.display = "block";
                this.echoText.innerText = data.question;
            } else {
                this.userQuestionEcho.style.display = "none";
            }
            this.askReplyText.innerText = data.answer;

            // Cache for Replay
            this.lastAnswerText = data.answer;
            this.lastAnswerAudioBase64 = data.audio_base64 || null;
            this.lastAnswerAudioFormat = data.audio_format || "audio/wav";

            // Automatically play speech response aloud!
            this.speakText(data.answer, data.audio_base64, data.audio_format);
        } catch (err) {
            console.error("Voice question error:", err);
            this.btnHeroMic.classList.remove("thinking");
            this.heroMicIcon.innerText = "🎙️";
            this.heroMicCaption.innerText = dict.heroMicCaption || "Tap to Speak Your Question";
            this.askReplyText.innerText = "Error answering question. Please try again.";
        }
    }

    async submitQuestion(query) {
        const dict = I18N[this.currentLang] || I18N.en;
        const formData = new FormData();
        formData.append("question", query);
        formData.append("language", this.currentLang);
        if (this.currentReportContext) {
            formData.append("context", this.currentReportContext);
        }

        this.askTextInput.value = "";
        this.askReplyBox.style.display = "block";
        this.userQuestionEcho.style.display = "block";
        this.echoText.innerText = query;
        this.askReplyText.innerText = dict.heroMicThinking || "Thinking...";

        try {
            const res = await fetch("/api/ask", {
                method: "POST",
                body: formData
            });
            const data = await res.json();
            this.askReplyText.innerText = data.answer;

            this.lastAnswerText = data.answer;
            this.lastAnswerAudioBase64 = data.audio_base64 || null;
            this.lastAnswerAudioFormat = data.audio_format || "audio/wav";

            this.speakText(data.answer, data.audio_base64, data.audio_format);
        } catch (e) {
            this.askReplyText.innerText = "Error answering question.";
        }
    }

    replayLastAnswer() {
        if (this.lastAnswerText || this.lastAnswerAudioBase64) {
            this.speakText(this.lastAnswerText, this.lastAnswerAudioBase64, this.lastAnswerAudioFormat);
        }
    }

    // Client speech recognition fallback
    toggleSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Please type your question or use a browser with microphone support.");
            return;
        }

        const dict = I18N[this.currentLang] || I18N.en;
        const recognition = new SpeechRecognition();
        const langCodes = {
            ml: "ml-IN", hi: "hi-IN", ta: "ta-IN", te: "te-IN",
            kn: "kn-IN", bn: "bn-IN", mr: "mr-IN", gu: "gu-IN",
            pa: "pa-IN", or: "or-IN", as: "as-IN", ur: "ur-IN", en: "en-IN"
        };
        recognition.lang = langCodes[this.currentLang] || "en-IN";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            this.btnHeroMic.classList.add("recording");
            this.heroMicIcon.innerText = "⏹️";
            this.heroMicCaption.innerText = dict.heroMicRecording || "Listening...";
        };

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            this.submitQuestion(text);
        };

        recognition.onerror = recognition.onend = () => {
            this.btnHeroMic.classList.remove("recording");
            this.heroMicIcon.innerText = "🎙️";
            this.heroMicCaption.innerText = dict.heroMicCaption || "Tap to Speak Your Question";
        };

        recognition.start();
    }
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    window.reportSakhi = new ReportSakhiApp();
});
