with open("C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/581/content.md", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("streamController.enqueue")
if idx != -1:
    snippet = text[idx:idx+500]
    print("Snippet:", snippet)
