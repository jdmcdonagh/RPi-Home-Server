from kubernetes import client, config
from kubernetes.stream import stream
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import time


SA_CREDS = '/etc/secrets/gdrive-serviceaccount.json'
NAMESPACE = 'pihole'
POD_LABEL = 'app=pihole'

PIHOLE_FOLDER_ID = '1ProBu1EShecvbiSVqjPeYTqqtpk5bSMD'
NUM_BACKUPS = 3

def update_database():
    print('Rebuilding database')

    config.load_incluster_config()

    v1 = client.CoreV1Api()

    # get pihole pod name
    res = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=POD_LABEL)
    pod_name = res.to_dict()['items'][0]['metadata']['name']
    
    # execute command to rebuild database
    exec_command = ['/bin/bash', '-c', 'pihole -g']
    stream(v1.connect_get_namespaced_pod_exec,
        pod_name,
        NAMESPACE,
        command=exec_command,
        stderr=True, stdin=True,
        stdout=True, tty=False
    )

def upload_backup():
    print('Uploading backup to Google Drive')

    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SA_CREDS, 
        ['https://www.googleapis.com/auth/drive']
    )
    drive = GoogleDrive(gauth)

    # get previous backups sorted by modified date
    file_list = drive.ListFile({
        'q': f"'{PIHOLE_FOLDER_ID}' in parents and trashed=False",
        'orderBy': 'modifiedDate desc'
    }).GetList()

    # write latest backup
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    pihole_db = drive.CreateFile({
        'title': f'pihole_backup_{timestamp}.bin',
        'parents': [{'id': PIHOLE_FOLDER_ID}]
    })
    pihole_db.SetContentFile('/etc/pihole/gravity.db')
    pihole_db.Upload()
    print('Pihole database backup complete!')

    # delete excess backups
    delete_list = file_list[NUM_BACKUPS-1:]
    for file in delete_list:
        file.Trash()
        print(f"Deleted previous backup {file['title']}")

def main():
    update_database()
    upload_backup()

if __name__ == '__main__':
    main()
