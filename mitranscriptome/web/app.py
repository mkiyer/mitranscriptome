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
    MAIN_DIR = '/Users/yniknafs/git/mitranscriptome/mitranscriptome/web/static/data'
elif MKIYER: 
    MAIN_DIR = '/Users/mkiyer/git/mitranscriptome/mitranscriptome/web/static/data'

# subdirectories
EXPRESSION_PLOT_DIR = os.path.join(MAIN_DIR, 'plots', 'expr_plots')
SSEA_PLOT_DIR = os.path.join(MAIN_DIR, 'plots', 'ssea_plots')
# path to data
TRANSCRIPT_METADATA_FILE = os.path.join(MAIN_DIR, 'metadata.manuscript.v3.txt')
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

def ssea_selector(type, cat):
    if type == 'aml':
        ssea_type = 'cancer_type_aml'
        ssea_can = 'NA'
        type_name = 'Acute Myelogenous Leukemia Associated Transcripts'
    if type == 'bladder':
        if cat == 'clat':
            ssea_type = 'cancer_type_bladder'
            ssea_can = 'cancer_versus_normal_bladder'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_bladder'
        type_name = 'Bladder Cancer Associated Transcripts'
    if type == 'breast':
        if cat == 'clat':
            ssea_type = 'cancer_type_breast_carcinoma'
            ssea_can = 'cancer_versus_normal_breast'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_breast'
        type_name = 'Breast Cancer Associated Transcripts'
    if type == 'cervical':
        ssea_type = 'cancer_type_cervical_carcinoma'
        ssea_can = 'NA'
        type_name = 'Cervical Cancer Associated Transcripts'
    if type == 'cml':
        ssea_type = 'cancer_type_cml'
        ssea_can = 'NA'
        type_name = 'Chronic Myelogenous Leukemia Associated Transcripts'
    if type == 'colorectal':
        ssea_type = 'cancer_type_colorectal_carcinoma'
        ssea_can = 'NA'
        type_name = 'Colorectal Cancer Associated Transcripts'
    if type == 'gbm':
        ssea_type = 'cancer_type_glioblastoma_multiforme_gbm'
        ssea_can = 'NA'
        type_name = 'Glioblastoma Multiforme Associated Transcripts'
    if type == 'head_neck':
        if cat == 'clat':
            ssea_type = 'cancer_type_head_and_neck_carcinoma'
            ssea_can = 'cancer_versus_normal_head_and_neck'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_head_and_neck'
        type_name = 'Head and Neck Cancer Associated Transcripts'
    if type == 'heart':
        ssea_type = 'normal_type_heart'
        ssea_can = 'NA'
        type_name = 'Heart Tissue Associated Transcripts'
    if type == 'hesc':
        ssea_type = 'normal_type_embryonic_stem_cells'
        ssea_can = 'NA'
        type_name = 'Human Embryonic Stem Cells Associated Transcripts'
    if type == 'hiclinc':
        ssea_type = 'NA'
        ssea_can = 'NA'
        type_name = 'Highly Conserved lncRNAs (not otherwise tissue/cancer associated)'
    if type == 'kich':
        if cat == 'clat':
            ssea_type = 'cancer_type_renal_cell_carcinoma_chromophobe'
            ssea_can = 'cancer_versus_normal_kidney_chromophobe'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_kidney_chromophobe'
        type_name = 'Chromophobe Renal Cell Carcinoma Associated Transcripts'
    if type == 'kirc':
        if cat == 'clat':
            ssea_type = 'cancer_type_renal_clear_cell_carcinoma'
            ssea_can = 'cancer_versus_normal_kidney_clear_cell'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_kidney_clear_cell'
        type_name = 'Renal Clear Cell Carcinoma Associated Transcripts'
    if type == 'kirp':
        if cat == 'clat':
            ssea_type = 'cancer_type_renal_papillary_cell_carcinoma'
            ssea_can = 'cancer_versus_normal_kidney_papillary_cell'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_kidney_papillary_cell'
        type_name = 'Renal Papillary Cell Carcinoma Associated Transcripts'
    if type == 'lgg':
        ssea_type = 'cancer_type_lower_grade_glioma_lgg'
        ssea_can = 'NA'
        type_name = 'Low Grade Glioma Associated Transcripts'
    if type == 'liver':
        if cat == 'clat':
            ssea_type = 'cancer_type_hepatocellular_carcinoma'
            ssea_can = 'cancer_versus_normal_liver'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_liver'
        type_name = 'Liver Cancer Associated Transcripts'
    if type == 'luad':
        if cat == 'clat':
            ssea_type = 'cancer_type_lung_adenocarcinoma'
            ssea_can = 'cancer_versus_normal_lung_adenocarcinoma'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_lung_adenocarcinoma'
        type_name = 'Lung Adenocarcinoma Associated Transcripts'
    if type == 'lusc':
        if cat == 'clat':
            ssea_type = 'cancer_type_lung_squamous_cell_carcinoma'
            ssea_can = 'cancer_versus_normal_lung_squamous'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_lung_squamous'
        type_name = 'Lung Squamous Cell Carcinoma Associated Transcripts'
    if type == 'medulloblastoma':
        ssea_type = 'cancer_type_medulloblastoma'
        ssea_can = 'NA'
        type_name = 'Medulloblastoma Associated Transcripts'
    if type == 'melanoma':
        ssea_type = 'cancer_type_melanoma'
        ssea_can = 'NA'
        type_name = 'Melanoma Associated Transcripts'
    if type == 'mpn':
        ssea_type = 'cancer_type_mpn'
        ssea_can = 'NA'
        type_name = 'Myeloproliferative Neoplasia Associated Transcripts'
    if type == 'ovarian':
        ssea_type = 'cancer_type_ovarian'
        ssea_can = 'NA'
        type_name = 'Ovarian Cancer Associated Transcripts'
    if type == 'pancreatic':
        ssea_type = 'cancer_type_pancreatic_carcinoma'
        ssea_can = 'NA'
        type_name = 'Pancreatic Cancer Associated Transcripts'
    if type == 'prostate':
        if cat == 'clat':
            ssea_type = 'cancer_type_prostate_carcinoma'
            ssea_can = 'cancer_versus_normal_prostate'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_prostate'
        type_name = 'Prostate Cancer Associated Transcripts'
    if type == 'skeletal_muscle':
        ssea_type = 'normal_type_skeletal_muscle'
        ssea_can = 'NA'
        type_name = 'Skeletal Muscle Tissue Associated Transcripts'
    if type == 'stomach':
        if cat == 'clat':
            ssea_type = 'cancer_type_stomach_adenocarcinoma'
            ssea_can = 'cancer_versus_normal_stomach'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_stomach'
        type_name = 'Stomach Cancer Associated Transcripts'
    if type == 'thyroid':
        if cat == 'clat':
            ssea_type = 'cancer_type_thyroid'
            ssea_can = 'cancer_versus_normal_thyroid'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_thyroid'
        type_name = 'Thyroid Cancer Associated Transcripts'
    if type == 'uterine':
        ssea_type = 'cancer_type_uterine_endometrial_carcinoma'
        ssea_can = 'NA'
        type_name = 'Uterine Endometrial Carcinoma Associated Transcripts'
    
    return ssea_type, ssea_can, type_name

