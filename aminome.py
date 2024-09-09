import yaml
import psycopg2
import psycopg2.extras
import orjson
import requests

def load_config(config_path):
    with open(config_path, 'r') as yml:
        return yaml.safe_load(yml)

def connect_db(config):
    return psycopg2.connect(
        host=config['db']['host'],
        user=config['db']['user'],
        password=config['db']['pass'],
        database=config['db']['db'],
        port=config['db']['port'],
        cursor_factory=psycopg2.extras.DictCursor
    )

def send_note_to_meil(config, notes):
    url = f"http://{config['meilisearch']['index']}:{config['meilisearch']['port']}/indexes/{config['meilisearch']['index']}---notes/documents?primaryKey=id"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['meilisearch']['apiKey']}"
    }
    response=requests.post(url, data=orjson.dumps(notes), headers=headers)
    print(response.content)

def parse_aid(id):
    TIME2000 = 946684800000
    t = int(int(id[:8], 36) + TIME2000)
    return t

def fetch_note_from_db(config, db, ofs=0, lmt=1000):
    notes = []

    while True:
        with db.cursor() as cur:
            if(config['meilisearch']['scope'] == 'local'):
                print("fetch local notes only")
                cur.execute('SELECT "id", "userId", "userHost", "channelId", "cw", "text", "tags" FROM "note" \
                            WHERE ("note"."visibility" = \'public\' OR "note"."visibility" = \'home\') AND\
                            ("note"."text" IS NOT NULL) AND\
                            ("note"."uri" IS NULL) \
                            LIMIT '  + str(lmt) + ' OFFSET ' + str(ofs))
            else:
                print("fetch local and global notes")
                cur.execute('SELECT "id", "userId", "userHost", "channelId", "cw", "text", "tags" FROM "note" \
                            WHERE ("note"."visibility" = \'public\' OR "note"."visibility" = \'home\') AND\
                            ("note"."text" IS NOT NULL) AND\
                            LIMIT '  + str(lmt) + ' OFFSET ' + str(ofs))
           
            qnotes = cur.fetchall()

            if not qnotes:
                break

        for note in qnotes:
            notes.append(format_note(note))

        print(f'{ofs=} {lmt=} {len(notes)=}')
        send_note_to_meil(config, notes)
        notes = []
        ofs = ofs + lmt

    db.close()

def format_note(note):
    return {
                'id': note['id'],
                'text': note['text'],
                'createdAt': parse_aid(note['id']),
                'userId': note['userId'],
                'userHost': note['userHost'],
                'channelId': note['channelId'],
                'cw': note['cw'],
                'text': note['text'],
                'tags': note['tags']
            }

def main():
    config = load_config('config/config.yml')

    db = connect_db(config)

    fetch_note_from_db(config, db)

if __name__ == "__main__":
    main()