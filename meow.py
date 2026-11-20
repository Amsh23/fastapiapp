import json
import random
from datetime import datetime, timezone

CATS = [
    {"mood": "happy", "sound": "Meow! 🐱", "emoji": "😸"},
    {"mood": "angry", "sound": "HISSS! 😾", "emoji": "😾"},
    {"mood": "sleepy", "sound": "Zzz... meow 💤", "emoji": "😴"},
    {"mood": "royal", "sound": "Meeeow, human! 👑", "emoji": "👑"},
    {"mood": "hungry", "sound": "Give me fish! 🐟", "emoji": "🐟"},
    {"mood": "chaotic", "sound": "MREOW-WOW! 🙀", "emoji": "🙀"},
    {"mood": "affectionate", "sound": "Purr purr... 💗", "emoji": "😻"},
]

def main():
    cat = random.choice(CATS)
    result = {
        "status": "success",
        "engine": "Meow Engine",
        "message": cat["sound"],
        "mood": cat["mood"],
        "emoji": cat["emoji"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
