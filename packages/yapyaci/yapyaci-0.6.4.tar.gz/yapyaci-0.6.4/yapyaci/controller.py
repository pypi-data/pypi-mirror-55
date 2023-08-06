from .exception import AuthFailure, InvalidLookupRequest, WsOpenFailure, InvalidToken, InvalidJsonPayload, AuthRefreshFailure, SubRefreshFailure, QueryFailure
from .object_set import AciSet, AciTree, ListOfAciTree, to_tree, to_ltree
import http.client
import threading
import logging
import json
import time

logger1 = logging.getLogger(__name__)


class ApiCtx:
    def __init__(self, ip, username, password):
        self.base_header = {
                'cache-control': 'no-cache',
                'Content-Type': 'test/plain'
        }

        # Ctrl access details
        self.ip = ip
        self.username = username
        self.password = password

        # Auth token details
        self.Cookie = ''
        self.token = ''
        self.urlToken = ''

        # Websocket Status
        self.ws_status = "CLOSE"

        # Threads details and Thread lock
        self.lock = threading.Lock()

        self.aaa_refresh_thread_running = False
        self.sub_refresh_thread_running = False

        self.subscription_list = list()

    def reset_token(self):
        self.Cookie = ''
        self.token = ''
        self.urlToken = ''

    @property
    def ws_url(self):
        return "wss://{0}/socket{1}?{2}".format(self.ip, self.token, self.urlToken)

    @property
    def http_header(self):
        header = self.base_header

        if self.urlToken and self.Cookie:
            header['APIC-challenge'] = self.urlToken
            header['Cookie'] = self.Cookie

        return header

    @property
    def authenticated(self):
        if self.Cookie and self.urlToken:
            return True
        else:
            return False


class HttpClient:
    def __init__(self, ctx: ApiCtx):
        self._ctx = ctx
        self.__conn = http.client.HTTPSConnection(self._ctx.ip, http.client.HTTPS_PORT)
        #self.__conn = http.client.HTTPConnection(self._ctx.ip, http.client.HTTP_PORT)

    def _authenticate(self):
        http_body = {
            'aaaUser' : {
                'attributes': {
                    'name': self._ctx.username,
                    'pwd': self._ctx.password
                }
            }
        }

        http_response_code, http_response_header, http_response_payload = self._send_post("/api/aaaLogin.json?gui-token-request=yes", http_body)

        if http_response_code == 200:
            logger1.warning('Authentication successful')
            ltree = ListOfAciTree(http_response_payload)
            aaaLogin = to_tree(ltree.search('aaaLogin'))
            self._ctx.urlToken = aaaLogin.urlToken
            self._ctx.token = aaaLogin.token
            self._ctx.Cookie =  http_response_header('Set-Cookie')

        else:
            raise AuthFailure('Failed to login to {0}'.format(self._ctx.ip))

    def _send_get(self, url):
        if not self._ctx.authenticated and url != "/api/aaaLogin.json?gui-token-request=yes":
            logger1.warning('Proceeding with authentication')
            self._authenticate()

        try:
            self.__conn.request('GET', url, '', self._ctx.http_header)
            http_response = self.__conn.getresponse()
            http_response_payload = json.loads(http_response.read().decode('utf-8'))

        except json.decoder.JSONDecodeError as error:
            logger1.critical("Respond payload not in JSON format")
            raise

        except TimeoutError as error:
            logger1.critical("Connection Timeout")
            raise

        except Exception as error:
            logger1.critical(error)
            raise

        logger1.info('{0} - {1}'.format(url, http_response.code))
        return http_response.code, http_response.getheader, http_response_payload


    def _send_post(self, url, payload):
        if not self._ctx.authenticated and url != "/api/aaaLogin.json?gui-token-request=yes":
            logger1.warning('Proceeding with authentication')
            self._authenticate()

        try:
            self.__conn.request('POST', url, json.dumps(payload), self._ctx.http_header)
            http_response = self.__conn.getresponse()
            http_response_payload = json.loads(http_response.read().decode('utf-8'))

        except json.decoder.JSONDecodeError as error:
            logger1.critical("Respond payload not in JSON format")
            raise

        except TimeoutError as error:
            logger1.critical("Connection Timeout")
            raise

        except Exception as error:
            logger1.critical(error)
            raise

        logger1.info('{0} - {1}'.format(url, http_response.code))
        return http_response.code, http_response.getheader, http_response_payload

    def disconnect(self):
        self.__conn.close()
        self._ctx.reset_token()


