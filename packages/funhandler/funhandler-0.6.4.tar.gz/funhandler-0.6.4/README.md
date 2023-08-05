# Funhandler
This is the general data handler for the funguana main trading bot.

TODO: Transition to a Gym-like environment.

```python
    bars, done = env.step(action=action, selector=selection)
    
    process_bars(bars, dispatcher=dispatcher)
```


## Requirements
- pandas
- funtime
- funpicker
- dask[complete]
## How to install
```
pip install funhandler
```
This is the general data handler for the funguana main trading bot

Use to run through various events inside of the DB.

or use this:
```python
fh.set_host('localhost')
fh.set_store_name('test_store_name')
fh.set_storage_model('local')
fh.set_local_storage_info(base_path='/tmp', storage_folder='parquet_data')
fh.initialize_database()
unique_data = {
    "type": "price",
    "base": "ETC",
    "trade": "BTC",
    "exchange": "binance",
    "period": "minute"
}
fh.add_bars([unique_data])
fh.load_data(**unique_data)

while fh.is_still_bars(**unique_data):
    unique_data.update({'limit': 5})
    bars = fh.get_latest_bar_v2(**unique_data)
    print(bars)
```

result:
```
➜ python manual_run.py
Register Library Type
   base     close exchange      high    ...     trade   type volumefrom  volumeto
25  ETC  0.001188  binance  0.001189    ...       BTC  price      93.40    0.1110
26  ETC  0.001187  binance  0.001188    ...       BTC  price     131.26    0.1559
27  ETC  0.001187  binance  0.001188    ...       BTC  price     192.74    0.2288
28  ETC  0.001186  binance  0.001187    ...       BTC  price     216.64    0.2570
29  ETC  0.001187  binance  0.001187    ...       BTC  price       0.00    0.0000

[5 rows x 13 columns]
   base     close exchange      high    ...     trade   type volumefrom  volumeto
20  ETC  0.001187  binance  0.001188    ...       BTC  price     366.37   0.43520
21  ETC  0.001188  binance  0.001189    ...       BTC  price     637.63   0.75680
22  ETC  0.001189  binance  0.001191    ...       BTC  price    1091.03   1.30000
23  ETC  0.001189  binance  0.001189    ...       BTC  price     137.56   0.16340
24  ETC  0.001189  binance  0.001189    ...       BTC  price      12.71   0.01511

[5 rows x 13 columns]
   base     close exchange      high    ...     trade   type volumefrom  volumeto
15  ETC  0.001187  binance  0.001188    ...       BTC  price      84.32   0.10010
16  ETC  0.001188  binance  0.001188    ...       BTC  price     137.08   0.16280
17  ETC  0.001185  binance  0.001189    ...       BTC  price      80.58   0.09568
18  ETC  0.001187  binance  0.001187    ...       BTC  price     118.99   0.14120
19  ETC  0.001187  binance  0.001188    ...       BTC  price      77.80   0.09236

[5 rows x 13 columns]
   base     close exchange      high    ...     trade   type volumefrom  volumeto
10  ETC  0.001187  binance  0.001188    ...       BTC  price     719.54    0.8544
11  ETC  0.001186  binance  0.001188    ...       BTC  price     154.78    0.1839
12  ETC  0.001188  binance  0.001188    ...       BTC  price     232.66    0.2763
13  ETC  0.001186  binance  0.001188    ...       BTC  price     100.48    0.1192
14  ETC  0.001188  binance  0.001188    ...       BTC  price     183.76    0.2181

[5 rows x 13 columns]
  base     close exchange      high    ...     trade   type volumefrom  volumeto
5  ETC  0.001186  binance  0.001187    ...       BTC  price     274.22    0.3253
6  ETC  0.001186  binance  0.001187    ...       BTC  price     636.99    0.7560
7  ETC  0.001186  binance  0.001186    ...       BTC  price      89.31    0.1059
8  ETC  0.001187  binance  0.001188    ...       BTC  price     193.95    0.2300
9  ETC  0.001188  binance  0.001188    ...       BTC  price     159.30    0.1892

[5 rows x 13 columns]
  base     close exchange      high    ...     trade   type volumefrom  volumeto
0  ETC  0.001185  binance  0.001186    ...       BTC  price     150.20   0.17800
1  ETC  0.001186  binance  0.001187    ...       BTC  price     161.09   0.19100
2  ETC  0.001186  binance  0.001187    ...       BTC  price     601.29   0.71350
3  ETC  0.001186  binance  0.001186    ...       BTC  price      38.33   0.04546
4  ETC  0.001186  binance  0.001186    ...       BTC  price     246.29   0.29210

[5 rows x 13 columns]
```


## Session Object

Upon reading the code for funhandler. We decided that the foundation of the code was perfect for our session store. The session store is the piece of code we use with strategies to handle outside information. This includes online learning/estimation algorithms, and constant data that needs to be called upon. It has many of the same calls the normal funhandler library has.

```python
sess = Session()
sess.set_host('localhost')
sess.set_store_name('test_store_name')
sess.set_storage_model('local')
sess.set_local_storage_info(base_path='/tmp', storage_folder='parquet_data')
sess.initialize_database()



# sess.load_bars({...})

# while fh.is_still_bars(**unique_data):
#     unique_data.update({'limit': 5})
#     bars = fh.get_latest_bar_v2(**unique_data)
#     print(bars)


# Adding state information as well

sess.add(CustomReinforcementAlgorithm())
sess.add(CustomDispatcher())
sess.add(CustomEstimatorCode())

```


