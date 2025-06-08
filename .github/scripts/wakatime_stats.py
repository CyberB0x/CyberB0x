import requests
import os

api_key = os.getenv('WAKATIME_API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}

# Получаем всю статистику
resp = requests.get('https://wakatime.com/api/v1/users/current/stats/all_time', headers=headers)
data = resp.json().get('data', {})
languages = data.get('languages', [])
editors = data.get('editors', [])

# Блоки в README
block_start_lang = '<!--START_SECTION:waka-->'
block_end_lang = '<!--END_SECTION:waka-->'
block_start_ide = '<!--START_SECTION:ide-->'
block_end_ide = '<!--END_SECTION:ide-->'

# ЯЗЫКИ
lang_lines = [f"| Язык | Время |", "|------|-------|"]
for lang in languages[:10]:
    lang_lines.append(f"| {lang['name']} | {lang['text']} |")
lang_block = f"{block_start_lang}\n" + '\n'.join(lang_lines) + f"\n{block_end_lang}"

# IDE
ide_lines = [f"| Редактор (IDE) | Время |", "|----------------|--------|"]
for ide in editors:
    ide_lines.append(f"| {ide['name']} | {ide['text']} |")
ide_block = f"{block_start_ide}\n" + '\n'.join(ide_lines) + f"\n{block_end_ide}"

# Чтение README
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# Обновление блоков
def replace_block(content, start, end, new_block):
    s = content.find(start)
    e = content.find(end)
    if s != -1 and e != -1:
        return content[:s] + new_block + content[e + len(end):]
    return content + '\n\n' + new_block

updated = readme
updated = replace_block(updated, block_start_lang, block_end_lang, lang_block)
updated = replace_block(updated, block_start_ide, block_end_ide, ide_block)

# Запись
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(updated)
