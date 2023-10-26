# Register local notes on Misskey to Meilisearch
import psycopg2
import psycopg2.extras
import orjson
import requests
from datetime import datetime

# postgresql config
db = psycopg2.connect(
    host='localhost',
    user='misskey-user',
    password='password',
    database='misskey',
    port=5432,
    cursor_factory=psycopg2.extras.DictCursor
)

# meilisearch config
api_key = "APIKEY"
index = ""
url = f"http://localhost:7700/indexes/{index}---notes/documents?primaryKey=id"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# decode unixtimestamp (include milliseconds) from aid.
# ref. https://github.com/misskey-dev/misskey/blob/4b295088fd6b4bead05087537415b10419eee78f/packages/backend/src/misc/id/aid.ts#L34
def parse_aid(id):
    TIME2000 = 946684800000
    t = int(int(id[:8], 36) + TIME2000)
    return t

lmt = 100000
ofs = 0

notes = []

while True:
    with db.cursor() as cur:
        cur.execute('SELECT "id", "userId", "userHost", "channelId", "cw", "text", "tags" FROM "note" \
                    WHERE ("note"."visibility" = \'public\' OR "note"."visibility" = \'home\') AND\
                    ("note"."text" IS NOT NULL) AND\
                    ("note"."uri" IS NULL) \
                    LIMIT '  + str(lmt) + ' OFFSET ' + str(ofs))
        qnotes = cur.fetchall()
        if not qnotes:
            break
    for note in qnotes:
        notes.append({
            'id': note['id'],
            'text': note['text'],
            'createdAt': parse_aid(note['id']),
            'userId': note['userId'],
            'userHost': note['userHost'],
            'channelId': note['channelId'],
            'cw': note['cw'],
            'text': note['text'],
            'tags': note['tags']
        })
    print(f'{ofs=} {lmt=} {len(notes)=}')
    response = requests.post(url, data=orjson.dumps(notes), headers=headers)
    print(response.content)
    notes = []
    ofs = ofs + lmt

db.close()
