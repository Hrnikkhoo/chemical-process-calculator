from flask import render_template, request

class Spn:
    @staticmethod
    def calculate():
        v = None
        w = None
        plate = None
        result_message = None
        result_type = None
    
        if request.method == 'POST':
            try:
                h = float(request.form['h_column'])
                d = float(request.form['d_column'])
                mesh_type = request.form['mesh_type']
                
                if h > 10000 or h <= 0:
                    result_message = 'ارتفاع ستون باید بین 0 تا 10000 میلیمتر باشد'
                    result_type = 'error'
                else:
                    spn, coef = mesh_type.split('_')
                    spn = float(spn)
                    coef = float(coef)
                    
                    radius_mm = d / 2
                    radius_cm = radius_mm / 10
                    height_cm = h / 10
                    
                    cross_section = 3.14159 * (radius_cm ** 2)
                    v = cross_section * height_cm / 1000
                    
                    w = v * spn
                    plate = h / (coef * 10)
                    
                    result_message = 'محاسبه با موفقیت انجام شد'
                    result_type = 'success'

            except (ValueError, KeyError) as e:
                print(f"Error: {str(e)}")
                result_message = "لطفاً تمام فیلدها را به درستی پر کنید"
                result_type = 'error'
        
        return {
            'v': round(v, 4) if v is not None else None,
            'w': round(w, 4) if w is not None else None,
            'plate': round(plate, 3) if plate is not None else None,
            'result_message': result_message,
            'result_type': result_type
        }

#spncalculate = Spn.calculate()