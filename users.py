# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import Popen, PIPE
from pelican import signals
from pelican.utils import pelican_open
import logging
import os

logger = logging.getLogger(__name__)

class Users():
    def __init__(self, generator):
        self.get_online = generator.settings['USERS_ONLINE']

    def fetch_online(self):
        users = Popen("users", shell=True, stdout=PIPE).stdout.read() 
        return sorted(set(users.split()))

    def fetch_all(self):
        users = [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d))]
        return sorted(users)

def fetch_online_users(gen, metadata):
    if gen.settings['USERS_ONLINE']:
        gen.context['online_users'] = gen.plugin_instance.fetch_online()

def fetch_all_users(gen, metadata):
    gen.context['all_users'] = gen.plugin_instance.fetch_all()

def initialization(generator):
    generator.plugin_instance = Users(generator)

def register():
    try:
        signals.article_generator_init.connect(initialization)
        signals.article_generator_context.connect(fetch_online_users)
        signals.article_generator_context.connect(fetch_all_users)
    except:
        logger.warning('something is broken')
