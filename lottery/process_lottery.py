# -*- coding: utf-8 -*-
"""
process lottery
"""

import logging
import random

from dataclasses import asdict
from typing import List

from .data_loader import load_data
from .datatypes import CashBucket, PoolBucket, User
from .exceptions import LocalRuntimeError

LOGGER = logging.getLogger(__name__)


def _run_lottery(
    cashBucket: CashBucket, poolBucket: PoolBucket, itemsTotalValue: int
) -> int:
    """Running lottery for a user"""

    user = User()
    user.totalCash = 0
    user.missingItemsTotalValue = itemsTotalValue

    pick_count = 1
    while user.totalCash < user.missingItemsTotalValue:
        isTenthPick = pick_count % 10 == 0

        randPoolWeight = random.randint(
            1, poolBucket.tenthTotalWeight if isTenthPick else poolBucket.totalWeight
        )
        selectedPool = next(
            filter(
                lambda pool: (pool.tenthWeight if isTenthPick else pool.weight) > 0
                and (pool.tenthAccWeight if isTenthPick else pool.accWeight)
                >= randPoolWeight,
                poolBucket.poolList,
            ),
            None,
        )
        if selectedPool is None:
            raise LocalRuntimeError(
                f"""Select pool error with isTenthPick={isTenthPick} randPoolWeight={randPoolWeight} 
                    poolsTotalWeight={poolBucket.tenthTotalWeight if isTenthPick else poolBucket.totalWeight}"""
            )
        LOGGER.debug("Selected pool id=%i name=%s randPoolWeight=%i", selectedPool.id, selectedPool.name, randPoolWeight)

        randItemWeight = random.randint(1, selectedPool.totalWeight)
        selectedItem = next(
            filter(
                lambda item: item.accWeight >= randItemWeight, selectedPool.itemList
            ),
            None,
        )
        if selectedItem is None:
            raise LocalRuntimeError(
                f"Select item error with randItemWeight={randItemWeight} itemsTotalWeight={selectedPool.totalWeight}"
            )
        LOGGER.debug("Selected item id=%i name=%s randItemWeight=%i", selectedItem.id, selectedItem.name, randItemWeight)

        if selectedItem.value == 0:
            user.totalCash += selectedItem.count
        elif selectedItem.id in user.itemIds:
            randCashWeight = random.randint(1, cashBucket.totalWeight)
            selectedCash = next(
                filter(
                    lambda cash: cash.accWeight >= randCashWeight, cashBucket.cashList
                ),
                None,
            )
            if selectedCash is None:
                raise LocalRuntimeError(
                    f"Select cash error with randCashWeight={randCashWeight} cashTotalWeight={cashBucket.totalWeight}"
                )
            LOGGER.debug("Selected cash multiplier=%i randCashWeight=%i", selectedCash.multiplier, randCashWeight)
            user.totalCash += selectedItem.value * selectedCash.multiplier
        else:
            user.itemIds.add(selectedItem.id)
            user.missingItemsTotalValue -= selectedItem.redeemValue

        pick_count += 1

    return pick_count


def run_scenarios(num_users: List[int]) -> None:
    cashBucket, poolBucket, itemsTotalValue = load_data()

    LOGGER.debug("Items Total Value: %i", itemsTotalValue)
    LOGGER.debug("Cash Bucket: %s", asdict(cashBucket))
    LOGGER.debug("Pool Bucket: %s", asdict(poolBucket))

    for index, num_user in enumerate(num_users, start=1):
        LOGGER.info("\n")
        LOGGER.info("----------------Scenario %i----------------", index)
        LOGGER.info("Running lottery for %i users:", num_user)
        total_pick_count = 0
        for i in range(1, num_user + 1):
            pick_count = _run_lottery(cashBucket, poolBucket, itemsTotalValue)
            LOGGER.info("User %i: makes %i picks to get all items.", i, pick_count)

            total_pick_count += pick_count

        LOGGER.info(
            "Result: %i users on average need to make %i picks to get all items!",
            num_user,
            int(total_pick_count/num_user),
        )
        LOGGER.info("----------------Scenario %i----------------", index)
