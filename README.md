# iFerment 1.0.0 - حسابگر تخمیر و تقطیر

یک برنامه وب جامع برای محاسبات دقیق فرآیندهای تخمیر و تقطیر الکل.

## 📋 ویژگی‌ها

### محاسبات تخمیر
- **محاسبه قند تخمیر**: محاسبه میزان قند، حجم آب و مواد مغذی مورد نیاز
- **تخمیر غلات**: محاسبات تخمیر برای انواع غلات
- **تخمیر میوه**: محاسبات تخمیر برای میوه‌جات
- **محاسبات تخمیر عمومی**: محاسبات کلی فرآیند تخمیر

### محاسبات تقطیر
- **پکینگ اسپیرال**: محاسبه پارامترهای پکینگ اسپیرال
- **ریفلاکس**: محاسبات نسبت ریفلاکس و پارامترهای مرتبط
- **آزئوتروپ**: محاسبه نقطه آزئوتروپ
- **اسپیریت ران**: محاسبات دقیق برای اسپیریت ران
- **زمان گرم شدن مخزن**: محاسبه زمان مورد نیاز برای گرم کردن مخزن تقطیر
- **نقطه جوش**: محاسبه نقطه جوش بر اساس فشار و دما
- **گرمای ستون**: محاسبات گرمایی ستون تقطیر
- **مایع باقیمانده**: محاسبه حجم مایع باقیمانده

### سایر محاسبات
- **محاسبه الکل خون**: محاسبه غلظت الکل در خون بر اساس مصرف نوشیدنی
- **قدرت المنت**: محاسبات قدرت المنت گرمایی
- **رفرکتومتر**: محاسبات رفرکتومتر

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.8 یا بالاتر
- pip (مدیر بسته Python)

### مراحل نصب

1. کلون کردن یا دانلود پروژه:
```bash
git clone https://github.com/Hrnikkhoo/chemical-process-calculator.git
cd iferment1.0.0
```

2. ایجاد محیط مجازی (اختیاری اما توصیه می‌شود):
```bash
python -m venv venv

# در Windows:
venv\Scripts\activate

# در Linux/Mac:
source venv/bin/activate
```

3. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

4. اجرای برنامه:
```bash
python app.py
```

5. باز کردن مرورگر و رفتن به:
```
http://localhost:5000
```

## 📁 ساختار پروژه

```
iferment1.0.0/
├── app.py                 # فایل اصلی Flask
├── requirements.txt       # وابستگی‌های پروژه
├── README.md             # این فایل
├── .gitignore            # فایل‌های نادیده گرفته شده توسط Git
│
├── templates/            # قالب‌های HTML
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   └── [سایر قالب‌ها]
│
├── static/               # فایل‌های استاتیک
│   ├── css/
│   ├── js/
│   └── img/
│
└── [فایل‌های محاسباتی]  # فایل‌های Python برای محاسبات
    ├── sugercalc.py
    ├── graincalc.py
    ├── fruitcalc.py
    ├── bloodalco.py
    └── ...
```

## 🛠️ تکنولوژی‌های استفاده شده

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Icons**: Font Awesome

## 📝 استفاده

1. پس از اجرای برنامه، صفحه اصلی را باز کنید
2. ماشین حساب مورد نظر خود را انتخاب کنید
3. مقادیر را وارد کنید
4. روی دکمه "محاسبه" کلیک کنید
5. نتایج را مشاهده کنید

## 🔧 توسعه

برای توسعه و بهبود پروژه:

1. Fork کردن پروژه
2. ایجاد یک branch جدید (`git checkout -b feature/AmazingFeature`)
3. Commit کردن تغییرات (`git commit -m 'Add some AmazingFeature'`)
4. Push کردن به branch (`git push origin feature/AmazingFeature`)
5. باز کردن Pull Request

## ⚠️ نکات مهم

- این برنامه برای اهداف آموزشی و تحقیقاتی طراحی شده است
- در استفاده از محاسبات الکل خون، همیشه احتیاط کنید و رانندگی در حالت مستی ممنوع است
- نتایج محاسبات تقریبی هستند و ممکن است با شرایط واقعی متفاوت باشند

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است.

## 👥 مشارکت

مشارکت‌ها، پیشنهادات و گزارش باگ‌ها همیشه خوش‌آمد هستند!

## 📧 تماس

برای سوالات و پشتیبانی، لطفاً یک Issue در GitHub ایجاد کنید.

---

**نسخه**: 1.0.0  
**آخرین بروزرسانی**: 2025

---

## English Description

This project, "chemical-process-calculator", is a Flask-based web application designed to provide a comprehensive suite of calculators for various parameters encountered in chemical processes, with a particular emphasis on fermentation and distillation. The application integrates a range of specialized computational tools to assist users in optimizing and understanding key aspects of these processes.

Key functionalities include:

*   **Specific Gravity and Alcohol Content Analysis:** The SPN Calculator facilitates the determination of specific gravity and potential alcohol yield, crucial for fermentation monitoring.
*   **Thermal Dynamics:** The Heat Time Calculator and Column Heat Calculator enable precise calculation of heating durations and thermal energy requirements for process optimization and energy efficiency.
*   **Distillation Column Optimization:** Two distinct Reflux Calculators provide tools for determining optimal reflux ratios and related operational parameters, critical for achieving desired separation efficiencies in distillation.
*   **Azeotropic Mixture Analysis:** The Azeotrope Calculator assists in identifying and characterizing azeotropic mixtures, which are fundamental to understanding distillation limitations and strategies.
*   **Fermentation Process Modeling:** The Sugar, Grain, and Fruit Calculators provide specialized tools for feedstock analysis and fermentation parameter prediction, while the Fermentation Calculator offers a broader overview of the fermentation process.
*   **Refractometry and Concentration:** The Refractometer Calculator aids in interpreting refractometric data, essential for accurate concentration measurements in various solutions.
*   **Spirit Production Optimization:** The Spirit Run Calculator is tailored for optimizing spirit distillation, considering factors such as cuts and yield.
*   **Ancillary Chemical Engineering Tools:** Additional calculators include the Element Power Calculator for electrical heating elements, Remaining Liquid Calculator for volume assessments, and Boiling Point Calculator for phase equilibrium analysis.

This platform serves as an invaluable resource for chemical engineers, distillers, brewers, and researchers, offering precise computational support for process design, control, and troubleshooting in chemical and biochemical industries.
