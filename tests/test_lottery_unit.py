from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery,enter_lottery
from scripts.helpful_scripts import (
    get_account,
    LOCAL_DEVELOPMENT_ENVS,
    get_contract,
    fund_with_link,
)
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_DEVELOPMENT_ENVS:
        pytest.skip()
    #skipping the test if not local devlopment network

    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrannce_fee = lottery.getEntrenceFee()
    assert expected_entrance_fee <= entrannce_fee


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_DEVELOPMENT_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": enter_lottery()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_DEVELOPMENT_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act
    lottery.enter({"from": account, "value": enter_lottery()})
    # Assert
    assert lottery.players(0) == account #check if the players are added correctly in array


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_DEVELOPMENT_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": enter_lottery()})
    fund_with_link(lottery)#funding ramdoness with link token
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2#this mean LOTTERY_STATE.CALCULATING_WINNER


def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in LOCAL_DEVELOPMENT_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    value=lottery.getEntrenceFee()
    lottery.enter({"from": account, "value": value})
    lottery.enter({"from": get_account(index=1), "value":value })#using diffrent account indices
    lottery.enter({"from": get_account(index=2), "value":value })#using diffrent account indices
    fund_with_link(lottery)#funding ramdoness with link token
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    transaction = lottery.endLottery({"from": account})
    """
    So here we have problem we need to call fullfill randomness on a development chain
    to keep track when the conract enters the LOTTERY_STATE.CALCULATING_WINNER state we will emit an Event
    
    
    EVENT : chuncks of data that are executed within blockchain and stored there but are not visible to the 
            Smartcontract equialent to print statment 


    to generate event first we will create even type in our contrat at top
    then to emit it we will  add emit function at enf of ecd lottery function


    now in our python test we will call the events attribute witth requested randones with 
    request id whis is emited at thw end ot the function

            
    """
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    '''lets see the contract vrfcoordinator.sol and function of callBackWithRandomness it take 3 parameters
    1->requestid
    2->a random number
    3->the address of the contract that wants ramdomness '''
    # 777 % 3 = 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
    #checking the balance for the winner
