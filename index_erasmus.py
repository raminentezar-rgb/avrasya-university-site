import os
import django
import sys

# Setup Django
sys.path.append('d:\\avrasya_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_site.settings')
django.setup()

from support.models import KnowledgeBase, FAQ, Department, Category

def index_erasmus():
    # Get or create Department
    dept, _ = Department.objects.get_or_create(name='Erasmus')

    # Create Categories
    cat_genel, _ = Category.objects.get_or_create(name='Genel Bilgiler', department=dept)
    cat_anlasmalar, _ = Category.objects.get_or_create(name='İkili Anlaşmalar', department=dept)
    cat_belgeler, _ = Category.objects.get_or_create(name='ECHE ve Belgeler', department=dept)
    cat_international, _ = Category.objects.get_or_create(name='International Students', department=dept)

    # 1. Genel Bilgiler
    KnowledgeBase.objects.update_or_create(
        title='Erasmus+ Programı Nedir?',
        defaults={
            'content': '''
            <h3>Erasmus+ Programı</h3>
            <p>Erasmus+ programı, Avrupa Birliği tarafından finanse edilen ve yükseköğretim kurumlarının işbirliğini teşvik eden bir programdır. Öğrencilere, akademik ve idari personele yurtdışında eğitim, staj ve mesleki gelişim imkanları sunar.</p>
            
            <h4>Programın Sunduğu Fırsatlar</h4>
            <ul>
                <li><b>Öğrenci Hareketliliği:</b> Yurt dışındaki bir üniversitede 1 veya 2 dönem eğitim alma.</li>
                <li><b>Staj Hareketliliği:</b> Yurt dışındaki bir işletme veya kuruluşta mesleki staj yapma.</li>
                <li><b>Personel Hareketliliği:</b> Akademik personel için ders verme, idari personel için eğitim alma imkanı.</li>
            </ul>
            
            <h4>Başvuru Şartları (Genel)</h4>
            <ul>
                <li>Tam zamanlı öğrenci olmak.</li>
                <li>Lisans öğrencileri için en az 2.20/4.00 GNO.</li>
                <li>Lisansüstü öğrencileri için en az 2.50/4.00 GNO.</li>
                <li>Yabancı dil yeterliliği (Genellikle B1/B2 seviyesi).</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_genel,
            'department': dept
        }
    )

    # 2. ECHE (Erasmus Charter for Higher Education)
    KnowledgeBase.objects.update_or_create(
        title='Erasmus Yükseköğretim Beyannamesi (ECHE)',
        defaults={
            'content': '''
            <h3>Erasmus Charter for Higher Education (ECHE) 2021-2027</h3>
            <p>Avrasya Üniversitesi, Avrupa Komisyonu tarafından 2021-2027 dönemi için Erasmus Yükseköğretim Beyannamesi (ECHE) ile ödüllendirilmiştir.</p>
            
            <h4>ECHE Temel İlkeleri</h4>
            <ul>
                <li><b>Ayrımcılık Yapmama:</b> Erasmus+ Programında belirtilen ayrımcılık yapmama, şeffaflık ve kapsayıcılık ilkelerine tam saygı göstermek.</li>
                <li><b>Eşit Erişim:</b> Tüm geçmişlerden gelen mevcut ve potansiyel katılımcılara eşit ve adil erişim ve fırsatlar sağlamak.</li>
                <li><b>Tam Tanınma:</b> Yurt dışında başarılı bir şekilde tamamlanan tüm çalışmaların (ECTS kredilerinin) tam ve otomatik olarak tanınmasını sağlamak.</li>
                <li><b>Ücret Muafiyeti:</b> Gelen değişim öğrencilerinden öğrenim ücreti, kayıt, sınav veya laboratuvar ve kütüphane tesislerine erişim için herhangi bir ücret talep etmemek.</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_belgeler,
            'department': dept
        }
    )

    # 3. Erasmus Policy Statement
    KnowledgeBase.objects.update_or_create(
        title='Erasmus Politika Beyanı (Policy Statement)',
        defaults={
            'content': '''
            <h3>Erasmus Politika Beyanı</h3>
            <p>Avrasya Üniversitesi, Erasmus+ Programını uluslararasılaşma ve modernleşme süreci için temel bir fırsat olarak görmektedir.</p>
            
            <h4>Stratejik Hedefler</h4>
            <ul>
                <li>Eğitimin kalitesini artırmak ve Avrupa standartlarına uyum sağlamak.</li>
                <li>Öğrenci ve personelin beceri ve yetkinliklerini geliştirmek.</li>
                <li>Yurt dışındaki üniversitelerle uzun vadeli ve sürdürülebilir ortaklıklar kurmak.</li>
                <li>Bilimsel araştırma faaliyetlerini desteklemek ve ağlar oluşturmak.</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_belgeler,
            'department': dept
        }
    )

    # 4. FAQs
    faq_data = [
        {
            'question': 'Erasmus başvurusu için asgari not ortalaması nedir?',
            'answer': 'Lisans öğrencileri için en az 2.20, yüksek lisans ve doktora öğrencileri için ise en az 2.50 genel not ortalaması (GNO) gereklidir.'
        },
        {
            'question': 'Erasmus ile kaç ay yurt dışında kalabilirim?',
            'answer': 'Öğrenim hareketliliği için genellikle 3 ile 12 ay arası, staj hareketliliği için ise 2 ile 12 ay arası yurt dışında kalınabilir.'
        },
        {
            'question': 'Erasmus hibesi alacak mıyım?',
            'answer': 'Kontenjanlar dahilinde seçilen öğrenciler, gidecekleri ülkenin yaşam maliyetine göre belirlenen aylık hibeyi alırlar. Hibeler karşılıksızdır.'
        },
        {
            'question': 'Hangi ülkelere gidebilirim?',
            'answer': 'Bölümünüzün ikili anlaşması olan tüm AB üyesi ülkelere ve programa dahil olan diğer ülkelere (Norveç, İzlanda, Lihtenştayn, Sırbistan, Kuzey Makedonya) gidebilirsiniz.'
        },
        {
            'question': 'Erasmus ofisi nerede?',
            'answer': 'Erasmus Ofisi, Pelitli Yerleşkesi Rize Caddesi No:226 Trabzon adresinde bulunmaktadır. Dahili telefon: 115.'
        }
    ]

    for item in faq_data:
        FAQ.objects.update_or_create(
            question=item['question'],
            department=dept,
            defaults={'answer': item['answer']}
        )

    # 5. International Students (from international app)
    KnowledgeBase.objects.update_or_create(
        title='Uluslararası Öğrenci Başvuru Süreci',
        defaults={
            'content': '''
            <h3>Uluslararası Öğrenci Başvuruları</h3>
            <p>Avrasya Üniversitesi, dünyanın her yerinden gelen öğrencilere kapılarını açmaktadır.</p>
            
            <h4>Başvuru Adımları</h4>
            <ol>
                <li>Online başvuru formunun doldurulması.</li>
                <li>Gerekli belgelerin (Pasaport, Lise Diploması, Transkript) sisteme yüklenmesi.</li>
                <li>Ön değerlendirme ve kabul mektubunun (Acceptance Letter) gönderilmesi.</li>
                <li>Vize işlemleri ve kesin kayıt için üniversiteye gelinmesi.</li>
            </ol>
            
            <h4>Gerekli Belgeler</h4>
            <ul>
                <li>Pasaport fotokopisi.</li>
                <li>Lise diploması (Türkçe veya İngilizce tercüme).</li>
                <li>Not dökümü (Transkript).</li>
                <li>Varsa dil yeterlilik belgesi (TÖMER, TOEFL vb.).</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_international,
            'department': dept
        }
    )

    # 6. Erasmus Anlaşmalı Kurumlar
    KnowledgeBase.objects.update_or_create(
        title='Erasmus İkili Anlaşmalı Üniversiteler',
        defaults={
            'content': '''
            <h3>Erasmus İkili Anlaşmalar</h3>
            <p>Üniversitemizin birçok Avrupa ülkesindeki saygın yükseköğretim kurumları ile ikili anlaşmaları bulunmaktadır. Bu anlaşmalar öğrenci ve personel hareketliliğini kapsamaktadır.</p>
            
            <h4>Anlaşmalı Olduğumuz Bazı Ülkeler ve Üniversiteler</h4>
            <ul>
                <li><b>Polonya:</b> Radom Academy of Economics, Katowice School of Technology, State University of Applied Sciences in Jaroslaw.</li>
                <li><b>Romanya:</b> University of Bucharest, Danubius University of Galati.</li>
                <li><b>Bulgaristan:</b> South-West University Neofit Rilski.</li>
                <li><b>Makedonya:</b> South East European University Tetovo.</li>
                <li><b>İspanya, İtalya, Almanya:</b> (Bölümlere göre değişiklik göstermektedir).</li>
            </ul>
            
            <p>Bölümünüze özel güncel anlaşma listesi için bölüm web sayfanızdaki "Erasmus" sekmesini veya Erasmus Ofisi panolarını kontrol ediniz.</p>
            ''',
            'content_type': 'kb',
            'category': cat_anlasmalar,
            'department': dept
        }
    )

    print("Erasmus content indexed successfully.")

if __name__ == '__main__':
    index_erasmus()
