from flask import request

class GrainCalc:
    # Constants
    CTS = 0.9  # Conversion coefficient of starch to sugar
    SAS = 0.51  # Specific volume of alcohol
    SV = 1.59  # Sugar volume coefficient
    SD = 40  # Standard strength

    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}

        # Get form data
        calculation_type = request.form.get('by', '')
        hydromodule = float(request.form.get('gm', 0))
        water_volume = float(request.form.get('v', 0))
        efficiency = float(request.form.get('ef', 100))
        efficiency_40 = 100

        # Get raw materials data from form
        raw_materials = []
        i = 0
        while True:
            mass = request.form.get(f'ms_{i}')
            if not mass:
                break
                
            raw_materials.append({
                'mass': float(mass),
                'starch': float(request.form.get(f'krah_{i}', 0)),
                'sugar': float(request.form.get(f'sah_{i}', 0))
            })
            i += 1

        if not raw_materials:
            return {'error': 'At least one type of raw material must be added'}

        if not 0 <= efficiency <= 100:
            return {'error': 'Efficiency must be between 0 and 100'}

        # Calculate totals
        total_mass = 0
        total_starch = 0
        total_sugar = 0
        total_suspension_volume = 0

        for material in raw_materials:
            mass = material['mass']
            sugar_percent = material['sugar']
            starch_percent = material['starch']

            if sugar_percent == 100:
                total_suspension_volume += mass * GrainCalc.SV
            elif starch_percent == 100:
                total_suspension_volume += (1 / 1.4) * mass
            else:
                total_suspension_volume += (1 / 1.6) * mass

            total_mass += mass
            total_starch += mass * starch_percent / 100
            total_sugar += mass * sugar_percent / 100

        avg_starch_percent = (total_starch * 100) / total_mass
        avg_sugar_percent = (total_sugar * 100) / total_mass

        # Calculate by water volume or hydromodule
        if calculation_type == 'by_water_volume':
            water_vol = water_volume
            hydromodule = water_vol / total_mass
        else:  # by_hydromodule
            water_vol = total_mass * hydromodule
            
        sugar_count = (total_mass * avg_sugar_percent / 100) + \
                     (total_mass * avg_starch_percent / 100) * GrainCalc.CTS
        alcohol_volume = (efficiency / 100) * sugar_count * GrainCalc.SAS
        braga_strength = alcohol_volume * 100 / water_vol
        volume_40 = (efficiency_40 / 100) * water_vol * braga_strength / GrainCalc.SD
        sugar_saturation = (sugar_count / (sugar_count + water_vol)) * 100
        total_suspension_volume += float(water_vol)

        return {
            'hydromodule': round(hydromodule, 1),
            'water_volume': round(water_vol, 3),
            'alcohol_volume': round(alcohol_volume, 3),
            'sugar_saturation': round(sugar_saturation, 2),
            'sugar_mass': round(sugar_count, 3),
            'braga_strength': round(braga_strength, 2),
            'volume_40': round(volume_40, 3),
            'total_volume': round(total_suspension_volume, 3),
            'total_mass': round(total_mass, 3),
            'total_starch_percent': round(avg_starch_percent, 2),
            'total_sugar_percent': round(avg_sugar_percent, 2)
        }