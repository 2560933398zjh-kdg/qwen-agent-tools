# 彻底清理 generate_5screen_app.py 中的旧代码
import re
path = r'd:\pycharm\Qwen\appinventor\generate_5screen_app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到所有 def build_bky_screen 定义
s3_new = None
s4_def = None
s5_def = None

# 找到 build_bky_screen3 和 build_bky_screen4 的 def 位置
for m in re.finditer(r'def build_bky_screen(\d)', content):
    num = int(m.group(1))
    pos = m.start()
    line = content[:pos].count('\n') + 1
    with open(r'd:\pycharm\Qwen\appinventor\_clean_result.txt', 'a', encoding='utf-8') as f:
        f.write(f"build_bky_screen{num} at pos {pos}, line {line}\n")
    if num == 3:
        s3_new = pos
    elif num == 4:
        s4_def = pos
    elif num == 5:
        s5_def = pos

# 找到"return ''.join(p)" - 新Screen3的返回
rp = None
for m in re.finditer(r"return\s+''\.join\(p\)", content):
    rp = m.start()

# 找到所有 "return ''.join(xml)"
rx = []
for m in re.finditer(r"return\s+''\.join\(xml\)", content):
    rx.append(m.end())

with open(r'd:\pycharm\Qwen\appinventor\_clean_result.txt', 'a', encoding='utf-8') as f:
    f.write(f"\ns3_new={s3_new}, s4_def={s4_def}, s5_def={s5_def}\n")
    f.write(f"'return ''.join(p)' at {rp}\n")
    f.write(f"'return ''.join(xml)' ends at: {rx}\n")

# 思路：新 Screen3 以 "return ''.join(p)" 结尾
# 旧代码从这个 return 之后到 s4_def 之前
# 新的部分: content[:rp+len("return ''.join(p)")] + content[s4_def:]

if rp and s4_def:
    # rp is the start of "return ''.join(p)"
    return_end = rp + len("return ''.join(p)")
    new_content = content[:return_end] + content[s4_def:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    with open(r'd:\pycharm\Qwen\appinventor\_clean_result.txt', 'a', encoding='utf-8') as f:
        f.write(f"\nCleaned! {len(content)} -> {len(new_content)} chars\n")
    print("DONE")
else:
    with open(r'd:\pycharm\Qwen\appinventor\_clean_result.txt', 'a', encoding='utf-8') as f:
        f.write("\nFAILED to find markers\n")
    print("FAILED")
