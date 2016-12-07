import datetime
import sqlite3
conn = sqlite3.connect('ple-tracker.sqlite')
c = conn.cursor()

# Input parsing helpers
def parse_bool_input(prompt_string):
    user_input = str(input(prompt_string)).lower()
    return bool_to_bin(user_input)

def bool_to_bin(input_string):
    if input_string != 'n':
        return 1
    else:
        return 0

def parse_optional_input(prompt_string, prompt_fn):
    user_input = str(input(prompt_string)).lower()
    if user_input == 'n':
        return 0
    else:
        return prompt_fn()

def parse_date_input(input_string):
    current_year = datetime.datetime.now().year
    return current_year + '-' + input_string

def notes_prompt():
    user_input = str(input('Please include any additional notes here: '))
    return user_input

def print_last(cols, vals):
    out = [str(cols[i]) + ': '+ str(vals[i]) for i in range(0, len(cols))]
    print(out)

def parse_input(input_type, prompt_string):
    return input_type(input(prompt_string))

# Prompts for user input
entry_list = [
    parse_date_input(parse_input(str, 'Date of entry (mm-dd): ')),
    parse_input(float, 'Weight in lbs : '),
    parse_input(float,'Arm size in cm: '),
    parse_input(float, 'Abdomen size in cm: '),
    parse_input(int, 'Number of bowel movments: '),
    parse_bool_input('Vomit? y/n: '),
    parse_bool_input('Received injection today? y/n: '),
    parse_bool_input('Noticeable swelling today? y/n: '),
    parse_bool_input('Increased irritability today? y/n: '),
    parse_optional_input('Any additional notes? y/n: ', notes_prompt)
]

# queries
def create_table(table_name):
    return ('CREATE TABLE IF NOT EXISTS %s' %table_name)

table_columns = (
    'date TEXT PRIMARY KEY, weight REAL, arm_size REAL, '
    'abdomen_size REAL, bm_count INTEGER, vomit INTEGER default 0, '
    'injection INTEGER default 0, swelling INTEGER default 0, '
    'irritable INTEGER default 0,  notes TEXT default NULL'
)
create_query = create_table("ple_measurements") + '(' + table_columns + ')'
column_names = ['Date', 'Weight', 'Arm Size', 'Abdomen Girth', '# of Bowel Movements', 'Vomit', 'Injection', 'Swelling', 'Irritable', 'Notes']

c.execute(create_query)
c.execute('INSERT INTO ple_measurements VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', entry_list)
conn.commit()

# store ref to last record to show on exit
last_insert_id = c.lastrowid
c.execute('SELECT * FROM ple_measurements where rowid=%s' %last_insert_id)

print('The following data was successfully written: ')
print('---------------------------------------------')
last_in = c.fetchone()
print_last(column_names, last_in)

conn.close()

