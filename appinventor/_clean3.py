import re
path = r'd:\pycharm\Qwen\appinventor\generate_5screen_app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

log = []
log.append(f"File size: {len(content)} chars, {content.count(chr(10))+1} lines")

matches_p = list(re.finditer(r"return\s+''\.join\(p\)", content))
log.append(f"'return ''.join(p)': {len(matches_p)}")
for m in matches_p:
    log.append(f"  pos {m.start()} line {content[:m.start()].count(chr(10))+1}")

matches_s4 = list(re.finditer(r"def build_bky_screen4", content))
log.append(f"'def build_bky_screen4': {len(matches_s4)}")
for m in matches_s4:
    log.append(f"  pos {m.start()} line {content[:m.start()].count(chr(10))+1}")

# Show lines around the first "return ''.join(p)"
for m in matches_p:
    line_num = content[:m.start()].count('\n') + 1
    lines = content.split('\n')
    start = max(0, line_num - 3)
    end = min(len(lines), line_num + 3)
    log.append(f"\nContext around line {line_num}:")
    for i in range(start, end):
        log.append(f"  {i+1}: {lines[i]}")
    break

with open(r'd:\pycharm\Qwen\appinventor\_clean_log.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print("Log written")
