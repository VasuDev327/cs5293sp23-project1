# project 1 - Redactor
# Author - Vasu Deva Sai Nadha Reddy Janapala

import spacy
import re
from spacy.matcher import Matcher
import argparse
import glob
import sys
from pathlib import Path
import json
import pyap

# spacy function where every arguments are passed

def spacy_function(arguments):
    inputfile = arguments["input"]
    output: Path = Path(arguments["output"])
    stats_out = arguments["stats"]

    redact_name = arguments["names"] if "names" in arguments else None
    redact_date = arguments["dates"] if "dates" in arguments else None
    redact_phone = arguments["phones"] if "phones" in arguments else None
    redact_gender = arguments["genders"] if "genders" in arguments else None
    redact_address = arguments["address"] if "address" in arguments else None

    txt_files = glob.glob(inputfile[0])
    nlp = spacy.load('en_core_web_sm')

    tracker = []

    # reading the .txt files one after the other
    for file in txt_files:
        file_tracker = {
            "file name": file
        }

        # opening the file
        try:
            with open(file, 'r') as f:
                text = f.read()
            doc = nlp(text)
        except Exception as e:
            print(f"This file {f} cannot be read")
        
        redacted_text = text

        # address
        if redact_address:
            # redact address
            redacted_text = redact_address_fun(redacted_text, file_tracker)

        if redact_name:
            # redact names
            redacted_text = redact_names_fun(redacted_text, doc, file_tracker)

        # genders
        if redact_gender:
            # redact genders
            redacted_text = redact_genders_fun(redacted_text, doc, file_tracker)
            
        # dates
        if redact_date:
            # redact dates
            redacted_text = redact_date_fun(redacted_text, text, file_tracker)
            
        # phone numbers
        if redact_phone:
            # redact phone numbers
            redacted_text = redact_phone_fun(redacted_text, text, file_tracker)

        new_filename = output / f"{file}.redacted"
        with open(new_filename, "w", encoding="utf-8") as f:
            f.write(redacted_text)

        tracker.append(file_tracker)

    # stats
    # stats_formatted = tracker # using tracker variable
    # for track in tracker:
    #     print("file name: ", track["file name"])
    #     print("------------NAMES-----------------")
    #     print("Number of names: ",track["names"]["count"])
    #     for n in track["names"]["values"]:
    #         print("Name:        ", n[0])
    #         print("start index: ", n[1])
    #         print("end index:   ", n[2])
    #     print("------------DATES-----------------")
    #     print("Number of dates: ",track["dates"]["count"])
    #     for d in track["dates"]["values"]:
    #         print("Date:        ", d[0])
    #         print("start index: ", d[1])
    #         print("end index:   ", d[2])
    #     print("------------PHONES-----------------")
    #     print("Number of phone numbers: ",track["phones"]["count"])
    #     for p in track["phones"]["values"]:
    #         print("Phone number: ", p[0])
    #         print("start index:  ", p[1])
    #         print("end index:    ", p[2])
    #     print("------------GENDERS-----------------")
    #     print("Number of names: ",track["genders"]["count"])
    #     for g in track["genders"]["values"]:
    #         print("Gender:      ", g[0])
    #         print("start index: ", g[1])
    #         print("end index:   ", g[2])
    #     print("-------------ADDRESS-----------------")
    #     print("Number of addresses found: ",track["address"]["count"])
    #     for a in track["address"]["values"]:
    #         print("Address:     ", a[0])
    #         print("start index: ", a[1])
    #         print("end index:   ", a[2])
    #     print()
    #     print("--+++++++++---NEW FILE----+++++++++---")
    #     print()
    output_str = ""
    for track in tracker:
        output_str += "file name: " + str(track["file name"]) + "\n"
        output_str += "------------NAMES-----------------\n"
        output_str += "Number of names: " + str(track["names"]["count"]) + "\n"
        for n in track["names"]["values"]:
            output_str += "Name:        " + str(n[0]) + "\n"
            output_str += "start index: " + str(n[1]) + "\n"
            output_str += "end index:   " + str(n[2]) + "\n"
        output_str += "------------DATES-----------------\n"
        output_str += "Number of dates: " + str(track["dates"]["count"]) + "\n"
        for d in track["dates"]["values"]:
            output_str += "Date:        " + str(d[0]) + "\n"
            output_str += "start index: " + str(d[1]) + "\n"
            output_str += "end index:   " + str(d[2]) + "\n"
        output_str += "------------PHONES-----------------\n"
        output_str += "Number of phone numbers: " + str(track["phones"]["count"]) + "\n"
        for p in track["phones"]["values"]:
            output_str += "Phone number: " + str(p[0]) + "\n"
            output_str += "start index:  " + str(p[1]) + "\n"
            output_str += "end index:    " + str(p[2]) + "\n"
        output_str += "------------GENDERS-----------------\n"
        output_str += "Number of genders: " + str(track["genders"]["count"]) + "\n"
        for g in track["genders"]["values"]:
            output_str += "Gender:      " + str(g[0]) + "\n"
            output_str += "start index: " + str(g[1]) + "\n"
            output_str += "end index:   " + str(g[2]) + "\n"
        output_str += "-------------ADDRESS-----------------\n"
        output_str += "Number of addresses found: " + str(track["address"]["count"]) + "\n"
        for a in track["address"]["values"]:
            output_str += "Address:     " + str(a[0]) + "\n"
            output_str += "start index: " + str(a[1]) + "\n"
            output_str += "end index:   " + str(a[2]) + "\n"
        output_str += "\n--+++++++++---NEW FILE----+++++++++---\n\n"
    # print(output_str)

    if stats_out == "stderr":
        print(output_str, file=sys.stderr)
    elif stats_out == "stdout":
        print(output_str, file=sys.stdout)
    else:
        with open(stats_out, "a") as f:
            f.write(output_str)

