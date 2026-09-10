/**
 * i18n.js — Kisan Mitra AI Multilingual Localization Engine
 * Supports: English, Hindi (हिन्दी), Telugu (తెలుగు), Tamil (தமிழ்), Kannada (ಕನ್ನಡ), Marathi (मराठी)
 * Created by Circuit Maze Team (SIH 2026)
 * Offline-first, client-side translation with speech audio synthesis.
 */

'use strict';

const KISAN_I18N = {
  en: {
    lang_name: "English",
    lang_code: "en",
    speech_lang: "en-IN",
    nav_dashboard: "📊 Dashboard",
    nav_analytics: "📈 Analytics",
    nav_alerts: "🚨 Alerts",
    nav_history: "📜 History",
    nav_settings: "⚙️ Settings",
    brand_title: "Kisan Mitra AI",
    brand_subtitle: "Circuit Maze · SIH 2026",
    env_normal: "NORMAL",
    env_alert: "ALERT",
    telemetry_temp: "Ambient Temperature",
    telemetry_hum: "Relative Humidity",
    telemetry_soil: "Soil Moisture (VWC)",
    telemetry_gas: "Air Quality (MQ-135)",
    telemetry_pump: "Irrigation Pump",
    telemetry_led: "Hardware Alert LED",
    telemetry_soil_tag: "Moist Root Zone",
    telemetry_gas_tag: "Clean Field Air",
    telemetry_hint_temp: "Optimal crop growth: 20–30°C",
    telemetry_hint_hum: "Fungal infection risk rises >85%",
    telemetry_hint_soil: "Threshold: auto-irrigation <30%",
    telemetry_hint_gas: "Hazard alert: gas level >350 ppm",
    telemetry_hint_pump: "Relay status: auto-shutoff enabled",
    telemetry_hint_led: "Actuator: triggers on thresholds",
    diag_studio_title: "AI Crop Disease Diagnostic Studio",
    diag_studio_sub: "Hugging Face ViT Edge Model · Zero Internet Required",
    input_card_title: "Test Crop Leaf Condition",
    input_card_sub: "Take a photo using your phone/webcam, upload an image file, or trigger edge hardware.",
    tab_upload: "📤 Upload Photo",
    tab_webcam: "📱 Device Camera",
    tab_picam: "🤖 Pi Camera",
    dropzone_prompt: "Drop leaf photo here or click to browse",
    dropzone_sub: "Supports high-res JPG, PNG, WEBP, BMP",
    btn_analyze: "RUN AI DISEASE ANALYSIS",
    btn_analyzing: "🔬 ANALYZING SPECIMEN…",
    dossier_title: "Diagnostic Dossier",
    dossier_subtitle: "Agronomic Action Plan & Treatment Report",
    btn_print: "🖨️ Print Report",
    btn_listen: "🔊 Listen (Audio)",
    btn_listening: "🔊 Speaking...",
    conf_label: "AI Confidence",
    health_score_label: "Crop Health Index",
    risk_low: "LOW RISK (Vigorous)",
    risk_high: "HIGH RISK (Action Needed)",
    status_healthy: "HEALTHY",
    status_diseased: "DISEASED",
    healthy_foliage: "Healthy Foliage",
    action_plan_title: "Agronomic Action Plan & Treatment",
    tab_immediate: "⚡ Immediate Action",
    tab_chemical: "🧪 Chemical Remedy",
    tab_organic: "🍃 Organic / Bio",
    tab_prevention: "🛡️ Prevention",
    immediate_healthy: "✓ Continue standard irrigation and scheduled fertilizer regime. No corrective spray needed.",
    immediate_diseased: "⚠️ Isolate affected crop patch. Remove and safely dispose of severely infected leaves. Avoid handling wet plants to prevent spreading fungal spores.",
    checklist_title: "On-Field Farmer Checklist:",
    checklist_1: "Inspect neighboring rows for early lesion spots",
    checklist_2: "Prune and incinerate infected foliage",
    checklist_3: "Apply recommended protective spray as scheduled",
    recent_scans_title: "Recent Crop Health Scans",
    recent_scans_sub: "Historical diagnostic records stored in local database",
    empty_scans: "No scan records available yet.",
    table_th_time: "Timestamp",
    table_th_crop: "Crop",
    table_th_condition: "Condition",
    table_th_confidence: "Confidence",
    table_th_status: "Status",
    table_th_action: "Action",
    view_dossier: "View Dossier →",
    view_all_history: "View All Historical Scans →",
    quick_stats_total: "Total Field Scans",
    quick_stats_healthy: "Healthy Samples",
    quick_stats_diseased: "Diseased Alerts",
    quick_stats_accuracy: "Avg AI Confidence",
    footer_text: "Created by Circuit Maze Team as part of SIH 2026 · Edge AI & IoT Farm Assistant",
    footer_disclaimer: "⚠ AI predictions are decision-support tools only — not a substitute for professional agronomic advice.",
    lang_changed_toast: "Language set to English",
    speech_not_supported: "Audio speech synthesis is not supported on this browser.",
    crop_potato: "Potato",
    crop_rice: "Rice",
    crop_wheat: "Wheat",
    crop_corn: "Corn",
    crop_sugarcane: "Sugarcane"
  },

  hi: {
    lang_name: "हिन्दी (Hindi)",
    lang_code: "hi",
    speech_lang: "hi-IN",
    nav_dashboard: "📊 डैशबोर्ड",
    nav_analytics: "📈 विश्लेषण",
    nav_alerts: "🚨 चेतावनियाँ",
    nav_history: "📜 इतिहास",
    nav_settings: "⚙️ सेटिंग्स",
    brand_title: "किसान मित्र AI",
    brand_subtitle: "सर्किट मेज़ · SIH 2026",
    env_normal: "सामान्य",
    env_alert: "चेतावनी",
    telemetry_temp: "परिवेश तापमान",
    telemetry_hum: "सापेक्ष आर्द्रता",
    telemetry_soil: "मिट्टी की नमी (VWC)",
    telemetry_gas: "वायु गुणवत्ता (MQ-135)",
    telemetry_pump: "सिंचाई पंप",
    telemetry_led: "हार्डवेयर अलर्ट एलईडी",
    telemetry_soil_tag: "उचित नमी स्तर",
    telemetry_gas_tag: "शुद्ध खेत हवा",
    telemetry_hint_temp: "अनुकूलतम फसल विकास: 20–30°C",
    telemetry_hint_hum: "फफूंद संक्रमण जोखिम बढ़ता है >85%",
    telemetry_hint_soil: "सीमा: ऑटो सिंचाई चालू <30%",
    telemetry_hint_gas: "खतरा चेतावनी: गैस स्तर >350 ppm",
    telemetry_hint_pump: "रिले स्थिति: ऑटो-शटऑफ सक्रिय",
    telemetry_hint_led: "एक्ट्यूएटर: सुरक्षा सीमा पर ट्रिगर",
    diag_studio_title: "एआई फसल रोग निदान केंद्र",
    diag_studio_sub: "हगिंग फेस वीआईटी एज मॉडल · बिना इंटरनेट के कार्यरत",
    input_card_title: "फसल की पत्ती की स्थिति जांचें",
    input_card_sub: "अपने फोन/कैमरे से फोटो लें, इमेज फाइल अपलोड करें, या सीधे हार्डवेयर ट्रिगर करें।",
    tab_upload: "📤 फोटो अपलोड",
    tab_webcam: "📱 फोन/डिवाइस कैमरा",
    tab_picam: "🤖 रास्पबेरी पाई कैमरा",
    dropzone_prompt: "पत्ती की फोटो यहां खींचकर लाएं या क्लिक करें",
    dropzone_sub: "उच्च गुणवत्ता वाली JPG, PNG, WEBP, BMP समर्थित",
    btn_analyze: "एआई रोग विश्लेषण शुरू करें",
    btn_analyzing: "🔬 पत्ती का विश्लेषण हो रहा है…",
    dossier_title: "नैदानिक विवरण (डोज़ियर)",
    dossier_subtitle: "कृषि कार्य योजना एवं उपचार रिपोर्ट",
    btn_print: "🖨️ रिपोर्ट प्रिंट करें",
    btn_listen: "🔊 सुनें (ऑडियो)",
    btn_listening: "🔊 बोल रहे हैं...",
    conf_label: "एआई विश्वसनीयता",
    health_score_label: "फसल स्वास्थ्य सूचकांक",
    risk_low: "कम जोखिम (स्वस्थ फसल)",
    risk_high: "उच्च जोखिम (उपचार आवश्यक)",
    status_healthy: "स्वस्थ",
    status_diseased: "रोगग्रस्त",
    healthy_foliage: "स्वस्थ पत्तियां",
    action_plan_title: "कृषि कार्य योजना एवं उपचार",
    tab_immediate: "⚡ तत्काल कार्रवाई",
    tab_chemical: "🧪 रासायनिक उपचार",
    tab_organic: "🍃 जैविक / बायो उपचार",
    tab_prevention: "🛡️ सुरक्षा एवं रोकथाम",
    immediate_healthy: "✓ सामान्य सिंचाई और निर्धारित खाद प्रबंधन जारी रखें। किसी कीटनाशक स्प्रे की आवश्यकता नहीं है।",
    immediate_diseased: "⚠️ प्रभावित फसल क्षेत्र को अलग करें। रोगग्रस्त पत्तियों को तुरंत काटकर सुरक्षित रूप से नष्ट करें। गीले पौधों को छूने से बचें।",
    checklist_title: "खेत में किसान चेकलिस्ट:",
    checklist_1: "संक्रमण के शुरुआती धब्बों के लिए आस-पास की कतारों की जाँच करें",
    checklist_2: "संक्रमित पत्तियों को काटकर सुरक्षित रूप से नष्ट करें",
    checklist_3: "अनुशंसित सुरक्षात्मक स्प्रे समय पर करें",
    recent_scans_title: "हालिया फसल स्वास्थ्य स्कैन",
    recent_scans_sub: "स्थानीय डेटाबेस में सुरक्षित ऐतिहासिक रिकॉर्ड",
    empty_scans: "अभी तक कोई स्कैन रिकॉर्ड उपलब्ध नहीं है।",
    table_th_time: "समय",
    table_th_crop: "फसल",
    table_th_condition: "स्थिति / रोग",
    table_th_confidence: "विश्वसनीयता",
    table_th_status: "दर्जा",
    table_th_action: "कार्रवाई",
    view_dossier: "विवरण देखें →",
    view_all_history: "सभी स्कैन इतिहास देखें →",
    quick_stats_total: "कुल स्कैन",
    quick_stats_healthy: "स्वस्थ नमूने",
    quick_stats_diseased: "रोगग्रस्त चेतावनियाँ",
    quick_stats_accuracy: "औसत सटीकता",
    footer_text: "सर्किट मेज़ टीम द्वारा SIH 2026 के लिए निर्मित · एज एआई एवं आईओटी कृषि सहायक",
    footer_disclaimer: "⚠ एआई भविष्यवाणियां केवल सहायता उपकरण हैं — पेशेवर कृषि विशेषज्ञ की सलाह का विकल्प नहीं।",
    lang_changed_toast: "भाषा हिन्दी में बदली गई",
    speech_not_supported: "इस ब्राउज़र पर ऑडियो भाषण उपलब्ध नहीं है।",
    crop_potato: "आलू (Potato)",
    crop_rice: "चावल / धान (Rice)",
    crop_wheat: "गेहूं (Wheat)",
    crop_corn: "मक्का (Corn)",
    crop_sugarcane: "गन्ना (Sugarcane)"
  },

  te: {
    lang_name: "తెలుగు (Telugu)",
    lang_code: "te",
    speech_lang: "te-IN",
    nav_dashboard: "📊 డాష్‌బోర్డ్",
    nav_analytics: "📈 విశ్లేషణలు",
    nav_alerts: "🚨 హెచ్చరికలు",
    nav_history: "📜 చరిత్ర",
    nav_settings: "⚙️ సెట్టింగ్‌లు",
    brand_title: "కిసాన్ మిత్ర AI",
    brand_subtitle: "సర్క్యూట్ మేజ్ · SIH 2026",
    env_normal: "సాధారణం",
    env_alert: "హెచ్చరిక",
    telemetry_temp: "పరిసర ఉష్ణోగ్రత",
    telemetry_hum: "గాలిలో తేమ (ఆర్ద్రత)",
    telemetry_soil: "నేల తేమ శాతం (VWC)",
    telemetry_gas: "గాలి నాణ్యత (MQ-135)",
    telemetry_pump: "సాగునీటి మోటార్ పంపు",
    telemetry_led: "హార్డ్‌వేర్ హెచ్చరిక LED",
    telemetry_soil_tag: "సరిపడా తేమ",
    telemetry_gas_tag: "పరిశుభ్రమైన గాలి",
    telemetry_hint_temp: "అనుకూలమైన పంట పెరుగుదల: 20–30°C",
    telemetry_hint_hum: "శిలీంధ్ర తెగులు ముప్పు ఎక్కువ: >85%",
    telemetry_hint_soil: "పరిమితి: స్వయం చాలక మోటార్ <30%",
    telemetry_hint_gas: "ప్రమాద హెచ్చరిక: గ్యాస్ స్థాయి >350 ppm",
    telemetry_hint_pump: "రిలే స్థితి: ఆటో షటాఫ్ ప్రారంభించబడింది",
    telemetry_hint_led: "యాక్చుయేటర్: ప్రమాద పరిమితి వద్ద వెలుగుతుంది",
    diag_studio_title: "AI పంట వ్యాధి నిర్ధారణ కేంద్రం",
    diag_studio_sub: "హగ్గింగ్ ఫేస్ ViT ఎడ్జ్ మోడల్ · ఇంటర్నెట్ అవసరం లేదు",
    input_card_title: "పంట ఆకు పరిస్థితిని పరీక్షించండి",
    input_card_sub: "మీ ఫోన్/వెబ్‌క్యామ్‌తో ఫోటో తీయండి, ఫైల్‌ను అప్‌లోడ్ చేయండి లేదా హార్డ్‌వేర్ ఉపయోగించండి.",
    tab_upload: "📤 ఫోటో అప్‌లోడ్",
    tab_webcam: "📱 ఫోన్ కెమెరా",
    tab_picam: "🤖 పై కెమెరా",
    dropzone_prompt: "ఆకు ఫోటోను ఇక్కడ ఉంచండి లేదా ఎంచుకోండి",
    dropzone_sub: "అధిక నాణ్యత గల JPG, PNG, WEBP, BMP సపోర్ట్ చేయబడుతుంది",
    btn_analyze: "AI వ్యాధి విశ్లేషణను ప్రారంభించండి",
    btn_analyzing: "🔬 ఆకును విశ్లేషిస్తోంది…",
    dossier_title: "వ్యాధి నిర్ధారణ నివేదిక (డాసియర్)",
    dossier_subtitle: "వ్యవసాయ కార్యాచరణ ప్రణాళిక & చికిత్స నివేదిక",
    btn_print: "🖨️ నివేదిక ముద్రించండి",
    btn_listen: "🔊 వినండి (ఆడియో)",
    btn_listening: "🔊 చదువుతోంది...",
    conf_label: "AI ఖచ్చితత్వం",
    health_score_label: "పంట ఆరోగ్య సూచిక",
    risk_low: "తక్కువ ప్రమాదం (ఆరోగ్యకరమైన పంట)",
    risk_high: "అధిక ప్రమాదం (తక్షణ చికిత్స అవసరం)",
    status_healthy: "ఆరోగ్యకరమైనది",
    status_diseased: "వ్యాధి సోకినది",
    healthy_foliage: "ఆరోగ్యకరమైన పంట ఆకులు",
    action_plan_title: "వ్యవసాయ కార్యాచరణ ప్రణాళిక & చికిత్స",
    tab_immediate: "⚡ తక్షణ చర్య",
    tab_chemical: "🧪 రసాయన చికిత్స",
    tab_organic: "🍃 సేంద్రీయ / బయో చికిత్స",
    tab_prevention: "🛡️ నివారణ చర్యలు",
    immediate_healthy: "✓ సాధారణ నీటిపారుదల మరియు ఎరువుల నిర్వహణ కొనసాగించండి. ఎటువంటి మందులు పిచికారీ చేయవలసిన అవసరం లేదు.",
    immediate_diseased: "⚠️ వ్యాధి సోకిన పంట భాగాన్ని వేరు చేయండి. దెబ్బతిన్న ఆకులను కోసి సురక్షితంగా కాల్చివేయండి. తడి మొక్కలను ముట్టుకోవద్దు.",
    checklist_title: "పొలంలో రైతు చెక్‌లిస్ట్:",
    checklist_1: "వ్యాధి ప్రారంభ మచ్చల కోసం పక్క వరుసలను పరిశీలించండి",
    checklist_2: "తెగులు సోకిన ఆకులను కత్తిరించి నాశనం చేయండి",
    checklist_3: "సిఫార్సు చేసిన రక్షణ మందును సరైన సమయంలో పిచికారీ చేయండి",
    recent_scans_title: "ఇటీవలి పంట ఆరోగ్య స్కాన్లు",
    recent_scans_sub: "స్థానిక డేటాబేస్‌లో భద్రపరిచిన చారిత్రక రికార్డులు",
    empty_scans: "ఇంకా స్కాన్ రికార్డులు ఏవీ లేవు.",
    table_th_time: "సమయం",
    table_th_crop: "పంట",
    table_th_condition: "పరిస్థితి / వ్యాధి",
    table_th_confidence: "ఖచ్చితత్వం",
    table_th_status: "స్థితి",
    table_th_action: "చర్య",
    view_dossier: "పూర్తి నివేదిక →",
    view_all_history: "మొత్తం స్కాన్ల చరిత్ర చూడండి →",
    quick_stats_total: "మొత్తం స్కాన్లు",
    quick_stats_healthy: "ఆరోగ్యకరమైనవి",
    quick_stats_diseased: "తెగులు హెచ్చరికలు",
    quick_stats_accuracy: "సగటు ఖచ్చితత్వం",
    footer_text: "సర్క్యూట్ మేజ్ టీమ్ ద్వారా SIH 2026 కోసం రూపొందించబడింది · ఎడ్జ్ AI & IoT వ్యవసాయ సహాయకుడు",
    footer_disclaimer: "⚠ AI అంచనాలు కేవలం సహాయక సాధనాలు మాత్రమే — వ్యవసాయ శాస్త్రవేత్తల సలహాకు ప్రత్యామ్నాయం కాదు.",
    lang_changed_toast: "భాష తెలుగులోకి మార్చబడింది",
    speech_not_supported: "ఈ బ్రౌజర్‌లో వాయిస్ స్పీచ్ సదుపాయం అందుబాటులో లేదు.",
    crop_potato: "బంగాళాదుంప (Potato)",
    crop_rice: "వరి (Rice)",
    crop_wheat: "గోధుమ (Wheat)",
    crop_corn: "మొక్కజొన్న (Corn)",
    crop_sugarcane: "చెరకు (Sugarcane)"
  },

  ta: {
    lang_name: "தமிழ் (Tamil)",
    lang_code: "ta",
    speech_lang: "ta-IN",
    nav_dashboard: "📊 முகப்புப்பலகை",
    nav_analytics: "📈 பகுப்பாய்வு",
    nav_alerts: "🚨 எச்சரிக்கைகள்",
    nav_history: "📜 வரலாறு",
    nav_settings: "⚙️ அமைப்புகள்",
    brand_title: "கிசான் மித்ரா AI",
    brand_subtitle: "சர்க்யூட் மேஸ் · SIH 2026",
    env_normal: "இயல்பு",
    env_alert: "எச்சரிக்கை",
    telemetry_temp: "சுற்றுப்புற வெப்பநிலை",
    telemetry_hum: "ஈரப்பதம்",
    telemetry_soil: "மண் ஈரப்பதம் (VWC)",
    telemetry_gas: "காற்று தரம் (MQ-135)",
    telemetry_pump: "பாசன பம்ப்",
    telemetry_led: "எச்சரிக்கை LED",
    telemetry_soil_tag: "போதுமான ஈரப்பதம்",
    telemetry_gas_tag: "சுத்தமான காற்று",
    telemetry_hint_temp: "உகந்த பயிர் வளர்ச்சி: 20–30°C",
    telemetry_hint_hum: "பூஞ்சை நோய் அபாயம் >85%",
    telemetry_hint_soil: "தானியங்கி பாசனம் <30%",
    telemetry_hint_gas: "எச்சரிக்கை வரம்பு >350 ppm",
    telemetry_hint_pump: "தானியங்கி நிறுத்தம் இயங்குகிறது",
    telemetry_hint_led: "வரம்பை மீறும்போது ஒளிரும்",
    diag_studio_title: "AI பயிர் நோய் கண்டறிதல் மையம்",
    diag_studio_sub: "இணையம் தேவையில்லை · நேரடி AI மாதிரி",
    input_card_title: "பயிர் இலையின் நிலையை சோதிக்கவும்",
    input_card_sub: "புகைப்படம் எடுக்கவும், கோப்பை பதிவேற்றவும் அல்லது கேமராவைப் பயன்படுத்தவும்.",
    tab_upload: "📤 படம் பதிவேற்று",
    tab_webcam: "📱 கேமரா",
    tab_picam: "🤖 பை கேமரா",
    dropzone_prompt: "இலை புகைப்படத்தை இங்கே பதிவேற்றவும்",
    dropzone_sub: "JPG, PNG, WEBP, BMP ஆதரிக்கப்படுகிறது",
    btn_analyze: "AI நோய் பரிசோதனை செய்க",
    btn_analyzing: "🔬 பரிசோதிக்கிறது…",
    dossier_title: "நோய் கண்டறிதல் அறிக்கை",
    dossier_subtitle: "வேளாண் செயல் திட்டம் & சிகிச்சை அறிக்கை",
    btn_print: "🖨️ அச்சிடுக",
    btn_listen: "🔊 கேளுங்கள் (ஆடியோ)",
    btn_listening: "🔊 பேசுகிறது...",
    conf_label: "துல்லியம்",
    health_score_label: "பயிர் நலக் குறியீடு",
    risk_low: "குறைந்த ஆபத்து (ஆரோக்கியமானது)",
    risk_high: "அதிக ஆபத்து (உடனடி சிகிச்சை தேவை)",
    status_healthy: "ஆரோக்கியமானது",
    status_diseased: "நோய் பாதிப்பு",
    healthy_foliage: "ஆரோக்கியமான இலைகள்",
    action_plan_title: "வேளாண் செயல் திட்டம் & சிகிச்சை",
    tab_immediate: "⚡ உடனடி நடவடிக்கை",
    tab_chemical: "🧪 ரசாயன சிகிச்சை",
    tab_organic: "🍃 இயற்கை சிகிச்சை",
    tab_prevention: "🛡️ தடுப்பு முறைகள்",
    immediate_healthy: "✓ வழக்கமான பாசனம் மற்றும் உர மேலாண்மையைத் தொடரவும். மருந்து தெளிக்க வேண்டியதில்லை.",
    immediate_diseased: "⚠️ பாதிக்கப்பட்ட பகுதியைப் பிரிக்கவும். பாதிக்கப்பட்ட இலைகளை வெட்டி அழிக்கவும்.",
    checklist_title: "வயல்வெளி சரிபார்ப்பு பட்டியல்:",
    checklist_1: "அருகிலுள்ள வரிசைகளில் நோய் அறிகுறிகளை சோதிக்கவும்",
    checklist_2: "பாதிக்கப்பட்ட இலைகளை வெட்டி அழிக்கவும்",
    checklist_3: "பரிந்துரைக்கப்பட்ட மருந்தை சரியான நேரத்தில் தெளிக்கவும்",
    recent_scans_title: "சமீபத்திய பயிர் ஸ்கேன்கள்",
    recent_scans_sub: "உள்ளூர் தரவுத்தளத்தில் சேமிக்கப்பட்ட பதிவுகள்",
    empty_scans: "இன்னும் ஸ்கேன் பதிவுகள் எதுவும் இல்லை.",
    table_th_time: "நேரம்",
    table_th_crop: "பயிர்",
    table_th_condition: "நிலை / நோய்",
    table_th_confidence: "துல்லியம்",
    table_th_status: "நிலை",
    table_th_action: "நடவடிக்கை",
    view_dossier: "அறிக்கையைக் காண்க →",
    view_all_history: "முழு வரலாற்றைக் காண்க →",
    quick_stats_total: "மொத்த ஸ்கேன்கள்",
    quick_stats_healthy: "ஆரோக்கியமானவை",
    quick_stats_diseased: "நோய் எச்சரிக்கைகள்",
    quick_stats_accuracy: "சராசரி துல்லியம்",
    footer_text: "சர்க்யூட் மேஸ் குழுவால் SIH 2026 க்காக உருவாக்கப்பட்டது · AI & IoT வேளாண் உதவியாளர்",
    footer_disclaimer: "⚠ AI கணிப்புகள் முடிவெடுக்கும் துணைக்கருவி மட்டுமே.",
    lang_changed_toast: "மொழி தமிழுக்கு மாற்றப்பட்டது",
    speech_not_supported: "ஆடியோ வசதி கிடைக்கவில்லை.",
    crop_potato: "உருளைக்கிழங்கு",
    crop_rice: "நெல் / அரிசி",
    crop_wheat: "கோதுமை",
    crop_corn: "சோளம்",
    crop_sugarcane: "கரும்பு"
  },

  kn: {
    lang_name: "ಕನ್ನಡ (Kannada)",
    lang_code: "kn",
    speech_lang: "kn-IN",
    nav_dashboard: "📊 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    nav_analytics: "📈 ವಿಶ್ಲೇಷಣೆ",
    nav_alerts: "🚨 ಎಚ್ಚರಿಕೆಗಳು",
    nav_history: "📜 ಇತಿಹಾಸ",
    nav_settings: "⚙️ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
    brand_title: "ಕಿಸಾನ್ ಮಿತ್ರ AI",
    brand_subtitle: "ಸರ್ಕ್ಯೂಟ್ ಮೇಜ್ · SIH 2026",
    env_normal: "ಸಾಮಾನ್ಯ",
    env_alert: "ಎಚ್ಚರಿಕೆ",
    telemetry_temp: "ತಾಪಮಾನ",
    telemetry_hum: "ತೇವಾಂಶ",
    telemetry_soil: "ಮಣ್ಣಿನ ತೇವಾಂಶ (VWC)",
    telemetry_gas: "ಗಾಳಿಯ ಗುಣಮಟ್ಟ",
    telemetry_pump: "ನೀರಾವರಿ ಪಂಪ್",
    telemetry_led: "ಎಚ್ಚರಿಕೆ ಎಲ್ಇಡಿ",
    telemetry_soil_tag: "ಸಾಕಷ್ಟು ತೇವಾಂಶ",
    telemetry_gas_tag: "ಸ್ವಚ್ಛ ಗಾಳಿ",
    telemetry_hint_temp: "ಉತ್ತಮ ಬೆಳೆ ಬೆಳವಣಿಗೆ: 20–30°C",
    telemetry_hint_hum: "ಶಿಲೀಂಧ್ರ ರೋಗದ ಅಪಾಯ: >85%",
    telemetry_hint_soil: "ಸ್ವಯಂಚಾಲಿತ ನೀರಾವರಿ <30%",
    telemetry_hint_gas: "ಅಪಾಯದ ಮಟ್ಟ >350 ppm",
    telemetry_hint_pump: "ಸ್ವಯಂಚಾಲಿತ ನಿಯಂತ್ರಣ ಸಕ್ರಿಯವಾಗಿದೆ",
    telemetry_hint_led: "ಮಿತಿ ಮೀರಿದಾಗ ಬೆಳಗುತ್ತದೆ",
    diag_studio_title: "AI ಬೆಳೆ ರೋಗ ಪತ್ತೆ ಕೇಂದ್ರ",
    diag_studio_sub: "ಇಂಟರ್ನೆಟ್ ಇಲ್ಲದೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ",
    input_card_title: "ಬೆಳೆ ಎಲೆಯ ಸ್ಥಿತಿ ಪರೀಕ್ಷಿಸಿ",
    input_card_sub: "ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ, ಫೈಲ್ ಅಪ್ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಕ್ಯಾಮೆರಾ ಬಳಸಿ.",
    tab_upload: "📤 ಫೋಟೋ ಅಪ್ಲೋಡ್",
    tab_webcam: "📱 ಕ್ಯಾಮೆರಾ",
    tab_picam: "🤖 ಪೈ ಕ್ಯಾಮೆರಾ",
    dropzone_prompt: "ಎಲೆಯ ಫೋಟೋವನ್ನು ಇಲ್ಲಿ ಅಪ್ಲೋಡ್ ಮಾಡಿ",
    dropzone_sub: "JPG, PNG, WEBP, BMP ಬೆಂಬಲಿತವಾಗಿದೆ",
    btn_analyze: "AI ರೋಗ ಪರೀಕ್ಷೆ ನಡೆಸಿ",
    btn_analyzing: "🔬 ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ…",
    dossier_title: "ರೋಗ ನಿರ್ಣಯ ವರದಿ",
    dossier_subtitle: "ಕೃಷಿ ಕ್ರಿಯಾ ಯೋಜನೆ & ಚಿಕಿತ್ಸಾ ವರದಿ",
    btn_print: "🖨️ ಮುದ್ರಿಸಿ",
    btn_listen: "🔊 ಆಲಿಸಿ (ಆಡಿಯೋ)",
    btn_listening: "🔊 ಮಾತನಾಡುತ್ತಿದೆ...",
    conf_label: "ನಿಖರತೆ",
    health_score_label: "ಬೆಳೆ ಆರೋಗ್ಯ ಸೂಚ್ಯಂಕ",
    risk_low: "ಕಡಿಮೆ ಅಪಾಯ (ಆರೋಗ್ಯಕರ)",
    risk_high: "ಹೆಚ್ಚಿನ ಅಪಾಯ (ತಕ್ಷಣದ ಕ್ರಮ ಅಗತ್ಯ)",
    status_healthy: "ಆರೋಗ್ಯಕರ",
    status_diseased: "ರೋಗಪೀಡಿತ",
    healthy_foliage: "ಆರೋಗ್ಯಕರ ಎಲೆಗಳು",
    action_plan_title: "ಕೃಷಿ ಕ್ರಿಯಾ ಯೋಜನೆ ಮತ್ತು ಚಿಕಿತ್ಸೆ",
    tab_immediate: "⚡ ತಕ್ಷಣದ ಕ್ರಮ",
    tab_chemical: "🧪 ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ",
    tab_organic: "🍃 ಸಾವಯವ ಚಿಕಿತ್ಸೆ",
    tab_prevention: "🛡️ ತಡೆಗಟ್ಟುವ ಕ್ರಮಗಳು",
    immediate_healthy: "✓ ಸಾಮಾನ್ಯ ನೀರಾವರಿ ಮುಂದುವರಿಸಿ. ಯಾವುದೇ ಔಷಧ ಸಿಂಪಡಣೆ ಅಗತ್ಯವಿಲ್ಲ.",
    immediate_diseased: "⚠️ ಸೋಂಕಿತ ಭಾಗವನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ. ರೋಗಪೀಡಿತ ಎಲೆಗಳನ್ನು ನಾಶಮಾಡಿ.",
    checklist_title: "ರೈತರ ಪರಿಶೀಲನಾ ಪಟ್ಟಿ:",
    checklist_1: "ನೆರೆಯ ಸಾಲುಗಳಲ್ಲಿ ರೋಗದ ಲಕ್ಷಣಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ",
    checklist_2: "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ ನಾಶಮಾಡಿ",
    checklist_3: "ಶಿಫಾರಸು ಮಾಡಿದ ಔಷಧವನ್ನು ಸಮಯಕ್ಕೆ ಸಿಂಪಡಿಸಿ",
    recent_scans_title: "ಇತ್ತೀಚಿನ ಬೆಳೆ ಸ್ಕ್ಯಾನ್‌ಗಳು",
    recent_scans_sub: "ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಸಂಗ್ರಹಿಸಲಾದ ದಾಖಲೆಗಳು",
    empty_scans: "ಇನ್ನೂ ಯಾವುದೇ ಸ್ಕ್ಯಾನ್ ದಾಖಲೆಗಳಿಲ್ಲ.",
    table_th_time: "ಸಮಯ",
    table_th_crop: "ಬೆಳೆ",
    table_th_condition: "ರೋಗ / ಸ್ಥಿತಿ",
    table_th_confidence: "ನಿಖರತೆ",
    table_th_status: "ಸ್ಥಿತಿ",
    table_th_action: "ಕ್ರಮ",
    view_dossier: "ವರದಿ ವೀಕ್ಷಿಸಿ →",
    view_all_history: "ಎಲ್ಲಾ ಇತಿಹಾಸ ವೀಕ್ಷಿಸಿ →",
    quick_stats_total: "ಒಟ್ಟು ಸ್ಕ್ಯಾನ್‌ಗಳು",
    quick_stats_healthy: "ಆರೋಗ್ಯಕರ ಮಾದರಿಗಳು",
    quick_stats_diseased: "ರೋಗದ ಎಚ್ಚರಿಕೆಗಳು",
    quick_stats_accuracy: "ಸರಾಸರಿ ನಿಖರತೆ",
    footer_text: "ಸರ್ಕ್ಯೂಟ್ ಮೇಜ್ ತಂಡದಿಂದ SIH 2026 ಗಾಗಿ ಅಭಿವೃದ್ಧಿಪಡಿಸಲಾಗಿದೆ · ಕೃಷಿ AI ಸಹಾಯಕ",
    footer_disclaimer: "⚠ AI ಭವಿಷ್ಯವಾಣಿಗಳು ಕೇವಲ ಸಹಾಯಕ್ಕಾಗಿ ಮಾತ್ರ.",
    lang_changed_toast: "ಭಾಷೆಯನ್ನು ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗಿದೆ",
    speech_not_supported: "ಆಡಿಯೋ ಬೆಂಬಲವಿಲ್ಲ.",
    crop_potato: "ಆಲೂಗಡ್ಡೆ",
    crop_rice: "ಭತ್ತ / ಅಕ್ಕಿ",
    crop_wheat: "ಗೋಧಿ",
    crop_corn: "ಜೋಳ",
    crop_sugarcane: "ಕಬ್ಬು"
  },

  mr: {
    lang_name: "मराठी (Marathi)",
    lang_code: "mr",
    speech_lang: "mr-IN",
    nav_dashboard: "📊 डॅशबोर्ड",
    nav_analytics: "📈 विश्लेषण",
    nav_alerts: "🚨 सूचना",
    nav_history: "📜 इतिहास",
    nav_settings: "⚙️ सेटिंग्ज",
    brand_title: "किसान मित्र AI",
    brand_subtitle: "सर्किट मेझ · SIH 2026",
    env_normal: "सामान्य",
    env_alert: "सूचना / धोका",
    telemetry_temp: "तापमान",
    telemetry_hum: "हवेतील आर्द्रता",
    telemetry_soil: "मातीतील ओलावा (VWC)",
    telemetry_gas: "हवेची गुणवत्ता (MQ-135)",
    telemetry_pump: "सिंचन पंप",
    telemetry_led: "हार्डवेअर अलर्ट एलईडी",
    telemetry_soil_tag: "पुरेसा ओलावा",
    telemetry_gas_tag: "स्वच्छ हवा",
    telemetry_hint_temp: "योग्य पीक वाढ: 20–30°C",
    telemetry_hint_hum: "बुरशीजन्य रोगाचा धोका >85%",
    telemetry_hint_soil: "स्वयंचलित पाणी <30%",
    telemetry_hint_gas: "धोका पातळी >350 ppm",
    telemetry_hint_pump: "ऑटो-शटऑफ सुरू आहे",
    telemetry_hint_led: "मर्यादा ओलांडल्यावर सुरू होते",
    diag_studio_title: "AI पीक रोग निदान केंद्र",
    diag_studio_sub: "इंटरनेटशिवाय काम करणारे AI मॉडेल",
    input_card_title: "पिकाच्या पानांची तपासणी करा",
    input_card_sub: "फोटो घ्या, फाइल अपलोड करा किंवा कॅमेरा सुरू करा.",
    tab_upload: "📤 फोटो अपलोड",
    tab_webcam: "📱 कॅमेरा",
    tab_picam: "🤖 पाय कॅमेरा",
    dropzone_prompt: "पानाचा फोटो येथे टाका किंवा निवडा",
    dropzone_sub: "JPG, PNG, WEBP, BMP समर्थित",
    btn_analyze: "AI रोग विश्लेषण सुरू करा",
    btn_analyzing: "🔬 विश्लेषण चालू आहे…",
    dossier_title: "रोग निदान अहवाल (डोसियर)",
    dossier_subtitle: "कृषी कृती योजना आणि उपचार अहवाल",
    btn_print: "🖨️ अहवाल प्रिंट करा",
    btn_listen: "🔊 ऐका (ऑडिओ)",
    btn_listening: "🔊 बोलत आहे...",
    conf_label: "AI अचूकता",
    health_score_label: "पीक आरोग्य निर्देशांक",
    risk_low: "कमी धोका (निरोगी पीक)",
    risk_high: "जास्त धोका (तातडीने उपाय करा)",
    status_healthy: "निरोगी",
    status_diseased: "रोगट / संसर्गित",
    healthy_foliage: "निरोगी पाने",
    action_plan_title: "कृषी कृती योजना आणि उपचार",
    tab_immediate: "⚡ तात्काळ कृती",
    tab_chemical: "🧪 रासायनिक उपाय",
    tab_organic: "🍃 सेंद्रिय / जैविक उपचार",
    tab_prevention: "🛡️ प्रतिबंधात्मक उपाय",
    immediate_healthy: "✓ नेहमीचे पाणी आणि खत व्यवस्थापन सुरू ठेवा. फवारणीची गरज नाही.",
    immediate_diseased: "⚠️ बाधित झाडे वेगळी करा. रोगट पाने तोडून नष्ट करा.",
    checklist_title: "शेतकऱ्यांसाठी तपासणी यादी:",
    checklist_1: "शेजारील ओळींमध्ये रोगाची लक्षणे तपासा",
    checklist_2: "रोगट पाने छाटून नष्ट करा",
    checklist_3: "शिफारस केलेली औषधे वेळेवर फवारा",
    recent_scans_title: "नुकतेच केलेले पीक स्कॅन",
    recent_scans_sub: "स्थानिक डेटाबेसमध्ये साठवलेले रेकॉर्ड",
    empty_scans: "अद्याप कोणतेही स्कॅन रेकॉर्ड उपलब्ध नाहीत.",
    table_th_time: "वेळ",
    table_th_crop: "पीक",
    table_th_condition: "स्थिती / रोग",
    table_th_confidence: "अचूकता",
    table_th_status: "स्थिती",
    table_th_action: "कृती",
    view_dossier: "अहवाल पहा →",
    view_all_history: "पूर्ण इतिहास पहा →",
    quick_stats_total: "एकूण स्कॅन",
    quick_stats_healthy: "निरोगी नमुने",
    quick_stats_diseased: "रोगाच्या सूचना",
    quick_stats_accuracy: "सरासरी अचूकता",
    footer_text: "सर्किट मेझ टीमने SIH 2026 साठी विकसित केले · कृषी AI सहाय्यक",
    footer_disclaimer: "⚠ AI अंदाज फक्त मदतीसाठी आहेत.",
    lang_changed_toast: "भाषा मराठीत बदलली",
    speech_not_supported: "ऑडिओ उपलब्ध नाही.",
    crop_potato: "बटाटा",
    crop_rice: "भात / तांदूळ",
    crop_wheat: "गहू",
    crop_corn: "मका",
    crop_sugarcane: "ऊस"
  }
};

