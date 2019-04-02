import sqlite3
import sys
import nltk
from nltk.stem import *
from nltk.stem.porter import *

'''
Create and fill the database
TODO -- Parse file line by line
TODO -- FIgure out how to tokenize each word
'''

def init_db(c):
    try:
        # cleanup
        c.execute("DROP TABLE IF EXISTS Token;")
        c.execute("DROP TABLE IF EXISTS Posting;")
        c.execute("DROP INDEX IF EXISTS Token_idx;")

        c.execute('''
            CREATE TABLE Token (
                token TEXT,
                token_id INT,
                PRIMARY KEY(token_id)
            );''')

        c.execute('''
            CREATE TABLE Posting (
                token_id INT,
                doc_id INT,
                offset INT,
                before INT,
                after INT,
                FOREIGN KEY (token_id) REFERENCES Token(token_id)
            );''')

        c.execute('''
            CREATE UNIQUE INDEX Token_idx ON Token(token);
        ''')
    except:
        # cleanup
        c.execute("DROP TABLE IF EXISTS Token;")
        c.execute("DROP TABLE IF EXISTS Posting;")
        c.execute("DROP INDEX IF EXISTS Token_idx;")

        sys.exit("Error setting up db, exiting.")

def main():

    try:
        fname = sys.argv[1]
        fh = open(fname, 'r')
    except FileNotFoundError:
        sys.exit("Error, file not found.")

    # initialize the db
    conn = sqlite3.connect("sonnet.db")
    c = conn.cursor()
    init_db(c)

    x = 0
    for line in fh:
        if x == 5:
            break
        print(line)
        x += 1


if __name__ == '__main__':
    main()
