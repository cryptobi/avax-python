# avax-python

A Python library and utils for the exploration of the [Avalanche AVAX](https://crypto.bi/category/avax/) network.

Includes an implementation of basic AVAX API calls.

## Installation

Clone the git repo and run scripts within the downloaded `avax-python/` subdirectory.


    git clone https://github.com/ojrdevcom/avax-python.git
    cd avax-python/api

If you don't have a `git` client available, you may [download a ZIP archive instead](https://github.com/ojrdevcom/avax-python/archive/master.zip).

[Avalanchego](https://github.com/ava-labs/avalanchego) must be running and listening on `localhost` port `9650`

## Examples

#### Launch a subnet validator:

First, generate user/password credentials for your node. 

Then, enter your username and password on `userpass.txt`.

Then run: 

    python3 send-x-p.py <dest_P_addr> <amount_nAVA> 

to send funds from X-Chain to P-Chain, then

    python3 platform.addDefaultSubnetValidator.py

Done!


#### Export all Blockchains IPC

    python3 ipcs.publishBlockchains.py

## Generate `apimeta.py`

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

## Requirements

If you plan on generating the python files from `api.specification`, then `spec2py.py` requires `TatSu`

    sudo pip install TatSu    

## License

This software released under the MIT license.

See the LICENSE file in this distribution for details.

## Legal Notice

Avalanche and AVAX are registered trademarks of Ava Labs Inc.

*This is not an official Ava Labs project. We are in no way affiliated with Ava Labs.*

This free open source software provided for Avalanche AVAX learning and exploration purposes.