/**
 * Current Active Language (Default: English or from localStorage)
 */
let _currentLang = 'en';

/**
 * Helper to translate key
 */
function t(key, defaultVal = '') {
  const langDict = KISAN_I18N[_currentLang] || KISAN_I18N['en'];
  if (langDict && langDict[key]) {
    return langDict[key];
  }
  const enDict = KISAN_I18N['en'];
  if (enDict && enDict[key]) {
    return enDict[key];
  }
  return defaultVal || key;
}

/**
 * Apply translations to DOM elements with data-i18n attributes
 */
function applyTranslations(lang = null) {
  if (lang && KISAN_I18N[lang]) {
    _currentLang = lang;
  } else {
    const saved = localStorage.getItem('kisan_lang');
    if (saved && KISAN_I18N[saved]) {
      _currentLang = saved;
    }
  }

  const dict = KISAN_I18N[_currentLang] || KISAN_I18N['en'];

  // Update language selector dropdown if present
  const selectElem = document.getElementById('lang-select');
  if (selectElem && selectElem.value !== _currentLang) {
    selectElem.value = _currentLang;
  }
  const settingsSelect = document.getElementById('settings-lang-select');
  if (settingsSelect && settingsSelect.value !== _currentLang) {
    settingsSelect.value = _currentLang;
  }

  // Update all elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      // Check if element has child icons that should be preserved
      const iconSpan = el.querySelector('.heading-icon, .nav-icon, .btn-analyze-icon, .rec-icon, .rx-icon');
      if (iconSpan) {
        const iconClone = iconSpan.cloneNode(true);
        el.textContent = ' ' + dict[key];
        el.prepend(iconClone);
      } else {
        el.textContent = dict[key];
      }
    }
  });

  // Update placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) {
      el.setAttribute('placeholder', dict[key]);
    }
  });

  // Update titles/tooltips
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    if (dict[key]) {
      el.setAttribute('title', dict[key]);
    }
  });

  // Document language attribute
  document.documentElement.lang = _currentLang;
}

