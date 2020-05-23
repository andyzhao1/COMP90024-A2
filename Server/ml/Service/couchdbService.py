import couchdb

def server_connection():
    try:
        server = couchdb.Server('http://COMP90024:COMP90024@172.26.132.195:5984/')
        print("CouchDB is connected: " + str(server) + "\n")
        return server

    except Exception as e:
        print(e)

def get_db(server, db_name):
    try:
        db = server[db_name]
        return db
    except Exception as e:
        print(e)

def create_db(server, db_name):
    try:
        db = server.create(db_name)
        print("Database %s is created\n" % (db_name))
        return db
    except Exception as e:
        print(e)
               
def create_doc(db, document):
    doc_id, doc_rev = db.save(document)
    doc = db[doc_id]
    return doc

# ServiceImpl
def getTextsFromView(db_name,view_name):
    server = server_connection()
    db = get_db(server,db_name)
    view = db.view(view_name,reduce = False)
    texts = []
    for each in view:
        texts.append(each.value)
    return texts

