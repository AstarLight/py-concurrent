

import time


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


def log_usetime(fn):
    def wrapper(uid, callfn):
        start = time.time()
        res = fn(uid, callfn)

        end = time.time()
        print ("%s usetime:%f s" % (callfn.__name__, end-start))
        return res
    
    return wrapper 


@log_usetime
def loop_test(uid, fn):
    result = []
    for i in range(1000):
        res = fn(uid)
        result.append(res)

    return result


def start_test():
    uid = 2899989

    result = loop_test(uid, base_func)
    #print(result)

if __name__ == '__main__':
    start_test()