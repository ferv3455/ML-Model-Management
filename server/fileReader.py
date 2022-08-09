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
    yield 0

