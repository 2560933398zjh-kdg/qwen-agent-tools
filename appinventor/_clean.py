# Clean up old Screen3 code and rewrite Screen4/Screen5 BKY functions
import os, random, string as _st, uuid as _u

path = r'd:\pycharm\Qwen\appinventor\generate_5screen_app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the marker: new Screen3 ends with "return ''.join(p)" followed by old code
# The pattern is: the FIRST "return ''.join(p)" after our new code
# The new code has: p.append('</xml>') then return ''.join(p)

# Find all positions of "return ''.join(p)"
import re
matches = list(re.finditer(r"return\s+''\.join\(p\)", content))
print(f"Found {len(matches)} 'return ''.join(p)' matches")
for i, m in enumerate(matches):
    ctx = content[m.start():m.start()+100].replace('\n',' ')
    print(f"  [{i}] at pos {m.start()}: ...{ctx}...")

# Find all positions of "def build_bky_screen4"
s4_matches = list(re.finditer(r"def build_bky_screen4", content))
print(f"\nFound {len(s4_matches)} 'def build_bky_screen4' matches")
for i, m in enumerate(s4_matches):
    print(f"  [{i}] at pos {m.start()}")

if len(matches) >= 1 and len(s4_matches) >= 1:
    # The last "return ''.join(p)" is the new one
    s3_end = matches[-1].end()  # end of return ''.join(p)
    s4_start = s4_matches[0].start()
    
    print(f"\nScreen3 new code ends at pos {s3_end}")
    print(f"Screen4 def starts at pos {s4_start}")
    print(f"Old code between: {s4_start - s3_end} chars")
    
    # Build new content: everything up to s3_end + everything from s4_start
    new_content = content[:s3_end] + content[s4_start:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Cleaned! Old size: {len(content)}, New size: {len(new_content)}")
else:
    print("ERROR: Could not find expected markers")
