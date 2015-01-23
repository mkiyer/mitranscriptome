'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.1.0
'''
# global imports
import collections
import os
import cStringIO

# flask imports
from flask import Flask, render_template, request, g, jsonify, send_file, make_response

# code version
VERSION = 'v0.1.0'

# paths to data
EXPR_PLOT_DIR = os.path.join('plots', 'expr_plots')
EXPR_PLOT_PDF_DIR = os.path.join('plots', 'expr_plots_pdf')
SSEA_PLOT_DIR = os.path.join('plots', 'ssea_plots')
TRANSCRIPT_SEQUENCE_FILE = 'seqs.txt'
TRANSCRIPT_METADATA_FILE = 'metadata.manuscript.v4.txt'
LIBRARY_INFO_FILE = 'library_info.txt'
EXPR_FPKM_MATRIX_FILE = 'mitranscriptome.expr.fpkm.tsv'

# metadata fields used by online portal
TRANSCRIPT_METADATA_FIELDS = ['transcript_id', 'gene_id', 'chrom', 'start', 'end', 'strand', 
                              'tstatus', 'tgenic', 'tcat', 'uce', 
                              'func_name_final', 'association_type', 'tissue', 'ssea_percentile',
                              'transcript_length', 'num_exons', 'conf_score', 
                              'coding_potential', 'pfam', 'orf_size',
                              'tissue_expr_mean', 'tissue_expr_95', 'tissue_expr_99']

# default configuration
class Config(object):
    # number of processes to use
    processes = 4
    # logging mode
    #DEBUG = False
    DEBUG = True
    # location of server data
    DATA_DIR = '/var/www/html/documents'
    #DATA_DIR = '/mctp/projects/mitranscriptome/web/documents'
    #DATA_DIR = '/Users/mkiyer/Documents/mitranscriptome/web_data'

# create flask application
app = Flask(__name__)
app.config.from_object(Config)

def init_transcript_metadata():
    # function to load sequences
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

def init_transcript_sequences():
    # function to load the sequences
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

def init_expr_fpkm():
    # function to load expression data
    path = os.path.join(app.config['DATA_DIR'], EXPR_FPKM_MATRIX_FILE)
    # read matrix data
    d = {}
    with open(path) as f:
        header_fields = f.next().strip().split('\t')
        for line in f:
            fields = line.strip().split('\t')
            d[fields[0]] = map(float, fields[1:])
    app.logger.debug('Loaded FPKM matrix')
    return header_fields[1:], d

@app.route('/get_ssea_plot')
def get_ssea_plot():
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

@app.route('/get_expression_boxplot_pdf')
def get_expression_boxplot_pdf():
    transcript_id = request.args.get('t_id')
    filename = os.path.join(app.config['DATA_DIR'], EXPR_PLOT_PDF_DIR, '%s_expr.pdf' % (transcript_id))
    return send_file(filename, as_attachment=True)

@app.route('/download_seq')
def request_sequence():
    # fetch sequence from metadata
    t_id = request.args.get('t_id')
    func_name, seq = app.config['sequence_dict'][t_id]
    # construct response
    response = make_response(seq)
    # set response header to trigger file download
    response.headers["Content-Disposition"] = "attachment; filename=%s.sequence.txt" % func_name
    return response

@app.route('/get_expr_fpkm')
def get_expr_fpkm():
    app.logger.debug('get_expr_fpkm')
    transcript_id = request.args.get('t_id')
    colnames = app.config['expr_fpkm_libs']
    rowvals = app.config['expr_fpkm_dict'][transcript_id]
    # output as string
    output = cStringIO.StringIO()
    print >>output, '\t'.join(['transcript_id', 'FPKM'])
    for i in xrange(len(colnames)):
        print >>output, '%s\t%f' % (colnames[i], rowvals[i])
    output.seek(0)
    return send_file(output,
                     attachment_filename='expr_fpkm_%s.tsv' % (transcript_id),
                     as_attachment=True)

@app.route('/transcript_metadata', methods=['GET'])
def request_metadata():
    return jsonify(data=app.config['transcript_metadata'])

@app.route('/')
def home():
    return render_template('home.html')

# initialize application
app.logger.debug('Loading metadata')
app.config['transcript_metadata'] = init_transcript_metadata()
app.logger.debug('Loading sequences')
app.config['sequence_dict'] = init_transcript_sequences()
app.logger.debug('Loading expression data')
app.config['expr_fpkm_libs'], app.config['expr_fpkm_dict'] = init_expr_fpkm()

if __name__ == '__main__':
    app.run()
