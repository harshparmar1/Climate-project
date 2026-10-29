import os
import re
import json
import math
import datetime
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional, Tuple

# Pre-populated dictionary for instant, fast geocoding of major Indian & Global cities
CITY_DATABASE: Dict[str, Tuple[float, float]] = {
    "ahmedabad": (23.0225, 72.5714),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "kolkata": (22.5726, 88.3639),
    "chennai": (13.0827, 80.2707),
    "hyderabad": (17.3850, 78.4867),
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "surat": (21.1702, 72.8311),
    "lucknow": (26.8467, 80.9462),
    "kanpur": (26.4499, 80.3319),
    "nagpur": (21.1458, 79.0882),
    "indore": (22.7196, 75.8577),
    "thane": (19.2183, 72.9781),
    "bhopal": (23.2599, 77.4126),
    "visakhapatnam": (17.6868, 83.2185),
    "patna": (25.5941, 85.1376),
    "vadodara": (22.3072, 73.1812),
    "ghaziabad": (28.6692, 77.4538),
    "ludhiana": (30.9010, 75.8573),
    "agra": (27.1767, 78.0081),
    "nashik": (19.9975, 73.7898),
    "faridabad": (28.4089, 77.3178),
    "meerut": (28.9845, 77.7064),
    "rajkot": (22.3039, 70.8022),
    "varanasi": (25.3176, 82.9739),
    "srinagar": (34.0837, 74.7973),
    "aurangabad": (19.8762, 75.3433),
    "amritsar": (31.6340, 74.8723),
    "navi mumbai": (19.0330, 73.0297),
    "allahabad": (25.4358, 81.8463),
    "prayagraj": (25.4358, 81.8463),
    "ranchi": (23.3441, 85.3096),
    "howrah": (22.5958, 88.2636),
    "coimbatore": (11.0168, 76.9558),
    "jabalpur": (23.1815, 79.9864),
    "gwalior": (26.2235, 78.1792),
    "vijayawada": (16.5062, 80.6480),
    "jodhpur": (26.2389, 73.0243),
    "madurai": (9.9252, 78.1198),
    "raipur": (21.2514, 81.6296),
    "kota": (25.2138, 75.8648),
    "guwahati": (26.1445, 91.7362),
    "chandigarh": (30.7333, 76.7794),
    "solapur": (17.6599, 75.9064),
    "hubli": (15.3647, 75.1240),
    "bareilly": (28.3670, 79.4304),
    "moradabad": (28.8386, 78.7733),
    "mysore": (12.2958, 76.6394),
    "mysuru": (12.2958, 76.6394),
    "gurgaon": (28.4595, 77.0266),
    "gurugram": (28.4595, 77.0266),
    "aligarh": (27.8974, 78.0880),
    "jalandhar": (31.3260, 75.5762),
    "tiruchirappalli": (10.7905, 78.7047),
    "bhubaneswar": (20.2961, 85.8245),
    "salem": (11.6643, 78.1460),
    "warangal": (17.9689, 79.5941),
    "thiruvananthapuram": (8.5241, 76.9366),
    "trivandrum": (8.5241, 76.9366),
    "dehradun": (30.3165, 78.0322),
    "shimla": (31.1048, 77.1734),
    "gangtok": (27.3389, 88.6065),
    "shillong": (25.5788, 91.8933),
    "imphal": (24.8170, 93.9368),
    "aizawl": (23.7271, 92.7176),
    "kohima": (25.6747, 94.1086),
    "itanagar": (27.0844, 93.6053),
    "agartala": (23.8315, 91.2868),
    "panaji": (15.4909, 73.8278),
    "goa": (15.2993, 74.1240),
    "noida": (28.5355, 77.3910),
    "kochi": (9.9312, 76.2673),
    "cochin": (9.9312, 76.2673),
    # Indian States & Union Territories
    "gujarat": (22.2587, 71.1924),
    "maharashtra": (19.7515, 75.7139),
    "punjab": (31.1471, 75.3412),
    "rajasthan": (27.0238, 74.2179),
    "karnataka": (15.3173, 75.7139),
    "tamil nadu": (11.1271, 78.6569),
    "kerala": (10.8505, 76.2711),
    "uttar pradesh": (26.8467, 80.9462),
    "up": (26.8467, 80.9462),
    "bihar": (25.0961, 85.3131),
    "west bengal": (22.9868, 87.8550),
    "bengal": (22.9868, 87.8550),
    "madhya pradesh": (22.9734, 78.6569),
    "mp": (22.9734, 78.6569),
    "haryana": (29.0588, 76.0856),
    "telangana": (18.1124, 79.0193),
    "andhra pradesh": (15.9129, 79.7400),
    "andhra": (15.9129, 79.7400),
    "odisha": (20.9517, 85.0985),
    "orissa": (20.9517, 85.0985),
    "assam": (26.2006, 92.9376),
    "himachal pradesh": (31.1048, 77.1734),
    "himachal": (31.1048, 77.1734),
    "jammu and kashmir": (33.7782, 76.5762),
    "kashmir": (33.7782, 76.5762),
    "jharkhand": (23.6102, 85.2799),
    "chhattisgarh": (21.2787, 81.8661),
    "uttarakhand": (30.0668, 79.0193),
    "goa": (15.2993, 74.1240),
    # International cities
    "london": (51.5074, -0.1278),
    "new york": (40.7128, -74.0060),
    "tokyo": (35.6762, 139.6503),
    "paris": (48.8566, 2.3522),
    "sydney": (-33.8688, 151.2093),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "toronto": (43.6532, -79.3832),
    "berlin": (52.5200, 13.4050),
    "beijing": (39.9042, 116.4074),
    "cairo": (30.0444, 31.2357),
    "moscow": (55.7558, 37.6173),
    "los angeles": (34.0522, -118.2437),
}

