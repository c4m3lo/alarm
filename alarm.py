import argparse
from imapfolder import IMAPFolder


def listen_to_jenkins(server='imap.gmail.com',
                      username=None, password=None,
                      folder='Jenkins',
                      job=None,
                      success=lambda: None,
                      unstable=lambda: None):
    with IMAPFolder('imap.gmail.com', username, password, 'Jenkins') as folder:
        for new_msg in folder:
            if new_msg['X-Jenkins-Job'] == job:
                new_msg['X-Jenkins-Result']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sound alarm if Jenkins breaks.')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    listen_to_jenkins(args.username, args.password)
