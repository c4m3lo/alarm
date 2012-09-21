import imaplib2
import argparse
import time


class IMAPFolder(imaplib2.IMAP4_SSL):
    def __init__(self, server, username, password, folder):
        super(IMAPFolder, self).__init__(server)
        self.login(username, password)
        self.select(folder)
        self.new_ids = []

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def next(self):
        while not len(self.new_ids):
            time.sleep(10)
            print 'checking'
            type, data = self.search(None, 'UNSEEN')
            if type != 'OK':
                raise StopIteration()
            self.new_ids = data[0].split()
        return self.new_ids.pop()

    def __exit__(self, type, value, traceback):
        self.close()
        self.logout()


def main(username, password):
    with IMAPFolder('imap.gmail.com', username, password, 'Jenkins') as folder:
        for new_msg in folder:
            print new_msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sound alarm if Jenkins breaks.')
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    main(args.username, args.password)
