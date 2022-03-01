import json
from neo4j import GraphDatabase


class MusicDatabase(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def write_data(
        self,
        singer_id,
        singer_name,
        singer_gender,
        singer_birthday,
        song_id,
        song_name,
        album_id,
        album_name,
    ):
        with self._driver.session() as session:
            greeting = session.write_transaction(
                self._write_data,
                singer_id,
                singer_name,
                singer_gender,
                singer_birthday,
                song_id,
                song_name,
                album_id,
                album_name,
            )
            print(greeting)

    @staticmethod
    def _write_data(
        tx,
        singer_id,
        singer_name,
        singer_gender,
        singer_birthday,
        song_id,
        song_name,
        album_id,
        album_name,
    ):
        result = tx.run(
            "MERGE (singer:Singer {id:$singer_id, name:$singer_name, gender:$singer_gender, birthday:$singer_birthday})"
            "MERGE (song:Song {id:$song_id, name:$song_name})"
            "MERGE (album:Album {id:$album_id, name:$album_name})"
            "MERGE (song)-[:SUNG_BY]->(singer)"
            "MERGE (song)-[:INCLUDED_IN]->(album)"
            "MERGE (album)-[:PUBLISHED_BY]->(singer)",
            singer_id=singer_id,
            singer_name=singer_name,
            singer_gender=singer_gender,
            singer_birthday=singer_birthday,
            song_id=song_id,
            song_name=song_name,
            album_id=album_id,
            album_name=album_name,
        )
        return result.single()


if __name__ == "__main__":
    with open("data.json") as fd:
        data = json.load(fd)
    db = MusicDatabase("bolt://localhost:7687", "neo4j", "neo4j")

    def get_singer_data(singer: str, attribute: str) -> str:
        for item in data["singer"]:
            if item["name"] == singer:
                return item[attribute]

        raise ValueError("value not found")

    singer_id = 0
    album_id = 0
    for item in data["song"]:
        db.write_data(
            singer_id,
            item["singer"],
            get_singer_data(item["singer"], "gender"),
            get_singer_data(item["singer"], "birthday"),
            item["id"],
            item["name"],
            album_id,
            item["album"],
        )
        singer_id += 1
        album_id += 1
    db.close()
