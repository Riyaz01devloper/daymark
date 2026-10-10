import urllib.parse
from typing import Any

from app.hindi_curriculum import (
    ENGLISH_SUBJECTS,
    HINDI_CHAPTER_REVERSE,
    HINDI_CHAPTER_TRANSLATIONS,
    HINDI_SUBJECTS,
    generate_hindi_notes_for_chapter,
    get_hindi_chapter_name,
    get_hindi_subject_name,
    normalize_chapter_to_english,
    normalize_subject_to_english,
)

# Standard NCERT Curriculum mappings by Class -> Subject -> Chapters

NCERT_CURRICULUM = {
    10: {
        "Science": [
            "Chemical Reactions and Equations",
            "Acids, Bases and Salts",
            "Metals and Non-Metals",
            "Carbon and its Compounds",
            "Life Processes",
            "Control and Coordination",
            "How do Organisms Reproduce?",
            "Heredity",
            "Light – Reflection and Refraction",
            "The Human Eye and the Colourful World",
            "Electricity",
            "Magnetic Effects of Electric Current",
            "Our Environment",
        ],
        "Mathematics": [
            "Real Numbers",
            "Polynomials",
            "Pair of Linear Equations in Two Variables",
            "Quadratic Equations",
            "Arithmetic Progressions",
            "Triangles",
            "Coordinate Geometry",
            "Introduction to Trigonometry",
            "Some Applications of Trigonometry",
            "Circles",
            "Areas Related to Circles",
            "Surface Areas and Volumes",
            "Statistics",
            "Probability",
        ],
        "Social Science": [
            "The Rise of Nationalism in Europe",
            "Nationalism in India",
            "The Making of a Global World",
            "Resources and Development",
            "Forest and Wildlife Resources",
            "Water Resources",
            "Agriculture",
            "Power Sharing",
            "Federalism",
            "Gender, Religion and Caste",
            "Development",
            "Sectors of the Indian Economy",
            "Money and Credit",
        ],
        "English": [
            "A Letter to God",
            "Nelson Mandela: Long Walk to Freedom",
            "Two Stories about Flying",
            "From the Diary of Anne Frank",
            "Glimpses of India",
            "Mijbil the Otter",
            "Madam Rides the Bus",
            "The Sermon at Benares",
            "The Proposal",
        ],
    },
    9: {
        "Science": [
            "Matter in Our Surroundings",
            "Is Matter Around Us Pure?",
            "Atoms and Molecules",
            "Structure of the Atom",
            "The Fundamental Unit of Life",
            "Tissues",
            "Motion",
            "Force and Laws of Motion",
            "Gravitation",
            "Work and Energy",
            "Sound",
            "Improvement in Food Resources",
        ],
        "Mathematics": [
            "Number Systems",
            "Polynomials",
            "Coordinate Geometry",
            "Linear Equations in Two Variables",
            "Introduction to Euclid's Geometry",
            "Lines and Angles",
            "Triangles",
            "Quadrilaterals",
            "Circles",
            "Heron's Formula",
            "Surface Areas and Volumes",
            "Statistics",
        ],
        "Social Science": [
            "The French Revolution",
            "Socialism in Europe and the Russian Revolution",
            "Nazism and the Rise of Hitler",
            "India - Size and Location",
            "Physical Features of India",
            "Drainage",
            "Climate",
            "What is Democracy? Why Democracy?",
            "Constitutional Design",
            "The Story of Village Palampur",
            "People as Resource",
        ],
        "English": [
            "The Fun They Had",
            "The Sound of Music",
            "The Little Girl",
            "A Truly Beautiful Mind",
            "The Snake and the Mirror",
            "My Childhood",
            "Reach for the Top",
            "Kathmandu",
            "If I Were You",
        ],
    },
    12: {
        "Physics": [
            "Electric Charges and Fields",
            "Electrostatic Potential and Capacitance",
            "Current Electricity",
            "Moving Charges and Magnetism",
            "Magnetism and Matter",
            "Electromagnetic Induction",
            "Alternating Current",
            "Electromagnetic Waves",
            "Ray Optics and Optical Instruments",
            "Wave Optics",
            "Dual Nature of Radiation and Matter",
            "Atoms",
            "Nuclei",
            "Semiconductor Electronics",
        ],
        "Chemistry": [
            "Solutions",
            "Electrochemistry",
            "Chemical Kinetics",
            "The d- and f-Block Elements",
            "Coordination Compounds",
            "Haloalkanes and Haloarenes",
            "Alcohols, Phenols and Ethers",
            "Aldehydes, Ketones and Carboxylic Acids",
            "Amines",
            "Biomolecules",
        ],
        "Mathematics": [
            "Relations and Functions",
            "Inverse Trigonometric Functions",
            "Matrices",
            "Determinants",
            "Continuity and Differentiability",
            "Application of Derivatives",
            "Integrals",
            "Application of Integrals",
            "Differential Equations",
            "Vector Algebra",
            "Three Dimensional Geometry",
            "Linear Programming",
            "Probability",
        ],
        "Biology": [
            "Sexual Reproduction in Flowering Plants",
            "Human Reproduction",
            "Reproductive Health",
            "Principles of Inheritance and Variation",
            "Molecular Basis of Inheritance",
            "Evolution",
            "Human Health and Disease",
            "Microbes in Human Welfare",
            "Biotechnology: Principles and Processes",
            "Biotechnology and its Applications",
            "Organisms and Populations",
            "Ecosystem",
            "Biodiversity and Conservation",
        ],
    },
    11: {
        "Physics": [
            "Units and Measurements",
            "Motion in a Straight Line",
            "Motion in a Plane",
            "Laws of Motion",
            "Work, Energy and Power",
            "System of Particles and Rotational Motion",
            "Gravitation",
            "Mechanical Properties of Solids",
            "Mechanical Properties of Fluids",
            "Thermal Properties of Matter",
            "Thermodynamics",
            "Kinetic Theory",
            "Oscillations",
            "Waves",
        ],
        "Chemistry": [
            "Some Basic Concepts of Chemistry",
            "Structure of Atom",
            "Classification of Elements and Periodicity in Properties",
            "Chemical Bonding and Molecular Structure",
            "Thermodynamics",
            "Equilibrium",
            "Redox Reactions",
            "Organic Chemistry: Some Basic Principles and Techniques",
            "Hydrocarbons",
        ],
        "Mathematics": [
            "Sets",
            "Relations and Functions",
            "Trigonometric Functions",
            "Complex Numbers and Quadratic Equations",
            "Linear Inequalities",
            "Permutations and Combinations",
            "Binomial Theorem",
            "Sequences and Series",
            "Straight Lines",
            "Conic Sections",
            "Introduction to Three Dimensional Geometry",
            "Limits and Derivatives",
            "Statistics",
            "Probability",
        ],
    },
    8: {
        "Science": [
            "Crop Production and Management",
            "Microorganisms: Friend and Foe",
            "Coal and Petroleum",
            "Combustion and Flame",
            "Conservation of Plants and Animals",
            "Reproduction in Animals",
            "Reaching the Age of Adolescence",
            "Force and Pressure",
            "Friction",
            "Sound",
            "Chemical Effects of Electric Current",
            "Some Natural Phenomena",
            "Light",
        ],
        "Mathematics": [
            "Rational Numbers",
            "Linear Equations in One Variable",
            "Understanding Quadrilaterals",
            "Data Handling",
            "Squares and Square Roots",
            "Cubes and Cube Roots",
            "Comparing Quantities",
            "Algebraic Expressions and Identities",
            "Mensuration",
            "Exponents and Powers",
            "Direct and Inverse Proportions",
            "Factorisation",
            "Introduction to Graphs",
        ],
        "Social Science": [
            "How, When and Where",
            "From Trade to Territory",
            "Ruling the Countryside",
            "When People Rebel 1857",
            "Resources",
            "Land, Soil, Water, Natural Vegetation",
            "Agriculture",
            "Industries",
            "The Indian Constitution",
            "Understanding Secularism",
            "Parliament and Making of Laws",
            "Judiciary",
        ],
        "English": [
            "The Best Christmas Present in the World",
            "The Tsunami",
            "Glimpses of the Past",
            "Bepin Choudhury's Lapse of Memory",
            "The Summit Within",
            "This is Jody's Fawn",
            "A Visit to Cambridge",
            "A Short Monsoon Diary",
        ],
    },
    7: {
        "Science": [
            "Nutrition in Plants",
            "Nutrition in Animals",
            "Heat",
            "Acids, Bases and Salts",
            "Physical and Chemical Changes",
            "Respiration in Organisms",
            "Transportation in Animals and Plants",
            "Reproduction in Plants",
            "Motion and Time",
            "Electric Current and its Effects",
            "Light",
            "Forests: Our Lifeline",
        ],
        "Mathematics": [
            "Integers",
            "Fractions and Decimals",
            "Data Handling",
            "Simple Equations",
            "Lines and Angles",
            "The Triangle and its Properties",
            "Comparing Quantities",
            "Rational Numbers",
            "Perimeter and Area",
            "Algebraic Expressions",
            "Exponents and Powers",
            "Symmetry",
        ],
        "Social Science": [
            "Tracing Changes Through a Thousand Years",
            "New Kings and Kingdoms",
            "The Delhi Sultans",
            "The Mughal Empire",
            "Environment",
            "Inside Our Earth",
            "Our Changing Earth",
            "Air",
            "Water",
            "On Equality",
            "Role of the Government in Health",
        ],
        "English": [
            "Three Questions",
            "A Gift of Chappals",
            "Gopal and the Hilsa Fish",
            "The Ashes That Made Trees Bloom",
            "Quality",
            "Expert Detectives",
            "The Invention of Vita-Wonk",
        ],
    },
    6: {
        "Science": [
            "Components of Food",
            "Sorting Materials into Groups",
            "Separation of Substances",
            "Getting to Know Plants",
            "Body Movements",
            "The Living Organisms — Characteristics and Habitats",
            "Motion and Measurement of Distances",
            "Light, Shadows and Reflections",
            "Electricity and Circuits",
            "Fun with Magnets",
            "Air Around Us",
        ],
        "Mathematics": [
            "Knowing Our Numbers",
            "Whole Numbers",
            "Playing with Numbers",
            "Basic Geometrical Ideas",
            "Understanding Elementary Shapes",
            "Integers",
            "Fractions",
            "Decimals",
            "Data Handling",
            "Mensuration",
            "Algebra",
            "Ratio and Proportion",
        ],
        "Social Science": [
            "What, Where, How and When?",
            "From Hunting-Gathering to Growing Food",
            "In the Earliest Cities",
            "What Books and Burials Tell Us",
            "Kingdoms, Kings and an Early Republic",
            "The Earth in the Solar System",
            "Globe: Latitudes and Longitudes",
            "Motions of the Earth",
            "Maps",
            "Understanding Diversity",
            "Diversity and Discrimination",
        ],
        "English": [
            "Who Did Patrick's Homework?",
            "How the Dog Found Himself a New Master!",
            "Taro's Reward",
            "An Indian - American Woman in Space: Kalpana Chawla",
            "A Different Kind of School",
            "Who I Am",
            "Fair Play",
        ],
    },
    5: {
        "Mathematics": ["The Fish Tale", "Shapes and Angles", "How Many Squares?", "Parts and Wholes", "Does it Look the Same?", "Be My Multiple, I'll be Your Factor", "Can You See the Pattern?"],
        "Environmental Studies": ["Super Senses", "A Snake Charmer's Story", "From Tasting to Digesting", "Mangoes Round the Year", "Seeds and Seeds", "Every Drop Counts", "Experiments with Water"],
        "English": ["Ice-Cream Man", "Wonderful Waste!", "Flying Together", "My Shadow", "Robinson Crusoe", "Class Discussion"],
    },
    4: {
        "Mathematics": ["Building with Bricks", "Long and Short", "A Trip to Bhopal", "Tick-Tick-Tick", "The Way The World Looks", "The Junk Seller", "Jugs and Mugs"],
        "Environmental Studies": ["Going to School", "Ear to Ear", "A Day with Nandu", "The Story of Amrita", "Anita and the Honeybees", "Omana's Journey"],
        "English": ["Wake Up!", "Neha's Alarm Clock", "Noses", "The Little Fir Tree", "Run!", "Nasruddin's Aim"],
    },
    3: {
        "Mathematics": ["Where to Look From", "Fun with Numbers", "Give and Take", "Long and Short", "Shapes and Designs", "Fun with Give and Take", "Time Goes On"],
        "Environmental Studies": ["Poonam's Day out", "The Plant Fairy", "Water O' Water!", "Our First School", "Chhotu's House", "Foods We Eat"],
        "English": ["Good Morning", "The Magic Garden", "Bird Talk", "Nina and the Baby Sparrows", "Little by Little", "The Enormous Turnip"],
    },
    2: {
        "Mathematics": ["What is Long, What is Round?", "Counting in Groups", "How Much Can You Carry?", "Counting in Tens", "Patterns", "Footprints"],
        "Environmental Studies": ["My Body", "My Family", "Food and Health", "Clothes We Wear", "Our Neighborhood", "Safety and First Aid"],
        "English": ["First Day at School", "Haldi's Adventure", "I am Lucky!", "I Want", "A Smile", "The Wind and the Sun"],
    },
    1: {
        "Mathematics": ["Shapes and Space", "Numbers from One to Nine", "Addition", "Subtraction", "Numbers from Ten to Twenty", "Time", "Measurement"],
        "Environmental Studies": ["About Me", "My Body Parts", "My Home and Family", "Animals Around Us", "Plants Around Us", "Good Habits"],
        "English": ["A Happy Child", "Three Little Pigs", "After a Bath", "The Bubble, the Straw and the Shoe", "One Little Kitten", "Lalu and Peelu"],
    },
}

