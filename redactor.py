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
            "name": file
        }

        # opening the file
        try:
            with open(file, 'r') as f:
                text = f.read()
            doc = nlp(text)
        except Exception as e:
            print(f"This file {f} cannot be read")
        
        redacted_text = text
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

        # address
        if redact_address:
            # redact address
            redacted_text = redact_address_fun(redacted_text, doc, file_tracker, text)
        
        new_filename = output / f"{file}.redacted"
        with open(new_filename, "w", encoding="utf-8") as f:
            f.write(redacted_text)

        tracker.append(file_tracker)

    # stats
    stats_formatted = tracker # using tracker variable
    
    if stats_out == "stderr":
        print(stats_formatted, file=sys.stderr)
    if stats_out == "stdout":
        print(stats_formatted, file=sys.stdout)
    else:
        with open(stats_out, "a") as f:
            f.write(json.dumps(stats_formatted))
            f.write("\n")

# function for the names

def redact_names_fun(redacted_text, doc, file_tracker):
    file_tracker["names"] = {
        "count": 0,
        "values": []
    }
    persons = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    for person in persons:
        first_name = ""
        last_name = ""
        for token in person:
            if token.is_alpha:
                redacted_text = redacted_text[:token.idx] + \
                        "\u2588" * len(token.text) + redacted_text[token.idx+len(token.text):]
                file_tracker["names"]["count"] += 1
                file_tracker["names"]["values"].append(
                    (token.text, token.idx, token.idx+len(token.text))
                )

                if first_name:
                    break
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
def redact_address_fun(redacted_text, doc, file_tracker, text):
    file_tracker["address"] = {
                "count": 0,
                "values": []
    }
    for ent in doc.ents:
        if ent.label_ == "GPE":
            start_index = text.find(ent.text)
            end_index = start_index+len(ent.text)
            file_tracker["address"]["count"] += 1
            file_tracker["address"]["values"].append(
                (ent.text, start_index, end_index)
            )
            redacted_text = redacted_text.replace(ent.text, "\u2588" * len(ent.text)) 
    
    for ent in doc.ents:
        if ent.label_ == "ADDRESS":
            start_index = text.find(ent.text)
            end_index = start_index+len(ent.text)
            file_tracker["address"]["count"] += 1
            file_tracker["address"]["values"].append(
                (ent.text, start_index, end_index)
            )
            redacted_text = redacted_text.replace(ent.text, "\u2588" * len(ent.text))
    
    zipcode_pattern = r"^\d{5}|\b\d{5}\b|\d{5}$"
    find_pattern = re.findall(zipcode_pattern, text)
    for p in find_pattern:
        start_index = text.find(p)
        end_index = start_index+len(p)
        file_tracker["address"]["count"] += 1
        file_tracker["address"]["values"].append(
            (p, start_index, end_index)
        )
        redacted_text = redacted_text.replace(p, "\u2588" * len(p))
    return(redacted_text)


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