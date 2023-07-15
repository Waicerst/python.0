import os

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
import pygal
# import pandas as pd

ALLOWED_EXTENTIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f'{filename.split(".")[0]}_{str(datetime.now().year)}.csv'
            save_location = os.path.join('input', new_filename)
            file.save(save_location)

            lines = open('input/'+new_filename, 'r').readlines()
            year_title = list()
            for i in lines:
                x = i.strip().split(';')
                if (x[4]== 'Cage, Nicolas'):
                    year_title.append(x[0]+','+x[2])

            if (len(year_title) == 0):
                return render_template('upload.html') + '''
                        <h2 style="color: brown">Выберите другой файл в прошлом нет нужных данных</h2> '''

            else:
                chart = pygal.HorizontalBar()
                for y in year_title:
                    data = y.strip().split(',')
                    chart.add(data[1], int(data[0]))

                chart = chart.render_data_uri()
                return render_template('upload.html', chart=chart)

    return render_template('upload.html')
    # return  app
