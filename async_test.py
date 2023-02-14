import time
import threading
from multiprocessing import Process, Queue, Pool
import asyncio
import gevent
from mt_test import mt_func

q = Queue()

async def async_query_user_name(uid):
    await asyncio.sleep(1)
    return "Madcola"

async def async_query_user_school(uid):
    await asyncio.sleep(1)
    return "sysu"

def query_user_skills(uid):
    for i in range(1000):
        for j in range(1000):
            a = i*j
    return "Python,Go,C++,Shell"

def query_user_name(uid):
    time.sleep(0.05)
    return "Madcola"

def query_user_school(uid):
    time.sleep(0.05)
    return "sysu"

def log_usetime(fn):
    def wrapper(uid, callfn):
        start = time.time()
        res = fn(uid, callfn)

        end = time.time()
        print ("%s usetime:%f s" % (callfn.__name__, end-start))
        return res
    
    return wrapper 

def base_func(uid):
    school = query_user_school(uid)
    name = query_user_name(uid)
    skills = query_user_skills(uid)

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills

    return user_info

def async_func(uid):
    loop = asyncio.new_event_loop()
    t1 = loop.create_task(async_query_user_name(uid))
    t2 = loop.create_task(async_query_user_school(uid))
    skills = query_user_skills(uid)

    loop.run_until_complete(t1)
    loop.run_until_complete(t2)
    loop.close()

    name = t1.result()
    school = t2.result()

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills

    return user_info

def base_func(uid):
    school = query_user_school(uid)
    name = query_user_name(uid)
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

async def launch_proc(fn, uid):
    proc = Process(target=process_with_mq, args=(fn, uid))  
    proc.start()

@log_usetime
def async_mp_loop(uid, fn):
    processes = []
    result = []
    total = 1000
    loop = asyncio.new_event_loop()

    tasks = []
    for i in range(total):
        tasks.append(loop.create_task(launch_proc(fn, uid))) 

    for t in tasks:
        loop.run_until_complete(t) 
        

    while len(result) != total:
        res = q.get()
        result.append(res)
    return result

@log_usetime
def loop_gevent(uid, fn):
    result = []
    total = 1000
    jobs = [gevent.spawn(launch_proc, fn, uid) for i in range(total)]

    gevent.joinall(jobs)
    
    while len(result) != total:
        res = q.get()
        print(res)
        result.append(res)
    return result

def start_test():
    uid = 2899989
    #result = mp_loop(uid, async_func)
    #result = async_mp_loop(uid, base_func)
    #result = async_mp_loop(uid, async_func)
    #result = mp_loop(uid, mt_func)
    result = async_mp_loop(uid, mt_func)

if __name__ == '__main__':
    start_test()