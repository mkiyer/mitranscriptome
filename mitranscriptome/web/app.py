'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.0.1
'''
from flask import Flask, render_template
app = Flask(__name__)

# configuration
DEBUG = True

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=DEBUG)