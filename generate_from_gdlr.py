import xml.etree.ElementTree as ET
import phpserialize
import json
import re
import os

def convert_bytes(data):
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='ignore')
    if isinstance(data, dict):
        return {convert_bytes(k): convert_bytes(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_bytes(v) for v in data]
    return data

def extract_activity(block_data):
    texts = []
    images = []
    
    def traverse(d):
        if isinstance(d, dict):
            if d.get('type') == 'text-box':
                val = d.get('value', {})
                if 'content' in val:
                    texts.append(val['content'])
            elif d.get('type') == 'gallery':
                val = d.get('value', {})
                if 'gallery' in val:
                    for g_k, g_v in val['gallery'].items():
                        if 'thumbnail' in g_v:
                            # Replace 150x150 with full image URL if possible, but thumbnail is fine
                            img_url = g_v['thumbnail'].replace('-150x150', '')
                            images.append(img_url)
            for k, v in d.items():
                traverse(v)
        elif isinstance(d, list):
            for item in d:
                traverse(item)
                
    traverse(block_data)
    return texts, images

def format_activity(texts, images, prefix, index):
    if not texts and not images:
        return ""
    
    # Combine texts
    raw_html = "".join(texts)
    
    # Parse title and date from text
    # Usually title is in <strong><em> or just the first <p>
    title_match = re.search(r'<strong><em>(.*?)</em></strong>|<strong>(.*?)</strong>|<p>(.*?)</p>', raw_html)
    title = "Faaliyet"
    if title_match:
        title = title_match.group(1) or title_match.group(2) or title_match.group(3)
        # Strip HTML from title
        title = re.sub(r'<[^>]+>', '', title)
        
    date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', raw_html)
    date_str = date_match.group(0) if date_match else ""
    
    # Clean text: remove title part if it's there
    content_html = raw_html
    
    html = f'''                                    <div class="activity-item">
                                        <div class="activity-header">
                                            <h4>{title}</h4>'''
    if date_str:
        html += f'\n                                            <span class="activity-date"><i class="far fa-calendar"></i> {date_str}</span>'
    
    html += f'''
                                        </div>
                                        <div class="activity-content">
                                            {content_html}'''
        
    if images:
        html += '\n                                            <div class="activity-gallery">'
        for j, img in enumerate(images):
            html += f'''
                                                <div class="gallery-item">
                                                    <a href="{img}" data-lightbox="activity-{prefix}-{index}-{j}">
                                                        <img src="{img}" alt="{title}">
                                                    </a>
                                                </div>'''
        html += '\n                                            </div>'
        
    html += '''
                                        </div>
                                    </div>'''
    
    return html

def create_template(filepath, html_formatted, title_text, year_text):
    # Read the base template
    base_filepath = r'd:\avrasya_site\insaat_teknolojisi\templates\insaat_teknolojisi\includes\idari_faaliyetler_2025_2026.html'
    with open(base_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_str = '<div class="tab-container">'
    start_idx = content.find(start_str)
    if start_idx == -1: return

    header_content = content[:start_idx]
    header_content = re.sub(r'<h1>.*?</h1>', f'<h1>İnşaat Teknolojisi_{title_text}</h1>', header_content)
    header_content = re.sub(r'{% block title %}.*?{% endblock %}', f'{{% block title %}}Avrasya Üniversitesi - İnşaat Teknolojisi {title_text}{{% endblock %}}', header_content)

    new_tab_container = f'''<div class="tab-container">
                        <div class="tab-header">
                            <ul class="tab-menu">
                                <li class="tab-menu-item active" data-tab="tab1">
                                    {title_text} ({year_text})
                                </li>
                            </ul>
                        </div>
                        
                        <div class="tab-content-wrapper">
                            <div class="tab-content active" id="tab1">
                                <div class="tab-content-header">
                                    <h3><i class="fas fa-calendar-check"></i> {title_text} ({year_text})</h3>
                                </div>
                                <div class="tab-content-body">
{html_formatted}
                                </div>
                            </div>
                        </div>
                    </div>'''

    css_content = ""
    if '<style>' in content and '</style>' in content:
        css_content = content[content.find('<style>'):content.rfind('</style>')+8]

    new_content = header_content + new_tab_container + "\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n" + css_content + "\n{% endblock %}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

tree = ET.parse(r'D:\avrasya_site\insaat_teknolojisi\avrasyaniversitesi.WordPress.2026-07-23.xml')
root = tree.getroot()
items = root.findall('.//item')
wp_ns = 'http://wordpress.org/export/1.2/'

years = ["2023-2024", "2024-2025", "2025-2026"]
categories = {
    "İdari Faaliyetler": "idari",
    "Diğer Faaliyetler": "diger"
}

base_dir = r'd:\avrasya_site\insaat_teknolojisi\templates\insaat_teknolojisi\includes'

for item in items:
    title_elem = item.find('title')
    if title_elem is not None and title_elem.text and 'Faaliyetler' in title_elem.text:
        title_text = title_elem.text
        
        # Match category
        cat_name = None
        for cn in categories.keys():
            match_word = "dari" if cn == "İdari Faaliyetler" else "Diger"
            match_word2 = "Di" if cn == "Diğer Faaliyetler" else match_word
            if match_word in title_text or match_word2 in title_text:
                cat_name = cn
                break
                
        if not cat_name: continue
        
        # Match year
        year = None
        for y in years:
            if y in title_text:
                year = y
                break
                
        if not year: continue
        
        # We have a matching item!
        for meta in item.findall(f'{{{wp_ns}}}postmeta'):
            key = meta.find(f'{{{wp_ns}}}meta_key')
            if key is not None and key.text == 'gdlr-core-page-builder':
                val = meta.find(f'{{{wp_ns}}}meta_value')
                if val is not None and val.text:
                    parsed = phpserialize.loads(val.text.encode('utf-8'))
                    clean_data = convert_bytes(parsed)
                    
                    html_blocks = []
                    if isinstance(clean_data, dict):
                        idx = 0
                        for k, v in clean_data.items():
                            texts, images = extract_activity(v)
                            html_str = format_activity(texts, images, categories[cat_name], idx)
                            if html_str:
                                html_blocks.append(html_str)
                                idx += 1
                                
                    final_html = "\n                                    <div class=\"divider-line\"></div>\n".join(html_blocks)
                    
                    file_name = f"{categories[cat_name]}_faaliyetler_{year.replace('-', '_')}.html"
                    file_path = os.path.join(base_dir, file_name)
                    create_template(file_path, final_html, cat_name, year)
                    print(f"Generated {file_name}")

print("Done.")
