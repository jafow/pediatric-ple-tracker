import sqlite3
import json

conn = sqlite3.connect('ple-tracker.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

## get all the records
c.execute("SELECT * from ple_measurements ORDER BY date DESC")
res = c.fetchall()


def format_dict(d):
    return {
    'date': d['date'],
    'measurements': {
        'weight': d['weight'],
        'abdomen_size': d['abdomen_size'],
        'arm_size': d['arm_size']
    },
    'output': {
        'bm_count': d['bm_count'],
        'vomit': bool(d['vomit'])
    },
    'symptoms': {
        'swelling': bool(d['swelling']),
        'irritabiliity': bool(d['irritable'])
    },
    'notes': d['notes']
    }

# format and print
j = [ format_dict(dict(o)) for o in res ]
print(json.dumps(j))

