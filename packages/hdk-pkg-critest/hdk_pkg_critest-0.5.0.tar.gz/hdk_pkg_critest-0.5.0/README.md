# hdk_pkg_critest

This is a demo package for CRI test. 
This package is for processing kline data and running strategy backtest. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hdk_pkg_critest.

```bash
pip install hdk_pkg_critest
```

## Quick Start

The package can be run on shell or CMD, but better to use an IDE (Try [Spyder](https://www.spyder-ide.org/) so that you can check the outputs clearly. 

This chapter gives a simple demo of doing a momentum strategy backtest using the package. All the codes can also be found in `demo.py`.

Please refer to next chapter for detailed documentation on the package.

### STEP 1: Import the Package and Initialization

First, let's import the package, then initialize four main classes inside. 
Once you initialize an instance of a class, you can easily call methods (functions) from it by doing this: `return = instance.function(Args..)`

```python
import hdk_pkg_critest

sampledata = critest.SampleData()    # a class packages the methods for fetching the sample data set
process = critest.Process()    # a class packages the methods for processing data
backtest = critest.BackTest()    # a class packages the methods for running backtesting
plotting = critest.Plotting()    # a class packages the methods for Plotting the backtest results

```

### STEP 2: Get a Sample Data Set for Test

Let's use the `get_sampledata()` from the `sampledata` to get a sample data set. Use `data.head()` to check the data.

```python
data = sampledata.get_sampledata()    # a time-series data set of a future's kline 

data.head()    # check what the data set looks like
```

### STEP 3: Process the Data to Generate Factors

There are some kline process funcions in the class `process`. You can call and apply any of them on the data. For a momentum strategy, we need to process the kline as below:

```python
#1 transfer the 1min kline to 60mins kline:
data_60 = process.chg_Granularity(data_1min=data, granularity=60)
data_60.head() 

#2 generate HA kline:
data_HA = process.get_BarHA(Open=data_60.open, High=data_60.high, Low=data_60.low, Close=data_60.close)
data_HA.head() 

#3 generate PS factor:
data_PS = process.get_BarPS(HA_Open=data_HA.HA_Open, HA_Close=data_HA.HA_Close, HA_PS_Lookback=20, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False)
data_PS.head() 

#4 generate CT factor:
data_CT = process.get_BarCT(HA_Open=data_HA.HA_Open, HA_Close=data_HA.HA_Close, HA_PS=data_PS, bar_pass_cut=2, ps_pass_cut=2)
data_CT.head() 
```

### STEP 4: Generate Buy Sell Indicators and Do Backtest

Now we should use it to generate buy sell indicators. This should follow some specific rules based on different strategies. 
(I have only built in one strategy rule called `momentum`. In fact, other strategies can be add inside the package easily.) 

Call `backtest_Momentum` from class `backtest`, then you will get a return as matrix (two-dimensional array). 
The buy sell indicator is in 4th column. We can use it to do backtest by calling `get_PnL`.

```python
backtest_Momentum = backtest.backtest_Momentum(data_PS=data_PS, data_CT=data_CT.bar_idx_live)
print (backtest_Momentum)    # see the return matrix

result = backtest.get_PnL(close=data_60.close, indicator=backtest_Momentum[:,2], cost=0.15/100, sharpe_frequency=365*2, beta=1)
print (result)    # see the backtest result
```

### STEP 5: Plot the Backtest Result

This step will plot a custom image based on the backtest result. Note that I only built-in one kind of custom image.

```python
plot1 = plotting.plot_type1(Open=data_60.open, High=data_60.high, Low=data_60.low, Close=data_60.close, indicator=backtest_Momentum[:,2], result=result)
```

## Author
He Dekun

## License
[MIT](https://choosealicense.com/licenses/mit/)

