import logging
import os
import time
from logging.handlers import RotatingFileHandler

class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, max_bytes, backup_count, max_age_days):
        super().__init__(filename, maxBytes=max_bytes, backupCount=backup_count)
        self.max_age_seconds = max_age_days * 24 * 3600  # Convert days to seconds
        self.cleanup_old_logs()

    def cleanup_old_logs(self):
        """Remove logs to keep the total count within the limit."""
        all_log_files = self.get_all_log_files()
        files_to_delete = len(all_log_files) - self.backupCount - 1  # Exclude current log file
        #print("all_log_files", len(all_log_files))
        #print("self.backupCount", self.backupCount)
        #print("files_to_delete", files_to_delete)
        # Delete excess files based on age and count limit
        for i in range(files_to_delete):
            file_path = all_log_files[i]
            file_age = time.time() - os.path.getctime(file_path)
            if file_age > self.max_age_seconds or files_to_delete > 0:
                os.remove(file_path)
                files_to_delete -= 1

    def get_all_log_files(self):
        """Get a list of all log files including backups."""
        dirname, basename = os.path.split(self.baseFilename)
        #print("dirname", dirname)
        #print("basename", basename)
        file_list = [os.path.join(dirname, f) for f in os.listdir(dirname) if not f.startswith(basename)]
        file_list.sort(key=lambda f: os.path.getctime(f))
        #print("file_list", file_list)
        return file_list

    def doRollover(self):
        """Do a rollover, as described in __init__."""
        super().doRollover()
        self.cleanup_old_logs()

        
        
def configure_logger(log_filename, max_bytes, backup_count, max_age_days, formatter=None):
    logger = logging.getLogger(log_filename)
    logger.setLevel(logging.INFO)

    # Create a custom rotating file handler
    handler = CustomRotatingFileHandler(
        filename=log_filename,
        max_bytes=max_bytes,
        backup_count=backup_count,
        max_age_days=max_age_days
    )
    if formatter is None:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
