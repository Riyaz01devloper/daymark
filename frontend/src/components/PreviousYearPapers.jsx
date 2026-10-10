import { useState, useEffect } from "react";
import { apiRequest } from "../api/client.js";

const OFFICIAL_PAPERS_BY_CLASS_EN = {
  10: [
    {
      year: "2024–25",
      title: "Class 10 CBSE Sample Question Papers & Marking Scheme",
      description: "Official board sample papers and answer key marking scheme released by CBSE Academic.",
      url: "https://cbseacademic.nic.in/SQP_CLASSX_2024-25.html",
      badge: "2024-25 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2023–24",
      title: "Class 10 CBSE Sample Question Papers & Solutions",
      description: "Official previous session board sample question papers and evaluation marking scheme.",
      url: "https://cbseacademic.nic.in/SQP_CLASSX_2023-24.html",
      badge: "2023-24 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2022–23",
      title: "Class 10 CBSE Previous Year Question Papers & MS",
      description: "Official questions with step-by-step marking schemes across all subjects.",
      url: "https://cbseacademic.nic.in/sqp_classx_2022-23.html",
      badge: "2022-23 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2021–22",
      title: "Class 10 CBSE Term 1 & Term 2 Question Papers",
      description: "Archived Term 1 MCQ papers and Term 2 subjective papers with answer keys.",
      url: "https://cbseacademic.nic.in/sqp_classx_2021-22.html",
      badge: "2021-22 Term 1 & 2",
      type: "official-cbse",
    },
    {
      year: "All Years Archive",
      title: "CBSE Official Board Question Papers Repository",
      description: "Direct official board question papers in ZIP/PDF for Class X (2018–2024 Main & Compartment).",
      url: "https://www.cbse.gov.in/cbsenew/question-paper.html",
      badge: "CBSE Official Portal",
      type: "official-portal",
    },
    {
      year: "Question Bank",
      title: "CBSE Official Class 10 Question Bank",
      description: "Chapter-wise case study, competency, and assertion-reasoning question bank.",
      url: "https://cbseacademic.nic.in/qbclass10.html",
      badge: "CBSE QB",
      type: "official-cbse",
    },
  ],
  12: [
    {
      year: "2024–25",
      title: "Class 12 CBSE Sample Question Papers & Marking Scheme",
      description: "Official board sample papers and marking schemes for Science, Commerce, and Arts streams.",
      url: "https://cbseacademic.nic.in/SQP_CLASSXII_2024-25.html",
      badge: "2024-25 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2023–24",
      title: "Class 12 CBSE Sample Question Papers & Solutions",
      description: "Official previous year sample question papers and answers key marking scheme.",
      url: "https://cbseacademic.nic.in/SQP_CLASSXII_2023-24.html",
      badge: "2023-24 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2022–23",
      title: "Class 12 CBSE Previous Year Question Papers & MS",
      description: "Subject-wise question papers and marking schemes across Science, Commerce & Humanities.",
      url: "https://cbseacademic.nic.in/sqp_classxii_2022-23.html",
      badge: "2022-23 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2021–22",
      title: "Class 12 CBSE Term 1 & Term 2 Question Papers",
      description: "Term-wise question papers and marking schemes for all major subjects.",
      url: "https://cbseacademic.nic.in/sqp_classxii_2021-22.html",
      badge: "2021-22 Term 1 & 2",
      type: "official-cbse",
    },
    {
      year: "All Years Archive",
      title: "CBSE Official Board Question Papers Repository",
      description: "Direct official board question papers in ZIP/PDF for Class XII (2018–2024 Main & Compartment).",
      url: "https://www.cbse.gov.in/cbsenew/question-paper.html",
      badge: "CBSE Official Portal",
      type: "official-portal",
    },
    {
      year: "Question Bank",
      title: "CBSE Official Class 12 Question Bank",
      description: "Official question bank with conceptual and higher-order thinking skill (HOTS) questions.",
      url: "https://cbseacademic.nic.in/qbclass12.html",
      badge: "CBSE QB",
      type: "official-cbse",
    },
  ],
};

