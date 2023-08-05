import time
from urllib.parse import urlparse, parse_qs
from threading import Thread
from threading import Lock
from .server import HttpServer
from .configuration import Configuration
from .scenario import Scenario
from .clients.android import AndroidClient
from .clients.ios import IosClient
from .clients.osx import OsxClient
from .storage import Storage
from .log import Log

class TestLab(object):
    def __init__(self, path_or_json):
        RequestHandler.TEST_LAB = self
        self.configuration = Configuration(path_or_json)

        self.server = None
        self.server_url = self.configuration.json.get('server_url', 'http://127.0.0.1:8010')
        self.server_url = str(self.server_url)
        if ':' in self.server_url:
            index = self.server_url.rfind(':')
            self.server_port = int(self.server_url[index+1:])
            self.server_url = self.server_url[:index]
        else:
            self.server_port = 8000
        self.server_thread = None
        self.monitor_thread = None
        self.start_time_monitor = 0

        self.results_storage = Storage()
        self.scenarios = []
        for scenario in self.configuration.json['scenarios']:
            self.scenarios.append(Scenario(scenario))

        self.clients = []
        self.clients_count = 0
        self._create_clients()
        self._terminate = False
        self.mutex = Lock()

    def run(self):
        self._run_server()
        for scenario in self.scenarios:
            self.results_storage.push_test_case(scenario.name)
            self._run_monitor(scenario)
            try:
                self._run_scenario(scenario)
            except RuntimeError as error:
                Log.error(error)
                self._terminate = True
            self.monitor_thread.join()
        self._stop_server()
        self._print_results()

    def _run_server(self):
        Log.info('Run server')

        def worker():
            self.server.serve_forever()

        self.server = HttpServer.start(url=self.server_url, port=self.server_port,
                                       request_handler_class=RequestHandler)
        self.server_thread = Thread(target=worker)
        self.server_thread.start()

    def _run_monitor(self, scenario):
        Log.info('Run monitor')

        def worker():
            self.start_time_monitor = time.time()
            while time.time() <= self.start_time_monitor + scenario.timeout:
                time.sleep(1)
                with self.mutex:
                    if self._terminate:
                        break
                    current = self.results_storage.get_records_count(scenario.name)
                    elapsed = int(time.time() - self.start_time_monitor)
                    Log.debug('Progress: {}s {}/{}', elapsed, current, self.clients_count)
                    if current >= self.clients_count:
                        break

        self.monitor_thread = Thread(target=worker)
        self.monitor_thread.start()

    def _run_scenario(self, scenario):
        def worker(client, scenario_name):
            self.clients_count += client.launch(self.configuration, scenario_name)

        threads = []
        for client in self.clients:
            thread = Thread(target=worker, args=(client, scenario.name))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def _stop_server(self):
        Log.info('Stop server')
        if self.server:
            self.server.shutdown()
            self.server_thread.join()
            self.server = None

    def _create_clients(self):
        threads = []

        def create(platform):
            clients = {
                'android': AndroidClient,
                'ios': IosClient,
                'osx': OsxClient,
            }
            if platform not in clients:
                return None
            client = clients[platform](self.configuration)
            client.server_url = 'http://{}:{}'.format(self.server_url, self.server_port)
            self.clients.append(client)
            self.clients_count += len(client.devices)

        for platform in self.configuration.json['clients']:
            thread = Thread(target=create, args=(platform, ))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def _print_results(self):
        Log.whitespace()
        Log.result('Tests result:')
        success = len(self.results_storage.results) == len(self.scenarios)
        for test_case in self.results_storage.results:
            Log.result('  Test: {}', test_case.name)
            for record in test_case.results:
                Log.result('    Platform: {}, Name: {}, ID: {}, Result code: {}, Duration: {}s', record.client_platform,
                                                                                                 record.client_name,
                                                                                                 record.client_id,
                                                                                                 record.result_code,
                                                                                                 record.duration)
                success = success and (record.result_code == 0)
            success = success and len(test_case.results) == self.clients_count
        Log.result('Sumary: {}', 'Success' if success else 'Failed')
        exit(0 if success else 1)

    def add_result(self, code, scenario, client_id, client_name, client_platform):
        elapsed_seconds = int(time.time() - self.start_time_monitor)
        self.results_storage.add_result(scenario, code, client_id, client_name, client_platform, elapsed_seconds)


class RequestHandler:
    TEST_LAB = None

    def __init__(self, server):
        self.response = None
        self.server = server

    def handle(self, _, payload):
        try:
            parsed = urlparse(payload)
            params = parse_qs(parsed.query)
            Log.debug('Got Payload: {}', payload)
            if parsed.path == '/result' and 'code' in params or 'scenario' in params:
                code = int(params['code'][0])
                scenario = params['scenario'][0]
                client_id = params['id'][0] if 'id' in params else 'unknown'
                client_name = params['name'][0] if 'name' in params else 'unknown'
                client_platform = params['platform'][0] if 'platform' in params else 'unknown'
                with RequestHandler.TEST_LAB.mutex:
                    RequestHandler.TEST_LAB.add_result(code, scenario, client_id, client_name, client_platform)
        except RuntimeError:
            self.server.send('error'.encode())
        else:
            self.server.send('ok'.encode())
