"""
ai/disease_knowledge.py — Agronomic disease intelligence database.

Contains rich botanical data, pathogen classification, visual symptoms,
chemical/organic treatments, dosage recommendations, and environmental risk factors.
Fully offline — zero network calls.
"""

DISEASE_KNOWLEDGE_BASE = {
    # ── Corn ─────────────────────────────────────────────────────────────────
    ("Corn", "Common Rust"): {
        "pathogen": "Fungus (Puccinia sorghi)",
        "pathogen_type": "Fungal",
        "severity": "MEDIUM",
        "health_score": 58,
        "symptoms": [
            "Golden-brown to cinnamon-brown powdery pustules (uredinia) on upper and lower leaf surfaces",
            "Pustules rupture epidermal tissue releasing powdery spores",
            "Severe infection leads to chlorosis and premature leaf death"
        ],
        "immediate_action": "Inspect field distribution; prune heavily rusted lower leaves to minimize spore dispersion.",
        "chemical_treatment": {
            "fungicide": "Azoxystrobin + Difenoconazole or Pyraclostrobin",
            "dosage": "1.0 - 1.5 ml/L of water",
            "interval": "Apply at first sign of pustules; repeat after 14 days if wet weather persists."
        },
        "organic_treatment": {
            "remedy": "Foliar spray of Neem Seed Kernel Extract (NSKE 5%) or Trichoderma harzianum",
            "dosage": "50 ml/L of water (NSKE) or 5g/L (Trichoderma)",
            "notes": "Best applied preventatively in early morning."
        },
        "prevention": [
            "Plant rust-resistant hybrid seed varieties",
            "Ensure early season planting to avoid peak spore migration",
            "Destroy volunteer corn plants and crop debris after harvest"
        ],
        "environmental_risk": "Fosters rapidly in high relative humidity (>85%) with moderate temperatures (16–25°C)."
    },

    ("Corn", "Gray Leaf Spot"): {
        "pathogen": "Fungus (Cercospora zeae-maydis)",
        "pathogen_type": "Fungal",
        "severity": "HIGH",
        "health_score": 42,
        "symptoms": [
            "Rectangular, pale brown to gray lesions bounded sharply by leaf veins",
            "Lesions expand to 1–5 cm in length, merging to cause extensive leaf blighting",
            "Loss of photosynthetic green leaf area leading to stalk lodging"
        ],
        "immediate_action": "Avoid overhead sprinkler irrigation during late afternoon; increase field drainage.",
        "chemical_treatment": {
            "fungicide": "Propiconazole 25% EC or Fluxapyroxad + Pyraclostrobin",
            "dosage": "1.0 ml/L of water",
            "interval": "Apply at tassel emergence (VT) if lower 3 leaves show lesions."
        },
        "organic_treatment": {
            "remedy": "Bacillus amyloliquefaciens microbial bio-fungicide or Copper Hydroxide",
            "dosage": "2.5 g/L of water",
            "notes": "Suppresses fungal hyphae expansion on leaf surfaces."
        },
        "prevention": [
            "Minimum 2-year crop rotation with non-grass crops (Soybean, Cotton)",
            "Till surface crop residues where permissible to speed up residue decomposition",
            "Balanced nitrogen fertilization (avoid excessive N that causes lush foliage)"
        ],
        "environmental_risk": "Prolonged leaf wetness (>12 hours) and warm, humid overcast weather (25–30°C)."
    },

    # ── Potato ───────────────────────────────────────────────────────────────
    ("Potato", "Early Blight"): {
        "pathogen": "Fungus (Alternaria solani)",
        "pathogen_type": "Fungal",
        "severity": "MEDIUM",
        "health_score": 52,
        "symptoms": [
            "Dark brown to black concentric ring lesions ('target board' / bullseye appearance)",
            "Narrow chlorotic yellow halos surrounding mature necrotic spots",
            "Older lower leaves infected first, moving upward through canopy"
        ],
        "immediate_action": "Remove and safely burn or bury heavily blighted lower foliage.",
        "chemical_treatment": {
            "fungicide": "Mancozeb 75% WP or Chlorothalonil 75% WP",
            "dosage": "2.0 - 2.5 g/L of water",
            "interval": "Spray every 7–10 days during periods of alternating wet and dry weather."
        },
        "organic_treatment": {
            "remedy": "Bordeaux Mixture (1%) or Copper Oxychloride 50% WP",
            "dosage": "3 g/L of water",
            "notes": "Protects healthy foliage from germinating airborne conidia."
        },
        "prevention": [
            "Use certified disease-free seed tubers",
            "Implement drip irrigation to keep potato foliage dry",
            "Maintain adequate soil potassium and nitrogen fertility"
        ],
        "environmental_risk": "Alternating cycles of high humidity / rain followed by dry sunny periods with 24–29°C."
    },

    ("Potato", "Late Blight"): {
        "pathogen": "Oomycete (Phytophthora infestans)",
        "pathogen_type": "Oomycete",
        "severity": "CRITICAL",
        "health_score": 25,
        "symptoms": [
            "Rapidly expanding water-soaked dark green to purplish-black lesions",
            "White fungal-like downy sporulation on undersides of leaves during humid mornings",
            "Foul decaying odor and complete foliar collapse within 4–7 days if untreated"
        ],
        "immediate_action": "URGENT: Immediately halt all sprinkler irrigation; alert neighboring farms.",
        "chemical_treatment": {
            "fungicide": "Metalaxyl-M + Mancozeb (Ridomil Gold) or Cymoxanil 8% + Mancozeb 64%",
            "dosage": "2.5 g/L of water (thorough canopy coverage)",
            "interval": "Apply immediately upon detection. Repeat in 5–7 days."
        },
        "organic_treatment": {
            "remedy": "Liquid Copper Octanoate or Potassium Bicarbonate + Horticultural Oil",
            "dosage": "5 ml/L of water",
            "notes": "Preventative only; late-stage late blight requires systemic intervention."
        },
        "prevention": [
            "Hill up soil around potato hills to prevent tuber spore contamination",
            "Destroy all volunteer potato cull piles before planting",
            "Plant blight-resistant cultivars (e.g., Kufri Girdhari, Defender)"
        ],
        "environmental_risk": "Cool, very wet weather (10–20°C) with prolonged relative humidity (>90%)."
    },

    # ── Rice ─────────────────────────────────────────────────────────────────
    ("Rice", "Brown Spot"): {
        "pathogen": "Fungus (Bipolaris oryzae / Cochliobolus miyabeanus)",
        "pathogen_type": "Fungal",
        "severity": "HIGH",
        "health_score": 48,
        "symptoms": [
            "Oval to circular brown spots with grayish-white necrotic centers and yellow halos",
            "Lesions develop on coleoptile, leaves, leaf sheaths, and glumes",
            "In severe cases, grain filling is hampered resulting in discolored chaffy grains"
        ],
        "immediate_action": "Top-dress field with Potassium (MOP) and slow-release Nitrogen.",
        "chemical_treatment": {
            "fungicide": "Hexaconazole 5% SC or Tricyclazole 75% WP",
            "dosage": "2.0 ml/L or 0.6 g/L of water",
            "interval": "Apply at tillering and boot leaf emergence."
        },
        "organic_treatment": {
            "remedy": "Pseudomonas fluorescens bio-agent seed treatment & foliar spray",
            "dosage": "10 g/kg seed; 2.5 g/L for foliar application",
            "notes": "Induces systemic acquired resistance in paddy tillers."
        },
        "prevention": [
            "Avoid nutritional stress — correct soil zinc, potassium, and silicon deficiencies",
            "Hot water seed treatment at 52–54°C for 10 minutes",
            "Maintain proper field water standing (2–5 cm) during critical growth stages"
        ],
        "environmental_risk": "Nutrient-depleted soils combined with high humidity (86–100%) and 25–30°C."
    },

    ("Rice", "Leaf Blast"): {
        "pathogen": "Fungus (Magnaporthe oryzae / Pyricularia oryzae)",
        "pathogen_type": "Fungal",
        "severity": "CRITICAL",
        "health_score": 30,
        "symptoms": [
            "Spindle/diamond-shaped lesions with grayish centers and dark brown borders",
            "Lesions coalesce rapidly causing complete drying and burning of leaves ('blast' look)",
            "Collar rot and neck blast causing panicles to fall over"
        ],
        "immediate_action": "Drain standing water if stagnant, apply fresh clean irrigation, avoid nitrogen top-dressing.",
        "chemical_treatment": {
            "fungicide": "Tricyclazole 75% WP or Isoprothiolane 40% EC or Kasugamycin 3% SL",
            "dosage": "0.6 g/L (Tricyclazole) or 1.5 ml/L (Isoprothiolane)",
            "interval": "Spray at first observation; repeat at early heading stage."
        },
        "organic_treatment": {
            "remedy": "Spray Panchagavya (3%) or Pseudomonas fluorescens + Bacillus subtilis",
            "dosage": "30 ml/L (Panchagavya) or 5 g/L (Bio-agents)",
            "notes": "Boosts plant phytoalexins against blast appressoria."
        },
        "prevention": [
            "Avoid split applications of excessive nitrogen fertilizer",
            "Seed treatment with bio-fungicides or certified fungicides",
            "Maintain continuous shallow flooding (avoid drought stress)"
        ],
        "environmental_risk": "Extended dew periods (>10 hrs), cloudy overcast skies, high humidity (>90%) with 20–26°C."
    },

    ("Rice", "Bacterial Blight Disease"): {
        "pathogen": "Bacterium (Xanthomonas oryzae pv. oryzae)",
        "pathogen_type": "Bacterial",
        "severity": "HIGH",
        "health_score": 40,
        "symptoms": [
            "Water-soaked to yellowish-green wavy stripes starting at leaf tips and margins",
            "Milky bacterial ooze drops visible on young lesions in early morning",
            "Leaves turn grayish-white and roll up ('kresek' seedling wilt phase)"
        ],
        "immediate_action": "Drain field water temporarily; halt nitrogen fertilization immediately.",
        "chemical_treatment": {
            "fungicide": "Streptocycline (90% Streptomycin + 10% Tetracycline) + Copper Oxychloride",
            "dosage": "0.1 g/L Streptocycline + 2.0 g/L Copper Oxychloride",
            "interval": "Spray twice at 10-day intervals."
        },
        "organic_treatment": {
            "remedy": "Cow dung filtrate spray (20%) or Fresh Neem cake extract",
            "dosage": "200 g/L soaked and filtered",
            "notes": "Suppresses bacterial multiplication on phylloplane."
        },
        "prevention": [
            "Grow BB-resistant rice varieties (e.g., Improved Samba Mahsuri, Swarna-Sub1)",
            "Clean farm bunds and eradicate weed hosts like Leersia oryzoides",
            "Avoid leaf clipping during seedling transplantation"
        ],
        "environmental_risk": "Strong winds, typhoon rains, flooding, and temperatures between 25–34°C."
    },

    ("Rice", "Blast Disease"): {
        "pathogen": "Fungus (Magnaporthe oryzae)",
        "pathogen_type": "Fungal",
        "severity": "CRITICAL",
        "health_score": 32,
        "symptoms": [
            "Elliptical diamond-shaped leaf lesions with point tips",
            "Node and panicle neck blackening resulting in blank/empty whiteheads"
        ],
        "immediate_action": "Apply systemic anti-blast fungicide and suspend nitrogenous fertilizers.",
        "chemical_treatment": {
            "fungicide": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC",
            "dosage": "1.0 ml/L of water",
            "interval": "Spray at tillering and boot leaf emergence."
        },
        "organic_treatment": {
            "remedy": "Silicon soil amendment (Potassium Silicate) + Trichoderma foliar spray",
            "dosage": "2.5 ml/L Potassium silicate",
            "notes": "Silicon deposits in epidermal cells form a physical barrier against hyphal entry."
        },
        "prevention": [
            "Use blast-resistant seeds",
            "Avoid dense seeding and overcrowded nurseries"
        ],
        "environmental_risk": "High night humidity (>93%), cool nights (18–22°C), and overcast rainy days."
    },

    ("Rice", "brown Spot Disease"): {
        "pathogen": "Fungus (Bipolaris oryzae)",
        "pathogen_type": "Fungal",
        "severity": "HIGH",
        "health_score": 45,
        "symptoms": [
            "Numerous uniform sesame-seed shaped brown spots covering leaves",
            "Yellow halo surrounding brown necrotic spots"
        ],
        "immediate_action": "Apply balanced micronutrient foliar spray (Zinc + Potassium).",
        "chemical_treatment": {
            "fungicide": "Carbendazim 12% + Mancozeb 63% WP (Saaf)",
            "dosage": "2.0 g/L of water",
            "interval": "Apply at 12–15 day intervals."
        },
        "organic_treatment": {
            "remedy": "Neem oil 10,000 ppm + Bio-fertilizer foliar spray",
            "dosage": "3 ml/L of water",
            "notes": "Reduces spore germination."
        },
        "prevention": [
            "Soil testing to balance NPK and apply Farmyard Manure (FYM)",
            "Proper water management without drying out roots"
        ],
        "environmental_risk": "Drought stress or nutrient-poor sandy soils with 27–30°C."
    },

    ("Rice", "False Smut Disease"): {
        "pathogen": "Fungus (Ustilaginoidea virens)",
        "pathogen_type": "Fungal",
        "severity": "HIGH",
        "health_score": 46,
        "symptoms": [
            "Individual rice grains transformed into large yellowish-green velvety smut balls",
            "Smut balls turn dark olive green to black powdery spore masses",
            "Reduced grain milling quality and mycotoxin contamination"
        ],
        "immediate_action": "Manually collect and incinerate smutted panicles in a plastic bag to prevent field dispersal.",
        "chemical_treatment": {
            "fungicide": "Propiconazole 25% EC or Copper Hydroxide 53.8% DF",
            "dosage": "1.0 ml/L or 2.0 g/L of water",
            "interval": "Crucial timing: spray at booting stage (5–7 days before panicle emergence)."
        },
        "organic_treatment": {
            "remedy": "Foliar application of Trichoderma viride culture broth",
            "dosage": "10 ml/L of water",
            "notes": "Competes with Ustilaginoidea in the floral cavity."
        },
        "prevention": [
            "Avoid late sowing and excessive late nitrogen application",
            "Thorough plowing after harvest to bury sclerotia"
        ],
        "environmental_risk": "High relative humidity (>90%), continuous rain during flowering stage, and 25–35°C."
    },

    # ── Sugarcane ────────────────────────────────────────────────────────────
    ("Sugarcane", "Bacterial Blight"): {
        "pathogen": "Bacterium (Acidovorax avenae subsp. avenae)",
        "pathogen_type": "Bacterial",
        "severity": "MEDIUM",
        "health_score": 55,
        "symptoms": [
            "Long, narrow red to dark brown stripes along leaf veins",
            "Shredding of leaf tips in advanced stages",
            "Stunted spindle and reduced cane stalk elongation"
        ],
        "immediate_action": "Disinfect cutting knives with 10% bleach before setts cutting.",
        "chemical_treatment": {
            "fungicide": "Copper Oxychloride 50% WP + Streptomycin Sulphate",
            "dosage": "2.5 g/L + 0.1 g/L of water",
            "interval": "Spray twice at 15-day intervals."
        },
        "organic_treatment": {
            "remedy": "Hot water sett treatment (50°C for 2 hours) prior to planting",
            "dosage": "Heat thermal soak",
            "notes": "Eradicates vascular bacterial colonies."
        },
        "prevention": [
            "Plant healthy disease-free setts",
            "Ensure proper field drainage to avoid waterlogging"
        ],
        "environmental_risk": "Heavy monsoon rains and water stagnation with 28–32°C."
    },

    ("Sugarcane", "Red Rot"): {
        "pathogen": "Fungus (Colletotrichum falcatum)",
        "pathogen_type": "Fungal",
        "severity": "CRITICAL",
        "health_score": 20,
        "symptoms": [
            "Third or fourth leaf from top shows yellowing and drying along margins",
            "Splitting the cane stalk reveals internal red tissue with distinctive white cross bands",
            "Alcoholic sour odor from rotting internal cane pith"
        ],
        "immediate_action": "URGENT: Uproot and burn entire affected sugarcane stool; treat soil with bleaching powder.",
        "chemical_treatment": {
            "fungicide": "Thiophanate Methyl 70% WP or Carbendazim 50% WP (Sett soak & Drench)",
            "dosage": "2.0 g/L of water",
            "interval": "Drench soil around affected clumps immediately."
        },
        "organic_treatment": {
            "remedy": "Soil application of Trichoderma viride enriched Farmyard Manure",
            "dosage": "5 kg Trichoderma mixed with 500 kg FYM per acre",
            "notes": "Creates a bio-shield against soil-borne fungal hyphae."
        },
        "prevention": [
            "Strict sett selection: never use setts from red-rot infected fields",
            "Grow red-rot resistant varieties (e.g., Co 0238, Co 86032)",
            "Crop rotation with paddy or green manure crops (Dhaincha) for 2 seasons"
        ],
        "environmental_risk": "Waterlogged fields, ill-drained alkaline soils, and temperatures between 28–32°C."
    },

    # ── Wheat ────────────────────────────────────────────────────────────────
    ("Wheat", "Brown Rust"): {
        "pathogen": "Fungus (Puccinia triticina)",
        "pathogen_type": "Fungal",
        "severity": "HIGH",
        "health_score": 44,
        "symptoms": [
            "Small, circular to oval bright orange-brown uredinial pustules scattered on leaf blades",
            "Pustules do not form distinct stripes, scattered randomly on upper leaf surface",
            "Leaves turn chlorotic and wither prematurely, shriveling grain yield"
        ],
        "immediate_action": "Inspect wheat canopy density; apply systemic triazole spray at first pustule sighting.",
        "chemical_treatment": {
            "fungicide": "Propiconazole 25% EC (Tilt) or Tebuconazole 25.9% EC",
            "dosage": "1.0 ml/L of water (500 ml/ha)",
            "interval": "Single spray at flag leaf emergence usually gives full protection."
        },
        "organic_treatment": {
            "remedy": "Foliar spray of Sour Buttermilk (Lassi 5%) + Neem oil",
            "dosage": "50 ml buttermilk + 3 ml neem oil per litre",
            "notes": "Lactic acid creates an unfavorable pH on the leaf surface."
        },
        "prevention": [
            "Cultivate rust-resistant wheat varieties (e.g., HD 2967, DBW 187, PBW 550)",
            "Adhere to recommended sowing window (avoid late November/December sowing)",
            "Avoid excessive nitrogen fertilization"
        ],
        "environmental_risk": "Moderate temperatures (15–25°C) with night dew or rain and high humidity."
    },

    ("Wheat", "Yellow Rust"): {
        "pathogen": "Fungus (Puccinia striiformis)",
        "pathogen_type": "Fungal",
        "severity": "CRITICAL",
        "health_score": 35,
        "symptoms": [
            "Distinct bright yellow-orange pustules arranged in linear stripes along leaf veins",
            "Yellow powdery dust rubs off easily on fingers or cloth",
            "Severe infection leads to complete leaf scorching and severe grain shrinkage"
        ],
        "immediate_action": "Community alert: yellow rust spores travel fast across borders; spray immediately.",
        "chemical_treatment": {
            "fungicide": "Propiconazole 25% EC or Triadimefon 25% WP",
            "dosage": "1.0 ml/L or 1.0 g/L of water",
            "interval": "Spray promptly; second spray after 15 days if yellow stripes reappear."
        },
        "organic_treatment": {
            "remedy": "Sulfur 80% WDG (Wettable Sulfur) foliar dusting/spray",
            "dosage": "3.0 g/L of water",
            "notes": "Traditional safe protective fungicide."
        },
        "prevention": [
            "Plant stripe-rust resistant cultivars with multiple Yr resistance genes",
            "Early morning field scouting in cooler northern agricultural belts",
            "Eradicate weed grasses (Barley grass, Bromus) around field edges"
        ],
        "environmental_risk": "Cool, humid weather (10–15°C) with persistent winter morning fogs."
    },

    # ── Tomato & General Fallbacks ──────────────────────────────────────────
    ("Tomato", "Early Blight"): {
        "pathogen": "Fungus (Alternaria solani)",
        "pathogen_type": "Fungal",
        "severity": "MEDIUM",
        "health_score": 50,
        "symptoms": [
            "Target-like dark brown concentric ring lesions on older leaves",
            "Yellow halo surrounding necrotic lesions",
            "Stem collar rot in young seedlings"
        ],
        "immediate_action": "Stake tomato vines off ground; prune bottom 30cm of foliage.",
        "chemical_treatment": {
            "fungicide": "Azoxystrobin 23% SC or Mancozeb 75% WP",
            "dosage": "1.0 ml/L or 2.0 g/L of water",
            "interval": "Every 7–10 days in wet conditions."
        },
        "organic_treatment": {
            "remedy": "Copper soap spray or Bacillus subtilis bio-fungicide",
            "dosage": "3 ml/L of water",
            "notes": "Covers leaf cuticle to block spore tubes."
        },
        "prevention": [
            "Mulch soil around plants to prevent rain-splash from soil to lower leaves",
            "Drip irrigation only — keep foliage dry",
            "3-year crop rotation avoiding Solanaceae family"
        ],
        "environmental_risk": "Warm temperatures (24–29°C) with intermittent rain and dew."
    }
}

