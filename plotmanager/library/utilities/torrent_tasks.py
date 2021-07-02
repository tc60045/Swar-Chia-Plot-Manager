import os
import time
from transmission_rpc import Client


def _torrent_connect():  #### BROKEN #####
    # get host (localhost), port (9091), username, password from config
    c = Client(host=bittorrent_host, port=bittorrent_port, username=bittorrent_username, password=bittorrent_password)
    return()


def create_dot_torrent(job-or-filename):
    #going to need to popen this / log this...
    #use distinct order_num_piece to create friendly torrent name 
    _torrent_connect()
    get_config_info -- for below... 
    friendly = torrent_path + job.order_something + '.torrent'
    subprocess.Popen(["transmission-create", "-p", "16384", "-o", torrent_path, "--tracker", torrent_tracker1, friendly] )
    # note that this will take 20m or so to finish...
    return()


def add_all_torrents():          # we cannot handle state with these, so we re-add completed instead, every 15 - 30 seconds
    path = get_config_info['torrent_path']
    _torrent_connect()
    for entry in os.scandir(path):
    if entry.path.endswith('.torrent'):
        if len(entry.name) == 48:
            c.add_torrent('file://'+entry)
    return()

def delete_older_torrents():   #### BROKEN #####
    path = get_config_info['torrent_path']
    _torrent_connect()
    expiration_threshold = time.time() - 3 * 24 * 60 * 60
    for entry in os.scandir(path):
        file_time = os.stat(entry.path).st_ctime
        if file_time < expiration_threshold:
            # get the name of the .plot so we can kill it...
            c.stop_torrent(entry)
            c.remove_torrent(entry)
            # exeucte an rm to remove the .torrent file
            # execute an rm to kill the .plot file
    return()


