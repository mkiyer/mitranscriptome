'''
MiTranscriptome web server

@author: mkiyer
@author: yniknafs

@version: 0.0.1
'''
import sys
from flask import Flask, render_template, request, g, jsonify

# project imports
from dbapi import DBInterfaceFile

# create flask application
app = Flask(__name__)

# configuration
DEBUG = True
TRANSCRIPT_METADATA_FILE = '/Users/mkiyer/Box Sync/mitranscriptome/data/annotate/metadata.transcript.candidates.txt'

def init_transcript_db():
    return DBInterfaceFile.open(TRANSCRIPT_METADATA_FILE)

def get_transcript_db():
    if not hasattr(g, 'transcript_db'):
        g.transcript_db = init_transcript_db()
    return g.transcript_db

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
    # parse the incoming json request
    d = request.get_json()
    functype = d['functype']
    lineage = d['lineage']
    # get transcript metadata
    tdb = get_transcript_db()
    # TODO: get lists of transcript ids by lineage and functype..
    # should just set up lists of results during initialization
    transcript_ids = None
    fields = ['transcript_id', 'gene_id', 'chrom', 'start', 'end', 'strand', 'tstatus', 'tgenic']
    results = tdb.get_transcript_metadata(transcript_ids, fields)
    app.logger.debug(results)
    return jsonify(results=results)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=DEBUG)