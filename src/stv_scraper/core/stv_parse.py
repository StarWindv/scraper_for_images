# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)


import argparse

from stv_scraper.utils.change_text import parse_text


def get_user_input(param_name, prompt):
    value = input(f"{prompt}")
    return value if value else None


def stv_parse():
    parser = argparse.ArgumentParser(description="\n=========================Options=========================")
    help_text = parse_text()
    parser.add_argument('-k', '--keyword', type=str, help=help_text[0])
    parser.add_argument('-pg', '--page', type=int, help=help_text[1])
    parser.add_argument('-r', '--remove', action='store_true', help=help_text[2])
    parser.add_argument('-w', '--window', type=int, help=help_text[3])
    parser.add_argument('-l', '--lines', type=int, help=help_text[4])
    parser.add_argument('-t', '--time', type=int, help=help_text[5])
    parser.add_argument('-pl', '--plate', type=int, help=help_text[6])
    parser.add_argument('-pt', '--path', type=str, help=help_text[7])
    parser.add_argument('--license', action='store_true', help=help_text[8])
    parser.add_argument('-v', '--version', action='store_true', help=help_text[9])
    args = parser.parse_args()
    return args