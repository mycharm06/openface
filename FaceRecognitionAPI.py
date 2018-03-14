import os, sys
from flask import Flask, render_template, request
from werkzeug import secure_filename
import shutil
import MySQLdb
from flask import jsonify
from flask import json

# running state code

app = Flask(__name__)

db = MySQLdb.connect("localhost", "root", "qwerty", "user")


@app.route('/', methods=['GET'])
def get_info():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "SELECT * FROM data"

        try:
            # Execute the SQL command
            cursor.execute(sql)
            myjson = {'Current Users': []}
            for user_id, user_name in cursor:
                jsonList = {}
                jsonList['ID'] = user_id
                jsonList['NAME'] = user_name
                myjson.get('Current Users').append(jsonList)
                # jsonList.append({"id" : data1[i], "name" : data[i]})
            return jsonify(myjson)


        except:
            # Rollback in case there is any error
            db.rollback()


@app.route('/training-dataset', methods=['GET', 'POST'])
def training_image():
    if request.method == 'POST':
        user = request.form['user']
        print user
        cursor = db.cursor()
        sql = "INSERT INTO data (user_name) VALUES ('%s')" % (user)
        sql1 = "SELECT user_id FROM data WHERE user_name = ('%s')" % (user)
        cursor.execute(sql)
        db.commit()
        cursor.execute(sql1)
        results = cursor.fetchall()
        for row in results:
            ids = int(row[0])
            print ids

        path = os.makedirs('/home/ankush/openface/training-images/' + str(ids))
        UPLOAD_FOLDER = '/home/ankush/openface/training-images/' + str(ids)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        for i in range(30):
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                        os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[0] + str(i) + '.jpg'))

        import alignImages
        output = alignImages.alignMain("align")

        import creatingcsv
        creatingcsv.csv()

        import classifier

        output = classifier.train('/home/ankush/openface/generated-embeddings')
        return jsonify(output)


@app.route('/old_user', methods=['POST'])
def old_user():
    if request.method == 'POST':
        id = request.form['id']
        print id

        UPLOAD_FOLDER = '/home/ankush/openface/training-images/' + id
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        for i in range(20):
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                        os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[0] + str(i) + '.jpg'))

        import alignImages
        output = alignImages.alignMain("align")

        import creatingcsv
        creatingcsv.csv()

        import classifier
        output = classifier.train('/home/ankush/openface/generated-embeddings')
        return jsonify(output)


@app.route("/recognize", methods=['POST'])
def upload_file():
    UPLOAD_FOLDER = '/home/ankush/openface/upload-folder'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        import classifier
        output = classifier.infer('/home/ankush/openface/upload-folder/' + filename)
        print output
        return jsonify(output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
