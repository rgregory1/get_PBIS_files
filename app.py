import requests
import credentials
import paramiko
import zipfile
import csv

# get files from SDEX
req = requests.get(credentials.sdex_url)

url_content = req.content

zip_file = open("files/sdex_download.zip", "wb")

zip_file.write(url_content)

zip_file.close()

# extract the files
with zipfile.ZipFile("files/sdex_download.zip", "r") as zip_ref:
    zip_ref.extractall("unzipped_files")

# create header row list
header_rows = [
    "ReferralId",
    "SchoolSwisId",
    "SchoolNcesId",
    "StudentDistrictId",
    "StudentSwisId",
    "StudentFirstName",
    "StudentLastName",
    "StudentGradeId",
    "StudentIep",
    "EducatorDistrictId",
    "EducatorSwisId",
    "EducatorFirstName",
    "EducatorLastName",
    "ReferralDate",
    "ReferralTime",
    "ProblemBehaviorId1",
    "ProblemBehaviorSubTypeIdentifier1",
    "ProblemBehaviorId2",
    "ProblemBehaviorSubTypeIdentifier2",
    "ProblemBehaviorId3",
    "ProblemBehaviorSubTypeIdentifier3",
    "ProblemBehaviorId4",
    "ProblemBehaviorSubTypeIdentifier4",
    "ProblemBehaviorId5",
    "ProblemBehaviorSubTypeIdentifier5",
    "LocationId",
    "MotivationId",
    "OthersInvolvedId",
    "AdminDecisionId1",
    "AdminDecisionDuration1",
    "AdminDecisionId2",
    "AdminDecisionDuration2",
    "AdminDecisionId3",
    "AdminDecisionDuration3",
    "AdminDecisionId4",
    "AdminDecisionDuration4",
    "AdminDecisionId5",
    "AdminDecisionDuration5",
    "SeclusionRestraintId",
    "OtherInfo",
    "5thminor",
    "Threat/Intimidation",
    "MajorProblemBehavior",
]

# add header and create new file for upload
with open("unzipped_files/SWIS_data.csv", "w", newline="") as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(header_rows)

    with open("unzipped_files/CSVReferralData.csv", "r", newline="") as incsv:
        reader = csv.reader(incsv)
        writer.writerows(row + [0.0] for row in reader)

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


sftp_client.put("unzipped_files/SWIS_data.csv", "custom/SWIS_data.csv")
print("Put file on remote server")
sftp_client.close()
ssh.close()
