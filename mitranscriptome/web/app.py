'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.0.1
'''
import collections
import os
from operator import itemgetter
from flask import Flask, render_template, request, g, jsonify, send_file

# project imports
from dbapi import DBInterfaceFile

# create flask application
app = Flask(__name__)

# configuration
DEBUG = True
MAIN_DIR = '/mctp/projects/mitranscriptome/naming/toy'
TRANSCRIPT_METADATA_FILE = os.path.join(MAIN_DIR, 'metadata.mitranscriptome.txt')
TRANSCRIPT_METADATA_FIELDS = ['transcript_id', 'gene_id', 'chrom', 'start', 
                              'end', 'strand', 'tstatus', 'tgenic', 
                              'func_name', 'func_type', 'func_cat', 
                              'func_dir', 'uce', 'cons', 'avg_frac']
EXPRESSION_PLOT_DIR = os.path.join(MAIN_DIR, 'expr_plots')
SSEA_PLOT_DIR = os.path.join(MAIN_DIR, 'ssea_plots')
def ssea_selector(type, cat):
    if type == 'aml':
        ssea_type = 'cancer_type_aml'
        ssea_can = 'NA'
    if type == 'bladder':
        if cat == 'clat':
            ssea_type = 'cancer_type_bladder'
            ssea_can = 'cancer_versus_normal_bladder'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_bladder'
    if type == 'breast':
        if cat == 'clat':
            ssea_type = 'cancer_type_breast_carcinoma'
            ssea_can = 'cancer_versus_normal_breast'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_breast'
    if type == 'cervical':
        ssea_type = 'cancer_type_cervical_carcinoma'
        ssea_can = 'NA'
    if type == 'cml':
        ssea_type = 'cancer_type_cml'
        ssea_can = 'NA'
    if type == 'colorectal':
        ssea_type = 'cancer_type_colorectal_carcinoma'
        ssea_can = 'NA'
    if type == 'gbm':
        ssea_type = 'cancer_type_glioblastoma_multiforme_gbm'
        ssea_can = 'NA'
    if type == 'head_neck':
        if cat == 'clat':
            ssea_type = 'cancer_type_head_and_neck_carcinoma'
            ssea_can = 'cancer_versus_normal_head_and_neck'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_head_and_neck'
    if type == 'heart':
        ssea_type = 'normal_type_heart'
        ssea_can = 'NA'
    if type == 'hesc':
        ssea_type = 'normal_type_embryonic_stem_cells'
        ssea_can = 'NA'
    if type == 'hiclinc':
        ssea_type = 'NA'
        ssea_can = 'NA'
    if type == 'kich':
        if cat == 'clat':
            ssea_type = 'cancer_type_renal_cell_carcinoma_chromophobe'
            ssea_can = 'cancer_versus_normal_kidney_chromophobe'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_kidney_chromophobe'
    if type == 'kirc':
        if cat == 'clat':
            ssea_type = 'cancer_type_renal_clear_cell_carcinoma'
            ssea_can = 'cancer_versus_normal_kidney_clear_cell'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_kidney_clear_cell'
    if type == 'kirp':
        if cat == 'clat':
            ssea_type = 'cancer_type_renal_papillary_cell_carcinoma'
            ssea_can = 'cancer_versus_normal_kidney_papillary_cell'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_kidney_papillary_cell'
    if type == 'lgg':
        ssea_type = 'cancer_type_lower_grade_glioma_lgg'
        ssea_can = 'NA'
    if type == 'liver':
        if cat == 'clat':
            ssea_type = 'cancer_type_hepatocellular_carcinoma'
            ssea_can = 'cancer_versus_normal_liver'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_liver'
    if type == 'luad':
        if cat == 'clat':
            ssea_type = 'cancer_type_lung_adenocarcinoma'
            ssea_can = 'cancer_versus_normal_lung_adenocarcinoma'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_lung_adenocarcinoma'
    if type == 'lusc':
        if cat == 'clat':
            ssea_type = 'cancer_type_lung_squamous_cell_carcinoma'
            ssea_can = 'cancer_versus_normal_lung_squamous'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_lung_squamous'
    if type == 'medulloblastoma':
        ssea_type = 'cancer_type_medulloblastoma'
        ssea_can = 'NA'
    if type == 'melanoma':
        ssea_type = 'cancer_type_melanoma'
        ssea_can = 'NA'
    if type == 'mpn':
        ssea_type = 'cancer_type_mpn'
        ssea_can = 'NA'
    if type == 'ovarian':
        ssea_type = 'cancer_type_ovarian'
        ssea_can = 'NA'
    if type == 'pancreatic':
        ssea_type = 'cancer_type_pancreatic_carcinoma'
        ssea_can = 'NA'
    if type == 'prostate':
        if cat == 'clat':
            ssea_type = 'cancer_type_prostate_carcinoma'
            ssea_can = 'cancer_versus_normal_prostate'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_prostate'
    if type == 'skeletal_muscle':
        ssea_type = 'normal_type_skeletal_muscle'
        ssea_can = 'NA'
    if type == 'stomach':
        if cat == 'clat':
            ssea_type = 'cancer_type_stomach_adenocarcinoma'
            ssea_can = 'cancer_versus_normal_stomach'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_stomach'
    if type == 'thyroid':
        if cat == 'clat':
            ssea_type = 'cancer_type_thyroid'
            ssea_can = 'cancer_versus_normal_thyroid'
        else: 
            ssea_type = 'NA'
            ssea_can = 'cancer_versus_normal_thyroid'
    if type == 'uterine':
        ssea_type = 'cancer_type_uterine_endometrial_carcinoma'
        ssea_can = 'NA'
    return ssea_type, ssea_can
    
def init_transcript_db():
    return DBInterfaceFile.open(TRANSCRIPT_METADATA_FILE)

def get_transcript_db():
    if not hasattr(g, 'transcript_db'):
        g.transcript_db = init_transcript_db()
    return g.transcript_db

def init_transcript_tables(tdb):
    results = tdb.get_transcript_metadata(transcript_ids=None, 
                                          fields=TRANSCRIPT_METADATA_FIELDS)
    ttables = collections.defaultdict(lambda: [])
    for r in results:
        k = r['func_type']
        # TODO: construct bigbed link
        r['ucsc_link'] = ('http://genome.ucsc.edu/cgi-bin/hgTracks?hgS_doOtherUser=submit&'
                            'hgS_otherUserName=mitranscriptome&'
                            'hgS_otherUserSessionName=mitranscriptome&position=%s' % 
                            (r['chrom'] + '%3A' + r['start'] + '-' + r['end']))
        r['expr_plot'] = 'http://127.0.0.1:5000/get_expression_boxplot?transcript_id=%s' % (r['transcript_id'])
        ssea_type, ssea_can = ssea_selector(k, r['func_cat'])
        r['ssea_type'] = 'http://127.0.0.1:5000/get_ssea?transcript_id=%s&subdir=%s&plot_type=eplot' % (r['transcript_id'], ssea_type)
        r['ssea_type_expr'] = 'http://127.0.0.1:5000/get_ssea?transcript_id=%s&subdir=%s&plot_type=fpkm' % (r['transcript_id'], ssea_type)        
        r['ssea_can'] = 'http://127.0.0.1:5000/get_ssea?transcript_id=%s&subdir=%s&plot_type=eplot' % (r['transcript_id'], ssea_can)
        r['ssea_can_expr'] = 'http://127.0.0.1:5000/get_ssea?transcript_id=%s&subdir=%s&plot_type=fpkm' % (r['transcript_id'], ssea_can)
        if r['avg_frac'] != 'NA':
            r['avg_frac'] = format(float(r['avg_frac']), '.4f')
        ttables[k].append(r)
    for k in ttables.iterkeys():
        ttables[k] = sorted(ttables[k], key=itemgetter('avg_frac'), reverse=True)
    
    return ttables

def get_transcript_tables(tdb):
    if not hasattr(g, 'transcript_tables'):
        g.transcript_tables = init_transcript_tables(tdb)
    return g.transcript_tables

@app.route('/get_expression_boxplot')
def get_expression_boxplot():
    transcript_id = request.args.get('transcript_id')
    filename = os.path.join(EXPRESSION_PLOT_DIR, '%s_expr.jpeg' % (transcript_id))
    app.logger.debug('Get expression boxplot: %s' % (filename))
    # TODO: debugging (make sure file exists)
    return send_file(filename, mimetype='image/jpeg')

@app.route('/get_ssea')
def get_ssea():
    transcript_id = request.args.get('transcript_id')
    subdir = request.args.get('subdir')
    plot_type = request.args.get('plot_type')
    
    filename = os.path.join(SSEA_PLOT_DIR, subdir, '%s.%s.png' % (transcript_id, plot_type))
    app.logger.debug('Get expression boxplot: %s' % (filename))
    # TODO: debugging (make sure file exists)
    return send_file(filename, mimetype='image/jpeg')

@app.route('/transcripts', methods=['POST'])
def request_transcripts():
    '''
    json request object with fields:
        'functype': functional type of transcript (CAT, LAT, CLAT, etc)
        'lineage': lineage / tissue type

    returns json 'results' with list of objects each with attributes:
        'transcript_id': transcript_id
        custom fields specified in configuration
    '''
    # get transcript metadata
    ttables = get_transcript_tables(get_transcript_db())
    # parse the incoming json request
    d = request.get_json()
    k = d['func_type']
    if k not in ttables:
        app.logger.error('Transcript table (%s) not found' % (k))
        # TODO: handle error?
        return jsonify(results=None)
    app.logger.debug('Transcript table %s' % (k))
    return jsonify(results=ttables[k])

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=DEBUG)