const OFFICIAL_PAPERS_BY_CLASS_HI = {
  10: [
    {
      year: "2024–25",
      title: "कक्षा 10 सीबीएसई मॉडल प्रश्न पत्र एवं अंकन योजना",
      description: "सीबीएसई एकेडमिक द्वारा जारी आधिकारिक बोर्ड मॉडल प्रश्न पत्र और उत्तर अंकन योजना।",
      url: "https://cbseacademic.nic.in/SQP_CLASSX_2024-25.html",
      badge: "2024-25 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2023–24",
      title: "कक्षा 10 सीबीएसई मॉडल प्रश्न पत्र एवं समाधान",
      description: "पूर्व सत्र के आधिकारिक बोर्ड मॉडल प्रश्न पत्र एवं मूल्यांकन अंकन योजना।",
      url: "https://cbseacademic.nic.in/SQP_CLASSX_2023-24.html",
      badge: "2023-24 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2022–23",
      title: "कक्षा 10 सीबीएसई विगत वर्ष प्रश्न पत्र एवं अंकन योजना",
      description: "सभी विषयों के चरण-दर-चरण अंकन योजना के साथ आधिकारिक प्रश्न।",
      url: "https://cbseacademic.nic.in/sqp_classx_2022-23.html",
      badge: "2022-23 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2021–22",
      title: "कक्षा 10 सीबीएसई टर्म 1 एवं टर्म 2 प्रश्न पत्र",
      description: "उत्तर कुंजी सहित टर्म 1 बहुविकल्पीय एवं टर्म 2 वर्णनात्मक प्रश्न पत्र।",
      url: "https://cbseacademic.nic.in/sqp_classx_2021-22.html",
      badge: "2021-22 Term 1 & 2",
      type: "official-cbse",
    },
    {
      year: "सभी वर्ष संग्रह",
      title: "सीबीएसई आधिकारिक बोर्ड प्रश्न पत्र रिपॉजिटरी",
      description: "कक्षा 10 (2018–2024 मुख्य एवं कंपार्टमेंट) के लिए सीधे आधिकारिक बोर्ड प्रश्न पत्र ज़िप/पीडीएफ में।",
      url: "https://www.cbse.gov.in/cbsenew/question-paper.html",
      badge: "सीबीएसई आधिकारिक पोर्टल",
      type: "official-portal",
    },
    {
      year: "प्रश्न बैंक",
      title: "सीबीएसई आधिकारिक कक्षा 10 प्रश्न बैंक",
      description: "अध्याय-वार केस स्टडी, योग्यता-आधारित और अभिकथन-कारण प्रश्न बैंक।",
      url: "https://cbseacademic.nic.in/qbclass10.html",
      badge: "सीबीएसई प्रश्न बैंक",
      type: "official-cbse",
    },
  ],
  12: [
    {
      year: "2024–25",
      title: "कक्षा 12 सीबीएसई मॉडल प्रश्न पत्र एवं अंकन योजना",
      description: "विज्ञान, वाणिज्य और कला संकायों के लिए आधिकारिक बोर्ड मॉडल प्रश्न पत्र और अंकन योजना।",
      url: "https://cbseacademic.nic.in/SQP_CLASSXII_2024-25.html",
      badge: "2024-25 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2023–24",
      title: "कक्षा 12 सीबीएसई मॉडल प्रश्न पत्र एवं समाधान",
      description: "पूर्व सत्र के आधिकारिक बोर्ड मॉडल प्रश्न पत्र और उत्तर कुंजी अंकन योजना।",
      url: "https://cbseacademic.nic.in/SQP_CLASSXII_2023-24.html",
      badge: "2023-24 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2022–23",
      title: "कक्षा 12 सीबीएसई विगत वर्ष प्रश्न पत्र एवं अंकन योजना",
      description: "विज्ञान, वाणिज्य और मानविकी संकायों में विषय-वार प्रश्न पत्र और अंकन योजना।",
      url: "https://cbseacademic.nic.in/sqp_classxii_2022-23.html",
      badge: "2022-23 SQP + MS",
      type: "official-cbse",
    },
    {
      year: "2021–22",
      title: "कक्षा 12 सीबीएसई टर्म 1 एवं टर्म 2 प्रश्न पत्र",
      description: "सभी प्रमुख विषयों के लिए टर्म-वार प्रश्न पत्र और अंकन योजना।",
      url: "https://cbseacademic.nic.in/sqp_classxii_2021-22.html",
      badge: "2021-22 Term 1 & 2",
      type: "official-cbse",
    },
    {
      year: "सभी वर्ष संग्रह",
      title: "सीबीएसई आधिकारिक बोर्ड प्रश्न पत्र रिपॉजिटरी",
      description: "कक्षा 12 (2018–2024 मुख्य एवं कंपार्टमेंट) के लिए सीधे आधिकारिक बोर्ड प्रश्न पत्र ज़िप/पीडीएफ में।",
      url: "https://www.cbse.gov.in/cbsenew/question-paper.html",
      badge: "सीबीएसई आधिकारिक पोर्टल",
      type: "official-portal",
    },
    {
      year: "प्रश्न बैंक",
      title: "सीबीएसई आधिकारिक कक्षा 12 प्रश्न बैंक",
      description: "अवधारणात्मक और उच्च स्तरीय चिंतन कौशल (HOTS) प्रश्नों के साथ आधिकारिक प्रश्न बैंक।",
      url: "https://cbseacademic.nic.in/qbclass12.html",
      badge: "सीबीएसई प्रश्न बैंक",
      type: "official-cbse",
    },
  ],
};

