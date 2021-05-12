# Networking

avax-python attempts to preserve the same overall structure of the avalanchego implementation

But, since we're not a reference implementation, we can implement experimental stuff like custom protocol handlers that are non-conformant to Avalanche standards.

## Examples

We've implemented a few experimental programs using avax-python. 

See the following articles for details:

* [avax-python Network Message Pipeline](https://crypto.bi/avax-python-messages/) - How network messages are processed by avax-python
* [Scrape AVAX network peers using avax-python](https://crypto.bi/list-avax-peers/) - A simple network message handler which prints out Avalanche peer IP's and ports
* [avax-python Avalanche AVAX Network Listener](https://crypto.bi/avalanche-network-listener/) - Capture blocks, vertices and transactions from the Avalanche network and into JSON or other custom format