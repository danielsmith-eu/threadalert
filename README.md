# Thread Monitor

Monitors a vBulletin forum and sends a desktop notification when a new thread is added.

## Setup, config and usage

I recommend using a virtualenv to handle the requirements, e.g.

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

Then copy `config.json.osx` or `config.json.pushbullet` to `config.json` depending on which notification style you want.

* OSX style is Desktop notification for the local machine's desktop.
* Pushbullet is a multi-device cloud notification system, useful if you want to run this monitor on your own server and notify your phone/desktop etc.

Then edit `config.json` to put in your watched thread URLs (there are examples from flyertalk.com already present).

If you are using pushbullet, you need to copy your API token from [the pushbullet settings page](https://www.pushbullet.com/#settings/account) into the `pushbullet_access_token` value.

Then run the monitor, e.g.:

    python monitor.py

If you want to run from another config file, you can supply it on the command line:

    python monitor.py config2.json