const NCERT_BOOK_LINKS_EN = [
  {
    title: "Official NCERT Textbooks Online Portal (Classes 1–12)",
    description: "Official government portal to read or download complete textbooks or chapter PDFs for any class.",
    url: "https://ncert.nic.in/textbook.php",
    badge: "Official NCERT PDF",
    action: "Download NCERT Books",
  },
  {
    title: "Official NCERT e-Books Portal",
    description: "Complete catalog of digitized textbooks, flipbooks, and ePub versions from NCERT.",
    url: "https://ncert.nic.in/ebooks.php",
    badge: "e-Books Hub",
    action: "Access e-Books",
  },
  {
    title: "Official NCERT Exemplar Problems (Classes 6–12)",
    description: "High-yield practice problems, MCQs, and detailed conceptual questions for board exams & NEET/JEE.",
    url: "https://ncert.nic.in/exemplar-problems.php",
    badge: "Exemplar Problems",
    action: "View Exemplars",
  },
  {
    title: "DIKSHA / PM eVIDYA Digital Textbooks Portal",
    description: "National repository for CBSE & NCERT curriculum with interactive digital books & QR codes.",
    url: "https://diksha.gov.in/",
    badge: "PM eVIDYA",
    action: "Open DIKSHA",
  },
];

const NCERT_BOOK_LINKS_HI = [
  {
    title: "आधिकारिक NCERT पाठ्यपुस्तक पोर्टल (कक्षा 1–12)",
    description: "किसी भी कक्षा के लिए संपूर्ण पाठ्यपुस्तक या अध्याय PDF पढ़ने या डाउनलोड करने का आधिकारिक सरकारी पोर्टल।",
    url: "https://ncert.nic.in/textbook.php",
    badge: "आधिकारिक NCERT PDF",
    action: "NCERT पुस्तकें डाउनलोड करें",
  },
  {
    title: "आधिकारिक NCERT ई-बुक्स पोर्टल",
    description: "NCERT की सभी डिजिटल पाठ्यपुस्तकों, फ्लिपबुक्स और ePub संस्करणों का संपूर्ण कैटलॉग।",
    url: "https://ncert.nic.in/ebooks.php",
    badge: "ई-बुक्स केंद्र",
    action: "ई-बुक्स देखें",
  },
  {
    title: "आधिकारिक NCERT प्रश्न प्रदर्शिका (एक्जम्प्लर - कक्षा 6–12)",
    description: "बोर्ड परीक्षाओं, NEET और JEE हेतु उच्च-स्तरीय अभ्यास प्रश्न, MCQs और विस्तृत अवधारणात्मक प्रश्न।",
    url: "https://ncert.nic.in/exemplar-problems.php",
    badge: "एक्जम्प्लर प्रश्न",
    action: "एक्जम्प्लर देखें",
  },
  {
    title: "दीक्षा (DIKSHA) / पीएम ई-विद्या डिजिटल पाठ्यपुस्तक पोर्टल",
    description: "इंटरैक्टिव डिजिटल पाठ्यपुस्तकों और क्यूआर कोड के साथ सीबीएसई और एनसीईआरटी पाठ्यक्रम का राष्ट्रीय पोर्टल।",
    url: "https://diksha.gov.in/",
    badge: "पीएम ई-विद्या",
    action: "दीक्षा खोलें",
  },
];

const DEFAULT_SUBJECTS_MAP_EN = {
  1: ["Mathematics", "Environmental Studies", "English"],
  2: ["Mathematics", "Environmental Studies", "English"],
  3: ["Mathematics", "Environmental Studies", "English"],
  4: ["Mathematics", "Environmental Studies", "English"],
  5: ["Mathematics", "Environmental Studies", "English"],
  6: ["Science", "Mathematics", "Social Science", "English"],
  7: ["Science", "Mathematics", "Social Science", "English"],
  8: ["Science", "Mathematics", "Social Science", "English"],
  9: ["Science", "Mathematics", "Social Science", "English"],
  10: ["Science", "Mathematics", "Social Science", "English"],
  11: ["Physics", "Chemistry", "Mathematics"],
  12: ["Physics", "Chemistry", "Mathematics", "Biology"],
};

const DEFAULT_SUBJECTS_MAP_HI = {
  1: ["गणित", "पर्यावरण अध्ययन", "अंग्रेजी"],
  2: ["गणित", "पर्यावरण अध्ययन", "अंग्रेजी"],
  3: ["गणित", "पर्यावरण अध्ययन", "अंग्रेजी"],
  4: ["गणित", "पर्यावरण अध्ययन", "अंग्रेजी"],
  5: ["गणित", "पर्यावरण अध्ययन", "अंग्रेजी"],
  6: ["विज्ञान", "गणित", "सामाजिक विज्ञान", "अंग्रेजी"],
  7: ["विज्ञान", "गणित", "सामाजिक विज्ञान", "अंग्रेजी"],
  8: ["विज्ञान", "गणित", "सामाजिक विज्ञान", "अंग्रेजी"],
  9: ["विज्ञान", "गणित", "सामाजिक विज्ञान", "अंग्रेजी"],
  10: ["विज्ञान", "गणित", "सामाजिक विज्ञान", "अंग्रेजी"],
  11: ["भौतिक विज्ञान", "रसायन विज्ञान", "गणित"],
  12: ["भौतिक विज्ञान", "रसायन विज्ञान", "गणित", "जीव विज्ञान"],
};

const EN_TO_HI_SUBJECTS = {
  "Science": "विज्ञान",
  "Mathematics": "गणित",
  "Social Science": "सामाजिक विज्ञान",
  "English": "अंग्रेजी",
  "Environmental Studies": "पर्यावरण अध्ययन",
  "Physics": "भौतिक विज्ञान",
  "Chemistry": "रसायन विज्ञान",
  "Biology": "जीव विज्ञान",
};

