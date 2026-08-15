import json
import re
import os
from glob import glob

def generate_apple_aliases(official_name):
    """Erzeugt vollautomatisch gängige Apple-Maps-Aliase aus dem offiziellen Clubnamen."""
    aliases = set()
    if not official_name:
        return []

    official_name = official_name.strip()
    aliases.add(official_name)
    
    # Bekannte Golf-Präfixe, die Apple Maps oft weglässt oder anpasst
    prefixes = [
        "Golf- und Landclub", "Golf- und Country-Club", "Golf- & Landclub", "Golf- & Country-Club",
        "Golfclub e.V.", "Golf-Club e.V.", "Golfclub", "Golf-Club", "Golfanlage", 
        "Golfpark", "Golf-Resort", "Golfresort", "Golf Range", "Golfrange", "Gut", "Hofgut"
    ]
    
    clean_name = official_name
    for prefix in sorted(prefixes, key=len, reverse=True):
        clean_name = re.sub(r"^\b" + re.escape(prefix) + r"\b", "", clean_name, flags=re.IGNORECASE)
    
    clean_name = clean_name.strip(" -.,")
    
    if clean_name:
        aliases.add(f"Golf Resort {clean_name}")
        aliases.add(f"Golfclub {clean_name}")
        aliases.add(f"Golfanlage {clean_name}")
        aliases.add(f"Golfpark {clean_name}")
        aliases.add(clean_name)
        
        base_name = re.sub(r"\s+am\s+.*$", "", clean_name, flags=re.IGNORECASE).strip()
        if base_name and base_name != clean_name:
            aliases.add(f"Golf Resort {base_name}")
            aliases.add(f"Golfclub {base_name}")
            aliases.add(base_name)

    return list(aliases)

def extract_courses_from_data(data):
    """Extrahiert flexibel die Kurs-/Club-Einträge aus unterschiedlichen JSON-Strukturen."""
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        for key in ["courses", "clubs", "features", "elements", "data"]:
            if key in data and isinstance(data[key], list):
                return data[key]
        for val in data.values():
            if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                return val
    return []

def build_global_alias_file():
    # Ermittelt das aktuelle Verzeichnis, in dem das Skript liegt
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ignorieren wir die Zieldatei selbst, falls sie schon existiert
    output_filename = "all_apple_aliases.json"
    output_file_path = os.path.join(current_dir, output_filename)
    
    # Suche alle .json Dateien im selben Verzeichnis
    json_files = glob(os.path.join(current_dir, "*.json"))
    
    master_alias_database = {}
    seen_names = set()
    ignored_names = {"driving range", "putting green", "pro shop", "golf academy", "chipping green"}

    for file_path in json_files:
        filename = os.path.basename(file_path)
        if filename == output_filename:
            continue  # Überspringe die Output-Datei selbst
            
        print(f"📂 Lese '{filename}'...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                courses = extract_courses_from_data(data)
                print(f"   ➔ {len(courses)} Einträge gefunden.")
                
                for course in courses:
                    # Offiziellen Namen über gängige Schlüssel ermitteln
                    official_name = (
                        course.get("name") or 
                        course.get("official_name") or 
                        course.get("clubName") or
                        course.get("properties", {}).get("name")
                    )
                    
                    if not official_name:
                        continue
                        
                    clean_name = official_name.strip()
                    if clean_name.lower() in ignored_names or clean_name in seen_names:
                        continue
                        
                    seen_names.add(clean_name)
                    
                    # Aliase generieren
                    aliases = generate_apple_aliases(clean_name)
                    
                    # Eintrag für die globale Alias-Datei strukturieren
                    master_alias_database[clean_name] = {
                        "official_name": clean_name,
                        "source_file": filename,
                        "apple_maps_aliases": aliases
                    }
                    
        except Exception as e:
            print(f"❌ Fehler beim Verarbeiten von {filename}: {e}")

    # In die finale JSON-Datei schreiben
    final_output = list(master_alias_database.values())
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 Fertig! Insgesamt {len(final_output)} Clubs verarbeitet und in '{output_filename}' gespeichert.")

if __name__ == "__main__":
    build_global_alias_file()