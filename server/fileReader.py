import io
import zipfile
import numpy as np

from PIL import Image


def readCSV(data):
    # Convert to generator
    gen = iter(data.stream)

    # Extract header
    line = next(gen).strip()   # a bytes object
    header = line.decode('utf-8').split(',')

    # Read each line
    for line in gen:
        numbers = (float(n) for n in line.strip().split(b','))
        yield dict(zip(header, numbers))


def readZIP(data):
    # Open zip
    zipObj = zipfile.ZipFile(data.stream._file)
    filenames = zipObj.namelist()

    # Open each file
    for filename in filenames:
        with zipObj.open(filename, 'r') as fp:
            img = Image.open(io.BytesIO(fp.read()))
            arr = np.asarray(img)
            yield arr
