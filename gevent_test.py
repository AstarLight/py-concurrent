import time
import threading
from multiprocessing import Process, Queue, Pool
from concurrent.futures import ProcessPoolExecutor
import gevent

q = Queue()

def query_user_name(uid):
    gevent.sleep(0.05)
    return "Madcola"

def query_user_school(uid):
    gevent.sleep(0.05)
    return "sysu"

def query_user_skills(uid):
    for i in range(1000):
        for j in range(1000):
            a = i*j
    return "Python,Go,C++,Shell"


def log_usetime(fn):
    def wrapper(uid, callfn):
        start = time.time()
        res = fn(uid, callfn)

        end = time.time()
        print ("%s usetime:%f s" % (callfn.__name__, end-start))
        return res
    
    return wrapper 


def gevent_func(uid):

    g1 = gevent.spawn(query_user_school, uid)
    g2 = gevent.spawn(query_user_name, uid)
    #g3 = gevent.spawn(query_user_skills, uid)
    gevent.joinall([g1,g2])

    school = g1.value
    name = g2.value
    skills = query_user_skills(uid)

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills
    
    return user_info



def process_with_mq(fn, args):
    res = fn(args)
    q.put(res)

def on_task_finish(future):
    res = future.result()
    q.put(res)


@log_usetime
def mp_loop(uid, fn):
    processes = []
    result = []
    total = 1000
    for i in range(total):
        proc = Process(target=process_with_mq, args=(fn, uid))  
        proc.start()
        

    while len(result) != total:
        res = q.get()
        result.append(res)
    return result


def start_test():
    uid = 2899989

    result = mp_loop(uid, gevent_func)
    #print(result)

if __name__ == '__main__':
    start_test()