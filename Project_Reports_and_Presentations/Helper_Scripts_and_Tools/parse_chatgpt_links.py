import re
import json

def parse_link(step, name):
    path = f"C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/{step}/content.md"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"\n======================================================\n{name}\n======================================================")
    
    # Extract string passed to streamController.enqueue
    matches = re.findall(r'window\.__reactRouterContext\.streamController\.enqueue\((.*?)\);', html, re.DOTALL)
    for m in matches:
        try:
            # m is a quoted json string literal
            decoded_outer = json.loads(m)
            decoded_inner = json.loads(decoded_outer)
            if isinstance(decoded_inner, list):
                for item in decoded_inner:
                    if isinstance(item, str) and len(item) > 40:
                        # filter out urls and css classes
                        if not item.startswith("http") and not item.startswith("/cdn"):
                            print(f"\n--- [CONTENT] ---\n{item}\n")
        except Exception as e:
            print("Parse error:", e)

if __name__ == "__main__":
    parse_link(581, "Link 1: Real Time System Design")
    parse_link(583, "Link 2: System Design Topics")
