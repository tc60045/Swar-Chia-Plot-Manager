import os
import logging

def assign_mount(actual_disk_path, job_path_alias):
    logging.info(f'Assigning {job_path_alias to} to {actual_disk_path}')
    os.symlink(actual_disk_path, job_path_alias)
    return()