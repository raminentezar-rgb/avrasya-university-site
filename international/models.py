from django.db import models
from django.utils.translation import gettext_lazy as _

class InternationalApplication(models.Model):
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ]
    
    COUNTRY_CHOICES = [
        ('tr', _('Turkey')),
        ('us', _('United States')),
        ('gb', _('United Kingdom')),
        ('de', _('Germany')),
        ('fr', _('France')),
    ]
    
    PROGRAM_CHOICES = [
        ('computer', _('Computer Engineering')),
        ('business', _('Business Administration')),
        ('medicine', _('Medicine')),
        ('law', _('Law')),
        ('architecture', _('Architecture')),
    ]
    
    SEMESTER_CHOICES = [
        ('fall2024', _('Fall 2024')),
        ('spring2025', _('Spring 2025')),
        ('fall2025', _('Fall 2025')),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('highschool', _('High School Diploma')),
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('phd', _('PhD')),
    ]
    
    ENGLISH_LEVEL_CHOICES = [
        ('beginner', _('Beginner (A1-A2)')),
        ('intermediate', _('Intermediate (B1-B2)')),
        ('advanced', _('Advanced (C1-C2)')),
        ('native', _('Native Speaker')),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    birth_date = models.DateField(verbose_name=_("Date of Birth"))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    email = models.EmailField(verbose_name=_("Email Address"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))

    # Address Information
    country = models.CharField(max_length=5, choices=COUNTRY_CHOICES, verbose_name=_("Country"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    address = models.TextField(verbose_name=_("Full Address"))

    # Academic Information
    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES, verbose_name=_("Desired Program"))
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, verbose_name=_("Start Date"))
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name=_("Education Level"))
    english_level = models.CharField(max_length=20, choices=ENGLISH_LEVEL_CHOICES, blank=True, null=True, verbose_name=_("English Proficiency"))

    # Documents
    passport_copy = models.FileField(upload_to='international/applications/passports/%Y/%m/%d/', verbose_name=_("Passport Copy"))
    diploma_certificate = models.FileField(upload_to='international/applications/diplomas/%Y/%m/%d/', verbose_name=_("Diploma/Certificate"))
    academic_transcript = models.FileField(upload_to='international/applications/transcripts/%Y/%m/%d/', verbose_name=_("Academic Transcript"))
    passport_photo = models.FileField(upload_to='international/applications/photos/%Y/%m/%d/', verbose_name=_("Passport Photo"))

    # Meta
    newsletter_subscription = models.BooleanField(default=False, verbose_name=_("Newsletter Subscription"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("International Application")
        verbose_name_plural = _("International Applications")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program}"
