import os
import zipfile

path = '8'
zf = zipfile.ZipFile("myzipfile.zip", "w")
for dirname, subdirs, files in os.walk(path):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()

os.remove("myzipfile.csv")