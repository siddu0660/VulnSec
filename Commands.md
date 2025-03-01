**ClamAV**

* Using clamscan:

Here’s the list of all possible clamscan commands with indexed numbering and examples:  
**1\. Basic Commands**

| Flag  | Function  | example |
| :---- | :---- | :---- |
| \-h or \--help | Display help information for clamscan.  | clamscan \-h |
|  \-V or \--version | Display the version of clamscan. | clamscan \-V  |

**2\. Scanning Options**

| Flag  | Function  | example |
| :---- | :---- | :---- |
|  \-r or \--recursive | Scan directories recursively. | clamscan \-r /home/user |
| \-i or \--infected | Show only infected files in the scan results.  | clamscan \-i /home/user  |
|  \--remove | Automatically remove infected files.  | clamscan \--remove /home/user  |
| \--move=DIR | Move infected files to the specified directory. | clamscan \--move=/home/user/quarantine /home/user  |
| \--copy=DIR | Copy infected files to the specified directory.  | clamscan \--copy=/home/user/quarantine /home/user  |
| \--exclude=PATTERN | Exclude files matching the specified pattern.  | clamscan \--exclude='\\.jpg$' /home/user |
| \--exclude-dir=PATTERN | Exclude directories matching the specified pattern. | clamscan \--exclude-dir='/tmp' /home/user  |
| \--log=FILE | Write scan results to a log file.  | clamscan \--log=/var/log/clamscan.log /home/user  |
| \--max-filesize=SIZE   | Specify the maximum file size to scan.  | clamscan \--max-filesize=10M /home/user  |
|  \--max-scansize=SIZE | Set the maximum total size of data scanned. | clamscan \--max-scansize=100M /home/user |
|  \--max-recursion=NUMBER | Set the maximum recursion level for scanning archives. | clamscan \--max-recursion=10 /home/user  |
| \--max-files=NUMBER | Set the maximum number of files to scan. | clamscan \--max-files=100 /home/user  |
| \--include=PATTERN | Include only files matching the specified pattern. | clamscan \--include='\\.txt$' /home/user  |

**3\. Output Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
| \--quiet | Suppress all output except errors | clamscan \--quiet /home/user |
| \--no-summary | Do not display the summary of the scan results. | clamscan \--no-summary /home/user |
| \--stdout | Write all messages to stdout. | clamscan \--stdout /home/user |

**4\. Debugging Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
|  \--debug | Display debugging information. | clamscan \--debug /home/user |
| \--leave-temps | Do not remove temporary files created during scanning. | clamscan \--leave-temps /home/user  |

**5\. Database and Configuration Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
|  \--config-file=FILE |  Specify a custom configuration file. | clamscan \--config-file=/etc/clamav/clamscan.conf /home/user |
| \--datadir=DIR | Specify a custom directory for the virus database. | clamscan \--datadir=/var/lib/clamav /home/user |
| \--database=FILE | Specify a specific database file to use. | clamscan \--database=/var/lib/clamav/main.cvd /home/user |
|  \--reload  | Reload the virus database. | clamscan \--reload |

**6\. Special Scan Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
| \--bell | Sound a bell when a virus is found. | clamscan \--bell /home/user |
|  \--scan-mail | Scan mail files. | clamscan \--scan-mail /home/user |
|  \--scan-archive | Scan within archive files. | clamscan \--scan-archive /home/user |
|  \--scan-pdf | Scan PDF files | clamscan \--scan-pdf /home/user |
|  \--scan-html  | Scan HTML files.  | clamscan \--scan-html /home/user |

This indexed list includes clamscan commands along with concise examples for each. Let me know if you need further details\!

* Using freshcalm(**Virus Database Updater)**

Here’s a comprehensive list of all possible freshclam commands and options, grouped for easy reference:  
**1\. Basic Commands**

| Flag | Function |
| :---- | :---- |
|  \-v or \--verbose | Display detailed output during the update process. |
| –quiet | Suppress output except for errors. |
|  \-h or \--help | Display help information for the freshclam command |
|  \-V or \--version | Display the version of freshclam. |

**2\. Configuration Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
| \--config-file=FILE | Specify a custom configuration file.  | freshclam \--config-file=/path/to/custom.conf |
| \--datadir=DIR  | Specify a custom directory for the virus database. | freshclam \--datadir=/var/lib/clamav |
| \--log=FILE | Write logs to a specified file. | freshclam \--log=/var/log/freshclam.log  |
|  \--pid=FILE | Specify a PID file for the daemon |  |

