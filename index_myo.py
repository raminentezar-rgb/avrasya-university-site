import os
import django
import sys

# Setup Django
sys.path.append('d:\\avrasya_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_site.settings')
django.setup()

from support.models import KnowledgeBase, FAQ, Department, Category

def index_myo():
    print("Indexing Meslek Yüksekokulu app content...")

    # 1. Get or Create Department
    dept, _ = Department.objects.get_or_create(name='Meslek Yüksekokulu')

    # 2. Create Categories
    cat_genel, _ = Category.objects.get_or_create(name='Genel Bilgiler', department=dept)
    cat_programlar, _ = Category.objects.get_or_create(name='Programlar', department=dept)
    cat_istatistik, _ = Category.objects.get_or_create(name='İstatistikler', department=dept)
    cat_iletisim, _ = Category.objects.get_or_create(name='İletişim', department=dept)

    # 3. Index General Info
    KnowledgeBase.objects.get_or_create(
        title='Meslek Yüksekokulu Genel Bilgi',
        category=cat_genel,
        defaults={
            'content': """
            Meslek Yüksekokulu, uygulamalı eğitim ve sektör işbirliği ile kalifiye teknik personel yetiştirmektedir.
            
            Özellikler:
            - Pratik Eğitim: Sektörle iç içe staj programları.
            - Sektör İşbirliği: Yerel ve ulusal firmalarla anlaşmalar.
            - İstihdam Odaklı: Yüksek mezun istihdam oranı.
            """,
            'content_type': 'guide',
            'department': dept
        }
    )

    # 4. Index Programs
    programs = [
        {
            'title': 'Adalet',
            'desc': 'Hukuk sisteminde yardımcı personel olarak görev alacak uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Aşçılık',
            'desc': 'Profesyonel mutfak teknikleri ve gastronomi alanında uzman şefler yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Bilgisayar Programcılığı',
            'desc': 'Yazılım geliştirme ve bilgisayar teknolojileri alanında uzmanlaşın.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Bilişim Teknolojileri Güvenliği',
            'desc': 'Siber güvenlik uzmanı yetiştiren, bilişim sistemlerini koruma programı.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Dış Ticaret',
            'desc': 'Uluslararası ticaret ve ihracat-ithalat işlemleri uzmanları yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'E-Ticaret ve Pazarlama',
            'desc': 'Dijital pazarlama ve online ticaret alanında uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Ergoterapi',
            'desc': 'Fiziksel ve zihinsel engelli bireylerin rehabilitasyonu için uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Grafik Tasarımı',
            'desc': 'Görsel iletişim ve dijital tasarım alanında yaratıcı uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Halkla İlişkiler ve Tanıtım',
            'desc': 'Kurumsal iletişim ve marka yönetimi alanında uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'İç Mekan Tasarımı',
            'desc': 'Mekan tasarımı ve dekorasyon alanında yaratıcı uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'İnşaat Teknolojisi',
            'desc': 'Yapı teknolojileri ve inşaat uygulamalarında uzmanlaşın.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Lojistik',
            'desc': 'Tedarik zinciri ve lojistik yönetimi alanında kariyer fırsatları.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Mimari Restorasyon',
            'desc': 'Tarihi yapıların korunması ve restorasyonu alanında uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Moda Tasarımı',
            'desc': 'Tekstil ve moda tasarımı alanında yaratıcı uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Otomotiv Teknolojisi',
            'desc': 'Otomotiv sektöründe teknik uzmanlar ve servis elemanları yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Sivil Havacılık',
            'desc': 'Havacılık sektöründe yer hizmetleri ve kabin memuru yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Sosyal Güvenlik',
            'desc': 'Sosyal güvenlik kurumlarında çalışacak uzman personel yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Sosyal Hizmetler',
            'desc': 'Toplumun dezavantajlı kesimlerine yönelik sosyal hizmet uzmanları yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Spor Yönetimi',
            'desc': 'Spor organizasyonları ve spor kulüplerinde yöneticiler yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Uygulamalı İngilizce ve Çevirmenlik',
            'desc': 'İngilizce tercümanlık ve dil hizmetleri alanında uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        },
        {
            'title': 'Web Tasarımı ve Kodlama',
            'desc': 'Web geliştirme ve front-end programlama alanında uzmanlar yetiştirir.',
            'duration': '2 Yıl',
            'ects': '120 AKTS'
        }
    ]

    for prog in programs:
        KnowledgeBase.objects.get_or_create(
            title=f"MYO - {prog['title']}",
            category=cat_programlar,
            defaults={
                'content': f"""
                Program: {prog['title']}
                Açıklama: {prog['desc']}
                Eğitim Süresi: {prog['duration']}
                Kredi: {prog['ects']}
                
                Bu program, öğrencilere ilgili sektörde doğrudan çalışabilecekleri uygulamalı beceriler kazandırmayı hedefler.
                """,
                'content_type': 'guide',
                'department': dept
            }
        )

    # 5. FAQs
    faqs = [
        {
            'question': 'Meslek Yüksekokulunda kaç program var?',
            'answer': 'Meslek Yüksekokulumuzda 22\'den fazla akademik program bulunmaktadır.'
        },
        {
            'question': 'MYO programlarının eğitim süresi ne kadar?',
            'answer': 'Tüm MYO programlarımız 2 yıl sürmektedir ve 120 AKTS kredisidir.'
        },
        {
            'question': 'Staj zorunluluğu var mı?',
            'answer': 'Evet, MYO programlarımızda sektörel staj zorunluluğu bulunmaktadır. Öğrencilerimiz anlaşmalı firmalarda staj yapabilirler.'
        },
        {
            'question': 'Öğrenci işleri ile nasıl iletişime geçerim?',
            'answer': 'E-posta: ogrenciisleri@avrasya.edu.tr'
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
            category=cat_istatistik if 'Kaç' in faq_data['question'] or 'ne kadar' in faq_data['question'] else cat_iletisim,
            defaults={
                'content': faq_data['answer'],
                'department': dept
            }
        )

    print("Meslek Yüksekokulu app content has been successfully indexed into KnowledgeBase and FAQs.")

if __name__ == '__main__':
    index_myo()
