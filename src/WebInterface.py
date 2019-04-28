from ChessBoardParse import ChessBoardParse
from flask import *
from werkzeug.utils import secure_filename
import time
import os
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
chessparser = ChessBoardParse('models/frozen_inference_graph.pb', 'models/go.pbtxt')
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/pro.log',
                filemode='w')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({})
    return jsonify({})


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    now = time.strftime("%Y-%m-%d %H:%M", time.localtime());
    file = request.files.get('file')
    if not file:
        return jsonify({'ret': -1, 'msg': 'file upload failed'})
    if not allowed_file(file.filename):
        return jsonify({'ret': -2, 'msg': 'TYPE ERROR:only png,jpg,jpeg are allowed'})
    filename = secure_filename(now + '_' + file.filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(img_path)
    output_matrix = chessparser.output_matrix(img_path)
    return jsonify({'ret': 0, 'filename': filename, 'output_matrix': json.dumps(output_matrix)})