STATE_CROP_INTELLIGENCE = {
    "Gujarat": {
        "kharif": ["Cotton (Bt Cotton)", "Groundnut (Peanut)", "Bajra (Pearl Millet)", "Soybean", "Sesame", "Castor"],
        "rabi": ["Wheat", "Mustard", "Gram (Chana)", "Cumin (Jeera)", "Fennel (Saunf)", "Barley"],
        "zaid": ["Watermelon", "Muskmelon", "Maize", "Summer Vegetables (Okra, Cluster Bean)"],
        "soil": "Black Cotton Soil (Regur) in Saurashtra/Central & Alluvial Sandy Loam in North Gujarat & Kutch",
        "climate": "Semi-arid to tropical, 25°C - 38°C summers, 600-900mm monsoon rainfall",
        "tip": "Gujarat is India's top producer of Cotton and Groundnut. Ensure good drainage in black soils to avoid root rot."
    },
    "Maharashtra": {
        "kharif": ["Cotton", "Sugarcane", "Soybean", "Tur (Pigeon Pea)", "Rice (Konkan region)", "Bajra"],
        "rabi": ["Jowar (Sorghum)", "Wheat", "Gram (Chana)", "Safflower", "Onion"],
        "zaid": ["Groundnut", "Sunflower", "Alphonso Mangoes", "Grapes", "Pomegranate"],
        "soil": "Deep Black Basaltic Soil (Regur) in Deccan Plateau & Laterite Soil in coastal Konkan",
        "climate": "Tropical monsoon, heavy rainfall in Western Ghats/Konkan, dry semi-arid in Marathwada",
        "tip": "Drip irrigation is highly recommended for Sugarcane and Fruit orchards in Marathwada & Vidarbha."
    },
    "Punjab": {
        "kharif": ["Paddy (Rice)", "Cotton", "Maize", "Sugarcane", "Moong"],
        "rabi": ["Wheat (India's Granary)", "Mustard", "Barley", "Gram (Chana)", "Potato"],
        "zaid": ["Sunflower", "Fodder Crops", "Summer Vegetables"],
        "soil": "Extremely fertile Deep Alluvial Soil (Indus Plains)",
        "climate": "Subtropical continental, hot summers (up to 40°C), cool winters (4°C - 15°C), 500-800mm rain",
        "tip": "Adopt Happy Seeder or zero-tillage wheat sowing after Paddy harvest to conserve soil moisture."
    },
    "Rajasthan": {
        "kharif": ["Bajra (Pearl Millet)", "Guar (Cluster Bean)", "Groundnut", "Moong", "Moth Bean", "Sesame"],
        "rabi": ["Mustard (Rapeseed)", "Wheat", "Gram (Chana)", "Barley", "Cumin", "Isabgol"],
        "zaid": ["Watermelon", "Muskmelon", "Fodder Crops"],
        "soil": "Desert Sandy Soil in West, Sandy Loam & Alluvial in East",
        "climate": "Arid to semi-arid, low rainfall (200-500mm), high summer temperatures",
        "tip": "Rajasthan produces 40%+ of India's Mustard and Pearl Millet. Drip and sprinkler systems are essential."
    },
    "Uttar Pradesh": {
        "kharif": ["Rice", "Sugarcane (Top Producer)", "Maize", "Arhar (Tur)", "Bajra"],
        "rabi": ["Wheat (Top Producer)", "Mustard", "Barley", "Gram", "Peas", "Potato"],
        "zaid": ["Muskmelon", "Watermelon", "Cucumber", "Urad"],
        "soil": "Deep Fertile Gangetic Alluvial Soil",
        "climate": "Humid subtropical, generous rainfall (800-1200mm), warm summers and chilly winters",
        "tip": "UP is India's leading producer of Wheat, Sugarcane, and Potatoes. Ensure proper crop rotation with pulses."
    },
    "Madhya Pradesh": {
        "kharif": ["Soybean (Soy Bowl of India)", "Cotton", "Maize", "Rice", "Pigeon Pea (Tur)"],
        "rabi": ["Wheat (Sharbati Wheat)", "Gram (Chana)", "Mustard", "Lentil (Masoor)", "Garlic"],
        "zaid": ["Moong", "Urad", "Vegetables"],
        "soil": "Deep Black Soil in Malwa/Narmada Valley & Red-Yellow Soil in Bundelkhand",
        "climate": "Subtropical to tropical, 900-1300mm annual rainfall",
        "tip": "MP is the top producer of Pulses and Soybean in India. Organic farming yields high market value for Sharbati Wheat."
    },
    "Karnataka": {
        "kharif": ["Ragi (Finger Millet)", "Maize", "Rice", "Cotton", "Sugarcane", "Groundnut"],
        "rabi": ["Jowar (Sorghum)", "Bengal Gram", "Wheat", "Sunflower"],
        "zaid": ["Coffee (Arabica/Robusta)", "Arecanut", "Cardamom", "Pepper", "Pomegranate"],
        "soil": "Red Sandy Loam in South, Black Cotton Soil in North Karnataka, Laterite in Coastal Canara",
        "climate": "Tropical wet and dry, high rainfall in Western Ghats/Malnad",
        "tip": "Karnataka is India's largest Coffee and Ragi producer. Intercropping Ragi with Pulses improves soil nitrogen."
    },
    "Tamil Nadu": {
        "kharif": ["Rice (Paddy - Kuruvai)", "Sugarcane", "Cotton", "Groundnut", "Sesame"],
        "rabi": ["Rice (Samba)", "Black Gram (Urad)", "Green Gram (Moong)", "Maize"],
        "zaid": ["Banana", "Coconut", "Mango", "Tapioca"],
        "soil": "Red Loamy Soil, Black Soil (Karisal), & Coastal Alluvial Soil",
        "climate": "Tropical climate influenced heavily by Northeast Monsoon (Oct-Dec)",
        "tip": "Tamil Nadu excels in Rice and Banana cultivation. Utilize System of Rice Intensification (SRI) to save water."
    },
    "Kerala": {
        "kharif": ["Rice (Paddy)", "Rubber (Top Producer)", "Tapioca", "Cardamom", "Pepper"],
        "rabi": ["Coconut", "Arecanut", "Cashew", "Coffee", "Tea"],
        "zaid": ["Banana (Nendran)", "Pineapple", "Ginger", "Turmeric"],
        "soil": "Laterite Soil on Slopes, Coastal Alluvial in Lowlands, Red Soil in Palakkad",
        "climate": "Tropical monsoon, heavy double-monsoon rainfall (2500-3000mm/year)",
        "tip": "Kerala is India's Spices & Rubber hub. Terracing laterite slopes prevents soil erosion during heavy rains."
    },
    "Bihar": {
        "kharif": ["Rice (Paddy)", "Maize", "Jute", "Arhar"],
        "rabi": ["Wheat", "Maize (Rabi Maize)", "Mustard", "Gram", "Lentil", "Potato"],
        "zaid": ["Litchi (Shahi Litchi)", "Mango", "Watermelon", "Pointed Gourd (Parwal)"],
        "soil": "Fertile Gangetic Alluvial Soil & Calcareous Soil in North Bihar",
        "climate": "Subtropical monsoon, fertile river basin with ample monsoon rainfall",
        "tip": "Bihar's Rabi Maize and Muzaffarpur Shahi Litchi have global demand. Ensure good drainage during flood season."
    },
    "West Bengal": {
        "kharif": ["Rice (Aus & Aman Paddy)", "Jute (Top Producer)", "Maize", "Sesame"],
        "rabi": ["Boro Rice", "Wheat", "Mustard", "Potato", "Lentil"],
        "zaid": ["Mango (Himsagar)", "Tea (Darjeeling)", "Pineapple", "Vegetables"],
        "soil": "Rich Deltaic Alluvial Soil & Terai Soil in North",
        "climate": "Tropical wet, heavy monsoon rainfall (1500-2500mm)",
        "tip": "West Bengal is India's top Rice and Jute producer. Boro rice in winter utilizes post-monsoon water reserves."
    },
    "Haryana": {
        "kharif": ["Paddy (Basmati Rice)", "Cotton", "Bajra", "Sugarcane"],
        "rabi": ["Wheat", "Mustard", "Gram (Chana)", "Barley"],
        "zaid": ["Sunflower", "Vegetables", "Fodder"],
        "soil": "Deep Fertile Alluvial Soil & Sandy Soil in Southwest",
        "climate": "Semi-arid continental, warm summers and cold winters",
        "tip": "Haryana is famous for premium Basmati Rice and high Wheat yields. Micro-irrigation reduces groundwater depletion."
    },
    "Andhra Pradesh": {
        "kharif": ["Rice (Rice Bowl)", "Cotton", "Groundnut", "Maize", "Sugarcane"],
        "rabi": ["Bengal Gram", "Black Gram", "Tobacco", "Sunflower"],
        "zaid": ["Chilli (Guntur Chilli)", "Mango", "Papaya", "Oil Palm"],
        "soil": "Red Loam, Black Cotton Soil, & Coastal Alluvium",
        "climate": "Tropical wet and dry, high rainfall in coastal districts",
        "tip": "AP is India's leading producer of Red Chillies and Oil Palm. Drip fertigation boosts Chilli yields significantly."
    },
    "Telangana": {
        "kharif": ["Cotton", "Paddy (Rice)", "Maize", "Soybean", "Red Gram (Tur)"],
        "rabi": ["Bengal Gram", "Groundnut", "Sesame", "Sunflower"],
        "zaid": ["Mango", "Sweet Lime (Mosambi)", "Vegetables"],
        "soil": "Red Sandy Soils (Chalka) & Deep Black Cotton Soils",
        "climate": "Semi-arid tropical, hot summers, 800-1000mm rainfall",
        "tip": "Telangana is a major Cotton and Maize hub. Crop diversification with Red Gram restores soil nitrogen."
    }
}

