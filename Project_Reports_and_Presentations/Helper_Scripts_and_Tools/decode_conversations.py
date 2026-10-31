import json

for step, name in [(581, "LINK 1"), (583, "LINK 2")]:
    path = f"C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/{step}/content.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    idx = content.find("streamController.enqueue(")
    script_end = content.find("</script>", idx)
    full_call = content[idx:script_end].strip()
    
    # Extract inside of streamController.enqueue(...)
    arg = full_call[len("streamController.enqueue("):]
    if arg.endswith(";"):
        arg = arg[:-1].strip()
    if arg.endswith(")"):
        arg = arg[:-1].strip()
    
    try:
        decoded_outer = json.loads(arg)
        decoded_inner = json.loads(decoded_outer)
        print(f"\n==================== {name} ====================")
        for item in decoded_inner:
            if isinstance(item, str) and len(item) > 30:
                if not item.startswith("http") and not item.startswith("/cdn") and not item.startswith("text/") and not "uuid" in item:
                    print("\n--- CONTENT PIECE ---")
                    print(item)
    except Exception as e:
        print(f"Error for {name}:", e)
