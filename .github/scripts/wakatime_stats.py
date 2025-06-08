import requests
import os

api_key = os.getenv('WAKATIME_API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}

resp = requests.get('https://wakatime.com/api/v1/users/current/stats/all_time', headers=headers)
data = resp.json().get('data', {})
languages = data.get('languages', [])

block_start = '<!--START_SECTION:waka-->'
block_end = '<!--END_SECTION:waka-->'
stats_lines = [f"| Язык | Время |", "|------|-------|"]

for lang in languages[:10]:  # топ-10 языков
    stats_lines.append(f"| {lang['name']} | {lang['text']} |")

new_stats = f"{block_start}\n" + '\n'.join(stats_lines) + f"\n{block_end}"

# обновляем README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

start = readme.find(block_start)
end = readme.find(block_end)

if start != -1 and end != -1:
    updated = readme[:start] + new_stats + readme[end + len(block_end):]
else:
    updated = readme + '\n\n' + new_stats

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(updated)

