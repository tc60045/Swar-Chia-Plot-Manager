import redis
import pickle
#import socket
#hostname = socket.gethostname()


def check_for_orders(xchiax_settings):
    r = redis.StrictRedis(host=redis_host, passwordd=redis_password, port=redis_port, db=0)  # use on a networked mac
    order_count = r.zcount('availabile-orders',0,'+inf') # assume ordered on epoch seconds
    if order_count > 0:
        order_pickle = r.zpopmin('available-orders').decode()
        order_details = pickle.loads(order_pickle.encode())
    else:
        order_details = dict()   # just keeping it null, folks
    return(order_details)

def inform_of_job_start(xchiax_settings, start_time, order_number, pid):   # keeping things stateful
    job_start_details = dict()
    job_start_details['machine_name'] = xchiax['unique_machine_name']
    job_start_details['start time'] = start_time
    job_start_details['order_number'] = order_number
    job_start_details['pid']=pid
    job_start_pickle = pickle.dumps(job_start_details,0)
    r.sadd('orders_started',job_start_pickle)
    # on server side, add that to global jobs started
    return()

