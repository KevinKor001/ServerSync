import os
from ftplib import FTP
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
import lib.paramiko as paramiko
import logging
from pathlib import Path



logging.basicConfig(
    filename="sftp_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SFTPSync:
    def __init__(self, host, user, password, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.client = None
        self.sftp = None

    def log(self, message):
        """Helper to log to file and console if needed"""
        logging.info(message)

    def connect(self):
        try:
            self.log(f"Initiating SSH connection to {self.host}:{self.port}")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.log(f"Attempting login for user: {self.user}")
            self.client.connect(
                self.host, 
                port=self.port, 
                username=self.user, 
                password=self.password,
                timeout=15,
                allow_agent=False, # Prevents interference from local SSH agents
                look_for_keys=False
            )
            
            self.log("SSH connection established. Opening SFTP session...")
            self.sftp = self.client.open_sftp()
            self.log("SFTP session opened successfully.")
            return True
        except paramiko.AuthenticationException:
            self.log("Authentication failed: Check username or password.")
            return "Auth failed: Invalid credentials."
        except paramiko.SSHException as e:
            self.log(f"SSH protocol error: {e}")
            return f"SSH Error: {e}"
        except Exception as e:
            self.log(f"Unexpected connection error: {e}")
            return f"Error: {e}"

    def upload_with_progress(self, local_path, remote_dir):
        if not os.path.exists(local_path):
            self.log(f"Local error: File {local_path} not found.")
            return "Local file not found."

        file_size = os.path.getsize(local_path)
        filename = os.path.basename(local_path)
        # Ensure remote path uses forward slashes for Linux servers
        remote_path = (Path(remote_dir) / filename).as_posix()

        self.log(f"Starting upload: {local_path} -> {remote_path} ({file_size} bytes)")

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
            ) as progress:
                
                task = progress.add_task(f"Uploading...", total=file_size)

                def callback(transferred, total):
                    progress.update(task, completed=transferred)
                    # Log every 25% to avoid bloating the log file
                    if transferred % (total // 4 + 1) < 8192: 
                        logging.debug(f"Progress: {transferred}/{total} bytes")

                self.sftp.put(local_path, remote_path, callback=callback)
            
            self.log(f"Upload completed successfully: {filename}")
            return True
        except PermissionError:
            self.log(f"Permission denied on server: Cannot write to {remote_dir}")
            return "Server Error: Permission denied."
        except Exception as e:
            self.log(f"Upload failed mid-transfer: {e}")
            return f"Upload error: {e}"
    def upload_directory(self, local_dir, remote_root):
        """Recursively uploads a directory, ensuring empty folders are created."""
        self.log(f"Scanning directory: {local_dir}")
        
        for root, dirs, files in os.walk(local_dir):
            rel_path = os.path.relpath(root, local_dir)
            
            # Build the remote path
            if rel_path == ".":
                # This is the root folder itself (e.g., 'core')
                remote_dir = (Path(remote_root) / Path(local_dir).name).as_posix()
            else:
                # These are subfolders (e.g., 'core/utils')
                remote_dir = (Path(remote_root) / Path(local_dir).name / rel_path).as_posix()

            # --- THE FIX: Create folder even if 'files' is empty ---
            try:
                self.sftp.mkdir(remote_dir)
                self.log(f"Created remote folder: {remote_dir}")
                print(f"Created: {remote_dir}") # Feedback for the user
            except IOError:
                # Folder likely exists
                self.log(f"Folder already exists: {remote_dir}")

            # Now upload files if there are any
            for filename in files:
                local_file = os.path.join(root, filename)
                self.upload_with_progress(local_file, remote_dir)


    def disconnect(self):
        self.log("Closing SFTP and SSH connections.")
        if self.sftp: self.sftp.close()
        if self.client: self.client.close()



class FTPSync:
    def __init__(self, host, user, password, port=21):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.ftp = FTP()

    def connect(self):
        try:
            self.ftp.connect(self.host, self.port, timeout=10)
            self.ftp.login(self.user, self.password)
            self.ftp.set_pasv(True)  # Passive mode is safer for most firewalls
            return True
        except Exception as e:
            return f"Connection error: {e}"

    def upload_with_progress(self, local_path, remote_dir):
        if not os.path.exists(local_path):
            return "Local file not found."

        file_size = os.path.getsize(local_path)
        filename = os.path.basename(local_path)

        try:
            self.ftp.cwd(remote_dir)

            # Define the Rich Progress Bar layout
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
            ) as progress:
                
                task = progress.add_task(f"Uploading {filename}...", total=file_size)

                with open(local_path, "rb") as f:
                    # Callback function called every time a chunk is sent
                    def callback(chunk):
                        progress.update(task, advance=len(chunk))

                    # 8KB is a standard buffer size for FTP
                    self.ftp.storbinary(f"STOR {filename}", f, blocksize=8192, callback=callback)

            return True
        except Exception as e:
            return f"Upload failed: {e}"

    def disconnect(self):
        try:
            self.ftp.quit()
        except:
            self.ftp.close()