**3\. Update Behavior Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
|  \--no-dns | Disable DNS-based version checks. |  |
|  \--no-digests | Disable downloading of database signature digests. |  |
|  \--no-mirror | Skip downloading database files from mirrors. |  |
| \--notify=COMMAND | Run a command after a successful database update. | freshclam \--notify="/path/to/script.sh" |
| \--databases=DB1,DB2,... | Update only specified databases (e.g., main, daily, bytecode). | freshclam \--databases=main,daily  |
| \--test-database=DBFILE | Test the integrity of a local database file. |  |

**4\. Proxy and Network Options**

| Flag | Function |
| :---- | :---- |
|  \--http-proxy\[=URL\] | Use an HTTP proxy for updates. If no URL is provided, use the value from the configuration file. |
|  \--log-verbose | Include detailed network information in logs |
|  \--connect-timeout=N | Set the connection timeout in seconds (default is 30\) |
| \--recv-timeout=N | Set the data receiving timeout in seconds (default is 30\) |
|  \--proxy-auth=USER:PASS | Set the proxy authentication credentials. |

**5\. Debugging Options**

| Flag | Function |
| :---- | :---- |
| \--debug | Enable debugging output for troubleshooting |
| \--force | Force updates even if the database is up to date |

**6\. Daemon Mode Options**

| Flag | Function |
| :---- | :---- |
|  \--foreground | Run freshclam in the foreground (don’t fork into the background) |
| \--on-update-execute=COMMAND | Execute a command after an update is completed. |
| \--on-error-execute=COMMAND  | Execute a command if an error occurs during the update. |
|  \--checks=N | Number of database checks per day (default is 24). |

* Using **clamdscan (Daemon-based Scanner):**

**1\. Basic Commands**

| Flag | Function | Example |
| :---- | :---- | :---- |
| \-h or \--help | Display help information for the clamdscan command. | clamdscan \-h  |
| \-V or \--version  | Display the version of clamdscan. | clamdscan \-V |

**2\. Scanning Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
|  \--multiscan | Use multiple threads for scanning to improve performance | clamdscan \--multiscan /home/user |
| \--fdpass | Pass file descriptors to the clamd daemon instead of file paths. | clamdscan \--fdpass /home/user |
|  \--stream | Stream file content to the clamd daemon for scanning | clamdscan \--stream /home/user |
| \--reload | Reload the virus database used by clamd. | clamdscan \--reload |
| \--config-file=FILE | Specify a custom configuration file. | clamdscan \--config-file=/etc/clamd.conf |
|  \--disable-precache | Disable file precaching before scanning. | clamdscan \--disable-precache /home/user |
| \--move=DIR | Move infected files to a specified directory.  | clamdscan \--move=/home/user/quarantine /home/user  |
| \--copy=DIR | Copy infected files to a specified directory. | clamdscan \--copy=/home/user/quarantine /home/user |
| \--remove | Remove infected files after scanning. | clamdscan \--remove /home/user |
| \--quiet | Suppress all output except errors. | clamdscan \--quiet /home/user |
|  \--log=FILE | Save scan results to a log file. | clamdscan \--log=/var/log/clamdscan.log /home/user |
|  \--max-filesize=SIZE | Set the maximum file size for scanning. | clamdscan \--max-filesize=10M /home/user |
| \--max-scansize=SIZE | Set the maximum total size of data scanned. | clamdscan \--max-scansize=100M /home/user |
| \-max-recursion=NUMBER | Set the maximum recursion level for scanning. | clamdscan \--max-recursion=10 /home/user |
| \--max-files=NUMBER  | Set the maximum number of files to scan. | clamdscan \--max-files=100 /home/user |

**3\. Advanced Options**

| Flag | Function | Example |
| :---- | :---- | :---- |
| \--no-summary  | Do not display summary information after scanning. | clamdscan \--no-summary /home/user  |
|  \--allmatch | Detect all malware in scanned files (not just the first). | clamdscan \--allmatch /home/user  |
|  \--infected  | Display only infected files in the output.  | clamdscan \--infected /home/user  |

* **Clamdscan is faster than clamscan** 

**Manual commands:**

| Command | Description |
| :---- | :---- |
| man clamscan | Opens the manual for the clamscan tool |
| man freshclam | Opens the manual for updating clamAV databases |
| man clamdscan | Opens the manual for clamdscan tool |

