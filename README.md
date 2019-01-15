# FileCruiserStress

**
**  2014-2015 PROMISE Technology, Inc. All Rights Reserved.
**
**  FileCruiser stress tool v1.0
**
**  Author:       Jack Lin
**  Date:         Aug 25, 2015
**  Filecruiser:  VA (1.01.0000.73 or older)
**                VR (1.01.0001.78 or older)
**

--------------------------
      Description
--------------------------
1. Install required packages on client
   Windows:
   pip install setuptools
   pip install websocket
   pip install websocket-client

   Ubuntu:
   apt-get install python-setuptools
   apt-get install python3-websockets

   Mac OS X:
   pip3 install setuptools
   pip3 install websocket
   pip3 install websocket-client

   (If you have problem, you can go to webside to download and install it)
    https://pypi.org/project/websocket-client/

2. Install monga-client on client
   - Under source code directory
   cd monga_client
   sudo python3 setup.py install

3. Run stress tool on client (Linux / Windows) and stress on filecruiser server.

Step 1 -   Put all source code and configuration files in same folder.
Step 2 -   Create "upload_files" folder and file in it by running $ create_files.sh (or create_files.bat)
Step 3 -   Run script (ex: stress.sh)
Step 4 -   Collect token.txt, log.txt and user_number_file_name.csv
Step 5 -   Use SSH tool (ex: putty) to log in filecruiser server and use monitor tool to verify performance.


--------------------------
      File lists
--------------------------
1. token1.py -          Get token.
2. connect.py -         Web socket connect.
3. upload.py -          File upload.
4. download.py -        File download.
5. delete.py -          File deletion.
6. trash.py -           Clean trash can.
7. StressTest.conf -    Define server IP, domain and password.
8. action.conf -        Define which operation to run.
9. token.conf -         Define token count, if stop getting token and token refresh time.
10. connect.conf -      Define connection count and if stop web socket connection.
11. upload.conf -       Define user count for uploading file and if stop uploading file.
12. download.conf -     Define user count for downloading file.
13. delete.conf -       Define user count for deleting file.
14. trash.conf -        Define user count for cleaning trash can.
15. monga_client        Monga client folder.
16. create_files.py -   Create required files in "upload_files" folder.
17. create_files.conf - Define file size and its count.
18. create_files.sh -   Create file script.
19. stress.sh -         Sample script.


--------------------------
      Output files
--------------------------
1. token.txt -                 Token list for all users, valid for 24 hours.
2. log.txt -                   All log messages.
3. user_number_file_name.csv - Format: user number, upload time, get metadata time.


--------------------------
      Usage
--------------------------
python function_name.py function_name.conf

Ex:
python token1.py Start/Stop token.conf
python connect.py Start/Stop connect.conf
python upload.py Start upload.conf
python download.py Start download.conf
python delete.py Start delete.conf
python trash.py Start trash.conf


--------------------------
      Note
--------------------------
Please reference stress.sh for usage.
