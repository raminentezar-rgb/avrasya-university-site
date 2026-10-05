import os

html_path = r'd:\avrasya_site\ogrenci_isleri\templates\ogrenci_isleri\includes\kayit.html'

new_content = """{% extends 'ogrenci_isleri/base.html' %}
{% load static %}
{% load i18n %}
{% block title %}{% trans "Avrasya Üniversitesi - Kayıt İşlemleri" %}{% endblock %}

{% block content %}

<!-- Hero Section -->
<section class="research-hero">
    <div class="container">
        <div class="research-hero-content">
            <h1>{% trans "Kayıt İşlemleri" %}</h1>
            <p></p>
        </div>
    </div>
</section>

<div class="container-fluid main-container">
    <div class="row g-4">
        <!-- سایدبار سمت چپ -->
        <div class="col-lg-3 col-xxl-2">
            <div class="sidebar-wrapper">
                {% include 'ogrenci_isleri/orenci_sidebar.html' %}
            </div>
        </div>
        
        <!-- محتوای اصلی -->
        <div class="col-lg-9 col-xxl-10">
            <div class="content-wrapper">
                <div class="page-intro">
                    <h1 class="section-title">{% trans "Kayıt İşlemleri" %}</h1>
                    <p class="section-subtitle">{% trans "Avrasya Üniversitesi'ne hoş geldiniz. Kayıt işlemleriniz için gerekli tüm bilgiler ve belgeler bu sayfada bulunmaktadır." %}</p>
                </div>
                
                <!-- تب‌ها برای بخش‌های مختلف -->
                <div class="ogrenci-isleri-tab-section">
                    <div class="tab-container">
                        <div class="tab-header">
                            <ul class="tab-menu">
                                <li class="tab-menu-item active" data-tab="tab-1">
                                    <i class="fas fa-user-graduate"></i> {% trans "Kayıt İşlemleri" %}
                                </li>
                                <li class="tab-menu-item" data-tab="tab-2">
                                    <i class="fas fa-file-alt"></i> {% trans "Gerekli Belgeler" %}
                                </li>
                                <li class="tab-menu-item" data-tab="tab-3">
                                    <i class="fas fa-credit-card"></i> {% trans "Ödeme Koşulları" %}
                                </li>
                            </ul>
                        </div>
                        
                        <div class="tab-content-wrapper">
                            <!-- تب 1: Kayıt İşlemleri -->
                            <div id="tab-1" class="tab-content active">
                                <div class="tab-content-header">
                                    <h3><i class="fas fa-user-graduate"></i> {% trans "2026 YKS Kayıt İşlemleri" %}</h3>
                                </div>
                                <div class="tab-content-body">
                                    <h4 style="color: var(--primary-dark-blue); margin-bottom: 25px;">
                                        {% trans "Sevgili Öğrencimiz, Avrasya Üniversitesi ailesine hoş geldiniz." %}
                                    </h4>
                                    
                                    <div class="highlight-box">
                                        <h4><i class="fas fa-laptop"></i> {% trans "1- Elektronik Kayıt (E-devlet):" %}</h4>
                                        <p>{% trans "Üniversitemize 2026-YKS ile yerleşen öğrenciler kayıt işlemlerini <strong>24.08.2026-26.08.2026</strong> tarihleri arasında e-devlet üzerinden yapabileceklerdir. (İndirimli veya Ücretli kontenjandan yerleşen öğrencilerimiz yıllık eğitim ücretinin tamamını ödeyerek e-devlet kayıt işlemini yapabilecektir.)" %}</p>
                                        <p>{% trans "Elektronik kayıt işlemlerini tamamlayan ve kayıt olduklarını gösterir barkodlu çıktıyı alan adaylarımızın ayrıca kayıt tarihlerinde Üniversitemize gelmeleri veya belge getirmelerine gerek yoktur." %}</p>
                                        <p>{% trans "PTT şubelerinden edinebileceğiniz e-devlet şifresi ile <strong>24.08.2026-26.08.2026</strong> tarihleri arasında <a href='https://www.turkiye.gov.tr' target='_blank' class='external-link'>www.turkiye.gov.tr</a> adresinden kaydınızı online yaparak elektronik kayıt belgenizi alabileceksiniz." %}</p>
                                    </div>
                                    
                                    <div class="highlight-box" style="border-left-color: #f79f10;">
                                        <h4><i class="fas fa-user-check"></i> {% trans "2- Yüzyüze (Bireysel) Kayıt:" %}</h4>
                                        <p>{% trans "E-devlet üzerinden e-kayıt yapamayan aday öğrenciler ile e-kayıt sistemine dâhil olmayan programa (<strong>Sivil Havacılık Kabin Hizmetleri</strong>) yerleşen öğrencilerin, şahsen veya noterden vekaletname vereceği vekili tarafından <strong>24.08.2026-28.08.2026</strong> tarihleri arasında Üniversiteye gelerek yaptırdığı kayıt işlemidir." %}</p>
                                    </div>

                                    <div class="mission-vision-container" style="margin-top: 30px;">
                                        <div class="mission-box" style="text-align: center; border-top: 4px solid var(--secondary-medium-blue);">
                                            <div class="mv-icon" style="margin: 0 auto 20px;">
                                                <i class="fas fa-users"></i>
                                            </div>
                                            <h4>{% trans "Yüz Yüze Kayıt" %}</h4>
                                            <p style="margin-bottom: 5px;"><strong>{% trans "Tarih:" %}</strong> {% trans "24 – 28 Ağustos 2026 (09:00 – 17:00)" %}</p>
                                            <p><strong>{% trans "Yer:" %}</strong> {% trans "Avrasya Üniversitesi Ömer Yıldız Yerleşkesi Yalıncak / TRABZON" %}</p>
                                        </div>
                                        
                                        <div class="vision-box" style="text-align: center; border-top: 4px solid #f79f10;">
                                            <div class="mv-icon" style="margin: 0 auto 20px; background: linear-gradient(135deg, #f79f10, #f39c12);">
                                                <i class="fas fa-laptop-house"></i>
                                            </div>
                                            <h4>{% trans "E-Devlet Kayıt" %}</h4>
                                            <p style="margin-bottom: 5px;"><strong>{% trans "Tarih:" %}</strong> {% trans "24 – 26 Ağustos 2026" %}</p>
                                            <p>
                                                {% trans "Üniversite e-kayıt Kullanım kılavuzu için" %} 
                                                <a href="https://static.turkiye.gov.tr/themes/ankara/assets/manuals/YOK-Kayit.pdf" target="_blank" class="external-link"><strong>{% trans "tıklayınız." %}</strong></a>
                                            </p>
                                        </div>
                                    </div>
                                    
                                    <div class="alert alert-info mt-4" style="background-color: rgba(141, 212, 227, 0.15); border: 1px solid rgba(141, 212, 227, 0.5); border-radius: 8px; padding: 20px;">
                                        <p style="margin-bottom: 10px;"><strong><i class="fas fa-info-circle" style="color: var(--secondary-medium-blue);"></i> {% trans "Not:" %}</strong> {% trans "E-devlet kaydını tamamlayan adayın Yüz Yüze kayıtta istenilen evrakları <strong>23.09.2026-30.10.2026</strong> tarihleri arasında Öğrenci İşleri Daire Başkanlığına teslim etmesi gerekmektedir." %}</p>
                                        <p style="margin-bottom: 0;">{% trans "E-kayıt yaptıran öğrenciler Ön Kayıt Formu için" %} <a href="https://obs.avrasya.edu.tr/oibs/ogrsis/ogr_on_kayit_op.aspx" target="_blank" class="external-link"><strong>{% trans "tıklayınız" %}</strong></a> {% trans "(doldurulması zorunludur)." %}</p>
                                    </div>

                                    <div class="action-buttons-container" style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 40px;">
                                        <a href="https://odeme.avrasya.edu.tr/" target="_blank" class="btn-action-orange">
                                            <i class="fas fa-credit-card"></i> {% trans "Online Ödeme Yapmak İçin Tıklayınız" %}
                                        </a>
                                        <a href="{% static 'files/2026-yeni-ogrencilerin-egitim-ucretleri-23.07.2026.pdf' %}" target="_blank" class="btn-action-outline">
                                            <i class="fas fa-file-invoice-dollar"></i> {% trans "2026-2027 Yeni Kayıt Eğitim Ücretleri Tablosu" %}
                                        </a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- تب 2: Gerekli Belgeler -->
                            <div id="tab-2" class="tab-content">
                                <div class="tab-content-header">
                                    <h3><i class="fas fa-folder-open"></i> {% trans "Yüz Yüze Kayıt İçin Gerekli Belgeler" %}</h3>
                                </div>
                                <div class="tab-content-body">
                                    <ul class="responsibilities-list">
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <a href="https://obs.avrasya.edu.tr/oibs/ogrsis/ogr_on_kayit_op.aspx" target="_blank" class="external-link">{% trans "Ön Kayıt Formu (doldurulması ve imzalanarak teslim edilmesi zorunludur)." %}</a>
                                        </li>
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <span>{% trans "Lise Diploması aslı veya mezuniyet belgesi (e-Devlet üzerinden alınan karekodlu belge geçerlidir)." %}</span>
                                        </li>
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <span>{% trans "YKS Yerleştirme Sonuç Belgesi (karekodlu internet çıktısı)." %}</span>
                                        </li>
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <span>{% trans "Nüfus Cüzdanı fotokopisi ve T.C. Kimlik kartı." %}</span>
                                        </li>
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <span>{% trans "Erkek adaylar için Askerlik Durum Belgesi (e-Devlet çıktısı)." %}</span>
                                        </li>
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <span>{% trans "1 adet vesikalık fotoğraf." %}</span>
                                        </li>
                                        <li>
                                            <i class="fas fa-check-circle"></i>
                                            <span>{% trans "Öğrenim ücretinin ödendiğine dair dekont veya banka sözleşmesi." %}</span>
                                        </li>
                                    </ul>
                                    
                                    <div class="highlight-box" style="border-left-color: #e74c3c; margin-top: 40px; background: linear-gradient(135deg, rgba(231, 76, 60, 0.03), rgba(192, 57, 43, 0.05));">
                                        <h4 style="color: #c0392b;"><i class="fas fa-plane-departure" style="color: #e74c3c;"></i> {% trans "SİVİL HAVACILIK KABİN HİZMETLERİ (Ön Lisans) Eğitim Nitelikleri" %}</h4>
                                        <p>{% trans "Bu mesleği icra edebilmek için aranan nitelikler:" %}</p>
                                        <ol class="custom-ol">
                                            <li>{% trans "Adli sicil kaydı veya Adli Sicil Arşiv Kaydı bulunmamak." %}</li>
                                            <li>{% trans "Bayanlar için 160 cm-180 cm arası boya sahip olmak (ağırlığı, boy uzunluğunun santimetre olarak ifade edilen değerinin son iki rakamından en çok 5 kilogram fazla veya 15 kilogram noksan ağırlıkta olmak)." %}</li>
                                            <li>{% trans "Erkekler için 170-190 cm arası boya sahip olmak (ağırlığı, boy uzunluğunun santimetre olarak ifade edilen değerinin son iki rakamından en çok 5 kilogram fazla veya 15 kilogram noksan ağırlıkta olmak)." %}</li>
                                            <li>
                                                {% trans "Sivil Havacılık Genel Müdürlüğü tarafından yetkilendirilmiş havacılık tıp merkezlerinde yapılan muayene sonucunda uçuşa elverişli olduğuna dair sağlık raporu almak." %}
                                                <a href="https://avrasya.edu.tr/wp-content/uploads/2026/08/ysk1.pdf" target="_blank" class="external-link" style="color: #c0392b;"><strong>{% trans "(Tıklayınız)" %}</strong></a>
                                            </li>
                                            <li>{% trans "Kabin memuru üniforması giyildiğinde vücudunun görünecek yerlerinde dövme, yara izi vb. bulunmamak." %}</li>
                                            <li>{% trans "Bu programa yerleşen aday öğrencilerden programa kayıt esnasında mesleği icra edebilmek için aranan nitelikleri sağlamamalarına rağmen kaydolarak eğitim almak istemeleri halinde adayların bilgilendirilerek Sivil Havacılık Genel Müdürlüğü tarafından hazırlanan taahhütnamenin adaylar tarafından doldurularak imzalanması durumunda kayıtlarının yapılması." %}</li>
                                        </ol>
                                    </div>

                                    <h3 style="margin-top: 50px; padding-bottom: 10px; border-bottom: 2px solid rgba(141, 212, 227, 0.3);"><i class="fas fa-download"></i> {% trans "İndirilebilir Kayıt Formları" %}</h3>
                                    <div class="download-grid">
                                        <a href="https://avrasya.edu.tr/wp-content/uploads/2026/08/Avrasya_Universitesi_basvuru_ve_kayit_dosyasi_kapak_formu_osym-21.08.2026.pdf" target="_blank" class="download-card">
                                            <div class="d-icon"><i class="fas fa-file-pdf"></i></div>
                                            <div class="d-text">{% trans "Başvuru ve Kayıt Dosyası Kapak Formu" %}</div>
                                        </a>
                                        <a href="https://obs.avrasya.edu.tr/oibs/ogrsis/ogr_on_kayit_op.aspx" target="_blank" class="download-card">
                                            <div class="d-icon"><i class="fas fa-file-alt"></i></div>
                                            <div class="d-text">{% trans "Ön Kayıt Formu" %}</div>
                                        </a>
                                        <a href="https://avrasya.edu.tr/wp-content/uploads/2026/08/Avrasya-Universitesi-Ogrenci-Egitim-Sozlesmesi-21.08.2026.pdf" target="_blank" class="download-card">
                                            <div class="d-icon"><i class="fas fa-file-signature"></i></div>
                                            <div class="d-text">{% trans "Öğrenci Eğitim Sözleşmesi ve Aydınlatma Metni" %}</div>
                                        </a>
                                        <a href="https://avrasya.edu.tr/wp-content/uploads/2026/08/Sivil-Havacilik-Kabin-Hizmetleri-Programina-kayit-icin-sart-olan-Saglik-Raporu-Beyani.pdf" target="_blank" class="download-card">
                                            <div class="d-icon"><i class="fas fa-plane"></i></div>
                                            <div class="d-text">{% trans "Sivil Havacılık Şartlı Kayıt Taahhütnamesi" %}</div>
                                        </a>
                                        <a href="https://avrasya.edu.tr/wp-content/uploads/2026/08/BEYANNAME-gecici-kayit-icin-YKS-21.08.2026.pdf" target="_blank" class="download-card">
                                            <div class="d-icon"><i class="fas fa-file-contract"></i></div>
                                            <div class="d-text">{% trans "Liseden Mezun Olamayanlar İçin Geçici Kayıt Taahhütnamesi" %}</div>
                                        </a>
                                        <a href="https://avrasya.edu.tr/wp-content/uploads/2026/08/2026-2027-Guz-Donemi-Ders-Kayit-Sureci-ve-OBS-giris-yeni-kazanan-ogrenciler-icin-21.08.2026.pdf" target="_blank" class="download-card">
                                            <div class="d-icon"><i class="fas fa-info-circle"></i></div>
                                            <div class="d-text">{% trans "Kayıt Sonrası Uygulanacak Süreç Rehberi" %}</div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- تب 3: Ödeme Koşulları -->
                            <div id="tab-3" class="tab-content">
                                <div class="tab-content-header">
                                    <h3><i class="fas fa-credit-card"></i> {% trans "Ödeme Koşulları" %}</h3>
                                </div>
                                <div class="tab-content-body">
                                    <div style="text-align: center; margin-bottom: 40px;">
                                        <a href="https://odeme.avrasya.edu.tr/" target="_blank" class="btn-action-orange" style="display: inline-flex; font-size: 1.2rem; padding: 15px 40px;">
                                            <i class="fas fa-credit-card"></i> {% trans "Hemen Online Ödeme Yap" %}
                                        </a>
                                    </div>

                                    <h2><strong>{% trans "ÖDEME KOŞULLARI" %}</strong></h2>
                                    
                                    <div class="highlight-box">
                                        <h4><i class="fas fa-money-bill-wave"></i> {% trans "Nakit Ödeme" %}</h4>
                                        <p>{% trans "Bölüm ücretinin tamamını nakit olarak ödemek isteyenler; Üniversitemizin aşağıda belirtilen Iban numaralarına dekontun açıklama kısmına öğrencinin Adı Soyadı ve T.C. Kimlik numarası yazılarak yapılmalıdır. Nakit ödemeler gişelerden veya internet bankacılığı aracılığı ile yapılabilmektedir." %}</p>
                                    </div>
                                    
                                    <div class="highlight-box">
                                        <h4><i class="fas fa-credit-card"></i> {% trans "Kredi Kartı ile Taksitli Ödeme" %}</h4>
                                        <p>{% trans "Bölüm ücretinin kredi kartına taksitli ödemek isteyenler ve anlaşmalı kredi kartlarına vade farksız faizsiz 9 taksit yaptırabilirler. Anlaşmalı banka kartlarına sahip olmayanlar," %} <strong>{% trans "Albaraka Türk Katılım Bankası" %}</strong> {% trans "ile otomatik katılım sistemi (OTS) anlaşması yaparak 9 taksite varan faizsiz kredi kullanabilirler. Faizsiz krediden, çalışan öğrenci veya veli Üniversitemiz muhasebe biriminden alacak olduğu proforma fatura ile kendisine ait bir gelir belgesi ekleyerek bankaya başvuru yaparak yararlanabilir." %}</p>
                                    </div>
                                    
                                    <h3 style="margin-top: 30px; color: var(--primary-dark-blue);">{% trans "Proforma Fatura İçin Gerekli Bilgiler" %}</h3>
                                    <p>{% trans "Proforma fatura düzenlemesi için muhasebe birimine bildirilmesi gereken bilgiler şunlardır:" %}</p>
                                    
                                    <ul class="responsibilities-list" style="padding-left: 20px;">
                                        <li><i class="fas fa-check-circle"></i> {% trans "Öğrencinin Yerleşme sonuç belgesi" %}</li>
                                        <li><i class="fas fa-check-circle"></i> {% trans "Krediyi kullanacak kişinin Adı Soyadı ve TC kimlik no" %}</li>
                                        <li><i class="fas fa-check-circle"></i> {% trans "Kredi çekilecek miktar" %}</li>
                                        <li><i class="fas fa-check-circle"></i> {% trans "Kredi Taksit Sayısı (En fazla 9 taksit)" %}</li>
                                    </ul>
                                    
                                    <p>{% trans "Yukarıda yazılı bilgileri eksiksiz olarak" %} <a href="mailto:muhasebe@avrasya.edu.tr" class="external-link">{% trans "muhasebe@avrasya.edu.tr" %}</a> {% trans "mail adresine gönderen öğrenciye proforma düzenlenip geri dönüş sağlanacaktır." %}</p>
                                    
                                    <div class="mission-vision-container" style="margin-top: 40px;">
                                        <div class="mission-box">
                                            <div class="mv-icon">
                                                <i class="fas fa-university"></i>
                                            </div>
                                            <h4>{% trans "NAKİT ÖDEME YAPILAN BANKALAR" %}</h4>
                                            <p><strong>{% trans "Alıcı Adı:" %}</strong> {% trans "T.C. Avrasya Üniversitesi" %}</p>
                                            <p><strong>{% trans "Banka Adı:" %}</strong> {% trans "Albaraka Türk Katılım Bankası Değirmendere Şubesi" %}</p>
                                            <p><strong>{% trans "İban No:" %}</strong> {% trans "TR78 0020 3000 0210 7500 0000 01" %}</p>
                                            <hr style="margin: 15px 0; border-color: rgba(141, 212, 227, 0.3);">
                                            <p><strong>{% trans "Alıcı Adı:" %}</strong> {% trans "T.C. Avrasya Üniversitesi" %}</p>
                                            <p><strong>{% trans "Banka Adı:" %}</strong> {% trans "Garanti Bankası Trabzon Merkez Şubesi" %}</p>
                                            <p><strong>{% trans "İban No:" %}</strong> {% trans "TR82 0006 2000 1580 0006 2949 19" %}</p>
                                            <p style="margin-top: 15px; padding: 10px; background-color: rgba(141, 212, 227, 0.1); border-radius: 8px;">
                                                <strong>{% trans "Not:" %}</strong> {% trans "Dekontun açıklama kısmına Öğrencinin Adı Soyadı ve T.C. Kimlik numarası yazılmalıdır." %}
                                            </p>
                                        </div>
                                        
                                        <div class="vision-box">
                                            <div class="mv-icon">
                                                <i class="fas fa-credit-card"></i>
                                            </div>
                                            <h4>{% trans "9 TAKSİT YAPILAN BANKA KREDİ KARTLARI" %}</h4>
                                            <p>{% trans "Akbank – Axess / Halkbankası - Paraf / İş Bankası - Maximum" %}<br>
                                            {% trans "Yapıkredi – World / Vakıfbank – World – Ziraat Bankası / Garanti ve Bonus özellikli bütün kredi kartları" %}</p>
                                            
                                            <div style="margin-top: 25px; padding: 15px; background-color: rgba(255, 0, 0, 0.05); border-radius: 8px; border-left: 4px solid #e74c3c;">
                                                <p style="margin: 0; color: #c0392b;">
                                                    <strong>{% trans "Önemli Notlar:" %}</strong><br>
                                                    {% trans "• Bu kartların haricindeki bütün kredi kartlarına tek çekim yapılmaktadır." %}<br>
                                                    {% trans "• Ticari kartlara BDDK kararı gereğince taksit yapılamamaktadır." %}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* متغیرهای رنگ */
:root {
    --primary-dark-blue: #092442;
    --secondary-medium-blue: rgb(29, 97, 169);
    --accent-light-blue: #8dd4e3;
    --neutral-cream: rgb(247, 243, 233);
    --pure-white: rgb(255, 255, 255);
    --text-dark: #1a1a1a;
    --text-light: #666666;
}
/* Hero Section */
.research-hero {
    background: linear-gradient(135deg, #4a6fa5 0%, #2e4a7d 100%);
    padding: 80px 0 60px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    margin-top: -120px;
}

.research-hero:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M0,0 L100,0 L100,100 Z" fill="rgba(255,255,255,0.1)"/></svg>');
    background-size: cover;
}

.research-hero-content h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 15px;
    margin-top: 20px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* Layout */
.main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.sidebar-wrapper {
    position: sticky;
    top: 120px;
    background: var(--pure-white);
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    padding: 20px;
    height: fit-content;
    border: 1px solid rgba(141, 212, 227, 0.2);
}

.content-wrapper {
    background: var(--pure-white);
    border-radius: 12px;
    padding: 40px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    border: 1px solid rgba(141, 212, 227, 0.2);
}

.page-intro {
    text-align: center;
    margin-bottom: 40px;
}

.section-title {
    color: var(--primary-dark-blue);
    font-size: 2.2rem;
    font-weight: 800;
    font-family: 'Metropolis', sans-serif;
    margin-bottom: 15px;
    position: relative;
    display: inline-block;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, var(--secondary-medium-blue), var(--accent-light-blue));
    border-radius: 2px;
}

.section-subtitle {
    color: var(--text-light);
    font-size: 1.1rem;
    max-width: 800px;
    margin: 30px auto 0;
    line-height: 1.6;
}

/* طراحی تب‌ها */
.ogrenci-isleri-tab-section {
    margin-top: 20px;
}

.tab-container {
    background: var(--pure-white);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(141, 212, 227, 0.3);
}

.tab-header {
    background: linear-gradient(135deg, var(--primary-dark-blue), var(--secondary-medium-blue));
    padding: 0;
}

.tab-menu {
    display: flex;
    list-style: none;
    padding: 0;
    margin: 0;
    overflow-x: auto;
}

.tab-menu-item {
    flex: 1;
    min-width: 180px;
    padding: 22px 20px;
    text-align: center;
    color: rgba(255, 255, 255, 0.85);
    font-weight: 600;
    font-size: 1.05rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border-bottom: 4px solid transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.tab-menu-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

.tab-menu-item.active {
    background: rgba(255, 255, 255, 0.15);
    color: white;
    border-bottom: 4px solid var(--accent-light-blue);
}

.tab-menu-item i {
    font-size: 1.2rem;
}

.tab-content-wrapper {
    padding: 0;
}

.tab-content {
    display: none;
    animation: fadeIn 0.5s ease;
}

.tab-content.active {
    display: block;
}

.tab-content-header {
    background: linear-gradient(135deg, rgba(9, 36, 66, 0.05), rgba(29, 97, 169, 0.08));
    padding: 25px 30px;
    border-bottom: 1px solid rgba(141, 212, 227, 0.3);
}

.tab-content-header h3 {
    color: var(--primary-dark-blue);
    margin: 0;
    font-size: 1.6rem;
    display: flex;
    align-items: center;
    gap: 15px;
}

.tab-content-header h3 i {
    color: var(--secondary-medium-blue);
}

.tab-content-body {
    padding: 30px;
}

.tab-content-body p {
    color: var(--text-dark);
    line-height: 1.7;
    margin-bottom: 20px;
    font-size: 1.05rem;
}

.tab-content-body h2 {
    color: var(--primary-dark-blue);
    margin-top: 30px;
    margin-bottom: 20px;
    font-size: 1.8rem;
}

.tab-content-body h3 {
    color: var(--secondary-medium-blue);
    margin-top: 25px;
    margin-bottom: 15px;
    font-size: 1.4rem;
}

.highlight-box {
    background: linear-gradient(135deg, rgba(9, 36, 66, 0.03), rgba(29, 97, 169, 0.05));
    border-radius: 12px;
    padding: 25px;
    margin: 30px 0;
    border-left: 5px solid var(--secondary-medium-blue);
}

.highlight-box h4 {
    color: var(--primary-dark-blue);
    margin-top: 0;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.3rem;
}

.highlight-box h4 i {
    color: var(--secondary-medium-blue);
}

/* Custom Ordered List */
.custom-ol {
    padding-left: 20px;
    margin-bottom: 0;
}
.custom-ol li {
    margin-bottom: 12px;
    color: var(--text-dark);
    line-height: 1.6;
}
.custom-ol li::marker {
    color: #e74c3c;
    font-weight: bold;
}

/* Download Grid */
.download-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 25px;
}

.download-card {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    text-decoration: none;
    color: var(--text-dark);
    transition: all 0.3s ease;
}

.download-card:hover {
    background: #ffffff;
    box-shadow: 0 8px 15px rgba(0,0,0,0.08);
    transform: translateY(-3px);
    color: var(--secondary-medium-blue);
    border-color: rgba(141, 212, 227, 0.5);
}

.d-icon {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: rgba(29, 97, 169, 0.1);
    color: var(--secondary-medium-blue);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    transition: all 0.3s ease;
}

.download-card:hover .d-icon {
    background: var(--secondary-medium-blue);
    color: #fff;
}

.d-text {
    font-weight: 600;
    font-size: 0.95rem;
    line-height: 1.4;
}

.responsibilities-list {
    list-style: none;
    padding: 0;
    margin: 20px 0;
}

.responsibilities-list li {
    padding: 12px 15px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    border-left: 4px solid var(--accent-light-blue);
    display: flex;
    align-items: center;
    gap: 15px;
    transition: all 0.3s ease;
}

.responsibilities-list li:hover {
    background: rgba(141, 212, 227, 0.1);
    transform: translateX(5px);
}

.responsibilities-list li i {
    color: var(--secondary-medium-blue);
}

.external-link {
    color: var(--secondary-medium-blue);
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

.external-link:hover {
    color: var(--primary-dark-blue);
    text-decoration: underline;
}

/* دکمه‌های اکشن جدید */
.btn-action-orange {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 12px 25px;
    background: linear-gradient(145deg, #f79f10, #e67e22);
    color: #ffffff !important;
    border: none;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1.05rem;
    text-decoration: none;
    box-shadow: 0 5px 15px rgba(247, 159, 16, 0.3);
    transition: all 0.3s ease;
}

.btn-action-orange:hover {
    background: linear-gradient(145deg, var(--primary-dark-blue), var(--secondary-medium-blue));
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(9, 36, 66, 0.25);
}

.btn-action-outline {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 12px 25px;
    background: transparent;
    color: var(--primary-dark-blue) !important;
    border: 2px solid var(--primary-dark-blue);
    border-radius: 30px;
    font-weight: 700;
    font-size: 1.05rem;
    text-decoration: none;
    transition: all 0.3s ease;
}

.btn-action-outline:hover {
    background: var(--primary-dark-blue);
    color: #ffffff !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(9, 36, 66, 0.2);
}

/* Misyon & Vizyon (Cards) */
.mission-vision-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 20px;
}

.mission-box, .vision-box {
    background: var(--pure-white);
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(141, 212, 227, 0.3);
    transition: transform 0.3s ease;
    height: 100%;
}

.mission-box:hover, .vision-box:hover {
    transform: translateY(-5px);
}

.mv-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--primary-dark-blue), var(--secondary-medium-blue));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    color: white;
    font-size: 28px;
}

.mission-box h4, .vision-box h4 {
    color: var(--primary-dark-blue);
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 1.4rem;
}

.mission-box p, .vision-box p {
    color: var(--text-dark);
    line-height: 1.7;
    margin-bottom: 10px;
}

/* انیمیشن‌ها */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.tab-content {
    animation: fadeIn 0.5s ease;
}

.mission-box, .vision-box {
    animation: fadeInUp 0.6s ease forwards;
    opacity: 0;
}

.mission-box { animation-delay: 0.1s; }
.vision-box { animation-delay: 0.2s; }

/* Responsive */
@media (max-width: 1200px) {
    .mission-vision-container {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 992px) {
    .sidebar-wrapper {
        position: relative;
        top: 0;
        margin-bottom: 30px;
    }
    
    .content-wrapper {
        padding: 25px;
    }
    
    .tab-menu {
        flex-wrap: wrap;
    }
    
    .tab-menu-item {
        flex: 1 0 45%;
        min-width: auto;
        padding: 18px 15px;
        font-size: 1rem;
    }
    
    .tab-content-header {
        padding: 20px;
    }
    
    .tab-content-header h3 {
        font-size: 1.4rem;
    }
    
    .tab-content-body {
        padding: 20px;
    }
    .action-buttons-container {
        flex-direction: column;
        align-items: stretch;
    }
    .btn-action-orange, .btn-action-outline {
        justify-content: center;
    }
}

@media (max-width: 768px) {
    .main-container {
        padding: 10px;
    }
    
    .section-title {
        font-size: 1.8rem;
    }
    
    .section-subtitle {
        font-size: 1rem;
    }
    
    .tab-menu-item {
        flex: 1 0 100%;
        justify-content: flex-start;
        padding: 15px 20px;
    }
    
    .mission-vision-container {
        grid-template-columns: 1fr;
    }
    
    .highlight-box {
        padding: 20px;
    }
}

@media (max-width: 576px) {
    .content-wrapper {
        padding: 20px;
    }
    
    .page-intro {
        margin-bottom: 30px;
    }
    
    .tab-content-header {
        padding: 15px;
    }
    
    .tab-content-header h3 {
        font-size: 1.3rem;
    }
    
    .tab-content-body {
        padding: 15px;
    }
    
    .tab-content-body p {
        font-size: 1rem;
    }
    
    .mission-box, .vision-box {
        padding: 20px;
    }
    
    .btn-action-orange, .btn-action-outline {
        padding: 10px 20px;
        font-size: 1rem;
    }
}

/* کاهش motion برای دسترسی */
@media (prefers-reduced-motion: reduce) {
    .tab-content, .mission-box, .vision-box,
    .responsibilities-list li {
        animation: none !important;
        transition: none !important;
    }
    
    .mission-box:hover, .vision-box:hover,
    .responsibilities-list li:hover, .btn-action-orange:hover, .btn-action-outline:hover, .download-card:hover {
        transform: none;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // مدیریت تب‌ها
    const tabMenuItems = document.querySelectorAll('.tab-menu-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabMenuItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // حذف کلاس active از همه تب‌ها
            tabMenuItems.forEach(tab => tab.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // اضافه کردن کلاس active به تب انتخاب شده
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Highlight کردن آیتم‌های لیست هنگام hover
    const listItems = document.querySelectorAll('.responsibilities-list li');
    
    listItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.borderLeftColor = 'var(--secondary-medium-blue)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.borderLeftColor = 'var(--accent-light-blue)';
        });
    });
    
    // انیمیشن‌های هنگام اسکرول
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
            }
        });
    }, observerOptions);
    
    // مشاهده عناصر برای انیمیشن
    const animatedElements = document.querySelectorAll('.mission-box, .vision-box');
    animatedElements.forEach(element => {
        observer.observe(element);
    });
});
</script>
{% endblock %}
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("HTML template updated successfully!")
