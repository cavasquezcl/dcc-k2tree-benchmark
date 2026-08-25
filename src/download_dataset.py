import os
import urllib.request
import gzip

os.makedirs("datasets", exist_ok=True)
urllib.request.urlretrieve("https://snap.stanford.edu/data/ca-GrQc.txt.gz", "datasets/ca-GrQc.txt.gz")
data = gzip.open("datasets/ca-GrQc.txt.gz", "rb").read()
open("datasets/ca-GrQc.txt", "wb").write(data)