from flask import Flask, render_template, request, url_for, jsonify
from spncalc import Spn
from heattime import HeatTime
from sugercalc import SugerCalc
from graincalc import GrainCalc
from fruitcalc import FruitCalc
from refrectcalc import RefrectCalc
from fermentcalc import FermentCalc
from spiritrun import SpiritRunCalc
from elementpower import ElementPower
from azeotropecalc import AzeotropeCalc
from refluxcalc import RefluxCalc
from refluxcalc1 import RefluxCalc1
from bloodalco import calculate_blood_alcohol
from remainingLiquid import RemainingLiquidCalc
from boilingPoint import BoilingPointCalc
from ColumnHeat import ColumnHeatCalc


app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')

#=======================================about====================
@app.route('/about', methods=['GET', 'POST'])
def about(): 
    return render_template('about.html')

#=======================================SpnCalculator====================
@app.route('/spncalc', methods=['GET', 'POST'])
def spncalc():
    if request.method == 'POST':
        result = Spn.calculate()
        return render_template('spncalc.html', **result)
    return render_template('spncalc.html')
#=======================================HeatCalculator=====================
@app.route('/heattime', methods=['GET', 'POST'])
def heattime():
    form_data = {}
    if request.method == 'POST':
        result = HeatTime.calculate()
        form_data = {
            'v': request.form.get('v', '20'),
            'w': request.form.get('w', '2000'),
            't1': request.form.get('t1', '25'),
            't2': request.form.get('t2', '85'),
            'ef': request.form.get('ef', '100'),
            'ef_trigger': request.form.get('ef_trigger') == 'on'
        }
        return render_template('heattime.html', result=result, form_data=form_data)
    return render_template('heattime.html', form_data=form_data)
#=======================================refluxCalculator1===================== 
@app.route('/refluxcalc', methods=['GET', 'POST'])
def refluxcalc():
    result = {
        'alcohol_percent': None,
        'power': None,
        'rate': None,
        'heat_loss': None,
        'reflux_ratio': None,
        'error': None
    }
    
    if request.method == 'POST':
        try:
            data = {
                'alcohol_percent': float(request.form.get('alcohol_percent', 0)),
                'power': float(request.form.get('power', 0)),
                'rate': float(request.form.get('rate', 0)),
                'heat_loss': float(request.form.get('heat_loss', 0))
            }
            result = RefluxCalc.calculate(data)
        except ValueError as e:
            result['error'] = "لطفا مقادیر عددی معتبر وارد کنید"
        except Exception as e:
            result['error'] = str(e)
    
    return render_template('refluxcalc.html', result=result)
#=======================================refluxCalculator2=====================
@app.route('/refluxcalc1', methods=['GET', 'POST'])
def refluxcalc1():
    result = {
        'alcohol_percent': None,
        'power': None,
        'rate': None,
        'heat_loss': None,
        'reflux_ratio': None,
        'error': None
    }
    
    if request.method == 'POST':
        try:
            data = {
                'power': float(request.form.get('power', 0)),
                'rate': float(request.form.get('rate', 0)),
                'heat_loss': float(request.form.get('heat_loss', 0))
            }
            result = RefluxCalc1.calculate(data)
        except ValueError as e:
            result['error'] = "لطفا مقادیر عددی معتبر وارد کنید"
        except Exception as e:
            result['error'] = str(e)
    
    return render_template('refluxcalc1.html', result=result)

#=======================================Azeotrope Calculator=====================
@app.route('/azeotropecalc')
def azeotropecalc():
    return render_template('azeotropecalc.html')

