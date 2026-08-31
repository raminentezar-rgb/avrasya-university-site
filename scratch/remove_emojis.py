import os
import re

# Comprehensive map of emojis to FontAwesome icons
emoji_map = {
    '📌': '<i class="fas fa-thumbtack"></i> ',
    '🔍': '<i class="fas fa-search"></i> ',
    '💰': '<i class="fas fa-coins"></i> ',
    '💳': '<i class="fas fa-credit-card"></i> ',
    '🏦': '<i class="fas fa-university"></i> ',
    '📞': '<i class="fas fa-phone-alt"></i> ',
    '⚠️': '<i class="fas fa-exclamation-triangle"></i> ',
    '❗': '<i class="fas fa-exclamation-circle"></i> ',
    '🎓': '<i class="fas fa-graduation-cap"></i> ',
    '🏫': '<i class="fas fa-school"></i> ',
    '🏢': '<i class="fas fa-building"></i> ',
    '📊': '<i class="fas fa-chart-bar"></i> ',
    '📋': '<i class="fas fa-clipboard-list"></i> ',
    '📝': '<i class="fas fa-edit"></i> ',
    '📅': '<i class="fas fa-calendar-alt"></i> ',
    '📈': '<i class="fas fa-chart-line"></i> ',
    '👥': '<i class="fas fa-users"></i> ',
    '🌍': '<i class="fas fa-globe"></i> ',
    '🏆': '<i class="fas fa-trophy"></i> ',
    '💡': '<i class="fas fa-lightbulb"></i> ',
    '✈️': '<i class="fas fa-plane"></i> ',
    '🤝': '<i class="fas fa-handshake"></i> ',
    '📚': '<i class="fas fa-book"></i> ',
    '📍': '<i class="fas fa-map-marker-alt"></i> ',
    '✅': '<i class="fas fa-check-circle"></i> ',
    '❌': '<i class="fas fa-times-circle"></i> ',
    'ℹ️': '<i class="fas fa-info-circle"></i> ',
    '🌟': '<i class="fas fa-star"></i> ',
    '🎯': '<i class="fas fa-bullseye"></i> ',
    '⚖️': '<i class="fas fa-balance-scale"></i> ',
    '🚀': '<i class="fas fa-rocket"></i> ',
    '🔔': '<i class="fas fa-bell"></i> ',
    '🔒': '<i class="fas fa-lock"></i> ',
    '💼': '<i class="fas fa-briefcase"></i> ',
    '💻': '<i class="fas fa-laptop"></i> ',
    '📱': '<i class="fas fa-mobile-alt"></i> ',
    '✉️': '<i class="fas fa-envelope"></i> ',
    '⚙️': '<i class="fas fa-cog"></i> ',
    '🔧': '<i class="fas fa-wrench"></i> ',
    '🛠️': '<i class="fas fa-tools"></i> ',
    '🔬': '<i class="fas fa-microscope"></i> ',
    '🧬': '<i class="fas fa-dna"></i> ',
    '🏥': '<i class="fas fa-hospital"></i> ',
    '🚑': '<i class="fas fa-ambulance"></i> ',
    '🩺': '<i class="fas fa-stethoscope"></i> ',
    '💊': '<i class="fas fa-pills"></i> ',
    '🎨': '<i class="fas fa-palette"></i> ',
    '🎭': '<i class="fas fa-masks-theater"></i> ',
    '🎬': '<i class="fas fa-film"></i> ',
    '📷': '<i class="fas fa-camera"></i> ',
    '🎵': '<i class="fas fa-music"></i> ',
    '🏃': '<i class="fas fa-running"></i> ',
    '⚽': '<i class="fas fa-futbol"></i> ',
    '🏀': '<i class="fas fa-basketball-ball"></i> ',
    '🏅': '<i class="fas fa-medal"></i> ',
    '🌱': '<i class="fas fa-seedling"></i> ',
    '🌳': '<i class="fas fa-tree"></i> ',
    '🍔': '<i class="fas fa-hamburger"></i> ',
    '☕': '<i class="fas fa-coffee"></i> ',
    '🍽️': '<i class="fas fa-utensils"></i> ',
    '🏠': '<i class="fas fa-home"></i> ',
    '🔑': '<i class="fas fa-key"></i> ',
    '🛒': '<i class="fas fa-shopping-cart"></i> ',
    '🏷️': '<i class="fas fa-tag"></i> ',
    '🎁': '<i class="fas fa-gift"></i> ',
    '🎉': '<i class="fas fa-tada"></i> ',
    '✨': '<i class="fas fa-sparkles"></i> ',
    '🔥': '<i class="fas fa-fire"></i> ',
    '💧': '<i class="fas fa-tint"></i> ',
    '⚡': '<i class="fas fa-bolt"></i> ',
    '🌞': '<i class="fas fa-sun"></i> ',
    '🌙': '<i class="fas fa-moon"></i> ',
    '⭐': '<i class="fas fa-star"></i> ',
    '🌈': '<i class="fas fa-rainbow"></i> ',
    '❤️': '<i class="fas fa-heart"></i> ',
    '👍': '<i class="fas fa-thumbs-up"></i> ',
    '👇': '<i class="fas fa-hand-point-down"></i> ',
    '👉': '<i class="fas fa-hand-point-right"></i> ',
    '👈': '<i class="fas fa-hand-point-left"></i> ',
    '👆': '<i class="fas fa-hand-point-up"></i> ',
    '💬': '<i class="fas fa-comment"></i> ',
    '🧠': '<i class="fas fa-brain"></i> ',
    '👁️': '<i class="fas fa-eye"></i> ',
    '🗣️': '<i class="fas fa-bullhorn"></i> ',
    '📝': '<i class="fas fa-file-signature"></i> ',
    '🧾': '<i class="fas fa-receipt"></i> ',
    '📁': '<i class="fas fa-folder"></i> ',
    '📂': '<i class="fas fa-folder-open"></i> ',
    '🔗': '<i class="fas fa-link"></i> ',
    '🔖': '<i class="fas fa-bookmark"></i> ',
    '🛡️': '<i class="fas fa-shield-alt"></i> ',
    '⚔️': '<i class="fas fa-khanda"></i> ',
    '🏁': '<i class="fas fa-flag-checkered"></i> ',
    '🚩': '<i class="fas fa-flag"></i> ',
    '🎌': '<i class="fas fa-flags"></i> ',
    '🥇': '<i class="fas fa-medal"></i> ',
    '🥈': '<i class="fas fa-medal"></i> ',
    '🥉': '<i class="fas fa-medal"></i> '
}

