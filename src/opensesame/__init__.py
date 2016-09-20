# -*- coding: UTF-8 -*-
from optparse import OptionParser
import clipboard
import getpass
import gnupg
import re


def parse_options():
    usage = "\n%prog [options] IDENTIFIER"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file",
                      dest="file", default='.pw.txt.gpg',
                      help=u"Path to the secrets file")
    parser.add_option("-p", "--password", action="store_true", 
                      dest="password", default=False,
                      help=u"Return the password for the given identifier")
    parser.add_option("-a", "--address", action="store_true", 
                      dest="address", default=False,
                      help=u"Return the password for the given identifier")
    parser.add_option("-i", "--identifier", action="store_true", 
                      dest="identifier", default=False,
                      help=u"Return the full identifier string for the given identifier")
    parser.add_option("-u", "--username", dest="username", action="store_true", 
                      default=False,
                      help=u"Return the username for the given identifier")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error(u"You need to specify exactly one credentials identifier")
    return (options, args)


class OpenSesame(object):
    """ """

    def __init__(self, options={}, args=()):
        self.options = options
        self.args = args

    def run(self):
        self.match = self.get_match()
        if self.options.username:
            username = self.get_username()
            clipboard.copy(username)
            print "The username is {}, and has been copied to your " \
                  "clipboard".format(username)
            raw_input("Press enter to continue")
        if self.options.password:
            clipboard.copy(self.get_password())
            print "The password has been copied to your clipboard"
            raw_input("Press enter to clear your clipboard and continue")
            clipboard.copy('')
        if self.options.identifier:
            identifier = self.get_identifier()
            clipboard.copy(identifier)
            print "The identifier is {}, and has been copied to your " \
                  "clipboard".format(identifier)
            raw_input("Press enter to continue")
        if self.options.address:
            address = self.get_address()
            clipboard.copy(identifier)
            print "The address is {}, and has been copied to your " \
                  "clipboard".format(address)
            raw_input("Press enter to continue")

    def get_match(self):
        gpg = gnupg.GPG()
        pw = getpass.getpass("Please enter your passphrase: ")
        output = gpg.decrypt_file(open(self.options.file, 'rb'), passphrase=pw)
        match = re.findall(
            ".*{}.*".format(self.args[0]), output.data, re.MULTILINE
        )
        if len(match) > 1:
            return "Got more than one hit, please refine your identifier"
        elif len(match) == 0:
            return "No match found"
        return match[0]

    def get_password(self):
        return self.match.split(',')[3]

    def get_username(self):
        return self.match.split(',')[2]

    def get_address(self):
        return self.match.split(',')[1]

    def get_identifier(self):
        return self.match.split(',')[1]

def main():
    options, args = parse_options()
    opensesame = OpenSesame(options, args)
    opensesame.run()