METRIC_EXPLANATIONS = {
    "t2m": "**T2M (Temperature at 2 Meters)** represents the ambient air temperature measured approximately 2 meters above the Earth's surface. It is a standard meteorological benchmark for human thermal comfort and weather analysis.",
    "prectotcorr": "**PRECTOTCORR (Corrected Total Precipitation)** represents the total bias-corrected daily rainfall/precipitation rate measured in millimeters per day (mm/day).",
    "prectot": "**PRECTOT (Precipitation)** refers to total daily precipitation in millimeters (mm).",
    "ws2m": "**WS2M (Wind Speed at 2 Meters)** measures wind velocity at a standard 2-meter elevation in meters per second (m/s).",
    "rh2m": "**RH2M (Relative Humidity at 2 Meters)** measures the percentage of water vapor present in the air compared to the maximum amount the air can hold at that temperature.",
    "astrokites": "**AstroKites** is an advanced climate intelligence and weather analytics web platform powered by NASA POWER data, interactive 3D WebGL visualizations, historical probability modeling, and real-time forecast mapping."
}


def geocode_city(city_name: str) -> Optional[Tuple[float, float]]:
    """Geocode a city or state name to (lat, lon) using dict first, then Nominatim fallback."""
    if not city_name:
        return None
    
    clean = city_name.strip().lower()
    if clean in CITY_DATABASE:
        return CITY_DATABASE[clean]
    
    # Try partial match in CITY_DATABASE
    for k, coords in CITY_DATABASE.items():
        if k in clean or clean in k:
            return coords
            
    # Nominatim online lookup
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(city_name)}&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "AstroKites-AI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return (lat, lon)
    except Exception:
        pass
        
    return None


