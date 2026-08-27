import os
import urllib.request
import gzip

os.makedirs("datasets", exist_ok=True)
urllib.request.urlretrieve("https://snap.stanford.edu/data/web-Stanford.txt.gz", "datasets/web-Stanford.txt.gz")
data = gzip.open("datasets/web-Stanford.txt.gz", "rb").read()
open("datasets/web-Stanford.txt", "wb").write(data)