# Default generic subjects for any grade 1-12
DEFAULT_CLASS_SUBJECTS = {
    "primary": ["English", "Mathematics", "Environmental Studies", "Hindi"],
    "middle": ["Mathematics", "Science", "Social Science", "English", "Hindi"],
    "secondary": ["Mathematics", "Science", "Social Science", "English"],
    "senior": ["Physics", "Chemistry", "Mathematics", "Biology", "English", "Computer Science"],
}

INITIAL_PYQS = [
    {
        "class_grade": 10,
        "subject": "Science",
        "chapter": "Chemical Reactions and Equations",
        "year": 2024,
        "exam_type": "CBSE Board",
        "marks": 3,
        "question": "Why does the color of copper sulphate solution change when an iron nail is dipped in it? Write the balanced chemical equation and identify the type of reaction.",
        "answer": "When an iron nail is placed in copper sulphate (CuSO4) solution, iron is more reactive than copper, so it displaces copper to form iron(II) sulphate (FeSO4). The blue solution changes to pale green and a reddish-brown copper coating deposits on the nail.\nEquation: Fe(s) + CuSO4(aq) -> FeSO4(aq) + Cu(s).\nReaction Type: Displacement Reaction.",
    },
    {
        "class_grade": 10,
        "subject": "Science",
        "chapter": "Life Processes",
        "year": 2023,
        "exam_type": "CBSE Board",
        "marks": 5,
        "question": "Describe the process of double circulation in human beings with its significance.",
        "answer": "Double circulation means blood flows through the heart twice during each complete cycle:\n1. Pulmonary Circulation: Deoxygenated blood is pumped from the right ventricle to lungs for oxygenation and returns to the left atrium.\n2. Systemic Circulation: Oxygenated blood from the left ventricle is pumped to all body tissues and deoxygenated blood returns to the right atrium.\nSignificance: It completely prevents mixing of oxygenated and deoxygenated blood, providing high energy efficiency required to maintain constant body temperature in warm-blooded organisms.",
    },
    {
        "class_grade": 10,
        "subject": "Science",
        "chapter": "Electricity",
        "year": 2023,
        "exam_type": "CBSE Board",
        "marks": 3,
        "question": "State Joule's law of heating. Derive the formula H = I^2 * R * t from Ohm's law.",
        "answer": "Joule's law states that heat produced in a resistor is directly proportional to:\n1. Square of current (I^2)\n2. Resistance of conductor (R)\n3. Time current flows (t).\nDerivation: Electric work done W = V * Q. Since Q = I * t, W = V * I * t. By Ohm's law, V = I * R. Substituting V, Heat H = W = (I * R) * I * t = I^2 * R * t.",
    },
    {
        "class_grade": 10,
        "subject": "Mathematics",
        "chapter": "Real Numbers",
        "year": 2024,
        "exam_type": "CBSE Board",
        "marks": 3,
        "question": "Prove that √5 is an irrational number using the method of contradiction.",
        "answer": "Assume √5 is rational. Then √5 = a/b where a and b are coprime integers and b ≠ 0.\nSquaring both sides: 5 = a^2 / b^2 => a^2 = 5b^2.\nThus 5 divides a^2, which implies 5 divides a (by theorem: if prime p divides a^2, p divides a).\nLet a = 5c. Then (5c)^2 = 5b^2 => 25c^2 = 5b^2 => b^2 = 5c^2.\nThus 5 divides b^2, meaning 5 divides b.\nHence 5 is a common factor of both a and b. This contradicts that a and b are coprime.\nTherefore, √5 is irrational.",
    },
    {
        "class_grade": 10,
        "subject": "Mathematics",
        "chapter": "Quadratic Equations",
        "year": 2022,
        "exam_type": "CBSE Board",
        "marks": 4,
        "question": "Find the discriminant of the quadratic equation 2x^2 - 4x + 3 = 0 and hence find the nature of its roots. If real roots exist, find them.",
        "answer": "Comparing with ax^2 + bx + c = 0: a = 2, b = -4, c = 3.\nDiscriminant D = b^2 - 4ac = (-4)^2 - 4(2)(3) = 16 - 24 = -8.\nSince D < 0, the equation has no real roots (roots are complex/imaginary).",
    },
    {
        "class_grade": 10,
        "subject": "Social Science",
        "chapter": "Nationalism in India",
        "year": 2023,
        "exam_type": "CBSE Board",
        "marks": 5,
        "question": "Explain the reasons why Mahatma Gandhi decided to launch the Non-Cooperation Movement in 1920.",
        "answer": "Key reasons:\n1. Rowlatt Act (1919): British government passed repressive laws allowing detention without trial.\n2. Jallianwala Bagh Massacre (1919): Brutal firing on unarmed peaceful crowd in Amritsar shocked the country.\n3. Khilafat Issue: Discontent over the treatment of the Ottoman Caliph; Gandhi saw this as opportunity to unite Hindus and Muslims.\n4. Economic Hardship: Post-WWI inflation, crop failure, and epidemic caused immense distress.\nGandhi believed British rule survived only with Indian cooperation; non-cooperation would collapse it.",
    },
    {
        "class_grade": 9,
        "subject": "Science",
        "chapter": "Motion",
        "year": 2023,
        "exam_type": "Annual Exam",
        "marks": 3,
        "question": "Differentiate between speed and velocity. Can an object have zero velocity but non-zero acceleration? Give an example.",
        "answer": "Differences:\n1. Speed is scalar (distance/time), velocity is vector (displacement/time with direction).\n2. Speed is always positive or zero; velocity can be positive, negative, or zero.\nYes: When a ball is thrown vertically upward, at the highest point its velocity is momentarily zero, but acceleration due to gravity (9.8 m/s^2 downwards) acts on it.",
    },
    {
        "class_grade": 12,
        "subject": "Physics",
        "chapter": "Electrostatic Potential and Capacitance",
        "year": 2024,
        "exam_type": "CBSE Board",
        "marks": 3,
        "question": "Derive an expression for the capacitance of a parallel plate capacitor with dielectric medium of constant K between its plates.",
        "answer": "For plate area A and separation d:\nElectric field without dielectric E0 = σ / ε0 = Q / (A * ε0).\nWith dielectric constant K, electric field becomes E = E0 / K = Q / (K * A * ε0).\nPotential difference V = E * d = (Q * d) / (K * A * ε0).\nCapacitance C = Q / V = (K * ε0 * A) / d = K * C0.\nHence dielectric increases capacitance by factor K.",
    },
]


