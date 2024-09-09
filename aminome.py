import argparse
import orjson
import requests
import psycopg2
import psycopg2.extras
import yaml

__version__ = '0.2.0'

def arg_parse():
    return argparse.ArgumentParser(
        prog="aminome",
        usage="python3 aminome.py -c config/config.yml",
        description="Add all misskey notes to Meilisearch.",
        add_help=True,
    )

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
    if(config['meilisearch']['ssl'] == "true"):
        url = f"https://{config['meilisearch']['index']}:{config['meilisearch']['port']}/indexes/{config['meilisearch']['index']}---notes/documents?primaryKey=id"
    else:
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

def fetch_note_from_db(config, db, ofs, lmt):
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
    parser = arg_parse()
    parser.add_argument("-c", "--config", 
                        type=str, 
                        default='config/config.yml', 
                        help="Set the path of the configuration file. Default is config/config.yml.")
    parser.add_argument("--offset", 
                        type=int, 
                        default=0, 
                        help="Set the offset value. Default is 0.")
    parser.add_argument("--limit", 
                        type=int, 
                        default=1000, 
                        help="Set how many notes to get in one query. Default is 1000.")
    parser.add_argument('-v', '--version', action='version',
                        version=__version__,
                        help='Show version and exit')
    args = parser.parse_args()

    config = load_config(args.config)

    db = connect_db(config)

    fetch_note_from_db(config, db, args.offset, args.limit)

if __name__ == "__main__":
    main()
