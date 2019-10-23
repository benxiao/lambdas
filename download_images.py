import requests
import tqdm
import time
import os
#from threading import Thread

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with open('urls.txt', 'r') as fp, open("remains.txt", 'a') as fp2:
    lines = set(x.rstrip('\n').strip('"') for x in fp)
    print(len(lines))
    for url in tqdm.tqdm(sorted(lines)):
        try:
            fn = url.rsplit("/")[-1]
            if os.path.isfile(fn):
                continue

            resp = requests.get(url, headers=HEADERS)

            if resp.status_code != 200:
                fp2.write(url+'\n')
                fp2.flush()

            with open(fn, "wb") as outfile:
                outfile.write(resp.content)

        except Exception as e:
            fp2.write(url+'\n')
            fp2.flush()
