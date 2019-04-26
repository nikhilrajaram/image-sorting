import os

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import csv


import ntpath
ntpath.basename("a/b/c")
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)




import sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from histograms.ImageHistogram import ImageHistogram
from histograms.KNearestImages import KNearestImages


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
class_list = []
with open("../yolo/yolov3.txt", 'rb') as f:
    class_list = f.read().splitlines()
class_list = [line.decode("utf-8")  for line in class_list]

# create flask instance
app = Flask(__name__, template_folder='views')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')
img_folder = os.path.join('static', 'PhotoSorter_images')
up_folder = os.path.join('static', 'uploads')

# main route
@app.route('/')
def index():
    imgs = os.listdir('static/PhotoSorter_images')
    imgs = [os.path.join(img_folder, file) for file in imgs]
    # imgs = imgs[0:2]
    return render_template('index.html', imgs = imgs)


@app.route('/image', methods=['GET', 'POST'])
def image():
    # /image?id=0100.png
    img_id = request.args.get('id', default = "", type = str)
    img_id = path_leaf(img_id)
    img_path = os.path.join(img_folder, img_id)

    clusters = request.args.get('clusters', default = 5, type = int)
    print(img_path)
    IH = ImageHistogram(img_path, (450, 450))
    knn = KNearestImages(int(clusters))

    knn.fit()
    dists, imgs = knn.kneighbors(IH)

    info = {"dists":dists}

    imgs = [os.path.join(img_folder, im) for im in imgs]

    return render_template('image.html', img = img_path, info=info, fromUpload=False, f=path_leaf(img_id), imgs=imgs)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    # /compare?id1=0100.png&id2=0101.png
    # if request.method == 'POST':
    #     im1 = request.form['im1']
    #     im2 = request.form['im2']
    #     redirect("/compare?id1=" + im1 + "&id2=" + im2)
    img_id1 = request.args.get('id1', default = "", type = str)
    img_path1 = os.path.join(img_folder, img_id1)
    img_id2 = request.args.get('id2', default = "", type = str)
    img_path2 = os.path.join(img_folder, img_id2)

    return render_template('compare.html', img1 = img_path1, img2 = img_path2)

@app.route('/classes', methods=['GET', 'POST'])
def classes():
    # /classes
    imgs = []
    if request.method == 'POST':
        selected_users = request.form.getlist("users")
        print(selected_users)
        with open('../yolo/yolo_classes.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for u in selected_users:
                    if u in row[1:]:
                        imgs.append(os.path.join(img_folder, row[0]))

    return render_template('classes.html', data=class_list, imgs=imgs)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/upload/" + filename)

    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''

@app.route('/upload/<filename>', methods = ['GET', 'POST'])
def uploaded_file(filename, clusters=5):
    clusters = request.args.get('clusters', default = 5, type = int)
    # if request.method == 'POST':
    # print(UPLOAD_FOLDER + "/" + filename)
    # print(clusters)

    IH = ImageHistogram(UPLOAD_FOLDER + "/" + filename, (450, 450))
    knn = KNearestImages(int(clusters))

    knn.fit()
    dists, imgs = knn.kneighbors(IH)

    info = {"dists":dists}

    print(os.path.join(UPLOAD_FOLDER, filename))

    imgs = [os.path.join(img_folder, im) for im in imgs]


    return render_template('upload.html', img=os.path.join(UPLOAD_FOLDER, filename), info=info, f=filename, fromUpload=True, imgs=imgs)

    # for img in imgs:
    #     print('open {} {}'.format(IH.filename.replace('../img/', ''), img))
    # return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                            filename)


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)


# @app.route('/search', methods=['POST'])
# def search():
#
#     if request.method == "POST":
#
#         RESULTS_ARRAY = []
#
#         # get url
#         image_url = request.form.get('img')
#
#         try:
#
#             # initialize the image descriptor
#             cd = ColorDescriptor((8, 12, 3))
#
#             # load the query image and describe it
#             from skimage import io
#             query = io.imread(image_url)
#             features = cd.describe(query)
#
#             # perform the search
#             searcher = Searcher(INDEX)
#             results = searcher.search(features)
#
#             # loop over the results, displaying the score and image name
#             for (score, resultID) in results:
#                 RESULTS_ARRAY.append(
#                     {"image": str(resultID), "score": str(score)})
#
#             # return success
#             return jsonify(results=(RESULTS_ARRAY[::-1][:3]))
#
#         except:
#
#             # return error
#             jsonify({"sorry": "Sorry, no results! Please try again."}), 500