const HI_TO_EN_SUBJECTS = {
  "विज्ञान": "Science",
  "गणित": "Mathematics",
  "सामाजिक विज्ञान": "Social Science",
  "अंग्रेजी": "English",
  "पर्यावरण अध्ययन": "Environmental Studies",
  "भौतिक विज्ञान": "Physics",
  "रसायन विज्ञान": "Chemistry",
  "जीव विज्ञान": "Biology",
};

const UI_STRINGS = {
  en: {
    hubTitle: "NCERT & CBSE Study Hub (Classes 1–12)",
    hubSubtitle: "High-yield notes, animated concept videos, and verified CBSE / NCERT exam resources for all classes, subjects & chapters",
    collapse: "Collapse ▲",
    explore: "Explore Study Hub ▼",
    selectClass: "Select Class:",
    classPrefix: "Class",
    tabVideosNotes: "🎥 Animated Videos & Notes",
    tabPyqs: "📅 Previous Year Papers",
    tabBooks: "📖 Official NCERT Books",
    subjectLabel: "Subject:",
    searchPlaceholder: (cls, sub) => `Search Class ${cls} ${sub} chapters (e.g. Electricity, Light)...`,
    clearFilter: "Clear Filter",
    showingChapters: (count, cls, sub) => `Showing ${count} chapters for Class ${cls} ${sub}`,
    featureHint: "🎬 Each chapter includes animated concept videos, revision notes & NCERT book links",
    loadingResources: (cls, sub) => `Loading Class ${cls} ${sub} curriculum & resources...`,
    noChaptersFound: (query) => `No chapters found matching "${query}".`,
    chapterPrefix: "Ch",
    animatedVideo: "Animated Video ↗",
    dikshaPortal: "DIKSHA eVIDYA ↗",
    ncertPdf: "NCERT PDF ↗",
    viewNotes: "View Notes ▼",
    hideNotes: "Hide Notes ▲",
    revisionNotesTitle: (ch) => `NCERT Revision Notes: ${ch}`,
    copyNotes: "📋 Copy Notes",
    copied: "✓ Copied!",
    keyTakeaways: "Key Exam Takeaways:",
    generateAiNotes: "🤖 Generate In-depth AI Notes",
    generatingAiNotes: "Generating AI Notes...",
    aiNoteSuccess: "✓ Deep-dive AI study note generated and saved to your Study Hub!",
    aiNoteFallback: "Full NCERT summary notes are ready above. Set GEMINI_API_KEY in .env for dynamic AI generation.",
    openOfficialPaper: "Open Official Paper ↗",
    footerSecureNote: "🛡️ All official links redirect securely to government and verified portals: cbse.gov.in, cbseacademic.nic.in, ncert.nic.in, diksha.gov.in, and YouTube educational channels.",
    langSwitchLabel: "Language / भाषा:",
  },
  hi: {
    hubTitle: "NCERT और CBSE अध्ययन केंद्र (कक्षा 1–12)",
    hubSubtitle: "सभी कक्षाओं, विषयों और अध्यायों के लिए आधिकारिक NCERT परीक्षा नोट्स, एनिमेटेड वीडियो और सत्यापित संसाधन",
    collapse: "संक्षिप्त करें ▲",
    explore: "अध्ययन केंद्र खोलें ▼",
    selectClass: "कक्षा चुनें:",
    classPrefix: "कक्षा",
    tabVideosNotes: "🎥 एनिमेटेड वीडियो एवं नोट्स",
    tabPyqs: "📅 विगत वर्षों के प्रश्न पत्र (PYQs)",
    tabBooks: "📖 आधिकारिक NCERT पाठ्यपुस्तकें",
    subjectLabel: "विषय:",
    searchPlaceholder: (cls, sub) => `कक्षा ${cls} ${sub} के अध्याय खोजें (उदा. रासायनिक अभिक्रियाएँ, विद्युत)...`,
    clearFilter: "फ़िल्टर हटाएं",
    showingChapters: (count, cls, sub) => `कक्षा ${cls} ${sub} के लिए ${count} अध्याय उपलब्ध`,
    featureHint: "🎬 प्रत्येक अध्याय में एनिमेटेड वीडियो, पाठ्यपुस्तक नोट्स और NCERT पुस्तकें सम्मिलित हैं",
    loadingResources: (cls, sub) => `कक्षा ${cls} ${sub} का पाठ्यक्रम व संसाधन लोड हो रहे हैं...`,
    noChaptersFound: (query) => `"${query}" से मेल खाने वाला कोई अध्याय नहीं मिला।`,
    chapterPrefix: "अध्याय",
    animatedVideo: "एनिमेटेड वीडियो ↗",
    dikshaPortal: "दीक्षा ई-विद्या ↗",
    ncertPdf: "NCERT पुस्तक PDF ↗",
    viewNotes: "नोट्स देखें ▼",
    hideNotes: "नोट्स छिपाएँ ▲",
    revisionNotesTitle: (ch) => `NCERT पुनरावृत्ति नोट्स: ${ch}`,
    copyNotes: "📋 नोट्स कॉपी करें",
    copied: "✓ कॉपी हो गया!",
    keyTakeaways: "परीक्षा हेतु महत्वपूर्ण मुख्य बिंदु:",
    generateAiNotes: "🤖 गहन AI नोट्स तैयार करें",
    generatingAiNotes: "AI नोट्स तैयार हो रहे हैं...",
    aiNoteSuccess: "✓ गहन AI अध्ययन नोट्स तैयार होकर आपके स्टडी हब में सुरक्षित हो गए!",
    aiNoteFallback: "आधिकारिक NCERT सारांश नोट्स ऊपर उपलब्ध हैं। गतिशील AI निर्माण हेतु .env में GEMINI_API_KEY सेट करें।",
    openOfficialPaper: "आधिकारिक प्रश्न पत्र खोलें ↗",
    footerSecureNote: "🛡️ सभी आधिकारिक लिंक सरकारी पोर्टल पर सुरक्षित रूप से ले जाते हैं: cbse.gov.in, cbseacademic.nic.in, ncert.nic.in, diksha.gov.in, एवं YouTube शैक्षिक चैनल।",
    langSwitchLabel: "भाषा / Language:",
  },
};

