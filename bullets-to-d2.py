#!/usr/bin/env python3
import sys
from termcolor import colored
import re

def usage():
    print_info("Usage: " + sys.argv[0] + " <filename>")
def print_error(str):
    print(colored("[-] "+ str,"red"))
    sys.exit()
def read_file(fileName):
    return [line.rstrip('\n') for line in open(fileName)]
def write_d2(filename, lines):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")

def get_title(title):
    # if format is [[this-this this|title]] extract title
    match_title = re.search(r'\|([^|\]]+)', title)
    if match_title:
        return "\"{}\"".format(match_title.group(1))
    title = title.replace("\"", "\\\"")
    title = "\"{}\"".format(title)
    return title    

def find_tab(lines):
    # find out if bullet points are tabbed with a tab or space
    # and how many tabs and/or spaces
    for line in lines:
        if line[0] == " ":
            # We have spaces!
            point = line.find("-")
            tab = line[:point]
            return tab
        if line[0] == "\t":
            # We have tabs!
            point = line.find("-")
            tab = line[:point]
            return tab
    return False

def to_dict(content_lines, tab):
    # return dictionary based on bullet point parsing
    out = {}
    entries = []
    latest = {}
    for line in content_lines:
        # verify if it is tabbed
        if line.startswith(tab):
            # indentention here, how many?
            indent = line[:line.find("-")]
            n_tabs = int(len(indent) / len(tab))
            title = get_title(line[line.find("-")+2:])
            title_up = latest[n_tabs - 1]

            latest[n_tabs] = title
            entry = {
                    "title": title,
                    "n_tabs": n_tabs,
                    "title_up": title_up
                    }
            entries.append(entry)
        else:
            # first lines, without indentation
            title = get_title(line[line.find("-")+2:])
            latest[0] = title
            entry = {
                    "title": title,
                    "n_tabs": 0,
                    "title_up": False
                    }
            entries.append(entry)
    return entries

def to_d2(entries):
    # dict to D2 syntax
    output = []
    for entry in entries:
        title = entry["title"]
        title_up = entry["title_up"]
        if entry["n_tabs"] == 0:
            output.append(title)
        else:
            d2_line = "{} -> {}".format(title_up, title)
            output.append(d2_line)

    for l in output:
        print(l)
    return output

def main():
    # bullet points -> dictionary -> D2
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    filename = sys.argv[1]
    content_lines = read_file(filename)

    tab = find_tab(content_lines)
    if not tab:
        print_error("Cannot find tab pattern")
    dict_list = to_dict(content_lines, tab)
    if not dict_list:
        print_error("Error building the intermediate python dictionary")
    d2_lines = to_d2(dict_list)
    write_d2(filename + ".d2", d2_lines)

if __name__ == "__main__":
    main()