def get_subjects_for_grade(grade: int | None, language: str = "en") -> list[str]:
    target_grade = grade if grade and 1 <= grade <= 12 else 10
    if target_grade in NCERT_CURRICULUM:
        subs = list(NCERT_CURRICULUM[target_grade].keys())
    elif target_grade <= 5:
        subs = DEFAULT_CLASS_SUBJECTS["primary"]
    elif target_grade <= 8:
        subs = DEFAULT_CLASS_SUBJECTS["middle"]
    elif target_grade <= 10:
        subs = DEFAULT_CLASS_SUBJECTS["secondary"]
    else:
        subs = DEFAULT_CLASS_SUBJECTS["senior"]

    if language in ("hi", "hindi"):
        return [get_hindi_subject_name(s) for s in subs]
    return subs


def get_curriculum_for_grade(
    grade: int | None, language: str = "en"
) -> dict[str, list[str]]:
    target_grade = grade if grade and 1 <= grade <= 12 else 10
    raw = NCERT_CURRICULUM.get(target_grade, {})
    if language in ("hi", "hindi"):
        return {
            get_hindi_subject_name(sub): [get_hindi_chapter_name(ch) for ch in chs]
            for sub, chs in raw.items()
        }
    return raw


def get_chapters_for_grade_subject(
    grade: int, subject: str, language: str = "en"
) -> list[str]:
    eng_sub = normalize_subject_to_english(subject)
    grade_data = NCERT_CURRICULUM.get(grade, {})
    for sub, chapters in grade_data.items():
        if sub.lower() == eng_sub.lower():
            if language in ("hi", "hindi"):
                return [get_hindi_chapter_name(ch) for ch in chapters]
            return chapters
    return []


OFFICIAL_RESOURCES: dict[int, dict[str, str | int]] = {
    10: {
        "class_grade": 10,
        "title": "Class 10 CBSE & NCERT Official Resources",
        "board_pyq_url": "https://www.cbse.gov.in/cbsenew/question-paper.html",
        "sqp_2024_25_url": "https://cbseacademic.nic.in/SQP_CLASSX_2024-25.html",
        "sqp_2023_24_url": "https://cbseacademic.nic.in/SQP_CLASSX_2023-24.html",
        "sqp_2022_23_url": "https://cbseacademic.nic.in/sqp_classx_2022-23.html",
        "question_bank_url": "https://cbseacademic.nic.in/qbclass10.html",
        "ncert_books_url": "https://ncert.nic.in/textbook.php",
        "ncert_ebooks_url": "https://ncert.nic.in/ebooks.php",
        "ncert_exemplar_url": "https://ncert.nic.in/exemplar-problems.php",
        "curriculum_url": "https://cbseacademic.nic.in/curriculum_2025.html",
    },
    12: {
        "class_grade": 12,
        "title": "Class 12 CBSE & NCERT Official Resources",
        "board_pyq_url": "https://www.cbse.gov.in/cbsenew/question-paper.html",
        "sqp_2024_25_url": "https://cbseacademic.nic.in/SQP_CLASSXII_2024-25.html",
        "sqp_2023_24_url": "https://cbseacademic.nic.in/SQP_CLASSXII_2023-24.html",
        "sqp_2022_23_url": "https://cbseacademic.nic.in/sqp_classxii_2022-23.html",
        "question_bank_url": "https://cbseacademic.nic.in/qbclass12.html",
        "ncert_books_url": "https://ncert.nic.in/textbook.php",
        "ncert_ebooks_url": "https://ncert.nic.in/ebooks.php",
        "ncert_exemplar_url": "https://ncert.nic.in/exemplar-problems.php",
        "curriculum_url": "https://cbseacademic.nic.in/curriculum_2025.html",
    },
}


