'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.0.1
'''
import collections
from flask import Flask, render_template, request, g, jsonify

# project imports
from dbapi import DBInterfaceFile

# create flask application
app = Flask(__name__)

# configuration
DEBUG = True
TRANSCRIPT_METADATA_FILE = '/mctp/projects/mitranscriptome/annotation/metadata.transcript.candidates.txt'
TRANSCRIPT_METADATA_FIELDS = ['transcript_id', 'gene_id', 'chrom', 'start', 
                              'end', 'strand', 'tstatus', 'tgenic', 
                              'func_name', 'func_type', 'func_cat', 
                              'func_dir']

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
        k = (r['func_cat'], r['func_type'])
        ttables[k].append(r)
    return ttables

def get_transcript_tables(tdb):
    if not hasattr(g, 'transcript_tables'):
        g.transcript_tables = init_transcript_tables(tdb)
    return g.transcript_tables

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
    func_cat = d['func_cat']
    func_type = d['func_type']
    k = (func_cat, func_type)
    if k not in ttables:
        app.logger.error('Transcript table (%s:%s) not found' % (k))
        # TODO: handle error?
        return jsonify(results=None)
    app.logger.debug('Transcript table %s:%s' % (k))
    return jsonify(results=ttables[k])

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=DEBUG)