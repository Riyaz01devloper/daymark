# Official NCERT Hindi Textbook Translations & Curriculum Data
from typing import Any

HINDI_SUBJECTS: dict[str, str] = {
    "Science": "विज्ञान",
    "Mathematics": "गणित",
    "Social Science": "सामाजिक विज्ञान",
    "English": "अंग्रेज़ी",
    "Environmental Studies": "पर्यावरण अध्ययन",
    "Physics": "भौतिक विज्ञान",
    "Chemistry": "रसायन विज्ञान",
    "Biology": "जीव विज्ञान",
}

ENGLISH_SUBJECTS: dict[str, str] = {v: k for k, v in HINDI_SUBJECTS.items()}

# Exact, verified chapter titles from official NCERT Hindi textbooks (NCERT पाठ्यपुस्तकें)
HINDI_CHAPTER_TRANSLATIONS: dict[str, str] = {
    # Class 10 Science (कक्षा 10 विज्ञान)
    "Chemical Reactions and Equations": "रासायनिक अभिक्रियाएँ एवं समीकरण",
    "Acids, Bases and Salts": "अम्ल, क्षारक एवं लवण",
    "Metals and Non-Metals": "धातु एवं अधातु",
    "Carbon and its Compounds": "कार्बन एवं उसके यौगिक",
    "Life Processes": "जैव प्रक्रम",
    "Control and Coordination": "नियंत्रण एवं समन्वय",
    "How do Organisms Reproduce?": "जीव जनन कैसे करते हैं?",
    "Heredity": "आनुवंशिकता",
    "Light – Reflection and Refraction": "प्रकाश – परावर्तन तथा अपवर्तन",
    "The Human Eye and the Colourful World": "मानव नेत्र तथा रंगबिरंगा संसार",
    "Electricity": "विद्युत",
    "Magnetic Effects of Electric Current": "विद्युत धारा के चुंबकीय प्रभाव",
    "Our Environment": "हमारा पर्यावरण",

    # Class 10 Mathematics (कक्षा 10 गणित)
    "Real Numbers": "वास्तविक संख्याएँ",
    "Polynomials": "बहुपद",
    "Pair of Linear Equations in Two Variables": "दो चर वाले रैखिक समीकरण युग्म",
    "Quadratic Equations": "द्विघात समीकरण",
    "Arithmetic Progressions": "समांतर श्रेढियाँ",
    "Triangles": "त्रिभुज",
    "Coordinate Geometry": "निर्देशांक ज्यामिति",
    "Introduction to Trigonometry": "त्रिकोणमिति का परिचय",
    "Some Applications of Trigonometry": "त्रिकोणमिति के कुछ अनुप्रयोग",
    "Circles": "वृत्त",
    "Areas Related to Circles": "वृत्तों से संबंधित क्षेत्रफल",
    "Surface Areas and Volumes": "पृष्ठीय क्षेत्रफल और आयतन",
    "Statistics": "सांख्यिकी",
    "Probability": "प्रायिकता",

    # Class 10 Social Science (कक्षा 10 सामाजिक विज्ञान)
    "The Rise of Nationalism in Europe": "यूरोप में राष्ट्रवाद का उदय",
    "Nationalism in India": "भारत में राष्ट्रवाद",
    "The Making of a Global World": "भूमंडलीकृत विश्व का बनना",
    "Resources and Development": "संसाधन एवं विकास",
    "Forest and Wildlife Resources": "वन एवं वन्य जीव संसाधन",
    "Water Resources": "जल संसाधन",
    "Agriculture": "कृषि",
    "Power Sharing": "सत्ता की साझेदारी",
    "Federalism": "संघवाद",
    "Gender, Religion and Caste": "जाति, धर्म और लैंगिक मसले",
    "Development": "विकास",
    "Sectors of the Indian Economy": "भारतीय अर्थव्यवस्था के क्षेत्रक",
    "Money and Credit": "मुद्रा और साख",

    # Class 10 English (कक्षा 10 अंग्रेज़ी)
    "A Letter to God": "अ लेटर टू गॉड (A Letter to God)",
    "Nelson Mandela: Long Walk to Freedom": "नेल्सन मंडेला: लॉन्ग वॉक टू फ्रीडम",
    "Two Stories about Flying": "टू स्टोरीज़ अबाउट फ्लाइंग",
    "From the Diary of Anne Frank": "फ्रॉम द डायरी ऑफ ऐनी फ्रैंक",
    "Glimpses of India": "ग्लिम्प्सिस ऑफ इंडिया",
    "Mijbil the Otter": "मिजबिल द ऑटर",
    "Madam Rides the Bus": "मैडम राइड्स द बस",
    "The Sermon at Benares": "द सेर्मन एट बनारस",
    "The Proposal": "द प्रपोजल",

    # Class 9 Science (कक्षा 9 विज्ञान)
    "Matter in Our Surroundings": "हमारे आस-पास के पदार्थ",
    "Is Matter Around Us Pure?": "क्या हमारे आस-पास के पदार्थ शुद्ध हैं?",
    "Atoms and Molecules": "परमाणु एवं अणु",
    "Structure of the Atom": "परमाणु की संरचना",
    "The Fundamental Unit of Life": "जीवन की मौलिक इकाई",
    "Tissues": "ऊतक",
    "Motion": "गति",
    "Force and Laws of Motion": "बल तथा गति के नियम",
    "Gravitation": "गुरुत्वाकर्षण",
    "Work and Energy": "कार्य तथा ऊर्जा",
    "Sound": "ध्वनि",
    "Improvement in Food Resources": "खाद्य संसाधनों में सुधार",

    # Class 9 Mathematics (कक्षा 9 गणित)
    "Number Systems": "संख्या पद्धति",
    "Linear Equations in Two Variables": "दो चरों वाले रैखिक समीकरण",
    "Introduction to Euclid's Geometry": "यूक्लिड की ज्यामिति का परिचय",
    "Lines and Angles": "रेखाएँ और कोण",
    "Quadrilaterals": "चतुर्भुज",
    "Heron's Formula": "हीरोन का सूत्र",

    # Class 9 Social Science (कक्षा 9 सामाजिक विज्ञान)
    "The French Revolution": "फ्रांसीसी क्रांति",
    "Socialism in Europe and the Russian Revolution": "यूरोप में समाजवाद एवं रूसी क्रांति",
    "Nazism and the Rise of Hitler": "नात्सीवाद और हिटलर का उदय",
    "India – Size and Location": "भारत – आकार और स्थिति",
    "Physical Features of India": "भारत का भौतिक स्वरूप",
    "Drainage": "अपवाह",
    "Climate": "जलवायु",
    "What is Democracy? Why Democracy?": "लोकतंत्र क्या? लोकतंत्र क्यों?",
    "Constitutional Design": "संविधान निर्माण",
    "The Story of Village Palampur": "पालमपुर गाँव की कहानी",
    "People as Resource": "संसाधन के रूप में लोग",

    # Class 9 English (कक्षा 9 अंग्रेज़ी)
    "The Fun They Had": "द फन दे हैड (The Fun They Had)",
    "The Sound of Music": "द साउंड ऑफ म्यूजिक",
    "The Little Girl": "द लिटिल गर्ल",
    "A Truly Beautiful Mind": "अ ट्रूली ब्यूटीफुल माइंड",
    "The Snake and the Mirror": "द स्नेक एंड द मिरर",
    "My Childhood": "माय चाइल्डहुड (मेरा बचपन)",
    "Reach for the Top": "रीच फॉर द टॉप",
    "Kathmandu": "काठमांडू",
    "If I Were You": "इफ आई वर यू",

    # Class 12 Physics (कक्षा 12 भौतिक विज्ञान)
    "Electric Charges and Fields": "वैद्युत आवेश तथा क्षेत्र",
    "Electrostatic Potential and Capacitance": "स्थिरवैद्युत विभव तथा धारिता",
    "Current Electricity": "विद्युत धारा",
    "Moving Charges and Magnetism": "गतिमान आवेश और चुंबकत्व",
    "Magnetism and Matter": "चुंबकत्व एवं द्रव्य",
    "Electromagnetic Induction": "वैद्युतचुंबकीय प्रेरण",
    "Alternating Current": "प्रत्यावर्ती धारा",
    "Electromagnetic Waves": "वैद्युतचुंबकीय तरंगें",
    "Ray Optics and Optical Instruments": "किरण प्रकाशिकी एवं प्रकाशिक यंत्र",
    "Wave Optics": "तरंग प्रकाशिकी",
    "Dual Nature of Radiation and Matter": "विकिरण तथा द्रव्य की द्वैत प्रकृति",
    "Atoms": "परमाणु",
    "Nuclei": "नाभिक",
    "Semiconductor Electronics: Materials, Devices and Simple Circuits": "अर्धचालक इलेक्ट्रॉनिकी: पदार्थ, युक्तियाँ तथा सरल परिपथ",

    # Class 12 Chemistry (कक्षा 12 रसायन विज्ञान)
    "Solutions": "विलयन",
    "Electrochemistry": "वैद्युतरसायन",
    "Chemical Kinetics": "रासायनिक बलगतिकी",
    "The d-and f-Block Elements": "d-एवं f-ब्लॉक के तत्व",
    "Coordination Compounds": "उपसहसंयोजन यौगिक",
    "Haloalkanes and Haloarenes": "हैलोएल्केन तथा हैलोएरीन",
    "Alcohols, Phenols and Ethers": "ऐल्कोहॉल, फीनॉल एवं ईथर",
    "Aldehydes, Ketones and Carboxylic Acids": "ऐल्डिहाइड, कीटोन एवं कार्बोक्सिलिक अम्ल",
    "Amines": "ऐमीन",
    "Biomolecules": "जैव-अणु",

    # Class 12 Mathematics (कक्षा 12 गणित)
    "Relations and Functions": "संबंध एवं फलन",
    "Inverse Trigonometric Functions": "प्रतिलोम त्रिकोणमितीय फलन",
    "Matrices": "आव्यूह",
    "Determinants": "सारणिक",
    "Continuity and Differentiability": "सांतत्य तथा अवकलनीयता",
    "Application of Derivatives": "अवकलज के अनुप्रयोग",
    "Integrals": "समाकलन",
    "Application of Integrals": "समाकलनों के अनुप्रयोग",
    "Differential Equations": "अवकल समीकरण",
    "Vector Algebra": "सदिश बीजगणित",
    "Three Dimensional Geometry": "त्रि-विमीय ज्यामिति",
    "Linear Programming": "रैखिक प्रोग्रामन",

    # Class 12 Biology (कक्षा 12 जीव विज्ञान)
    "Sexual Reproduction in Flowering Plants": "पुष्पी पादपों में लैंगिक जनन",
    "Human Reproduction": "मानव जनन",
    "Reproductive Health": "जनन स्वास्थ्य",
    "Principles of Inheritance and Variation": "वंशागति तथा विविधता के सिद्धांत",
    "Molecular Basis of Inheritance": "वंशागति के आणविक आधार",
    "Evolution": "विकास",
    "Human Health and Disease": "मानव स्वास्थ्य तथा रोग",
    "Microbes in Human Welfare": "मानव कल्याण में सूक्ष्मजीव",
    "Biotechnology: Principles and Processes": "जैव प्रौद्योगिकी - सिद्धांत व प्रक्रम",
    "Biotechnology and its Applications": "जैव प्रौद्योगिकी एवं उसके उपयोग",
    "Organisms and Populations": "जीव और समष्टियाँ",
    "Ecosystem": "पारितंत्र",
    "Biodiversity and Conservation": "जैव विविधता एवं संरक्षण",

    # Class 11 Physics (कक्षा 11 भौतिक विज्ञान)
    "Units and Measurements": "मात्रक और मापन",
    "Motion in a Straight Line": "सरल रेखा में गति",
    "Motion in a Plane": "समतल में गति",
    "Laws of Motion": "गति के नियम",
    "Work, Energy and Power": "कार्य, ऊर्जा और शक्ति",
    "System of Particles and Rotational Motion": "कणों के निकाय तथा घूर्णी गति",
    "Mechanical Properties of Solids": "ठोसों के यांत्रिक गुण",
    "Mechanical Properties of Fluids": "तरलों के यांत्रिकी गुण",
    "Thermal Properties of Matter": "द्रव्य के तापीय गुण",
    "Thermodynamics": "ऊष्मागतिकी",
    "Kinetic Theory": "अणुगति सिद्धांत",
    "Oscillations": "दोलन",
    "Waves": "तरंगें",

    # Class 11 Chemistry (कक्षा 11 रसायन विज्ञान)
    "Some Basic Concepts of Chemistry": "रसायन विज्ञान की कुछ मूल अवधारणाएँ",
    "Structure of Atom": "परमाणु की संरचना",
    "Classification of Elements and Periodicity in Properties": "तत्वों का वर्गीकरण एवं गुणधर्मों में आवर्तिता",
    "Chemical Bonding and Molecular Structure": "रासायनिक आबंधन तथा आण्विक संरचना",
    "Chemical Thermodynamics": "रासायनिक ऊष्मागतिकी",
    "Equilibrium": "साम्यावस्था",
    "Redox Reactions": "अपचयोपचय (रेडॉक्स) अभिक्रियाएँ",
    "Organic Chemistry: Some Basic Principles and Techniques": "कार्बनिक रसायन: कुछ आधारभूत सिद्धांत तथा तकनीकें",
    "Hydrocarbons": "हाइड्रोकार्बन",

    # Class 11 Mathematics (कक्षा 11 गणित)
    "Sets": "समुच्चय",
    "Trigonometric Functions": "त्रिकोणमितीय फलन",
    "Complex Numbers and Quadratic Equations": "सम्मिश्र संख्याएँ और द्विघातीय समीकरण",
    "Linear Inequalities": "रैखिक असमिकाएँ",
    "Permutations and Combinations": "क्रमचय और संचय",
    "Binomial Theorem": "द्विपद प्रमेय",
    "Sequences and Series": "अनुक्रम तथा श्रेणी",
    "Straight Lines": "सरल रेखाएँ",
    "Conic Sections": "शंकु परिच्छेद",
    "Introduction to Three Dimensional Geometry": "त्रिविमीय ज्यामिति का परिचय",
    "Limits and Derivatives": "सीमा और अवकलज",

    # Class 8 Science (कक्षा 8 विज्ञान)
    "Crop Production and Management": "फसल उत्पादन एवं प्रबंध",
    "Microorganisms: Friend and Foe": "सूक्ष्मजीव: मित्र एवं शत्रु",
    "Coal and Petroleum": "कोयला और पेट्रोलियम",
    "Combustion and Flame": "दहन और ज्वाला",
    "Conservation of Plants and Animals": "पौधों एवं जंतुओं का संरक्षण",
    "Reproduction in Animals": "जंतुओं में जनन",
    "Reaching the Age of Adolescence": "किशोरावस्था की ओर",
    "Force and Pressure": "बल तथा दाब",
    "Friction": "घर्षण",
    "Chemical Effects of Electric Current": "विद्युत धारा के रासायनिक प्रभाव",
    "Some Natural Phenomena": "कुछ प्राकृतिक परिघटनाएँ",

    # Class 8 Mathematics (कक्षा 8 गणित)
    "Rational Numbers": "परिमेय संख्याएँ",
    "Linear Equations in One Variable": "एक चर वाले रैखिक समीकरण",
    "Understanding Quadrilaterals": "चतुर्भुजों को समझना",
    "Data Handling": "आँकड़ों का प्रबंधन",
    "Squares and Square Roots": "वर्ग और वर्गमूल",
    "Cubes and Cube Roots": "घन और घनमूल",
    "Comparing Quantities": "राशियों की तुलना",
    "Algebraic Expressions and Identities": "बीजीय व्यंजक एवं सर्वसमिकाएँ",
    "Mensuration": "क्षेत्रमिति",
    "Exponents and Powers": "घातांक और घात",
    "Direct and Inverse Proportions": "सीधा और प्रतिलोम समानुपात",
    "Factorisation": "गुणनखंडन",
    "Introduction to Graphs": "आलेखों से परिचय",

    # Class 8 Social Science (कक्षा 8 सामाजिक विज्ञान)
    "How, When and Where": "कैसे, कब और कहाँ",
    "From Trade to Territory": "व्यापार से साम्राज्य तक",
    "Ruling the Countryside": "ग्रामीण क्षेत्र पर शासन चलाना",
    "When People Rebel 1857": "जब जनता बगावत करती है (1857 और उसके बाद)",
    "Resources": "संसाधन",
    "Land, Soil, Water, Natural Vegetation": "भूमि, मृदा, जल, प्राकृतिक वनस्पति और वन्य जीवन संसाधन",
    "Industries": "उद्योग",
    "The Indian Constitution": "भारतीय संविधान",
    "Understanding Secularism": "धर्मनिरपेक्षता की समझ",
    "Parliament and Making of Laws": "संसद तथा कानूनों का निर्माण",
    "Judiciary": "न्यायपालिका",

    # Class 8 English (कक्षा 8 अंग्रेज़ी)
    "The Best Christmas Present in the World": "द बेस्ट क्रिसमस प्रेजेंट इन द वर्ल्ड",
    "The Tsunami": "द सुनामी",
    "Glimpses of the Past": "ग्लिम्प्सिस ऑफ द पास्ट",
    "Bepin Choudhury's Lapse of Memory": "बिपिन चौधरी'ज लैप्स ऑफ मेमोरी",
    "The Summit Within": "द समिट विदइन",
    "This is Jody's Fawn": "दिस इज़ जोडी'ज फॉन",
    "A Visit to Cambridge": "अ विजिट टू कैम्ब्रिज",
    "A Short Monsoon Diary": "अ शॉर्ट मानसून डायरी",

    # Class 7 Science (कक्षा 7 विज्ञान)
    "Nutrition in Plants": "पादपों में पोषण",
    "Nutrition in Animals": "प्राणियों में पोषण",
    "Heat": "ऊष्मा",
    "Physical and Chemical Changes": "भौतिक एवं रासायनिक परिवर्तन",
    "Respiration in Organisms": "जीवों में श्वसन",
    "Transportation in Animals and Plants": "पादप एवं जंतुओं में परिवहन",
    "Reproduction in Plants": "पादप में जनन",
    "Motion and Time": "गति एवं समय",
    "Electric Current and its Effects": "विद्युत धारा और इसके प्रभाव",
    "Forests: Our Lifeline": "वन: हमारी जीवन रेखा",

    # Class 7 Mathematics (कक्षा 7 गणित)
    "Integers": "पूर्णांक",
    "Fractions and Decimals": "भिन्न एवं दशमलव",
    "Simple Equations": "सरल समीकरण",
    "The Triangle and its Properties": "त्रिभुज और उसके गुण",
    "Perimeter and Area": "परिमाप और क्षेत्रफल",
    "Algebraic Expressions": "बीजीय व्यंजक",
    "Symmetry": "सममिति",

    # Class 7 Social Science (कक्षा 7 सामाजिक विज्ञान)
    "Tracing Changes Through a Thousand Years": "हज़ार वर्षों के दौरान हुए परिवर्तनों की पड़ताल",
    "New Kings and Kingdoms": "नए राजा और उनके राज्य",
    "Delhi: 12th to 15th Century": "दिल्ली: 12वीं से 15वीं शताब्दी",
    "The Mughals": "मुगल (16वीं से 17वीं शताब्दी)",
    "Environment": "पर्यावरण",
    "Inside Our Earth": "हमारी पृथ्वी के अंदर",
    "Our Changing Earth": "हमारी बदलती पृथ्वी",
    "Air": "वायु",
    "Water": "जल",
    "On Equality": "समानता",
    "Role of the Government in Health": "स्वास्थ्य में सरकार की भूमिका",

    # Class 7 English (कक्षा 7 अंग्रेज़ी)
    "Three Questions": "थ्री क्वेश्चन्स",
    "A Gift of Chappals": "अ गिफ्ट ऑफ चप्पल",
    "Gopal and the Hilsa Fish": "गोपाल एंड द हिल्सा फिश",
    "The Ashes That Made Trees Bloom": "द ऐशेज़ दैट मेड ट्रीज़ ब्लूम",
    "Quality": "क्वालिटी",
    "Expert Detectives": "एक्सपर्ट डिटेक्टिव्स",
    "The Invention of Vita-Wonk": "द इन्वेंशन ऑफ वीटा-वॉन्क",

    # Class 6 Science (कक्षा 6 विज्ञान)
    "Components of Food": "भोजन के घटक",
    "Sorting Materials into Groups": "वस्तुओं के समूह बनाना",
    "Separation of Substances": "पदार्थों का पृथक्करण",
    "Getting to Know Plants": "पौधों को जानिए",
    "Body Movements": "शरीर में गति",
    "The Living Organisms — Characteristics and Habitats": "सजीव – विशेषताएँ एवं आवास",
    "Motion and Measurement of Distances": "गति एवं दूरियों का मापन",
    "Light, Shadows and Reflections": "प्रकाश – छायाएँ एवं परावर्तन",
    "Electricity and Circuits": "विद्युत तथा परिपथ",
    "Fun with Magnets": "चुंबकों द्वारा मनोरंजन",
    "Air Around Us": "हमारे चारों ओर वायु",

    # Class 6 Mathematics (कक्षा 6 गणित)
    "Knowing Our Numbers": "अपनी संख्याओं की जानकारी",
    "Whole Numbers": "पूर्ण संख्याएँ",
    "Playing with Numbers": "संख्याओं के साथ खेलना",
    "Basic Geometrical Ideas": "आधारभूत ज्यामितीय अवधारणाएँ",
    "Understanding Elementary Shapes": "प्रारंभिक आकारों को समझना",
    "Fractions": "भिन्न",
    "Decimals": "दशमलव",
    "Algebra": "बीजगणित",
    "Ratio and Proportion": "अनुपात और समानुपात",

    # Class 6 Social Science (कक्षा 6 सामाजिक विज्ञान)
    "What, Where, How and When?": "क्या, कब, कहाँ और कैसे?",
    "From Hunting-Gathering to Growing Food": "आरंभिक मानव की खोज में",
    "In the Earliest Cities": "आरंभिक नगर",
    "What Books and Burials Tell Us": "क्या बताती हैं हमें किताबें और कब्रें",
    "The Earth in the Solar System": "सौरमंडल में पृथ्वी",
    "Globe: Latitudes and Longitudes": "ग्लोब: अक्षांश एवं देशांतर",
    "Motions of the Earth": "पृथ्वी की गतियाँ",
    "Maps": "मानचित्र",
    "Understanding Diversity": "विविधता की समझ",
    "Diversity and Discrimination": "विविधता एवं भेदभाव",
    "What is Government?": "सरकार क्या है?",

    # Class 6 English (कक्षा 6 अंग्रेज़ी)
    "Who Did Patrick's Homework?": "हू डिड पैट्रिक्स होमवर्क?",
    "How the Dog Found Himself a New Master!": "हाउ द डॉग फाउंड हिमसेल्फ अ न्यू मास्टर!",
    "Taro's Reward": "टारोज़ रिवार्ड",
    "An Indian-American Woman in Space: Kalpana Chawla": "कल्पना चावला: अंतरिक्ष में पहली भारतीय महिला",
    "A Different Kind of School": "अ डिफरेंट काइंड ऑफ स्कूल",
    "Who I Am": "हू आई एम",
    "Fair Play": "फेयर प्ले",

    # Primary Classes (कक्षा 1 से 5)
    "Super Senses": "कैसे पहचाना चींटी ने दोस्त को? (सुपर सेंसेज)",
    "A Snake Charmer's Story": "कहानी सपेरों की",
    "From Tasting to Digesting": "चखने से पचने तक",
    "Mangoes Round the Year": "खाएं आम बारहों महीने",
    "Seeds and Seeds": "बीज, बीज, बीज",
    "Every Drop Counts": "बूंद-बूंद, दरिया-दरिया",
    "Experiments with Water": "पानी के प्रयोग",
    "Going to School": "चलो, चलें स्कूल!",
    "Ear to Ear": "कान-कान में",
    "A Day with Nandu": "नंदू हाथी",
    "The Story of Amrita": "अमृता की कहानी",
    "Anita and the Honeybees": "अनीता की मधुमक्खियाँ",
    "Omana's Journey": "ओमना का सफर",
    "Poonam's Day out": "पूनम की दिनचर्या",
    "The Plant Fairy": "पौधों की परी",
    "Water O' Water!": "पानी रे पानी!",
    "Our First School": "हमारा पहला स्कूल",
    "Chhotu's House": "छोटू का घर",
    "Foods We Eat": "खाना अपना-अपना",
    "About Me": "मेरे बारे में (About Me)",
    "My Body Parts": "मेरे शरीर के अंग",
    "My Family": "मेरा परिवार",
    "My Home": "मेरा घर",
    "Plants Around Us": "हमारे आस-पास के पौधे",
    "Animals Around Us": "हमारे आस-पास के जीव-जंतु",
    "Shapes and Space": "आकृतियाँ और स्थान",
    "Numbers from One to Nine": "एक से नौ तक की संख्याएँ",
    "Addition": "जोड़",
    "Subtraction": "घटाव",
    "Numbers from Ten to Twenty": "दस से बीस तक की संख्याएँ",
    "Time": "समय",
    "Measurement": "माप",
    "Counting in Groups": "गिनती समूहों में",
    "How Much Can You Carry?": "तुम कितना उठा सकते हो?",
    "Counting in Tens": "दहाई में गिनती",
    "Patterns": "पैटर्न",
    "Footprints": "पैरों के निशान",
    "Give and Take": "लेना और देना",
    "Where to Look From": "कहाँ से देखें",
    "Fun with Numbers": "संख्याओं की उछलकूद",
    "Building with Bricks": "ईंटों से बनी इमारत",
    "Long and Short": "लंबा और छोटा",
    "A Trip to Bhopal": "भोपाल की सैर",
    "Tick-Tick-Tick": "टिक-टिक-टिक",
    "The Fish Tale": "मछली उछली",
    "Shapes and Angles": "आकृतियाँ और कोण",
    "How Many Squares?": "कितने वर्ग?",
    "Parts and Wholes": "हिस्से और पूरे",
    "Does it Look the Same?": "क्या यह एक जैसा दिखता है?",
    "Be My Multiple, I'll be Your Factor": "मैं तेरा गुणनखंड, तू मेरा गुणज",
    "Can You See the Pattern?": "क्या तुम पैटर्न देख सकते हो?",
    "A Happy Child": "अ हैप्पी चाइल्ड",
    "Three Little Pigs": "थ्री लिटिल पिग्स",
    "After a Bath": "आफ्टर अ बाथ",
    "The Bubble, the Straw and the Shoe": "द बबल, द स्ट्रॉ एंड द शू",
    "One Little Kitten": "वन लिटिल किटन",
    "Lalu and Peelu": "लालू और पीलू",
    "First Day at School": "स्कूल का पहला दिन",
    "Haldi's Adventure": "हल्दी का एडवेंचर",
    "I am Lucky!": "आई एम लकी!",
    "I Want": "आई वॉन्ट",
    "A Smile": "अ स्माइल",
    "The Wind and the Sun": "हवा और सूरज",
    "Good Morning": "गुड मॉर्निंग",
    "The Magic Garden": "द मैजिक गार्डन",
    "Bird Talk": "बर्ड टॉक",
    "Nina and the Baby Sparrows": "नीना एंड द बेबी स्पैरोज़",
    "Little by Little": "लिटिल बाय लिटिल",
    "The Enormous Turnip": "द इनॉर्मस टर्निप",
    "Wake Up!": "वेक अप!",
    "Neha's Alarm Clock": "नेहा का अलार्म क्लॉक",
    "Noses": "नोसेज",
    "The Little Fir Tree": "द लिटिल फर ट्री",
    "Run!": "रन!",
    "Nasruddin's Aim": "नसरुद्दीन का निशाना",
    "Ice-Cream Man": "आइसक्रीम मैन",
    "Wonderful Waste!": "वंडरफुल वेस्ट",
    "Teamwork": "टीमवर्क",
    "Flying Together": "फ्लाइंग टुगेदर",
    "My Shadow": "माय शैडो",
    "Robinson Crusoe Discovers a footprint": "रॉबिंसन क्रूसो",
    "Robinson Crusoe": "रॉबिंसन क्रूसो",
    "Class Discussion": "क्लास डिस्कशन",
    "My Home and Family": "मेरा घर और परिवार",
    "Good Habits": "अच्छी आदतें",
    "What is Long, What is Round?": "क्या है लंबा, क्या है गोल?",
    "My Body": "मेरा शरीर",
    "Food and Health": "भोजन और स्वास्थ्य",
    "Clothes We Wear": "हमारे वस्त्र",
    "Our Neighborhood": "हमारा पड़ोस",
    "Safety and First Aid": "सुरक्षा और प्राथमिक उपचार",
    "Shapes and Designs": "आकृतियों का कमाल",
    "Fun with Give and Take": "लेने-देने का खेल",
    "Time Goes On": "समय-समय की बात",
    "The Way The World Looks": "दुनिया कुछ ऐसी दिखती है",
    "The Junk Seller": "कबाड़ीवाली",
    "Jugs and Mugs": "जग और मग",
    "Kingdoms, Kings and an Early Republic": "राज्य, राजा और एक प्राचीन गणराज्य",
    "An Indian - American Woman in Space: Kalpana Chawla": "कल्पना चावला: अंतरिक्ष में पहली भारतीय महिला",
    "Light": "प्रकाश",
    "The Delhi Sultans": "दिल्ली के सुल्तान",
    "The Mughal Empire": "मुगल साम्राज्य",
    "India - Size and Location": "भारत – आकार और स्थिति",
    "Semiconductor Electronics": "अर्धचालक इलेक्ट्रॉनिकी",
    "The d- and f-Block Elements": "d-एवं f-ब्लॉक के तत्व",
}

