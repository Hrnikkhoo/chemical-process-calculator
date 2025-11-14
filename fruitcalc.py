from flask import request

class FruitCalc:
    # Constants
    SAS = 0.51  # Specific volume of alcohol
    SV = 1.59   # Sugar volume coefficient
    SD = 40     # Standard strength

    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}

        # Get calculation type
        calc_type = request.form.get('by', '')
        efficiency = float(request.form.get('ef', 100))
        efficiency_40 = 100
        replace_sugar_mass = float(request.form.get('ms', 0))
        add_sugar_mass = float(request.form.get('msd', 0))
        hydromodule = float(request.form.get('gm', 0))
        water_volume = float(request.form.get('vr', 0))

        # Get fruit materials data from form
        fruit_materials = []
        i = 0
        while True:
            volume = request.form.get(f'vs_{i}')
            if not volume:
                break
            
            fruit_materials.append({
                'volume': float(volume),
                'sugar': float(request.form.get(f'sah_{i}', 0))
            })
            i += 1

        if not fruit_materials:
            return {'error': 'At least one type of fruit must be added'}

        if not 0 <= efficiency <= 100:
            return {'error': 'Efficiency must be between 0 and 100'}

        # Calculate totals
        total_volume = 0
        total_sugar = 0

        for material in fruit_materials:
            volume = material['volume']
            sugar_percent = material['sugar']
            
            total_volume += volume
            total_sugar += volume * sugar_percent / 100

        # Calculate based on method
        if calc_type == 'by_sugar_mass_replace':
            # Calculate with sugar mass replacement
            mass_sugar_total = total_sugar + replace_sugar_mass
            mass_sugar_required = replace_sugar_mass - total_sugar
            volume_total = total_volume + water_volume + replace_sugar_mass * FruitCalc.SV
            hydromodule_calc = volume_total / mass_sugar_total
            alcohol_volume = efficiency / 100 * mass_sugar_total * FruitCalc.SAS
            sugar_brix = (mass_sugar_total / (mass_sugar_total + volume_total)) * 100
            strength = alcohol_volume * 100 / volume_total
            volume_40 = efficiency_40 / 100 * volume_total * strength / FruitCalc.SD

            if replace_sugar_mass == 0:
                mass_sugar_required = 0

            return {
                'add_sugar_mass': round(mass_sugar_required, 3),
                'hydromodule': round(hydromodule_calc, 1),
                'sugar_mass_in_juice': round(total_sugar, 3),
                'juice_volume': round(total_volume, 3),
                'wort_volume': round(volume_total, 3),
                'sugar_percentage': round(sugar_brix),
                'alcohol_strength': round(strength),
                'alcohol_volume': round(alcohol_volume, 3),
                'volume_40': round(volume_40, 3)
            }

        elif calc_type == 'by_add_sugar_mass':
            # Calculate with additional sugar mass
            mass_sugar_total = total_sugar + add_sugar_mass
            volume_total = total_volume + water_volume + add_sugar_mass * FruitCalc.SV
            hydromodule_calc = volume_total / mass_sugar_total
            alcohol_volume = efficiency / 100 * mass_sugar_total * FruitCalc.SAS
            sugar_brix = (mass_sugar_total / (mass_sugar_total + volume_total)) * 100
            strength = alcohol_volume * 100 / volume_total
            volume_40 = efficiency_40 / 100 * volume_total * strength / FruitCalc.SD

            return {
                'hydromodule': round(hydromodule_calc, 1),
                'juice_volume': round(total_volume, 3),
                'sugar_mass_in_juice': round(total_sugar, 3),
                'total_sugar_mass': round(mass_sugar_total, 3),
                'wort_volume': round(volume_total, 3),
                'sugar_percentage': round(sugar_brix),
                'alcohol_strength': round(strength),
                'alcohol_volume': round(alcohol_volume, 3),
                'volume_40': round(volume_40, 3)
            }

        else:  # by_hydromodule
            # Calculate with hydromodule
            volume_sugar_total = total_volume + water_volume
            mass_sugar_total = volume_sugar_total / hydromodule
            mass_sugar_required = mass_sugar_total - total_sugar
            volume_total = volume_sugar_total + mass_sugar_required * FruitCalc.SV
            sugar_brix = (mass_sugar_total / (mass_sugar_total + volume_total)) * 100
            alcohol_volume = efficiency / 100 * mass_sugar_total * FruitCalc.SAS
            strength = alcohol_volume * 100 / volume_total
            volume_40 = efficiency_40 / 100 * volume_total * strength / FruitCalc.SD

            return {
                'add_sugar_mass': round(mass_sugar_required, 3),
                'sugar_mass_in_juice': round(total_sugar, 3),
                'total_sugar_mass': round(mass_sugar_total, 3),
                'juice_volume': round(total_volume, 3),
                'wort_volume': round(volume_total, 3),
                'sugar_percentage': round(sugar_brix),
                'alcohol_strength': round(strength),
                'alcohol_volume': round(alcohol_volume, 3),
                'volume_40': round(volume_40, 3)
            }