def get_official_resources_for_grade(
    grade: int | None, language: str = "en"
) -> dict[str, str | int]:
    target_grade = grade if grade and 1 <= grade <= 12 else 10
    is_hi = language in ("hi", "hindi")
    res = OFFICIAL_RESOURCES.get(target_grade, {
        "class_grade": target_grade,
        "title": f"Class {target_grade} Official Study Resources",
        "board_pyq_url": "https://www.cbse.gov.in/cbsenew/question-paper.html",
        "sqp_2024_25_url": "https://cbseacademic.nic.in/SQP_CLASSX_2024-25.html" if target_grade <= 10 else "https://cbseacademic.nic.in/SQP_CLASSXII_2024-25.html",
        "sqp_2023_24_url": "https://cbseacademic.nic.in/SQP_CLASSX_2023-24.html" if target_grade <= 10 else "https://cbseacademic.nic.in/SQP_CLASSXII_2023-24.html",
        "sqp_2022_23_url": "https://cbseacademic.nic.in/sqp_classx_2022-23.html" if target_grade <= 10 else "https://cbseacademic.nic.in/sqp_classxii_2022-23.html",
        "question_bank_url": f"https://cbseacademic.nic.in/qbclass{target_grade}.html" if target_grade in (10, 12) else "https://cbseacademic.nic.in/cbe/",
        "ncert_books_url": "https://ncert.nic.in/textbook.php",
        "ncert_ebooks_url": "https://ncert.nic.in/ebooks.php",
        "ncert_exemplar_url": "https://ncert.nic.in/exemplar-problems.php",
        "curriculum_url": "https://cbseacademic.nic.in/curriculum_2025.html",
    }).copy()

    if is_hi:
        res["title"] = f"कक्षा {target_grade} सीबीएसई एवं एनसीईआरटी आधिकारिक अध्ययन सामग्री"
    return res


