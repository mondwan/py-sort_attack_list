"""
- `File`: sort_attack_list.py

- `Author`: Me

- `Email`: 0

- `Github`: 0

- `Description`: Sort attack list from travian builder
"""

import sys
import argparse
import json as JSON
import ConfigParser
import math
import io

CONFIG_PATH = 'config.ini'
OUTPUT_PATH = 'sorted.json'

def initializeParser():
    """
    Helper method returns a parser for us to parsing command line argument

    Return:

    - `argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(description='Sort attack list from travian builder')

    parser.add_argument(
        'inputList',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )

    return parser

def readFromJson(fp):
    """
    Helper method return a JSON object by reading from a given f

    Parameters:

    - `f`: file

    Return:

    - json
    """
    ret = None
    with fp as f:
        ret = JSON.load(f)

    return ret

def readFromConfig():
    """
    Helper method reads configuration from config.ini

    Return:

    - `ConfigParser.RawConfigParser`
    """
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_PATH)

    return config

def sort_attack_list_by_distance(commands, config):
    """
    Helper method sorts given commands by distance compared to given config

    Parameters:

    - `commands` : Array of objects

        .. code-block:: py

            {
                "arriveDate":"2015-05-09T00:37:54",
                "attackTimes":1,
                "attackTimes_Limit":0,
                "attack_interval_max":4,
                "attack_interval_min":1,
                "bContinuous":false,
                "bPause":false,
                "bWithHero":false,
                "backDate":"2015-05-09T02:16:51",
                "decrease":0.0,
                "decrease_max":0.0,
                "error":"",
                "rand":2,
                "send_number":0,
                "startTime":"2015-05-08T22:58:57",
                "state":5,
                "target":"OMG",
                "target_x":76,
                "target_y":77,
                "troops":[ 0, 5, 0, 0, 0, 0, 0, 0, 0, 0 ],
                "troops_max":[ 0, 5, 0, 0, 0, 0, 0, 0, 0, 0 ],
                "type":3 
            }

    - `config`: ConfigParser.RawConfigParser

    Return:

    - `Array of objects`
    """
    # Cast our position to integer
    myX = int(config.get('position', 'x'))
    myY = int(config.get('position', 'y'))

    for record in commands:
        # Cast target position to integer
        targetX = int(record['target_x'])
        targetY = int(record['target_y'])
        distance = math.hypot(targetX - myX, targetY - myY)
        distance = round(distance, 2)
        record['distance'] = distance

    ret = sorted(commands, key=lambda record: record['distance'])

    return ret


def filter_attack_list(commands, config):
    """
    Filter command in commands accordingly depends on given config

    Parameters:

    - `commands`: Array of Object

    - `config`: ConfigParser.RawConfigParser

    Return:

    - `Array of objects`
    """
    ret = []

    isFilterByPosition = config.get('filter', 'by_position')

    if isFilterByPosition:
        positions = []
        for record in commands:
            # Cast string to int
            targetX = int(record['target_x'])
            targetY = int(record['target_y'])
            position = (targetX, targetY)

            # Skip this record
            if position in positions:
                continue

            positions.append(position)
            ret.append(record)
    else:
        ret = commands

    return ret


def main(argv=None):
    """
    Main entry

    Parameters:

    - `argv`: Array of string
    """

    # Get system command line arguments if there is no given argv to override
    if argv is None:
        argv = sys.argv[1:]

    parser = initializeParser()
    arg = parser.parse_args(argv)
    
    # Get the json list
    json = readFromJson(arg.inputList)

    # Get configurtaion from config.ini
    config = readFromConfig()

    # Objects in the commands are the one we are going to sort
    commands = json['commands']

    # Sort by distance
    ret = sort_attack_list_by_distance(commands, config)

    # Filter if required
    ret = filter_attack_list(commands, config)
    
    # Write to a file
    json['commands'] = ret

    with io.open(OUTPUT_PATH, 'w', encoding='utf8') as f:
        data = JSON.dumps(json, ensure_ascii=False)
        f.write(unicode(data))

# main()
if __name__ == "__main__":
    main()
