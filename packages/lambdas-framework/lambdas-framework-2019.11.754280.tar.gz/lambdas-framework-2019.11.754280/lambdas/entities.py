# Standard imports
import base64
import pickle
import random
import asyncio
import inspect
import sqlite3 as db
import tempfile
import textwrap
import functools
from typing import Any, Callable, Iterable, List, Tuple

# Third parties imports
import flask
import aiohttp
import requests
from ruamel import yaml
# pylint: disable=import-error
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Local imports
from lambdas.constants import (
    AVAILABLE_CPUS,
    COMPUTING_NODE_DEFAULT_HOST,
    COMPUTING_NODE_DEFAULT_PORT,
    HEADERS_BINARY,
    HEADERS_TEXT,
)
from lambdas.exceptions import (
    ManagerNodeException,
)
from lambdas import log

# Setup
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def response_text(msg: str):
    return \
        flask.Response(status=200, headers=HEADERS_TEXT, response=f'{msg}\n')


def response_binary(msg: bytes):
    return \
        flask.Response(status=200, headers=HEADERS_BINARY, response=msg)


def object_to_data(obj: Any) -> bytes:
    obj_pickled: bytes = pickle.dumps(obj)
    obj_encoded: bytes = base64.b64encode(obj_pickled)
    return obj_encoded


def data_to_object(data: bytes) -> Any:
    data_decoded: bytes = base64.b64decode(data)
    obj: Any = pickle.loads(data_decoded)
    return obj


def object_from_request() -> Any:
    data: bytes = flask.request.get_data(cache=False)
    return data_to_object(data)


def param_from_request(param: str, default=None) -> Any:
    return flask.request.args.get(param, default)


def execute_function(function, function_args, function_kwargs):
    func_sig: inspect.Signature = inspect.signature(function)
    func_bind: inspect.BoundArguments = \
        func_sig.bind(*function_args, **function_kwargs)
    func_bind.apply_defaults()
    params = ', '.join(
        f'{arg}={value!r}'
        for arg, value in func_bind.arguments.items())
    log.info(textwrap.dedent(f"""
        signature:    {function.__name__}{func_sig}
        arguments:    {function.__name__}({params})
    """))
    return_object = function(*function_args, **function_kwargs)
    log.info(textwrap.dedent(f"""
        return-type:  {type(return_object)}
        return-value: {return_object}
    """))
    return return_object


def asynchronous_map(func: Callable, args: List[Any],
                     results_per_loop: int = 64,
                     return_exceptions: bool = True,
                     ) -> Iterable[Any]:
    loop = asyncio.new_event_loop()
    for index in range(0, len(args), results_per_loop):
        future = asyncio.gather(
            *(asyncio.ensure_future(func(*a, **k), loop=loop)
              for a, k in args[index:index + results_per_loop]),
            return_exceptions=return_exceptions,
            loop=loop)
        yield from loop.run_until_complete(future)
    loop.close()


