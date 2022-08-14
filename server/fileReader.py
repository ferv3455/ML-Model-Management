import base64
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


def readZIP(data, param_name):
    # Open zip
    zipObj = zipfile.ZipFile(data.stream._file)
    filenames = zipObj.namelist()

    # Open each file
    for filename in filenames:
        with zipObj.open(filename, 'r') as fp:
            img = Image.open(io.BytesIO(fp.read()))
            arr = np.asarray(img)
            yield {param_name: arr}


def decodeFile(string: str):
    '''Converting base64-encoded string into numpy ndarray.'''
    # Identify header
    try:
        header, string = string.split(',')
        fmt, encoding = header.split(';')
        assert encoding == 'base64'
        print(fmt)
        # TODO: different formats can be processed
    except:
        print('No header in string')

    # Decoding
    result = base64.b64decode(string)
    img = Image.open(io.BytesIO(result))
    arr = np.asarray(img)
    return arr
