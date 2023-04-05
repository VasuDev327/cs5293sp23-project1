## cs5293sp23-project1
## Redactor project - Text Analytics
## Vasu Deva Sai Nadha Reddy Janapala

### The objective of this project is to obfuscate sensitive information, such as names, dates, genders, phone numbers, and addresses, that is present in a given text file. This will involve using various tools and modules, including Spacy and regular expressions, to identify and redact the confidential data.

```
  import spacy
  import re
  from spacy.matcher import Matcher
  import argparse
  import glob
  import sys
  from pathlib import Path
  import json
```

In the main method, we extract the argument parsers to obtain the necessary parameters, which include input, names, dates, genders, phone numbers, and addresses.
 ```
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
    
   ```
   
Starting from this point, I have constructed separate code blocks, which will be executed based on the corresponding command line inputs.
In each block, for each text file, the redacted data information will be collected in the form of object.