class ComputingNode():

    def __init__(self,
                 host: str = COMPUTING_NODE_DEFAULT_HOST,
                 port: int = COMPUTING_NODE_DEFAULT_PORT,
                 processes: int = AVAILABLE_CPUS):
        log.info(f'Running with {processes} CPUs')
        self.connection = db.connect(database=tempfile.mkstemp()[1],
                                     isolation_level=None)
        self.cursor = self.connection.cursor()
        self.db_create_table()

        self.service = flask.Flask(ComputingNode.__name__)
        self.service.add_url_rule(
            rule='/',
            view_func=self.route,
            methods=['GET'])
        self.service.add_url_rule(
            rule='/list',
            view_func=self.route_list,
            methods=['GET'])
        self.service.add_url_rule(
            rule='/set',
            view_func=self.route_set,
            methods=['PUT'])
        self.service.add_url_rule(
            rule='/del',
            view_func=self.route_del,
            methods=['DELETE'])
        self.service.add_url_rule(
            rule='/run',
            view_func=self.route_run,
            methods=['GET', 'POST'])
        self.service.run(
            host=host, port=port,
            processes=processes, threaded=False,
            ssl_context='adhoc')

    @staticmethod
    def route():
        return response_text('Welcome to this Computing Node!')

    def route_list(self):
        log.info('Listing lambdas')
        lambdas_list = self.db_get_lambdas()
        lambdas = yaml.safe_dump(lambdas_list,
                                 allow_unicode=True,
                                 default_style='|',
                                 default_flow_style=False,
                                 explicit_start=True,
                                 explicit_end=True)
        log.info(lambdas)
        return response_text(lambdas)

    def route_set(self):
        log.info('Received function code')
        function_code = object_from_request()
        function_code = self.sanitize_code(function_code)
        log.info(textwrap.indent(function_code, '+ '))
        function_name, _ = self.load_function(function_code)
        self.db_set_lambda(function_name, function_code)
        log.info(f'Mapped to: {function_name}')
        return f'Bound: {function_name}'

    def route_del(self):
        function_name = param_from_request('lambda')
        log.info(f'Received query to delete: {function_name}')
        self.db_del_lambda(function_name)
        log.info(f'Deleted: {function_name}')
        return f'Un-bound: {function_name}'

    def route_run(self):
        function_name = param_from_request('lambda')
        log.info(f'Received query to execute: {function_name}')
        function_code = self.db_get_lambda(function_name)
        _, function = self.load_function(function_code)
        return function()

    @staticmethod
    def sanitize_code(function_code):
        return textwrap.dedent(function_code).strip('\n')

    @staticmethod
    def load_function(function_code):
        locals_gathered = {}
        exec(function_code, {}, locals_gathered)  # pylint: disable=exec-used
        function_name, function = locals_gathered.popitem()

        @functools.wraps(function)
        def function_wrapped():
            payload = object_from_request()
            function_args = payload.get('args', [])
            function_kwargs = payload.get('kwargs', {})
            return_object = \
                execute_function(function, function_args, function_kwargs)
            return_encoded: bytes = object_to_data(return_object)
            return response_binary(return_encoded)

        return function_name, function_wrapped

    def db_create_table(self):
        self.cursor.execute("""
            CREATE TABLE lambdas (name TEXT PRIMARY KEY, code TEXT)
            """)
        self.db_set_lambda('demo', """
            def demo():
                return "Hello world!"
            """)

    def db_set_lambda(self, name, code):
        code = self.sanitize_code(code)
        self.cursor.execute('REPLACE INTO lambdas VALUES (?, ?)', (name, code))

    def db_del_lambda(self, name):
        self.cursor.execute('DELETE FROM lambdas WHERE name=?', (name,))

    def db_get_lambdas(self):
        return {
            name: code
            for name, code in
            self.cursor.execute('SELECT name, code FROM lambdas')
        }

    def db_get_lambda(self, name):
        function_code = [
            name for name, in self.cursor.execute(
                'SELECT code FROM lambdas WHERE name=?', (name,))]
        if function_code:
            return function_code[0]
        raise ManagerNodeException(f'No such function: {name}')


class ManagerNode():

    def __init__(self):
        self.computing_nodes: List[Tuple[str, int]] = []
        self.computations_to_do: List[Tuple[Any, Any]] = []

    def register_computing_node(self,
                                host: str = COMPUTING_NODE_DEFAULT_HOST,
                                port: int = COMPUTING_NODE_DEFAULT_PORT):
        self.computing_nodes.append((host, port))

    def register_lambda(self, function_code):
        for host, port in self.computing_nodes:
            response = requests.put(
                url=f'https://{host}:{port}/set',
                data=object_to_data(function_code),
                verify=False,
            )
            log.info(f'status: {response.status_code}, {response.text}')

    def deregister_lambda(self, function_name):
        for host, port in self.computing_nodes:
            response = requests.delete(
                url=f'https://{host}:{port}/del',
                params={
                    'lambda': function_name,
                },
                verify=False,
            )
            log.info(f'status: {response.status_code}, {response.text}')

    def compute(self, function_name: str, *args, **kwargs):
        if not self.computing_nodes:
            raise ManagerNodeException('No available Computing Nodes')

        host, port = random.choice(self.computing_nodes)

        response = requests.get(
            url=f'https://{host}:{port}/run',
            params={
                'lambda': function_name,
            },
            data=object_to_data({
                'args': args,
                'kwargs': kwargs
            }),
            timeout=None,
            verify=False,
        )
        if response.status_code == 200:
            return data_to_object(response.content)
        raise ManagerNodeException(response.content)

    async def compute_async(self, function_name: str, *args, **kwargs):
        if not self.computing_nodes:
            raise ManagerNodeException('No available Computing Nodes')

        host, port = random.choice(self.computing_nodes)

        async with aiohttp.ClientSession(
                trust_env=True,
                connector=aiohttp.TCPConnector(
                    verify_ssl=False),
                timeout=aiohttp.ClientTimeout(
                    total=None,
                    connect=None,
                    sock_connect=None,
                    sock_read=None)) as session:
            async with session.get(
                    url=f'https://{host}:{port}/run',
                    params={
                        'lambda': function_name,
                    },
                    data=object_to_data({
                        'args': args,
                        'kwargs': kwargs,
                    })) as response:
                response_content = await response.read()
                response_status = response.status

        if response_status == 200:
            return data_to_object(response_content)
        raise ManagerNodeException(response_content)

    def queue_computation(self, function_name: str, *args, **kwargs):
        self.computations_to_do.append(((function_name, *args), kwargs))

    def solve_computations(self) -> Iterable[Any]:
        yield from asynchronous_map(self.compute_async,
                                    self.computations_to_do)
        self.computations_to_do.clear()
