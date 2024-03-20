# -*- coding: utf-8 -*-
"""
general data types
"""

from typing import List, Set

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Cash:
    """Leaf class for cash multiplier"""

    multiplier: int = 0
    weight: int = 0
    accWeight: int = 0


@dataclass(kw_only=True)
class CashBucket:
    """Root class for all available cash buckets for randomization"""

    cashList: List[Cash] = field(default_factory=list)
    totalWeight: int = 0


@dataclass(kw_only=True)
class Item:
    """Leaf class for game items"""

    id: int = 0
    name: str = ""
    poolId: str = ""
    poolName: str = ""
    weight: int = 0
    accWeight: int = 0
    count: int = 0
    value: int = 0
    redeemValue: int = 0


@dataclass(kw_only=True)
class Pool:
    """Node class for pool of a set of game items"""

    id: int = 0
    name: str = ""
    itemList: List[Item] = field(default_factory=list)
    weight: int = 0
    accWeight: int = 0
    tenthWeight: int = 0
    tenthAccWeight: int = 0
    totalWeight: int = 0


@dataclass(kw_only=True)
class PoolBucket:
    """Root class for all available pools for randomization"""

    poolList: List[Pool] = field(default_factory=list)
    totalWeight: int = 0
    tenthTotalWeight: int = 0


@dataclass(kw_only=True)
class User:
    """Root class for keeping track of user owned items and cash"""

    itemIds: Set[int] = field(default_factory=set)
    totalCash: int = 0
    missingItemsTotalValue: int = 0
