import sqlite3
import sys
import nltk
from nltk.stem import *
from nltk.stem.porter import *

'''
Create and fill the database
TODO -- Stemming has been commented out for now
TODO -- Find way to get before/after IDs
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

        sys.exit("Error setting up db, aborting.")


def parse_line(line):
    tokens = nltk.word_tokenize(line)
    # stemmer = PorterStemmer()
    stemmed_tokens = []
    punctuation = [',', '.', ';', ':', "'", '"', '-']

    for token in tokens:
        if token in punctuation:
            continue

        # token = stemmer.stem(token.lower())
        stemmed_tokens.append(token)

    return stemmed_tokens


def index_tokens(c, tokens, id, offset):
    before = after = None
    for token in tokens:
        token_id = in_index(token, c)       # check if token exists

        if token_id is None:                # else, add it
            token_id = get_highest_id(c)

            if token_id is None:
                token_id = 0
            else:
                token_id += 1

            c.execute('''
            INSERT INTO Token VALUES (?,?);
            ''', (token, token_id,))

        c.execute('''
        INSERT INTO Posting VALUES (?,?,?,?,?);
        ''', (token_id, doc_id, offset, before, after))

        offset += 1

    return offset


def in_index(token, c):
    c.execute('''
        SELECT token_id
        FROM Token
        WHERE token=?;''', (token,))

    token_id = c.fetchone()

    if token_id is not None:
        return token_id[0]

    return None


def get_highest_id(c):
    c.execute('''SELECT MAX(token_id) FROM Token;''')
    max_id = c.fetchone()

    return max_id[0]


def main():

    try:
        fname = sys.argv[1]
        infile = open(fname, 'r')
    except FileNotFoundError:
        sys.exit("Error, file not found.")

    # initialize the db
    conn = sqlite3.connect("sonnet.db")
    c = conn.cursor()
    init_db(c)

    id = 0
    x = 0
    for line in infile:

        line = line.strip()

        try:                    # new sonnet
            id = int(line)
            offset = 0          # reset offset
            # print(id)

        except ValueError:                 # sonnet body
            tokens = parse_line(line)
            # if x < 5:
            #     print(tokens)
            #     x += 1
            offset = index_tokens(c, tokens, id, offset)


if __name__ == '__main__':
    main()
