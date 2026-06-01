import logging

logger = logging.getLogger(__name__)

class OBSIntegrationService:
    """
    این کلاس وظیفه ارتباط با سیستم OBS دانشگاه را بر عهده دارد.
    فعلا از داده‌های Mock (تستی) استفاده می‌کند اما بعداً کدهای اتصال به API واقعی 
    در همین قسمت جایگزین خواهد شد.
    """
    
    # دیتابیس فرضی برای شبیه‌سازی OBS
    MOCK_OBS_DB = {
        "11111111111": {
            "name": "Ali Yılmaz",
            "department": "Computer Engineering",
            "faculty": "Engineering and Architecture",
            "enrollment_year": 2023,
            "scholarship_percentage": 50, # 50% بورس
            "previous_debt": 0.00,
            "term": "2026-2027 Fall"
        },
        "22222222222": {
            "name": "Ayşe Demir",
            "department": "Business Administration",
            "faculty": "Economics and Administrative Sciences",
            "enrollment_year": 2024,
            "scholarship_percentage": 25, # 25% بورس
            "previous_debt": 1500.00, # بدهی از ترم قبل
            "term": "2026-2027 Fall"
        },
        "33333333333": {
            "name": "John Doe",
            "department": "Medicine",
            "faculty": "Faculty of Medicine",
            "enrollment_year": 2025,
            "scholarship_percentage": 0, # بدون بورس (پرداخت کامل)
            "previous_debt": 0.00,
            "term": "2026-2027 Fall"
        }
    }

    @staticmethod
    def get_student_data(student_id: str) -> dict:
        """
        دریافت اطلاعات خام دانشجو از سیستم OBS
        بعداً این تابع شامل کدهای requests.get() به سرور OBS خواهد بود.
        """
        # TODO: جایگزینی با API واقعی OBS در آینده
        student_data = OBSIntegrationService.MOCK_OBS_DB.get(student_id)
        if not student_data:
            return None
        return student_data


class TuitionCalculatorService:
    """
    این کلاس وظیفه محاسبه مبلغ نهایی شهریه دانشجو را بر عهده دارد.
    قوانین تجاری (Business Rules) دانشگاه در این کلاس اعمال می‌شوند.
    """
    
    # تعرفه پایه سالانه دانشکده‌ها (برای مثال)
    BASE_TUITION_FEES = {
        "Engineering and Architecture": 50000.00,
        "Economics and Administrative Sciences": 40000.00,
        "Faculty of Medicine": 100000.00,
        "DEFAULT": 30000.00
    }

    @staticmethod
    def calculate_final_balance(student_data: dict) -> dict:
        """
        محاسبه شهریه بر اساس اطلاعات دریافتی از OBS:
        ۱. پیدا کردن شهریه پایه دانشکده
        ۲. اعمال درصد بورسیه (تخفیف)
        ۳. اضافه کردن بدهی‌های قبلی
        """
        faculty = student_data.get("faculty", "")
        
        # ۱. استخراج شهریه پایه
        base_fee = TuitionCalculatorService.BASE_TUITION_FEES.get(
            faculty, 
            TuitionCalculatorService.BASE_TUITION_FEES["DEFAULT"]
        )
        
        # ۲. محاسبه تخفیف بورسیه
        scholarship_percent = student_data.get("scholarship_percentage", 0)
        discount = base_fee * (scholarship_percent / 100)
        term_fee = base_fee - discount
        
        # ۳. اضافه کردن بدهی قبلی
        previous_debt = student_data.get("previous_debt", 0.00)
        total_payable = term_fee + previous_debt
        
        # بروزرسانی دیکشنری دانشجو با مبالغ محاسبه شده
        student_data["base_fee"] = base_fee
        student_data["discount_amount"] = discount
        student_data["term_fee"] = term_fee
        student_data["total_payable"] = total_payable
        student_data["currency"] = "TRY"
        
        return student_data
