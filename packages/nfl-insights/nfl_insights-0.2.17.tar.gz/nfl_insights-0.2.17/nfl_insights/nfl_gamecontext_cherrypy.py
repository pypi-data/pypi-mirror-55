import os, os.path
import random
import string
from pathlib import Path

import cherrypy

from contendo_utils import *
from nfl_insights import NFLGameContext

class NFLGameContextDemo(object):
    def __init__(self, gamesDir='./'):
        self._localdir = str(Path(__file__).parent) + '/'
        self._conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': self._localdir
            },
            '/generator': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': self._localdir
            }
        }
        self.generator = GameContextWebService(gamesDir=gamesDir)

    def start(self):
        cherrypy.quickstart(self, '/', self._conf)

    @cherrypy.expose
    def index(self):
        return open(self._localdir+'index.html')


@cherrypy.expose
class GameContextWebService(object):

    def __init__(self, gamesDir):
        self._gamesDir = gamesDir

    def _reset(self, gamefile):
        _pbpDict = ProUtils.get_dict_from_jsonfile('{}/{}'.format(self._gamesDir, gamefile))
        _gameInfo = _pbpDict['game']
        _playCursor = 0
        _context = NFLGameContext(_gameInfo)
        cherrypy.session['context'] = _context
        cherrypy.session['gamefile'] = gamefile
        cherrypy.session['pbpDict'] = _pbpDict
        cherrypy.session['playCursor'] = _playCursor

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, gamefile):
        gamefile=str(Path(gamefile))[12:]
        print('Next ...', gamefile)
        _context = cherrypy.session.get('context', None)
        _gamefile = cherrypy.session.get('gamefile', None)
        if _context is None or gamefile != _gamefile:
            self._reset(gamefile)
            _context = cherrypy.session['context']
        else:
            _gamefile = cherrypy.session['gamefile']

        _plays = cherrypy.session['pbpDict']['plays']
        _playCursor = cherrypy.session['playCursor']

        _context.add_next_play(_plays[_playCursor])
        _playCursor += 1
        cherrypy.session['playCursor'] = _playCursor
        ret = dict_to_html(_context.get_context())
        #print(ret)
        return ret

    def POST(self, gamefile, quarter, seconds):
        gamefile = str(Path(gamefile))[12:]
        quarter = int(quarter)
        seconds = int(seconds)
        print('Jump to ...', gamefile, quarter, seconds)
        self._reset(gamefile)
        _context = cherrypy.session['context']
        _gamefile = cherrypy.session['gamefile']
        _plays = cherrypy.session['pbpDict']['plays']

        _playCursor = 0
        for play in _plays:
            _context.add_next_play(play)
            _playCursor += 1
            context = _context.get_context()
            #print('----------------------------\n', context, '\n----------------------------\n')
            if context['quarter'] == quarter and context['secondsElapsed'] >= seconds:
                break
        # set the play cursor and return the context
        cherrypy.session['playCursor'] = _playCursor
        ret = dict_to_html(_context.get_context())
        #print(ret)
        return ret

    def DELETE(self):
        print('Deleting...')
        cherrypy.session.pop('context', None)
        cherrypy.session.pop('gamefile', None)
        cherrypy.session.pop('pbpDict', None)
        cherrypy.session.pop('playCursor', None)

if __name__ == '__main__':
    _localdir = str(Path(__file__).parent)+'/'
    print(_localdir)
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': _localdir
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': _localdir
        }
    }
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    webapp = NFLGameContextDemo(gamesDir='results/nfl/game_playbyplay/')
    webapp.start()