# function for the names

def redact_names_fun(redacted_text, doc, file_tracker):
    file_tracker["names"] = {
        "count": 0,
        "values": []
    }
    persons = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    updated_persons = []
    for p in persons:
        str_conversion = str(p)
        special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '?', '/', '<', '>', ':', '"', '[', ']', '-', '+', '=', '`', '~', ';']
        for char in str_conversion:
            if char in special_characters:
                updated_persons.append(p)
                char_idx = str_conversion.index(char)
                person_idx = redacted_text.find(str_conversion)
                file_tracker["names"]["count"] += 1
                file_tracker["names"]["values"].append(
                    (redacted_text[person_idx:person_idx+char_idx], person_idx, person_idx+char_idx)
                    )
                redacted_text = redacted_text[:person_idx] + "\u2588" * len(str_conversion[:char_idx]) + redacted_text[char_idx+person_idx:]
                
                break
    persons = [item for item in persons if item not in updated_persons]
    for p in persons:
        str_conversion = str(p)
        person_idx = redacted_text.find(str_conversion)
        file_tracker["names"]["count"] += 1
        file_tracker["names"]["values"].append(
            (redacted_text[person_idx:person_idx+len(str_conversion)], person_idx, person_idx+len(str_conversion))
            )
        redacted_text = redacted_text[:person_idx] + "\u2588" * len(str_conversion) + redacted_text[len(str_conversion)+person_idx:]
    return(redacted_text)

# function for genders

def redact_genders_fun(redacted_text, doc, file_tracker):
    genders = ["he", "him", "his", "she", "her", "hers", "father", "mother", "girl", "boy", "man", "woman",
                "male", "female", "sister", "brother", "men", "women"]
    file_tracker["genders"] = {
        "count": 0,
        "values": []
    }
    for token in doc:
        if token.text.lower() in genders:
            file_tracker["genders"]["count"] += 1
            file_tracker["genders"]["values"].append(
                (token.text, token.idx, token.idx+len(token.text))
            )
            redacted_text = redacted_text[:token.idx] + "\u2588" * len(token.text) + redacted_text[token.idx+len(token.text):]
    return(redacted_text)

# function for dates
def redact_date_fun(redacted_text, text, file_tracker):
    file_tracker["dates"] = {
                "count": 0,
                "values": []
    }
    date_regex = r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(st|nd|rd|th)|\d{2}-\d{2}-\d{4})"
    date_matches = re.findall(date_regex, text)
    for m in date_matches:
        if m[1]:
            start_index = text.find(m[1])
            end_index = start_index+len(m[1])
            file_tracker["dates"]["count"] += 1
            file_tracker["dates"]["values"].append(
                (m[0] + " " + m[1], start_index, end_index)
            )
            redacted_text = redacted_text.replace(m[0] + " " + m[1], "\u2588" * len(m[0] + " " + m[1]))
        else:
            start_index = text.find(m[0])
            end_index = start_index+len(m[0])
            file_tracker["dates"]["count"] += 1
            file_tracker["dates"]["values"].append(
                (m[0], start_index, end_index)
            )
            redacted_text = redacted_text.replace(m[0], "\u2588" * len(m[0]))
    return(redacted_text)

# function for phone numbers
def redact_phone_fun(redacted_text, text, file_tracker):
    file_tracker["phones"] = {
                "count": 0,
                "values": []
    }
    phone_regex = r"\(\d{3}\)\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\+\d{1,2}\(\d{3}\)\d{3}-\d{4}|\+\d{1,2}\d{3}-\d{3}-\d{4}"
    parsed_numbers = re.findall(phone_regex, text)
    for m in parsed_numbers:
        start_index = text.find(m)
        end_index = start_index+len(m)
        file_tracker["phones"]["count"] += 1
        file_tracker["phones"]["values"].append(
            (m, start_index, end_index)
        )
        redacted_text = redacted_text.replace(m, "\u2588" * len(m))
    return(redacted_text)

# function for address
def redact_address_fun(redacted_text, file_tracker):
    file_tracker["address"] = {
                "count": 0,
                "values": []
    }
    addresses = pyap.parse(redacted_text, country='US')

    for address in addresses:
        address_conversion = str(address)
        address_idx = redacted_text.find(address_conversion)
        end_idx = address_idx + len(address_conversion)
        # number_of_characters_redacted = end_idx - address_idx
        file_tracker["address"]["count"] += 1
        file_tracker["address"]["values"].append(
            (address_conversion, address_idx, end_idx)
        )
        redacted_text = redacted_text[:address_idx] + '\u2588' * len(address_conversion) + redacted_text[end_idx:]
        
    return (redacted_text)


# main function

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Redacts sensitive content in a given file.')
    arg_parser.add_argument("--input", required=True, action="append", help="*.txt")
    arg_parser.add_argument('--names', action='store_true', help='redact names')
    arg_parser.add_argument('--dates', action='store_true', help='redact dates')
    arg_parser.add_argument('--phones', action='store_true', help='redact phone numbers')
    arg_parser.add_argument('--genders', action='store_true', help='redact genders')
    arg_parser.add_argument('--address', action='store_true', help='redact addresses')
    arg_parser.add_argument('--output', type=str, help='output directory', required=True)
    arg_parser.add_argument('--stats', type=str, default='stdout', help='output statistics to stdout or stderr')

    args = arg_parser.parse_args()

    # trying to read the current working directory for the output, 
    # where we can create a named folder called 'files'

    if args.output:
        cwd = Path.cwd()
        out_folder: Path = cwd / args.output

        if not out_folder.exists():
            out_folder.mkdir(parents=True)

    if args.input:
        spacy_function(vars(args))