# Regex to match emojis (simple unicode ranges)
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\u2702-\u27B0"          # Dingbats
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "]+", flags=re.UNICODE)

def replace_emojis():
    base_dir = r"d:\avrasya_site"
    for root, dirs, files in os.walk(base_dir):
        if "Env" in root or ".git" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # First, replace known emojis with their FontAwesome equivalents
                for emoji_char, icon_html in emoji_map.items():
                    if emoji_char in content:
                        # Replace inside trans tags
                        pattern1 = r'\{%\s*trans\s*"([^"]*)' + emoji_char + r'([^"]*)"\s*%\}'
                        def repl1(m):
                            text = m.group(1) + m.group(2)
                            return f'{icon_html}{{% trans "{text.strip()}" %}}'
                        content = re.sub(pattern1, repl1, content)
                        
                        pattern2 = r"\{%\s*trans\s*'([^']*)" + emoji_char + r"([^']*)'\s*%\}"
                        def repl2(m):
                            text = m.group(1) + m.group(2)
                            return f"{icon_html}{{% trans '{text.strip()}' %}}"
                        content = re.sub(pattern2, repl2, content)
                        
                        # Replace standalone emojis
                        content = content.replace(emoji_char, icon_html)
                
                # Next, find any remaining emojis in trans tags and remove them
                def remove_emojis_from_match(m):
                    text = m.group(0)
                    cleaned_text = emoji_pattern.sub('', text)
                    return cleaned_text
                
                content = re.sub(r'\{%\s*trans\s*"[^"]*"\s*%\}', remove_emojis_from_match, content)
                content = re.sub(r"\{%\s*trans\s*'[^']*'\s*%\}", remove_emojis_from_match, content)
                
                # Finally, remove any remaining emojis from the file
                content = emoji_pattern.sub('', content)
                
                # Clean up empty trans tags or tags with just spaces
                content = re.sub(r'\{%\s*trans\s*""\s*%\}', '', content)
                content = re.sub(r"\{%\s*trans\s*''\s*%\}", '', content)
                
                if content != original_content:
                    print(f"Removed emojis from {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    replace_emojis()
