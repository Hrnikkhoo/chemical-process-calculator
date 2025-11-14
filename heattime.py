from flask import request

class HeatTime:
    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}
        
        try:
            # دریافت مقادیر ورودی
            v = float(request.form.get('v', 20))      # حجم (لیتر)
            w = float(request.form.get('w', 2000))    # توان (وات)
            t1 = float(request.form.get('t1', 25))    # دمای اولیه (°C)
            t2 = float(request.form.get('t2', 85))    # دمای نهایی (°C)
            
            # دریافت راندمان (اختیاری)
            e = float(request.form.get('ef', 100)) if request.form.get('ef_trigger') == 'on' else 100
            
            # اعتبارسنجی ورودی‌ها
            if v <= 0:
                return {'error': 'حجم باید بیشتر از 0 باشد'}
            if w <= 0:
                return {'error': 'توان باید بیشتر از 0 باشد'}
            if t1 < 0 or t1 > 200:
                return {'error': 'دمای اولیه باید بین 0 تا 200 درجه سانتی‌گراد باشد'}
            if t2 < 0 or t2 > 200:
                return {'error': 'دمای نهایی باید بین 0 تا 200 درجه سانتی‌گراد باشد'}
            if t2 <= t1:
                return {'error': 'دمای نهایی باید بیشتر از دمای اولیه باشد'}
            if e <= 0 or e > 100:
                return {'error': 'راندمان باید بین 0 تا 100 درصد باشد'}
            
            # محاسبه زمان گرم شدن با استفاده از فرمول فیزیکی
            # Q = m * c * ΔT (انرژی مورد نیاز)
            # P = W * efficiency (توان موثر)
            # t = Q / P (زمان)
            
            # فرض می‌کنیم که مایع آب است (می‌توان بعداً برای مخلوط الکل-آب گسترش داد)
            density = 1.0  # kg/L (آب)
            specific_heat = 4186  # J/kg°C (آب)
            
            # محاسبه جرم
            mass_kg = v * density
            
            # تفاوت دما
            delta_temp = t2 - t1
            
            # محاسبه انرژی مورد نیاز (ژول)
            energy_needed = mass_kg * specific_heat * delta_temp
            
            # محاسبه توان موثر (وات)
            efficiency = e / 100.0
            effective_power = w * efficiency
            
            # محاسبه زمان (ثانیه)
            time_seconds = energy_needed / effective_power
            
            # تبدیل به دقیقه
            time_minutes = time_seconds / 60.0
            
            return {
                'result': {
                    'time_minutes': round(time_minutes, 1),
                    'volume': v,
                    'power': w,
                    'initial_temp': t1,
                    'final_temp': t2,
                    'efficiency': e
                }
            }
        
        except ValueError:
            return {'error': 'مقادیر ورودی باید عددی باشند'}
        except Exception as e:
            return {'error': 'خطا در انجام محاسبات'}
