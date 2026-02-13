import os
import django
import sys

# Setup Django
sys.path.append('d:\\avrasya_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_site.settings')
django.setup()

from support.models import KnowledgeBase, FAQ, Department, Category

def index_akademik():
    print("Indexing Akademik app content...")

    # 1. Get or Create Department
    dept, _ = Department.objects.get_or_create(name='Akademik')

    # 2. Create Categories
    cat_genel, _ = Category.objects.get_or_create(name='Genel Bilgiler', department=dept)
    cat_birimler, _ = Category.objects.get_or_create(name='Akademik Birimler', department=dept)
    cat_iletisim, _ = Category.objects.get_or_create(name='İletişim', department=dept)
    cat_istatistik, _ = Category.objects.get_or_create(name='İstatistikler', department=dept)

    # 3. Index General Info (from home.html main text)
    kb_vizyon, _ = KnowledgeBase.objects.get_or_create(
        title='Avrasya Üniversitesi Akademik Vizyonu',
        category=cat_genel,
        defaults={
            'content': """
            Öğretim üyeleri, öğrencileri ve idari kadrosu ile akademik mükemmeliyet vizyonuna sahip olan Avrasya Üniversitesi; 
            hem mühendislik/fen bilimleri hem de beşeri/sosyal bilimlerin tümünde üstün nitelikli eğitim vererek, 
            yıllardır Türkiye'nin en saygın eğitim kurumu kimliğini korumayı başarmıştır.
            
            Eğitim dili İngilizce olan Avrasya Üniversitesi'nde 30'un üzerinde lisans programı vardır. 
            Lisans eğitiminde öğrenciler, kendi bölümlerinde derinlikli eğitim alırken, farklı disiplinlerden seçmeli derslerle 
            ilgi ve becerilerini geliştirme fırsatı bulurlar. Ayrıca 80'in üzerinde lisansüstü programı bulunmaktadır.
            
            Uluslararasılaşmayı önemseyen üniversitemiz, yurtdışındaki seçkin üniversiteler ile 400'ün üzerinde öğrenci değişim anlaşmasına sahiptir.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # 4. Index Academic Units (from home.html cards and sidebar)
    
    # Enstitüler
    KnowledgeBase.objects.get_or_create(
        title='Enstitüler ve Lisansüstü Eğitim',
        category=cat_birimler,
        defaults={
            'content': """
            Lisansüstü eğitim ve araştırma faaliyetlerinin yürütüldüğü, akademik derinlik ve uzmanlaşmanın merkezi olan enstitülerimiz:
            - Fen Bilimleri Enstitüsü
            - Sosyal Bilimler Enstitüsü
            - Sağlık Bilimleri Enstitüsü
            
            Genel Özellikler:
            - Eğitim Süresi: 2-4 Yıl
            - AKTS: 120+
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # Fakülteler
    KnowledgeBase.objects.get_or_create(
        title='Fakültelerimiz',
        category=cat_birimler,
        defaults={
            'content': """
            6 farklı fakültemizde lisans düzeyinde kaliteli eğitim ve multidisipliner araştırma olanakları sunuyoruz:
            - Fen Edebiyat Fakültesi
            - İktisadi ve İdari Bilimler Fakültesi
            - Mühendislik ve Mimarlık Fakültesi
            - Sağlık Bilimleri Fakültesi
            - İletişim Fakültesi
            
            Genel Özellikler:
            - Eğitim Süresi: 4 Yıl
            - AKTS: 240
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # Yüksekokullar
    KnowledgeBase.objects.get_or_create(
        title='Yüksekokullar',
        category=cat_birimler,
        defaults={
            'content': """
            Uygulamalı bilimler alanında nitelikli eğitim veren ve sektörle entegre çalışan yüksekokullarımız:
            - Yabancı Diller Yüksekokulu
            - Uygulamalı Bilimler Yüksekokulu
            
            Genel Özellikler:
            - Eğitim Süresi: 4 Yıl
            - AKTS: 240
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # Meslek Yüksekokulları
    KnowledgeBase.objects.get_or_create(
        title='Meslek Yüksekokulları (MYO)',
        category=cat_birimler,
        defaults={
            'content': """
            Pratik becerilere odaklanan ve sektörün ihtiyaçlarına yönelik teknik elemanlar yetiştiren meslek yüksekokullarımız:
            - Teknik Bilimler Meslek Yüksekokulu
            - Sağlık Hizmetleri Meslek Yüksekokulu
            - Sosyal Bilimler Meslek Yüksekokulu
            - Adalet Meslek Yüksekokulu
            
            Genel Özellikler:
            - Eğitim Süresi: 2 Yıl
            - AKTS: 120
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # 5. FAQs (from stats and footer)
    faqs = [
        {
            'question': 'Avrasya Üniversitesinde kaç lisans programı var?',
            'answer': 'Üniversitemizde 30\'un üzerinde lisans programı bulunmaktadır.'
        },
        {
            'question': 'Kaç adet lisansüstü program mevcut?',
            'answer': 'Çeşitli disiplinlerde 80\'in üzerinde lisansüstü programımız mevcuttur.'
        },
        {
            'question': 'Değişim programı imkanları nelerdir?',
            'answer': 'Yurtdışındaki seçkin üniversiteler ile 400\'ün üzerinde öğrenci değişim anlaşmamız bulunmaktadır.'
        },
        {
            'question': 'Akademik Merkezleri Koordinatörlüğüne nasıl ulaşabilirim?',
            'answer': 'E-posta yoluyla akademik.merkezleri@avrasya.edu.tr adresinden ulaşabilirsiniz.'
        },
        {
            'question': 'Üniversitenin iletişim bilgileri nedir?',
            'answer': 'Adres: Yenişehir Mahallesi, Avrasya Üniversitesi\nTelefon: +90 462 000 0000\nE-posta: akademik@avrasya.edu.tr'
        }
    ]

    for faq_data in faqs:
        # Create legacy FAQ model
        FAQ.objects.get_or_create(
            question=faq_data['question'],
            department=dept,
            defaults={
                'answer': faq_data['answer'],
                'is_active': True 
            }
        )
        
        # Create KnowledgeBase FAQ entry for Search
        KnowledgeBase.objects.get_or_create(
            title=faq_data['question'],
            content_type='faq',
            category=cat_istatistik if 'Kaç' in faq_data['question'] else cat_iletisim,
            defaults={
                'content': faq_data['answer'],
                'department': dept
            }
        )

    print("Akademik app content has been successfully indexed into KnowledgeBase and FAQs.")

if __name__ == '__main__':
    index_akademik()
