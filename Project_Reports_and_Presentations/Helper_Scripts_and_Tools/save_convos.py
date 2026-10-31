import json

out_lines = []

for step, name in [(581, "LINK 1: Real Time System Design"), (583, "LINK 2: System Design Topics")]:
    path = f"C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/{step}/content.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    idx = content.find("streamController.enqueue(")
    script_end = content.find("</script>", idx)
    full_call = content[idx:script_end].strip()
    
    arg = full_call[len("streamController.enqueue("):]
    if arg.endswith(";"):
        arg = arg[:-1].strip()
    if arg.endswith(")"):
        arg = arg[:-1].strip()
    
    try:
        decoded_outer = json.loads(arg)
        decoded_inner = json.loads(decoded_outer)
        out_lines.append(f"# ==================== {name} ====================\n\n")
        for item in decoded_inner:
            if isinstance(item, str) and len(item) > 30:
                if not item.startswith("http") and not item.startswith("/cdn") and not item.startswith("text/") and not "uuid" in item:
                    out_lines.append(f"### Content Block\n\n{item}\n\n---\n\n")
    except Exception as e:
        out_lines.append(f"Error for {name}: {e}\n\n")

with open("C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/extracted_chatgpt_convos.md", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Saved successfully to extracted_chatgpt_convos.md")
