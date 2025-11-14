from flask import request
import math

class RemainingLiquidCalc:
    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}
        
        try:
            # دریافت مقادیر ورودی
            d = float(request.form.get('d', 36))  # قطر مخزن (سانتی‌متر)
            h = float(request.form.get('h', 8))   # ارتفاع از پایین تا سطح المنت (سانتی‌متر)
            s = float(request.form.get('s', 10))  # درصد الکل مایع (%)
            
            # دریافت دمای مایع (اختیاری)
            t = float(request.form.get('t', 20)) if request.form.get('t_trigger') == 'on' else None
            
            # اعمال تصحیح دما اگر فعال باشد
            if t is not None:
                s = RemainingLiquidCalc.temperature_correction(t, s)
            
            # اعتبارسنجی ورودی‌ها
            if d <= 0:
                return {'error': 'قطر مخزن باید بیشتر از 0 باشد'}
            if h <= 0:
                return {'error': 'ارتفاع باید بیشتر از 0 باشد'}
            if s < 0 or s > 100:
                return {'error': 'درصد الکل باید بین 0 تا 100 باشد'}
            
            # محاسبه حجم مایع باقی‌مانده در پایان تقطیر
            # M = ((3.14 * D²) / 4 * H) / 1000
            m = ((3.14 * d * d) / 4 * h) / 1000
            
            # محاسبه حداقل حجم مایعی که می‌توان در مخزن ریخت
            # V = M / ((100 - S) / 100)
            v = m / ((100 - s) / 100)
            
            return {
                'result': {
                    'remaining_volume': round(m, 3),
                    'min_volume': round(v, 3),
                    'diameter': d,
                    'height': h,
                    'alcohol_percent': s
                }
            }
        
        except ValueError:
            return {'error': 'مقادیر ورودی باید عددی باشند'}
        except Exception as e:
            return {'error': 'خطا در انجام محاسبات'}
    
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

