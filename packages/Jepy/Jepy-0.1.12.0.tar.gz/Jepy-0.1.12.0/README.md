# Jepy

A simple Python wrapper to access the Johns Eastern Company API.

## Installation

To get Jepy on your machine, ensure you're running Python 3.7 or higher and use `pip install jepy`.

(Note that it will almost definitely work on Python 3.4+ and will likely work on any version of Python 3 or higher but has not been tested below 3.7).

## Getting Started

Jepy is designed to handle the JWT authentication required by the API for you easily.

Import Jepy and set up the client.

```python
from jepy import Jepy

creds = {'user_id': '0123456789', 'password': '0123456789876543210'}
client = Jepy(**creds)
```

Then use the client you've set up to make calls.

```python
client.detail_by_claim('012345')
```


### Usage

Jepy supports all endpoints of the API. Currently the following functions exist:

* Detail of one claim
  ```python
  client.detail_by_claim('012345')
  ```
* Detail of all claims
  ```python
  client.all_claims_detail()
  ```
* List of claim numbers
  ```python
  client.all_claims()
  ```
* List notes by claim
  ```python
  client.note_by_claim('012345')
  ```
* List checks by claim and/or date
  ```python
  client.check(claim_num = '012345', from_date = '19940206', to_date = '20191016')
  ```

### Interpreting Results

The API answers calls by dumping results into a JSON file with one of three keys. Jepy handles these as follows:
  * Results – Returns a dictionary keyed as 'results', value will be a list of dicts.
  *	Message – Like results, this returns a dictionary keyed as 'message', the value is a message from the server that is not an error. Most often this means no results were found.
  *	Error – Raises an exception. Usually indicates authentication failed, the request syntax is bad, or the server is down.

## Troubleshooting

If you're continuously getting errors, check the status of the server to ensure it is up.

__Simply checking server status does not require authentication__ (and is the only command that does not).

Run `print(Jepy())` with no arguments. You'll either get `JEAPI is up.` or an exception. (Note that if you do try to check status with credentials a la `print(Jepy(**creds))` you will get the object).

If the server is up, your credentials may be invalid and you should contact the [Johns Eastern Helpdesk](https://je.zendesk.com/hc/en-us/requests/new) for assistance.

You can also [click here](https://je-api.com/) to see if the server is up, too.

## Dependencies

Jepy wouldn't be possible without [Requests](https://pypi.org/project/requests/). It is the only non-built-in dependency (and it will automatically install with `pip`).

## Bug Reports/Feature Requests

Please submit a ticket at the [Johns Eastern Helpdesk](https://je.zendesk.com/hc/en-us/requests/new) for feature requests or bug fixes.

## License

This project is licensed under the GNU General Public License v3.0. Please see the [LICENSE.md](LICENSE.md) file for details.
