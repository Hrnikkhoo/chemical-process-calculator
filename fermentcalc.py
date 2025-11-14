from flask import request
import logging


# Create logger for this module
logger = logging.getLogger(__name__)

class FermentCalc:
    """محاسبه‌گر میزان الکل در فرآیند تخمیر"""
    
    # Constants
    MIN_SUGAR_CONTENT = 0
    MAX_SUGAR_CONTENT = 25
    SAS = 0.51  # Specific volume of alcohol
    SV = 1.59   # Sugar volume coefficient
    SD = 40     # Standard strength

    @classmethod
    def calculate(cls):
        """محاسبه میزان الکل بر اساس درصد قند اولیه و نهایی"""
        try:
            logger.info("شروع محاسبه میزان الکل")
            start_sugar = float(request.form.get('start', 0))
            end_sugar = float(request.form.get('end', 0))
            
            logger.debug(f"مقادیر ورودی: قند اولیه={start_sugar}, قند نهایی={end_sugar}")

            # اعتبارسنجی مقادیر ورودی
            if not cls.MIN_SUGAR_CONTENT <= start_sugar <= cls.MAX_SUGAR_CONTENT:
                logger.warning(f"میزان قند اولیه {start_sugar} خارج از محدوده مجاز است")
                return {'error': 'میزان قند اولیه باید بین 0 تا 25 درصد باشد'}

            if not cls.MIN_SUGAR_CONTENT <= end_sugar <= cls.MAX_SUGAR_CONTENT:
                logger.warning(f"میزان قند نهایی {end_sugar} خارج از محدوده مجاز است")
                return {'error': 'میزان قند نهایی باید بین 0 تا 25 درصد باشد'}

            if end_sugar >= start_sugar:
                logger.warning("میزان قند نهایی نمی‌تواند بیشتر یا مساوی قند اولیه باشد")
                return {'error': 'میزان قند نهایی باید کمتر از قند اولیه باشد'}

            # محاسبه میزان الکل
            sugar_consumed = start_sugar - end_sugar
            alcohol_content = sugar_consumed * cls.SAS
            alcohol_percentage = (alcohol_content / (100 + alcohol_content)) * 100

            logger.info(f"محاسبه انجام شد: میزان الکل={alcohol_percentage:.2f}%")

            return {
                'result': {
                    'alcohol_content': f"{alcohol_percentage:.2f}",
                    'unit': '%'
                }
            }

        except ValueError as e:
            logger.error(f"خطای تبدیل مقدار: {e}")
            return {'error': 'مقادیر ورودی باید عددی باشند'}
        except Exception as e:
            logger.error(f"خطای غیرمنتظره در محاسبات: {e}", exc_info=True)
            return {'error': 'خطا در انجام محاسبات'}