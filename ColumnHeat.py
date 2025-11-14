from flask import request

class ColumnHeatCalc:
    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}
        
        try:
            # دریافت مقادیر ورودی
            v = float(request.form.get('v', 70))      # مصرف آب (لیتر در ساعت)
            tin = float(request.form.get('tin', 20))  # دمای آب ورودی (°C)
            tout = float(request.form.get('tout', 45)) # دمای آب خروجی (°C)
            w = float(request.form.get('w', 3))       # توان مصرفی (کیلووات)
            
            # اعتبارسنجی ورودی‌ها
            if v <= 0:
                return {'error': 'مصرف آب باید بیشتر از 0 باشد'}
            if tin < 0 or tin > 100:
                return {'error': 'دمای آب ورودی باید بین 0 تا 100 درجه سانتی‌گراد باشد'}
            if tout < 0 or tout > 100:
                return {'error': 'دمای آب خروجی باید بین 0 تا 100 درجه سانتی‌گراد باشد'}
            if tout <= tin:
                return {'error': 'دمای آب خروجی باید بیشتر از دمای آب ورودی باشد'}
            if w <= 0:
                return {'error': 'توان مصرفی باید بیشتر از 0 باشد'}
            
            # محاسبات طبق فرمول‌های مرجع
            # V = V / (60 * 60) - تبدیل مصرف آب از لیتر در ساعت به لیتر بر ثانیه
            v_sec = v / (60 * 60)
            
            # W1 = V * (4.2 * (Tout - Tin)) - قدرت وقتی برای خودت کار می‌کنی
            w1 = v_sec * (4.2 * (tout - tin))
            
            # W2 = W1 + (W1 * 0.04) - قدرت در انتخاب (4% بیشتر)
            w2 = w1 + (w1 * 0.04)
            
            # L1abs = W - W1 - اتلاف حرارت هنگام کار برای خودتان (مطلق)
            l1abs = w - w1
            
            # L1rel = L1abs / W * 100 - اتلاف حرارت هنگام کار برای خودتان (نسبی %)
            l1rel = (l1abs / w) * 100 if w > 0 else 0
            
            # L2abs = W - W2 - اتلاف حرارت در طول انتخاب (مطلق)
            l2abs = w - w2
            
            # L2rel = L2abs / W * 100 - اتلاف حرارت در طول انتخاب (نسبی %)
            l2rel = (l2abs / w) * 100 if w > 0 else 0
            
            return {
                'result': {
                    'power_self': round(w1, 3),
                    'heat_loss_self_abs': round(l1abs, 3),
                    'heat_loss_self_rel': round(l1rel, 2),
                    'power_selection': round(w2, 3),
                    'heat_loss_selection_abs': round(l2abs, 3),
                    'heat_loss_selection_rel': round(l2rel, 2)
                }
            }
        
        except ValueError:
            return {'error': 'مقادیر ورودی باید عددی باشند'}
        except Exception as e:
            return {'error': 'خطا در انجام محاسبات'}

