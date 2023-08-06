import os
import logging

from contendo_utils import *
from nfl_insights import *

class NFLGameContext:
    @contendo_classfunction_logger
    def __init__(self, gameInfo, season='2019-regular'):
        self._gameInfo = gameInfo
        self._pbpContext = NFLPbpContextBuilder()
        self._pbpContext.reset(gameInfo, season=season)
        self.nfldata = NFLGetData()
        self.teams = ProUtils.pandas_df_to_dict(self.nfldata.get_teams_df(season).reset_index(), 'teamId')

    @contendo_classfunction_logger
    def add_next_play(self, play: dict) -> dict:
        return self._pbpContext.add_next_play(play)

    @contendo_classfunction_logger
    def get_context(self) -> dict:
        context = dict()
        context['away'] = self.teams[self._pbpContext._playContext.awayTeam]['teamFullname']
        context['home'] = self.teams[self._pbpContext._playContext.homeTeam]['teamFullname']
        context['score'] = self._pbpContext._playContext.score
        context['playType'] = self._pbpContext._playContext.lastPlayType
        context['endDown'] = self._pbpContext._playContext.down
        playkeys = ['quarter', 'currentDown', 'secondsElapsed', 'playDescription', 'playIndex', '', '', '', '', '', '']
        _lastPlay = self._pbpContext.prevPlay.copy()
        for key in playkeys:
            if key in _lastPlay:
                context[key] = _lastPlay[key]
        context['dimensions'] = self._pbpContext.get_play_context_dimentions(_lastPlay)#[True]
        return context


@contendo_function_logger
def test():
    logger.info('Starting...')
    import os
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    gamefile = 'game_playbyplay-2019-regular-51578-20192710-NE-CLE.json'
    pbpDict = ProUtils.get_dict_from_jsonfile('results/nfl/game_playbyplay/'+gamefile)
    gameInfo = pbpDict['game']
    plays = pbpDict['plays']
    gc = NFLGameContext(gameInfo)

    for play in plays:
        gc.add_next_play(play)
        context = gc.get_context()
        print_dict(context)

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.INFO)
    test()
