from brownie import accounts, Lottery, config, network
from scripts.helpful_scripts import get_account, get_contract, adbhut_print,fund_with_link
from web3 import Web3
import time

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    adbhut_print(f"||||lottery contract deployed at: '{lottery.address}'|||","#") 
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_txn = lottery.startLottery({"from": account})
    starting_txn.wait(1)
    adbhut_print("Lottery started","-")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntrenceFee()
    tx = lottery.enter({"from": account, "value": value}) 
    #adbhut_print("Enter ur amount vere:","$")
    #val=input()
    #tx = lottery.enter({"from": account, "value": Web3.toWei(val,"ether")})
    tx.wait(1)
    adbhut_print("You entered the lottery!","+")
    
def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    # then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)#wainting for 3 minutes so that the fulfil randomness is called
    adbhut_print(f"{lottery.recentWinner()} is the new winner!","s")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
   