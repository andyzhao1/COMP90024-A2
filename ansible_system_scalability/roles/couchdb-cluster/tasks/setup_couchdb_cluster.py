import requests

#------------------configuration----------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------

def register_couchdb_node(master, node):
    master = master["domain"]
    node = node["domain"]

    url = "http://{}:{}@{}:{}/_cluster_setup".format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS)
    data = dict(
        action="enable_cluster",
        bind_address="0.0.0.0",
        username=COUCH_DB_USER,
        password=COUCH_DB_PASSWORD,
        port=COUCH_DB_PORTS,
        node_count=3,
        remote_node=node,
        remote_current_user=COUCH_DB_USER,
        remote_current_password=COUCH_DB_PASSWORD
    )
    headers = dict(
        contentType="application/json"
    )
    resp = requests.post(url, json=data, headers=headers)
    print(resp.status_code, resp.content)

    url2 = "http://{}:{}@{}:{}/_cluster_setup".format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS)
    data2 = dict(
        action="add_node",
        host=node,
        port=COUCH_DB_PORTS,
        username=COUCH_DB_USER,
        password=COUCH_DB_PASSWORD
    )
    resp = requests.post(url2, json=data2, headers=headers)
    print(resp.status_code, resp.content)

def finish_couchdb_cluster(master):
    master = master["domain"]

    url = "http://{}:{}@{}:{}/_cluster_setup".format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS)
    resp = requests.get(url)
    print(resp.status_code, resp.content)

    url2 = "http://{}:{}@{}:{}/_cluster_setup".format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS)
    data = dict(
        action="finish_cluster"
    )
    header = dict(
        contentType="application/json"
    )
    resp = requests.post(url2, json=data, headers=header)
    print(resp.status_code, resp.content)

def check_couchdb_membership(node):
    node = node["domain"]

    url = "http://{}:{}@{}:{}/_membership".format(COUCH_DB_USER, COUCH_DB_PASSWORD, node, COUCH_DB_PORTS)
    resp = requests.get(url)
    print(resp.status_code, resp.content)

if __name__ == "__main__" :
    register_couchdb_node(DOCKER_DOMAIN["instance-1"], DOCKER_DOMAIN["instance-2"])
    register_couchdb_node(DOCKER_DOMAIN["instance-1"], DOCKER_DOMAIN["instance-3"])
    register_couchdb_node(DOCKER_DOMAIN["instance-1"], DOCKER_DOMAIN["instance-4"])
    finish_couchdb_cluster(DOCKER_DOMAIN["instance-1"])

    #check_couchdb_membership(DOCKER_DOMAIN["instance-1"])
    #check_couchdb_membership(DOCKER_DOMAIN["instance-2"])
    #check_couchdb_membership(DOCKER_DOMAIN["instance-3"])
    check_couchdb_membership(DOCKER_DOMAIN["instance-4"])