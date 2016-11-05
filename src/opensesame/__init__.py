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
    """
    parser.add_option("-a", "--add", action="store_true", 
                      dest="add", default=False,
                      help=u"Add a new password to the store")
    """
    parser.add_option("-l", "--locator", action="store_true", 
                      dest="locator", default=False,
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
        if self.match is None:
            return
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
        if self.options.locator:
            locator = self.get_locator()
            clipboard.copy(identifier)
            print "The locator is {}, and has been copied to your " \
                  "clipboard".format(locator)
            raw_input("Press enter to continue")

    def get_match(self):
        gpg = gnupg.GPG()
        pw = getpass.getpass("Please enter your passphrase: ")
        output = gpg.decrypt_file(open(self.options.file, 'rb'), passphrase=pw)
        match = re.findall(
            "(?im).*{}.*".format(self.args[0]), output.data,
        )
        if len(match) > 1:
            print "Got more than one hit, please refine your identifier.\n"
            print "Here are the hits: "
            for m in match:
                print "Identifier: {}, Username: {}".format(
                    self.get_identifier(m),
                    self.get_username(m)
                );
            return None
        elif len(match) == 0:
            print output.status
            print "No match found"
            return None
        return match[0]

    def get_password(self):
        return self.match.split('\t')[3]

    def get_username(self):
        return self.match.split('\t')[2]

    def get_locator(self):
        return self.match.split('\t')[1]

    def get_identifier(self, match=None):
        if match is not None:
            return match.split('\t')[0]
        else:
            return self.match.split('\t')[0]

def main():
    options, args = parse_options()
    opensesame = OpenSesame(options, args)
    opensesame.run()
