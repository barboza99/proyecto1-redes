from fileinput import filename
import ftplib

HOSTNAME = "ftp.dlptest.com"
USERNAME = "dlpuser"
PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu"

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
ftp_server.encoding = "UTF-8"

filename = "client.py"

fl = open(filename, "rb")
ftp_server.storbinary(f"STOR {filename}", fl)
# with open("holamundo.txt", "rb") as file:
#     ftp_server.storbinary(f"STOR {filename}", file)

ftp_server.dir()

ftp_server.quit()