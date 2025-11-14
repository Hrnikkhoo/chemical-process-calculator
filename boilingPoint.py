from flask import request
import math

class BoilingPointCalc:
    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}
        
        try:
            # دریافت مقادیر ورودی
            s = float(request.form.get('s', 40))  # درصد الکل مایع (%)
            p = float(request.form.get('p', 300))  # فشار در مخزن (میلی‌متر جیوه)
            
            # دریافت دمای مایع (اختیاری) - برای تصحیح درصد الکل
            t = float(request.form.get('t', 20)) if request.form.get('t_trigger') == 'on' else None
            
            # اعمال تصحیح دما اگر فعال باشد
            if t is not None:
                s = BoilingPointCalc.temperature_correction(t, s)
            
            # اعتبارسنجی ورودی‌ها
            if s < 0 or s > 100:
                return {'error': 'درصد الکل باید بین 0 تا 100 باشد'}
            if p > 1495 or p < 50:
                return {'error': 'فشار باید بین 50 تا 1495 میلی‌متر جیوه باشد'}
            
            # محاسبه نقطه جوش
            boiling_point = BoilingPointCalc.calculate_boiling_point(s, p)
            
            return {
                'result': {
                    'boiling_point': boiling_point,
                    'alcohol_percent': s,
                    'pressure': p
                }
            }
        
        except ValueError:
            return {'error': 'مقادیر ورودی باید عددی باشند'}
        except Exception as e:
            return {'error': 'خطا در انجام محاسبات'}
    
    @staticmethod
    def linear_interpolation(x0, x, x1, y0, y1):
        """درون‌یابی خطی برای محاسبه نقطه جوش"""
        if x1 == x0:
            return y0
        return y0 + ((y1 - y0) / (x1 - x0)) * (x - x0)
    
    @staticmethod
    def calculate_boiling_point(alcohol_percent, pressure):
        """
        محاسبه نقطه جوش مخلوط الکل-آب بر اساس درصد الکل و فشار
        استفاده از جدول استاندارد و فرمول تصحیح فشار
        """
        try:
            # جدول دقیق نقطه جوش برای درصدهای مختلف الکل در فشار 760 میلیمتر جیوه
            # این مقادیر بر اساس داده‌های تجربی برای مخلوط اتانول-آب است
            boiling_points = {
                0: 100.00,    # آب خالص
                5: 95.90,
                10: 92.60,
                15: 90.20,
                20: 88.50,
                25: 87.10,
                30: 86.00,
                35: 85.20,
                40: 84.50,
                45: 84.00,
                50: 83.60,
                55: 83.20,
                60: 82.80,
                65: 82.40,
                70: 82.00,
                75: 81.50,
                80: 81.00,
                85: 80.30,
                90: 79.60,
                95: 79.00,
                100: 78.37    # اتانول خالص
            }
            
            # محدود کردن درصد الکل به بازه معتبر
            alcohol_percent = max(0, min(100, alcohol_percent))
            
            # پیدا کردن نقاط مجاور برای درون‌یابی
            concentrations = sorted(boiling_points.keys())
            
            # اگر دقیقاً روی یک نقطه داده باشیم
            if alcohol_percent in boiling_points:
                bp = boiling_points[alcohol_percent]
            else:
                # پیدا کردن بازه مناسب برای درون‌یابی
                x0 = max([c for c in concentrations if c <= alcohol_percent], default=0)
                x1 = min([c for c in concentrations if c >= alcohol_percent], default=100)
                
                if x0 == x1:
                    bp = boiling_points[x0]
                else:
                    # درون‌یابی خطی بین دو نقطه
                    y0 = boiling_points[x0]
                    y1 = boiling_points[x1]
                    bp = BoilingPointCalc.linear_interpolation(x0, alcohol_percent, x1, y0, y1)

            # اعمال تصحیح فشار
            # فرمول تصحیح فشار برای مخلوط الکل-آب
            # استفاده از فرمول دقیق‌تر با توان بالاتر برای دقت بیشتر
            if pressure != 760:
                # برای فشارهای کم، از توان بالاتر استفاده می‌کنیم
                # این باعث می‌شود نقطه جوش سریع‌تر کاهش یابد
                pressure_factor = (pressure / 760.0) ** 0.36
                bp = bp * pressure_factor

            return round(bp, 2)

        except Exception:
            # محاسبه ساده به عنوان پشتیبان در صورت خطا
            base_temp = 78.37  # نقطه جوش اتانول خالص
            water_temp = 100.0  # نقطه جوش آب خالص
            temp_range = water_temp - base_temp
            alcohol_factor = 1 - (alcohol_percent / 100)
            
            # محاسبه نقطه جوش تقریبی
            bp = base_temp + (temp_range * alcohol_factor)
            
            # اعمال تصحیح فشار
            if pressure != 760:
                pressure_factor = (pressure / 760.0) ** 0.36
                bp = bp * pressure_factor
            
            return round(bp, 2)
    
    @staticmethod
    def temperature_correction(temperature, alcohol_percent):
        """
        تصحیح درصد الکل بر اساس دما
        فرمول تقریبی: اگر دما بالاتر از 20°C باشد، درصد الکل کمتر نشان داده می‌شود
        """
        if temperature == 20:
            return alcohol_percent
        
        # تصحیح دما: برای هر درجه تفاوت از 20°C، حدود 0.1% تغییر
        correction = (temperature - 20) * 0.1
        corrected = alcohol_percent - correction
        
        # محدود کردن به بازه معقول
        return max(0, min(100, corrected))

