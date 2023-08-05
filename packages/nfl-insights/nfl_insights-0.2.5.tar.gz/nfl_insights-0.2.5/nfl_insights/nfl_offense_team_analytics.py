import pandas as pd
import numpy as np
import os
import logging
import pickle

from nfl_insights import NFLStatsQueries
from contendo_utils import *

# noinspection PyUnresolvedReferences
class OffenseTeamData:

    @contendo_classfunction_logger
    def __init__(self, seasons):
        assert type(seasons)==list, 'seasons parameter must be a list, "{}" is illegal'.format(seasons)
        self.generator = NFLStatsQueries('sportsight-tests')
        #
        # combining the regular and complex stats
        self.statsDict = self.generator.statsDict.copy()
        for key,value in self.generator.compStatsDict.items():
            self.statsDict[key] = value

        self.all_team_stats_filename = 'resource/all_team_stats.csv'
        # get team names and IDs
        self.teams = self.generator.nfldata.get_teams_df(season=seasons[0])

        #build a table for each stats with all dimensions
        self.metrics = dict()
        self.allTeamsStatsDF = pd.DataFrame()
        #self.generator.nfldata._update_pbp_data()
        self._read_all_metrics(seasons)

    def _read_all_metrics(self, seasons):
        if not os.path.exists(self.all_team_stats_filename):
            logger.info('Building metrics...')
            self._build_all_metrics(seasons)

        self.allTeamsStatsDF = pd.read_csv(self.all_team_stats_filename)
        return

        for statName in self.statList:
            statsfile = 'resource/stats_{}.pkl'.format(statName)
            if os.path.exists(statsfile):
                logger.info('Reading %s', statsfile)
                self.metrics[statName] = pd.read_pickle(statsfile)

    def _add_result_df_to_team_metrics(self, statName, df, dim):
        #_result = self.metrics[statName]
        #_colname = statName + "_" + dim
        #_result[_colname] = np.zeros(32)
        if df.shape[0] != 0:
            #df = df.set_index('teamId')
            df['teamName'] = self.teams['teamFullname']
            #_result[_colname] = df["statValue"]
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
        #print(_result)
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

        #logger.debug('Dimensions groups: %s', _dimensionGroupsDict)
        counter = 0
        lineCounter=0
        self.outfile = open(self.all_team_stats_filename, 'w')
        self.header = True
        for statName, statDef in self.statsDict.items():
            if statDef['Doit'] !='y':
                continue
            #self.metrics[statName] = self.teams.copy()
            for object in ['offenseTeam', 'defenseTeam']:
                _alldf = None
                for dimGroup1 in _dimGroupList:
                    logger.info('%4d. calculating stat: %s, dim-group1: %s, data: %s', counter, statName, dimGroup1, lineCounter)
                    for dimGroup2 in _dimGroupList:
                        if _dimensionsMatrixDict[dimGroup2][dimGroup1]==1:
                            for dim1 in _dimensionGroupsDict[dimGroup1]:
                                for dim2 in _dimensionGroupsDict[dimGroup2]:
                                    counter+=1
                                    _dimComb2 = [dim1, dim2]
                                    #print('{}\t{}\t{}'.format( counter,dim1, dim2))

                                    if 'StatRatio' in statDef:
                                        calculation = 'ratio'
                                        _df = self.generator.pbp_get_composed_stat(
                                            compstat=statName,
                                            object=object,
                                            dimensions=_dimComb2,
                                            seasons=seasons,
                                        )
                                    else:
                                        calculation = 'stat'
                                        _df = self.generator.pbp_get_stat(
                                            statName=statName,
                                            object=object,
                                            dimensions=_dimComb2,
                                            seasons=seasons,
                                        )

                                    if _dimComb2 == ['all', 'all']:
                                        #print ('setting alldf')
                                        _alldf = _df

                                    if _df.shape[0]>0:
                                        lineCounter+=_df.shape[0]
                                        _calcDF = _df.copy()
                                        _calcDF['calculation'] = calculation
                                        self._add_result_df_to_team_metrics(statName, _calcDF, dim='{}_{}'.format(dim1, dim2))
                                        if 'playType' in statDef: # not ratio stat
                                            _calcDF['calculation'] = 'pct'
                                            _calcDF['statValue'] = _df['statValue']/_alldf['statValue']
                                            self._add_result_df_to_team_metrics(statName, _calcDF, dim='{}_{}_pct'.format(dim1, dim2))
                                            _calcDF['calculation'] = 'per-game'
                                            _calcDF['statValue'] = _df['statValue']/_df['nGames']
                                            self._add_result_df_to_team_metrics(statName, _calcDF, dim='{}_{}_pg'.format(dim1, dim2))
                                            _calcDF['calculation'] = 'per-drive'
                                            _calcDF['statValue'] = _df['statValue']/_df['nDrives']
                                            self._add_result_df_to_team_metrics(statName, _calcDF, dim='{}_{}_pg'.format(dim1, dim2))
                                            if statDef['Function'] == 'sum':
                                                _calcDF['calculation'] = 'per-play'
                                                _calcDF['statValue'] = _df['statValue'] / _df['count']
                                                self._add_result_df_to_team_metrics(statName, _calcDF,
                                                                                    dim='{}_{}_avg'.format(dim1, dim2))

            #self.metrics[statName].fillna(0)
            logger.info ('Writing stat: %s', statName)
            #self.metrics[statName].to_pickle('resource/stats_{}.pkl'.format(statName))
            #self.metrics[statName].to_csv('resource/stats_{}.csv'.format(statName), index=True)
            #break
        self.outfile.close()
        logger.debug('Num queries: %d, Num results: %d', counter, lineCounter)
        return lineCounter

@contendo_function_logger
def test():
    logger.info('Starting...')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/sportsight-tests.json".format(os.environ["HOME"])
    os.chdir('{}/tmp/'.format(os.environ["HOME"]))
    pd.set_option('display.max_columns', 1500)
    pd.set_option('display.width', 20000)
    ostats = OffenseTeamData(seasons=['2019-regular'])
    logger.info (ostats.allTeamsStatsDF.shape)
    groups = ostats.allTeamsStatsDF.groupby(['statName', 'dimensions', 'seasons', 'calculation'])
    logger.info(len(groups.groups.keys()))
    for key in list(groups.groups.keys()):
        #logger.info(key)
        gr = groups.get_group(key)
    logger.info('Done.')

if __name__ == '__main__':
    contendo_logging_setup(default_level=logging.INFO)
    test()
