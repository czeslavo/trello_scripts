create_trello_card
==================
Script allows to add a Trello card based on your .json template to the list on your board.

Installation
===========
```
pip install -r requirements.txt
```

Usage
====
Before using the script you should get your api keys and place them in _config.json_. 

```
create_trello_card.py [-h] [-d DAYS] [-w WEEKS] board list template

Create a Trello card basing on a .json template.

positional arguments:
  board       name of the board
  list        name of the list
  template    name of the .json template file

optional arguments:
  -h, --help  show this help message and exit
  -d DAYS     number of days from now due to the task should be done
              (accumulates with weeks)
  -w WEEKS    number of weeks from now due to task should be done (accumulates
              with days)
```
