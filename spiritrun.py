from flask import request
import math

class SpiritRunCalc:
    # Constants from calc.js
    PARAMS = {
        'sas': 0.682,     # sweetness coefficient
        'sv': 0.63,       # alcohol coefficient
        'cts': 1.11,      # conversion coefficient
        'kss': 0.025,     # specialty parameter 1
        'kss_w': 0.05,    # specialty parameter 2
        'pas': 0.78927,   # alcohol density
        'kip': 78.37,     # boiling point
        't_w': 4.2        # water temperature
    }

    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}

        try:
            # Get basic values with defaults
            vss = float(request.form.get('vss', 20))    # Raw alcohol volume
            sss = float(request.form.get('sss', 21))    # Raw alcohol content
            se = float(request.form.get('se', 65))      # Output alcohol content
            dg = float(request.form.get('dg', 8))       # Heads percentage
            dh = float(request.form.get('dh', 5))       # Tails percentage
            
            # Get optional values
            tv = float(request.form.get('tv', 20)) if request.form.get('tv_trigger') == 'on' else None
            ts = float(request.form.get('ts', 20)) if request.form.get('ts_trigger') == 'on' else None
            dpg = float(request.form.get('dpg', 0)) if request.form.get('dpg_trigger') == 'on' else None
            dph = float(request.form.get('dph', 0)) if request.form.get('dph_trigger') == 'on' else None
            p = float(request.form.get('p', 760)) if request.form.get('p_trigger') == 'on' else 760
            ef = float(request.form.get('ef', 100)) if request.form.get('ef_trigger') == 'on' else 100
            vo = float(request.form.get('vo', 0)) if request.form.get('vo_trigger') == 'on' else None

            # Apply temperature correction if needed (like JavaScript)
            if tv is not None:
                se = SpiritRunCalc.temperature_correction(tv, se)
            
            if ts is not None:
                sss = SpiritRunCalc.temperature_correction(ts, sss)

            # Input validation
            if p > 1495 or p < 200:
                return {'error': 'فشار باید بین 200 تا 1495 میلی‌متر جیوه باشد'}

            if ef < 0 or ef > 100:
                return {'error': 'راندمان باید بین 0 تا 100 درصد باشد'}

            if sss < 0 or sss > 100 or se < 0 or se > 100:
                return {'error': 'میزان الکل باید بین 0 تا 100 درصد باشد'}

            # Calculate boiling point first
            t_kip = SpiritRunCalc.calculate_boiling_point(sss, p)

            # Core calculations - following JavaScript logic exactly
            # VAS = VSS * SSS / 100
            vas = vss * sss / 100     # Absolute alcohol volume
            
            # VG = VAS * DG / 100
            vg = vas * dg / 100       # Heads volume
            
            # VH = VAS * DH / 100
            vh = vas * dh / 100       # Tails volume
            
            # Initialize r0 and r1 like in JavaScript
            r0 = vas - vg - vh        # Remaining alcohol
            r1 = -vh - vg             # Volume adjustment factor
            
            # Initialize pre-heads and pre-tails volumes
            vpg = 0  # Pre-heads volume
            vph = 0  # Pre-tails volume

            # Handle optional pre-heads and pre-tails (like JavaScript)
            if dpg is not None:
                # VPG = VAS * DPG / 100
                vpg = vas * dpg / 100
                r0 -= vpg
                r1 -= vpg

            if dph is not None:
                # VPH = VAS * DPH / 100
                vph = vas * dph / 100
                r0 -= vph
                r1 -= vph

            # VT = (EF / 100) * r0 / (SE / 100)
            # Body volume calculation (exactly like JavaScript line 77)
            vt = (ef / 100) * r0 / (se / 100)
            
            # VB = VSS - VT + r1
            # Remaining liquid in cube (exactly like JavaScript line 78)
            vb = vss - vt + r1

            # Initialize results
            results = {
                'heads_volume': round(vg, 3),
                'tails_volume': round(vh, 3),
                'pre_heads_volume': round(vpg, 3),
                'pre_tails_volume': round(vph, 3),
                'body_volume': round(vt, 3),
                'pick_body_time': None,
                'absolute_alcohol': round(vas, 3),
                'cube_liquid_rest': round(vb, 3),
                'boiling_point': round(t_kip, 2)
            }

            # Calculate collection time if sampling rate is provided
            # VOT = VT / (VO / 60)
            if vo is not None and vo > 0:
                total_minutes = round(vt / (vo / 60))
                hours = total_minutes // 60
                minutes = total_minutes % 60
                results['pick_body_time'] = f"{hours} ساعت و {minutes} دقیقه"

            return {'result': results}

        except ValueError as e:
            return {'error': 'مقادیر ورودی باید عددی باشند'}
        except Exception as e:
            return {'error': 'خطا در انجام محاسبات'}

    @staticmethod
    def linear_interpolation(x0, x, x1, y0, y1):
        """درون‌یابی خطی برای محاسبه نقطه جوش"""
        return y0 + ((y1 - y0) / (x1 - x0)) * (x - x0)

    @staticmethod
    def temperature_correction(temperature, alcohol_percent):
        """
        تصحیح درصد الکل بر اساس دما
        فرمول تقریبی: اگر دما بالاتر از 20°C باشد، درصد الکل کمتر نشان داده می‌شود
        """
        if temperature == 20:
            return alcohol_percent
        
        # تصحیح دما: برای هر درجه تفاوت از 20°C، حدود 0.1% تغییر
        # این یک فرمول تقریبی است
        correction = (temperature - 20) * 0.1
        corrected = alcohol_percent - correction
        
        # محدود کردن به بازه معقول
        return max(0, min(100, corrected))

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
                20: 88.50,    # 89.4 در منابع دیگر
                25: 87.10,
                30: 86.00,    # 86.7 در منابع دیگر
                35: 85.20,
                40: 84.50,    # 84.9 در منابع دیگر
                45: 84.00,
                50: 83.60,    # 83.9 در منابع دیگر
                55: 83.20,
                60: 82.80,    # 82.9 در منابع دیگر
                65: 82.40,
                70: 82.00,    # 81.8 در منابع دیگر
                75: 81.50,
                80: 81.00,    # 80.7 در منابع دیگر
                85: 80.30,
                90: 79.60,    # 79.4 در منابع دیگر
                95: 79.00,    # 78.8 در منابع دیگر
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
                    bp = SpiritRunCalc.linear_interpolation(x0, alcohol_percent, x1, y0, y1)

            # اعمال تصحیح فشار
            # فرمول تصحیح فشار: T = T0 * (P/P0)^0.19
            # که در آن P0 = 760 mmHg و T0 نقطه جوش در فشار استاندارد است
            if pressure != 760:
                pressure_factor = (pressure / 760) ** 0.19
                bp = bp * pressure_factor

            return round(bp, 2)

        except Exception as e:
            # محاسبه ساده به عنوان پشتیبان در صورت خطا
            base_temp = 78.37  # نقطه جوش اتانول خالص
            water_temp = 100.0  # نقطه جوش آب خالص
            temp_range = water_temp - base_temp
            alcohol_factor = 1 - (alcohol_percent / 100)
            
            # محاسبه نقطه جوش تقریبی
            bp = base_temp + (temp_range * alcohol_factor)
            
            # اعمال تصحیح فشار
            if pressure != 760:
                pressure_factor = (pressure / 760) ** 0.19
                bp = bp * pressure_factor
            
            return round(bp, 2)