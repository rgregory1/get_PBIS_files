import requests
import credentials
import paramiko
import zipfile

req = requests.get(credentials.sdex_url)

url_content = req.content

zip_file = open("files/sdex_download.zip", "wb")

zip_file.write(url_content)

zip_file.close()

import zipfile

with zipfile.ZipFile("files/sdex_download.zip", "r") as zip_ref:
    zip_ref.extractall("unzipped_files")


# Put files to raspberrypi server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname=credentials.pi_host,
    username=credentials.pi_user,
    password=credentials.pi_pass,
    port=credentials.pi_port,
)
sftp_client = ssh.open_sftp()


sftp_client.put("unzipped_files/CSVReferralData.csv", "custom/CSVReferralData.csv")
print("Put file on remote server")
sftp_client.close()
ssh.close()
