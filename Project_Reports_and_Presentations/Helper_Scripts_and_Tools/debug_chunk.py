with open("C:/Users/SABARIKARTHICK/.gemini/antigravity-ide/brain/7697093a-88a1-4803-af1d-abc0bc619ef6/.system_generated/steps/581/content.md", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("streamController.enqueue(")
print("idx:", idx)
sub = content[idx:idx+200]
print("First 200 chars:", repr(sub))

# Find the matching closing parenthesis or </script>
script_end = content.find("</script>", idx)
print("script_end:", script_end)
full_call = content[idx:script_end].strip()
print("full_call length:", len(full_call))
print("Last 100 chars:", repr(full_call[-100:]))
