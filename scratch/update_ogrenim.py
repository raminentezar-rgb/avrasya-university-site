import os
import re

html_path = r'd:\avrasya_site\ogrenci_isleri\templates\ogrenci_isleri\includes\ogrenim_ucretleri.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title and Headers
content = content.replace('2025 YKS Eğitim Ücretleri', '2026-2027 EĞİTİM ÜCRETLERİ')
content = content.replace('2025-2026 EĞİTİM-ÖĞRETİM YILI YENİ KAYIT EĞİTİM ÜCRETLERİ', '2026-2027 EĞİTİM VE ÖĞRETİM YILI EĞİTİM ÜCRETLERİ')

# Info cards update
content = re.sub(r'(<p id="totalProgramsCount">\{% trans ")[^"]+(" %\}</p>)', r'\g<1>63 Program\g<2>', content)
content = content.replace('%10 İlk 3 Tercih', 'Yok (Yeni Bölümler Hariç)')

# Faculty filter options update
content = content.replace('Fen Edebiyat Fakültesi', 'İnsan ve Toplum Bilimleri Fakültesi')
content = content.replace('Mühendislik ve Mimarlık Fakültesi', 'Mühendislik ve Doğa Bilimleri Fakültesi')

# Table Header Update
table_header = """                                        <tr>
                                            <th width="30%">{% trans "Fakülte / Yüksekokul" %}</th>
                                            <th width="40%">{% trans "Bölüm / Program" %}</th>
                                            <th width="15%">{% trans "Tam Ücret" %}</th>
                                            <th width="15%">{% trans "%50 İndirimli" %}</th>
                                        </tr>"""

content = re.sub(r'<tr>\s*<th width="25%">\{% trans "Fakülte / Yüksekokul".*?</tr>', table_header, content, flags=re.DOTALL)