@app.route('/modal')
@requires_auth
def request_transcript_view():
    t_id = request.args.get('t_id')
    meta = get_transcript_db().metadata_json_dict[t_id]
    ssea_type, ssea_can, type_name = ssea_selector(meta['func_type'], meta['func_cat'])
    meta['loc'] = meta['chrom'] + ':' + meta['start'] + '-' + meta['end'] + '[' + meta['strand'] + ']'   
    meta['can_show'] = ''
    meta['type_show'] = ''
    if meta['tcat'] == 'lncrna':
        meta['tcat'] = 'lncRNA'
    if meta['tcat'] == 'tucp':
        meta['tcat'] = 'TUCP'
    if meta['func_cat'] == 'clat':
        meta['func_cat'] = 'Cancer and Lineage Association'
    if meta['func_cat'] == 'at':
        meta['func_cat'] = 'Lineage Association'
        meta['can_show'] = 'hide'
    if meta['func_cat'] == 'cat':
        meta['func_cat'] = 'Cancer Association'
        meta['type_show'] = 'hide'
    if meta['func_cat'] == 'hiclinc':
        meta['type_show'] = 'hide'
        meta['can_show'] = 'hide'
    if meta['avg_frac'] != 'NA':
        meta['avg_frac'] = float(format(float(meta['avg_frac']), '.4f'))
    # construct links to images
    meta['ssea_type_img'] = '/get_ssea?transcript_id=%s&subdir=%s&plot_type=eplot' % (t_id, ssea_type)
    meta['ssea_type_expr_img'] = '/get_ssea?transcript_id=%s&subdir=%s&plot_type=fpkm' % (t_id, ssea_type)        
    meta['ssea_can_img'] = '/get_ssea?transcript_id=%s&subdir=%s&plot_type=eplot' % (t_id, ssea_can)
    meta['ssea_can_expr_img'] = '/get_ssea?transcript_id=%s&subdir=%s&plot_type=fpkm' % (t_id, ssea_can)
    meta['expr_img'] = '/get_expression_boxplot?transcript_id=%s' % (t_id)
    meta['ucsc_link'] = ('http://genome.ucsc.edu/cgi-bin/hgTracks?hgS_doOtherUser=submit&'
                            'hgS_otherUserName=mitranscriptome&'
                            'hgS_otherUserSessionName=mitranscriptome&position=%s' % 
                            (meta['chrom'] + '%3A' + meta['start'] + '-' + meta['end']))
    meta['seq_link'] = '/download_seq?t_id=%s' % t_id
    meta['type_name'] = type_name
    return render_template('transcript_view.html', meta=meta)

@app.route('/get_ssea')
@requires_auth
def get_ssea():
    transcript_id = request.args.get('t_id')
    subdir = request.args.get('subdir')
    plot_type = request.args.get('plot_type')
    filename = os.path.join(SSEA_PLOT_DIR, subdir, '%s.%s.png' % (transcript_id, plot_type))
    return send_file(filename, mimetype='image/jpeg')

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
    app.logger.debug('Metadata')
    m = get_transcript_metadata()
    return jsonify(data=m)

@app.route('/')
@requires_auth
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
