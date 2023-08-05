import pandas as pd
import numpy as np
import os
import logging
import pickle

from nfl_insights import *
from contendo_utils import *

# noinspection PyUnresolvedReferences
class NFLTeamAnalytics:

    class TeamsStatsDict(dict):
        def __init__(self, statsDF):
            self._statsDF = statsDF
            self._dfkeys = ['statValue', 'teamName', 'count','nGames','nDrives','rank','avg','stddev','stddev/avg','stdFactor','absStdFactor', 'nItems'
                            #, 'statName','statObject','dimensions','season','calculation'
                            ]
            self._statGroups = self._statsDF.groupby(['dimensions', 'calculation'])
            for _groupkey in self._statGroups.groups.keys():
                self[_groupkey] = ''

        def __getitem__(self, key):
            _df = self._statGroups.get_group(key).set_index('teamId')
            return _df

        def get(self, dimensions: list, calculation: str):
            dimensions.sort()
            key = (str(dimensions), calculation)
            logger.debug(key)
            return self[key]

    @contendo_classfunction_logger
    def __init__(self, seasons, build=False):
        assert type(seasons)==list, 'seasons parameter must be a list, "{}" is illegal'.format(seasons)
        self.generator = NFLStatsQueries('sportsight-tests')
        #
        # combining the regular and complex stats
        self.statsDict = self.generator.statsDict.copy()
        for key,value in self.generator.compStatsDict.items():
            self.statsDict[key] = value

        self.all_team_stats_filename = 'resource/nfl_team_stats.csv'
        self.all_team_stats_pickle_filename = 'resource/nfl_team_stats.pkl'

        #build a table for each stats with all dimensions
        self.metrics = dict()
        self.allTeamsStatsDF = pd.DataFrame()
        if build:
            self._build_all_metrics(seasons=seasons)
        self._read_all_metrics(seasons)

    def _read_all_metrics(self, seasons):
        logger.debug('downloading metrics files from GCP')
        self.generator.nfldata.bqu.download_from_gcp(NFL_GCP_BUCKET, self.all_team_stats_filename, self.all_team_stats_filename, checkTimestamp=True)
        self.generator.nfldata.bqu.download_from_gcp(NFL_GCP_BUCKET, self.all_team_stats_pickle_filename, self.all_team_stats_pickle_filename, checkTimestamp=True)
        logger.debug('Loading csv file to memory')
        self.allTeamsStatsDF = pd.read_csv(self.all_team_stats_filename)
        logger.debug('Loading pickle file to memory')
        with open(self.all_team_stats_pickle_filename, 'rb') as handle:
            self.allStatsDict = pickle.load(handle)
        logger.debug('Done loading')
        return

    def _add_result_df_to_team_metrics(self, statName, df):
        if df.shape[0] != 0:
            #
            # Enrich the df with aggregative stats.
            avg = df['statValue'].mean()
            std = df['statValue'].std()
            df['avg'] = avg
            df['stddev'] = std
            df['stddev/avg'] = std / avg
            df['stdFactor'] = (df['statValue'] - avg) / std
            df['absStdFactor'] = abs((df['statValue'] - avg) / std)
            df['avgDiff%'] = (df['statValue'] - avg) / avg * 100
            df['nItems'] = df.shape[0]
            df['rank'] = df['statValue'].rank(method='min', ascending=False)
            # add to the csv
            df.to_csv(self.outfile, header=self.header)
            self.header = False
            # Add the df to the dictionary
            row = dict(df.iloc[0])
            _mainkey = (row['season'], row['statName'], row['statObject'])
            _seckey = (row['dimensions'], row['calculation'])
            self.allStatsDict[_mainkey] = self.allStatsDict.get(_mainkey, dict())
            self.allStatsDict[_mainkey][_seckey] = df

    @contendo_classfunction_logger
    def _build_all_metrics(self, seasons):

        _dimensionsMatrixDict = self.generator.dimentionsMatrixDict
        _dimensionsDF = self.generator.dimentionsDF
        _dimensionGroups = _dimensionsDF.groupby(['GroupCode'])
        _dimGroupList = list(_dimensionsMatrixDict.keys())
        _dimGroupList.sort()
        print(_dimGroupList)

        _dimensionGroupsDict = dict()
        for dimGroup in _dimGroupList:
            _dimDF = _dimensionGroups.get_group(dimGroup)
            _dimensionGroupsDict[dimGroup] = list(_dimDF['ConditionCode'])

        counter = 0
        lineCounter=0
        _statsfile = self.all_team_stats_filename+'new'
        self.outfile = open(_statsfile, 'w')
        self.allStatsDict = dict()
        self.header = True
        for statName, statDef in self.statsDict.items():
            if statDef['Doit'] !='y':
                continue
            for season in seasons:
                for object in ['offenseTeam']: #, 'defenseTeam']:
                    _alldf = None
                    for dimGroup1 in _dimGroupList:
                        logger.info('%4d. calculating stat: %s, object: %s, dim-group1: %s, data: %s', counter, statName, object, dimGroup1, lineCounter)
                        for dimGroup2 in _dimGroupList:
                            if _dimensionsMatrixDict[dimGroup2][dimGroup1]==1:
                                for dim1 in _dimensionGroupsDict[dimGroup1]:
                                    for dim2 in _dimensionGroupsDict[dimGroup2]:
                                        counter+=1
                                        _dimComb2 = [dim1, dim2]

                                        if 'StatRatio' in statDef:
                                            calculation = 'ratio'
                                            _df = self.generator.pbp_get_composed_stat(
                                                compstat=statName,
                                                object=object,
                                                dimensions=_dimComb2,
                                                season=season,
                                            )
                                        else:
                                            calculation = 'stat'
                                            _df = self.generator.pbp_get_stat(
                                                statName=statName,
                                                object=object,
                                                dimensions=_dimComb2,
                                                season=season,
                                            )

                                        if _dimComb2 == ['all', 'all']:
                                            _alldf = _df

                                        if _df.shape[0]>0:
                                            lineCounter+=_df.shape[0]
                                            _calcDF = _df.copy()
                                            _calcDF['calculation'] = calculation
                                            self._add_result_df_to_team_metrics(statName, _calcDF)
                                            if 'playType' in statDef: # not ratio stat
                                                _calcDF['calculation'] = 'pct'
                                                _calcDF['statValue'] = _df['statValue']/_alldf['statValue']
                                                self._add_result_df_to_team_metrics(statName, _calcDF)
                                                _calcDF['calculation'] = 'per-game'
                                                _calcDF['statValue'] = _df['statValue']/_df['nGames']
                                                self._add_result_df_to_team_metrics(statName, _calcDF)
                                                _calcDF['calculation'] = 'per-drive'
                                                _calcDF['statValue'] = _df['statValue']/_df['nDrives']
                                                self._add_result_df_to_team_metrics(statName, _calcDF)
                                                if statDef['Function'] == 'sum':
                                                    _calcDF['calculation'] = 'per-play'
                                                    _calcDF['statValue'] = _df['statValue'] / _df['nPlays']
                                                    self._add_result_df_to_team_metrics(statName, _calcDF)
                        #break
                    #break
            logger.info ('End stat: %s', statName)
            #break
        self.outfile.close()
        logger.debug('Num queries: %d, Num results: %d', counter, lineCounter)
        logger.info('Uploading %s uploaded to GCP', self.all_team_stats_filename)
        self.generator.nfldata.bqu.upload_file_to_gcp(NFL_GCP_BUCKET, _statsfile, self.all_team_stats_filename, timestamp=True)
        logger.info('Saving pickle File %s', self.all_team_stats_pickle_filename)
        with open(self.all_team_stats_pickle_filename, 'wb') as handle:
            pickle.dump(self.allStatsDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info('Uploading %s uploaded to GCP', self.all_team_stats_pickle_filename)
        self.generator.nfldata.bqu.upload_file_to_gcp(NFL_GCP_BUCKET, self.all_team_stats_pickle_filename, self.all_team_stats_pickle_filename, timestamp=True)
        logger.info('File %s uploaded to GCP', self.all_team_stats_filename)

        return lineCounter

    @contendo_classfunction_logger
    def get_stat_iterator(self, statName, season, statObject):
        assert statName in self.statsDict, 'Illegal statname {}, must be one of {}'.format(statName, self.statsDict)
        assert season in ['2019-regular'], 'illegal season' + season
        assert statObject in ['offenseTeam', 'defenseTeam']
        _statsDF = self.allTeamsStatsDF.query('statName=="{}" and season=="{}" and statObject=="{}"'.format(statName, season, statObject))
        return self.TeamsStatsDict(_statsDF)

    @contendo_classfunction_logger
    def get_dimentions(self) -> dict:
        _dimsDict = dict()
        for dim, dimdef in self.generator.dimentionsDict.items():
            grc = dimdef['GroupCode']
            if grc not in _dimsDict:
                _dimsDict[grc] = list()
            _dimsDict[grc].append(dim)
        return _dimsDict


    @contendo_classfunction_logger
    def get_stats(self, teamType: str) -> list:
        _retList = list()
        for statName, statDef in self.statsDict.items():
            if statDef['TeamObjects'].find(teamType) >= 0 and statDef['Doit']=='y':
                _retList.append(statName)
        return _retList


@contendo_function_logger
def test():
    logger.info('Starting...')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    pd.set_option('display.max_columns', 1500)
    pd.set_option('display.width', 20000)
    #ostats = NFLTeamAnalytics(seasons=['2019-regular'], build=True)
    ostats = NFLTeamAnalytics(seasons=['2019-regular'], build=False)
    logger.info (ostats.allTeamsStatsDF.shape)
    #logger.info ('offense stats: %s', ostats.get_stats(teamType='offense'))
    #logger.info ('Dimensions: %s', ostats.get_dimentions())
    #groups = ostats.allTeamsStatsDF.groupby(['statName',  'statObject', 'seasons', 'dimensions', 'calculation'])
    #logger.info(len(groups.groups.keys()))
    stats = ostats.get_stats(teamType='offense')
    logger.info('starting dict, len=%d', len(ostats.allStatsDict))
    count=0
    for key in ostats.allStatsDict:
        for key1 in ostats.allStatsDict[key]:
            count+=1
            df = ostats.allStatsDict[key][key1]
    logger.info('dict done, #DFs: %d', count)
    print (df)

    #return
    for stat in stats:
        logger.info('Stat: %s', stat)
        statsDict = ostats.get_stat_iterator(statName=stat, season='2019-regular', statObject='offenseTeam')
        logger.info('Got iterator, keys: %d', len(statsDict))
        for key in statsDict:
            df = statsDict[key]
            if df.shape[0]!=32:
                logger.error('Error with metric %s, %s #teams=%d', stat, key, df.shape[0])
    logger.info('Done.')

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.DEBUG)
    test()