KNOWN_CHAPTER_NOTES: dict[tuple[int, str], dict[str, Any]] = {
    (10, "chemical reactions and equations"): {
        "summary": (
            "### Overview & Core Concepts\n"
            "- **Chemical Reaction**: Process where reactants transform into products with distinct chemical properties.\n"
            "- **Observation Clues**: Change in state, color change, evolution of a gas, temperature fluctuation, or precipitate formation.\n"
            "- **Law of Conservation of Mass**: Total mass of reactants must equal total mass of products; atoms are neither created nor destroyed.\n\n"
            "### Major Types of Reactions\n"
            "1. **Combination**: $A + B \\rightarrow AB$ (e.g., $CaO + H_2O \\rightarrow Ca(OH)_2$ quicklime to slaked lime).\n"
            "2. **Decomposition**: Single reactant breaks down under heat (thermal), light (photolytic), or electricity (electrolytic).\n"
            "3. **Displacement**: More reactive metal displaces less reactive metal ($Fe + CuSO_4 \\rightarrow FeSO_4 + Cu$).\n"
            "4. **Double Displacement & Precipitation**: Exchange of ions between reactants ($Na_2SO_4 + BaCl_2 \\rightarrow BaSO_4\\downarrow + 2NaCl$).\n"
            "5. **Redox (Oxidation & Reduction)**: Oxidation is gain of oxygen / loss of hydrogen / loss of electrons; Reduction is loss of oxygen / gain of hydrogen / gain of electrons.\n\n"
            "### Practical Everyday Redox Phenomena\n"
            "- **Corrosion**: Degradation of metals exposed to moisture and oxygen (rusting of iron: hydrated iron(III) oxide).\n"
            "- **Rancidity**: Aerial oxidation of fats and oils leading to unpleasant odor and flavor; prevented with antioxidants or nitrogen packaging.\n\n"
            "### NCERT High-Yield Exam Pointers\n"
            "- Always specify physical state symbols: (s), (l), (g), (aq).\n"
            "- Remember key precipitate colors: White for barium sulphate, yellow for lead iodide ($PbI_2$).\n"
            "- Respiration is exothermic; decomposition of calcium carbonate is endothermic."
        ),
        "takeaways": [
            "Balanced chemical equations satisfy the Law of Conservation of Mass.",
            "Know all 5 reaction types with at least one balanced example equation.",
            "Redox involves simultaneous reduction and oxidation.",
            "Corrosion and rancidity are everyday oxidation effects."
        ],
    },
    (10, "electricity"): {
        "summary": (
            "### Overview & Core Concepts\n"
            "- **Electric Current ($I$)**: Rate of flow of electric charges. $I = Q / t$, measured in Amperes (A).\n"
            "- **Potential Difference ($V$)**: Work done per unit charge moving between two points. $V = W / Q$, measured in Volts (V).\n\n"
            "### Fundamental Laws & Formulas\n"
            "- **Ohm's Law**: At constant temperature, $V \\propto I \\implies V = IR$.\n"
            "- **Resistance Factors**: $R = \\rho \\frac{l}{A}$ (directly proportional to length, inversely proportional to cross-sectional area).\n"
            "- **Series Combination**: $R_s = R_1 + R_2 + \\dots$; current remains uniform, voltage divides.\n"
            "- **Parallel Combination**: $\\frac{1}{R_p} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\dots$; voltage remains constant, current divides.\n"
            "- **Joule's Heating Law**: $H = I^2 R t$.\n"
            "- **Electric Power**: $P = VI = I^2 R = \\frac{V^2}{R}$. Commercial unit is kilowatt-hour (1 kWh = $3.6 \\times 10^6$ J).\n\n"
            "### NCERT High-Yield Exam Pointers\n"
            "- Ammeter is always connected in series (low resistance); Voltmeter is always connected in parallel (high resistance).\n"
            "- Household circuits are connected in parallel to ensure independent appliance switching and equal supply voltage."
        ),
        "takeaways": [
            "Ohm's Law ($V = IR$) governs ohmic conductors at constant temperature.",
            "Equivalent resistance is maximum in series and minimum in parallel.",
            "Joule's heat $H = I^2 R t$ powers heaters, geysers, and fuses.",
            "1 kWh = 3.6 × 10^6 Joules."
        ],
    },
    (10, "real numbers"): {
        "summary": (
            "### Overview & Core Concepts\n"
            "- **Fundamental Theorem of Arithmetic**: Every composite number can be expressed (factorized) as a product of primes uniquely, apart from the order of prime factors.\n"
            "- **HCF and LCM Relationship**: For two positive integers $a$ and $b$, $\\text{HCF}(a, b) \\times \\text{LCM}(a, b) = a \\times b$.\n\n"
            "### Proof of Irrationality\n"
            "- Proof by contradiction for numbers like $\\sqrt{2}$, $\\sqrt{3}$, $\\sqrt{5}$, and $a + b\\sqrt{p}$.\n"
            "- Assume rational as $\\frac{p}{q}$ (coprime integers, $q \\neq 0$), square both sides, and deduce that both $p$ and $q$ share common factor, contradicting coprimality.\n\n"
            "### Exam Tips & Working Rules\n"
            "- In prime factorization trees, group powers of primes clearly.\n"
            "- State standard theorem reasons explicitly in subjective proofs for full step marks."
        ),
        "takeaways": [
            "Every composite number has a unique prime factorization.",
            "HCF(a, b) × LCM(a, b) = a × b (valid for two numbers only).",
            "Proof by contradiction is standard for proving irrationality of √p."
        ],
    },
    (12, "electric charges and fields"): {
        "summary": (
            "### Overview & Electrostatics Principles\n"
            "- **Coulomb's Law**: $F = \\frac{1}{4\\pi\\varepsilon_0} \\frac{|q_1 q_2|}{r^2}\\hat{r}$.\n"
            "- **Electric Field ($E$)**: Force per unit positive test charge. $E = \\frac{F}{q_0}$. Point charge: $E = \\frac{q}{4\\pi\\varepsilon_0 r^2}$.\n"
            "- **Electric Dipole Moment**: $\\vec{p} = q(2\\vec{a})$, directed from negative to positive charge.\n"
            "- **Torque on Dipole**: $\\vec{\\tau} = \\vec{p} \\times \\vec{E}$.\n\n"
            "### Gauss's Law & High-Yield Applications\n"
            "- **Gauss's Theorem**: Total electric flux through a closed surface $\\Phi = \\oint \\vec{E} \\cdot d\\vec{A} = \\frac{q_{\\text{enclosed}}}{\\varepsilon_0}$.\n"
            "- Infinitely long straight wire: $E = \\frac{\\lambda}{2\\pi\\varepsilon_0 r}$.\n"
            "- Infinite plane sheet of charge: $E = \\frac{\\sigma}{2\\varepsilon_0}$.\n"
            "- Thin spherical shell: $E_{\\text{out}} = \\frac{q}{4\\pi\\varepsilon_0 r^2}$; $E_{\\text{inside}} = 0$."
        ),
        "takeaways": [
            "Quantization of charge: Q = ne; Charge is scalar, conserved, and invariant.",
            "Gauss's Law relates electric flux through a Gaussian surface to enclosed net charge.",
            "Electric field inside a uniformly charged conducting shell is strictly zero."
        ],
    },
    (12, "solutions"): {
        "summary": (
            "### Overview & Concentration Units\n"
            "- Solutions are homogeneous mixtures of two or more components.\n"
            "- **Molarity ($M$)**: Moles of solute per liter of solution (temperature dependent).\n"
            "- **Molality ($m$)**: Moles of solute per kg of solvent (temperature independent).\n"
            "- **Mole Fraction ($x$)**: Ratio of moles of component to total moles.\n\n"
            "### Gas Solubility & Raoult's Law\n"
            "- **Henry's Law**: $p = K_H \\cdot x$. Higher $K_H$ implies lower gas solubility at a given temperature.\n"
            "- **Raoult's Law**: For volatile liquids, $p_A = p_A^\\circ x_A$.\n"
            "- **Colligative Properties**: Depend only on number of solute particles, not identity.\n"
            "  1. Relative lowering of vapor pressure: $\\frac{p_A^\\circ - p_A}{p_A^\\circ} = x_B$.\n"
            "  2. Elevation of boiling point: $\\Delta T_b = i \\cdot K_b \\cdot m$.\n"
            "  3. Depression of freezing point: $\\Delta T_f = i \\cdot K_f \\cdot m$.\n"
            "  4. Osmotic pressure: $\\Pi = i \\cdot CRT$.\n"
            "- **Van 't Hoff Factor ($i$)**: Measures association ($i < 1$) or dissociation ($i > 1$)."
        ),
        "takeaways": [
            "Molality and mole fraction are temperature independent concentration terms.",
            "Henry's law constant KH increases with temperature, reducing gas solubility.",
            "Colligative properties depend exclusively on solute particle concentration.",
            "Van 't Hoff factor i accounts for dissociation or association in non-ideal solutions."
        ],
    },
    (10, "acids, bases and salts"): {
        "summary": (
            "### Overview & Core Concepts\n"
            "- **Acids**: Sour taste, turn blue litmus red, release $H^+$ (or $H_3O^+$ hydronium) ions in aqueous solution.\n"
            "- **Bases**: Bitter taste, soapy feel, turn red litmus blue, release $OH^-$ hydroxide ions. Soluble bases are called alkalis.\n"
            "- **pH Scale (0 to 14)**: Measure of hydrogen ion concentration. $pH < 7$ acidic, $pH = 7$ neutral, $pH > 7$ basic. $pH = -\\log_{10}[H^+]$.\n\n"
            "### Chemical Reactions & Indicators\n"
            "- **Acid + Metal**: $\\text{Acid} + \\text{Metal} \\rightarrow \\text{Salt} + H_2\\uparrow$ ($Zn + 2HCl \\rightarrow ZnCl_2 + H_2\\uparrow$, pop sound test).\n"
            "- **Neutralization**: $\\text{Acid} + \\text{Base} \\rightarrow \\text{Salt} + H_2O$ ($HCl + NaOH \\rightarrow NaCl + H_2O$).\n"
            "- **Acid + Metal Carbonate**: $\\text{Salt} + H_2O + CO_2\\uparrow$ ($Ca(OH)_2 + CO_2 \\rightarrow CaCO_3\\downarrow + H_2O$ lime water turns milky).\n\n"
            "### Important Commercial Salts\n"
            "1. **Bleaching Powder ($CaOCl_2$)**: Action of chlorine on dry slaked lime ($Ca(OH)_2 + Cl_2 \\rightarrow CaOCl_2 + H_2O$). Used as disinfectant.\n"
            "2. **Baking Soda ($NaHCO_3$)**: Sodium hydrogen carbonate. Mild non-corrosive base used in antacids and baking powder with tartaric acid.\n"
            "3. **Washing Soda ($Na_2CO_3\\cdot 10H_2O$)**: Recrystallization of sodium carbonate. Used in glass, soap, paper, and removing permanent hardness of water.\n"
            "4. **Plaster of Paris ($CaSO_4\\cdot \\frac{1}{2}H_2O$)**: Prepared by heating gypsum ($CaSO_4\\cdot 2H_2O$) at 373 K. Sets hard when mixed with water.\n\n"
            "### High-Yield Board Exam Pointers\n"
            "- Always add acid slowly to water with constant stirring, never water to concentrated acid (highly exothermic).\n"
            "- Dry $HCl$ gas does not change color of dry blue litmus paper (requires moisture to produce $H^+$ ions)."
        ),
        "takeaways": [
            "pH < 7 is acidic, pH = 7 is neutral, pH > 7 is basic.",
            "Neutralization reaction: Acid + Base -> Salt + Water.",
            "Remember chemical formulas and preparations: CaOCl2, NaHCO3, Na2CO3·10H2O, CaSO4·1/2H2O.",
            "Water of crystallization gives crystalline salts their characteristic shape and color (e.g. blue CuSO4·5H2O)."
        ],
    },
    (10, "metals and non-metals"): {
        "summary": (
            "### Physical & Chemical Properties\n"
            "- **Metals**: Malleable, ductile, sonorous, good conductors of heat and electricity. Form basic oxides ($Na_2O, MgO$).\n"
            "- **Amphoteric Oxides**: React with both acids and bases to produce salt and water (e.g., $Al_2O_3, ZnO$).\n"
            "- **Non-Metals**: Brittle, non-sonorous, poor conductors (except graphite). Form acidic or neutral oxides.\n\n"
            "### Reactivity Series of Metals\n"
            "- Order of decreasing reactivity: $K > Na > Ca > Mg > Al > Zn > Fe > Pb > [H] > Cu > Hg > Ag > Au$.\n"
            "- Highly reactive metals ($K, Na$) react vigorously with cold water; $Mg$ reacts with hot water; $Al, Fe, Zn$ react with steam.\n"
            "- $Cu, Ag, Au$ do not react with water or dilute acids.\n\n"
            "### Metallurgy & Extraction of Metals\n"
            "- **Roasting**: Heating sulfide ores in excess air below melting point ($2ZnS + 3O_2 \\rightarrow 2ZnO + 2SO_2\\uparrow$).\n"
            "- **Calcination**: Heating carbonate ores in limited air ($ZnCO_3 \\rightarrow ZnO + CO_2\\uparrow$).\n"
            "- **Thermite Process**: Reduction of iron(III) oxide with aluminum: $Fe_2O_3 + 2Al \\rightarrow 2Fe + Al_2O_3 + \\text{Heat}$ (used for railway tracks).\n"
            "- **Corrosion Prevention**: Galvanization (coating zinc on iron), alloying (e.g. Brass: $Cu + Zn$, Bronze: $Cu + Sn$, Stainless Steel: $Fe + Ni + Cr$)."
        ),
        "takeaways": [
            "Reactivity series determines displacement reactions and extraction methods.",
            "Amphoteric oxides (Al2O3, ZnO) react with both acids and bases.",
            "Roasting treats sulfide ores in excess air; Calcination treats carbonate ores in limited air.",
            "Ionic compounds have high melting points and conduct electricity in molten/solution state."
        ],
    },
    (10, "carbon and its compounds"): {
        "summary": (
            "### Bonding & Nature of Carbon\n"
            "- **Covalent Bond**: Sharing of electrons between atoms. Carbon has atomic number 6 (configuration 2, 4) and is tetravalent.\n"
            "- **Versatile Nature**: Catenation (self-linking ability to form long chains) and Tetravalency enable millions of carbon compounds.\n"
            "- **Allotropes**: Diamond (rigid 3D tetrahedral structure, hardest substance), Graphite (hexagonal layers, conductor due to free electrons), Fullerenes ($C_{60}$ football-like).\n\n"
            "### Saturated vs Unsaturated Hydrocarbons\n"
            "- **Alkanes ($C_n H_{2n+2}$)**: Single covalent bonds (saturated).\n"
            "- **Alkenes ($C_n H_{2n}$)** & **Alkynes ($C_n H_{2n-2}$)**: Double / triple bonds (unsaturated; decolorize bromine water).\n"
            "- **Homologous Series**: Series of compounds with identical functional group differing by $-CH_2-$ unit ($14\\text{ u}$ mass).\n\n"
            "### Chemical Reactions of Carbon Compounds\n"
            "- **Combustion**: $\\text{Hydrocarbon} + O_2 \\rightarrow CO_2 + H_2O + \\text{Heat} + \\text{Light}$.\n"
            "- **Oxidation**: Ethanol to Ethanoic acid using alkaline $KMnO_4$ or acidified $K_2Cr_2O_7$.\n"
            "- **Esterification**: $CH_3COOH + C_2H_5OH \\xrightarrow{H_2SO_4} CH_3COOC_2H_5 + H_2O$ (sweet-smelling ester).\n"
            "- **Saponification**: Alkaline hydrolysis of esters to form soap ($CH_3COOC_2H_5 + NaOH \\rightarrow CH_3COONa + C_2H_5OH$).\n"
            "- **Soaps vs Detergents**: Soaps form insoluble scum in hard water ($Ca^{2+}, Mg^{2+}$); synthetic detergents remain effective in hard water."
        ),
        "takeaways": [
            "Carbon forms covalent bonds due to tetravalency and high catenation capability.",
            "Homologous series members share same functional group and differ by -CH2- unit.",
            "Esterification produces sweet-smelling esters; Saponification produces soaps.",
            "Soap micelles have a hydrophobic hydrocarbon tail and a hydrophilic ionic head."
        ],
    },
    (10, "life processes"): {
        "summary": (
            "### 1. Nutrition\n"
            "- **Autotrophic (Photosynthesis)**: $6CO_2 + 12H_2O \\xrightarrow{\\text{Chlorophyll, Sunlight}} C_6H_{12}O_6 + 6O_2 + 6H_2O$. Key events: Light absorption, water splitting, $CO_2$ reduction.\n"
            "- **Heterotrophic**: Holozoic (Amoeba, Humans), Saprophytic (Fungi), Parasitic (Cuscuta, tapeworm).\n"
            "- **Human Digestion**: Salivary amylase (starch $\\rightarrow$ maltose) $\\rightarrow$ Pepsin in stomach ($HCl$ provides acidic medium) $\\rightarrow$ Bile (emulsifies fats in small intestine) $\\rightarrow$ Pancreatic enzymes (Trypsin, Lipase).\n\n"
            "### 2. Respiration\n"
            "- **Breakdown of Glucose**: Glucose (6C) in cytoplasm $\\rightarrow$ Pyruvate (3C).\n"
            "  - Aerobic (in mitochondria with $O_2$): $CO_2 + H_2O + 38\\text{ ATP}$.\n"
            "  - Anaerobic (in yeast): Ethanol $+ CO_2 + 2\\text{ ATP}$.\n"
            "  - Lack of $O_2$ (in human muscle cells): Lactic acid $+ 2\\text{ ATP}$ (causes muscle cramps).\n\n"
            "### 3. Transportation\n"
            "- **Human Heart**: 4 chambers preventing mixing of oxygenated and deoxygenated blood. Double circulation: Pulmonary (Heart-Lungs) + Systemic (Heart-Body).\n"
            "- **Plants**: Xylem transports water and minerals (unidirectional via transpiration pull); Phloem translocates food/sucrose (bidirectional, requires ATP energy).\n\n"
            "### 4. Excretion\n"
            "- **Nephron**: Functional unit of kidney. Steps: Ultrafiltration in glomerulus $\\rightarrow$ Selective reabsorption (glucose, amino acids, salts, water in tubules) $\\rightarrow$ Tubular secretion $\\rightarrow$ Collecting duct."
        ),
        "takeaways": [
            "Photosynthesis converts light energy into chemical energy releasing O2.",
            "Aerobic respiration generates significantly more ATP than anaerobic pathways.",
            "Double circulation in humans ensures complete separation of oxygenated and deoxygenated blood.",
            "Nephrons filter blood, selectively reabsorb nutrients and water, and excrete urine."
        ],
    },
    (10, "light – reflection and refraction"): {
        "summary": (
            "### Reflection & Spherical Mirrors\n"
            "- **Concave Mirror**: Converging. Produces real & inverted images (except when object is between pole $P$ and focus $F$, where image is virtual, erect & magnified).\n"
            "- **Convex Mirror**: Diverging. Always forms virtual, erect, and diminished images; used as rear-view mirrors in vehicles.\n"
            "- **Mirror Formula**: $\\frac{1}{f} = \\frac{1}{v} + \\frac{1}{u}$. Magnification: $m = -\\frac{v}{u} = \\frac{h'}{h}$.\n"
            "- **Sign Convention**: Distances against incident light are negative; focal length of concave is negative, convex is positive.\n\n"
            "### Refraction & Spherical Lenses\n"
            "- **Snell's Law**: $\\frac{\\sin i}{\\sin r} = \\text{constant} = n_{21} = \\frac{v_1}{v_2}$.\n"
            "- **Absolute Refractive Index**: $n = \\frac{c}{v}$ (speed of light in vacuum / speed in medium).\n"
            "- **Lens Formula**: $\\frac{1}{f} = \\frac{1}{v} - \\frac{1}{u}$. Magnification: $m = \\frac{v}{u} = \\frac{h'}{h}$.\n"
            "- **Power of a Lens**: $P = \\frac{1}{f\\text{ (in meters)}}$. Unit: Dioptre ($D$). Convex lens has positive power; Concave lens has negative power."
        ),
        "takeaways": [
            "Mirror formula: 1/f = 1/v + 1/u; Lens formula: 1/f = 1/v - 1/u.",
            "Magnification: m = -v/u (mirrors) and m = +v/u (lenses).",
            "Convex mirrors and concave lenses always form virtual, erect, diminished images.",
            "Power of lens P = 1/f(m) in Dioptres (D)."
        ],
    },
    (10, "polynomials"): {
        "summary": (
            "### Core Concepts & Zeroes of Polynomials\n"
            "- **Zero of Polynomial**: Real number $k$ is a zero of $p(x)$ if $p(k) = 0$. Geometrically, zeroes are x-coordinates where graph $y = p(x)$ intersects the x-axis.\n"
            "- A linear polynomial has at most 1 zero, quadratic at most 2 zeroes, cubic at most 3 zeroes.\n\n"
            "### Relationship between Zeroes and Coefficients (Quadratic: $ax^2 + bx + c$)\n"
            "- **Sum of Zeroes**: $\\alpha + \\beta = -\\frac{b}{a} = -\\frac{\\text{coefficient of } x}{\\text{coefficient of } x^2}$.\n"
            "- **Product of Zeroes**: $\\alpha \\cdot \\beta = \\frac{c}{a} = \\frac{\\text{constant term}}{\\text{coefficient of } x^2}$.\n"
            "- **Forming Quadratic Polynomial**: $p(x) = k [x^2 - (\\alpha + \\beta)x + \\alpha\\beta]$, where $k \\neq 0$ is any real constant.\n\n"
            "### High-Yield Exam Tips\n"
            "- To find zeroes, set $p(x) = 0$ and factorize using splitting the middle term.\n"
            "- Symmetric identities: $\\alpha^2 + \\beta^2 = (\\alpha + \\beta)^2 - 2\\alpha\\beta$ and $\\frac{1}{\\alpha} + \\frac{1}{\\beta} = \\frac{\\alpha + \\beta}{\\alpha\\beta}$."
        ),
        "takeaways": [
            "Sum of zeroes α + β = -b/a; Product of zeroes αβ = c/a.",
            "Quadratic polynomial with given zeroes: k[x^2 - (Sum)x + Product].",
            "Number of zeroes equals number of points where graph crosses x-axis."
        ],
    },
    (10, "quadratic equations"): {
        "summary": (
            "### Standard Form & Solution Methods\n"
            "- **Standard Form**: $ax^2 + bx + c = 0$, where $a, b, c \\in \\mathbb{R}$ and $a \\neq 0$.\n"
            "- **Methods of Solution**:\n"
            "  1. Factorization (Splitting the middle term).\n"
            "  2. Quadratic Formula: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$.\n\n"
            "### Nature of Roots & Discriminant ($D = b^2 - 4ac$)\n"
            "- If $D > 0$: Two distinct real roots ($x = \\frac{-b + \\sqrt{D}}{2a}, \\frac{-b - \\sqrt{D}}{2a}$).\n"
            "- If $D = 0$: Two equal (coincident) real roots ($x = -\\frac{b}{2a}$).\n"
            "- If $D < 0$: No real roots.\n\n"
            "### NCERT High-Yield Problem Types\n"
            "- Word problems on speed-distance-time, upstream/downstream, tap/pipe work, and age relations.\n"
            "- Finding unknown $k$ when equation has equal real roots: Set $D = b^2 - 4ac = 0$ and solve for $k$."
        ),
        "takeaways": [
            "Quadratic formula: x = (-b ± √D) / (2a) where D = b^2 - 4ac.",
            "For equal real roots, set Discriminant D = 0.",
            "Always check that solutions to word problems are positive and physically meaningful."
        ],
    },
    (10, "arithmetic progressions"): {
        "summary": (
            "### Definition & Fundamentals\n"
            "- **Arithmetic Progression (AP)**: Sequence of numbers in which each term is obtained by adding a fixed number $d$ (common difference) to the preceding term ($a_k - a_{k-1} = d$).\n"
            "- General form: $a, a + d, a + 2d, a + 3d, \\dots$\n\n"
            "### Core Formulas\n"
            "- **$n$-th Term ($a_n$)**: $a_n = a + (n - 1)d$.\n"
            "- **$n$-th Term from the End**: $a_n(\\text{end}) = l - (n - 1)d$, where $l$ is the last term.\n"
            "- **Sum of First $n$ Terms ($S_n$)**:\n"
            "  - $S_n = \\frac{n}{2} [2a + (n - 1)d]$\n"
            "  - $S_n = \\frac{n}{2} [a + l]$ (when first and last term are known)\n"
            "- **Relation between $a_n$ and $S_n$**: $a_n = S_n - S_{n-1}$.\n\n"
            "### Standard Problem Patterns\n"
            "- 3 terms in AP: Let them be $a - d, a, a + d$.\n"
            "- Sum of first $n$ natural numbers: $S_n = \\frac{n(n + 1)}{2}$."
        ),
        "takeaways": [
            "n-th term: an = a + (n - 1)d.",
            "Sum of n terms: Sn = n/2 [2a + (n - 1)d] = n/2 [a + l].",
            "an = Sn - S(n-1) links nth term directly with partial sums."
        ],
    },
    (10, "introduction to trigonometry"): {
        "summary": (
            "### Trigonometric Ratios (in a Right Triangle)\n"
            "- $\\sin\\theta = \\frac{\\text{Perpendicular}}{\\text{Hypotenuse}}$, $\\cos\\theta = \\frac{\\text{Base}}{\\text{Hypotenuse}}$, $\\tan\\theta = \\frac{\\text{Perpendicular}}{\\text{Base}} = \\frac{\\sin\\theta}{\\cos\\theta}$.\n"
            "- Reciprocals: $\\csc\\theta = \\frac{1}{\\sin\\theta}$, $\\sec\\theta = \\frac{1}{\\cos\\theta}$, $\\cot\\theta = \\frac{1}{\\tan\\theta}$.\n\n"
            "### Standard Specific Angle Values\n"
            "- $\\sin(0^\\circ, 30^\\circ, 45^\\circ, 60^\\circ, 90^\\circ) = (0, \\frac{1}{2}, \\frac{1}{\\sqrt{2}}, \\frac{\\sqrt{3}}{2}, 1)$.\n"
            "- $\\cos(0^\\circ, 30^\\circ, 45^\\circ, 60^\\circ, 90^\\circ) = (1, \\frac{\\sqrt{3}}{2}, \\frac{1}{\\sqrt{2}}, \\frac{1}{2}, 0)$.\n"
            "- $\\tan(0^\\circ, 30^\\circ, 45^\\circ, 60^\\circ, 90^\\circ) = (0, \\frac{1}{\\sqrt{3}}, 1, \\sqrt{3}, \\text{not defined})$.\n\n"
            "### Fundamental Trigonometric Identities\n"
            "1. $\\sin^2\\theta + \\cos^2\\theta = 1$\n"
            "2. $1 + \\tan^2\\theta = \\sec^2\\theta$\n"
            "3. $1 + \\cot^2\\theta = \\csc^2\\theta$\n\n"
            "### Exam Proving Strategies\n"
            "- Convert all terms into $\\sin\\theta$ and $\\cos\\theta$ if other simplifications are not obvious.\n"
            "- Multiply numerator and denominator by conjugate when dealing with square roots or $1 \\pm \\sin\\theta, 1 \\pm \\cos\\theta$."
        ),
        "takeaways": [
            "Core identity: sin^2(θ) + cos^2(θ) = 1.",
            "sec^2(θ) - tan^2(θ) = 1 and csc^2(θ) - cot^2(θ) = 1.",
            "Memorize the standard ratio table for 0°, 30°, 45°, 60°, 90°.",
            "Converting complex expressions into sin and cos simplifies proof questions."
        ],
    },
}


