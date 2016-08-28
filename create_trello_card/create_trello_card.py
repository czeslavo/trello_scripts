from trello import TrelloClient

import json
import argparse
from datetime import date, timedelta


def parse_args():
    parser = argparse.ArgumentParser(description='Create a Trello card basing on a .json template.')
    parser.add_argument('board', type=str, help='name of the board')
    parser.add_argument('list', type=str, help='name of the list')
    parser.add_argument('template', type=str, help='name of the .json template file')
    parser.add_argument('-d', dest='days', type=int, default=0, choices=range(1, 7), help='number of days from now due to the task should be done (accumulates with weeks)')
    parser.add_argument('-w', dest='weeks', type=int, default=0, choices=range(1, 12), help='number of weeks from now due to task should be done (accumulates with days)')
    
    return parser.parse_args()


def get_client():
    with open('config.json') as configf:
        config = json.loads(configf.read())
        return TrelloClient(
            api_key = config['api_key'],
            api_secret = config['api_secret'],
            token = config['token'],
            token_secret = config['token_secret']
            )


def get_board(trello_client, board_name):
    for board in trello_client.list_boards():
        if board.name == board_name:
            return board
    raise Exception("No requested board in your boards: " + board_name)


def get_list(board, list_name):
    for lst in board.all_lists():
        if lst.name == list_name:
            return lst
    raise Exception("No requested list [" + list_name + " in " + board.name) 


def get_member_id(board, member_name):
    for member in board.all_members():
        if member.full_name == member_name:
            print("member: " + member.id)
            return member.id
            
    raise Exception('Invalid member name: ' + member_name)


def add_card(lst, card_json, due):
    labels = []
    try:
        labels = [get_label(lst.board, label_name) for label_name in card_json['labels']] or []
    except KeyError as e:
        pass

    card = lst.add_card(card_json['name'], card_json['desc'], labels, due) 
    try:
        for checklist in card_json['checklists']:
            card.add_checklist(checklist['name'], checklist['elements'])
    except KeyError as e:
        pass

    return card


def move_member_last_in_queue(template_filename):
    with open(template_filename) as template_file:
        jsonobj = json.loads(template_file.read())
        queue = jsonobj['members_queue']
        queue = queue[1:] + [queue[0]]
        jsonobj['members_queue'] = queue
    with open(template_filename, 'w') as template_file:
        json.dump(jsonobj, template_file, indent=4)


def get_label(board, label_name):
    for label in board.get_labels():
        if label.name == label_name:
            return label
    print("No given label in your board: " + label_name)
    return None


if __name__ == "__main__":
    args = parse_args()
    
    desired_board = args.board
    desired_list = args.list
    desired_card = args.template

    client = get_client()

    board = get_board(client, desired_board)
    lst = get_list(board, desired_list)
    card = None

    with open(desired_card) as jsonf:
        jsonobj = json.loads(jsonf.read())
        due = date.today() + timedelta(days=args.days, weeks=args.weeks)
        card = add_card(lst, jsonobj, str(due))
        try:
            card.assign(get_member_id(board, jsonobj['members_queue'][0]))
            move_member_last_in_queue(desired_card)
        except:
            pass

    if card:
        card.fetch()
        print("Success: added card with id " + card.id + "[ " + card.short_url + " ]")