class Api(HttpClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def lookup_by_class(self, cls, **kwarg) -> ListOfAciTree:
        if not self._ctx.authenticated:
            logger1.warning('Proceeding with authentication')
            self._authenticate()

        base_url = "/api/node/class/"
        url = base_url + cls + ".json?"

        for key, value in kwarg.items():
            url += "&" + key.replace('_', '-') + '=' + value

        http_response_code, http_response_header, http_response_payload = self._send_get(url)

        if http_response_code == 200:
            return ListOfAciTree(http_response_payload)

        else:
            logger1.error('Lookup failed with code {0}'.format(http_response_code))
            self._ctx.reset_token()

            raise QueryFailure('Query failed with code {0}'.format(http_response_code))

    def lookup_by_dn(self, dn, **kwarg) -> AciTree:
        if not self._ctx.authenticated:
            logger1.warning('Proceeding with authentication')
            self._authenticate()

        base_url = "/api/mo/"
        url = base_url + dn + ".json?"

        for key, value in kwarg.items():
            url += "&" + key.replace('_', '-') + '=' + value

        http_response_code, http_response_header, http_response_payload = self._send_get(url)

        if http_response_code == 200:
            return AciTree(http_response_payload)

        else:
            logger1.error('Lookup failed with code {0}'.format(http_response_code))
            self._ctx.reset_token()
            raise QueryFailure('Query failed with code {0}'.format(http_response_code))

    def lookup(self, **kwarg) -> AciSet:
        if not self._ctx.authenticated:
            logger1.warning('Proceeding with authentication')
            self._authenticate()

        if 'cls' in kwarg.keys():
            base_url = "/api/node/class/"
            url = base_url + kwarg.pop('cls') + ".json?"

        elif 'dn' in kwarg.keys():
            base_url = "/api/mo/"
            url = base_url + kwarg.pop('dn') + ".json?"

        else:
            raise InvalidLookupRequest("Failed to lookup. Neither a class nor a dn was provided")

        for key, value in kwarg.items():
            url += "&" + key.replace('_', '-') + '=' + value

        http_response_code, http_response_header, http_response_payload = self._send_get(url)

        if http_response_code == 200:
            return AciTree(http_response_payload)

        else:
            logger1.error('Lookup failed with code {0}'.format(http_response_code))
            self._ctx.reset_token()
            raise QueryFailure('Query failed with code {0}'.format(http_response_code))

    def mqapi2(self, tool, **kwarg):
        base_url = "/mqapi2/"
        url = base_url + tool + ".json?"

        for key, value in kwarg.items():
            url += "&" + key.replace('_', '-') + '=' + value

        http_response_code, http_response_header, http_response_payload = self._send_get(url)
        return ListOfAciTree(http_response_payload)


class AuthRefreshThread(threading.Thread):
    def __init__(self, ctx, *args, **kwargs):
        super(AuthRefreshThread, self).__init__(*args, **kwargs)
        self._ctx = ctx

    def run(self):
        logger1.error('Starting the refresh authentication loop')

        while self._ctx.authenticated:
            try:
                time.sleep(360)

                logger1.warning('Refreshing auth token')

                self._ctx.lock.acquire()

                # conn = http.client.HTTPConnection(self._ctx.ip, http.client.HTTP_PORT)
                conn = http.client.HTTPSConnection(self._ctx.ip, http.client.HTTPS_PORT)
                conn.request('GET', "/api/aaaRefresh.json?gui-token-request=yes", '', self._ctx.http_header)
                http_response = conn.getresponse()

                http_response_payload = json.loads(http_response.read().decode('utf-8'))

                if http_response.code == 200:
                    logger1.error('Token successfully refreshed')

                    ltree = ListOfAciTree(http_response_payload)
                    aaaLogin = to_tree(ltree.search('aaaLogin'))
                    # shared.urlToken = aaaLogin.urlToken
                    self._ctx.token = aaaLogin.token
                    self._ctx.Cookie = http_response.getheader('Set-Cookie')
                    self._ctx.lock.release()

                else:
                    logger1.error(
                        'Failed to refresh token with HTTP respond code {0}. Stopping the aaa refresh loop'.format(
                            http_response.code))
                    self._ctx.aaa_refresh_thread_running = False
                    self._ctx.reset_token()
                    self._ctx.lock.release()

            except Exception as error:
                logger1.critical(error)


class SubscriptionRefreshThread(threading.Thread):
    def __init__(self, ctx, stream_handler, *args, **kwargs):
        super(SubscriptionRefreshThread, self).__init__(*args, **kwargs)
        self._stream_handler = stream_handler
        self._ctx = ctx

    def run(self):
        refresh_failure = False
        while not refresh_failure:
            time.sleep(30)

            self._ctx.lock.acquire()
            # conn = http.client.HTTPConnection(self._ctx.ip, http.client.HTTP_PORT)
            conn = http.client.HTTPSConnection(self._ctx.ip, http.client.HTTPS_PORT)

            for sub in self._ctx.subscription_list:
                conn.request('GET', '/api/subscriptionRefresh.json?id={0}'.format(sub), '', self._ctx.http_header)
                http_response = conn.getresponse()
                http_response_payload = json.loads(http_response.read().decode('utf-8'))

                if http_response.code == 200:
                    logger1.error('Sub {0} successfully refresh'.format(sub))

                else:
                    logger1.error('Sub {0} failed to be refresh'.format(sub))
                    self._stream_handler.kill_thread()
                    self._ctx.reset_token()
                    refresh_failure = True

            self._ctx.lock.release()
            conn.close()

        logger1.error("The subscription loop has been stopped")


class EApi(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream_handler_thread = None

    def lookup_by_class(self, *args, **kwarg) -> ListOfAciTree:
        rsp = super().lookup_by_class(*args, **kwarg)

        if not self._ctx.aaa_refresh_thread_running:
            refresh_loop = AuthRefreshThread(ctx=self._ctx, name='AuthRefreshThread')
            refresh_loop.start()
            self._ctx.aaa_refresh_thread_running = True

        return rsp

    def lookup_by_dn(self, *args, **kwarg) -> AciTree:
        rsp = super().lookup_by_dn(*args, **kwarg)

        if not self._ctx.aaa_refresh_thread_running:
            refresh_loop = AuthRefreshThread(ctx=self._ctx, name='AuthRefreshThread')
            refresh_loop.start()
            self._ctx.aaa_refresh_thread_running = True

        return rsp

    def lookup(self, **kwarg) -> AciSet:
        rsp = super().lookup(**kwarg)

        if not self._ctx.aaa_refresh_thread_running:
            refresh_loop = AuthRefreshThread(ctx=self._ctx, name='AuthRefreshTread')
            refresh_loop.start()
            self._ctx.aaa_refresh_thread_running = True

        return rsp

    def subscribe(self, *args, **kwarg):
        rsp = self.lookup(**{**kwarg, **{'subscription': 'yes'}})

        if rsp.subscription_id and not self._ctx.sub_refresh_thread_running:
            logger1.warning('Starting subscription loop')
            sub_refresh_loop = SubscriptionRefreshThread(self._ctx, self._stream_handler_thread, name='SubRefreshThread')
            self._ctx.sub_refresh_thread_running = True
            sub_refresh_loop.start()

        if rsp.subscription_id and rsp.subscription_id not in self._ctx.subscription_list:
            logger1.info('New subscription id {0}'.format(rsp.subscription_id))
            self._ctx.subscription_list.append(rsp.subscription_id)

        return rsp

    def setup_stream(self, stream_handler_class, *args, **kwargs):
        if not self._ctx.authenticated:
            self._authenticate()

        self._stream_handler_thread = stream_handler_class(ctx=self._ctx, *args, **kwargs)
        self._stream_handler_thread.start()

        for c in range(5):
            if self._ctx.ws_status == "OPEN":
                break

            logger1.warning('Waiting for WebSocket to be opened...')
            time.sleep(1)

        if self._ctx.ws_status != "OPEN":
            raise WsOpenFailure('Failed to opened WebSocket within 5 sec')

        return self._stream_handler_thread




