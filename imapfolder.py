import imaplib2
import email


class IMAPFolder(imaplib2.IMAP4_SSL):
    def __init__(self, server, username, password, folder):
        super(IMAPFolder, self).__init__(server)
        self.login(username, password)
        self.select(folder)
        self.new_ids = self.new_messages()

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def new_messages(self):
        type, data = self.search(None, 'UNSEEN')
        if type != 'OK':
            raise StopIteration()
        return data[0].split()

    def next(self):
        while not len(self.new_ids):
            self.idle()
            self.new_ids = self.new_messages()
        type, data = self.fetch(str(self.new_ids.pop()), '(RFC822)')
        return email.message_from_string(data[0][1])

    def __exit__(self, type, value, traceback):
        self.close()
        self.logout()
