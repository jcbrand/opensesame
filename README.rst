Open Sesame
===========

Open Sesame is a commandline based password manager.

It uses GPG to encrypt and decrypt your passwords.

Achtung! This is still a work in progress.

Development
-----------

    git clone git@github.com:jcbrand/opensesame.git

    cd opensesame

    virtualenv .

    ./bin/pip install zc.buildout

    ./bin/buildout

Usage
-----

    ./bin/opensesame -f ~/.pw.txt.gpg --username --password wikipedia.org

TODO
----

* Ability to generate new file
* Ability to add new passwords (auto-generate with pwgen)
