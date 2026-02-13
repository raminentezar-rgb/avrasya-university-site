import os
import django
import sys

# Setup Django
sys.path.append('d:\\avrasya_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avrasya_site.settings')
django.setup()

from support.models import KnowledgeBase, FAQ, Department, Category

def index_international():
    # Get or create Department
    dept, _ = Department.objects.get_or_create(name='International')

    # Create Categories
    cat_genel, _ = Category.objects.get_or_create(name='General Information', department=dept)
    cat_application, _ = Category.objects.get_or_create(name='Application & Admissions', department=dept)
    cat_campus, _ = Category.objects.get_or_create(name='Campus Life', department=dept)
    cat_academic, _ = Category.objects.get_or_create(name='Academic Environment & Programs', department=dept)
    cat_city, _ = Category.objects.get_or_create(name='City of Trabzon', department=dept)

    # 1. General Information
    KnowledgeBase.objects.update_or_create(
        title='International Students at Avrasya University',
        defaults={
            'content': '''
            <h3>Welcome to Avrasya University</h3>
            <p>Avrasya University is a vibrant international community with students from over 150 nationalities. We offer a supportive environment and high-quality education to our international students.</p>
            
            <h4>Quick Facts</h4>
            <ul>
                <li><b>150+</b> Nationalities</li>
                <li><b>98%</b> Student Satisfaction Rate</li>
                <li><b>24/7</b> International Students Support</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_genel,
            'department': dept
        }
    )

    # 2. Application Process
    KnowledgeBase.objects.update_or_create(
        title='International Student Application Process 2025',
        defaults={
            'content': '''
            <h3>How to Apply</h3>
            <p>Admissions for 2025 are now open! You can apply through two paths:</p>
            
            <h4>1. Individual Application</h4>
            <p>Apply directly via our Online Application System (OIB). Best for students who want direct control and real-time tracking.</p>
            
            <h4>2. Agency Application</h4>
            <p>Apply through our registered education partners for expert guidance and counseling.</p>
            
            <h4>Required Documents</h4>
            <ul>
                <li><b>Passport Copy:</b> Clear scan of the information page.</li>
                <li><b>Diploma/Certificate:</b> High school or previous degree.</li>
                <li><b>Academic Transcript:</b> Official records from previous institutions.</li>
                <li><b>Passport Photo:</b> White background.</li>
            </ul>
            
            <h4>Timeline</h4>
            <ol>
                <li><b>Application Review:</b> 3-5 business days.</li>
                <li><b>Interview:</b> Online interview if shortlisted.</li>
                <li><b>Admission Decision:</b> Within 2 weeks of interview.</li>
                <li><b>Welcome Package:</b> Receipt of official acceptance letter.</li>
            </ol>
            ''',
            'content_type': 'kb',
            'category': cat_application,
            'department': dept
        }
    )

    # 3. Campus Life
    KnowledgeBase.objects.update_or_create(
        title='Campus Life for International Students',
        defaults={
            'content': '''
            <h3>Living on Campus</h3>
            <p>Avrasya University provides a rich campus life experience with various facilities:</p>
            
            <h4>Accommodation</h4>
            <p>Safe and comfortable dormitories are available for international students near our campuses.</p>
            
            <h4>Dining Services</h4>
            <p>Our cafeterias offer a variety of healthy and affordable meals, including traditional Turkish and international cuisine.</p>
            
            <h4>Sports & Social Activities</h4>
            <ul>
                <li>Fitness centers and sports courts.</li>
                <li>Student clubs and cultural organizations.</li>
                <li>Regular social events and campus festivals.</li>
            </ul>
            
            <h4>Support Services</h4>
            <ul>
                <li><b>International Students Office:</b> Guidance for residence permits and adaptation.</li>
                <li><b>Counseling Service:</b> Personal and academic support.</li>
                <li><b>Student Union:</b> Student representation and peer support.</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_campus,
            'department': dept
        }
    )

    # 4. Academic Environment
    KnowledgeBase.objects.update_or_create(
        title='Academic Environment and Facilities',
        defaults={
            'content': '''
            <h3>Learning Resources</h3>
            <ul>
                <li><b>Computer Center:</b> Modern labs with high-speed internet and necessary software.</li>
                <li><b>Library:</b> Extensive collection of digital and physical resources, study areas.</li>
                <li><b>International Students Office:</b> Dedicated office to assist with all academic and administrative needs.</li>
            </ul>
            
            <h4>Academic Programs</h4>
            <p>We offer diverse programs across various faculties:</p>
            <ul>
                <li>Faculty of Arts and Sciences</li>
                <li>Faculty of Economic and Administrative Sciences</li>
                <li>Faculty of Engineering and Architecture</li>
                <li>Faculty of Health Sciences</li>
            </ul>
            ''',
            'content_type': 'kb',
            'category': cat_academic,
            'department': dept
        }
    )

    # 5. City of Trabzon
    KnowledgeBase.objects.update_or_create(
        title='Exploring the City of Trabzon',
        defaults={
            'content': '''
            <h3>Life in Trabzon</h3>
            <p>Trabzon is an ancient port city on the Black Sea, rich in history and culture.</p>
            
            <h4>Historic Landmarks</h4>
            <ul>
                <li><b>Sumela Monastery:</b> A magnificent cliff-side monastery in the Zigana Mountains.</li>
                <li><b>Hagia Sophia Mosque:</b> A stunning example of Byzantine architecture.</li>
                <li><b>Trabzon Castle:</b> Historic citadels (Inner, Middle, and Lower).</li>
            </ul>
            
            <h4>Culture & Nature</h4>
            <ul>
                <li><b>Mountain Plateaus (Yayla):</b> Beautiful green highlands like Uzungöl and Hıdırnebi.</li>
                <li><b>Traditional Crafts:</b> Beaten copper, jewelry, and textiles.</li>
                <li><b>Sports:</b> Home to the famous <b>Trabzonspor</b> football club.</li>
            </ul>
            
            <h4>Economy</h4>
            <p>Trabzon is a major hub for trade, agriculture (hazelnuts, tea), and fishing (anchovy).</p>
            ''',
            'content_type': 'kb',
            'category': cat_city,
            'department': dept
        }
    )

    # 6. FAQs
    faq_data = [
        {
            'question': 'How long does the application process take?',
            'answer': 'The review process takes 3-5 business days. An admission decision is usually reached within 2 weeks after the interview.'
        },
        {
            'question': 'What languages are used for instruction?',
            'answer': 'Most programs are in Turkish, but we have several programs offered in English. We also provide Turkish and English preparatory courses (TÖMER).'
        },
        {
            'question': 'Is there a residence permit support?',
            'answer': 'Yes, the International Students Office provides full guidance on obtaining and renewing your residence permit in Turkey.'
        },
        {
            'question': 'Are there scholarships for international students?',
            'answer': 'Avrasya University offers various partial and full-tuition scholarships based on academic merit and country of origin.'
        },
        {
            'question': 'How can I reach the campus from the airport?',
            'answer': 'Trabzon Airport is very close to our main campus (Pelitli). You can use public buses, taxis, or university shuttle services during registration periods.'
        }
    ]

    for item in faq_data:
        FAQ.objects.update_or_create(
            question=item['question'],
            department=dept,
            defaults={'answer': item['answer']}
        )

    print("International app content indexed successfully.")

if __name__ == '__main__':
    index_international()