/**
 * Switch active language
 */
function changeLanguage(langCode) {
  if (!KISAN_I18N[langCode]) return;
  _currentLang = langCode;
  localStorage.setItem('kisan_lang', langCode);

  applyTranslations(langCode);

  if (typeof showToast === 'function') {
    showToast(t('lang_changed_toast', 'Language updated'), 'success', 2500);
  }
}

/**
 * Audio Assistant: Read out the diagnostic dossier & action plan in chosen language
 */
function speakDossier() {
  if (!('speechSynthesis' in window)) {
    if (typeof showToast === 'function') {
      showToast(t('speech_not_supported', 'Speech not supported'), 'warning');
    }
    return;
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  const listenBtn = document.getElementById('btn-listen-speech');
  if (listenBtn) {
    listenBtn.textContent = t('btn_listening', '🔊 Speaking...');
  }

  // Gather text from diagnosis and action plan
  const cropEl = document.querySelector('.dossier-crop, .diag-crop');
  const diseaseEl = document.querySelector('.dossier-disease, .diag-disease');
  const statusBadge = document.querySelector('.result-badge');
  const immediateEl = document.querySelector('#rx-pane-immediate .rx-text, .recommendation');

  const crop = cropEl ? cropEl.textContent.trim() : '';
  const disease = diseaseEl ? diseaseEl.textContent.trim() : '';
  const status = statusBadge ? statusBadge.textContent.trim() : '';
  const action = immediateEl ? immediateEl.textContent.trim() : '';

  let speechText = '';
  if (_currentLang === 'hi') {
    speechText = `किसान मित्र डायग्नोस्टिक रिपोर्ट. फसल: ${crop}. स्थिति: ${disease}. दर्जा: ${status}. तत्काल सलाह: ${action}`;
  } else if (_currentLang === 'te') {
    speechText = `కిసాన్ మిత్ర నివేదిక. పంట: ${crop}. వ్యాధి: ${disease}. పరిస్థితి: ${status}. తక్షణ సూచన: ${action}`;
  } else if (_currentLang === 'ta') {
    speechText = `கிசான் மித்ரா அறிக்கை. பயிர்: ${crop}. நிலை: ${disease}. உடனடி நடவடிக்கை: ${action}`;
  } else if (_currentLang === 'kn') {
    speechText = `ಕಿಸಾನ್ ಮಿತ್ರ ವರದಿ. ಬೆಳೆ: ${crop}. ರೋಗ: ${disease}. ತಕ್ಷಣದ ಸಲಹೆ: ${action}`;
  } else if (_currentLang === 'mr') {
    speechText = `किसान मित्र अहवाल. पीक: ${crop}. रोग: ${disease}. तात्काळ सल्ला: ${action}`;
  } else {
    speechText = `Kisan Mitra Diagnostic Report. Crop: ${crop}. Condition: ${disease}. Status: ${status}. Immediate action: ${action}`;
  }

  const utterance = new SpeechSynthesisUtterance(speechText);
  const dict = KISAN_I18N[_currentLang] || KISAN_I18N['en'];
  utterance.lang = dict.speech_lang || 'en-IN';
  utterance.rate = 0.92; // Slightly slower for clarity
  utterance.pitch = 1.0;

  utterance.onend = () => {
    if (listenBtn) {
      listenBtn.textContent = t('btn_listen', '🔊 Listen (Audio)');
    }
  };

  utterance.onerror = () => {
    if (listenBtn) {
      listenBtn.textContent = t('btn_listen', '🔊 Listen (Audio)');
    }
  };

  window.speechSynthesis.speak(utterance);
}

// Auto-run on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  applyTranslations();
});
