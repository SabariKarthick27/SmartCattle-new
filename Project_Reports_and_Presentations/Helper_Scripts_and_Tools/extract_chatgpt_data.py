import json

def extract_strings_from_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    results = []
    pos = 0
    search_str = "streamController.enqueue("
    while True:
        idx = content.find(search_str, pos)
        if idx == -1:
            break
        start_quote = idx + len(search_str)
        # Find closing quote
        end = content.find(')\n', start_quote)
        if end == -1:
            end = content.find(');', start_quote)
        
        chunk = content[start_quote:end].strip()
        if chunk.endswith(")"):
            chunk = chunk[:-1].strip()
        
        try:
            # chunk is a json string literal like "[...]"
            decoded_str = json.loads(chunk)
            data = json.loads(decoded_str)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str) and len(item) > 20 and not item.startswith("http") and not item.startswith("/cdn") and not item.startswith("text/"):
                        results.append(item)
        except Exception as e:
            pass
        pos = end + 1
    return results

print("=== LINK 1 ===")
res1 = extract_strings_from_html("C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/581/content.md")
for r in res1:
    print("\n--- BLOCK ---")
    print(r)

print("\n\n=== LINK 2 ===")
res2 = extract_strings_from_html("C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/583/content.md")
for r in res2:
    print("\n--- BLOCK ---")
    print(r)
