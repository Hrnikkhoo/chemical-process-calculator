class RefluxCalc:
    # ثابت‌های فیزیکی
    ETHANOL_DENSITY = 0.789  # چگالی اتانول (g/cm³)
    WATER_VAPORIZATION_HEAT = 2260  # گرمای نهان تبخیر آب (kJ/kg)
    ETHANOL_VAPORIZATION_HEAT = 855  # گرمای نهان تبخیر اتانول (kJ/kg)
    MINUTES_PER_HOUR = 60
    ML_PER_HOUR_TO_L = 0.06  # تبدیل میلی‌لیتر به لیتر در ساعت

    @staticmethod
    def calculate(data):
        try:
            # دریافت پارامترها
            alcohol_percent = float(data.get('alcohol_percent', 0))  # درصد الکل
            power_watts = float(data.get('power', 0))               # توان المنت به وات
            collection_rate = float(data.get('rate', 0))           # نرخ برداشت به لیتر در ساعت
            heat_loss_percent = float(data.get('heat_loss', 0))    # درصد اتلاف حرارت
            
            # بررسی اعتبار داده‌ها
            if alcohol_percent > 100 or alcohol_percent <= 0:
                return {"error": "میزان درصد الکل باید از 0 تا 100 باشد"}
            if power_watts <= 0:
                return {"error": "توان المنت باید بیشتر از 0 وات باشد"}
            if collection_rate <= 0:
                return {"error": "نرخ برداشت باید بیشتر از 0 لیتر در ساعت باشد"}
            if heat_loss_percent > 100 or heat_loss_percent < 0:
                return {"error": "مقدار درصد اتلاف حرارت باید از 0 تا 100 باشد"}
            
            # محاسبات نسبت رفلاکس
            # 1. تبدیل درصد الکل به نسبت (0-1)
            alcohol_ratio = alcohol_percent / 100
            
            # 2. محاسبه نرخ تبخیر بر اساس توان و گرمای نهان
            total_vaporization_heat = (
                ((1 - alcohol_ratio) * RefluxCalc.WATER_VAPORIZATION_HEAT) + 
                (alcohol_ratio * RefluxCalc.ETHANOL_VAPORIZATION_HEAT)
            )
            evaporation_rate = power_watts / total_vaporization_heat
            
            # 3. محاسبه نسبت رفلاکس با در نظر گرفتن چگالی و نرخ جمع‌آوری
            volume_ratio = (1 - alcohol_ratio) + (alcohol_ratio / RefluxCalc.ETHANOL_DENSITY)
            reflux_ratio = (
                volume_ratio * 
                evaporation_rate * 
                RefluxCalc.MINUTES_PER_HOUR / 
                (collection_rate / RefluxCalc.ML_PER_HOUR_TO_L)
            )
            
            # 4. اعمال اتلاف حرارتی
            final_reflux_ratio = reflux_ratio * (1 - (heat_loss_percent / 100))
            
            # گرد کردن نتیجه نهایی
            result_reflux = round(final_reflux_ratio, 1)
            
            return {
                "alcohol_percent": alcohol_percent,
                "power": power_watts,
                "rate": collection_rate,
                "heat_loss": heat_loss_percent,
                "reflux_ratio": result_reflux,
                "error": None
            }
            
        except Exception as e:
            return {"error": "خطا در محاسبات. لطفا مقادیر را بررسی کنید."}