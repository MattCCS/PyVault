
import datetime

# TODO: return True/False

def check_datetime(d, cutoff=datetime.timedelta(days=1)):
    d_client = datetime.datetime.fromtimestamp(float(d))
    d_server = datetime.datetime.now()
    if cutoff <= (d_server - d_client):
        print "Replay attack in connect M1"
        exit()
    else: 
        return d_client

def timestamp():
    return datetime.datetime.now().strftime("%s")
