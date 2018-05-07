from flask import Flask, render_template, redirect, url_for, send_from_directory, request
from flask_bootstrap import Bootstrap
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime
import os
#from flask_table import Table, Col
from random import randint

app = Flask(__name__)
Bootstrap(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

glo = -1

row_array=[20, 10, 20, 20, 25, 25, 25]

no_Of_tests = 6

#skip_values=[[(1, 1), (2, 4)],[(0,3),(0,2)]]

skip_values=[[],[],[],[],[],[],[]]
skip_times =[0, 60, 0, 350, 150, 220, 5]
all_letters = ["G", "G", "|", "|", "m", "M"]

search_letter = ["T", "T", "!", "!", "n", "N", "r", "L"]

#search_position = [(),(),(),(),(),(),()]

time = []

state=0



def gencoordinates(m, n):
    seen = set()

    x, y = randint(m, n), randint(m, n)

    while True:
        seen.add((x, y))
        yield (x, y)
        x, y = randint(m, n), randint(m, n)
        while (x, y) in seen:
            x, y = randint(m, n), randint(m, n)

def genr(m, n):
    seen = set()

    x = randint(m, n)

    while True:
        seen.add((x))
        yield (x)
        x = randint(m, n)
        while x in seen:
            x = randint(m, n)

@app.route('/index')
def index():
    return render_template('index.html')

def get_mat():
    if glo==6:
        g=genr(65, 90)
    else:
        g=genr(91, 122)
    s=row_array[glo]*row_array[glo]
    print(s)
    mat=[[]]
    for i in range(glo):
        arr=[]
        for j in range(glo):
            x = chr(next(g))
            arr.append(x)
        mat.append(arr)
    print (mat)
    return mat

@app.route('/inter', methods=['GET', 'POST'])
def inter():
    #thumbnail_names = os.listdir('./thumbnails')
    global glo
    global state
    global time
    global no_Of_tests
    if request.method == 'GET':
        
        if state==0:
            state =1
            #time.append(datetime.utcnow())
            return render_template('inter.html', time=time,state=0,tests=no_Of_tests)
        print("Hey")
        if glo < no_Of_tests:
            #print "Hey2"
            glo+=1
            if glo==6 or glo==7:
                print("qwe")
                print(glo)
                g=gencoordinates(0, row_array[glo]-1)
                #print(next(g))
                s=skip_times[glo]

                print(s)
                while(s>0):
                    skip_values[glo].append(next(g))
                    s=s-1
                print (skip_values)
                search_ind = next(g)
                print(search_ind)
                print(search_ind[0])
                print("yayy")
                print(mat)
                mat=get_mat()
                time.append(datetime.utcnow())

                return render_template('table1.html', mat=mat, rows=row_array[glo], cols=row_array[glo], search_let=search_letter[glo], search_row=search_ind[0], search_col=search_ind[1], skip_values=skip_values[glo])
            
            print(glo)
            g=gencoordinates(0, row_array[glo]-1)
            #print(next(g))
            s=skip_times[glo]

            print(s)
            while(s>0):
                skip_values[glo].append(next(g))
                s=s-1
            print (skip_values)
            search_ind = next(g)
            print(search_ind)
            print(search_ind[0])
            time.append(datetime.utcnow())
            return render_template('table.html', rows=row_array[glo], cols=row_array[glo], all_let=all_letters[glo], search_let=search_letter[glo], search_row=search_ind[0], search_col=search_ind[1], skip_values=skip_values[glo])
        else:
            glo=0
            state=2
            time[-1]=datetime.utcnow()-time[-1]
            return render_template('inter.html', time=time,state=state,tests=no_Of_tests)

    if glo >= no_Of_tests-1:
        state = 2  
    time[-1]=datetime.utcnow()-time[-1]
    return render_template('inter.html',time=time,state=state,tests=no_Of_tests)

@app.route('/table', methods=['GET', 'POST'])
def table():
    #thumbnail_names = os.listdir('./thumbnails')
    global state
    global glo
    if request.method == 'POST':
        return redirect(url_for('inter',state=1))
    state = 0
    glo =-1
    return redirect(url_for('inter',state=0))


# @app.route('/thumbnails/<filename>')
# def thumbnails(filename):
#     return send_from_directory('thumbnails', filename)

# @app.route('/images/<filename>')
# def images(filename):
#     return send_from_directory('images', filename)

# @app.route('/public/<path:filename>')
# def static_files(filename):
#     return send_from_directory('./public', filename)

# @app.route('/next', methods=['GET', 'POST'])
# def next():
#     if request.method == 'POST':
#         return redirect(url_for('inter'))

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         for upload in request.files.getlist('images'):
#             filename = upload.filename
#             # Always a good idea to secure a filename before storing it
#             filename = secure_filename(filename)
#             # This is to verify files are supported
#             ext = os.path.splitext(filename)[1][1:].strip().lower()
#             if ext in set(['jpg', 'jpeg', 'png']):
#                 print('File supported moving on...')
#             else:
#                 return render_template('error.html', message='Uploaded files are not supported...')
#             destination = '/'.join([images_directory, filename])
#             # Save original image
#             upload.save(destination)
#             # Save a copy of the thumbnail image
#             image = Image.open(destination)
#             image.thumbnail((300, 170))
#             image.save('/'.join([thumbnails_directory, filename]))
#         return redirect(url_for('gallery'))
#     return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000))