export default function PreviousYearPapers({ userGrade = 10, language = "en", onLanguageChange }) {
  const [activeClass, setActiveClass] = useState(userGrade || 10);
  const [activeTab, setActiveTab] = useState("videos_notes"); // "videos_notes" | "pyqs" | "books"
  const [isExpanded, setIsExpanded] = useState(true);

  const strings = UI_STRINGS[language] || UI_STRINGS.en;

  // Chapter resources state
  const initialSubjects =
    (language === "hi" ? DEFAULT_SUBJECTS_MAP_HI : DEFAULT_SUBJECTS_MAP_EN)[userGrade || 10] ||
    (language === "hi" ? ["विज्ञान", "गणित"] : ["Science", "Mathematics"]);

  const [availableSubjects, setAvailableSubjects] = useState(initialSubjects);
  const [activeSubject, setActiveSubject] = useState(initialSubjects[0]);
  const [chapterResources, setChapterResources] = useState([]);
  const [loadingResources, setLoadingResources] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedNotes, setExpandedNotes] = useState({});
  const [copiedChapter, setCopiedChapter] = useState(null);
  const [generatingAiNote, setGeneratingAiNote] = useState(null);
  const [aiNoteFeedback, setAiNoteFeedback] = useState({});

  // Synchronize when activeClass or language changes
  useEffect(() => {
    let isMounted = true;
    const defaultMap = language === "hi" ? DEFAULT_SUBJECTS_MAP_HI : DEFAULT_SUBJECTS_MAP_EN;
    const fallbackSubjects =
      defaultMap[activeClass] || (language === "hi" ? ["विज्ञान", "गणित"] : ["Science", "Mathematics"]);

    // Fetch curriculum subjects for this class in selected language
    apiRequest(`/study/curriculum?class_grade=${activeClass}&language=${language}`)
      .then((res) => {
        if (!isMounted) return;
        const subs = res?.curriculum ? Object.keys(res.curriculum) : fallbackSubjects;
        const finalSubs = subs.length > 0 ? subs : fallbackSubjects;
        setAvailableSubjects(finalSubs);
        setActiveSubject((prev) => {
          if (finalSubs.includes(prev)) return prev;
          const translated =
            language === "hi" ? EN_TO_HI_SUBJECTS[prev] : HI_TO_EN_SUBJECTS[prev];
          if (translated && finalSubs.includes(translated)) return translated;
          return finalSubs[0] || fallbackSubjects[0];
        });
      })
      .catch(() => {
        if (!isMounted) return;
        setAvailableSubjects(fallbackSubjects);
        setActiveSubject((prev) => {
          if (fallbackSubjects.includes(prev)) return prev;
          const translated =
            language === "hi" ? EN_TO_HI_SUBJECTS[prev] : HI_TO_EN_SUBJECTS[prev];
          if (translated && fallbackSubjects.includes(translated)) return translated;
          return fallbackSubjects[0];
        });
      });

    return () => {
      isMounted = false;
    };
  }, [activeClass, language]);

  // Fetch chapter resources when activeClass, activeSubject, or language changes
  useEffect(() => {
    if (!activeSubject) return;
    let isMounted = true;
    setLoadingResources(true);

    apiRequest(
      `/study/chapter-resources?class_grade=${activeClass}&subject=${encodeURIComponent(
        activeSubject
      )}&language=${language}`
    )
      .then((res) => {
        if (!isMounted) return;
        setChapterResources(Array.isArray(res) ? res : []);
        setLoadingResources(false);
      })
      .catch(() => {
        if (!isMounted) return;
        setChapterResources([]);
        setLoadingResources(false);
      });

    return () => {
      isMounted = false;
    };
  }, [activeClass, activeSubject, language]);

  function toggleNotes(chapter) {
    setExpandedNotes((prev) => ({
      ...prev,
      [chapter]: !prev[chapter],
    }));
  }

  function handleCopyNotes(chapterName, notesText) {
    navigator.clipboard
      ?.writeText(notesText)
      .then(() => {
        setCopiedChapter(chapterName);
        setTimeout(() => setCopiedChapter(null), 2500);
      })
      .catch(() => {});
  }

  async function handleGenerateAiNotes(chapterName) {
    setGeneratingAiNote(chapterName);
    setAiNoteFeedback((prev) => ({ ...prev, [chapterName]: { status: "loading" } }));

    try {
      await apiRequest("/study/generate-notes", {
        method: "POST",
        body: JSON.stringify({
          subject: activeSubject,
          chapter: chapterName,
          language: language,
        }),
      });
      setAiNoteFeedback((prev) => ({
        ...prev,
        [chapterName]: {
          status: "success",
          msg: strings.aiNoteSuccess,
        },
      }));
    } catch (err) {
      setAiNoteFeedback((prev) => ({
        ...prev,
        [chapterName]: {
          status: "error",
          msg: err.message?.includes("503")
            ? strings.aiNoteFallback
            : (language === "hi"
                ? `AI नोट्स उत्पन्न नहीं हो सके: ${err.message}`
                : `Could not generate AI notes: ${err.message}`),
        },
      }));
    } finally {
      setGeneratingAiNote(null);
    }
  }

  // Determine papers to display
  const papersByClass = language === "hi" ? OFFICIAL_PAPERS_BY_CLASS_HI : OFFICIAL_PAPERS_BY_CLASS_EN;
  const papers =
    papersByClass[activeClass] || [
      {
        year: language === "hi" ? "वार्षिक / बोर्ड संग्रह" : "Annual / Board Archive",
        title:
          language === "hi"
            ? `सीबीएसई आधिकारिक प्रश्न पत्र पोर्टल (कक्षा ${activeClass})`
            : `CBSE Official Question Papers Portal (Class ${activeClass})`,
        description:
          language === "hi"
            ? "सीबीएसई से आधिकारिक बोर्ड प्रश्न पत्र और अंकन योजना संग्रह।"
            : "Official board question papers and marking scheme archive from CBSE.",
        url: "https://www.cbse.gov.in/cbsenew/question-paper.html",
        badge: language === "hi" ? "आधिकारिक सीबीएसई" : "Official CBSE",
        type: "official-portal",
      },
      {
        year: language === "hi" ? "अभ्यास एवं मूल्यांकन" : "Practice & Assessment",
        title:
          language === "hi"
            ? `सीबीएसई योग्यता अभ्यास प्रश्न (कक्षा ${activeClass})`
            : `CBSE Competency Practice Questions (Class ${activeClass})`,
        description:
          language === "hi"
            ? "आधिकारिक योग्यता-आधारित मूल्यांकन और शिक्षण प्रश्न।"
            : "Official competency-based assessment and learning questions.",
        url: "https://cbseacademic.nic.in/cbe/",
        badge: language === "hi" ? "सीबीएसई मूल्यांकन" : "CBSE Assessment",
        type: "official-cbse",
      },
      {
        year: language === "hi" ? "पाठ्यक्रम" : "Curriculum",
        title:
          language === "hi"
            ? `सीबीएसई आधिकारिक पाठ्यक्रम एवं सिलेबस`
            : `CBSE Official Curriculum & Syllabus`,
        description:
          language === "hi"
            ? "नवीनतम पाठ्यक्रम, मॉडल प्रश्न दिशानिर्देश और ब्लूप्रिंट।"
            : "Latest curriculum, sample question guidelines, and course blueprints.",
        url: "https://cbseacademic.nic.in/curriculum_2025.html",
        badge: language === "hi" ? "पाठ्यक्रम" : "Curriculum",
        type: "official-cbse",
      },
    ];

  const bookLinks = language === "hi" ? NCERT_BOOK_LINKS_HI : NCERT_BOOK_LINKS_EN;

  // Filtered chapters for current search
  const filteredChapters = chapterResources.filter((res) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      res.chapter?.toLowerCase().includes(q) ||
      res.summary_notes?.toLowerCase().includes(q) ||
      res.key_takeaways?.some((t) => t.toLowerCase().includes(q))
    );
  });

  return (
    <section className="pyq-hub-section" aria-labelledby="study-hub-heading">
      <div className="pyq-hub-header">
        <div className="pyq-hub-title-group">
          <span className="pyq-hub-icon" aria-hidden="true">
            📚
          </span>
          <div>
            <h3 id="study-hub-heading" className="pyq-hub-title">
              {strings.hubTitle}
            </h3>
            <p className="pyq-hub-subtitle">
              {strings.hubSubtitle}
            </p>
          </div>
        </div>

        <button
          type="button"
          className="pyq-toggle-btn"
          onClick={() => setIsExpanded((prev) => !prev)}
          aria-expanded={isExpanded}
        >
          {isExpanded ? strings.collapse : strings.explore}
        </button>
      </div>

      {isExpanded && (
        <div className="pyq-hub-body">
          {/* Controls: Class switcher, Language switcher, and Tab buttons */}
          <div className="pyq-hub-toolbar">
            <div className="pyq-class-selector-wrapper">
              <span className="pyq-toolbar-label">{strings.selectClass}</span>
              <div className="pyq-class-selector" role="group" aria-label={strings.selectClass}>
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((cls) => (
                  <button
                    key={cls}
                    type="button"
                    className={`pyq-class-pill ${activeClass === cls ? "is-active" : ""}`}
                    onClick={() => setActiveClass(cls)}
                  >
                    {strings.classPrefix} {cls}
                  </button>
                ))}
              </div>
            </div>

            {/* Language Switcher in Study Hub */}
            <div className="pyq-lang-selector" role="group" aria-label={strings.langSwitchLabel}>
              <span className="pyq-toolbar-label">{strings.langSwitchLabel}</span>
              <button
                type="button"
                className={`pyq-lang-pill ${language === "en" ? "is-active" : ""}`}
                onClick={() => onLanguageChange && onLanguageChange("en")}
              >
                English
              </button>
              <button
                type="button"
                className={`pyq-lang-pill ${language === "hi" ? "is-active" : ""}`}
                onClick={() => onLanguageChange && onLanguageChange("hi")}
              >
                हिंदी
              </button>
            </div>

            <div className="pyq-tab-buttons" role="tablist">
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === "videos_notes"}
                className={`pyq-tab-btn ${activeTab === "videos_notes" ? "is-active" : ""}`}
                onClick={() => setActiveTab("videos_notes")}
              >
                {strings.tabVideosNotes}
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === "pyqs"}
                className={`pyq-tab-btn ${activeTab === "pyqs" ? "is-active" : ""}`}
                onClick={() => setActiveTab("pyqs")}
              >
                {strings.tabPyqs}
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === "books"}
                className={`pyq-tab-btn ${activeTab === "books" ? "is-active" : ""}`}
                onClick={() => setActiveTab("books")}
              >
                {strings.tabBooks}
              </button>
            </div>
          </div>

          {/* TAB 1: Video Animations and Chapter Notes */}
          {activeTab === "videos_notes" && (
            <div className="study-notes-tab-content">
              {/* Subject Selector & Search Bar */}
              <div className="study-sub-nav">
                <div className="study-subjects-row" role="group" aria-label={strings.subjectLabel}>
                  <span className="pyq-toolbar-label">{strings.subjectLabel}</span>
                  {availableSubjects.map((sub) => (
                    <button
                      key={sub}
                      type="button"
                      className={`study-subject-pill ${activeSubject === sub ? "is-active" : ""}`}
                      onClick={() => setActiveSubject(sub)}
                    >
                      {sub}
                    </button>
                  ))}
                </div>

                <div className="study-search-box">
                  <span className="study-search-icon" aria-hidden="true">
                    🔍
                  </span>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder={strings.searchPlaceholder(activeClass, activeSubject)}
                    className="study-search-input"
                    aria-label="Search chapters"
                  />
                  {searchQuery && (
                    <button
                      type="button"
                      className="study-search-clear"
                      onClick={() => setSearchQuery("")}
                      aria-label={strings.clearFilter}
                    >
                      ✕
                    </button>
                  )}
                </div>
              </div>

              {/* Status Header */}
              <div className="study-status-bar">
                <span className="study-status-count">
                  {strings.showingChapters(filteredChapters.length, activeClass, activeSubject)}
                </span>
                <span className="study-status-hint">
                  {strings.featureHint}
                </span>
              </div>

              {/* Loading State */}
              {loadingResources && (
                <div className="study-loading-box">
                  <div className="study-spinner" aria-hidden="true" />
                  <p>{strings.loadingResources(activeClass, activeSubject)}</p>
                </div>
              )}

              {/* Chapter Cards List */}
              {!loadingResources && filteredChapters.length === 0 && (
                <div className="study-empty-state">
                  <p>{strings.noChaptersFound(searchQuery)}</p>
                  <button
                    type="button"
                    className="pyq-link-button"
                    onClick={() => setSearchQuery("")}
                  >
                    {strings.clearFilter}
                  </button>
                </div>
              )}

              {!loadingResources && filteredChapters.length > 0 && (
                <div className="chapter-cards-grid">
                  {filteredChapters.map((ch, idx) => {
                    const isNotesOpen = !!expandedNotes[ch.chapter];
                    const isCopied = copiedChapter === ch.chapter;
                    const isAiLoading = generatingAiNote === ch.chapter;
                    const feedback = aiNoteFeedback[ch.chapter];

                    return (
                      <article key={ch.chapter} className="chapter-card">
                        <div className="chapter-card-top">
                          <div className="chapter-index-badge">
                            {strings.chapterPrefix} {idx + 1}
                          </div>
                          <div className="chapter-meta-badges">
                            <span className="chapter-meta-pill">{strings.classPrefix} {ch.class_grade}</span>
                            <span className="chapter-meta-pill subject-pill">{ch.subject}</span>
                          </div>
                        </div>

                        <h4 className="chapter-card-title">{ch.chapter}</h4>

                        {/* Quick Concept Takeaways */}
                        {ch.key_takeaways && ch.key_takeaways.length > 0 && (
                          <ul className="chapter-takeaways-preview">
                            {ch.key_takeaways.slice(0, 2).map((pt, pIdx) => (
                              <li key={pIdx}>
                                <span className="takeaway-bullet">✓</span> {pt}
                              </li>
                            ))}
                          </ul>
                        )}

                        {/* Direct Action Buttons */}
                        <div className="chapter-actions-grid">
                          <a
                            href={ch.animation_video_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="chapter-btn chapter-btn-anim"
                            title={`${strings.animatedVideo}: ${ch.chapter}`}
                          >
                            <span className="chapter-btn-icon" aria-hidden="true">🎬</span>
                            <span>{strings.animatedVideo}</span>
                          </a>

                          <a
                            href={ch.diksha_video_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="chapter-btn chapter-btn-diksha"
                            title="Open PM eVIDYA / DIKSHA portal"
                          >
                            <span className="chapter-btn-icon" aria-hidden="true">🏛️</span>
                            <span>{strings.dikshaPortal}</span>
                          </a>

                          <a
                            href={ch.ncert_book_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="chapter-btn chapter-btn-book"
                            title="Read official NCERT textbook PDF"
                          >
                            <span className="chapter-btn-icon" aria-hidden="true">📖</span>
                            <span>{strings.ncertPdf}</span>
                          </a>

                          <button
                            type="button"
                            className={`chapter-btn chapter-btn-notes ${isNotesOpen ? "is-active" : ""}`}
                            onClick={() => toggleNotes(ch.chapter)}
                            aria-expanded={isNotesOpen}
                          >
                            <span className="chapter-btn-icon" aria-hidden="true">📝</span>
                            <span>{isNotesOpen ? strings.hideNotes : strings.viewNotes}</span>
                          </button>
                        </div>

                        {/* Expanded Interactive Notes Accordion */}
                        {isNotesOpen && (
                          <div className="chapter-notes-drawer" role="region" aria-label={`Notes for ${ch.chapter}`}>
                            <div className="chapter-notes-drawer-header">
                              <div className="chapter-notes-title-group">
                                <span className="notes-icon" aria-hidden="true">📋</span>
                                <h5>{strings.revisionNotesTitle(ch.chapter)}</h5>
                              </div>
                              <button
                                type="button"
                                className="chapter-copy-btn"
                                onClick={() => handleCopyNotes(ch.chapter, ch.summary_notes)}
                              >
                                {isCopied ? strings.copied : strings.copyNotes}
                              </button>
                            </div>

                            <div className="chapter-notes-body">
                              <pre className="chapter-notes-text">{ch.summary_notes}</pre>
                            </div>

                            {/* Full Takeaways List */}
                            {ch.key_takeaways && (
                              <div className="chapter-notes-takeaways">
                                <h6>{strings.keyTakeaways}</h6>
                                <ul>
                                  {ch.key_takeaways.map((point, kIdx) => (
                                    <li key={kIdx}>
                                      <span className="takeaway-check">🎯</span> {point}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}

                            {/* AI Deep-Dive Study Note Button */}
                            <div className="chapter-ai-note-box">
                              <button
                                type="button"
                                className="chapter-ai-gen-btn"
                                onClick={() => handleGenerateAiNotes(ch.chapter)}
                                disabled={isAiLoading}
                              >
                                {isAiLoading ? strings.generatingAiNotes : strings.generateAiNotes}
                              </button>
                              {feedback && (
                                <p className={`chapter-ai-status ${feedback.status === "error" ? "status-err" : "status-ok"}`}>
                                  {feedback.msg}
                                </p>
                              )}
                            </div>
                          </div>
                        )}
                      </article>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* TAB 2: Year-Wise Previous Year Question Papers */}
          {activeTab === "pyqs" && (
            <div className="pyq-cards-grid">
              {papers.map((paper, idx) => (
                <div key={idx} className="pyq-card">
                  <div className="pyq-card-top">
                    <span className="pyq-year-tag">{paper.year}</span>
                    <span className="pyq-badge">{paper.badge}</span>
                  </div>
                  <h4 className="pyq-card-title">{paper.title}</h4>
                  <p className="pyq-card-desc">{paper.description}</p>
                  <div className="pyq-card-actions">
                    <a
                      href={paper.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="pyq-link-button"
                    >
                      {strings.openOfficialPaper}
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB 3: Official NCERT Textbook PDFs */}
          {activeTab === "books" && (
            <div className="pyq-cards-grid">
              {bookLinks.map((book, idx) => (
                <div key={idx} className="pyq-card pyq-card-book">
                  <div className="pyq-card-top">
                    <span className="pyq-year-tag">NCERT PDF</span>
                    <span className="pyq-badge pyq-badge-ncert">{book.badge}</span>
                  </div>
                  <h4 className="pyq-card-title">{book.title}</h4>
                  <p className="pyq-card-desc">{book.description}</p>
                  <div className="pyq-card-actions">
                    <a
                      href={book.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="pyq-link-button pyq-link-button-ncert"
                    >
                      {book.action} ↗
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="pyq-footer-note">
            <span>
              {strings.footerSecureNote}
            </span>
          </div>
        </div>
      )}
    </section>
  );
}
