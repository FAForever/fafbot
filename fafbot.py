#!/usr/bin/python
#-------------------------------------------------------------------------------
# Copyright (c) 2014 Gael Honorez.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Public License v3.0
# which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/gpl.html
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#-------------------------------------------------------------------------------


import sys  # sys.setdefaultencoding is cancelled by site.py

from dispatcher import dispatcher


reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')
from irc import bot as ircbot
import time
from PySide import QtSql

from passwords import DB_SERVER, DB_PORT, DB_LOGIN, DB_PASSWORD, DB_TABLE

from configobj import ConfigObj
config = ConfigObj("/etc/faforever/faforever.conf")
fafbot_config = ConfigObj("fafbot.conf")['fafbot']


class BotModeration(ircbot.SingleServerIRCBot):
    def __init__(self):
        # FIXME: hardcoded ip
        ircbot.SingleServerIRCBot.__init__(
            self,
            [("37.58.123.2", 6667)],
            "fafbot",
            "FAF bot"
        )

        self.nickpass = fafbot_config['nickpass']
        self.nickname = fafbot_config['nickname']

        self.dispatcher = dispatcher(self)

        self.init_database()

    def init_database(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        self.db.setHostName(DB_SERVER)
        self.db.setPort(DB_PORT)

        self.db.setDatabaseName(DB_TABLE)
        self.db.setUserName(DB_LOGIN)
        self.db.setPassword(DB_PASSWORD)
        self.db.open()
        self.db.setConnectOptions("MYSQL_OPT_RECONNECT = 1")

    def on_pubmsg(self, c, e):
        try:
            self.dispatcher(e.arguments[0])
        except:
            pass

    def on_welcome(self, c, e):
        """

        """
        print "got welcomed"
        #self.connection.join("#aeolus")
        try:
            if self.nickpass and c.get_nickname() != self.nickname:
                # Reclaim our desired nickname
                #print "nick on use"
                c.privmsg('nickserv', 'ghost %s %s' % (self.nickname, self.nickpass))
        except:
            pass

    def on_privnotice(self, c, e):
        try:
            source = e.source.nick        
            print source, e.arguments[0]
            if source and source.lower() == 'ze_pilot_':
                if 'SENDALL' in e.arguments[0]:
                    users = self.channels["#aeolus"].users()
                    chunks = lambda l, n: [l[x: x+n] for x in xrange(0, len(l), n)]
                    mesg = e.arguments[0][9:]
                    print mesg 
                    c = chunks(users, 40)
                    for manyPlayer in c:
                        s = ",".join(manyPlayer)
                        raw = "PRIVMSG %s :%s" % (s, mesg)
                        print raw
                        #self.send_raw(raw)
                        #self.connection.privmsg(s, mesg)
                elif 'REGISTER' in e.arguments[0]:
                    self.connection.privmsg('nickserv', 'register %s fafbot@faforever.com' % (self.nickpass))
                elif 'LOGIN' in e.arguments[0]:
                    self.connection.privmsg('nickserv', 'identify %s %s' % (self.nickname, self.nickpass))
            
            elif source and source.lower() == 'nickserv':
                if 'IDENTIFY' in e.arguments[0] :
                    # Received request to identify
                    print "identifying"
                    if self.nickpass and self.nickname == c.get_nickname():
                        self.connection.privmsg('nickserv', 'identify %s %s' % (self.nickname, self.nickpass))
                        
                elif "Password accepted" in e.arguments[0]:
                    print "password accepted, joining"
                    time.sleep(1)
                    self.connection.privmsg('Chanserv', 'INVITE #aeon')
                    self.connection.privmsg('Chanserv', 'INVITE #cybran')
                    self.connection.privmsg('Chanserv', 'INVITE #seraphim')
                    self.connection.privmsg('Chanserv', 'INVITE #uef')
                    time.sleep(5)
                    
                    self.connection.join("#aeon")
                    time.sleep(1)
                    self.connection.join("#cybran")
                    time.sleep(1)
                    self.connection.join("#seraphim")
                    time.sleep(1)
                    self.connection.join("#uef")
                    self.connection.join("#aeolus")

        except:
            pass

    def _on_join(self, c, e):
        try:
            ch = e.target
            nick = e.source.nick
            self.channels[ch].add_user(nick)
        except:
            pass

if __name__ == "__main__":
    BotModeration().start()
