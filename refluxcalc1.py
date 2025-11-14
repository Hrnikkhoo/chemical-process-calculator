class RefluxCalc1:
    # ثابت‌های فیزیکی
    ETHANOL_DENSITY = 0.789  # چگالی اتانول (g/cm³)
    EVAPORATION_HEAT = 925   # گرمای نهان تبخیر (kJ/kg)
    ALCOHOL_PERCENT = 96.6   # درصد الکل ثابت
    EFFICIENCY = 0.8        # بازده
    SECONDS_PER_HOUR = 3600

    @staticmethod
    def calculate(data):
        try:
            # دریافت پارامترها
            power_watts = float(data.get('power', 0))               # توان المنت به وات
            collection_rate = float(data.get('rate', 0))           # نرخ برداشت به لیتر در ساعت
            heat_loss_percent = float(data.get('heat_loss', 0))    # درصد اتلاف حرارت
            
            # بررسی اعتبار داده‌ها
            if power_watts <= 0:
                return {"error": "توان المنت باید بیشتر از 0 وات باشد"}
            if collection_rate <= 0:
                return {"error": "نرخ برداشت باید بیشتر از 0 لیتر در ساعت باشد"}
            if heat_loss_percent > 100 or heat_loss_percent < 0:
                return {"error": "مقدار درصد اتلاف حرارت باید از 0 تا 100 باشد"}
            
            # تبدیل توان از وات به کیلووات
            power_kw = power_watts / 1000
            
            # محاسبه نرخ جرمی (Mr)
            mass_rate = (power_kw / RefluxCalc1.EVAPORATION_HEAT) / RefluxCalc1.EFFICIENCY * RefluxCalc1.SECONDS_PER_HOUR
            
            # محاسبه نسبت رفلاکس اولیه
            reflux_ratio_initial = (mass_rate - collection_rate) / collection_rate
            
            # اعمال اتلاف حرارتی
            reflux_ratio = reflux_ratio_initial * (1 - (heat_loss_percent / 100))
            
            # گرد کردن نتیجه نهایی
            result_reflux = round(reflux_ratio, 1)
            
            return {
                "alcohol_percent": RefluxCalc1.ALCOHOL_PERCENT,
                "power": power_watts,
                "rate": collection_rate,
                "heat_loss": heat_loss_percent,
                "reflux_ratio": result_reflux,
                "error": None
            }
            
        except Exception as e:
            return {"error": "خطا در محاسبات. لطفا مقادیر را بررسی کنید."}