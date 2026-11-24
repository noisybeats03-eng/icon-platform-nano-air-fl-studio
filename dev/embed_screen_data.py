import sys, re
html_path, json_path = sys.argv[1], sys.argv[2]
html = open(html_path, encoding='utf-8').read()
data = open(json_path, encoding='utf-8').read().strip()
assert '/*SCR*/' in html and '/*SCR-END*/' in html
html = re.sub(r'/\*SCR\*/.*?/\*SCR-END\*/', lambda m: '/*SCR*/' + data + '/*SCR-END*/', html, count=1, flags=re.S)
open(html_path, 'w', encoding='utf-8', newline='\n').write(html)
print('embedded', len(data), 'bytes of screen data; page', len(html.encode('utf-8')), 'bytes')
