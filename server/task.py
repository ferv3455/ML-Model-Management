import pickle
from traceback import print_exc

from celery import Celery

from model import Model

app = Celery('task', backend='redis://localhost:16379/1',
             broker='redis://localhost:16379/2')


@app.task
def predict(modelID, type, data, pre_processer=None):
    for key, value in data.items():
        try:
            # convert back to ndarray if it is a encoded
            if isinstance(value, str) and value.startswith('encoded-ndarray:'):
                data[key] = pickle.loads(value[16:].encode('latin-1'))
                print(data[key].shape)
        except:
            print_exc()

    model = Model('name', 'des', type, './models/{}.{}'.format(modelID, type))
    return model.predict(data, pre_processer)


if __name__ == '__main__':
    args = [
        'worker',
        '--loglevel=INFO',
        '-Q',
        'service1',
        '--without-gossip',
        '--without-mingle',
        '--without-heartbeat',
        '-Ofair',
        '--purge'
    ]
    app.worker_main(argv=args)
