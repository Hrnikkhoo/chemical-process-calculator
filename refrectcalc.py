from flask import request
import math

class RefrectCalc:
    # AS3 refractometer correction table
    # Temperature in °C as first key, sugar percentage as second key
    AS3_TABLE = {
        10: {10: 9.85, 15: 14.80, 20: 19.75, 25: 24.70},
        15: {10: 9.90, 15: 14.87, 20: 19.84, 25: 24.81},
        20: {10: 10.00, 15: 15.00, 20: 20.00, 25: 25.00},
        25: {10: 10.10, 15: 15.13, 20: 20.16, 25: 25.19},
        30: {10: 10.20, 15: 15.26, 20: 20.32, 25: 25.38}
    }

    @staticmethod
    def closest_left(keys, target):
        """Find closest value in sorted list that is less than or equal to target"""
        keys = sorted([float(k) for k in keys])
        return max([k for k in keys if k <= target], default=None)

    @staticmethod
    def closest_right(keys, target):
        """Find closest value in sorted list that is greater than or equal to target"""
        keys = sorted([float(k) for k in keys])
        return min([k for k in keys if k >= target], default=None)

    @staticmethod
    def linear_interpolation(x1, x, x2, y1, y2):
        """Perform linear interpolation"""
        if x1 == x2:
            return y1
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

    @staticmethod
    def calculate():
        if request.method != 'POST':
            return {}

        try:
            temperature = float(request.form.get('t', 20))
            sugar_percent = float(request.form.get('p', 15))
            
            result = None
            
            # Find exact temperature match
            if temperature in RefrectCalc.AS3_TABLE:
                values = RefrectCalc.AS3_TABLE[temperature]
                if sugar_percent in values:
                    result = values[sugar_percent]
                else:
                    # Interpolate sugar percentage
                    sugar_keys = list(values.keys())
                    left = RefrectCalc.closest_left(sugar_keys, sugar_percent)
                    right = RefrectCalc.closest_right(sugar_keys, sugar_percent)
                    
                    if left is not None and right is not None:
                        result = RefrectCalc.linear_interpolation(
                            left, sugar_percent, right,
                            values[left], values[right]
                        )
            else:
                # Find temperature range and interpolate
                temp_keys = sorted(list(RefrectCalc.AS3_TABLE.keys()))
                left_temp = RefrectCalc.closest_left(temp_keys, temperature)
                right_temp = RefrectCalc.closest_right(temp_keys, temperature)
                
                if left_temp is not None and right_temp is not None:
                    # Get values for both temperatures
                    left_values = RefrectCalc.AS3_TABLE[left_temp]
                    right_values = RefrectCalc.AS3_TABLE[right_temp]
                    
                    if sugar_percent in left_values and sugar_percent in right_values:
                        # Direct interpolation between temperatures
                        result = RefrectCalc.linear_interpolation(
                            left_temp, temperature, right_temp,
                            left_values[sugar_percent],
                            right_values[sugar_percent]
                        )
                    else:
                        # Double interpolation required
                        sugar_keys = list(left_values.keys())
                        left_sugar = RefrectCalc.closest_left(sugar_keys, sugar_percent)
                        right_sugar = RefrectCalc.closest_right(sugar_keys, sugar_percent)
                        
                        if left_sugar is not None and right_sugar is not None:
                            # Interpolate at lower temperature
                            left_result = RefrectCalc.linear_interpolation(
                                left_sugar, sugar_percent, right_sugar,
                                left_values[left_sugar], left_values[right_sugar]
                            )
                            # Interpolate at higher temperature
                            right_result = RefrectCalc.linear_interpolation(
                                left_sugar, sugar_percent, right_sugar,
                                right_values[left_sugar], right_values[right_sugar]
                            )
                            # Interpolate between temperatures
                            result = RefrectCalc.linear_interpolation(
                                left_temp, temperature, right_temp,
                                left_result, right_result
                            )
                if result is None:
                    return {'error': 'مقادیر خارج از محدوده هستند'}
            
            return {
                'temperature': temperature,
                'reading': sugar_percent,
                'corrected': round(result, 2),
                'correction': round(result - sugar_percent, 2)
            }
            
        except Exception as e:
            return {'error': str(e)}