def extract_locations_from_query(query: str, page_context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Extract location/state name(s) and coordinates from user prompt or page context."""
    query_lower = query.lower()
    found_locations = []
    
    # 1. Check for comparison patterns (e.g. "between Mumbai and Delhi" or "Gujarat vs Maharashtra")
    vs_match = re.search(r'([a-zA-Z\s]+)\s+(?:vs|versus|and|to|compare(?:d)?\s+with)\s+([a-zA-Z\s]+)', query, re.IGNORECASE)
    
    # Check known cities and states present in text (prioritize longer names first)
    sorted_places = sorted(CITY_DATABASE.keys(), key=len, reverse=True)
    detected_city_names = []
    for place in sorted_places:
        pattern = r'\b' + re.escape(place) + r'\b'
        if re.search(pattern, query_lower):
            title_name = place.title()
            if title_name not in detected_city_names:
                detected_city_names.append(title_name)
            
    if detected_city_names:
        for name in detected_city_names:
            coords = geocode_city(name)
            if coords:
                found_locations.append({"name": name, "lat": coords[0], "lon": coords[1]})
        return found_locations

    # 2. Check general city/state geocoding if query contains phrases like "in <Location>", "at <Location>", "for <Location>"
    loc_match = re.search(r'(?:in|at|for|near|around|of)\s+([a-zA-Z\s]+)', query, re.IGNORECASE)
    if loc_match:
        raw_name = loc_match.group(1).strip()
        raw_name = re.sub(r'\s+(state|today|tomorrow|yesterday|this week|now|in 2024|\?|\.)$', '', raw_name, flags=re.IGNORECASE)
        coords = geocode_city(raw_name)
        if coords:
            return [{"name": raw_name.title(), "lat": coords[0], "lon": coords[1]}]

    # 3. Fallback to page context if available
    if page_context and isinstance(page_context, dict):
        sel_loc = page_context.get("selectedLocation")
        if sel_loc:
            if isinstance(sel_loc, dict) and "lat" in sel_loc and ("lon" in sel_loc or "lng" in sel_loc):
                lon = sel_loc.get("lon") if "lon" in sel_loc else sel_loc.get("lng")
                name = sel_loc.get("name", "Selected Location")
                return [{"name": name, "lat": float(sel_loc["lat"]), "lon": float(lon)}]
            elif isinstance(sel_loc, str):
                coords = geocode_city(sel_loc)
                if coords:
                    return [{"name": sel_loc.title(), "lat": coords[0], "lon": coords[1]}]

    return []


# Groq API configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def call_groq_llm(user_prompt: str, system_prompt: str = None, model: str = "openai/gpt-oss-120b", max_tokens: int = 700) -> Optional[str]:
    """Call Groq API for high-speed, intelligent climate & agriculture answers."""
    api_key = os.environ.get("GROQ_API_KEY") or GROQ_API_KEY
    if not api_key:
        return None

    if not system_prompt:
        system_prompt = (
            "You are AstroKites AI, a helpful, friendly climate & farming assistant. "
            "FORMATTING GUIDELINES FOR ATTRACTIVE & EASY READABILITY: "
            "1. Use simple, clear language with short sentences. "
            "2. Use attractive section titles with emojis (e.g. 🌾, ☀️, 🌧️, 💡, 📍). "
            "3. Present key information in clean bullet points instead of dense paragraphs. "
            "4. Highlight important keywords in **bold**. "
            "5. Always end with a practical 💡 Quick Tip. "
            "6. DO NOT output thinking logs, raw code, or internal reasoning."
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "AstroKites-Backend/1.0"
    }

    # Try models in order of capability
    candidate_models = [model, "openai/gpt-oss-20b", "qwen/qwen3.6-27b", "allam-2-7b"]
    for m in candidate_models:
        payload = {
            "model": m,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }

        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                content = res_json["choices"][0]["message"]["content"]
                if content:
                    # Strip any lingering thinking tags
                    clean_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
                    return clean_content
        except Exception as e:
            continue

    return None


def classify_intent(message: str) -> str:
    """Classify the user intent."""
    m = message.lower()
    
    # Agricultural & Crop suitability queries
    if any(k in m for k in ["crop", "crops", "grow", "growing", "farming", "farm", "farmer", "agriculture", "soil", "kharif", "rabi", "zaid", "harvest", "sow", "plant", "cultivate", "yield"]):
        return "AGRICULTURE_CROPS"

    # Metric explanations
    if any(k in m for k in ["what is t2m", "explain t2m", "prectotcorr", "prectot", "ws2m", "rh2m", "what does t2m mean", "what is astrokites"]):
        return "METRIC_EXPLANATION"
        
    # Comparison
    if any(k in m for k in ["compare", "versus", " vs ", "difference between"]):
        return "COMPARISON"
        
    # Forecast
    if any(k in m for k in ["tomorrow", "next week", "forecast", "will it rain", "upcoming weather", "future"]):
        return "FORECAST"
        
    # Historical / Climate Trend
    if any(k in m for k in ["historical", "climate trend", "in 2024", "past year", "average temperature in 202", "history"]):
        return "HISTORICAL_WEATHER"
        
    # Weather / Current
    if any(k in m for k in ["temperature", "temp", "rain", "rainfall", "precipitation", "wind", "speed", "humidity", "weather"]):
        return "CURRENT_WEATHER"
        
    # General AstroKites / App feature
    if any(k in m for k in ["astrokites", "map", "chart", "export", "download", "feature", "help", "hello", "hi"]):
        return "GENERAL_ASTROKITES"
        
    return "UNKNOWN"


def format_ai_response_with_llm_or_fallback(
    query: str,
    locations_data: List[Dict[str, Any]],
    intent: str,
    history: Optional[List[Dict[str, str]]] = None,
    unit: str = "°C"
) -> Dict[str, Any]:
    """
    Format attractive, easy-to-read natural language response for the user.
    Uses Groq API (openai/gpt-oss-120b) if configured for fast AI generation,
    otherwise uses high-quality structured template generator.
    """
    if "fahrenheit" in query.lower() or "°f" in query.lower() or "in f" in query.lower():
        unit = "°F"

    def c_to_f(val_c):
        if val_c is None:
            return None
        return round((val_c * 9 / 5) + 32, 1)

    # Helper to generate status badge & advice based on weather metrics
    def get_weather_insights(temp_c, rain_mm, wind_ms):
        badge = "☀️ Pleasant & Fair"
        tip = "Great weather for outdoor activities and travel!"
        
        if rain_mm is not None and rain_mm >= 15.0:
            badge = "🌧️ Heavy Rain Alert"
            tip = "Expect heavy rainfall! Keep an umbrella handy and drive cautiously."
        elif rain_mm is not None and rain_mm >= 3.0:
            badge = "🌧️ Rainy Conditions"
            tip = "Light to moderate rain expected. Outdoor plans may need an umbrella."
        elif temp_c is not None and temp_c >= 35.0:
            badge = "🔥 Hot & Sunny"
            tip = "Stay hydrated and avoid direct sun during peak afternoon hours."
        elif temp_c is not None and temp_c <= 12.0:
            badge = "❄️ Cold Weather"
            tip = "Cool temperatures ahead! Layer up before heading outside."
        elif wind_ms is not None and wind_ms >= 8.0:
            badge = "💨 Windy Breeze"
            tip = "Breezy conditions. Secure loose outdoor objects."
            
        return badge, tip

    # 1. Handle Agriculture / Crop suitability intent via Groq API
    if intent == "AGRICULTURE_CROPS":
        loc_str = None
        temp = 28.5
        rain = 0.5
        humidity = 65

        if locations_data and len(locations_data) > 0:
            loc = locations_data[0]
            loc_str = loc.get("name")
            temp = loc.get("temperature", 28.5)
            rain = loc.get("rainfall", 0.5)
            humidity = loc.get("humidity", 65)

        if not loc_str or loc_str == "Selected Location":
            # Extract location from query using regex pattern
            loc_match = re.search(r'(?:in|for|at|around|of|near)\s+([a-zA-Z\s]+)', query, re.IGNORECASE)
            if loc_match:
                extracted_name = loc_match.group(1).strip()
                loc_str = re.sub(r'\s+(state|today|tomorrow|yesterday|this week|now|in 2024|\?|\.)$', '', extracted_name, flags=re.IGNORECASE).title()

        if not loc_str:
            q_low = query.lower()
            known_places = ["uttar pradesh", "up", "punjab", "maharashtra", "gujarat", "rajasthan", "karnataka", "tamil nadu", "kerala", "bihar", "west bengal", "madhya pradesh", "mp", "haryana", "telangana", "andhra pradesh", "odisha", "assam", "himachal pradesh", "jammu and kashmir", "kashmir", "jharkhand", "chhattisgarh", "uttarakhand", "goa", "delhi", "mumbai", "ahmedabad", "surat", "pune", "jaipur", "lucknow", "kanpur", "varanasi", "agra"]
            for place in known_places:
                if place in q_low:
                    loc_str = place.title()
                    break

        if not loc_str:
            extracted = extract_locations_from_query(query)
            if extracted:
                loc_str = extracted[0]["name"]

        if not loc_str:
            loc_str = query.strip().title()

        sys_prompt = (
            f"You are AstroKites AI Agricultural Expert powered by Groq LLM.\n"
            f"Provide a 100% REAL, authentic, highly accurate crop suitability guide specifically for {loc_str}.\n"
            f"LIVE NASA WEATHER METRICS FOR {loc_str}:\n"
            f"- Current Temperature: {temp}°C\n"
            f"- Daily Rainfall Rate: {rain} mm/day\n"
            f"- Relative Humidity: {humidity}%\n\n"
            f"FORMATTING TEMPLATE (Simple, Clean & Attractive):\n"
            f"📍 **Location:** {loc_str}\n"
            f"🌡️ **Live Climate Metrics:** {temp}°C | Rainfall: {rain} mm/day | Humidity: {humidity}%\n\n"
            f"🌱 **Most Suitable Real Crops for {loc_str}**\n"
            f"• **Commercial Crops:** [List real primary cash crops grown in {loc_str}]\n"
            f"• **Staple Food Crops:** [List real primary grain/food crops grown in {loc_str}]\n"
            f"• **Horticulture / Fruits / Vegetables:** [List real fruit & vegetable crops grown in {loc_str}]\n\n"
            f"🌦️ **Soil & Climate Profile**\n"
            f"• **Soil Type:** [Describe real soil types specifically found in {loc_str}]\n"
            f"• **Climate Match:** [Describe real growing conditions and climate in {loc_str}]\n\n"
            f"💡 **Practical Farmer Advice**\n"
            f"[Provide 1-2 practical, high-value farming advice specifically for {loc_str}]\n\n"
            f"CRITICAL REQUIREMENT:\n"
            f"All crop names, soil types, and advice MUST be 100% SPECIFIC to {loc_str}. Do NOT mention any other location."
        )

        groq_resp = call_groq_llm(
            user_prompt=f"User asked: '{query}'. Provide real, highly accurate location-specific crop suitability data for {loc_str} with NASA weather ({temp}°C, {rain}mm/day rainfall).",
            system_prompt=sys_prompt,
            model="openai/gpt-oss-120b"
        )

        if groq_resp:
            return {
                "answer": groq_resp,
                "data": {"location": loc_str, "type": "crop_intelligence"},
                "source": f"Groq AI & NASA POWER Agriculture ({loc_str})",
                "intent": intent
            }

        # Dynamic fallback if LLM is offline
        fallback_ans = (
            f"📍 **Location:** {loc_str}\n"
            f"🌡️ **Live Climate Metrics:** {temp}°C | Rainfall: {rain} mm/day | Humidity: {humidity}%\n\n"
            f"🌱 **Most Suitable Real Crops for {loc_str}**\n"
            f"• **Commercial Crops:** Regional primary cash crops for {loc_str}\n"
            f"• **Staple Food Crops:** Grain and pulse crops cultivated in {loc_str}\n"
            f"• **Horticulture / Vegetables:** Fruits, vegetables & spices suited for {loc_str}\n\n"
            f"🌦️ **Soil & Climate Profile**\n"
            f"• **Soil Type:** Regional soil profile for {loc_str}\n"
            f"• **Climate Match:** Local climate profile suited for agriculture\n\n"
            f"💡 **Practical Farmer Advice**\n"
            f"Consult local agricultural extension services for optimal sowing windows in {loc_str}."
        )

        return {
            "answer": fallback_ans,
            "data": {"location": loc_str, "type": "crop_intelligence"},
            "source": f"AstroKites Agriculture ({loc_str})",
            "intent": intent
        }

    # 2. Handle Metric Explanation intent
    if intent == "METRIC_EXPLANATION":
        q = query.lower()
        if "t2m" in q:
            ans = (
                "🌡️ **T2M (Temperature at 2 Meters)**\n\n"
                "• **What it is:** Ambient air temperature measured 2 meters above ground level.\n"
                "• **Why it matters:** Standard global benchmark for human thermal comfort.\n"
                "• **Unit:** Degrees Celsius (°C) or Fahrenheit (°F)."
            )
        elif "prectot" in q:
            ans = (
                "🌧️ **PRECTOT (Total Precipitation)**\n\n"
                "• **What it is:** Total daily precipitation/rainfall rate.\n"
                "• **Scale:**\n"
                "  - `< 5 mm/day`: Light drizzle / dry\n"
                "  - `5 – 15 mm/day`: Moderate rainfall\n"
                "  - `> 15 mm/day`: Heavy rain alert ⚠️\n"
                "• **Unit:** Millimeters per day (mm/day)."
            )
        elif "ws2m" in q:
            ans = (
                "💨 **WS2M (Wind Speed at 2 Meters)**\n\n"
                "• **What it is:** Wind velocity measured at 2 meters height.\n"
                "• **Conversion:** 1 m/s ≈ 3.6 km/h.\n"
                "• **Unit:** Meters per second (m/s)."
            )
        elif "rh2m" in q:
            ans = (
                "💧 **RH2M (Relative Humidity)**\n\n"
                "• **What it is:** Amount of moisture in the air relative to maximum capacity.\n"
                "• **Comfort Range:** 30% – 60% feels most comfortable for humans."
            )
        elif "astrokites" in q:
            ans = (
                "🚀 **AstroKites Climate Intelligence**\n\n"
                "AstroKites is an advanced 3D weather intelligence console powered by **NASA POWER** satellite data. "
                "It offers real-time forecasts, historical probability analysis, and interactive 3D visualizations."
            )
        else:
            ans = (
                "📊 **NASA POWER Weather Parameters**\n\n"
                "• 🌡️ **T2M**: Air Temperature at 2m (°C)\n"
                "• 🌧️ **PRECTOTCORR**: Daily Rainfall (mm/day)\n"
                "• 💨 **WS2M**: Wind Speed (m/s)\n"
                "• 💧 **RH2M**: Relative Humidity (%)"
            )
            
        return {
            "answer": ans,
            "data": None,
            "source": "AstroKites Knowledge Base",
            "intent": intent
        }

    # 3. Handle Unknown / Out of Scope via Groq API
    if intent == "UNKNOWN":
        groq_resp = call_groq_llm(
            user_prompt=f"Answer the user query concisely and attractively: '{query}'",
            system_prompt=(
                "You are AstroKites AI, an expert weather, climate, and agriculture assistant. "
                "Provide an attractive, helpful answer using markdown, bullet points, and emojis."
            )
        )
        if groq_resp:
            return {
                "answer": groq_resp,
                "data": None,
                "source": "Groq AI",
                "intent": intent
            }

        return {
            "answer": (
                "👋 **Hi! I'm AstroKites AI Weather & Agriculture Assistant**\n\n"
                "I can give you instant weather forecasts, crop recommendations, and climate insights for any location!\n\n"
                "💡 **Try asking me:**\n"
                "  • *\"Which crops grow in Gujarat?\"*\n"
                "  • *\"What is the weather in Mumbai?\"*\n"
                "  • *\"Will it rain in Ahmedabad tomorrow?\"*\n"
                "  • *\"Compare weather between Delhi and Bangalore\"*"
            ),
            "data": None,
            "source": "AstroKites AI",
            "intent": intent
        }

    # 4. If no location data returned or missing location
    if not locations_data:
        return {
            "answer": (
                "📍 **Which location would you like to check?**\n\n"
                "Please specify a city or state name (e.g. *\"Which crops grow in Gujarat?\"* or *\"Weather in Ahmedabad\"*) or select a spot on the **Map**."
            ),
            "data": None,
            "source": "AstroKites AI",
            "intent": intent,
            "needs_location": True
        }

    # 5. Single Location Weather Details
    loc = locations_data[0]
    loc_name = loc.get("name", "Target Location")
    temp_c = loc.get("temperature")
    rain_mm = loc.get("rainfall")
    wind_ms = loc.get("wind_speed")
    humidity = loc.get("humidity", 65)
    
    disp_temp = c_to_f(temp_c) if unit == "°F" and temp_c is not None else temp_c
    temp_unit_str = "°F" if unit == "°F" else "°C"
    badge, advice_tip = get_weather_insights(temp_c, rain_mm, wind_ms)

    # Try Groq LLM enrichment if available
    sys_prompt = (
        "You are AstroKites AI. Format an attractive, easy-to-read answer using emojis, bold highlights, bullet points, and a friendly tip. "
        "Strictly use the provided authoritative weather numbers without modifying them."
    )
    groq_resp = call_groq_llm(
        user_prompt=f"User asked: '{query}'. Retrieved Weather for {loc_name}: Temp={disp_temp}{temp_unit_str}, Rainfall={rain_mm} mm/day, Wind={wind_ms} m/s, Humidity={humidity}%. Condition Badge: {badge}.",
        system_prompt=sys_prompt
    )

    if groq_resp:
        return {
            "answer": groq_resp,
            "data": {
                "location": loc_name,
                "latitude": loc.get("lat"),
                "longitude": loc.get("lon"),
                "temperature": disp_temp,
                "humidity": humidity,
                "wind_speed": wind_ms,
                "precipitation": rain_mm,
                "unit": temp_unit_str
            },
            "source": "NASA POWER & Groq AI",
            "intent": intent
        }

    # Comparison intent
    if intent == "COMPARISON" and len(locations_data) >= 2:
        loc1 = locations_data[0]
        loc2 = locations_data[1]
        
        t1 = c_to_f(loc1.get("temperature")) if unit == "°F" else loc1.get("temperature")
        t2 = c_to_f(loc2.get("temperature")) if unit == "°F" else loc2.get("temperature")
        
        diff = abs(round(t1 - t2, 1)) if (t1 is not None and t2 is not None) else 0
        warmer_city = loc1["name"] if (t1 and t2 and t1 > t2) else loc2["name"]
        
        answer_text = (
            f"⚔️ **Weather Comparison: {loc1['name']} vs {loc2['name']}**\n\n"
            f"📍 **{loc1['name']}**\n"
            f"  • 🌡️ Temp: **{t1}{temp_unit_str}** | 🌧️ Rain: **{loc1.get('rainfall', 0)} mm** | 💨 Wind: **{loc1.get('wind_speed', 3.2)} m/s**\n\n"
            f"📍 **{loc2['name']}**\n"
            f"  • 🌡️ Temp: **{t2}{temp_unit_str}** | 🌧️ Rain: **{loc2.get('rainfall', 0)} mm** | 💨 Wind: **{loc2.get('wind_speed', 3.2)} m/s**\n\n"
            f"🏆 **Takeaway:** **{warmer_city}** is currently **{diff}{temp_unit_str} warmer**."
        )
        
        return {
            "answer": answer_text,
            "data": {
                "location": f"{loc1['name']} vs {loc2['name']}",
                "comparisons": [loc1, loc2],
                "unit": temp_unit_str
            },
            "source": "NASA POWER",
            "intent": intent
        }

    # Forecast intent
    if intent == "FORECAST":
        rain_prob = loc.get("rain_probability", 25)
        rain_desc = "High rain chance 🌧️" if rain_prob >= 50 else "Low precipitation risk ☀️"
        
        answer_text = (
            f"🔮 **Weather Outlook for {loc_name}**\n"
            f"Status: **{badge}**\n\n"
            f"📊 **Forecast Highlights:**\n"
            f"  • 🌡️ **Expected Temp:** {disp_temp}{temp_unit_str}\n"
            f"  • 🌧️ **Rain Probability:** {rain_prob}% ({rain_desc})\n"
            f"  • 💧 **Rainfall Rate:** {rain_mm if rain_mm is not None else 0.0} mm/day\n"
            f"  • 💨 **Wind Velocity:** {wind_ms if wind_ms is not None else 3.2} m/s\n\n"
            f"💡 **Tip:** {advice_tip}"
        )
        
        return {
            "answer": answer_text,
            "data": {
                "location": loc_name,
                "temperature": disp_temp,
                "humidity": humidity,
                "wind_speed": wind_ms,
                "precipitation": rain_mm,
                "unit": temp_unit_str
            },
            "source": "NASA POWER / AstroKites Forecast",
            "intent": intent
        }

    # Default Current Weather
    answer_text = (
        f"🌍 **Current Weather in {loc_name}**\n"
        f"Condition: **{badge}**\n\n"
        f"📊 **Metrics Summary:**\n"
        f"  • 🌡️ **Temperature:** {disp_temp}{temp_unit_str}\n"
        f"  • 🌧️ **Rainfall:** {rain_mm if rain_mm is not None else 0.0} mm/day\n"
        f"  • 💨 **Wind Speed:** {wind_ms if wind_ms is not None else 3.4} m/s\n"
        f"  • 💧 **Humidity:** {humidity}%\n\n"
        f"💡 **Tip:** {advice_tip}"
    )

    return {
        "answer": answer_text,
        "data": {
            "location": loc_name,
            "latitude": loc.get("lat"),
            "longitude": loc.get("lon"),
            "temperature": disp_temp,
            "humidity": humidity,
            "wind_speed": wind_ms,
            "precipitation": rain_mm,
            "unit": temp_unit_str
        },
        "source": "NASA POWER",
        "intent": intent
    }
