from kubernetes import client, config
from kubernetes.stream import stream
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import time
import os

SA_CREDS = '/etc/secrets/gdrive-serviceaccount.json'
NAMESPACE = 'pihole'
POD_LABEL = 'app=pihole'

PIHOLE_FOLDER_ID = '1ProBu1EShecvbiSVqjPeYTqqtpk5bSMD'

def download_backup():
    print('Downloading backup from Google Drive')

    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SA_CREDS, 
        ['https://www.googleapis.com/auth/drive']
    )
    drive = GoogleDrive(gauth)

    # wait for initial database to be written
    while True:
        if os.path.isfile('/etc/pihole/gravity.db'):
            break
        print('Initial database not created yet, sleeping...')
        time.sleep(5)

    # get backups sorted by modified date
    file_list = drive.ListFile({
        'q': f"'{PIHOLE_FOLDER_ID}' in parents and trashed=False",
        'orderBy': 'modifiedDate desc',
        'maxResults': 1
    }).GetList()

    # copy latest to dest
    file_list[0].GetContentFile('/etc/pihole/gravity.db')
    print(f"Restored backup {file_list[0]['title']}")

def update_database():
    print('Rebuilding database from backup')

    config.load_incluster_config()

    v1 = client.CoreV1Api()

    # get pihole pod name
    res = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=POD_LABEL)
    pod_name = res.to_dict()['items'][0]['metadata']['name']
    
    # execute command to rebuild database
    exec_command = ['/bin/bash', '-c', 'pihole restartdns reload-lists']
    res = stream(v1.connect_get_namespaced_pod_exec,
        pod_name,
        NAMESPACE,
        command=exec_command,
        stderr=True, stdin=True,
        stdout=True, tty=False
    )

def main():
    download_backup()
    update_database()

if __name__ == '__main__':
    main()
