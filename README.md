# About

Depreciated. Please refer to [this repository][1]

[1]: https://github.com/mondwan/py-tb_attack_list

This is a project for sorting attack list from tb (travian builder)

@author: Mond Wan

# Usage

    # Make sure you get below 2 files at start
    $> ls
    config.ini sort_attack_list.py

    # Put your attack list at the same directory
    $> ls
    config.ini sort_attack_list.py myList.attack
    
    # Define your position in config.ini which will be involved in distance
    # calculation

    # Define your filtering algorithm in config.ini:
    # Currently, it supports filtering by_position only. In other words,
    # records with same position will be deleted

    # Sort list
    $> python sort_attack_list.py myList.attack

    # Get output
    $> ls
    config.ini sort_attack_list.py myList.attack sorted.json

    # Rename the output file
    $> mv sorted.json sorted.attack

    # Place the sorted.attack back to travian builder folder (/sdcard/TravianBuilder)

    # Import this list

    # Enjoy
