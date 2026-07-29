import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

def process_html(html_content, prefix="idari"):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    blocks = soup.find_all('div', class_=re.compile(r'(toplanti-blok|etkinlik-blok|faaliyet-blok|sergi-blok)'))
    
    output = []
    
    for i, block in enumerate(blocks):
        title_tag = block.find(['h2', 'h3', 'h4'])
        title = title_tag.text.strip() if title_tag else "Faaliyet"
        
        # Extract date from text if possible
        date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', block.text)
        date_str = date_match.group(0) if date_match else "2025-2026"
        
        text_tags = block.find_all('p')
        texts = [p.text.strip() for p in text_tags if p.text.strip()]
        
        images = []
        img_tags = block.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            if src:
                images.append(src)
                
        # Build the HTML
        html = f'''                                    <div class="activity-item">
                                        <div class="activity-header">
                                            <h4>{title}</h4>
                                            <span class="activity-date"><i class="far fa-calendar"></i> {date_str}</span>
                                        </div>
                                        <div class="activity-content">'''
        
        for text in texts:
            html += f'\n                                            <p>{text}</p>'
            
        if images:
            html += '\n                                            <div class="activity-gallery">'
            for j, img in enumerate(images):
                html += f'''
                                                <div class="gallery-item">
                                                    <a href="{img}" data-lightbox="activity-{prefix}-{i}-{j}">
                                                        <img src="{img}" alt="{title}">
                                                    </a>
                                                </div>'''
            html += '\n                                            </div>'
            
        html += '''
                                        </div>
                                    </div>'''
        
        if i < len(blocks) - 1:
            html += '\n                                    <div class="divider-line"></div>\n'
            
        output.append(html)
        
    return '\n'.join(output)

def update_template(filepath, html_formatted, title_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_str = '<div class="tab-container">'
    end_str = '</div>\n                </div>\n            </div>\n        </div>\n    </div>\n</div>'
    
    start_idx = content.find(start_str)
    
    # We will just replace everything after start_idx
    if start_idx == -1:
        print(f"Error finding boundaries in {filepath}")
        return

    new_tab_container = f'''<div class="tab-container">
                        <div class="tab-header">
                            <ul class="tab-menu">
                                <li class="tab-menu-item active" data-tab="tab1">
                                    {title_text} (2025-2026)
                                </li>
                            </ul>
                        </div>
                        
                        <div class="tab-content-wrapper">
                            <div class="tab-content active" id="tab1">
                                <div class="tab-content-header">
                                    <h3><i class="fas fa-calendar-check"></i> {title_text} (2025-2026)</h3>
                                </div>
                                <div class="tab-content-body">
{html_formatted}
                                </div>
                            </div>
                        </div>
                    </div>'''

    # Read CSS from the insaat_teknolojisi template
    css_content = ""
    try:
        with open(r'd:\avrasya_site\insaat_teknolojisi\templates\insaat_teknolojisi\includes\idari_faaliyetler_2024_2025.html', 'r', encoding='utf-8') as insaat_f:
            insaat_content = insaat_f.read()
            if '<style>' in insaat_content and '</style>' in insaat_content:
                css_content = insaat_content[insaat_content.find('<style>'):insaat_content.rfind('</style>')+8]
    except Exception as e:
        print(f"Failed to read CSS: {e}")

    new_content = content[:start_idx] + new_tab_container + "\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n" + css_content + "\n{% endblock %}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# 1. Parse XML and find the correct keys (containing Faaliyetler)
tree = ET.parse(r'd:\avrasya_site\ic_mekan\avrasyaniversitesi.WordPress.2026-07-23.xml')
root = tree.getroot()
items = root.findall('.//item')
ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}

idari_html = ''
diger_html = ''

for item in items:
    title_elem = item.find('title')
    if title_elem is not None and title_elem.text:
        title = title_elem.text
        if 'Faaliyetler' in title and '2025-2026' in title:
            content_elem = item.find('content:encoded', ns)
            if content_elem is not None:
                if 'dari' in title:
                    idari_html = content_elem.text
                elif 'Diger' in title or 'Di' in title:
                    diger_html = content_elem.text

print("Idari length:", len(idari_html))
print("Diger length:", len(diger_html))

idari_formatted = process_html(idari_html, "idari")
diger_formatted = process_html(diger_html, "diger")

idari_path = r'd:\avrasya_site\ic_mekan\templates\ic_mekan\includes\idari_faaliyetler_2024_2025.html'
diger_path = r'd:\avrasya_site\ic_mekan\templates\ic_mekan\includes\diger_faaliyetler_2024_2025.html'

update_template(idari_path, idari_formatted, "İdari Faaliyetler")
update_template(diger_path, diger_formatted, "Diğer Faaliyetler")

print("Templates updated successfully.")
