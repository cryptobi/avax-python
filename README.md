# ava-python

A Python implementation of the [AVA API](https://docs.ava.network/v1.0/en/api/intro-apis/)

This lib stemmed from utility scripts I used while developing [AVA.DOG](https://AVA.DOG)

License: MIT 

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

## Yo

This is Bacon, the [AVA DOG](https://AVA.DOG):

![Bacon the AVA DOG](https://ava.dog/wp-content/themes/avaexplorer/assets/images/bacon2-cartoon-300px-h.png "Bacon, the AVA DOG")