# Data from PDF
data = [
    # İnsan ve Toplum Bilimleri Fakültesi
    ("İnsan ve Toplum Bilimleri Fakültesi", "İngiliz Dili ve Edebiyatı", "275,000.00 ₺", "137,500.00 ₺"),
    ("İnsan ve Toplum Bilimleri Fakültesi", "İngilizce Mütercim ve Tercümanlık", "275,000.00 ₺", "137,500.00 ₺"),
    ("İnsan ve Toplum Bilimleri Fakültesi", "Psikoloji", "308,000.00 ₺", "-"),
    ("İnsan ve Toplum Bilimleri Fakültesi", "Türk Dili ve Edebiyatı", "-", "137,500.00 ₺"),

    # İktisadi ve İdari Bilimler Fakültesi
    ("İktisadi ve İdari Bilimler Fakültesi", "İşletme (İngilizce)", "-", "110,000.00 ₺"),
    ("İktisadi ve İdari Bilimler Fakültesi", "Siyaset Bilimi ve Kamu Yönetimi", "275,000.00 ₺", "137,500.00 ₺"),

    # İletişim Fakültesi
    ("İletişim Fakültesi", "Görsel İletişim Tasarımı", "-", "99,000.00 ₺"),
    ("İletişim Fakültesi", "Yeni Medya Ve İletişim", "-", "99,000.00 ₺"),

    # Mühendislik ve Doğa Bilimleri Fakültesi
    ("Mühendislik ve Doğa Bilimleri Fakültesi", "Bilgisayar Mühendisliği", "275,000.00 ₺", "137,500.00 ₺"),
    ("Mühendislik ve Doğa Bilimleri Fakültesi", "Moleküler Biyoloji ve Genetik", "308,000.00 ₺", "154,000.00 ₺"),
    ("Mühendislik ve Doğa Bilimleri Fakültesi", "İç Mimarlık ve Çevre Tasarımı", "308,000.00 ₺", "154,000.00 ₺"),
    ("Mühendislik ve Doğa Bilimleri Fakültesi", "İnşaat Mühendisliği", "-", "0,00 ₺ (Burslu)"),
    ("Mühendislik ve Doğa Bilimleri Fakültesi", "Mimarlık", "-", "0,00 ₺ (Burslu)"),

    # Sağlık Bilimleri Fakültesi
    ("Sağlık Bilimleri Fakültesi", "Beslenme ve Diyetetik", "275,000.00 ₺", "137,500.00 ₺"),
    ("Sağlık Bilimleri Fakültesi", "Çocuk Gelişimi", "275,000.00 ₺", "137,500.00 ₺"),
    ("Sağlık Bilimleri Fakültesi", "Ebelik", "308,000.00 ₺", "-"),
    ("Sağlık Bilimleri Fakültesi", "Ergoterapi", "275,000.00 ₺", "137,500.00 ₺"),
    ("Sağlık Bilimleri Fakültesi", "Fizyoterapi ve Rehabilitasyon", "275,000.00 ₺", "137,500.00 ₺"),
    ("Sağlık Bilimleri Fakültesi", "Hemşirelik", "308,000.00 ₺", "-"),
    ("Sağlık Bilimleri Fakültesi", "Odyoloji", "-", "137,500.00 ₺"),

    # Spor Bilimleri Fakültesi
    ("Spor Bilimleri Fakültesi", "Antrenörlük Eğitimi", "-", "99,000.00 ₺"),
    ("Spor Bilimleri Fakültesi", "Egzersiz ve Spor Bilimleri", "-", "99,000.00 ₺"),
    ("Spor Bilimleri Fakültesi", "Rekreasyon", "-", "99,000.00 ₺"),
    ("Spor Bilimleri Fakültesi", "Spor Yöneticiliği", "-", "99,000.00 ₺"),

    # Uygulamalı Bilimler Yüksekokulu
    ("Uygulamalı Bilimler Yüksekokulu", "Gastronomi ve Mutfak Sanatları", "275,000.00 ₺", "137,500.00 ₺"),
    ("Uygulamalı Bilimler Yüksekokulu", "Yönetim Bilişim Sistemleri", "-", "137,500.00 ₺"),

    # Meslek Yüksekokulu
    ("Meslek Yüksekokulu", "Aşçılık", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "Bilgisayar Programcılığı", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "Bilişim Güvenliği Teknolojisi", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "Dış Ticaret", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "E-Ticaret ve Pazarlama", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Elektrik", "154,000.00 ₺", "İlk 5 Tercihe %30 İndirim: 107,800.00 ₺"),
    ("Meslek Yüksekokulu", "Halkla İlişkiler ve Tanıtım", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Harita ve Kadastro", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "İç Mekan Tasarımı", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "İnşaat Teknolojisi", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Lojistik", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Mahkeme Büro Hizmetleri", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Mimari Restorasyon", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "Moda Tasarımı", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Mekatronik", "154,000.00 ₺", "İlk 5 Tercihe %30 İndirim: 107,800.00 ₺"),
    ("Meslek Yüksekokulu", "Otomotiv Teknolojisi", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "Sivil Havacılık Kabin Hizmetleri", "198,000.00 ₺", "99,000.00 ₺"),
    ("Meslek Yüksekokulu", "Sosyal Hizmetler", "154,000.00 ₺", "77,000.00 ₺"),
    ("Meslek Yüksekokulu", "Web Tasarımı ve Kodlama", "198,000.00 ₺", "99,000.00 ₺"),

    # Sağlık Hizmetleri Meslek Yüksekokulu
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Ağız ve Diş Sağlığı", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Ameliyathane Hizmetleri", "220,000.00 ₺", "-"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Anestezi", "220,000.00 ₺", "-"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Çocuk Gelişimi", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Diş Protez Teknolojisi", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Diyaliz", "220,000.00 ₺", "110,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Eczane Hizmetleri", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Elektronörofizyoloji", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Fizyoterapi", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "İlk ve Acil Yardım", "220,000.00 ₺", "-"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "İş ve Uğraşı Terapisi", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Odyometri", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Optisyenlik", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Ortopedik Protez ve Ortez", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Patoloji Laboratuvar Teknikleri", "198,000.00 ₺", "99,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Radyoterapi", "220,000.00 ₺", "110,000.00 ₺"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Tıbbi Görüntüleme Teknikleri", "220,000.00 ₺", "-"),
    ("Sağlık Hizmetleri Meslek Yüksekokulu", "Tıbbi Laboratuvar Teknikleri", "198,000.00 ₺", "99,000.00 ₺"),
]

tbody_content = []
for fac, dep, full, disc in data:
    tr = f'''                                        <tr>
                                            <td>{{% trans "{fac}" %}}</td>
                                            <td><span class="program-name">{{% trans "{dep}" %}}</span></td>
                                            <td class="price{" empty" if full == "-" else ""}">{full}</td>
                                            <td class="price{" empty" if disc == "-" else " discount"}">{disc}</td>
                                        </tr>'''
    tbody_content.append(tr)

new_tbody = '<tbody id="tuitionTableBody">\n' + '\n'.join(tbody_content) + '\n                                    </tbody>'
content = re.sub(r'<tbody id="tuitionTableBody">.*?</tbody>', new_tbody, content, flags=re.DOTALL)

# Clean up legend (remove the %10 tercih indirimli star part)
legend_html = """                                <div class="legend">
                                    <div class="legend-item">
                                        <span class="legend-color discount-color"></span>
                                        <span>{% trans "%50 İndirimli" %}</span>
                                    </div>
                                    <div class="legend-item">
                                        <span class="legend-color" style="background-color: #f1c40f;"></span>
                                        <span>{% trans "%30 Tercih İndirimi (Yeni Bölümler İçin İlk 5 Tercih)" %}</span>
                                    </div>
                                    <div class="legend-item">
                                        <span class="legend-color" style="background-color: #27ae60;"></span>
                                        <span>{% trans "Burslu (Ücretsiz)" %}</span>
                                    </div>
                                    <div class="legend-item">
                                        <span class="legend-color" style="background-color: #c0392b;"></span>
                                        <span>{% trans "Burslu ve Ücretli Kontenjan" %}</span>
                                    </div>
                                </div>"""

content = re.sub(r'<div class="legend">.*?</div>\s*<div class="table-summary">', legend_html + '\n                                <div class="table-summary">', content, flags=re.DOTALL)
content = content.replace('(35 program tercih indirimine uygundur)', '(Sadece yeni açılan bölümlere tercih indirimi uygulanmaktadır)')
content = content.replace('48 program', '63 program')
content = content.replace('48 Program', '63 Program')
content = content.replace('35 İndirimli', 'Yeni Bölümler Hariç Tercih İndirimi Yoktur')


with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Update completed successfully!")
