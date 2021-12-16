import os
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, flash, request, redirect, send_file, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def find_measures_of_central_tendency(image_filename_path):
    image = cv2.imread(image_filename_path)
    mean = np.mean(image)
    standard_deviation = np.std(image)
    median = np.median(image)
    return mean, median, standard_deviation


def remove_file(image_filename_path):
    if os.path.exists(image_filename_path):
        os.remove(image_filename_path)


@app.route('/binarize', methods=['GET', 'POST'])
@cross_origin()
def binarize():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            binarize_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename) + "otsu" + ".png",
                             mimetype='image/png')
            # remove_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def binarize_image(image_path):
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    otsu_threshold, image_result = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU, )
    cv2.imwrite(image_path + "otsu.png", image_result)


def find_snr_cnr(orginalfile, croppedfile):
    OI = cv2.imread(orginalfile)
    CI = cv2.imread(croppedfile)
    meanOI = np.mean(OI)
    SDCI = np.std(CI)
    SNR = meanOI/SDCI
    meanCI = np.mean(CI)
    CNR = (meanOI - meanCI )/SDCI
    return SNR, CNR




@app.route('/calculateSnrCnr', methods=[ 'POST'])
@cross_origin()
def calculateSnrCnr():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'originalfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        originalfile = request.files['originalfile']
        croppedpart = request.files['croppedpart']
        # if user does not select file, browser also
        # submit an empty part without filename
        if originalfile.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if originalfile and allowed_file(originalfile.filename):
            filename = secure_filename(originalfile.filename)
            originalfile.save(os.path.join(app.config['UPLOAD_FOLDER'], "originalfile.png"))
            croppedpart.save(os.path.join(app.config['UPLOAD_FOLDER'], "croppedpart.png"))
            SNR, CNR = find_snr_cnr(
                os.path.join(app.config['UPLOAD_FOLDER'], "originalfile.png"),
                os.path.join(app.config['UPLOAD_FOLDER'], "croppedpart.png"))
            remove_file(os.path.join(app.config['UPLOAD_FOLDER'], "originalfile.png"))
            remove_file(os.path.join(app.config['UPLOAD_FOLDER'], "croppedpart.png"))
            return jsonify(
                SNR=SNR,
                CNR=CNR
            )



@app.route('/calculateMetrics', methods=['GET', 'POST'])
@cross_origin()
def calculate_metrics():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mean, median, standard_deviation = find_measures_of_central_tendency(
                os.path.join(app.config['UPLOAD_FOLDER'], filename))
            remove_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(
                mean=mean,
                median=median,
                standard_deviation=standard_deviation
            )
        return "hello"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def plotIntensity(imagepath, row_count, column_count):
    figure, axis = plt.subplots(1, 2)
    column_count = int(column_count)
    row_count = int(row_count)
    image = cv2.imread(imagepath, 0)
    (column, row) = image.shape
    x = np.arange(0, row)
    y = image[row_count]

    axis[0].set_title("row intensity graph")
    axis[0].set_xlabel("row number")
    axis[0].set_ylabel("intensities")
    axis[0].plot(x, y)
    x = np.arange(0, column)
    y = image[:, column_count]
    axis[ 1].set_title("column intensity graph")
    axis[ 1].set_xlabel("column number")
    axis[1].set_ylabel("intensities")
    axis[1].plot(x, y, color="green")
    # plotting
    plt.savefig(imagepath + "intensity" + ".png")
    plt.close()
    return send_file(imagepath + "intensity" + ".png", mimetype='image/png')


# def plotIntensityForColumn(imagepath, column_count):
#     column_count = int(column_count)
#     image = cv2.imread(imagepath, 0)
#     (column, row) = image.shape
#     x = np.arange(0, column)
#     y = image[:, column_count]
#     plt.title("column intensity graph")
#     plt.xlabel("column number")
#     plt.ylabel("intensities")
#     plt.plot(x, y, color="green")
#     plt.savefig(imagepath + "column" + ".png")
#
#     return send_file(imagepath + "column" + ".png", mimetype='image/png')


@app.route('/plotIntensities', methods=['GET', 'POST'])
@cross_origin()
def plotIntensities():
    if request.method == 'POST':
        row = request.form['row']
        column = request.form['column']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return plotIntensity(os.path.join(app.config['UPLOAD_FOLDER'], filename), row, column)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def generate_histogram_and_save(image_filename_path):
    image = cv2.imread(image_filename_path, 0)
    plt.hist(image.ravel(), 256, (0, 256))
    plt.savefig(image_filename_path + "histogram" + ".png")
    plt.close()
    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # h, s, v = cv2.split(hsv)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # for x, c, z in zip([h, s, v], ['r', 'g', 'b'], [30, 20, 10]):
    #     xs = np.arange(256)
    #     ys = cv2.calcHist([x], [0], None, [256], [0, 256])
    #     cs = [c] * len(xs)
    #     cs[0] = 'c'
    #     ax.bar(xs, ys.ravel(), zs=z, zdir='y', color=cs, alpha=0.8)
    #
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # plt.savefig(image_filename_path + "histogram" + ".png")


@app.route('/generateHistogram', methods=['GET', 'POST'])
@cross_origin()
def generate_histogram():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            generate_histogram_and_save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            remove_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # try:
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename) + "histogram" + ".png",
                             mimetype='image/png')

            # finally:
            #     # remove_file(os.path.join(app.config['UPLOAD_FOLDER'], filename) + "histogram" + ".png")

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# sending files
# return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/png')
