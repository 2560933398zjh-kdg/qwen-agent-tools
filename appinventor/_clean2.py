import re, sys
path = r'd:\pycharm\Qwen\appinventor\generate_5screen_app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find "return ''.join(p)" - there should be only 1
matches_p = list(re.finditer(r"return\s+''\.join\(p\)", content))
print(f"'return ''.join(p)' matches: {len(matches_p)}")
for m in matches_p:
    print(f"  pos {m.start()}: line {content[:m.start()].count(chr(10))+1}")

# Find "def build_bky_screen4"
matches_s4 = list(re.finditer(r"def build_bky_screen4", content))
print(f"\n'def build_bky_screen4' matches: {len(matches_s4)}")
for m in matches_s4:
    print(f"  pos {m.start()}: line {content[:m.start()].count(chr(10))+1}")

# Find the old Screen3 code ending "return ''.join(xml)" before Screen4
matches_xml = list(re.finditer(r"return\s+''\.join\(xml\)", content))
print(f"\n'return ''.join(xml)' matches: {len(matches_xml)}")
for m in matches_xml:
    print(f"  pos {m.start()}: line {content[:m.start()].count(chr(10))+1}")

# Do the cleanup
if matches_p and matches_s4:
    s3_end = matches_p[-1].end()
    s4_start = matches_s4[0].start()
    # But we want to also keep "return ''.join(p)" so use start of next content
    # Actually s3_end is already after the return statement
    
    # Check what's between
    between = content[s3_end:s4_start]
    print(f"\nBetween chars: {len(between)}")
    print(f"First 200 chars of between:\n{between[:200]}")
    
    new_content = content[:s3_end] + content[s4_start:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\nDone! {len(content)} -> {len(new_content)}")
else:
    print("ERROR: Missing markers")
