'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.1.0
'''
# global imports
import collections
import os
import hashlib
from operator import itemgetter

# flask imports
from flask import Flask, render_template, request, g, jsonify, send_file, make_response, Response
from functools import wraps

# project imports
from dbapi import DBInterfaceFile

# create flask application
app = Flask(__name__)

# run on server or run local (set only one)
SERVER = False
YNIKNAFS = False
MKIYER = True
# enable/disable debugging
DEBUG = not SERVER

# for authentication
SECURE_USERNAME = '4e1b98cdd7dc28789293e67d1779acee77277b517ff3525a5e2fdf6079b65d8480d0aa02c60d772d6049e9f3583ccfae85367599c23435a414394d829be9289c'
SECURE_PASSWORD = '491118ba32bec59bdcf53f4e4b6671c5881a2f265740337f54ea2fca3a74e53698304ca24e87765585f968f89520c0522c630b91658449812dcc40f8f6862133'

# location of static files on server
if SERVER: 
    MAIN_DIR = '/var/www/html/mitranscriptome/mitranscriptome/web/static/data'
elif YNIKNAFS: 
#     MAIN_DIR = '/Users/yniknafs/git/mitranscriptome/mitranscriptome/web/static/data'
    MAIN_DIR = '/mctp/users/yniknafs/scripts/workspace_laptop/mitranscriptome/mitranscriptome/web/static/data'
elif MKIYER: 
    MAIN_DIR = '/Users/mkiyer/git/mitranscriptome/mitranscriptome/web/static/data'

# subdirectories
EXPRESSION_PLOT_DIR = os.path.join(MAIN_DIR, 'plots', 'expr_plots')
SSEA_PLOT_DIR = os.path.join(MAIN_DIR, 'plots', 'ssea_plots')
# path to data
TRANSCRIPT_METADATA_FILE = os.path.join(MAIN_DIR, 'metadata.manuscript.v4.txt')
TRANSCRIPT_SEQUENCE_FILE = os.path.join(MAIN_DIR, 'seqs.txt')
# metadata fields used by online portal
TRANSCRIPT_TABLE_FIELDS = ['transcript_id', 'gene_id', 'chrom', 'start', 'end', 'strand', 
                           'tstatus', 'tgenic', 'tcat', 'uce', 
                           'func_name_final', 'association_type', 'tissue', 'ssea_percentile',
                           'transcript_length', 'num_exons', 'conf_score', 
                           'coding_potential', 'pfam', 'orf_size',
                           'tissue_expr_mean', 'tissue_expr_95', 'tissue_expr_99']

def init_transcript_metadata():
    # read transcript metadata
    rows = []
    with open(TRANSCRIPT_METADATA_FILE) as f:
        header_fields = f.next().strip().split('\t')
        header_indexes = [header_fields.index(x) for x in TRANSCRIPT_TABLE_FIELDS]
        for line in f:
            fields = line.strip().split('\t')
            d = dict((header_fields[x], fields[x]) for x in header_indexes)
            rows.append(d)
    return rows

def get_transcript_metadata():
    if not hasattr(g, 'transcript_metadata'):
        g.transcript_metadata = init_transcript_metadata()
    return g.transcript_metadata

def init_transcript_sequences():
    # read transcript sequences
    d = {}
    with open(TRANSCRIPT_SEQUENCE_FILE) as f:
        header_fields = f.next().strip().split('\t')
        for line in f:
            fields = line.strip().split('\t')
            d[fields[0]] = fields[1:]
        app.logger.debug('Loaded transcript metadata')
    return d

def get_sequence_dict():
    if not (hasattr(g, 'transcript_sequence_dict')):
        g.transcript_sequence_dict = init_transcript_sequences()
        app.logger.debug('Loaded transcript sequences')
    return g.transcript_sequence_dict

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    username = hashlib.sha512(username).hexdigest()
    password = hashlib.sha512(password).hexdigest()
    return username == SECURE_USERNAME and password == SECURE_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your login/password', 401, 
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/get_ssea')
@requires_auth
def get_ssea():
    app.logger.debug('get ssea')
    transcript_id = request.args.get('t_id')
    tissue = request.args.get('tissue')
    association_type = request.args.get('association_type')
    plot_type = request.args.get('plot_type')
    filename = '%s.%s.%s.%s.png' % (tissue, association_type, transcript_id, plot_type)
    filename = os.path.join(SSEA_PLOT_DIR, filename)
    app.logger.debug('get ssea ' + filename)
    return send_file(filename, mimetype='image/png')

@app.route('/get_expression_boxplot')
@requires_auth
def get_expression_boxplot():
    transcript_id = request.args.get('t_id')
    filename = os.path.join(EXPRESSION_PLOT_DIR, '%s_expr.jpeg' % (transcript_id))
    return send_file(filename, mimetype='image/jpeg')

@app.route('/download_seq')
@requires_auth
def request_sequence():
    # fetch sequence from metadata
    t_id = request.args.get('t_id')
    func_name, seq = get_sequence_dict()[t_id]
    # construct response
    response = make_response(seq)
    # set response header to trigger file download
    response.headers["Content-Disposition"] = "attachment; filename=%s.sequence.txt" % func_name
    return response

@app.route('/transcript_metadata', methods=['GET'])
@requires_auth
def request_metadata():
    app.logger.debug('Metadata requested')
    m = get_transcript_metadata()
    return jsonify(data=m)

@app.route('/')
@requires_auth
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
