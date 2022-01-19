import sqlite3


class DaoDB():
    def __init__(self):
        super().__init__()
        self.database = sqlite3.connect("./danser/danser.db")
        self.cursor = self.database.cursor()

    def get_beatmap_data(self, beatmap_hash):
        self.cursor.execute(f'SELECT artist, title, version, dir||"/"||bg FROM beatmaps WHERE md5 = ?', [(beatmap_hash)])
        return self.cursor.fetchall()[0]
