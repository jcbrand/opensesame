# -*- coding: UTF-8 -*-
import sys
import clipboard
import getpass
import gnupg
import re
import argparse


parser = argparse.ArgumentParser(description='OpenSesame password manager')
parser.add_argument("-f", "--file",
                    dest="file", default='~/.pw.txt.gpg',
                    help=u"Path to the secrets file")
parser.add_argument("-p", "--password", action="store_true", 
                    dest="password", default=False,
                    help=u"Return the password for the given identifier")
parser.add_argument("-a", "--add", action="store_true", 
                    dest="add", default=False,
                    help=u"Add a new password to the store")
parser.add_argument("-l", "--locator", action="store_true", 
                    dest="locator", default=False,
                    help=u"Return the password for the given identifier")
parser.add_argument("-i", "--identifier", action="store_true", 
                    dest="identifier", default=False,
                    help=u"Return the full identifier string for the given identifier")
parser.add_argument("-u", "--username", dest="username", action="store_true", 
                    default=False,
                    help=u"Return the username for the given identifier")
parser.add_argument("-s", "--paste", action="store_true", default=False)
parser.add_argument("descriptor")


class OpenSesame(object):
    """ """

    def __init__(self, options={}, args=()):
        self.options = options
        self.args = args

    def run(self):
        self.match = self.get_match()
        if self.match is None:
            return
        if self.options.identifier:
            identifier = self.get_identifier()
            clipboard.copy(identifier)
            print "The identifier is {}, and has been copied to your " \
                  "clipboard".format(identifier)
            raw_input("Press enter to continue")
        if self.options.locator:
            locator = self.get_locator()
            clipboard.copy(locator)
            print "The locator is {}, and has been copied to your " \
                  "clipboard".format(locator)
            raw_input("Press enter to continue")
        if self.options.username:
            username = self.get_username()
            clipboard.copy(username)
            print "The username is {}, and has been copied to your " \
                  "clipboard".format(username)
            raw_input("Press enter to continue")
        if self.options.password:
            clipboard.copy(self.get_password())
            if self.options.paste:
                print "The password is {} and has been copied to your " \
                      "clipboard".format(self.get_password())
            else:
                print "The password has been copied to your clipboard"
            raw_input("Press enter to clear your clipboard and continue")
            clipboard.copy('')

    def get_match(self):
        gpg = gnupg.GPG()
        pw = getpass.getpass("Please enter your passphrase: ")
        output = gpg.decrypt_file(open(self.options.file, 'rb'), passphrase=pw)
        match = re.findall(
            "(?im).*{}.*".format(self.options.descriptor), output.data,
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

    def get_username(self, match=None):
        if match is not None:
            return match.split('\t')[2]
        else:
            return self.match.split('\t')[2]

    def get_locator(self):
        return self.match.split('\t')[1]

    def get_identifier(self, match=None):
        if match is not None:
            return match.split('\t')[0]
        else:
            return self.match.split('\t')[0]

def main(args=sys.argv[1:]):
    """ Main function called by `opensesame` command.
    """
    options = parser.parse_args(args=args)
    opensesame = OpenSesame(options, args)
    opensesame.run()
