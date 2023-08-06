import eel
import time
import os
import pathlib
import shutil
import zipfile
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']
SAMPLE_RANGE_NAME = 'Mallas!A3:A1000'

spreadsheet_uri = ""

HOME_PATH = os.getenv("HOME")
CALAMARDO_LAUNCHER_PATH = HOME_PATH + "/.calamardo"
CALAMARDO_LAUNCHER_CREDENTIAL_PATH = CALAMARDO_LAUNCHER_PATH + "/google-credential.json"
CALAMARDO_LAUNCHER_TOKEN_PATH = CALAMARDO_LAUNCHER_PATH + "/token.pickle"
CALAMARDO_LAUNCHER_TOKENS_PATH = CALAMARDO_LAUNCHER_PATH + "/tokens"
CALAMARDO_LAUNCHER_EXTRACT_PATH = CALAMARDO_LAUNCHER_PATH + "/calamardo_jar"
CALAMARDO_JAR_PATH = HOME_PATH + "/.m2/repository/com/bbva/cib/core/common/calamardo-app/0.1.6/calamardo-app-0.1.6-jar-with-dependencies.jar"


def get_calamardo_google_credentials():
    if not pathlib.Path(CALAMARDO_LAUNCHER_CREDENTIAL_PATH).exists():
        pathlib.Path(CALAMARDO_LAUNCHER_PATH).mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(CALAMARDO_JAR_PATH) as z:
            z.extractall(CALAMARDO_LAUNCHER_EXTRACT_PATH)
        shutil.copy(CALAMARDO_LAUNCHER_EXTRACT_PATH + "/tokens/google-credential.json", CALAMARDO_LAUNCHER_PATH)
        shutil.rmtree(CALAMARDO_LAUNCHER_EXTRACT_PATH)

    if pathlib.Path(CALAMARDO_LAUNCHER_TOKENS_PATH).exists():
        shutil.copy(CALAMARDO_LAUNCHER_TOKENS_PATH, ".")


def ask_for_credentials(scopes):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists(CALAMARDO_LAUNCHER_TOKEN_PATH):
        with open(CALAMARDO_LAUNCHER_TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CALAMARDO_LAUNCHER_CREDENTIAL_PATH, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CALAMARDO_LAUNCHER_TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


@eel.expose
def load_data(spreadsheet):
    global spreadsheet_uri
    spreadsheet_uri = spreadsheet
    creds = ask_for_credentials(SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return [value[0].split("_")[0] for value in values]


@eel.expose
def generate_data(chain, enviroment, outputs):
    # TODO checkear si se puede ejecutar java
    # TODO checkear si existe el binario de calamardo
    for output in outputs:
        cmd = ("java -jar " + CALAMARDO_JAR_PATH +
               " -m " + chain +
               " -e " + enviroment +
               " -g " + spreadsheet_uri +
               " -x " + output + " >file.log 2>&1")
        os.system(cmd)

        send_log()
    shutil.copy("tokens", CALAMARDO_LAUNCHER_PATH)


def send_log():
    logger = open("file.log", "r")
    for line in logger:
        eel.addOutput(line)
        time.sleep(0.03)

    os.remove("file.log")


def run():

    mvn_return = os.system("mvn dependency:get -DgroupId=com.bbva.cib.core.common -DartifactId=calamardo-app -Dclassifier=jar-with-dependencies -Dversion=0.1.6  > /dev/null")
    if mvn_return is not 0:
        print("Error downloading Calamardo jar file")
        exit(-1)

    get_calamardo_google_credentials()

    web_location = 'web'
    web_path = os.path.dirname(os.path.realpath(__file__)) + '/' + web_location
    eel.init(web_path)

    try:
        chrome_instance_path = eel.chrome.get_instance_path()
        if chrome_instance_path is not None and os.path.exists(chrome_instance_path):
            eel.start('main.html', size=(1100, 900), options={'port': 0})
        else:
            eel.start('main.html', size=(1100, 900), options={'port': 0, 'mode': 'user selection'})
    except (SystemExit, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    run()