# Reverse mapping for chapter titles
HINDI_CHAPTER_REVERSE: dict[str, str] = {v: k for k, v in HINDI_CHAPTER_TRANSLATIONS.items()}


def get_hindi_subject_name(subject: str) -> str:
    clean = subject.strip()
    return HINDI_SUBJECTS.get(clean, clean)


def get_hindi_chapter_name(chapter: str) -> str:
    clean = chapter.strip()
    return HINDI_CHAPTER_TRANSLATIONS.get(clean, clean)


def normalize_subject_to_english(subject: str) -> str:
    clean = subject.strip()
    return ENGLISH_SUBJECTS.get(clean, clean)


def normalize_chapter_to_english(chapter: str) -> str:
    clean = chapter.strip()
    return HINDI_CHAPTER_REVERSE.get(clean, clean)


# Curated detailed Hindi NCERT textbook notes for major high-frequency chapters
KNOWN_CHAPTER_NOTES_HI: dict[tuple[int, str], dict[str, Any]] = {
    (10, "chemical reactions and equations"): {
        "summary": (
            "### अध्याय अवलोकन एवं मूल अवधारणाएँ\n"
            "- **रासायनिक अभिक्रिया**: ऐसा प्रक्रम जिसमें अभिकारकों के रासायनिक गुणधर्म बदलकर नए उत्पाद बनते हैं।\n"
            "- **पहचान के लक्षण**: अवस्था में परिवर्तन, रंग में परिवर्तन, गैस का निकास या तापमान में परिवर्तन।\n"
            "- **द्रव्यमान संरक्षण का नियम**: किसी भी रासायनिक अभिक्रिया में द्रव्यमान का न तो निर्माण होता है और न ही विनाश। इसलिए समीकरणों को संतुलित करना आवश्यक है।\n\n"
            "### रासायनिक अभिक्रियाओं के प्रमुख प्रकार\n"
            "1. **संयोजन अभिक्रिया**: दो या दो से अधिक अभिकारक मिलकर एकल उत्पाद बनाते हैं ($CaO + H_2O \\rightarrow Ca(OH)_2$)।\n"
            "2. **वियोजन (अपघटन) अभिक्रिया**: एकल अभिकारक टूटकर दो या अधिक उत्पाद बनाता है (ऊष्मीय, प्रकाशिक या विद्युत अपघटन)।\n"
            "3. **विस्थापन अभिक्रिया**: अधिक क्रियाशील तत्व कम क्रियाशील तत्व को उसके यौगिक से विस्थापित करता है ($Fe + CuSO_4 \\rightarrow FeSO_4 + Cu$)।\n"
            "4. **द्विविस्थापन एवं अवक्षेपण**: अभिकारकों के बीच आयनों का परस्पर आदान-प्रदान ($Na_2SO_4 + BaCl_2 \\rightarrow BaSO_4\\downarrow + 2NaCl$)।\n"
            "5. **उपचयन एवं अपचयन (रेडॉक्स)**: ऑक्सीजन की वृद्धि या हाइड्रोजन का ह्रास = उपचयन; ऑक्सीजन का ह्रास या हाइड्रोजन की वृद्धि = अपचयन।\n\n"
            "### दैनिक जीवन में उपचयन अभिक्रियाएँ\n"
            "- **संक्षारण**: धातु की सतह नमी और वायु के संपर्क में आने पर नष्ट होना (लोहे पर जंग लगना: जलयोजित आयरन ऑक्साइड)।\n"
            "- **विकृतगंधिता**: वसा एवं तेलों का उपचयन जिससे गंध एवं स्वाद बदल जाता है (नाइट्रोजन गैस से पैकेजिंग द्वारा बचाव)।\n\n"
            "### NCERT बोर्ड परीक्षा मुख्य बिंदु\n"
            "- समीकरणों में भौतिक अवस्थाएँ अवश्य लिखें: (s), (l), (g), (aq)।\n"
            "- बेरियम सल्फेट का अवक्षेप श्वेत (सफेद) और लेड आयोडाइड ($PbI_2$) का पीला होता है।\n"
            "- श्वसन एक ऊष्माक्षेपी अभिक्रिया है; कैल्शियम कार्बोनेट का अपघटन ऊष्माशोषी है।"
        ),
        "takeaways": [
            "संतुलित रासायनिक समीकरण द्रव्यमान संरक्षण के नियम का पालन करता है।",
            "पाँचों मुख्य अभिक्रिया प्रकारों को संतुलित समीकरण सहित याद रखें।",
            "रेडॉक्स अभिक्रिया में उपचयन और अपचयन साथ-साथ होते हैं।",
            "संक्षारण तथा विकृतगंधिता दैनिक जीवन में उपचयन के प्रमुख उदाहरण हैं।"
        ],
    },
    (10, "electricity"): {
        "summary": (
            "### अध्याय अवलोकन एवं मूल अवधारणाएँ\n"
            "- **विद्युत धारा ($I$)**: विद्युत आवेश के प्रवाह की दर। $I = Q / t$, मात्रक: ऐम्पीयर (A)।\n"
            "- **विद्युत विभवांतर ($V$)**: एकांक धन आवेश को एक बिंदु से दूसरे बिंदु तक लाने में किया गया कार्य। $V = W / Q$, मात्रक: वोल्ट (V)।\n\n"
            "### मुख्य नियम एवं सूत्र\n"
            "- **ओम का नियम**: नियत ताप पर धातु के तार में प्रवाहित धारा उसके सिरों के बीच विभवांतर के अनुक्रमानुपाती होती है ($V = IR$)।\n"
            "- **प्रतिरोध की निर्भरता**: $R = \\rho \\frac{l}{A}$ (तार की लंबाई के समानुपाती, अनुप्रस्थ काट के क्षेत्रफल के व्युत्क्रमानुपाती)।\n"
            "- **श्रेणीक्रम संयोजन**: $R_s = R_1 + R_2 + \\dots$; धारा समान रहती है, विभवांतर विभाजित होता है।\n"
            "- **पार्श्वक्रम (समांतर क्रम) संयोजन**: $\\frac{1}{R_p} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\dots$; विभवांतर समान रहता है, धारा विभाजित होती है।\n"
            "- **जूल का तापन नियम**: $H = I^2 R t$।\n"
            "- **विद्युत शक्ति**: $P = VI = I^2 R = \\frac{V^2}{R}$। व्यापारिक मात्रक: किलोवाट-घंटा ($1 \\text{ kWh} = 3.6 \\times 10^6 \\text{ J}$)।\n\n"
            "### NCERT बोर्ड परीक्षा मुख्य बिंदु\n"
            "- ऐमीटर को सदैव श्रेणीक्रम में तथा वोल्टमीटर को सदैव पार्श्वक्रम (समांतर क्रम) में जोड़ा जाता है।\n"
            "- घरेलू परिपथ पार्श्वक्रम में संयोजित किए जाते हैं ताकि सभी उपकरणों को समान 220V वोल्टता मिले।"
        ),
        "takeaways": [
            "ओम का नियम ($V = IR$) नियत ताप पर चालक के लिए मान्य है।",
            "श्रेणीक्रम में तुल्य प्रतिरोध अधिकतम तथा पार्श्वक्रम में न्यूनतम होता है।",
            "जूल का तापन नियम: $H = I^2 R t$ हीटर, गीज़र तथा फ्यूज में प्रयुक्त होता है।",
            "1 यूनिट = 1 kWh = 3.6 × 10^6 जूल।"
        ],
    },
    (10, "real numbers"): {
        "summary": (
            "### अध्याय अवलोकन एवं मूल अवधारणाएँ\n"
            "- **अंकगणित की आधारभूत प्रमेय**: प्रत्येक भाज्य संख्या को अभाज्य संख्याओं के एक गुणनफल के रूप में अद्वितीय रूप से व्यक्त (गुणनखंडित) किया जा सकता है।\n"
            "- **HCF और LCM संबंध**: किन्हीं दो धनात्मक पूर्णांकों $a$ और $b$ के लिए: $\\text{HCF}(a, b) \\times \\text{LCM}(a, b) = a \\times b$।\n\n"
            "### अपरिमेय संख्याओं का सत्यापन (विरोधाभास विधि)\n"
            "- $\\sqrt{2}, \\sqrt{3}, \\sqrt{5}$ तथा $a + b\\sqrt{p}$ की अपरिमेयता सिद्ध करना।\n"
            "- माना संख्या परिमेय है $\\frac{p}{q}$ (सह-अभाज्य पूर्णांक, $q \\neq 0$), दोनों पक्षों का वर्ग कर विरोधाभास प्राप्त करते हैं कि $p$ और $q$ का उभयनिष्ठ गुणनखंड है।\n\n"
            "### परीक्षा रणनीति एवं युक्तियाँ\n"
            "- अभाज्य गुणनखंडन करते समय घातों को स्पष्ट लिखें।\n"
            "- बोर्ड परीक्षा में प्रत्येक चरण के पीछे प्रयुक्त प्रमेय का कारण अवश्य लिखें।"
        ),
        "takeaways": [
            "प्रत्येक भाज्य संख्या का अभाज्य गुणनखंडन अद्वितीय होता है।",
            "दो संख्याओं के लिए: HCF(a, b) × LCM(a, b) = a × b।",
            "विरोधाभास विधि द्वारा अपरिमेयता सिद्ध करने के प्रश्नों का विशेष अभ्यास करें।"
        ],
    },
    (12, "electric charges and fields"): {
        "summary": (
            "### स्थिरवैद्युतिकी मूल सिद्धांत\n"
            "- **कूलॉम का नियम**: दो स्थिर बिंदु आवेशों के बीच आकर्षण या प्रतिकर्षण बल: $F = \\frac{1}{4\\pi\\varepsilon_0} \\frac{|q_1 q_2|}{r^2}$।\n"
            "- **विद्युत क्षेत्र ($E$)**: एकांक धनात्मक परीक्षण आवेश पर लगने वाला बल ($E = F / q_0$)। बिंदु आवेश के कारण: $E = \\frac{q}{4\\pi\\varepsilon_0 r^2}$।\n"
            "- **विद्युत द्विध्रुव आघूर्ण**: $\\vec{p} = q(2\\vec{a})$, दिशा ऋण आवेश से धन आवेश की ओर।\n"
            "- **द्विध्रुव पर बल आघूर्ण**: $\\vec{\\tau} = \\vec{p} \\times \\vec{E}$।\n\n"
            "### गाउस का नियम एवं अनुप्रयोग\n"
            "- **गाउस का प्रमेय**: किसी बंद पृष्ठ से गुजरने वाला कुल विद्युत फ्लक्स $\\Phi = \\oint \\vec{E} \\cdot d\\vec{A} = \\frac{q_{\\text{enclosed}}}{\\varepsilon_0}$।\n"
            "- अनंत लंबाई के सीधे तार के कारण: $E = \\frac{\\lambda}{2\\pi\\varepsilon_0 r}$।\n"
            "- समतल अनंत आवेशित चादर के कारण: $E = \\frac{\\sigma}{2\\varepsilon_0}$।\n"
            "- पतले गोलीय खोल के भीतर विद्युत क्षेत्र सर्वत्र शून्य होता है ($E_{\\text{inside}} = 0$)।"
        ),
        "takeaways": [
            "आवेश का क्वांटीकरण: Q = ne; आवेश संरक्षित तथा निश्चर राशि है।",
            "गाउस का नियम किसी भी बंद गाउसीय पृष्ठ पर परिबद्ध कुल आवेश से संबंधित है।",
            "समान रूप से आवेशित गोलीय कोश के अंदर विद्युत क्षेत्र शून्य होता है।"
        ],
    },
    (12, "solutions"): {
        "summary": (
            "### अध्याय अवलोकन एवं सांद्रता इकाइयाँ\n"
            "- विलयन दो या अधिक घटकों का समांगी मिश्रण होता है।\n"
            "- **मोलरता ($M$)**: प्रति लीटर विलयन में विलेय के मोलों की संख्या (ताप पर निर्भर)।\n"
            "- **मोललता ($m$)**: प्रति किलोग्राम विलायक में विलेय के मोलों की संख्या (ताप पर स्वतंत्र)।\n"
            "- **मोल अंश ($x$)**: घटक के मोलों का कुल मोलों से अनुपात।\n\n"
            "### हेनरी का नियम तथा राउल्ट का नियम\n"
            "- **हेनरी का नियम**: गैस की विलेयता $p = K_H \\cdot x$। उच्च $K_H$ मान पर गैस की विलेयता कम होती है।\n"
            "- **राउल्ट का नियम**: वाष्पशील द्रवों के लिए $p_A = p_A^\\circ x_A$।\n"
            "- **अणुसंख्य गुणधर्म**: केवल विलेय कणों की संख्या पर निर्भर करते हैं, उनकी प्रकृति पर नहीं:\n"
            "  1. वाष्प दाब का आपेक्षिक अवनमन: $\\frac{p_A^\\circ - p_A}{p_A^\\circ} = x_B$\n"
            "  2. क्वथनांक का उन्नयन: $\\Delta T_b = i \\cdot K_b \\cdot m$\n"
            "  3. हिमांक का अवनमन: $\\Delta T_f = i \\cdot K_f \\cdot m$\n"
            "  4. परासरण दाब: $\\Pi = i \\cdot CRT$\n"
            "- **वांट हॉफ गुणांक ($i$)**: संगुणन ($i < 1$) या वियोजन ($i > 1$) की मात्रा दर्शाता है।"
        ),
        "takeaways": [
            "मोललता तथा मोल अंश ताप परिवर्तन से अप्रभावित रहते हैं।",
            "ताप बढ़ाने पर हेनरी स्थिरांक KH बढ़ता है जिससे गैसों की विलेयता घटती है।",
            "अणुसंख्य गुणधर्म केवल विलेय कणों की सांद्रता पर निर्भर करते हैं।",
            "वांट हॉफ गुणांक i असामान्य मोलर द्रव्यमान के संशोधन में उपयोगी है।"
        ],
    },
}


