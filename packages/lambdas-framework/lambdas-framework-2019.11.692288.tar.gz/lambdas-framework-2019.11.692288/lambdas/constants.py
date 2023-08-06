# Standard imports
import multiprocessing

# Constants
AVAILABLE_CPUS = multiprocessing.cpu_count()
COMPUTING_NODE_DEFAULT_HOST = '0.0.0.0'
COMPUTING_NODE_DEFAULT_PORT = 4000

HEADERS_BINARY = {
    'Content-Type': ' application/octet-stream; charset=binary'
}
HEADERS_TEXT = {
    'Content-Type': 'text/plain; charset=utf-8'
}
