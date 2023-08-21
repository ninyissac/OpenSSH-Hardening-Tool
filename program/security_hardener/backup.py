import shutil
import datetime

# Take backup of file with timestamp
def backup(file_name):
    backup_file_name = f"{file_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy(file_name, backup_file_name)