def generate_hindi_notes_for_chapter(
    grade: int, subject: str, chapter: str
) -> tuple[str, list[str]]:
    eng_chapter = normalize_chapter_to_english(chapter)
    key = (grade, eng_chapter.strip().lower())
    if key in KNOWN_CHAPTER_NOTES_HI:
        item = KNOWN_CHAPTER_NOTES_HI[key]
        return item["summary"], item["takeaways"]

    hi_subject = get_hindi_subject_name(subject)
    hi_chapter = get_hindi_chapter_name(chapter)
    eng_sub_lower = normalize_subject_to_english(subject).lower()

    if "math" in eng_sub_lower or "गणित" in hi_subject:
        summary = (
            f"### कक्षा {grade} गणित — {hi_chapter}\n\n"
            f"#### 1. मूल गणितीय अवधारणा\n"
            f"- **अध्याय का केंद्र**: आधिकारिक NCERT पाठ्यक्रम के अनुसार **{hi_chapter}** के आधारभूत नियम, प्रमेय तथा सूत्र।\n"
            f"- **सिद्धांत एवं अवधारणा**: परिभाषाओं, प्रतिबंधों तथा हल करने की मानक विधियों को स्पष्ट रूप से समझें।\n\n"
            f"#### 2. महत्वपूर्ण सूत्र, प्रमेय एवं विधियाँ\n"
            f"- *{hi_chapter}* से संबंधित सभी बीजगणितीय सर्वसमिकाएँ एवं प्रमेय याद रखें।\n"
            f"- प्रत्येक गणना को चरणबद्ध (Step-by-step) तरीके से उचित संकेतों व मात्रकों के साथ लिखें।\n"
            f"- शून्य विभाजक प्रतिबंधों एवं आकृतियों की ज्यामितीय विशेषताओं का ध्यान रखें।\n\n"
            f"#### 3. परीक्षा में अंक प्राप्त करने की रणनीति\n"
            f"- NCERT उदाहरणों तथा प्रश्नावली के प्रश्नों को स्वयं हल करके अभ्यास करें।\n"
            f"- बोर्ड परीक्षा में प्रत्येक चरण के पीछे प्रयुक्त प्रमेय व सूत्र का कारण अवश्य लिखें।"
        )
        takeaways = [
            f"{hi_chapter} के सभी मुख्य सूत्रों एवं प्रमेयों को कंठस्थ करें।",
            "उत्तर-पुस्तिका में सभी चरणों को स्पष्ट लिखें ताकि स्टेप-मार्किंग का लाभ मिले।",
            "NCERT अभ्यास प्रश्नों तथा उदाहरणों को बार-बार हल करें।"
        ]
    elif any(k in eng_sub_lower for k in ["physics", "science", "chemistry", "biology"]) or any(k in hi_subject for k in ["विज्ञान", "भौतिक", "रसायन", "जीव"]):
        summary = (
            f"### कक्षा {grade} {hi_subject} — {hi_chapter}\n\n"
            f"#### 1. वैज्ञानिक अवलोकन एवं परिघटना\n"
            f"- **मुख्य विषय**: NCERT पाठ्यपुस्तक के अनुसार **{hi_chapter}** के आधारभूत वैज्ञानिक सिद्धांत, नियम एवं प्रायोगिक अवलोकन।\n"
            f"- **प्रक्रिया एवं क्रियाविधि**: कार्य-कारण संबंध, रासायनिक समीकरणों तथा प्राकृतिक नियमों को भली-भाँति समझें।\n\n"
            f"#### 2. महत्वपूर्ण परिभाषाएँ, नियम एवं समीकरण\n"
            f"- वैज्ञानिक नियमों व परिभाषाओं को सटीक शब्दों में याद रखें।\n"
            f"- आंकिक प्रश्नों में: दिए गए मान, मानक SI मात्रक, सूत्र एवं इकाई सहित अंतिम उत्तर लिखें।\n"
            f"- जीव विज्ञान में: नामांकित स्वच्छ रेखाचित्र बनाने का अभ्यास करें।\n\n"
            f"#### 3. उच्च-अंक NCERT परीक्षा बिंदु\n"
            f"- NCERT पाठ के सारांश व विशेष बिंदुओं को अनिवार्य रूप से दोहराएँ।\n"
            f"- कथन-कारण (Assertion-Reason) एवं केस-आधारित प्रश्नों पर विशेष ध्यान दें।"
        )
        takeaways = [
            f"{hi_chapter} के वैज्ञानिक नियमों, परिभाषाओं व सूत्रों को याद रखें।",
            "स्वच्छ नामांकित चित्रों व आंकिक प्रश्नों में SI मात्रकों का ध्यान रखें।",
            "NCERT के क्रियाकलापों एवं सारांश बिंदुओं की पुनरावृत्ति करें।"
        ]
    elif any(k in eng_sub_lower for k in ["social", "history", "geography", "civics", "economics"]) or "सामाजिक" in hi_subject:
        summary = (
            f"### कक्षा {grade} {hi_subject} — {hi_chapter}\n\n"
            f"#### 1. ऐतिहासिक एवं सामाजिक-आर्थिक परिप्रेक्ष्य\n"
            f"- **केंद्रीय विषय**: **{hi_chapter}** के मुख्य ऐतिहासिक घटनाक्रम, भौगोलिक स्वरूप तथा लोकतांत्रिक संस्थाओं की समझ।\n"
            f"- **समय-रेखा एवं कारण**: महत्वपूर्ण घटनाओं के कारणों, परिणामों तथा सामाजिक प्रभावों का विश्लेषण करें।\n\n"
            f"#### 2. मुख्य शब्दावली एवं अवधारणाएँ\n"
            f"- महत्वपूर्ण तिथियों, संवैधानिक अनुच्छेदों तथा भौगोलिक वर्गीकरणों को याद रखें।\n"
            f"- सामाजिक, आर्थिक एवं राजनीतिक पहलुओं को बिंदुवार समझें।\n\n"
            f"#### 3. उत्तर लेखन रणनीति\n"
            f"- उत्तर लिखते समय मुख्य शीर्षकों एवं बुलेट-पॉइंट्स का प्रयोग करें।\n"
            f"- आवश्यकतानुसार मानचित्र (Map Work) का नियमित अभ्यास करें।"
        )
        takeaways = [
            f"{hi_chapter} की प्रमुख तिथियों, परिभाषाओं व स्थानों को याद रखें।",
            "वर्णनात्मक उत्तरों को उप-शीर्षकों व बिंदुओं में लिखें।",
            "मानचित्र कार्य (Map-work) का अभ्यास अवश्य करें।"
        ]
    elif "environmental" in eng_sub_lower or "पर्यावरण" in hi_subject or grade <= 5:
        summary = (
            f"### कक्षा {grade} {hi_subject} — {hi_chapter}\n\n"
            f"#### 1. प्रकृति एवं परिवेश की समझ\n"
            f"- **{hi_chapter}** में अपने आस-पास के वातावरण, पेड़-पौधों, जीव-जंतुओं और समाज को जानें।\n"
            f"- प्रकृति के संतुलन और पर्यावरण संरक्षण के महत्व को समझें।\n\n"
            f"#### 2. दैनिक जीवन के अनुभव एवं गतिविधियाँ\n"
            f"- पाठ की बातों को अपने दैनिक जीवन, मौसम, स्वास्थ्य व परिवार के अनुभवों से जोड़ें।\n"
            f"- स्वच्छता, अच्छी आदतों व पर्यावरण की सुरक्षा का अभ्यास करें।\n\n"
            f"#### 3. सीखने के मुख्य बिंदु\n"
            f"- अपने आस-पास की दुनिया के प्रति जिज्ञासु और जागरूक बनें।"
        )
        takeaways = [
            f"{hi_chapter} से जुड़े दैनिक जीवन के उदाहरणों को समझें।",
            "पर्यावरण के नियमों और अच्छी आदतों का पालन करें।",
            "चित्रों और गतिविधियों के माध्यम से आनंदपूर्वक सीखें।"
        ]
    else:
        summary = (
            f"### कक्षा {grade} {hi_subject} — {hi_chapter}\n\n"
            f"#### 1. अध्याय का सारांश\n"
            f"- आधिकारिक NCERT पाठ्यक्रम के अनुसार **{hi_chapter}** की विस्तृत अध्ययन सामग्री।\n"
            f"- पाठ के मूल भाव, पात्रों के चरित्र-चित्रण एवं केंद्रीय संदेश को समझें।\n\n"
            f"#### 2. मुख्य बिंदु एवं सीख\n"
            f"- कठिन शब्दों के अर्थ, व्याकरण के नियम एवं भाषा-शैली का अभ्यास करें।\n"
            f"- पाठ के नैतिक संदेश को समझें।\n\n"
            f"#### 3. NCERT अभ्यास प्रश्न\n"
            f"- पाठ के अंत में दिए गए प्रश्नों के संक्षिप्त व स्पष्ट उत्तर लिखने का अभ्यास करें।"
        )
        takeaways = [
            f"{hi_chapter} के मुख्य संदेश और सारांश को समझें।",
            "NCERT पाठ्यपुस्तक के प्रश्नों का उत्तर लिखने का अभ्यास करें।",
            "शब्दार्थ एवं व्याकरण के नियमों को दोहराएँ।"
        ]

    return summary, takeaways
