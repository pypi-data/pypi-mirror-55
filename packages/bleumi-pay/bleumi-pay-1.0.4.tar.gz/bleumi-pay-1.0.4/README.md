<img src="https://pay.bleumi.com/wp-content/uploads/2019/04/logo_dark_bleumi_invoice_6797x1122.png" height="30">

# Bleumi Pay SDK for Python

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/bleumi/bleumi-pay-sdk-python/master/LICENSE)

The Bleumi Pay SDK is a one-stop shop to help you integrate ERC-20 payments  into your business or application. The SDK bundles [Bleumi Pay API](https://pay.bleumi.com/docs/#introduction) into one SDK to ease implementation and support.

bleumi-pay-sdk-python is a Python library that provides an interface between your Python application and [Bleumi Pay API](https://pay.bleumi.com/docs/#introduction). This tutorial covers the basics, including examples, needed to use the SDK.

## Getting Started

### Pre-requisites

#### Development Environment

Python 2.7 and 3.4+

#### Obtain An API Key

Bleumi Pay SDK uses API keys to authenticate requests. You can obtain an API key through the [Bleumi Pay Dashboard](https://pay.bleumi.com/app/).

### Install Package

[![pypi (scoped)](https://img.shields.io/pypi/v/bleumi-pay.svg)](https://pypi.org/project/bleumi-pay/)

To install, use `pip` or `easy_install`:

```bash
pip install --upgrade bleumi-pay
```

or

```bash
easy_install --upgrade bleumi-pay
```

Or you can install directly from Github

```sh
pip install git+https://github.com/bleumi/bleumi-pay-sdk-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/bleumi/bleumi-pay-sdk-python.git`)

Then import the package:
```python
import bleumi_pay 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import bleumi_pay
```

### Run Sample Code

The following code generates a wallet to accept payment from the buyer specific for the ECR-20 Token.

```python
from __future__ import print_function
import time
import bleumi_pay
from bleumi_pay.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = bleumi_pay.Configuration()
configuration.api_key['x-api-key'] = '<Your API Key>' # Replace <Your API Key> with your actual API key

# create an instance of the API class
api_instance = bleumi_pay.Erc20PaymentsApi(bleumi_pay.ApiClient(configuration))
body = bleumi_pay.WalletCreateInput() # PaymentCreateInput | 
body.id = '1'
body.buyer_address = bleumi_pay.EthAddress('<BUYER_ADDR>') # Replace <BUYER_ADDR> with the Buyer Address
body.transfer_address = bleumi_pay.EthAddress('<MERCHANT_ADDR>') # Replace <MERCHANT_ADDR> with the Merchant Address
chain = bleumi_pay.EthNetwork.ROPSTEN # Ethereum network in which wallet is to be created.

try:
    # Create an unique wallet address to accept payments for an ERC-20 token from a buyer
    api_response = api_instance.generate_wallet(body, chain=chain)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Erc20PaymentsApi->generate_wallet: %s\n" % e)

```

More examples can be found under each method in [SDK Classes](#sdk-classes) section.

## SDK Classes

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
Erc20PaymentsApi | [**generate_wallet**](docs/Erc20PaymentsApi.md#generate_wallet) | **POST** /v1/payment/eth/wallet | Generates an unique wallet address to accept payments for an ERC-20 token.
Erc20PaymentsApi | [**get_wallet**](docs/Erc20PaymentsApi.md#get_wallet) | **GET** /v1/payment/eth/wallet/{id} | Retrieve a wallet.
Erc20PaymentsApi | [**list_wallets**](docs/Erc20PaymentsApi.md#list_wallets) | **GET** /v1/payment/eth/wallet | Retrieve all wallets.
Erc20PaymentsApi | [**settle_wallet**](docs/Erc20PaymentsApi.md#settle_wallet) | **POST** /v1/payment/eth/wallet/{id}/settle | This method settles a specific amount of an ERC-20 token of a wallet to the transferAddress specified during [Generate Wallet](/docs/Erc20PaymentsApi.md#generatewallet)
Erc20PaymentsApi | [**refund_wallet**](docs/Erc20PaymentsApi.md#refund_wallet) | **POST** /v1/payment/eth/wallet/{id}/refund | This method refunds the balance of an ERC-20 token of a wallet to the buyerAddress specified during [Generate Wallet](/docs/Erc20PaymentsApi.md#generatewallet).
Erc20PaymentsApi | [**get_wallet_operation**](docs/Erc20PaymentsApi.md#get_wallet_operation) | **GET** /v1/payment/eth/wallet/{id}/operation/{txid} | Retrieve an operation of a wallet
Erc20PaymentsApi | [**list_wallet_operations**](docs/Erc20PaymentsApi.md#list_wallet_operations) | **GET** /v1/payment/eth/wallet/{id}/operation | Retrieve all operations of a wallet.

## Documentation For Models

 - [BadRequest](docs/BadRequest.md)
 - [EthAddress](docs/EthAddress.md)
 - [EthNetwork](docs/EthNetwork.md)
 - [PaginatedWalletOperations](docs/PaginatedWalletOperations.md)
 - [PaginatedWallets](docs/PaginatedWallets.md)
 - [Wallet](docs/Wallet.md)
 - [WalletBalance](docs/WalletBalance.md)
 - [WalletCreateInput](docs/WalletCreateInput.md)
 - [WalletCreateOutput](docs/WalletCreateOutput.md)
 - [WalletInputs](docs/WalletInputs.md)
 - [WalletOperation](docs/WalletOperation.md)
 - [WalletOperationInputs](docs/WalletOperationInputs.md)
 - [WalletOperationOutput](docs/WalletOperationOutput.md)
 - [WalletRefundOperationInput](docs/WalletRefundOperationInput.md)
 - [WalletSettleOperationInput](docs/WalletSettleOperationInput.md)

## Limitations

 - [Bleumi Pay API Limits](https://pay.bleumi.com/docs/#api-limits)

## Recommendation

It's recommended to create an instance of `ApiClient` per thread in a multi-threaded environment to avoid any potential issues.

## License

Copyright 2019 Bleumi, Inc.

Code licensed under the [MIT License](LICENSE).
