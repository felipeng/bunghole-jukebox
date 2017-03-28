#!/usr/bin/env python
from werkzeug import script

def make_app():
    from jukebox.application import Jukebox
    return Jukebox()

def make_shell():
    from jukebox import models, utils
    application = make_app()
    return locals()

action_runserver = script.make_runserver(make_app, use_reloader=True)
action_shell = script.make_shell(make_shell)

script.run()

