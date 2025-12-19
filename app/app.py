import os
import sys
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'template')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')

try:
    from business_logic import calculate_priority
except ImportError as e:
    print(f"ERROR: Failed to import the business_logic module: {e}")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


# --- Web Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = None
    form_data = {
        'type_a': 'car', 'road_a': 'paved', 'sign_a': 'none',
        'type_b': 'car', 'road_b': 'paved', 'sign_b': 'none', 'dir_b': 'left'
    }

    if request.method == 'POST':
        data_a = {
            'type': request.form.get('type_a'),
            'road': request.form.get('road_a'),
            'sign': request.form.get('sign_a')
        }
        data_b = {
            'type': request.form.get('type_b'),
            'road': request.form.get('road_b'),
            'sign': request.form.get('sign_b'),
            'direction': request.form.get('dir_b')
        }
        
        form_data = {
            'type_a': data_a['type'], 'road_a': data_a['road'], 'sign_a': data_a['sign'],
            'type_b': data_b['type'], 'road_b': data_b['road'], 'sign_b': data_b['sign'], 'dir_b': data_b['direction']
        }

        result_text = calculate_priority(data_a, data_b)

    return render_template('index.html', result=result_text, form=form_data)

# --- 404 Error Handler ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- Application Startpoint ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)