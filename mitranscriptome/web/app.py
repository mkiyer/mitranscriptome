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

# code version
VERSION = 'v0.1.0'

# paths to data
EXPR_PLOT_DIR = os.path.join('plots', 'expr_plots')
SSEA_PLOT_DIR = os.path.join('plots', 'ssea_plots')
TRANSCRIPT_SEQUENCE_FILE = 'seqs.txt'
TRANSCRIPT_METADATA_FILE = 'metadata.manuscript.v4.txt'
# metadata fields used by online portal
TRANSCRIPT_METADATA_FIELDS = ['transcript_id', 'gene_id', 'chrom', 'start', 'end', 'strand', 
                              'tstatus', 'tgenic', 'tcat', 'uce', 
                              'func_name_final', 'association_type', 'tissue', 'ssea_percentile',
                              'transcript_length', 'num_exons', 'conf_score', 
                              'coding_potential', 'pfam', 'orf_size',
                              'tissue_expr_mean', 'tissue_expr_95', 'tissue_expr_99']

# create flask application
app = Flask(__name__)

# default configuration
class Config(object):
    # logging mode
    DEBUG = False
    # number of processes to use
    processes = 4
    # location of server data
    DATA_DIR = '/var/www/html/documents'

class DevelopmentConfig(Config):
    DEBUG = True

class MatthewConfig(Config):
    DEBUG = False
    processes = 1
    DATA_DIR = '/Users/mkiyer/Documents/mitranscriptome/web_data'

def get_transcript_metadata():
    # function to load the sequences
    def init_transcript_metadata():
        path = os.path.join(app.config['DATA_DIR'], TRANSCRIPT_METADATA_FILE)
        app.logger.debug(path)
        # read transcript metadata
        rows = []
        with open(path) as f:
            header_fields = f.next().strip().split('\t')
            header_indexes = [header_fields.index(x) for x in TRANSCRIPT_METADATA_FIELDS]
            for line in f:
                fields = line.strip().split('\t')
                d = dict((header_fields[x], fields[x]) for x in header_indexes)
                rows.append(d)
        return rows

    if not hasattr(g, 'transcript_metadata'):
        g.transcript_metadata = init_transcript_metadata()
    return g.transcript_metadata

def get_sequence_dict():    
    # function to load the sequences
    def init_transcript_sequences():
        path = os.path.join(app.config['DATA_DIR'], TRANSCRIPT_SEQUENCE_FILE)
        # read transcript sequences
        d = {}
        with open(path) as f:
            header_fields = f.next().strip().split('\t')
            for line in f:
                fields = line.strip().split('\t')
                d[fields[0]] = fields[1:]
            app.logger.debug('Loaded transcript sequences')
        return d

    if not (hasattr(g, 'transcript_sequence_dict')):
        g.transcript_sequence_dict = init_transcript_sequences()
        app.logger.debug('Loaded transcript sequences')
    return g.transcript_sequence_dict

@app.route('/get_ssea')
def get_ssea():
    app.logger.debug('get ssea')
    transcript_id = request.args.get('t_id')
    tissue = request.args.get('tissue')
    association_type = request.args.get('association_type')
    plot_type = request.args.get('plot_type')
    filename = '%s.%s.%s.%s.png' % (tissue, association_type, transcript_id, plot_type)
    filename = os.path.join(app.config['DATA_DIR'], SSEA_PLOT_DIR, filename)
    app.logger.debug('get ssea ' + filename)
    return send_file(filename, mimetype='image/png')

@app.route('/get_expression_boxplot')
def get_expression_boxplot():
    transcript_id = request.args.get('t_id')
    filename = os.path.join(app.config['DATA_DIR'], EXPR_PLOT_DIR, '%s_expr.jpeg' % (transcript_id))
    return send_file(filename, mimetype='image/jpeg')

@app.route('/download_seq')
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
def request_metadata():
    m = get_transcript_metadata()
    return jsonify(data=m)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    # load config
    import sys
    config = 'app.' + sys.argv[1]
    app.config.from_object(config)
    app.config.fr
    # run
    app.run()
