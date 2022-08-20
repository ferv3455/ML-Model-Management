import base64
import io
import tempfile
import zipfile
import numpy as np

from PIL import Image
# import skvideo.io       # sudo apt-get install ffmpeg


def readCSV(data):
    # Convert to generator
    gen = iter(data.stream)

    # Extract header
    line = next(gen).strip()   # a bytes object
    header = line.decode('utf-8').split(',')

    # Read each line
    for i, line in enumerate(gen, 1):
        numbers = (float(n) for n in line.strip().split(b','))
        yield ('index', i, dict(zip(header, numbers)))


def readZIP(data, param_name):
    # Open zip
    zipObj = zipfile.ZipFile(data.stream._file)
    filenames = zipObj.namelist()

    # Open each file
    for filename in filenames:
        with zipObj.open(filename, 'r') as fp:
            # Process different formats
            if filename.endswith('.npy'):
                # NumPy data file
                arr = np.load(fp)

            # elif filename.endswith('.mp4'):
            #     # Video file: write to a temporary file first
            #     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            #         tmp.write(fp.read())
            #         arr = skvideo.io.vread(tmp.name)

            else:
                # Image file
                img = Image.open(io.BytesIO(fp.read()))
                arr = np.asarray(img)

            yield ('filename', filename, {param_name: arr})


def decodeFile(string: str):
    '''Converting base64-encoded string into numpy ndarray.'''
    # Identify header
    try:
        header, string = string.split(',')
        fmt, encoding = header.split(';')
        assert encoding == 'base64'
        print(fmt)
    except:
        print('No header in string')

    # Decoding
    try:
        result = base64.b64decode(string)
        if fmt.startswith('data:image/'):
            # Image
            img = Image.open(io.BytesIO(result))
            arr = np.asarray(img)
            return arr

        elif fmt == 'data:application/octet-stream':
            # Other: NumPy supported only
            arr = np.load(io.BytesIO(result))
            return arr
        
        else:
            # Default: Image
            img = Image.open(io.BytesIO(result))
            arr = np.asarray(img)
            return arr

    except Exception as exc:
        print('Data not readable:', exc)
