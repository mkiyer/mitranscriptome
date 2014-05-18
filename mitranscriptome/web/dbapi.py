'''
Created on May 9, 2014

@author: mkiyer
'''

class DBInterfaceFile(object):
    def __init__(self):
        self.metadata_json_dict = {}
    
    @staticmethod
    def open(metadata_file):
        '''
        parse tab-delimited file containing metadata     
        first row contains column headers
        remaining columns contain metadata
        '''
        self = DBInterfaceFile()
        # read transcript metadata
        with open(metadata_file) as f:
            header_fields = f.next().strip().split('\t')
            self.metadata_fields = header_fields
            for line in f:
                fields = line.strip().split('\t')
                t_id = fields[0]
                d = dict(zip(header_fields, fields))
                self.metadata_json_dict[t_id] = d
        return self
    
    def get_transcript_metadata(self, transcript_ids=None, fields=None):
        if transcript_ids is None:
            transcript_ids = set(self.metadata_json_dict)
        if fields is None:
            fields = list(self.metadata_fields)
        fields = set(fields)
        results = []
        for t_id in transcript_ids:
            d = self.metadata_json_dict[t_id]
            d = dict((k,v) for k,v in d.iteritems() if k in fields)
            results.append(d)
        return results

if __name__ == '__main__':
    import sys
    db = DBInterfaceFile.open(sys.argv[1])
    print db.get_transcript_metadata(['T000723'], ('transcript_id', 'uce', 'prob.cons'))


    
        
    