import os

from flask import Flask, render_template, request, jsonify

# from pyimagesearch.colordescriptor import ColorDescriptor
# from pyimagesearch.searcher import Searcher

# create flask instance
app = Flask(__name__, template_folder='views')

# INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')
img_folder = os.path.join('static', 'PhotoSorter_images')

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
    img_id = request.args.get('id')
    img_path = os.path.join(img_folder, img_id)

    return render_template('image.html', img = img_path)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    # /image?id1=0100.png&id2=0101.png
    img_id1 = request.args.get('id1')
    img_path1 = os.path.join(img_folder, img_id1)
    img_id2 = request.args.get('id2')
    img_path2 = os.path.join(img_folder, img_id2)

    return render_template('compare.html', img1 = img_path1, img2 = img_path2)

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


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
