# -*- coding: utf-8 -*-

"""rellax.rellax: provides entry point main()."""

__version__ = "0.1.rc1"

import sys
import argparse
import inquirer
import prompt_toolkit

from os import getenv
from pathlib import Path
from json import loads, dumps
from datetime import datetime
from queue import PriorityQueue, Empty

from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from colored import fg, bg, attr

ENGAGEMENT_FILE = "rellax.json"
HOME_DIR = getenv("HOME")


def msg(text):
    '''Formalizes default message string for UI'''
    return "[+] {0}".format(text)

def get_date_timestamp():
    '''Helper function to create uniform date time string'''
    date_fmt = "%Y%m%d %H%M"
    return datetime.now().strftime(date_fmt)

def colorize_question(text):
    return "{0}{1}{2}".format(fg('white'), text, attr('reset'))

def sorted_questions_and_answers(data_store):
    sorting_queue = PriorityQueue()

    question_pairs = data_store['qna']     
    for question_dict in question_pairs:
        sorting_queue.put((question_dict['question']['date'], question_dict))

    while True:
        try:
            i = sorting_queue.get(block=False)
            question_dict = i[1]
            print("Q : {0}".format(question_dict['question']['text']))
            if 'answers' in question_dict.keys():
                for answer in question_dict['answers']:
                    print(" A : {0}".format(answer['text']))
            print("")

        except Empty:
            break

def list_questions(data_store):
    '''Lists questions from data store'''
    questions = {q['question']['date']: q['question']['text']
                 for q in data_store['qna']
                 if 'qna' in data_store.keys()
                 if 'question' in q.keys()
                 if 'date' in q['question'].keys()
                 if 'text' in q['question'].keys()}

    return questions

def print_sorted(questions):
    ''' Prints list of questions sorted by date'''
    for date in sorted(questions):
        print(colorize_question(questions[date].capitalize()))

def get_user_file_history():
    ''' Returns the file history object for the user to support autosuggesstion'''
    # File history file for this user
    return  FileHistory(str(Path(getenv("HOME")).joinpath('qna-hist.txt')))
        

def load_engagement_json(home_dir):
    '''Loads the json data store file associated with the user of this script'''
    search_path = Path(home_dir).joinpath(ENGAGEMENT_FILE)
    if search_path.exists():
        return loads(open(str(search_path), 'r').read(-1))

def write_json_store(obj):
    '''Overwrites json_data store with all new data'''
    with open(str(Path(HOME_DIR).joinpath(ENGAGEMENT_FILE)), 'w') as eng_file:
        eng_file.write(dumps(obj, indent=4))

def add_question(_):
    '''Adds a question to the data store'''
    # TODO: Change to python-editor library module

    question = prompt_toolkit.prompt('> ', vi_mode=True)
    # TODO: Validate that question is actually a question. Or atleast ends in with a ?
    if not question.endswith("?"):
        question = "{0}?".format(question)

    # create a question object
    q = {"question":
         {"text": question,
             "date": get_date_timestamp()
          }
         }

    # load the data store
    json_data_store = load_engagement_json(getenv("HOME"))

    # TODO: Do a fuzzy search to see if question already exists
    json_data_store['qna'].append(q)
    write_json_store(json_data_store)


def create_engagement_json(_):
    '''Initializes a new data store with 
        engagement information'''

    # File history file for this user
    file_history = get_user_file_history()

    name = prompt_toolkit.prompt('Name of Engagement : ',
                  history=file_history,
                  auto_suggest=AutoSuggestFromHistory())

    # create a new blank engament json data file store with only a new name
    obj = {"engagement": name,
           "qna": []
           }

    write_json_store(obj)


def create_answer_object(answer):
    
    return {"text" : answer , 
     "date" : get_date_timestamp()}

def answer_question(_):
    '''Adds an answer to a given question'''
    # Locate engagement json file in HOME directory
    json_data_store = load_engagement_json(getenv("HOME"))

    #get a list of all submitted questions
    questions = list_questions(json_data_store)

    #build list of choices
    choices = [
        inquirer.List('chosen',
                      message="Provide answer for",
                      choices= [q for q in questions.values()]
                      ),
    ]
    #Get choice from user
    choice = inquirer.prompt(choices)

    # File history file for this user
    file_history = get_user_file_history()

    answer = prompt_toolkit.prompt('Answer : ', vi_mode=True,
                  history=file_history,
                  auto_suggest=AutoSuggestFromHistory())

    answer_obj = create_answer_object(answer)

    #update data_store with answer
    print("Saving answer ({0}) to question ({1})".format(answer, choice['chosen']))

    print("!!!! Not actually saved")
    #search data store to add answer in correct place
    target_question = [q for q in json_data_store['qna'] if q['question']['text'] == choice['chosen']]

    #if for some reason there are more than or less than one question matching then throw an error
    if len(target_question) != 1:
        raise ValueError("Unable to locate target question")
    
    #If there already exists an answer then just append a new one
    if 'answers' in target_question[0].keys():
        target_question[0]['answers'].append(answer_obj)
    else:
        target_question[0]['answers'] = [answer_obj]

    #write the object back to the file system
    write_json_store(json_data_store)

def search_questions(args):
    '''Searches through data store for a particular question'''
    found = False

    # Locate engagement json file in HOME directory
    json_data_store = load_engagement_json(getenv("HOME"))

    questions = list_questions(json_data_store)
    for date, question in questions.items():
        if args.keyword in question:
            found = True
            print(question)
    
    if not found:
        print(msg("No Question found using keyword {0}".format(args.keyword)))



def main():
    parser = argparse.ArgumentParser(
        description="Command line Knowledgebase tracker")
    subparsers = parser.add_subparsers()
    init_group = subparsers.add_parser(
        'init', description="Initialize json datastore")
    add_group = subparsers.add_parser('add', description="Add a new question")
    search_group = subparsers.add_parser(
        'search', description="Search questions")
    answer_group = subparsers.add_parser('ans', description="Answer a question")

    # init_group arguments
    init_group.set_defaults(func=create_engagement_json)

    # add group arguments
    add_group.set_defaults(func=add_question)

    # search group arguments
    search_group.set_defaults(func=search_questions)
    search_group.add_argument("keyword", help="Keyword(s) to search for")

    # answer group arguments
    answer_group.set_defaults(func=answer_question)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
        sys.exit()

    # Locate engagement json file in HOME directory
    json_data_store = load_engagement_json(getenv("HOME"))

    if not json_data_store:
        print(msg("You must run init command first"))
        sys.exit(1)

    # default action is to list all questions in store
    questions = list_questions(json_data_store)
    if questions:
        print(msg("All current questions :\n"))

        sorted_questions_and_answers(json_data_store)

    else:
        print(msg("No Knowledge found. Perhaps .. Idunno.. add some?"))
