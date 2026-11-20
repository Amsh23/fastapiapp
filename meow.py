import json

def main():
    print(json.dumps({
        "status": "success",
        "message": "Meow! 🐱"
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
