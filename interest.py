from __future__ import division
import abc
import random

class AbstractFund(object):
  __metaclass__ = abc.ABCMeta
  
  @property
  def startBalance(self):
    return self.__startBalance
  @startBalance.setter
  def startBalance(self, value):
    self.__startBalance = value
  
  def __init__(self, startBalance=0):
    self.startBalance = startBalance

class ExchangeTradedFund(AbstractFund):
  __metaclass__ = abc.ABCMeta
  
  @property
  def interestRate(self):
    return self.__interestRate
  @interestRate.setter
  def interestRate(self, value):
    self.__interestRate = value
    
  @property
  def expenseRatio(self):
    return self.__expenseRatio
  @expenseRatio.setter
  def expenseRatio(self, value):
    self.__expenseRatio = value

  @property
  def dividendTax(self):
    return self.__dividendTax
  @dividendTax.setter
  def dividendTax(self, value):
    self.__dividendTax = value
  
  def __init__(self, interestRate, expenseRatio, dividendTax, *args, **kwargs):
    super(ExchangeTradedFund, self).__init__(*args, **kwargs)
    
    self.interestRate = interestRate
    self.expenseRatio = expenseRatio
    self.dividendTax = dividendTax
  
  def calculateBalance(self, dividends, dividendRate):
    balance = self.startBalance
    dividend = 0
    dividendTax = 0
    
    for n in range(0, len(dividends)):
      # calculate equity increase during this dividend window
      balance = balance * (1 + self.interestRate) ** dividendRate
      
      # calculate dividend
      grossDividend = balance * dividends[n]
      netDividend = grossDividend * (1 - self.dividendTax)
      
      dividendTax = dividendTax + grossDividend - netDividend
      dividend = dividend + netDividend
    
    return (balance, dividend, dividendTax)

class ETFVanguardFTSE100(ExchangeTradedFund):
  def __init__(self, *args, **kwargs):
    super(ETFVanguardFTSE100, self).__init__(expenseRatio=0.001, dividendTax=0.15, *args, **kwargs)

class AbstractBond(object):
  __metaclass__ = abc.ABCMeta
  
  @property
  def bondValue(self):
    return self.__bondValue
  @bondValue.setter
  def bondValue(self, value):
    self.__bondValue = value
  
  @property
  def numberOfBonds(self):
    return self.__numberOfBonds
  @numberOfBonds.setter
  def numberOfBonds(self, value):
    self.__numberOfBonds = value
  
  def __init__(self, bondValue, numberOfBonds):
    self.bondValue = bondValue
    self.numberOfBonds = numberOfBonds

class PremiumBond(AbstractBond):
  """
  odds = 1 / chance of winning per bond per month
    so odds of 1/26000 would be stated as 26000.
  """
  
  __metaclass__ = abc.ABCMeta
  
  @property
  def prize(self):
    return self.__prize
  @prize.setter
  def prize(self, value):
    self.__prize = value
    
  @property
  def odds(self):
    return self.__odds
  @odds.setter
  def odds(self, value):
    self.__odds = value
  
  def __init__(self, prize, odds, *args, **kwargs):
    super(PremiumBond, self).__init__(*args, **kwargs)
    
    self.prize = prize
    self.odds = odds

  def calculateBalance(self, days):
    balance = self.numberOfBonds * self.bondValue
    
    while days >= 0:
      for i in range(0, self.numberOfBonds):
	if random.randint(0, self.odds) == self.odds:
	  balance += self.prize
      
      days -= 30
    
    return balance

class NationalSavingsAndInvestmentsPremiumBond(PremiumBond):
  def __init__(self, *args, **kwargs):
    super(NationalSavingsAndInvestmentsPremiumBond, self).__init__(prize=25, odds=26000, bondValue=1, *args, **kwargs)

###
# ETF example

balance = 1000
rate = 0.1/365
dividends = [0.0036, 0.0026, 0.0017, 0.0023, 0.0037, 0.003, 0.0018, 0.0119]
window = 91

fund = ETFVanguardFTSE100(startBalance=balance, interestRate=rate)
balance = fund.calculateBalance(dividends=dividends, dividendRate=window)

print "\nETF example"
print "\nAfter {0} days...\nBalance: {1:.2f}\nGrowth: {2:.2f} ({3:.2f}%)\nDividends: {4:.2f}\nTax: {5:.2f}".format(len(dividends) * window,
 balance[0], balance[0] - fund.startBalance, 100 * (balance[0] - fund.startBalance) / fund.startBalance, balance[1], balance[2])

###
# Premium bond example

days = 365 * 2
bonds = 1000

bond = NationalSavingsAndInvestmentsPremiumBond(numberOfBonds=bonds)
balance = bond.calculateBalance(days)

print "\nPremium bond example (includes random chance element)"
print "\nAfter {0} days with {1} bonds...\nBalance: {2:.2f}\nGrowth: {3:.2f} ({4:.2f}%)".format(days, bonds, balance, balance - bonds * bond.bondValue, 100 * (balance - bonds * bond.bondValue) / (bonds * bond.bondValue))