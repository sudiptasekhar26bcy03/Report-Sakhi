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
        scanHeading: "ലാബ് റിപ്പോർട്ട് സമർപ്പിക്കുക",
        scanSubheading: "മൾട്ടി-പേജ് PDF അല്ലെങ്കിൽ വ്യക്തമായ ഫോട്ടോകൾ നൽകാം",
        scanBtnLabel: "ലാബ് റിപ്പോർട്ട് സമർപ്പിക്കുക",
        scanBtnSub: "PDF അല്ലെങ്കിൽ ഫോട്ടോകൾ (മൾട്ടി-പേജ്)",
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
        sendBtnText: "ചോദിക്കൂ",
        trendTitle: "ആരോഗ്യ പുരോഗതിയും മാറ്റങ്ങളും",
        trendSubtitle: "കഴിഞ്ഞ പരിശോധനയുമായുള്ള താരതമ്യം",
        historyModalTitle: "റിപ്പോർട്ട് ചരിത്രം",
        clearHistoryLabel: "ചരിത്രം മായ്ക്കുക",
        demoFollowupText: "തുടർ പരിശോധന കാണുക (മാറ്റങ്ങൾ നിരീക്ഷിക്കാം)",
        demoPdfText: "മൾട്ടി-പേജ് PDF റിപ്പോർട്ട് (2 പേജുകൾ)"
    },
    hi: {
        brandTagline: "आपकी सेहत की सच्ची सखी",
        simpleModeText: "सरल मोड",
        simpleModeSub: "बड़े अक्षर और आवाज़",
        langSectionTitle: "अपनी भाषा चुनें",
        langSectionHint: "अपनी भाषा में रिपोर्ट की व्याख्या सुनें",
        scanHeading: "लैब रिपोर्ट अपलोड या स्कैन करें",
        scanSubheading: "मल्टी-पेज PDF या जांच रिपोर्ट के साफ़ फ़ोटो दें",
        scanBtnLabel: "लैब रिपोर्ट अपलोड करें",
        scanBtnSub: "PDF या फ़ोटो (मल्टी-पेज समर्थित)",
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
        sendBtnText: "पूछें",
        trendTitle: "प्रगति और बदलाव ट्रैकर",
        trendSubtitle: "पिछली जांच रिपोर्ट से तुलना",
        historyModalTitle: "रिपोर्ट इतिहास",
        clearHistoryLabel: "इतिहास हटाएं",
        demoFollowupText: "फॉलो-अप रिपोर्ट देखें (ट्रेंड ट्रैकर)",
        demoPdfText: "मल्टी-पेज PDF रिपोर्ट देखें (2 पेज)"
    },
    ta: {
        brandTagline: "உங்கள் மருத்துவத் தோழி",
        simpleModeText: "எளிய முறை",
        simpleModeSub: "பெரிய எழுத்துகள் & குரல்",
        langSectionTitle: "மொழியைத் தேர்ந்தெடுக்கவும்",
        langSectionHint: "உங்கள் சொந்த மொழியில் விளக்கத்தைக் கேளுங்கள்",
        scanHeading: "ஆய்வக அறிக்கையைப் பதிவேற்றவும்",
        scanSubheading: "பல பக்க PDF அல்லது தெளிவான புகைப்படங்களை வழங்கவும்",
        scanBtnLabel: "அறிக்கையைப் பதிவேற்றவும்",
        scanBtnSub: "PDF அல்லது புகைப்படங்கள் (பல பக்கங்கள்)",
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
        sendBtnText: "கேட்க",
        trendTitle: "முன்னேற்றப் போக்கு கண்காணிப்பு",
        trendSubtitle: "முந்தைய அறிக்கையுடன் ஒப்பீடு",
        historyModalTitle: "அறிக்கை வரலாறு",
        clearHistoryLabel: "வரலாற்றை அழி",
        demoFollowupText: "அடுத்த பரிசோதனை காண்க (போக்கை அறிய)",
        demoPdfText: "பல பக்க PDF அறிக்கை காண்க (2 பக்கங்கள்)"
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
        sendBtnText: "అడగండి",
        trendTitle: "ఆరోగ్య పురోగతి & మార్పులు",
        trendSubtitle: "మునుపటి పరీక్షలతో పోలిక",
        historyModalTitle: "రిపోర్టు చరిత్ర",
        clearHistoryLabel: "చరిత్రను తొలగించండి",
        demoFollowupText: "ఫాలో-అప్ నివేదిక (ట్రెండ్ ట్రాకర్ చూడండి)",
        demoPdfText: "మల్టీ-పేజీ PDF నివేదిక (2 పేజీలు)"
    },
    en: {
        brandTagline: "Your AI health friend",
        simpleModeText: "Simple Mode",
        simpleModeSub: "Large icons & audio",
        langSectionTitle: "Choose Your Language",
        langSectionHint: "Tap to hear explanations in your mother tongue",
        scanHeading: "Upload or Scan Lab Report",
        scanSubheading: "Upload multi-page PDF document or take clear photos",
        scanBtnLabel: "UPLOAD LAB REPORT",
        scanBtnSub: "PDF or Photos (Multi-page supported)",
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
        sendBtnText: "Ask",
        trendTitle: "Progress & Trend Tracker",
        trendSubtitle: "Comparing consecutive test reports over time",
        historyModalTitle: "Report History",
        clearHistoryLabel: "Clear History",
        demoFollowupText: "Simulate Follow-up Report (See Trend Tracker)",
        demoPdfText: "Or Try Multi-Page PDF Report (2 Pages)"
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
        this.trendChartInstance = null;

        this.initElements();
        this.bindEvents();
        this.applyLanguage(this.currentLang);
        this.applySimpleMode(this.simpleMode);
        this.updateHistoryBadge();
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
        this.btnDemoFollowup = document.getElementById("btnDemoFollowup");
        this.btnBackHome = document.getElementById("btnBackHome");

        // History Elements
        this.btnHistoryToggle = document.getElementById("btnHistoryToggle");
        this.historyCountBadge = document.getElementById("historyCountBadge");
        this.historyModal = document.getElementById("historyModal");
        this.btnCloseHistory = document.getElementById("btnCloseHistory");
        this.historyList = document.getElementById("historyList");
        this.btnClearHistory = document.getElementById("btnClearHistory");

        // Audio Listen Buttons
        this.btnListenAudio = document.getElementById("btnListenAudio");
        this.listenIcon = document.getElementById("listenIcon");
        this.btnAttachedListen = document.getElementById("btnAttachedListen");
        this.attachedListenIcon = document.getElementById("attachedListenIcon");
        this.attachedAudioWaves = document.getElementById("attachedAudioWaves");

        // Trend Tracker Elements
        this.trendTrackerCard = document.getElementById("trendTrackerCard");
        this.trendTitle = document.getElementById("trendTitle");
        this.trendSubtitle = document.getElementById("trendSubtitle");
        this.trendTrajectoryBadge = document.getElementById("trendTrajectoryBadge");
        this.trendMetricSelect = document.getElementById("trendMetricSelect");
        this.trendDeltaPill = document.getElementById("trendDeltaPill");
        this.trendDeltaIcon = document.getElementById("trendDeltaIcon");
        this.trendDeltaText = document.getElementById("trendDeltaText");
        this.trendDeltaStatus = document.getElementById("trendDeltaStatus");
        this.trendChartCanvas = document.getElementById("trendChartCanvas");
        this.trendInsightText = document.getElementById("trendInsightText");

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

        // History Modal Triggers
        if (this.btnHistoryToggle) {
            this.btnHistoryToggle.addEventListener("click", () => {
                this.openHistoryModal();
            });
        }
        if (this.btnCloseHistory) {
            this.btnCloseHistory.addEventListener("click", () => {
                this.closeHistoryModal();
            });
        }
        if (this.btnClearHistory) {
            this.btnClearHistory.addEventListener("click", () => {
                this.clearHistory();
            });
        }

        // Scan Buttons
        this.btnScanMain.addEventListener("click", () => {
            this.fileInput.click();
        });

        this.fileInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files.length > 0) {
                const files = Array.from(e.target.files);
                this.fileInput.value = "";
                this.processScan(files);
            }
        });

        this.btnDemoSample.addEventListener("click", () => {
            this.processScan(null, "baseline"); // Runs demo payload
        });

        if (this.btnDemoFollowup) {
            this.btnDemoFollowup.addEventListener("click", () => {
                this.processScan(null, "followup"); // Runs follow-up payload
            });
        }

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
        if (key === "rbc" || name.includes("rbc") || name.includes("red blood cell")) return "🔴";
        if (key === "mch" || name.includes("mch")) return "🧬";
        if (key === "mchc" || name.includes("mchc")) return "🧬";
        if (key === "mcv" || name.includes("mcv")) return "🔬";
        if (key === "hct" || name.includes("hematocrit") || name.includes("pcv")) return "🧪";
        if (key.includes("neutrophil") || name.includes("neutrophil")) return "🛡️";
        if (key.includes("lymphocyte") || name.includes("lymphocyte")) return "🦠";
        if (key.includes("monocyte") || name.includes("monocyte")) return "🧫";
        if (key.includes("eosinophil") || name.includes("eosinophil")) return "🌸";
        if (key.includes("basophil") || name.includes("basophil")) return "🫐";
        if (key.includes("esr") || name.includes("esr")) return "⏳";
        if (key.includes("hemoglobin") || name.includes("hemoglobin") || name.includes("haemoglobin") || name.includes("hb")) return "🩸";
        if (key.includes("fasting") || name.includes("fasting") || name.includes("fbs")) return "🍬";
        if (key.includes("post_prandial") || name.includes("ppbs") || name.includes("post prandial") || name.includes("pp")) return "🍚";
        if (key.includes("random") || name.includes("rbs")) return "🍬";
        if (key.includes("hba1c") || name.includes("hba1c")) return "📊";
        if (key.includes("wbc") || name.includes("wbc") || name.includes("leukocyte") || name.includes("tlc")) return "🛡️";
        if (key.includes("platelet") || name.includes("platelet") || name.includes("plt")) return "🩹";
        // Lipids
        if (key.includes("hdl") || name.includes("hdl")) return "💚";
        if (key.includes("ldl") || name.includes("ldl")) return "⚠️";
        if (key.includes("vldl") || name.includes("vldl")) return "🫀";
        if (key.includes("triglyceride") || name.includes("triglyceride") || name.includes("tg")) return "🧈";
        if (key.includes("cholesterol") || name.includes("cholesterol") || name.includes("lipid")) return "🫀";
        // Liver
        if (key.includes("bilirubin") || name.includes("bilirubin")) return "🟡";
        if (key.includes("sgpt") || key.includes("alt") || name.includes("sgpt") || name.includes("alt")) return "🧪";
        if (key.includes("sgot") || key.includes("ast") || name.includes("sgot") || name.includes("ast")) return "🧪";
        if (key.includes("alkaline") || name.includes("alkaline") || key.includes("alp") || name.includes("alp")) return "🧬";
        if (key.includes("protein") || name.includes("protein")) return "🥚";
        if (key.includes("albumin") || name.includes("albumin")) return "🥛";
        if (key.includes("globulin") || name.includes("globulin")) return "🛡️";
        if (key.includes("ggt") || name.includes("ggt")) return "🔬";
        // Thyroid
        if (key.includes("tsh") || name.includes("tsh") || name.includes("thyroid")) return "⚡";
        if (key.includes("t3") || name.includes("t3")) return "🦋";
        if (key.includes("t4") || name.includes("t4")) return "🦋";
        // Kidney
        if (key.includes("creatinine") || name.includes("creatinine")) return "💧";
        if (key.includes("urea") || name.includes("urea") || key.includes("bun") || name.includes("bun")) return "🚽";
        if (key.includes("uric") || name.includes("uric")) return "💎";
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

    // -------------------------------------------------------------
    // History Management (localStorage)
    // -------------------------------------------------------------
    getHistory() {
        try {
            const raw = localStorage.getItem("reportSakhi_history");
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            return [];
        }
    }

    saveToHistory(scanResult) {
        if (!scanResult || !scanResult.success) return;
        const checker = scanResult.checker || {};
        const explainer = scanResult.explainer || {};
        const history = this.getHistory();
        const now = new Date();
        const entry = {
            id: "rep_" + Date.now(),
            timestamp: Date.now(),
            dateStr: now.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
            items: checker.items || [],
            overall_status: checker.overall_status || "green",
            headline: explainer.headline || "Lab Report",
            summary_text: explainer.summary_text || ""
        };
        history.push(entry);
        if (history.length > 25) history.shift();
        localStorage.setItem("reportSakhi_history", JSON.stringify(history));
        this.updateHistoryBadge();
    }

    clearHistory() {
        localStorage.removeItem("reportSakhi_history");
        this.updateHistoryBadge();
        this.renderHistoryList();
        if (this.trendTrackerCard) {
            this.trendTrackerCard.style.display = "none";
        }
        if (this.trendChartInstance) {
            this.trendChartInstance.destroy();
            this.trendChartInstance = null;
        }
    }

    updateHistoryBadge() {
        const count = this.getHistory().length;
        if (this.historyCountBadge) {
            this.historyCountBadge.innerText = count;
            this.historyCountBadge.style.display = count > 0 ? "inline-flex" : "none";
        }
    }

    openHistoryModal() {
        if (this.historyModal) {
            this.renderHistoryList();
            this.historyModal.style.display = "flex";
        }
    }

    closeHistoryModal() {
        if (this.historyModal) {
            this.historyModal.style.display = "none";
        }
    }

    renderHistoryList() {
        if (!this.historyList) return;
        const history = this.getHistory();
        if (history.length === 0) {
            this.historyList.innerHTML = `<p class="history-empty">No reports saved yet. Scan a report to begin tracking trends.</p>`;
            return;
        }

        this.historyList.innerHTML = "";
        [...history].reverse().forEach((rep) => {
            const item = document.createElement("div");
            item.className = `history-item status-${rep.overall_status || 'green'}`;
            const statusLabel = rep.overall_status === "red" ? "URGENT" : (rep.overall_status === "yellow" ? "WATCH" : "NORMAL");
            item.innerHTML = `
                <div class="history-item-top">
                    <span class="history-item-date">📅 ${rep.dateStr}</span>
                    <span class="history-status-tag tag-${rep.overall_status || 'green'}">${statusLabel}</span>
                </div>
                <h4 class="history-item-headline">${rep.headline || 'Lab Report'}</h4>
                <div class="history-item-meta">
                    <span>${(rep.items || []).length} Tests Checked</span>
                </div>
            `;
            this.historyList.appendChild(item);
        });
    }

    // -------------------------------------------------------------
    // Longitudinal Trend Tracker (Chart.js Integration)
    // -------------------------------------------------------------
    renderLongitudinalTracker(data) {
        const comparison = data.comparison;
        if (!comparison || !comparison.has_comparison || !comparison.comparisons || comparison.comparisons.length === 0) {
            if (this.trendTrackerCard) this.trendTrackerCard.style.display = "none";
            return;
        }

        if (this.trendTrackerCard) this.trendTrackerCard.style.display = "block";

        // Set overall trajectory badge
        const traj = comparison.overall_trajectory || "stable";
        const trajLabels = {
            improving: { en: "Improving", ml: "മെച്ചപ്പെടുന്നു", hi: "सुधार", ta: "மேம்படுகிறது" },
            worsening: { en: "Needs Attention", ml: "ശ്രദ്ധിക്കുക", hi: "ध्यान दें", ta: "கவனம் தேவை" },
            stable: { en: "Stable", ml: "സ്ഥിരത", hi: "स्थिर", ta: "சீராக உள்ளது" }
        };
        if (this.trendTrajectoryBadge) {
            this.trendTrajectoryBadge.className = `trend-trajectory-badge trajectory-${traj}`;
            this.trendTrajectoryBadge.innerText = (trajLabels[traj] && trajLabels[traj][this.currentLang]) || traj.toUpperCase();
        }

        // Populate metric dropdown
        if (this.trendMetricSelect) {
            this.trendMetricSelect.innerHTML = "";
            comparison.comparisons.forEach((item, idx) => {
                const opt = document.createElement("option");
                opt.value = idx;
                const arrow = item.trend_direction === "down" ? "📉" : (item.trend_direction === "up" ? "📈" : "➡️");
                opt.innerText = `${arrow} ${item.canonical_name} (${item.delta_formatted} ${item.unit})`;
                this.trendMetricSelect.appendChild(opt);
            });

            this.trendMetricSelect.onchange = () => {
                const selectedIdx = parseInt(this.trendMetricSelect.value, 10);
                this.renderSingleMetricGraph(comparison.comparisons[selectedIdx]);
            };
        }

        // Render first metric graph by default
        this.renderSingleMetricGraph(comparison.comparisons[0]);
    }

    renderSingleMetricGraph(item) {
        if (!item) return;

        // 1. Delta Pill
        if (this.trendDeltaPill) {
            this.trendDeltaPill.className = `trend-delta-pill delta-${item.health_impact}`;
        }
        if (this.trendDeltaIcon) {
            this.trendDeltaIcon.innerText = item.trend_direction === "down" ? "📉" : (item.trend_direction === "up" ? "📈" : "➡️");
        }
        if (this.trendDeltaText) {
            this.trendDeltaText.innerText = `${item.delta_formatted} ${item.unit}`;
        }
        if (this.trendDeltaStatus) {
            const impactLabels = {
                improved: { en: "(Improved)", ml: "(മെച്ചപ്പെട്ടു)", hi: "(सुधार हुआ)", ta: "(மேம்பட்டது)" },
                worsened: { en: "(Needs Attention)", ml: "(ശ്രദ്ധിക്കുക)", hi: "(ध्यान दें)", ta: "(கவனம் தேவை)" },
                stable: { en: "(Steady)", ml: "(മാറ്റമില്ല)", hi: "(स्थिर)", ta: "(சீராக உள்ளது)" }
            };
            const impactMap = impactLabels[item.health_impact] || impactLabels.stable;
            this.trendDeltaStatus.innerText = (impactMap && impactMap[this.currentLang]) || `(${item.health_impact})`;
        }

        // 2. Insight Text
        if (this.trendInsightText) {
            const msg = (item.message && item.message[this.currentLang]) || (item.message && item.message.en) || "";
            this.trendInsightText.innerText = msg;
        }

        // 3. Chart.js rendering
        if (!this.trendChartCanvas || typeof Chart === "undefined") return;

        const ctx = this.trendChartCanvas.getContext("2d");
        if (this.trendChartInstance) {
            this.trendChartInstance.destroy();
            this.trendChartInstance = null;
        }

        // Extract historical values for this metric from localStorage
        const history = this.getHistory();
        const dataPoints = [];
        const rawDates = [];

        // Robust matching across history records (fuzzy on rule_key, canonical_name, test_name)
        const clean = str => (str || "").toLowerCase().replace(/[^a-z0-9]/g, "");
        const targetRuleKey = (item.rule_key && item.rule_key !== "custom_lab_test") ? item.rule_key : null;
        const targetCanon = clean(item.canonical_name);
        const targetName = clean(item.test_name);

        const isMatch = t => {
            if (!t) return false;
            if (targetRuleKey && t.rule_key && t.rule_key !== "custom_lab_test" && t.rule_key === targetRuleKey) {
                return true;
            }
            const tCanon = clean(t.canonical_name);
            const tName = clean(t.test_name);
            if (targetCanon && (targetCanon === tCanon || targetCanon === tName)) return true;
            if (targetName && (targetName === tCanon || targetName === tName)) return true;
            if (targetCanon && tCanon && (targetCanon.includes(tCanon) || tCanon.includes(targetCanon)) && Math.min(targetCanon.length, tCanon.length) >= 4) return true;
            if (targetCanon && tName && (targetCanon.includes(tName) || tName.includes(targetCanon)) && Math.min(targetCanon.length, tName.length) >= 4) return true;
            if (targetName && tName && (targetName.includes(tName) || tName.includes(targetName)) && Math.min(targetName.length, tName.length) >= 4) return true;
            return false;
        };

        history.forEach(h => {
            const found = (h.items || []).find(isMatch);
            if (found && typeof found.value === "number") {
                rawDates.push(h.dateStr || "");
                dataPoints.push(found.value);
            }
        });

        // Ensure at least previous & current points exist if history had incomplete records
        if (dataPoints.length === 0 && item.previous_value !== undefined && item.current_value !== undefined) {
            dataPoints.push(item.previous_value);
            dataPoints.push(item.current_value);
            rawDates.push("Previous Test");
            rawDates.push("Current Test");
        } else if (dataPoints.length === 1 && item.previous_value !== undefined && Math.abs(dataPoints[0] - item.current_value) < 0.001) {
            dataPoints.unshift(item.previous_value);
            rawDates.unshift("Previous Test");
        }

        // Generate clean chronological labels (Test #1, Test #2, Test #3, etc.)
        const labels = dataPoints.map((val, idx) => {
            const isLast = idx === dataPoints.length - 1;
            const testNum = idx + 1;
            const d = rawDates[idx] || "";
            if (isLast) {
                const latestLabel = this.currentLang === "ml" ? "ഇന്നത്തെ പരിശോധന" : (this.currentLang === "hi" ? "आज की जांच" : "Current Test");
                return d ? `Test #${testNum} (${latestLabel})` : `Test #${testNum} (${latestLabel})`;
            }
            return d ? `Test #${testNum} (${d})` : `Test #${testNum}`;
        });

        const isImproved = item.health_impact === "improved";
        const isWorsened = item.health_impact === "worsened";
        const primaryColor = isImproved ? "#16a34a" : (isWorsened ? "#dc2626" : "#2563eb");
        const bgColor = isImproved ? "rgba(22, 163, 74, 0.12)" : (isWorsened ? "rgba(220, 38, 38, 0.12)" : "rgba(37, 99, 235, 0.12)");

        this.trendChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `${item.canonical_name} (${item.unit})`,
                    data: dataPoints,
                    borderColor: primaryColor,
                    backgroundColor: bgColor,
                    fill: true,
                    tension: 0.35,
                    borderWidth: 3,
                    pointBackgroundColor: primaryColor,
                    pointBorderColor: "#ffffff",
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 9
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#1e293b',
                            font: { family: "'Plus Jakarta Sans', sans-serif", weight: '600', size: 13 },
                            boxWidth: 12
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
                        bodyFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12, weight: 'bold' },
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: (context) => `Value: ${context.parsed.y} ${item.unit}`
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: { color: "rgba(0, 0, 0, 0.05)" },
                        ticks: {
                            font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 },
                            color: "#64748b"
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            font: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: '600' },
                            color: "#475569"
                        }
                    }
                }
            }
        });
    }

    async processScan(files, demoType = null) {
        this.mainHomeView.style.display = "none";
        this.loadingOverlay.style.display = "flex";
        this.resultsContainer.style.display = "none";

        const fileList = files ? (Array.isArray(files) ? files : (files instanceof FileList ? Array.from(files) : [files])) : [];
        const isPdf = (fileList.length > 0 && (
            (fileList[0].name && fileList[0].name.toLowerCase().endsWith(".pdf")) ||
            (fileList[0].type && fileList[0].type.includes("pdf"))
        )) || demoType === "pdf";

        if (isPdf && this.loadingStep) {
            this.loadingStep.textContent = "Analyzing multi-page PDF document...";
        } else if (fileList.length > 1 && this.loadingStep) {
            this.loadingStep.textContent = `Analyzing ${fileList.length} report pages...`;
        } else if (this.loadingStep) {
            this.loadingStep.textContent = "Reader Agent extracting values from document...";
        }

        const formData = new FormData();
        if (fileList.length > 0) {
            for (const f of fileList) {
                formData.append("files", f);
            }
            formData.append("file", fileList[0]);
        }
        if (demoType) {
            formData.append("demo_type", demoType);
        }
        formData.append("language", this.currentLang);
        formData.append("simple_mode", this.simpleMode);

        // Include latest previous report from localStorage history if present
        const history = this.getHistory();
        if (history.length > 0) {
            const mergedItems = {};
            history.forEach(rep => {
                (rep.items || []).forEach(item => {
                    const key = item.rule_key || item.canonical_name || item.test_name;
                    if (key) {
                        mergedItems[key] = item;
                    }
                });
            });
            const previousReport = { items: Object.values(mergedItems) };
            formData.append("previous_report", JSON.stringify(previousReport));
        }

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

            // Save report to localStorage history
            this.saveToHistory(data);

            this.renderResults(data);
        } catch (error) {
            console.error("Scan error:", error);
            this.loadingOverlay.style.display = "none";
            this.showRetakeModal("Could not read document clearly. Please upload a clear PDF or well-lit photos.");
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
        const comparison = data.comparison || {};
        const overallStatus = checker.overall_status || "green";

        // Store context for Explainer Agent Q&A
        this.currentReportContext = JSON.stringify(checker.items || []);

        // Store synthesized audio
        this.currentAudioBase64 = voice.audio_base64 || null;
        this.currentAudioFormat = voice.audio_format || "audio/wav";

        // Urgency pill
        this.urgencyPill.className = `urgency-pill urgency-${overallStatus}`;
        const statusMap = {
            green: { en: "Normal", hi: "सामान्य", ml: "സാധാരണ", ta: "இயல்பானது", te: "సాధారణం" },
            yellow: { en: "Consult Doctor", hi: "डॉक्टर से मिलें", ml: "ഡോക്ടറെ കാണുക", ta: "ஆலோசனை பெறுக", te: "వైద్యుడిని సంప్రదించండి" },
            red: { en: "Needs Attention", hi: "तुरंत ध्यान दें", ml: "അടിയന്തിരം", ta: "கவனம் தேவை", te: "అత్యవసరం" }
        };
        this.urgencyPillText.innerText = (statusMap[overallStatus] && statusMap[overallStatus][this.currentLang]) || overallStatus.toUpperCase();

        // Summary and Safety Line
        this.explanationHeadline.innerText = explainer.headline || "Report Overview";
        this.explanationText.innerText = explainer.summary_text || "";
        this.safetyLineText.innerText = explainer.safety_line || I18N[this.currentLang]?.safetyLineText || "This explains your report. It is not a diagnosis. Please consult a doctor.";
        this.currentSpeechScript = explainer.full_speech_script || explainer.summary_text || "";

        // Render Longitudinal Trend Tracker (Chart.js + Metric Picker)
        this.renderLongitudinalTracker(data);

        // Tests Grid - Grouped by Health Panels
        this.testsGrid.innerHTML = "";
        const items = checker.items || [];
        const compList = comparison.comparisons || [];

        const panelConfigs = [
            { key: "diabetes", icon: "🍬", titles: { en: "Diabetes & Blood Sugar", hi: "मधुमेह और ब्लड शुगर", ml: "പ്രമേഹ പരിശോധന", ta: "சர்க்கரை பரிசோதனை", te: "మధుమేహం & బ్లడ్ షుగర్" } },
            { key: "lipids", icon: "🫀", titles: { en: "Heart & Lipid Profile", hi: "हृदय और लिपिड प्रोफाइल", ml: "ഹൃദയാരോഗ്യവും കൊളസ്ട്രോളും", ta: "இதயம் & கொழுப்பு அளவு", te: "గుండె & లిపిడ్ ప్రొఫైల్" } },
            { key: "liver", icon: "🧪", titles: { en: "Liver Function Tests (LFT)", hi: "लिवर फंक्शन टेस्ट (एलएफटी)", ml: "കരൾ പ്രവർത്തന പരിശോധന", ta: "கல்லீரல் செயல்பாடு பரிசோதனை", te: "కాలేయ పనితీరు పరీక్షలు (LFT)" } },
            { key: "kidney", icon: "💧", titles: { en: "Kidney & Vital Organs", hi: "किडनी व मुख्य अंग", ml: "വൃക്ക പരിശോധന", ta: "சிறுநீரக பரிசோதனை", te: "కిడ్నీ & ముఖ్య అవయవాలు" } },
            { key: "thyroid", icon: "⚡", titles: { en: "Thyroid Profile", hi: "थायराइड प्रोफाइल", ml: "തൈറോയ്ഡ് പരിശോധന", ta: "தைராய்டு பரிசோதனை", te: "థైరాయిడ్ ప్రొఫైల్" } },
            { key: "cbc", icon: "🩸", titles: { en: "Complete Blood Count (CBC)", hi: "रक्त गणना (सीबीसी)", ml: "രക്ത പരിശോധന (സിബിസി)", ta: "முழு இரத்த எண்ணிக்கை (CBC)", te: "కంప్లీట్ బ్లడ్ కౌంట్ (CBC)" } },
            { key: "general", icon: "🔬", titles: { en: "General Clinical Tests", hi: "सामान्य नैदानिक जांच", ml: "മറ്റു പരിശോധനകൾ", ta: "பொது ஆய்வக பரிசோதனைகள்", te: "సాధారణ క్లినికల్ పరీక్షలు" } }
        ];

        // Map items by panel
        const panelMap = new Map();
        panelConfigs.forEach(p => panelMap.set(p.key, []));

        items.forEach((test, idx) => {
            const panelKey = (test.panel && panelMap.has(test.panel)) ? test.panel : "general";
            panelMap.get(panelKey).push({ test, idx });
        });

        // Helper to construct a single test card element
        const createCardElement = (test, idx) => {
            const card = document.createElement("div");
            const color = test.color || "green";
            card.className = `test-item-card color-${color}`;
            
            const desc = (test.description && test.description[this.currentLang]) || (test.description && test.description.en) || "";
            const normFormatted = test.normal_range ? test.normal_range.formatted : "";
            const testIcon = this.getTestIcon(test);
            const statusIcon = this.getStatusIcon(color);
            const statusLabel = test.status_label || (color === "red" ? "URGENT" : (color === "yellow" ? "WATCH" : "NORMAL"));

            // Match test comparison if available
            const matchedComp = compList.find(c => 
                (c.rule_key && c.rule_key === test.rule_key) ||
                (c.canonical_name && c.canonical_name.toLowerCase() === (test.canonical_name || test.test_name).toLowerCase()) ||
                (c.test_name && c.test_name.toLowerCase() === test.test_name.toLowerCase())
            );

            let deltaBadgeHtml = "";
            if (matchedComp) {
                const impactClass = matchedComp.health_impact === "improved" ? "delta-improved" : (matchedComp.health_impact === "worsened" ? "delta-worsened" : "delta-stable");
                const arrow = matchedComp.trend_direction === "down" ? "📉" : (matchedComp.trend_direction === "up" ? "📈" : "➡️");
                const impactTag = matchedComp.health_impact === "improved" ? "Improved" : (matchedComp.health_impact === "worsened" ? "Attention" : "Steady");
                deltaBadgeHtml = `
                    <div class="test-delta-badge ${impactClass}">
                        <span>${arrow}</span>
                        <span>${matchedComp.delta_formatted} ${matchedComp.unit}</span>
                        <span class="impact-text">(${impactTag})</span>
                    </div>
                `;
            }

            card.innerHTML = `
                <div class="test-card-main">
                    <div class="test-icon-badge" aria-hidden="true">${testIcon}</div>
                    <div class="test-meta">
                        <span class="test-title">${test.canonical_name || test.test_name}</span>
                        <div class="test-status-pill pill-${color}">
                            <span class="status-symbol" aria-hidden="true">${statusIcon}</span>
                            <span class="status-name">${statusLabel}</span>
                        </div>
                        ${deltaBadgeHtml}
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
                    this.speakTestCard(test, miniBtn, matchedComp);
                });
            }

            return card;
        };

        // Render sections for panels with active test items
        let renderedCount = 0;
        panelConfigs.forEach(pConfig => {
            const list = panelMap.get(pConfig.key) || [];
            if (list.length === 0) return;
            renderedCount += list.length;

            const panelSec = document.createElement("section");
            panelSec.className = `panel-section panel-${pConfig.key}`;
            
            const panelTitle = (pConfig.titles && pConfig.titles[this.currentLang]) || pConfig.titles.en;
            const countLabel = list.length === 1 ? "1 test" : `${list.length} tests`;

            panelSec.innerHTML = `
                <div class="panel-header">
                    <div class="panel-header-left">
                        <span class="panel-header-icon" aria-hidden="true">${pConfig.icon}</span>
                        <h4 class="panel-header-title">${panelTitle}</h4>
                    </div>
                    <span class="panel-header-badge">${countLabel}</span>
                </div>
                <div class="panel-cards-grid"></div>
            `;

            const cardsGrid = panelSec.querySelector(".panel-cards-grid");
            list.forEach(({ test, idx }) => {
                const cardEl = createCardElement(test, idx);
                cardsGrid.appendChild(cardEl);
            });

            this.testsGrid.appendChild(panelSec);
        });

        // Fallback: If no panel matched (e.g. unknown panel), append cards directly
        if (renderedCount === 0 && items.length > 0) {
            items.forEach((test, idx) => {
                const cardEl = createCardElement(test, idx);
                this.testsGrid.appendChild(cardEl);
            });
        }

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
            hi: "hi-IN", en: "en-IN", ml: "ml-IN", ta: "ta-IN", te: "te-IN"
        };
        utterance.lang = langCodes[this.currentLang] || "en-IN";
        utterance.rate = 0.95;

        utterance.onstart = () => this.setSpeakingState(true);
        utterance.onend = utterance.onerror = () => this.setSpeakingState(false);

        window.speechSynthesis.speak(utterance);
    }

    speakTestCard(test, btnElement, comp = null) {
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
        } else if (this.currentLang === "te") {
            script = `${name}: విలువ ${val}. స్థితి: ${status}.`;
        } else {
            script = `${name} is ${val}. Status is ${status}.`;
        }

        if (comp && comp.message) {
            const compSentence = comp.message[this.currentLang] || comp.message.en;
            if (compSentence) {
                script += ` ${compSentence}`;
            }
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
            hi: "hi-IN", en: "en-IN", ml: "ml-IN", ta: "ta-IN", te: "te-IN"
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
