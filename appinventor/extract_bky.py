import zipfile
with zipfile.ZipFile(r'd:\pycharm\Qwen\appinventor\SmartAI.aia', 'r') as z:
    data = z.read('src/appinventor/ai_user/SmartAI/Screen4.bky')
with open(r'd:\pycharm\Qwen\appinventor\_screen4.bky', 'wb') as f:
    f.write(data)
print('extracted', len(data), 'bytes')
