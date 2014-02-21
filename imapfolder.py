import imaplib2
import email
import logging
from time import sleep


class IMAPFolder(imaplib2.IMAP4_SSL):
    def __init__(self, server, username, password, folder):
        super(IMAPFolder, self).__init__(server)
        self.logger = logging.getLogger('IMAPFolder.' + server + '.' + username + '.' + folder)
        self.logger.debug("Initialisation of IMAP4_SSL complete.")
        self.username = username
        self.password = password
        self.folder = folder
        self.try_starting()

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def new_messages(self):
        type, data = self.search(None, 'UNSEEN')
        if type != 'OK':
            self.logger.error("Received %s from self.search()", type)
            self.logger.error("    data: %s", data)
            raise StopIteration
        return data[0].split()

    def next(self):
        while True:
            try:
                while not len(self.new_ids):
                    self.logger.debug("Waiting for a new message...")
                    self.idle()
                    self.new_ids = self.new_messages()
                    self.logger.debug("Found %s new messages.", len(self.new_ids) or "no")
                type, data = self.fetch(str(self.new_ids.pop()), '(RFC822)')
                self.logger.debug("Retreived message:\n%s", data[0][1])
                break
            except:
                self.logger.exception("Caught exception in next.")
                self.try_closing()
                self.try_starting()
        return email.message_from_string(data[0][1])

    def try_closing(self):
        try:
            self.close()
        except:
            self.logger.exception("Close failed with an exception:")
        try:
            self.logout()
        except:
            self.logger.exception("Logout failed with an exception:")

    def try_starting(self):
        backoff = 30
        while True:
            try:
                self.login(self.username, self.password)
                self.select(self.folder)
                self.new_ids = self.new_messages()
                self.logger.debug("Connected successfully.")
                break
            except:
                self.logger.exception("Couldn't re-connect")
                sleep(backoff)
                backoff = min(backoff * 2, 5 * 60)

    def __exit__(self, type, value, traceback):
        self.logger.error("__exit__ called with the following parameters")
        self.logger.error("type: %s", type)
        self.logger.error("value: %s", value)
        self.logger.error("traceback:\n%s", traceback)
        self.try_closing()