# Healthy fallback template
HEALTHY_PROFILE = {
    "pathogen": "None (Plant is Vigorous & Healthy)",
    "pathogen_type": "None",
    "severity": "OPTIMAL",
    "health_score": 98,
    "symptoms": [
        "Vibrant uniform green foliage with no chlorotic spots or necrotic lesions",
        "Intact leaf margins and healthy turgor pressure",
        "Normal photosynthetic activity and balanced vegetative growth"
    ],
    "immediate_action": "Continue regular nutrient and water management as scheduled.",
    "chemical_treatment": {
        "fungicide": "Not Required",
        "dosage": "None",
        "interval": "N/A"
    },
    "organic_treatment": {
        "remedy": "Maintain prophylactic compost tea or seaweed extract foliar tonic",
        "dosage": "5 ml/L monthly for enhanced vitality",
        "notes": "Promotes beneficial phyllosphere microbiota."
    },
    "prevention": [
        "Maintain balanced drip irrigation without waterlogging",
        "Monitor soil moisture between 40%–70%",
        "Regular field scouting for early pest/disease detection"
    ],
    "environmental_risk": "Current crop state is robust and resilient against ambient pathogens."
}


def get_disease_dossier(crop: str, disease: str, confidence: float = 0.90) -> dict:
    """
    Retrieve comprehensive agronomic information for a given (crop, disease) pair.
    """
    if not crop or crop == "Unknown" or not disease or disease.lower() in ("healthy", "none"):
        dossier = dict(HEALTHY_PROFILE)
        dossier["crop"] = crop or "Crop"
        dossier["disease"] = "Healthy"
        dossier["status"] = "healthy"
        dossier["health_score"] = min(100, int(90 + (confidence * 10)))
        return dossier

    key = (crop, disease)
    info = DISEASE_KNOWLEDGE_BASE.get(key)

    if not info:
        # Fuzzy match on disease substring
        for (c, d), data in DISEASE_KNOWLEDGE_BASE.items():
            if c.lower() == crop.lower() and (d.lower() in disease.lower() or disease.lower() in d.lower()):
                info = data
                break

    if not info:
        # Generic disease profile fallback
        info = {
            "pathogen": "Plant Pathogen",
            "pathogen_type": "Fungal / Bacterial",
            "severity": "MEDIUM",
            "health_score": max(30, int(100 - (confidence * 60))),
            "symptoms": [
                f"Foliar lesions or spotting consistent with {disease}",
                "Localized loss of green pigmentation (chlorosis)",
                "Potential reduction in photosynthetic efficiency"
            ],
            "immediate_action": "Isolate affected foliage, check field moisture, and consult local extension officer.",
            "chemical_treatment": {
                "fungicide": "Broad-spectrum systemic fungicide (e.g., Mancozeb or Azoxystrobin)",
                "dosage": "2.0 g/L of water",
                "interval": "Apply at 10–14 day intervals upon disease confirmation."
            },
            "organic_treatment": {
                "remedy": "Neem oil spray (0.5%) + Copper Oxychloride",
                "dosage": "3 ml/L of water",
                "notes": "Suppresses fungal spore germination on healthy leaf area."
            },
            "prevention": [
                "Implement strict field sanitation and crop rotation",
                "Maintain optimal plant spacing and drip irrigation",
                "Avoid overhead irrigation in evening hours"
            ],
            "environmental_risk": "Prolonged leaf wetness and warm humid conditions."
        }

    dossier = dict(info)
    dossier["crop"] = crop
    dossier["disease"] = disease
    dossier["status"] = "diseased"
    # Adjust score based on confidence
    return dossier
