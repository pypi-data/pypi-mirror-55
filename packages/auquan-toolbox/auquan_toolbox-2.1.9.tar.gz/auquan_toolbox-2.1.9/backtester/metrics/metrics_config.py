import numpy as np
import pandas as pd
from backtester.logger import *

class MetricCalculator(object):

    '''
    Compute Metric
    '''
    @classmethod
    def compute(cls, dict=None, df=None, params=None, metricKey=None):
        raise NotImplementedError
        return None

class Accuracy(MetricCalculator):

    @classmethod
    def compute(cls, dict=None, df=None, params=None, metricKey=None):
        if dict is not None:
            total_count =dict.getFeatureDf(params['count_profit']).iloc[-1] + dict.getFeatureDf(params['count_loss']).iloc[-1]
            total_count[total_count==0] = 1
            return  (dict.getFeatureDf(params['count_profit']).iloc[-1] / total_count.astype(float)).to_dict()
        
        elif df is not None:
            total_count = df[params['count_profit']].iloc[-1] + df[params['count_loss']].iloc[-1]
            if total_count == 0:
                return 0
            return df[params['count_profit']].iloc[-1] / float(total_count)
        
        else:
            logError('You havent specified either a instrumentFeatures dict or a marketDf')
            return None


class ProfitFactor(MetricCalculator):

    @classmethod
    def compute(cls, dict=None, df=None, params=None, metricKey=None):
        if dict is not None:
            total_profit = dict.getFeatureDf(params['total_profit']).iloc[-1]
            total_loss = dict.getFeatureDf(params['total_loss']).iloc[-1]
            total_loss[total_loss==0] = 1
            return  (total_profit.astype(float) / total_loss.astype(float)).to_dict()
        
        elif df is not None:
            total_profit = df[params['total_profit']].iloc[-1]
            total_loss = df[params['total_loss']].iloc[-1]
            if total_loss == 0:
                return float('nan')
            return total_profit / float(total_loss)
        
        else:
            logError('You havent specified either a instrumentFeatures dict or a marketDf')
            return None



