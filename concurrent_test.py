import gevent
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import Future

from concurrent.futures import ProcessPoolExecutor
import asyncio
from multiprocessing import Process, Queue, Pool


thread_pool = ThreadPoolExecutor(max_workers=10)
proc_pool = ProcessPoolExecutor()

q = Queue()

future = Future()

async def async_query_user_name(uid):
    await asyncio.sleep(0.05)
    return "Madcola"

async def async_query_user_school(uid):
    await asyncio.sleep(0.05)
    return "sysu"

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

class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread,self).__init__()
        self.result = None
        self.func = func
        self.args = args
    
    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result

def gevent_func(uid):

    g1 = gevent.spawn(query_user_school, uid)
    g2 = gevent.spawn(query_user_name, uid)
    g3 = gevent.spawn(query_user_skills, uid)
    gevent.joinall([g1,g2,g3])

    school = g1.value
    name = g2.value
    skills = g3.value

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills
    
    return user_info

def mt_func(uid) :

    t1 = MyThread(query_user_name, args=(uid,))
    t2 = MyThread(query_user_school, args=(uid,))
    t3 = MyThread(query_user_skills, args=(uid,))
    t1.start()
    t2.start()
    t3.start()

    # 等待三个线程的返回
    t1.join()
    t2.join()
    t3.join()

    name = t1.get_result()
    school = t2.get_result()
    skills = t3.get_result()

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills

    return user_info

#线程池
def mt_pool_func(uid) :

    f1 = thread_pool.submit(query_user_name, uid)
    f2 = thread_pool.submit(query_user_school, uid)
    f3 = thread_pool.submit(query_user_skills, uid)

    # 阻塞等待
    name = f1.result()
    school = f2.result()
    skills = f3.result()

    user_info = {}
    user_info["uid"] = uid
    user_info["school"] = school
    user_info["name"] = name
    user_info["skills"] = skills

    return user_info

async def async_call(fn, uid):
    response = await fn(uid)
    return response

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


def process_with_mq(fn, args):
    res = fn(args)
    q.put(res)

def on_task_finish(future):
    res = future.result()
    q.put(res)

@log_usetime
def mp_loop_with_pool(uid, fn):
    processes = []
    result = []
    total = 1000
    for i in range(total):
        future = proc_pool.submit(fn, uid)
        future.add_done_callback(on_task_finish)

    while len(result) != total:
        result.append(q.get())


@log_usetime
def mp_loop(uid, fn):
    processes = []
    result = []
    total = 1000
    for i in range(total):
        proc = Process(target=process_with_mq, args=(fn, uid))  
        proc.start()
        
    for p in processes:
        p.join()

    while q.qsize() != 0:
        result.append(q.get())


@log_usetime
def mt_loop(uid, fn) :
    futures = []
    result = []
    for i in range(1000):
        f = thread_pool.submit(fn, uid)
        futures.append(f)
        
    for f in futures:
        result.append(f.result())

@log_usetime
def loop_test(uid, fn):
    result = []
    for i in range(1000):
        res = fn(uid)
        result.append(res)

    return result

@log_usetime
def loop_gevent(uid, fn):
    result = []
    jobs = [gevent.spawn(fn, uid) for i in range(1000)]

    gevent.joinall(jobs)
    
    result = [job.value for job in jobs]

    return result

def start_test():
    uid = 2899989
    #loop_test(uid, base_func)
    #loop_test(uid, gevent_func)
    #loop_test(uid, mt_pool_func)
    #mt_loop(uid, base_func)
    #mp_loop_with_pool(uid, mt_func)
    #loop_gevent(uid, mt_func)
    #mp_loop_with_pool(uid, gevent_func)
    mp_loop_with_pool(uid, async_func)

    #loop_test(uid, async_func)

if __name__ == '__main__':
    start_test()
    proc_pool.shutdown(wait=True)
    thread_pool.shutdown()