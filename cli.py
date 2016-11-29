import argparse
import sqlite3
conn = sqlite3.connect('ple-tracker.sqlite')
c = conn.cursor()

# Readline input
entry_dict = {
    weight: float(input('Weight in lbs :')),
    arm_size: float(input('Arm size in cm: ')),
    ab_size: float(input('Abdomen size in cm: ')),
    poo_count: int(input('Number of BMs ')),
    vomit: int(input('Vomiting? ')),
    injection: int(input('injection? ')),
    notes: str(input('Include other notes: '))
}

columns = ['weight', 'arm_size', 'abdomen_size', 'bm_count', 'vomit', 'injection', 'notes']
c.execute('''CREATE TABLE IF NOT EXISTS ple_measurements (date TEXT, weight REAL, arm_size REAL, abdomen_size REAL, bm_count INTEGER, vomit INTEGER default 0, injection INTEGER default 0, notes TEXT default NULL)''')
c.commit()
