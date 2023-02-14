import time
import threading
from multiprocessing import Process, Queue, Pool
from concurrent.futures import ProcessPoolExecutor

q = Queue()

def query_user_name(uid):
    time.sleep(1)
    return "Madcola"

def query_user_school(uid):
    time.sleep(1)
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


proc_pool = ProcessPoolExecutor()

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

    return result

def start_test():
    uid = 2899989

    #result = mp_loop(uid, base_func)
    #print(result)
    result = mp_loop(uid, mt_func)
    #print(result)
    #result = mp_loop_with_pool(uid, base_func)
    #result = mp_loop_with_pool(uid, mt_func)

if __name__ == '__main__':
    start_test()