def generate_notes_for_chapter(
    grade: int, subject: str, chapter: str
) -> tuple[str, list[str]]:
    key = (grade, chapter.strip().lower())
    if key in KNOWN_CHAPTER_NOTES:
        item = KNOWN_CHAPTER_NOTES[key]
        return item["summary"], item["takeaways"]

    sub_lower = subject.lower()
    if "math" in sub_lower:
        summary = (
            f"### Class {grade} Mathematics — {chapter}\n\n"
            f"#### 1. Core Mathematical Concept\n"
            f"- **Chapter Focus**: Fundamental algebraic, geometric, and numerical principles of **{chapter}**.\n"
            f"- **Axioms & Foundations**: Master the foundational definitions, formulas, and conditions for solutions according to the NCERT curriculum.\n\n"
            f"#### 2. Key Formulas, Theorems & Methods\n"
            f"- Apply standard properties and identity expansions relevant to *{chapter}*.\n"
            f"- Maintain clean step-by-step calculations with proper units and sign conventions.\n"
            f"- Double check boundary conditions, non-zero denominator constraints, and geometric figures.\n\n"
            f"#### 3. Board & School Exam Strategies\n"
            f"- Practice standard NCERT examples and in-text exercise problems before attempting advanced question banks.\n"
            f"- State all theorems, formulas, and assumptions explicitly for step-marking.\n"
            f"- Check final answers with reverse substitution or sanity checks."
        )
        takeaways = [
            f"Memorize all core formulas and theorems in {chapter}.",
            "Show every working step clearly to maximize step-marking in exams.",
            "Solve NCERT exemplar and exercise questions thoroughly.",
        ]
    elif any(k in sub_lower for k in ["physics", "science", "chemistry", "biology"]):
        summary = (
            f"### Class {grade} {subject} — {chapter}\n\n"
            f"#### 1. Scientific Overview & Phenomena\n"
            f"- **Core Theme**: Fundamental principles, natural laws, and experimental observations in **{chapter}**.\n"
            f"- **Mechanism & Process**: Understand the underlying cause-and-effect relationships and scientific theories outlined in NCERT.\n\n"
            f"#### 2. Essential Definitions, Laws & Equations\n"
            f"- Formulate precise scientific definitions and state governing physical/chemical laws.\n"
            f"- For numerical problems: state given values, SI units, standard formulas, and final answers with units.\n"
            f"- For biology/anatomy: practice neat, labeled diagrams with directional flow arrows.\n\n"
            f"#### 3. High-Yield Exam Takeaways\n"
            f"- Review NCERT summary bullet points and highlighted margin boxes.\n"
            f"- Focus on conceptual reasoning questions (Assertion-Reason and Case-Based studies).\n"
            f"- Learn common experimental setups, observations, and conclusion reasoning."
        )
        takeaways = [
            f"Learn textbook definitions, physical laws, and equations for {chapter}.",
            "Practice neat labeled diagrams and SI units for numericals.",
            "Review NCERT reasoning and case-study questions.",
        ]
    elif any(
        k in sub_lower
        for k in ["social", "history", "geography", "civics", "political", "economics"]
    ):
        summary = (
            f"### Class {grade} {subject} — {chapter}\n\n"
            f"#### 1. Historical & Socio-Economic Context\n"
            f"- **Central Theme**: Key events, geographical patterns, and civic structures explored in **{chapter}**.\n"
            f"- **Timeline & Causality**: Connect major historical transitions, geographical causes, and democratic institutions.\n\n"
            f"#### 2. Critical Terms & Key Concepts\n"
            f"- Memorize vital terminology, constitutional articles, and geographical classifications.\n"
            f"- Analyze causes, consequences, and global/national impacts of core events.\n\n"
            f"#### 3. Exam Answer Writing Strategy\n"
            f"- Write structured answers with clear sub-headings and bullet points.\n"
            f"- Mention relevant years, acts, treaties, and geographic map locations where applicable."
        )
        takeaways = [
            f"Memorize key dates, terminology, and definitions in {chapter}.",
            "Structure subjective answers with bullet points and clear headings.",
            "Practice map work and timeline associations.",
        ]
    elif "environmental" in sub_lower or grade <= 5:
        summary = (
            f"### Class {grade} {subject} — {chapter}\n\n"
            f"#### 1. Nature & Real-Life Concepts\n"
            f"- Discover everyday surroundings, plant and animal habitats, and community life in **{chapter}**.\n"
            f"- Understand how our environment functions and why nature conservation matters.\n\n"
            f"#### 2. Everyday Observations & Activities\n"
            f"- Connect textbook lessons to hands-on activities, seasons, health, and family life.\n"
            f"- Identify practical safety habits and environmental care tips.\n\n"
            f"#### 3. Learning Takeaways\n"
            f"- Be observant and curious about natural surroundings and local community."
        )
        takeaways = [
            f"Observe real-world examples related to {chapter}.",
            "Learn core terms, habits, and environmental principles.",
            "Practice answering simple observation and activity questions.",
        ]
    else:
        summary = (
            f"### Class {grade} {subject} — {chapter}\n\n"
            f"#### 1. Chapter Overview & Core Concepts\n"
            f"- Master the fundamental concepts of **{chapter}** aligned with the NCERT curriculum.\n"
            f"- Understand themes, characters, literary devices, and core messages.\n\n"
            f"#### 2. Key Terms & Insights\n"
            f"- Highlight significant vocabulary, rules, and chapter expressions.\n"
            f"- Relate chapter themes to practical usage and textual comprehension.\n\n"
            f"#### 3. NCERT Practice Tips\n"
            f"- Review textbook questions, grammar rules, and summary points thoroughly."
        )
        takeaways = [
            f"Understand central ideas and core concepts of {chapter}.",
            "Review NCERT questions and summary exercises.",
            "Practice writing concise, coherent answers.",
        ]
    return summary, takeaways


