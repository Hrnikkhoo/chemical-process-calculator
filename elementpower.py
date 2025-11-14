import math

class ElementPower:
    @staticmethod
    def calculate(data):
        v1 = float(data.get('v1', 0))  # nominal power
        v2 = float(data.get('v2', 0))  # required power
        rr = float(data.get('rr', 0))  # resistance
        calc_by = data.get('by', '')

        result = []
        
        if calc_by == 'power':  # Calculate by power
            r = 220 * 220 / v1
            u = math.sqrt(v2 * r)
            result = [
                ['ولتاژ', round(u, 2), 'ولت'],
                ['مقاومت', round(r, 2), 'اهم']
            ]
        else:  # Calculate by resistance
            u = math.sqrt(v2 * rr)
            result = [
                ['ولتاژ', round(u, 2), 'ولت']
            ]
        
        return result