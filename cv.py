from flask import render_template, Blueprint

cv_page = Blueprint('cv_page', __name__,
                        template_folder='templates')

@cv_page.route('/cv')
def cv():
    return render_template('cv.html')