def get_chapter_resource(
    grade: int, subject: str, chapter: str, language: str = "en"
) -> dict[str, Any]:
    lang = "hi" if language in ("hi", "hindi") else "en"
    eng_sub = normalize_subject_to_english(subject)
    eng_ch = normalize_chapter_to_english(chapter)

    if lang == "hi":
        display_sub = get_hindi_subject_name(eng_sub)
        display_ch = get_hindi_chapter_name(eng_ch)
        summary, takeaways = generate_hindi_notes_for_chapter(grade, eng_sub, eng_ch)
        video_query = f"CBSE कक्षा {grade} {display_sub} {display_ch} animated explanation in hindi"
        diksha_query = f"कक्षा {grade} {display_sub} {display_ch}"
        khan_query = f"कक्षा {grade} {display_sub} {display_ch}"
    else:
        display_sub = eng_sub
        display_ch = eng_ch
        summary, takeaways = generate_notes_for_chapter(grade, eng_sub, eng_ch)
        video_query = f"CBSE Class {grade} {eng_sub} {eng_ch} animated concept explanation"
        diksha_query = f"Class {grade} {eng_sub} {eng_ch}"
        khan_query = f"Class {grade} {eng_sub} {eng_ch}"

    return {
        "class_grade": grade,
        "subject": display_sub,
        "chapter": display_ch,
        "language": lang,
        "summary_notes": summary,
        "key_takeaways": takeaways,
        "animation_video_url": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(video_query)}",
        "diksha_video_url": f"https://diksha.gov.in/explore?query={urllib.parse.quote_plus(diksha_query)}",
        "khan_academy_url": f"https://www.khanacademy.org/search?page_search_query={urllib.parse.quote_plus(khan_query)}",
        "ncert_book_url": "https://ncert.nic.in/textbook.php",
        "english_chapter": eng_ch,
        "english_subject": eng_sub,
    }


