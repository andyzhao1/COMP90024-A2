DOCKER_DOMAIN = {
    "instance-1": dict(
        domain="172.26.132.195"
    ),
    "instance-2": dict(
        domain="172.26.129.104"
    ),
    "instance-3": dict(
        domain="172.26.130.101"
    ),
    "instance-4": dict(
        domain="172.26.129.79"
    )
}


COUCH_DB_PORTS = 5984
COUCH_DB_USER = "COMP90024"
COUCH_DB_PASSWORD = "COMP90024"
COUCH_DB_ENV = ["COUCHDB_USER={}".format(COUCH_DB_USER), "COUCHDB_PASSWORD={}".format(COUCH_DB_PASSWORD)]