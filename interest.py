import abc

class AbstractFund():
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

balance = 1000
rate = 0.1/365
dividends = [0.0036, 0.0026, 0.0017, 0.0023, 0.0037, 0.003, 0.0018, 0.0119]
window = 91

fund = ETFVanguardFTSE100(startBalance=balance, interestRate=rate)

balance = fund.calculateBalance(dividends=dividends, dividendRate=window)

print "After {0} days...\nBalance: {1}\nGrowth: {2}\nDividends: {3}\nTax: {4}".format(len(dividends) * window, balance[0], balance[0] - fund.startBalance, balance[1], balance[2])