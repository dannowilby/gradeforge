import atexit
from multiprocessing import Process, Queue

from waitress import serve

from .app import app
from .generator import run

if __name__ == '__main__':
    queue = Queue()
    
    generator = Process(target=run, args=(queue,))
    generator.start()

    atexit.register(lambda: queue.put(None)) # send kill signal
    serve(app(generator, queue), host='0.0.0.0', port=5000)