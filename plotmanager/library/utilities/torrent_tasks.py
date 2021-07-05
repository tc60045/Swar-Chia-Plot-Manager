import os
import time
import logging
from transmission_rpc import Client

from plotmanager.library.utilities.xchiax_orders import send_torrent_home


def create_dot_torrent(filename, order_number, xchiax_settings):
    logging.info(f'Creating a torrent for {order_number}...')
    c = Client(host=bittorrent_host, port=bittorrent_port, username=bittorrent_username, password=bittorrent_password)
    path = xchiax_settings['torrent_path']
    friendly_torrent_name = path + '/' +  order_number + '.torrent'
    link_file = path + '/' + 'link_file.txt'
    wg = open(linkfile,'a')
    out_line = friendly_torrent_name + '|' + order_number + '|' + filename
    wg.write(f'{out_line}\n')
    wg.close()
    tcreate = subprocess.Popen(["transmission-create", "-p", "16384", "-o", friendly_torrent_name, \
       "--tracker", torrent_tracker1, filename])
    # note that this will take 20m or so to finish...
    # probably need to tell redis that it is available...
    return(friendly_torrent_name)


def add_all_torrents(xchiax_settings):          # we cannot handle state with these, so we re-add completed instead, every 15 - 30 seconds
    logging.info(f'Adding torrents..')
    path = xchiax_settings['torrent_path']
    target_time = time.time() - 30
    c = Client(host=bittorrent_host, port=bittorrent_port, username=bittorrent_username, password=bittorrent_password)
    for entry in os.scandir(path):
        if entry.path.endswith('.torrent'):   # entry.path = fq fname
            if len(entry.name) == 48:
                if os.path.getmtime(entry) < target_time:
                    tor_id = c.add_torrent('file://' + path + entry.name)
                    c.start_torrent(tor_id)
    return()

def find_send_new_torrents(xchiax_settings):
    logging.info(f'Find and send new torrents..')
    path = xchiax_settings['torrent_path']
    torrents_sent = path + '/' + 'torrents_sent.txt'
    f = open(torrents_sent,'r')
    data = f.read()
    f.close()
    target_time = time.time() - 30
    for entry in os.scandir(path):
        if entry.path.endswith('.torrent'):
            if len(entry.name) == 48:
                if os.path.getmtime(entry) < target_time:
                    if entry.name not in data:
                        payload = open(entry.path,'rb').read()
                        send_torrent_home(payload)
                        f = open(torrents_sent,'a')
                        f.write(f'{entry.name}\n')
                        f.close()
    return()    


def delete_older_torrents(xchiax_settings):   #### BROKEN #####
    logging.info(f'Checking for old torrents to delete')
    path = xchiax_settings['torrent_path']
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

def do_torrent_check(xchiax_settings):
    add_all_torrents(xchiax_settings)
    find_send_new_torrents(xchiax_settings)
    #delete_older_torrents(xchiax_settings)   # needs work
    return()
