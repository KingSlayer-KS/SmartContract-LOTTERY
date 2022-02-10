from brownie import(
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface
)

DECIMALS = 18
INITIALANSWER = 200000000000

FORKED_ENVS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_DEVELOPMENT_ENVS = ["development", "Ganache-local"]

contract_to_mock =  {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_DEVELOPMENT_ENVS
        or network.show_active() in FORKED_ENVS
    ):
        return accounts[0]
    # if nothing above 3 statmens is true the below one will be done
    return accounts.add(config["Wallets"]["from_key"])

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_DEVELOPMENT_ENVS:
        if len(contract_type) <= 0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract

def deploy_mock():
    
    adbhut_print(f"active network is {network.show_active()}","=")
    adbhut_print("Deploying MOCKS.....!!","?")
    MockV3Aggregator.deploy(
        DECIMALS,  # Parameter that constructor takes this is _decimals
        INITIALANSWER,  # Parameter that constructor takes _initialAnswer
        {"from": get_account()},  # since it is state change type
    )
    link_token = LinkToken.deploy({"from": get_account()})#deploying contract of link token
    VRFCoordinatorMock.deploy(link_token.address,{"from":get_account()})
    #deploying contract of VRFCoordinatorMock, tales link token address as input to contract 
    adbhut_print("|||||||mock deployed|||||||","=")

def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    #OR
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    #before doing this make sure to copy pasete the link token interface file into your interfaces folder
    tx.wait(1)
    adbhut_print("Contract Funded!")
    return tx

def adbhut_print(input_str,second_char="="):
    char_pairs=int((len(input_str))/2)
    if (len(input_str))%2==0:
        char_len=("="+second_char)*char_pairs
        print(f"{char_len}\n{input_str}\n{char_len}")
    else:
        char_len=("="+second_char)*char_pairs
        print(f"{char_len}=\n{input_str}\n{char_len}=")

