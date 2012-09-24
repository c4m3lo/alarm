import argparse
from imapfolder import IMAPFolder
from datetime import datetime


def success(msg):
    print "%s: Build succeeded" % datetime.now()


def unstable(msg):
    print "%s: Build unstable" % datetime.now()


def listen_to_jenkins(server='imap.gmail.com',
                      username=None, password=None,
                      folder='Jenkins',
                      job=None,
                      success=lambda: None,
                      unstable=lambda: None):
    with IMAPFolder('imap.gmail.com', username, password, 'Jenkins') as folder:
        for new_msg in folder:
            if new_msg['X-Jenkins-Job'] == job:
                if new_msg['X-Jenkins-Result'] == 'SUCCESS':
                    success(new_msg)
                elif new_msg['X-Jenkins-Result'] == 'UNSTABLE':
                    unstable(new_msg)
                else:
                    print 'Found matching Jenkins job, with unknown result: {}'.format(new_msg['X-Jenkins-Result'])
            elif new_msg['X-Jenkins-Job']:
                print 'Received message for {} - ignoring.'.format(new_msg['X-Jenkins-Job'])
            else:
                print "Message received without Jenkins headers - ignoring."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sound alarm if Jenkins breaks.')
    parser.add_argument('job')
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('-s', '--server', default='imap.gmail.com')
    parser.add_argument('-f', '--folder', default='Jenkins')
    args = parser.parse_args()
    listen_to_jenkins(server=args.server,
                      username=args.username,
                      password=args.password,
                      folder=args.folder,
                      job=args.job,
                      success=success,
                      unstable=unstable)
