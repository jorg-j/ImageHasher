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

    def writedupes(self):
        cursor = self.connection.cursor()
        hashes = ["ahash", "phash", "dhash", "dhash", "whashhaar", "whashdb4"]

        for hash in hashes:
            query = f"""
            SELECT filename, {hash} FROM hashes
            WHERE {hash} in(
                SELECT {hash} FROM hashes GROUP BY {hash} HAVING COUNT(id)>1
            )
            ORDER BY {hash};
            """
            data = cursor.execute(query).fetchall()
            if len(data) > 0:
                import csv

                header = ["filename", hash]
                with open(f"{hash}.csv", "w", encoding="UTF-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for i in data:
                        writer.writerow(i)

    def check_exist(self, filename):
        """
        It checks if a filename exists in the database

        :param filename: The name of the file to be checked
        :return: A list of tuples.
        """
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

    def check_crop_resist(self, hash):
        """
        It takes a hash, splits it into chunks, and then checks if any of those chunks are in the database.
        If they are, it returns True and the filename

        :param hash: the hash of the image
        :return: a tuple.
        """
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

    def check_hash(self, hash, mode):
        """
        It takes a hash and a mode (ahash, phash, etc) and checks if the hash is in the database. If it
        is, it returns True and the filename. If it isn't, it returns False and an empty list.

        :param hash: the hash to check
        :param mode: ahash, phash, dhash, haar, db4, color, crop
        :return: A tuple of two values.
        """
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
        """
        It takes a filename, and the hashes of that file, and inserts them into the database

        :param filename: the name of the file
        :param ahash: Average hash
        :param phash: Perceptual hash
        :param dhash: Difference hash
        :param haar: Haar wavelet hash
        :param db4: wavelet hash
        :param color: a 64-bit integer that represents the color of the image
        :param crop: a boolean value that indicates whether the image is crop resistant or not
        """
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

    def get_file_by_hash(self, hash):
        cursor = self.connection.cursor()
        query = f"""SELECT filename FROM hashes where cropresistant = '{hash}';"""
        data = cursor.execute(query).fetchall()
        cleanedValue = self.listify(data)
        return cleanedValue[0]

    def cropresist_csv(self):
        import csv

        storage = []
        cursor = self.connection.cursor()
        query = """SELECT cropresistant FROM hashes;"""
        data = cursor.execute(query).fetchall()
        cleanedValue = self.listify(data)
        for row in cleanedValue:
            hashes = row.split(",")
            for chunk in hashes:
                if chunk != "0000000000000000":
                    query = f"""
                    SELECT filename, cropresistant
                    FROM hashes
                    WHERE cropresistant LIKE '%{chunk}%'
                    AND cropresistant != '{row}';
                    """
                    data = cursor.execute(query).fetchall()
                    if len(data) > 0:
                        source_file = self.get_file_by_hash(row)
                        temp = (data[0][0], source_file, data[0][1], chunk, row)
                        storage.append(temp)

        if len(storage) > 0:
            header = ["filename", "matchedFile", "hash", "match_chunk", "fullhash"]
            with open(f"cropresist.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(storage)

