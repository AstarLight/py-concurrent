import requests
import json
import time


if __name__ == '__main__':
    url = "http://127.0.0.1:9999/query_user_info?uid=102329"
    total = 100

    start = time.time()

    for i in range(total):
        response = requests.get(url)

    end = time.time()
    use_time = end-start
    print("use time: %fs, avg: %fs" % (use_time, use_time/total))
    print (response.text)