def get_chapter_resources_for_subject(
    grade: int, subject: str = "", chapter: str = "", language: str = "en"
) -> list[dict[str, Any]]:
    target_grade = grade if 1 <= grade <= 12 else 10
    grade_data = NCERT_CURRICULUM.get(target_grade, {})
    if not grade_data:
        return []

    norm_subject = normalize_subject_to_english(subject) if subject else ""
    norm_chapter = normalize_chapter_to_english(chapter) if chapter else ""

    matched_subjects: list[tuple[str, list[str]]] = []
    if norm_subject:
        for sub_name, ch_list in grade_data.items():
            if sub_name.lower() == norm_subject.lower():
                matched_subjects.append((sub_name, ch_list))
                break
    if not matched_subjects:
        if norm_subject:
            for sub_name, ch_list in grade_data.items():
                if norm_subject.lower() in sub_name.lower():
                    matched_subjects.append((sub_name, ch_list))
        if not matched_subjects:
            matched_subjects = list(grade_data.items())

    results: list[dict[str, Any]] = []
    ch_filter_eng = norm_chapter.strip().lower()
    ch_filter_raw = chapter.strip().lower()

    for sub_name, ch_list in matched_subjects:
        for ch in ch_list:
            hi_ch = get_hindi_chapter_name(ch).lower()
            ch_lower = ch.lower()
            if ch_filter_eng and (ch_filter_eng not in ch_lower and ch_filter_raw not in hi_ch):
                continue
            results.append(
                get_chapter_resource(target_grade, sub_name, ch, language=language)
            )

    return results



