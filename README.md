# avax-python

A Python library and utils for the exploration of the [Avalanche AVAX](https://crypto.bi/category/avax/) network.

Includes an implementation of basic AVAX API calls, offline wallet generator and other utilities.


## Documentation and Tutorials

* [avax-python – Python utils for AVAX cryptocurrency and Avalanche network exploration](https://crypto.bi/avax-python/)
* [avax-python Avalanche AVAX Network Listener](https://crypto.bi/avalanche-network-listener/) - Capture blocks, vertices and transactions from the Avalanche network and into JSON or other custom format
* [avax-python Implementation Notes](https://crypto.bi/avax-python-notes/)
* [avax-python Network Message Pipeline](https://crypto.bi/avax-python-messages/)
* [Scrape AVAX network peers using avax-python](https://crypto.bi/list-avax-peers/)
* [Generate AVAX addresses and keys from a mnemonic phrase in Python](https://crypto.bi/avax-mnemonic-python/)

Visit the [crypto.bi AVAX section](https://crypto.bi/category/avax/) for up to date samples and tutorials.


## Requirements

    sudo pip3 install numpy
    sudo pip3 install pyopenssl
    sudo pip3 install cryptography
    sudo pip3 install asn1crypto
    sudo pip3 install plyvel

If you plan on generating the python files from `api.specification`, then `spec2py.py` requires `TatSu`

    sudo pip install TatSu    

Other required libraries are embedded in this project, under the `3rdparty` subdirectory. You can also install these using pip, if you wish to run online:

    sudo pip install mnemonic
    sudo pip install py-crypto-hd-wallet
    sudo pip install bip-utils
    sudo pip install pysha3

We've embedded some of the security-related libs so that the project can run offline as much as possible, if you choose to.

Specifically, this project includes code from the following libraries under the `3rdparty/` subdirectory:

* [mnemonic](https://github.com/trezor/python-mnemonic) 
* [py_crypto_hd_wallet](https://github.com/ebellocchia/py_crypto_hd_wallet) 
* [bip_utils](https://github.com/ebellocchia/bip_utils) 
* [pysha3](https://github.com/tiran/pysha3) 
* [cb58ref](https://github.com/moreati/cb58ref)
* [bech32 Encoding under wallet/bech32](https://github.com/sipa/bech32)


## Installation

`avax-python` runs from its downloaded location.

If a `git` client is not available, then you may [download a ZIP archive instead](https://github.com/ojrdevcom/avax-python/archive/master.zip).

For the online functions, [Avalanchego](https://github.com/ava-labs/avalanchego) must be running and listening on `localhost` port `9650`

To use the library and utils, just :

* Clone the git repo 
* Set the environment 
* Build and install `pysha3`

In short:

    git clone https://github.com/ojrdevcom/avax-python.git
    cd avax-python/
    . setenv.sh


### pysha3 Build

For this step you'll need the Python development headers to be installed. 

E.g. on Ubuntu do :

    sudo apt-get install python3-dev

Then do:

    cd 3rdparty/pysha3
    python3 setup.py build
    sudo python3 setup.py install

## Offline Scripts

Scripts under the `offline/` directory at the project root do not make use of the network.

If you want to be extra safe and perform some actions in an air-gapped environment, then we've grouped the offline scripts inside this directory.

There shouldn't be any network activity coming from any of the scripts in the `offline/` subdirectory. 

## Examples

Here are some quick examples of `avax-python` usage. For more tutorials and complete documentation, visit [crypto.bi](https://crypto.bi/category/avax/)


### List AVAX addresses from a mnemonic phrase [Offline]

    python3 offline/wallet/addresses_from_mnemonic.py shoulder man day worry sweet clip outdoor little matter interest option eyebrow asset visa snake find toddler labor puzzle danger quit secret flip foil

    # Sample Output:
    X-avax1qur7n8zupwtwd6g5xpepmt6cm75595lrkp7msg
    X-avax1f3uaym89er87f2dm3h4wdftp3yut9p8qzu8zf5
    X-avax1mhvz53e5zhffu9ydekuk83wwfg3dzce6sdut2h
    X-avax18pkfangejtdxnxsn0r8ax8fr264ysv0tfkukrs
    X-avax1v0zdtnay2ef6m48f2jmp6dzhfcql2wqdq5z8am
    X-avax1hvyfx0468vmd2eqsaxqe0dackkr4y8tqh83qxl
    X-avax1k2wrx2r4rveyfp0f2ymagce6gfvzjht6rn0ua2
    X-avax1s3d9v2v0sdsgnvuq0kfkfgr92ckrgzw8xsc6tf
    X-avax1n6vsqv07cjgy8gnn9gmxghp6f6xkyrlkvrrcuu
    X-avax1jxeey8hhsp2vfpu7k2p63kpprflv9tfl9pgg85

### Launch a subnet validator [Online]

First, generate user/password credentials for your node. 

Then, enter your username and password into `userpass.txt`.

Then run: 

    python3 send-x-p.py <dest_P_addr> <amount_nAVA> 

to send funds from X-Chain to P-Chain, then

    python3 platform.addDefaultSubnetValidator.py

Done!


### Export all Blockchains via IPC [Online]

    python3 ipcs.publishBlockchains.py

## Generate `apimeta.py` [Offline]

If you update the `api.specification` file, then you must regenerate the API metainformation file `apimeta.py`

To recreate it, run generate_api.py:

```
python3 generate_api.py
```

## Implement the AVA API in Any Language

The `spec2py.py` script reads the API specification in `api.specification`, the grammar in `api.tatsu` and generates an AST which can be
used to implement the API in any language.

If you need to customize the API, the `api.specification` file format is very simple. 

* An API endpoint begins a new section. Leave a blank line after the endpoint:/url/here line.
* See the provided `api.specification` file and follow the same syntax for function definitions.
* Functions can be defined over several lines. Don't leave blank lines within a function definition.
* Leave one blank line after each function definition.

To customize the generator grammar, see the [Tatsu documentation](https://tatsu.readthedocs.io/en/stable/syntax.html) 

Note that changing the grammar will require changes to `spec2py.py`. The generator uses hard coded offsets which will break if the grammar is modified.

## List AVAX Network Nodes

To list AVAX network peers received via P2P communications, run:

    python3 bin/list_peers.py

What this script does is install a custom network handler which prints out the content of PeerList messages.

## Experimental AVAX Network Node

To run an experimental, passive non-validating node that listens to events on the AVAX network, run :

    python3 bin/avax.py

This is a work in progress.  

## Notes

Where possible, the python sources follow the same directory structure as the [reference Go implementation](https://github.com/ava-labs/avalanchego).

It isn't always possible to keep the code exactly the same, because Go and Python differ in many ways. For example, Go names which are defined in one file and are automatically available across a package in multiple sources, must be explicitly part of some Python module. This leads to some apparent namespace redundancy, like `genesis.genesis.FromConfig(...)`. You can often mitigate this by working the import statement in Python, e.g. `from genesis import genesis`.

We've tried to make the code as intuitive as possible for those familiar with the Go implementation. Just keep in mind it isn't always possible.


## License

This software released under the MIT License.

See the LICENSE file in this distribution for details.

### Embedded Software Licenses

This project includes source code from :

[avalanchego](https://github.com/ava-labs/avalanchego) : BSD-3-Clause License

[mnemonic](https://github.com/trezor/python-mnemonic) : MIT License

[py_crypto_hd_wallet](https://github.com/ebellocchia/py_crypto_hd_wallet) : MIT License

[bip_utils](https://github.com/ebellocchia/bip_utils) : MIT License

[pysha3](https://github.com/tiran/pysha3) : PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2

[cb58ref](https://github.com/moreati/cb58ref) : MIT License

[bech32 Encoding under wallet/bech32](https://github.com/sipa/bech32) : by Pieter Wuille, License unspecified, MIT License Presumed


## Legal Notices

Avalanche and AVAX are registered trademarks of Ava Labs Inc.

*This is not an official Ava Labs project. We are in no way affiliated with Ava Labs.*

This free open source software provided for Avalanche AVAX learning and exploration purposes. No warranty is offered, express or implied, as to the suitability or correctness of this code. **Cryptocurrency transactions are irreversible.** We are not responsible for losses incurred during the use of this software.


## Sponsor

Development of `avax-python` is partly sponsored by **[crypto.bi](https://crypto.bi/)**

Please help support this Open Source project!

Donate to `X-avax1qr6yzjykcjmeflztsgv6y88dl0xnlel3chs3r4`




---

*From Snowflake to Avalanche. Per consensum ad astra.*