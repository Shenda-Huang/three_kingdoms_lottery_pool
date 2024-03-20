# -*- coding: utf-8 -*-
"""
load data from xlsx files
"""

import logging

import pandas as pd

from pathlib import Path
from typing import Tuple

from .datatypes import Cash, CashBucket, Item, Pool, PoolBucket
from .exceptions import LocalRuntimeError
from .utils import Settings

LOGGER = logging.getLogger(__name__)


def load_from_file(filepath) -> pd.core.frame.DataFrame:
    """load from files"""

    path = Path(filepath)

    if path.exists() and path.is_file():
        LOGGER.info("Start loading data from %s", filepath)
        df = pd.read_excel(path)
        LOGGER.info("Successfully loaded data from %s", filepath)
        return df

    error = f"File '{filepath} does not exist'"
    LOGGER.error("DATA_LOADER_ERROR: %s", error)
    raise LocalRuntimeError(error)


def fillCashBucket(cash_df: pd.core.frame.DataFrame) -> CashBucket:
    """fill cash bucket"""
    cashBucket = CashBucket()

    accWeight = 0
    for _, row in cash_df.iterrows():
        accWeight += row["权重"]

        cash = Cash()
        cash.multiplier = row["倍率"]
        cash.weight = row["权重"]
        cash.accWeight = accWeight

        cashBucket.cashList.append(cash)
        cashBucket.totalWeight += cash.weight

    cashBucket.cashList.sort(key=lambda i: i.accWeight)

    return cashBucket


def fillItems(pool: Pool, items_df: pd.core.frame.DataFrame) -> Tuple[Pool, int]:
    """Fill items to a pool"""
    itemAccWeight = 0
    poolItemsTotalValue = 0

    for index, row in items_df.iterrows():
        if row["所属池"].lower() == pool.name.lower():
            itemAccWeight += row["权重"]

            item = Item()
            item.id = index
            item.name = row["道具"]
            item.poolId = pool.id
            item.poolName = pool.name
            item.weight = row["权重"]
            item.accWeight = itemAccWeight
            item.count = row["数量"]
            item.value = row["替换数量"]
            item.redeemValue = row["兑换数量"]

            pool.itemList.append(item)
            pool.totalWeight += item.weight
            poolItemsTotalValue += item.redeemValue

    pool.itemList.sort(key=lambda i: i.accWeight)

    return pool, poolItemsTotalValue


def fillPoolBucket(
    pool_df: pd.core.frame.DataFrame, items_df: pd.core.frame.DataFrame
) -> Tuple[PoolBucket, int]:
    pool_df.sort_values(by=["第十抽权重", "单抽权重"])
    items_df.sort_values(by=["所属池", "权重"])

    poolBucket = PoolBucket()
    itemsTotalValue = 0

    poolAccWeight = 0
    poolTenthAccWeight = 0
    for index, row in pool_df.iterrows():
        poolAccWeight += row["单抽权重"]
        poolTenthAccWeight += row["第十抽权重"]

        pool = Pool()
        pool.id = index
        pool.name = row["奖池"]
        pool.weight = row["单抽权重"]
        pool.accWeight = poolAccWeight
        pool.tenthWeight = row["第十抽权重"]
        pool.tenthAccWeight = poolTenthAccWeight

        pool, poolItemsTotalValue = fillItems(pool, items_df)

        poolBucket.poolList.append(pool)
        poolBucket.totalWeight += pool.weight
        poolBucket.tenthTotalWeight += pool.tenthWeight

        itemsTotalValue += poolItemsTotalValue

    # We use accWeight instead of tenthAccWeight because we sort the dataframe by tenthAccWeight initially
    poolBucket.poolList.sort(key=lambda i: i.accWeight)

    return poolBucket, itemsTotalValue


def load_data() -> Tuple[CashBucket, PoolBucket, int]:
    """load data from default files in Settings"""

    items_df = load_from_file(Settings.ITEMS_FILE_PATH)
    pool_df = load_from_file(Settings.POOL_FILE_PATH)
    cash_df = load_from_file(Settings.CASH_FILE_PATH)

    cashBucket = fillCashBucket(cash_df)
    poolBucket, itemsTotalValue = fillPoolBucket(pool_df, items_df)

    return cashBucket, poolBucket, itemsTotalValue
