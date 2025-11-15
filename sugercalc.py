from flask import request

# ثابت‌ها
sv = 0.63
sas = 0.682
sd = 40
ef40 = 100

ch4n2o2 = 2
kh2po4 = 4.5
mgso4 = 2
nacl = 4
kcl = 10
mnso4 = 0.6
znso4 = 0.6

def safe_float(value, default=0):
    """تبدیل امن مقدار به float - اگر خالی یا نامعتبر باشد مقدار پیش‌فرض برمی‌گرداند"""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        if not value.strip():
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

class SugerCalc:
    @staticmethod
    def calculate():
        try:
            method = request.form.get("by", "")
            if not method:
                return {"error": "روش محاسبه انتخاب نشده است"}
            
            ms = safe_float(request.form.get("ms"), 0)
            ef = safe_float(request.form.get("ef"), 100)

            if method == "by_hydromodule":
                gm = safe_float(request.form.get("gm"), 0)
                vW = ms * gm
                vWTotal = vW + ms * sv
                vAS = ef / 100 * ms * sas
                sb = (ms / (ms + vW)) * 100 if (ms + vW) > 0 else 0
                s = vAS * 100 / vWTotal if vWTotal > 0 else 0
                v40 = ef40 / 100 * vWTotal * s / sd

            elif method == "by_water_volume":
                v = safe_float(request.form.get("v"), 0)
                gm = v / ms if ms > 0 else 0
                vWTotal = v + ms * sv
                vAS = ef / 100 * ms * sas
                sb = (ms / (ms + v)) * 100 if (ms + v) > 0 else 0
                s = vAS * 100 / vWTotal if vWTotal > 0 else 0
                v40 = ef40 / 100 * vWTotal * s / sd
                vW = v

            elif method == "by_total_volume":
                vb = safe_float(request.form.get("vb"), 0)
                vW = vb - ms * sv
                gm = vW / ms if ms > 0 else 0
                vAS = ef / 100 * ms * sas
                sb = (ms / (ms + vW)) * 100 if (ms + vW) > 0 else 0
                s = vAS * 100 / vb if vb > 0 else 0
                v40 = ef40 / 100 * vb * s / sd
                vWTotal = vb

            else:
                return {"error": "روش انتخابی نامعتبر است"}

            result = {
                "vW": round(vW, 3),
                "gm": f"1 : {round(gm, 1)}",
                "vWTotal": round(vWTotal, 3),
                "vAS": round(vAS, 3),
                "sb": round(sb, 1),
                "s": round(s, 2),
                "v40": round(v40, 3),
                "nutrients": {
                    "carbamide": round(ch4n2o2 * ms, 2),
                    "kh2po4": round(kh2po4 * ms, 2),
                    "mgso4": round(mgso4 * ms, 2),
                    "nacl": round(nacl * ms, 2),
                    "kcl": round(kcl * ms, 2),
                    "mnso4": round(mnso4 * ms, 2),
                    "znso4": round(znso4 * ms, 2),
                }
            }
            return result
        except Exception as e:
            return {"error": str(e)}