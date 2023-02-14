import time
import threading

def query_user_name(uid):
    time.sleep(0.05)
    return "Madcola"

def query_user_school(uid):
    time.sleep(0.05)
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


from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(max_workers=10)

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

@log_usetime
def loop_test(uid, fn):
    result = []
    for i in range(1000):
        res = fn(uid)
        result.append(res)

    return result

@log_usetime
def mt_loop(uid, fn) :
    futures = []
    result = []
    for i in range(1000):
        f = thread_pool.submit(fn, uid)
        futures.append(f)
        
    for f in futures:
        result.append(f.result())

    return result


def start_test():
    uid = 2899989

    result = loop_test(uid, mt_func)
    result = loop_test(uid, mt_pool_func)
    #print(result)
    result = mt_loop(uid, mt_func)
    #result = mt_loop(uid, mt_pool_func)

if __name__ == '__main__':
    start_test()