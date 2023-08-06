# Belvo Python SDK

**Documentation**: <https://belvo-finance.github.io/belvo-python/>

**Developers portal**: <https://developers.belvo.co> 

.. comment: split here

## :clipboard: Requirements
* Python 3.6+

## :rocket: Getting started

Install using `pip`:
```
$ pip install belvo-python
```
---

## Example
```python

from pprint import pprint

from belvo.client import Client

# Login to Belvo API
client = Client("my-secret-key-id", "my-secret-key", "https://api.belvo.co")

# Register a link 
link = client.Links.create(
    institution="banamex",
    username="johndoe",
    password="supersecret"
)

# Get all accounts
client.Accounts.create(link["id"])

# Pretty print all checking accounts
for account in client.Accounts.list(type="checking"):
    pprint(account)
```
