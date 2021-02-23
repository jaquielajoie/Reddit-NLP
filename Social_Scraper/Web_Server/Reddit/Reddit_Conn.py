import praw
import json

import betamax
from betamax_serializers import pretty_json
import requests
from prawcore import Requestor

from datetime import datetime

#from praw import Reddit


class JSONDebugRequestor(Requestor):
    def request(self, *args, **kwargs):
        response = super().request(*args, **kwargs)
        print(json.dumps(response.json(), indent=4))
        return response



class Reddit_Conn:
    def __init__(self, url, username='', password=''):

        betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
        with betamax.Betamax.configure() as config:
            config.cassette_library_dir = 'cassettes'
            config.default_cassette_options['serialize_with'] = 'prettyjson'


        self.session = requests.Session()

        self.reddit_conn = praw.Reddit(
            "bot1"
            #user_agent='AGenderOfGeese user agent'
            #requestor_class=JSONDebugRequestor,
            #requestor_kwargs={"session": my_session}
        )
        self.reddit_conn.read_only = True

        #http = self.reddit_conn._core._requestor._http
        #http.headers['Accept-Encoding'] = 'identity'
        self.recorder = betamax.Betamax(self.session,
                                        cassette_library_dir='cassettes')

        with self.recorder.use_cassette(f'recording-session-bot1-{datetime.now()}'):
            self.session.get(f'{url}')
        '''
        comment = self.reddit_conn.comment('dhb7fxz')
        with self.recorder.use_cassette('test_check_comment__valid'):
            return None



        self.session = betamax.Betamax(requests.Session())
        CASSETTE_LIBRARY_DIR = 'Social_Scraper/cassettes/'
        self.recorder = betamax.Betamax(
            self.session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )
        with self.recorder.use_cassette('our-first-recorded-session'):
            self.session.get('https://httpbin.org/get')
            '''
    def connection(self):
        return self.reddit_conn
