from flask import Blueprint, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from app.latex_generator import JupyterCVGenerator
from config import Config

main = Blueprint('main', __name__)
generator = JupyterCVGenerator()

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            linkedin = request.form['linkedin']
            
            code_cells = []
            for key in request.form:
                if key.startswith('cell_'):
                    code_cells.append(request.form[key])
            
            latex_content = generator.generate_latex(
                name=name,
                email=email,
                phone=phone,
                linkedin=linkedin,
                code_cells=code_cells
            )
            
            pdf_path = generator.save_and_compile(
                latex_content,
                output_dir=Config.OUTPUT_DIR,
                filename=secure_filename(f"jupyter_cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            )
            
            return send_file(pdf_path, as_attachment=True, download_name=f"jupyter_cv_{name}.pdf")
            
        except Exception as e:
            flash(str(e), 'error')
            
    return render_template('index.html')