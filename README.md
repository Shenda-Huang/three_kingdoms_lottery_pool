# run-lottery

## About

This script will give an average number of drawings a user need to make for obtaining all items inside a lottery pool.

## Usage of script

``` bash
usage: __main__.py [-h] [-l LOG_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] -n NUM_USERS [NUM_USERS ...] taskname

positional arguments:
  taskname

options:
  -h, --help            show this help message and exit
  -l LOG_FILE, --log-file LOG_FILE
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  -n NUM_USERS [NUM_USERS ...], --num-users NUM_USERS [NUM_USERS ...]
                        Number of users who entered in the lottery
```

## Input file

There are 3 files to be imported. Listed as following with explanation of each column.

### Pool

- `奖池`
- `单抽权重`
- `单抽概率`
- `第十抽权重`
- `十抽概率`
- `综合概率`

### Items

- `类型`
- `道具`
- `数量`
- `所属池`
- `权重`
- `替换数量`
- `兑换数量`

### Cash

- `倍率`
- `权重`
- `概率`
