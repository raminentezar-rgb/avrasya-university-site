import os
import django
import sys

# Setup Django
sys.path.append('d:\\avrasya_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_site.settings')
django.setup()

from support.models import KnowledgeBase, FAQ, Department, Category

def index_fakulteler():
    print("Indexing Fakulteler app content...")

    # 1. Get or Create Department
    dept, _ = Department.objects.get_or_create(name='Fakülteler')

    # 2. Create Categories
    cat_genel, _ = Category.objects.get_or_create(name='Genel Bilgiler', department=dept)
    cat_birimler, _ = Category.objects.get_or_create(name='Fakülteler ve Bölümler', department=dept)
    cat_istatistik, _ = Category.objects.get_or_create(name='İstatistikler', department=dept)
    cat_iletisim, _ = Category.objects.get_or_create(name='İletişim', department=dept)

    # 3. Index General Info
    KnowledgeBase.objects.get_or_create(
        title='Avrasya Üniversitesi Fakülteleri Genel Bilgi',
        category=cat_genel,
        defaults={
            'content': """
            Avrasya Üniversitesi, 6 farklı fakültesiyle lisans düzeyinde kaliteli eğitim ve multidisipliner araştırma olanakları sunmaktadır. 
            Her fakülte, kendi alanında uzman akademik kadrosu ve modern altyapısıyla öğrencilerine en iyi eğitim deneyimini sağlamaktadır.
            
            Fakültelerimiz, öğrencilerine sadece teorik bilgi değil aynı zamanda pratik beceriler de kazandırarak, 
            mezun olduklarında iş dünyasının aradığı nitelikli profesyoneller olmalarını hedeflemektedir.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # 4. Index Faculties (Content merged from main page cards + sidebar submenus)
    
    # Fen Edebiyat Fakültesi
    KnowledgeBase.objects.get_or_create(
        title='Fen Edebiyat Fakültesi',
        category=cat_birimler,
        defaults={
            'content': """
            Temel bilimler ve sosyal bilimler alanında nitelikli eğitim veren, bilimsel araştırmalarla topluma katkı sağlayan bir fakülte.
            
            Bölümler:
            - İngiliz Dili ve Edebiyatı
            - Psikoloji
            - Türk Dili ve Edebiyatı
            - Moleküler Biyoloji ve Genetik
            - Mütercim Tercümanlık

            İstatistikler: 8 Bölüm, 120+ AKTS.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # İktisadi ve İdari Bilimler Fakültesi
    KnowledgeBase.objects.get_or_create(
        title='İktisadi ve İdari Bilimler Fakültesi',
        category=cat_birimler,
        defaults={
            'content': """
            İş dünyasının ihtiyaçlarına yönelik uzmanlar yetiştiren, modern ekonominin gereksinimlerine uygun eğitim veren fakülte.

            Bölümler:
            - İşletme
            - İşletme (İngilizce)
            - Siyaset Bilimi ve Kamu Yönetimi
            - Maliye
            - Uluslararası İlişkiler
            
            İstatistikler: 6 Bölüm, 240 AKTS.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # Mühendislik ve Mimarlık Fakültesi
    KnowledgeBase.objects.get_or_create(
        title='Mühendislik ve Mimarlık Fakültesi',
        category=cat_birimler,
        defaults={
            'content': """
            Teknolojik yenilikler ve yaratıcı tasarımlarla geleceği şekillendiren mühendis ve mimarlar yetiştiren fakülte.

            Bölümler:
            - Bilgisayar Mühendisliği
            - Elektrik Elektronik Mühendisliği
            - Gıda Mühendisliği
            - Harita Mühendisliği
            - İç Mimarlık ve Çevre Tasarımı
            - İnşaat Mühendisliği
            - Makine Mühendisliği
            - Mimarlık
            
            İstatistikler: 10 Bölüm, 240 AKTS.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # Sağlık Bilimleri Fakültesi
    KnowledgeBase.objects.get_or_create(
        title='Sağlık Bilimleri Fakültesi',
        category=cat_birimler,
        defaults={
            'content': """
            Sağlık sektörünün ihtiyaç duyduğu nitelikli sağlık profesyonellerini yetiştiren, modern tıp eğitimi veren fakülte.

            Bölümler:
            - Beslenme ve Diyetetik
            - Çocuk Gelişimi
            - Ebelik
            - Ergoterapi
            - Fizyoterapi ve Rehabilitasyon
            - Hemşirelik
            - Odyoloji
            - Sağlık Yönetimi
            - Sosyal Hizmet
            
            İstatistikler: 7 Bölüm, 240 AKTS.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # Spor Bilimleri Fakültesi
    KnowledgeBase.objects.get_or_create(
        title='Spor Bilimleri Fakültesi',
        category=cat_birimler,
        defaults={
            'content': """
            Sporun bilimsel temellerini öğreten, antrenör ve spor yöneticileri yetiştiren fakülte.

            Bölümler:
            - Antrenörlük Eğitimi
            - Egzersiz ve Spor Bilimleri
            - Spor Yöneticiliği
            - Rekreasyon
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # İletişim Fakültesi
    KnowledgeBase.objects.get_or_create(
        title='İletişim Fakültesi',
        category=cat_birimler,
        defaults={
            'content': """
            Medya ve iletişim sektörüne yaratıcı ve donanımlı profesyoneller kazandıran, dijital dönüşüme öncülük eden fakülte.

            Bölümler:
            - Yeni Medya ve İletişim
            - Görsel İletişim Tasarımı
            
            İstatistikler: 5 Bölüm, 240 AKTS.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # 5. FAQs
    faqs = [
        {
            'question': 'Avrasya Üniversitesinde toplam kaç fakülte var?',
            'answer': 'Üniversitemizde toplam 6 fakülte bulunmaktadır: Fen Edebiyat, İktisadi ve İdari Bilimler, Mühendislik ve Mimarlık, Sağlık Bilimleri, Spor Bilimleri ve İletişim Fakültesi.'
        },
        {
            'question': 'Fakültelerde toplam kaç bölüm ve öğrenci var?',
            'answer': 'Fakültelerimizde 36\'dan fazla bölüm, 540\'tan fazla akademisyen ve 8000\'den fazla öğrenci bulunmaktadır.'
        },
        {
            'question': 'Fakülte bölümlerinin AKTS değeri nedir?',
            'answer': 'Genel olarak lisans bölümlerimiz 240 AKTS değerindedir. Fen Edebiyat Fakültesi bazı bölümleri 120+ AKTS olabilir.'
        },
        {
            'question': 'Akademik Merkezleri ile nasıl iletişime geçebilirim?',
            'answer': 'E-posta: akademik.merkezleri@avrasya.edu.tr'
        }
    ]

    for faq_data in faqs:
        # Legacy FAQ
        FAQ.objects.get_or_create(
            question=faq_data['question'],
            department=dept,
            defaults={
                'answer': faq_data['answer'],
                'is_active': True
            }
        )
        # Searchable KB Entry
        KnowledgeBase.objects.get_or_create(
            title=faq_data['question'],
            content_type='faq',
            category=cat_istatistik if 'kaç' in faq_data['question'].lower() else cat_iletisim,
            defaults={
                'content': faq_data['answer'],
                'department': dept
            }
        )

    print("Fakulteler app content has been successfully indexed into KnowledgeBase and FAQs.")

if __name__ == '__main__':
    index_fakulteler()
