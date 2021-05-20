from flask import Flask, render_template, redirect, request, Blueprint, Response, json

cv_page = Blueprint('cv_page', __name__,
                        template_folder='templates')

@cv_page.route('/cv')
def cv():
    return render_template('cv.html')

def sort_json(in_json):
    # Return None if our input is invalid (e.g. None, Missing keys, etc)
    if not in_json or 'payload' not in in_json or 'sortKeys' not in in_json:
        return None
    for sort_key in in_json['sortKeys']:
        # Make sure that the key is present in the payload
        if sort_key not in in_json['payload']:
            return None
        in_json['payload'][sort_key] = sorted(in_json['payload'][sort_key])
    return in_json

@cv_page.route('/sort', methods=['GET', 'POST'])
def sort():
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        json_data = sort_json(request.get_json(silent=True))
        if json_data:
            return Response(json.dumps(json_data), status=200, mimetype='application/json')
        return Response('Invalid JSON', status=400)
    else:
        return 'Bad Request', 400
