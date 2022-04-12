import sqlite3
import imagehash


class Db:
    def __init__(self, dblocation) -> None:
        self.connection = sqlite3.connect(dblocation)
        self.Create()

    def commit_to_db(self, query):

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def Create(self):
        """
        Creates Databases
        """
        query = """
        CREATE TABLE IF NOT EXISTS hashes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL UNIQUE,
        ahash TEXT,
        phash TEXT,
        dhash TEXT,
        whashhaar TEXT,
        whashdb4 TEXT,
        colorhash TEXT,
        cropresistant BLOB
        );
        """

        self.commit_to_db(query)

    def listify(self, results):
        """
        This function takes a list of tuples and returns a list of the first element of each tuple

        :param results: the results of the SQL query
        :return: A list of the first item in the tuple.
        """
        packet = []
        try:
            for field in results:
                packet.append(field[0])
        except:

            pass
        return packet

    def check_exist(self, filename):
        cursor = self.connection.cursor()
        query = f"""
        SELECT filename
        FROM hashes
            WHERE filename = '{filename}';
        """
        data = cursor.execute(query).fetchall()
        cleanedValue = self.listify(data)
        if len(cleanedValue) == 1:
            return True
        else:
            return False

    def check_crop_resist(self, hash, mode):
        # return False, ""
        cursor = self.connection.cursor()
        chunks = str(hash).split(",")
        for chunk in chunks:
            if chunk != "0000000000000000":

                query = f"""
                SELECT cropresistant, filename
                FROM hashes
                WHERE cropresistant LIKE '%{chunk}%';
                """
                data = cursor.execute(query).fetchall()

                if len(data) > 0:
                    print(data[0][1])
                    return True, [data[0][1]]
        return False, ""
        # hash_match, filename

    def check_hash(self, hash, mode):
        cursor = self.connection.cursor()
        query = f"""
        SELECT filename
        FROM hashes
        WHERE {mode} = '{hash}';
        """
        data = cursor.execute(query).fetchall()
        cleanedValue = self.listify(data)
        if len(cleanedValue) == 1:
            return True, cleanedValue
        else:
            return False, cleanedValue

    def add_hash(self, filename, ahash, phash, dhash, haar, db4, color, crop):
        query = f"""
        INSERT INTO hashes
        (    
        filename,
        ahash,
        phash,
        dhash,
        whashhaar,
        whashdb4,
        colorhash,
        cropresistant)
        VALUES
        (
            '{filename}',
            '{ahash}',
            '{phash}',
            '{dhash}',
            '{haar}',
            '{db4}',
            '{color}',
            '{crop}'
        );
        """
        self.commit_to_db(query)