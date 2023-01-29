import pathlib
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow, _RedirectWSGIApp, _WSGIRequestHandler
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import webbrowser
import wsgiref.simple_server
import wsgiref.util


def create_Service():
    CLIENT_SECRET_FILE = str(pathlib.Path(__file__).parent.resolve())+"/client-secrets.json"
    API_SERVICE_NAME = 'content'
    API_VERSION = 'v2.1'
    SCOPES = ['https://www.googleapis.com/auth/content']

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            success_message = """
            The authentication flow has completed. You may close this window.
            """
            wsgi_app = _RedirectWSGIApp(success_message)
            wsgiref.simple_server.WSGIServer.allow_reuse_address = False
            local_server = wsgiref.simple_server.make_server(
                'localhost', 8080, wsgi_app, handler_class=_WSGIRequestHandler
            )

            redirect_uri_format = ("http://{}:{}/")
            flow.redirect_uri = redirect_uri_format.format('localhost',
                                                           local_server.server_port)
            auth_url, _ = flow.authorization_url()
            webbrowser.open(auth_url, new=1, autoraise=True)
            print(auth_url)
            local_server.timeout = None
            local_server.handle_request()

            authorization_response = \
                wsgi_app.last_request_uri.replace("http", "https")
            flow.fetch_token(authorization_response=authorization_response)
            local_server.server_close()
            cred = flow.credentials

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service, 1
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None, 0