@app.route('/calculate_azeotrope', methods=['POST'])
def calculate_azeotrope():
    try:
        data = request.json
        result = AzeotropeCalc.calculate(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

#=======================================BloodAlcoholCalculator=====================
@app.route('/bloodalco', methods=['GET', 'POST'])
def bloodalco():
    result = None
    if request.method == 'POST':
        result = calculate_blood_alcohol(request.form)
    return render_template('bloodalco.html', result=result)

@app.route('/calculate_blood_alcohol', methods=['POST'])
def calculate_blood_alcohol_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        result = calculate_blood_alcohol(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#=======================================SpiritrunCalculator=====================
@app.route('/spiritrun', methods=['GET', 'POST'])
def spiritrun():
    form_data = {}
    if request.method == 'POST':
        result = SpiritRunCalc.calculate()
        # حفظ مقادیر فرم
        form_data = {
            'vss': request.form.get('vss', '20'),
            'sss': request.form.get('sss', '21'),
            'se': request.form.get('se', '65'),
            'dg': request.form.get('dg', '8'),
            'dh': request.form.get('dh', '5'),
            'dpg': request.form.get('dpg', '0'),
            'dph': request.form.get('dph', '0'),
            'ts': request.form.get('ts', '20'),
            'tv': request.form.get('tv', '20'),
            'vo': request.form.get('vo', '1.1'),
            'p': request.form.get('p', '760'),
            'ef': request.form.get('ef', '100'),
            'dpg_trigger': request.form.get('dpg_trigger') == 'on',
            'dph_trigger': request.form.get('dph_trigger') == 'on',
            'ts_trigger': request.form.get('ts_trigger') == 'on',
            'tv_trigger': request.form.get('tv_trigger') == 'on',
            'vo_trigger': request.form.get('vo_trigger') == 'on',
            'p_trigger': request.form.get('p_trigger') == 'on',
            'ef_trigger': request.form.get('ef_trigger') == 'on',
            'column_diameter': request.form.get('column_diameter', '48')
        }
        return render_template('spiritrun.html', result=result, form_data=form_data)
    return render_template('spiritrun.html', form_data=form_data)

#=======================================SugerCalc=====================
@app.route('/sugercalc', methods=['GET', 'POST'])
def sugercalc(): 
    if request.method == 'POST':
        result = SugerCalc.calculate()
        return render_template('sugercalc.html', result=result)
    return render_template('sugercalc.html')

#=======================================GrainCalc=====================
@app.route('/graincalc', methods=['GET', 'POST'])
def graincalc():
    if request.method == 'POST':
        result = GrainCalc.calculate()
        return render_template('graincalc.html', result=result)
    return render_template('graincalc.html')

#=======================================FruitCalc=====================
@app.route('/fruitcalc', methods=['GET', 'POST'])
def fruitcalc():
    if request.method == 'POST':
        result = FruitCalc.calculate()
        return render_template('fruitcalc.html', result=result)
    return render_template('fruitcalc.html')

#=======================================FruitCalc=====================
@app.route('/refrectcalc', methods=['GET', 'POST'])
def refrectcalc():
    if request.method == 'POST':
        result = RefrectCalc.calculate()
        return render_template('refrectcalc.html', result=result)
    return render_template('refrectcalc.html')

#=======================================FermentCalc=====================
@app.route('/fermentcalc', methods=['GET', 'POST'])
def fermentcalc():
    if request.method == 'POST':
        result = FermentCalc.calculate()
        return render_template('fermentcalc.html', result=result)
    return render_template('fermentcalc.html')

#=======================================ElementPower=====================
@app.route('/elementpower')
def elementpower():
    return render_template('elementpower.html')

@app.route('/calculate_element_power', methods=['POST'])
def calculate_element_power():
    data = request.json
    result = ElementPower.calculate(data)
    return jsonify(result)

#=======================================RemainingLiquid=====================
@app.route('/remainingliquid', methods=['GET', 'POST'])
def remainingliquid():
    form_data = {}
    if request.method == 'POST':
        result = RemainingLiquidCalc.calculate()
        # حفظ مقادیر فرم
        form_data = {
            'd': request.form.get('d', '36'),
            'h': request.form.get('h', '8'),
            's': request.form.get('s', '10'),
            't': request.form.get('t', '20'),
            't_trigger': request.form.get('t_trigger') == 'on'
        }
        return render_template('remainingLiquid.html', result=result, form_data=form_data)
    return render_template('remainingLiquid.html', form_data=form_data)

#=======================================BoilingPoint=====================
@app.route('/boilingpoint', methods=['GET', 'POST'])
def boilingpoint():
    form_data = {}
    if request.method == 'POST':
        result = BoilingPointCalc.calculate()
        # حفظ مقادیر فرم
        form_data = {
            's': request.form.get('s', '40'),
            'p': request.form.get('p', '300'),
            't': request.form.get('t', '20'),
            't_trigger': request.form.get('t_trigger') == 'on'
        }
        return render_template('boilingPoint.html', result=result, form_data=form_data)
    return render_template('boilingPoint.html', form_data=form_data)

#=======================================ColumnHeat=====================
@app.route('/columnheat', methods=['GET', 'POST'])
def columnheat():
    form_data = {}
    if request.method == 'POST':
        result = ColumnHeatCalc.calculate()
        # حفظ مقادیر فرم
        form_data = {
            'v': request.form.get('v', '70'),
            'tin': request.form.get('tin', '20'),
            'tout': request.form.get('tout', '45'),
            'w': request.form.get('w', '3')
        }
        return render_template('ColumnHeat.html', result=result, form_data=form_data)
    return render_template('ColumnHeat.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)