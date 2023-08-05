import decimal
import math
import random

import numpy
import numpy.random as nrand
import scipy.linalg


class ModelParameters:
    """
    Encapsulates model parameters
    """

    def __init__(self,
                 all_s0,
                 all_time,
                 all_delta,
                 all_sigma,
                 gbm_mu,
                 jumps_lamda=0.0,
                 jumps_sigma=0.0,
                 jumps_mu=0.0,
                 cir_a=0.0,
                 cir_mu=0.0,
                 all_r0=0.0,
                 cir_rho=0.0,
                 ou_a=0.0,
                 ou_mu=0.0,
                 heston_a=0.0,
                 heston_mu=0.0,
                 heston_vol0=0.0):
        # This is the starting asset value
        self.all_s0 = all_s0
        # This is the amount of time to simulate for
        self.all_time = all_time
        # This is the delta, the rate of time e.g. 1/252 = daily, 1/12 = monthly
        self.all_delta = all_delta
        # This is the volatility of the stochastic processes
        self.all_sigma = all_sigma
        # This is the annual drift factor for geometric brownian motion
        self.gbm_mu = gbm_mu
        # This is the probability of a jump happening at each point in time
        self.lamda = jumps_lamda
        # This is the volatility of the jump size
        self.jumps_sigma = jumps_sigma
        # This is the average jump size
        self.jumps_mu = jumps_mu
        # This is the rate of mean reversion for Cox Ingersoll Ross
        self.cir_a = cir_a
        # This is the long run average interest rate for Cox Ingersoll Ross
        self.cir_mu = cir_mu
        # This is the starting interest rate value
        self.all_r0 = all_r0
        # This is the correlation between the wiener processes of the Heston model
        self.cir_rho = cir_rho
        # This is the rate of mean reversion for Ornstein Uhlenbeck
        self.ou_a = ou_a
        # This is the long run average interest rate for Ornstein Uhlenbeck
        self.ou_mu = ou_mu
        # This is the rate of mean reversion for volatility in the Heston model
        self.heston_a = heston_a
        # This is the long run average volatility for the Heston model
        self.heston_mu = heston_mu
        # This is the starting volatility value for the Heston model
        self.heston_vol0 = heston_vol0

    def set_time(self, _time):
        self.all_time = _time

    def set_start_price(self, price):
        self.all_s0 = price

    def set_gbm_trend(self, trend: float):
        self.gbm_mu = trend

    def set_jump_size(self, size):
        pass

    def set_drift_factor(self):
        pass

    def set_jump_probability(self, prob):
        pass

    def set_start_hest_vol(self, vol):
        pass

    def set_avg_hest_vol(self, vol):
        pass


def convert_to_returns(log_returns):
    """
    This method exponentiates a sequence of log returns to get daily returns.
    :param log_returns: the log returns to exponentiated
    :return: the exponentiated returns
    """
    return numpy.exp(log_returns)


def convert_to_prices(param, log_returns):
    """
    This method converts a sequence of log returns into normal returns (exponentiation) and then computes a price
    sequence given a starting price, param.all_s0.
    :param param: the model parameters object
    :param log_returns: the log returns to exponentiated
    :return:
    """
    returns = convert_to_returns(log_returns)
    # A sequence of prices starting with param.all_s0
    price_sequence = [param.all_s0]
    for i in range(1, len(returns)):
        # Add the price at t-1 * return at t
        price_sequence.append(price_sequence[i - 1] * returns[i - 1])
    return numpy.array(price_sequence)
