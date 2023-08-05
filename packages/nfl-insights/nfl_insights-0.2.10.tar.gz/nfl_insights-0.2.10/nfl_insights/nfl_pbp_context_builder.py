from datetime import datetime as dt
import json
import os
import pandas as pd
import logging
from typing import Optional

from setuptools.command.test import test

from contendo_utils import *
from nfl_insights import *

class NFLPbpContextBuilder:
    @contendo_classfunction_logger
    def __init__(self) -> None:
        self.ccm = ContendoConfigurationManager()
        self.dimentionsDict = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 71679784, 'ConditionCode')
        self.playPropMap = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 138336971, 'PropertyName')
        self.descriptionConfig = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 1063246855, 'Text')

    @contendo_classfunction_logger
    def reset(self, pbpDict: dict, season: str):
        self.playsList = list()
        self.playCounter = 0
        self.playIndex = 0
        self.gameInfo = pbpDict['game']
        self.gc = NFLGameContext(self.gameInfo['awayTeam']['id'], self.gameInfo['homeTeam']['id'], year = season.split('-')[0])
        self.prevPlay = None
        self.inconsistentCount=0
        self.nofumbleInconsistentCount=0
        self.contextError = False
        self.homeDrive=0
        self.awayDrive=0
        self.teamDrive=0
        self.gameDrive=0

    @contendo_classfunction_logger
    def add_play(self, play):
        self._create_play(play)

    @contendo_classfunction_logger
    def _create_play(self, play, parent=None):
        try:
            _newplay = dict()
            #
            # Extracting relevant contextual info from game-context (if top play)
            _newplay['awayScore'] = self.gc.score[0]
            _newplay['homeScore'] = self.gc.score[1]
            #
            # processing play keys
            for key, value in play.items():
                if key == 'description':
                    _newplay['playDescription'] = value
                elif key == 'playStatus':
                    self._digest_playstatus(_newplay, value)
                elif key in ['pass', 'rush', 'sack', 'kick', 'penalty', 'punt', 'fumble', 'fieldGoalAttempt',
                             'extraPointAttempt', 'lateralPass']:
                    _newplay['playType'] = key
                    self._digest_play_properties(_newplay, playType=key, playProperties=value)
                    if key == 'penalty' and not parent:
                        properties = value.get('penalty')
                        self._digest_play_properties(_newplay, playType='penalty', playProperties=properties)
                    # set team_id to team in possession
                else:
                    _newplay[key] = value

            if not 'playType' in _newplay:
                logger.error('Error play: \n%s\n_newplay:\n%d.%s\n', play, self.playCounter+1, _newplay)
                return None

            #
            # Processing post-play info (if top play)
            if not parent: # main play
                self._digest_description(_newplay)
                try:
                    consistent = self.gc.play(playjson=play)
                except Exception as e:
                    logger.exception('Error GC-processing play:\n%s\n', play)
                    self.contextError = True
                    self.playCounter += 1
                    _newplay['index'] = self.playCounter
                    return _newplay

                if not consistent and self.prevPlay:
                    try:
                        errors = '\n\t Inconsistent:'
                        if self.prevPlay["lineOfScrimmage"]:
                            if self.prevPlay["lineOfScrimmage_team_id"]!=self.gc.ballTerritory and self.gc.ballPosition != 50 and self.gc.ballTerritory != -1:
                                errors += 'lineOfScrimmage team territory, '
                            if int(self.prevPlay["lineOfScrimmage_yardLine"]) != self.gc.ballPosition:
                                errors += 'lineOfScrimmage yardLine, '
                            if int(self.prevPlay["currentDown"]) != self.gc.down:
                                errors += 'currentDown, '
                            if int(self.prevPlay["yardsRemaining"]) != self.gc.yardsRemaining:
                                errors += 'yardsRemaining, '
                        if int(self.prevPlay["teamInPossession_id"]) != self.gc.offense:
                            errors += 'teamInPossession, '
                        logger.debug('Inconsistent playstatus: %d. %s, Errors:%s', self.playCounter, self.prevPlay['playDescription'], errors)
                        self.inconsistentCount += 1
                        _newplay['inconsistent'] = True
                    except Exception as e:
                        logger.Error('Error processing prev-play: %s\n', self.prevPlay)

                # Handle conversion
                if self.gc.conversion:
                    _newplay['isConversion'] = True
                else:
                    _newplay['isConversion'] = False

                # handle Drives
                if self.gc.drive>0 and self.gc.drive > self.gameDrive:
                    self.gameDrive = self.gc.drive
                    if _newplay['teamInPossession_id']==self.gc.homeTeam:
                        self.homeDrive += 1
                        self.teamDrive = self.homeDrive
                    else:
                        self.awayDrive += 1
                        self.teamDrive = self.awayDrive
            else: # not top - subplay
                self._digest_playstatus(_newplay, parent['playStatus'])

            # handle score-diff
            _newplay['scoringPlay'] = self.gc.scoringPlay
            _newplay['scoreDiff'] = abs(_newplay['homeScore'] - _newplay['awayScore'])
            if _newplay['teamInPossession_id'] == self.gc.homeTeam:
                _newplay['teamScoreDiff'] = _newplay['homeScore'] - _newplay['awayScore']
            else:
                _newplay['teamScoreDiff'] = _newplay['awayScore'] - _newplay['homeScore']

            # play (and subplays) been canceled.
            _newplay['isCanceled'] = self.gc.isCanceled
            if _newplay['playType'] == 'punt':
                _newplay['netYardsPunt'] = _newplay.get('yardsKicked',0) - _newplay.get('yardsReturned',0)

            # offense/defense team setting
            _newplay['team_id'] = _newplay['teamInPossession_id']
            _newplay['offenseTeam_id'] = _newplay['teamInPossession_id']
            _newplay['defenseTeam_id'] = self.gc.awayTeam if _newplay['team_id']==self.gc.homeTeam else self.gc.homeTeam
            # set drive
            _newplay['gameDrive'] = self.gc.drive
            if self.gameDrive > 0:
                _newplay['teamDrive'] = self.teamDrive
                _newplay['uniqueTeamDrive'] = '{}-{}-{}'.format(self.gameInfo['id'], _newplay['team_id'], self.teamDrive)
            else:
                _newplay['teamDrive'] = 0
            #logger.info('PlayType=%s, Playindex=%d, Drive=%d, gamedrive=%d, teamdrive=%d', self.playIndex, self.gc.drive, self.gc._drivenum, self.gameDrive, self.teamDrive)

            self.playCounter += 1
            if not parent:
                self.playIndex += 1
            else:
                self.subplayIndex+=1
                _newplay['subplayIndex'] = self.subplayIndex
            _newplay['index'] = self.playCounter
            _newplay['playIndex'] = self.playIndex
            _newplay['uniquePlayIndex'] = '{}-{}-{}'.format(self.gameInfo['id'], _newplay['team_id'], self.playIndex)
            #_newplay['context'] = self.get_play_context_dimentions(_newplay)

            self.playsList.append(_newplay)
        except Exception as e:
            logger.error('Error processing play:\n%s\nNewplay: %s\n', play, _newplay)
            raise e

        return _newplay

    @contendo_classfunction_logger
    def _digest_player(self, newplay, propname, player):
        if not player:
            return
        #newplay[propname+'_jerseyNumber'] = player['jerseyNumber']
        newplay[propname+'_position'] = player['position']
        #newplay[propname+'_lastName'] = player['lastName']
        #newplay[propname+'_firstName'] = player['firstName']
        newplay[propname+'_id'] = int(player['id'])

    @contendo_classfunction_logger
    def _digest_position(self, newplay, propname, position):
        if not position:
            return
        newplay[propname+'_point'] = position['point']
        newplay[propname+'_yardLine'] = int(position['yardLine'] if position['yardLine'] else -1)
        self._digest_team(newplay, propname+'_team', position['team'])

    @contendo_classfunction_logger
    def _digest_team(self, newplay, propname, team):
        if not team:
            return
        newplay[propname+'_id'] = int(team['id'])
        newplay[propname+'_abbreviation'] = team['abbreviation']

    @contendo_classfunction_logger
    def _digest_simple(self, newplay, propname, value):
        newplay[propname] = value

    @contendo_classfunction_logger
    def _digest_zout(self, newplay, propname, value):
        pass

    @contendo_classfunction_logger
    def _digest_lineofscrimmage(self, newplay, propname, lineofscrimmage):
        if not lineofscrimmage:
            newplay['lineOfScrimmage'] = False
            return
        else:
            newplay['lineOfScrimmage'] = True

        newplay[propname+'_yardLine'] = lineofscrimmage['yardLine']
        self._digest_team(newplay, propname+'_team', lineofscrimmage['team'])

    @contendo_classfunction_logger
    def _digest_description(self, play):
        if not 'playDescription' in play:
            return
        description = play['playDescription']
        playType = play['playType']

        for text, configDict in self.descriptionConfig.items():
            if configDict['playType'] == '' or configDict['playType'].find(playType) >-1:
                if description.find(text) > -1:
                    for i in range(1,3):
                        key = 'Key{}'.format(i)
                        if configDict[key] != '':
                            play[configDict[key]] = configDict['Value{}'.format(i)]

    @contendo_classfunction_logger
    def _digest_play_properties(self, newplay, playType, playProperties):
        for propname,value in playProperties.items():
            propDef = self.playPropMap[propname]
            # assert property is expected for this playtype
            assert propDef[playType] == 1, 'Illegal property "{}" for playType "{}"'.format(propname, newplay['playType'])

            objType = propDef['ObjType']
            _digestFunc = self.__getattribute__('_digest_{objType}'.format(objType=str.lower(objType)))
            _digestFunc(newplay, propname, value)

    @contendo_classfunction_logger
    def _digest_playstatus(self, newplay: dict, playStatus: [dict,list]) -> None:
        if type(playStatus)==list:
            playStatus=playStatus[0]

        if type(playStatus) == dict:
            self._digest_play_properties(newplay, playType='playStatus', playProperties=playStatus)
        else:
            logger.error('Playstatus is not a dict, type: {}, {}'.format(type(playStatus), playStatus))

    @contendo_classfunction_logger
    def digest_pbp(self, pbpDict: dict, season) -> dict:
        self.reset(pbpDict, season)
        #
        # process all newplays
        for play in pbpDict['plays']:
            _newplay = self._create_play(play)
            # TODO: Handle penalties and subplays

            # finally set the previous play
            self.prevPlay = _newplay

            # handle subplays if exists
            _newplay['nFumbles'] = 0
            self.subplayIndex = 0
            subplays = play[_newplay['playType']].get('subPlays', list())
            if subplays:
                for subPlay in subplays:
                    found=False
                    for sybplayName in ['fumble', 'lateralPass', 'pass', 'rush']:
                        if sybplayName in subPlay:
                            found=True
                            if type(subPlay[sybplayName]) == dict:
                                subplays2 = [subPlay[sybplayName]]
                            elif type(subPlay[sybplayName]) == list:
                                subplays2 = subPlay[sybplayName]
                            else:
                                logger.error('Error: illegal Subplay: %s', subPlay)
                            for subplay2 in subplays2:
                                self._create_subplay(_newplay, {sybplayName: subplay2}, parent=play)
                    if not found:
                        logger.error('Error: Unknown Subplay: %s', subPlay)

            # handle penalties.
            penalties = play[_newplay['playType']].get('penalties', list())
            if penalties:
                for penalty in penalties:
                    if type(penalty['penalty'])==dict:
                        penalties2 = [penalty['penalty']]
                    else:
                        penalties2 = penalty['penalty']

                    for penalty2 in penalties2:
                        self._create_subplay(_newplay, {'penalty': penalty2}, parent=play)

            if 'inconsistent' in _newplay and _newplay['nFumbles'] == 0:
                self.nofumbleInconsistentCount+=1

        return {'plays': self.playsList}

    @contendo_classfunction_logger
    def _create_subplay(self, newplay, subplay, parent):
        _newsubplay = self._create_play(subplay, parent=parent)
        _newsubplay['parentIndex'] = newplay['index']
        _newsubplay['parentPlayType'] = newplay['playType']
        _newsubplay['isSubplay'] = True
        if _newsubplay['playType'] == 'fumble':
            newplay['nFumbles'] += 1

    @contendo_classfunction_logger
    def get_play_context_dimentions(self, play: dict) -> dict:
        contextDims = dict()
        df = DictToObject(play)
        #
        # loop over all dimentions to check if the play is one of them
        for dim, dimDef in self.dimentionsDict.items():
            dimentionQuery = dimDef['Condition']
            if dimDef['playType'] != 'all':
                dimentionQuery = '({}) & (df.playType=="{}")'.format(dimentionQuery, dimDef['playType'])
            try:
                res = eval(dimentionQuery)
            except:
                res = 'N/A'

            contextDims[res] = contextDims.get(res, list())
            contextDims[res].append(dim)

        return contextDims

    @contendo_classfunction_logger
    def _pbp_play_properties(self, playProperties):
        def _validate_player_record(player):
            if type(player) == dict:
                if not player['position']:
                    player['position']=''
                if player['position']=='T':
                    player['position']='TE'
                return player
            else:
                return None

        def _validate_team_record(team):
            if type(team) == dict:
                if not isinstance(team.get('abbreviation', None), str):
                    return None
                return team
            else:
                return None

        def _validate_position_record(position):
            if type(position) == dict:
                if not _validate_team_record(position['team']):
                    return None
                return position
            else:
                return None

        newPlayProperties = dict()
        playerFieldNames = ['assistedTacklingPlayer1', 'assistedTacklingPlayer2', 'centerPlayer', 'forcedByPlayer', 'fumblingPlayer', 'holdingPlayer', 'interceptingPlayer', 'kickingPlayer', 'passingPlayer', 'penalizedPlayer', 'receivingPlayer', 'recoveringPlayer', 'retrievingPlayer', 'rushingPlayer', 'soloTacklingPlayer']
        teamFieldNames = ['fumblingTeam', 'recoveringTeam']
        positionFieldNames = ['receivedAtPosition', 'sackedAtPosition', 'kickedFromPosition', 'stoppedAtPosition', 'retrievedAtPosition', 'enforcedAtPosition', 'rushedFromPosition', 'interceptedAtPosition', 'fumbledAtPosition', 'blockedAtPosition']
        arrayProps = ['subPlays', 'penalties']
        dropProps = ['awayPlayersOnField', 'homePlayersOnField']

        for propname,value in playProperties.items():
            if propname in positionFieldNames:
                newValue = _validate_position_record(value)
            elif propname in playerFieldNames:
                newValue = _validate_player_record(value)
            elif propname in teamFieldNames:
                newValue = _validate_team_record(value)
            elif propname in dropProps:
                continue
            elif propname in arrayProps:
                if type(value) == list:
                    newValue = value
            else:
                newValue = value

            if newValue is None or newValue=='':
                if newValue == '':
                    logger.debug('Dropping value %s=%s', propname, value)
                continue

            newPlayProperties[propname] = newValue

        return newPlayProperties

    @contendo_classfunction_logger
    def _pbp_playstatus(self, playStatus):
        newPlayStatus = dict()

        if type(playStatus)==list:
            playStatus=playStatus[0]

        if type(playStatus) == dict:
            ignoreKeys = ['homePlayersOnField', 'awayPlayersOnField']
            for key,value in playStatus.items():
                if key in ignoreKeys:
                    continue
                newPlayStatus[key] = value
        else:
            logger.error('Playstatus is not a dict, type: {}, {}'.format(type(playStatus), playStatus))

        #logger.debug('new Playstatus: {}, orig playstatus: {}'.format(newPlayStatus, playStatus))
        return newPlayStatus

    @contendo_classfunction_logger
    def _pbp_parse_description(self, play):
        if not 'description' in play:
            return
        descriptionConfig = self.ccm.get_configuration_dict(NFL_DOMAIN_NAME, 1063246855, 'Text')
        description = play['description']
        playType = play['name']
        properties = play['properties']

        for text, configDict in descriptionConfig.items():
            if configDict['playType'] == '' or configDict['playType'].find(playType) >-1:
                if description.find(text) > -1:
                    for i in range(1,3):
                        key = 'Key{}'.format(i)
                        if configDict[key] != '':
                            properties[configDict[key]] = configDict['Value{}'.format(i)]


    @contendo_classfunction_logger
    def _create_newplay(self, play, top=False):
        try:
            newPlay = dict()
            for key, value in play.items():
                if key == 'description':
                    newPlay[key] = value
                elif key == 'playStatus':
                    newPlay[key] = self._pbp_playstatus(value)
                elif key in ['pass', 'rush', 'sack', 'kick', 'penalty', 'punt', 'fumble', 'fieldGoalAttempt',
                             'extraPointAttempt', 'lateralPass']:
                    newPlay['name'] = key
                    newPlay['properties'] = self._pbp_play_properties(value)
                else:
                    newPlay[key] = value

            if not 'name' in newPlay:
                logger.error('Error play: \n%s\nnewPlay:\n%s\n', play, newPlay)
                return None

            self._pbp_parse_description(newPlay)
            if newPlay['name'] == 'penalty' and top:
                penaltyProperties = self._pbp_play_properties(newPlay['properties']['penalty'])
                # logger.debug('Opening penalty: \n%s\nproperties:\n%s\n', newPlay['properties'], penaltyProperties)
                newPlay['properties'].pop('penalty')
                for key, value in penaltyProperties.items():
                    newPlay['properties'][key] = value

            self.playCounter += 1
            newPlay['index'] = self.playCounter
            self.playsList.append(newPlay)
        except Exception as e:
            logger.error('Error processing play:\n%s\n', play)
            raise e

        return newPlay

    @contendo_classfunction_logger
    def _create_new_subplay(self, newPlay, subplay):
        newSubplay = self._create_newplay(subplay)
        newSubplay['parentIndex'] = newPlay['index']
        newSubplay['parentPlayType'] = newPlay['name']
        newSubplay['playStatus'] = newPlay['playStatus']
        newSubplay['isSubplay'] = True

    @contendo_classfunction_logger
    def pbp_to_bigqery_form(self, pbpDict, season):

        self.reset(pbpDict, season)

        for play in pbpDict['plays']:
            newPlay = self._create_newplay(play, top=True)

            if 'penalties' in newPlay['properties']:
                penalties = newPlay['properties'].pop('penalties')
                for penalty in penalties:
                    if type(penalty['penalty'])==dict:
                        penalties2 = [penalty['penalty']]
                    else:
                        penalties2 = penalty['penalty']

                    for penalty2 in penalties2:
                        self._create_new_subplay(newPlay, {'penalty': penalty2})

            if 'subPlays' in newPlay['properties']:
                subplays = newPlay['properties'].pop('subPlays')
                for subPlay in subplays:
                    found=False
                    for sybplayName in ['fumble', 'lateralPass', 'pass', 'rush']:
                        if sybplayName in subPlay:
                            found=True
                            if type(subPlay[sybplayName]) == dict:
                                subplays2 = [subPlay[sybplayName]]
                            elif type(subPlay[sybplayName]) == list:
                                subplays2 = subPlay[sybplayName]
                            else:
                                logger.error('Error: illegal Subplay: %s', subPlay)
                            for subplay2 in subplays2:
                                self._create_new_subplay(newPlay, {sybplayName: subplay2})
                    if not found:
                        logger.error('Error: Unknown Subplay: %s', subPlay)

        return {'plays': self.playsList}

# Main Test function
@contendo_function_logger
def test():
    startTime=dt.now()
    pd.set_option('display.max_columns', 200)
    pd.set_option('display.width', 2000)
    #os.environ['CONTENDO_AT_HOME'] = 'y'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.environ['CONTENDO_DEV']='y'
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))

    testfile = 'game_playbyplay-2019-regular-51555-20192010-CIN-JAX.json'
    testfile = 'game_playbyplay-2019-regular-51578-20192710-NE-CLE.json'
    pbpDict = ProUtils.get_dict_from_jsonfile('results/nfl/game_playbyplay/'+testfile)
    pcb = NFLPbpContextBuilder()
    newpbp = pcb.digest_pbp(pbpDict=pbpDict, season='2019-regular')
    #print(json.dumps(newpbp))
    ProUtils.save_dict_to_jsonfile(testfile, newpbp)

    df = pd.DataFrame(newpbp['plays'])
    print(df.shape, df.columns)
    df.to_csv(testfile+'.csv')

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.DEBUG)
    test()
