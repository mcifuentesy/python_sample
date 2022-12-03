import pickle
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import utils, encoders
import mimetypes
import subprocess
import base64


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'\\token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file,'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

#Definimos la conexión de Gmail para el envio de correos
def envioEmail(Msg,To,Bcc,Subject):
    CLIENT_SECRET_FILE = r"\credentials.json"
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg= Msg
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = To
    mimeMessage['bcc'] = Bcc
    mimeMessage['from'] = 'Sender'
    mimeMessage['subject'] = Subject

    mimeMessage.attach(MIMEText(emailMsg, 'html'))
   
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_string().encode()).decode()

    message = service.users().messages().send(userId = 'me', body = {'raw': raw_string}).execute()

mensaje_enviar = '''<p class="MsoNormal" style="background-image:initial;background-position:initial;background-size:initial;background-repeat:initial;background-origin:initial;background-clip:initial"><i><span lang="EN-US" style="font-size:12pt;font-family:inherit;color:black">Good morning,</span></i><span lang="EN-US" style="font-size:12pt;color:black"><u></u><u></u></span></p>
<p style="margin:0cm;font-size:11pt;font-family:Calibri,sans-serif"><i><span lang="EN-US" style="color:black">&nbsp;</span></i><span lang="EN-US"><u></u><u></u></span></p>
<p style="margin:0cm;font-size:11pt;font-family:Calibri,sans-serif"><i><span lang="EN-US" style="color:black">MESSAGE TO SEND</span></i><span lang="EN-US"><u></u><u></u></span></p>
<p style="margin:0cm;font-size:11pt;font-family:Calibri,sans-serif"><span lang="EN-US">&nbsp;</span></p>
<p><i><span lang="ES-CO" style="color:black">Cordially</span></i></p>'''    

envioEmail(mensaje_enviar, "Recipient", "Sender", "Subject")
