from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_DEVELOPMENT_ENVS,
    get_account,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_DEVELOPMENT_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntrenceFee()})
    lottery.enter({"from": account, "value": lottery.getEntrenceFee()})
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0