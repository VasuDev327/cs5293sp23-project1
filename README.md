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
I have used spacy module for the function blocks *names, genders, address* and regular expression for remaining function blocks.

Used the following command to run the code
![image](https://user-images.githubusercontent.com/102677891/229963600-9e045a49-103e-4ccd-9a92-8745c09941c0.png)

# Stats output
After that as the output is the object format: It looks as follows:
![image](https://user-images.githubusercontent.com/102677891/229963677-26730dac-b84e-45eb-b697-dd7ec697dc9c.png)

Its format is the name of the file, followed by that it has the count, values in the form of list[(name/date/gender/phone/address, start_index, end_index)]

## Video recording
I have added the video file under the name **pipenv run output video.mp4** which shows the run of this code(redactor.py)

## Bug:
Despite its usefulness, Spacy's precision may not be sufficient for certain tasks. To overcome this, I have incorporated regular expressions in my code. However, even with this approach, I am still encountering issues with partial matches in addresses. To tackle this challenge, I have utilized both Spacy's GEO and ADDRESS modules, as well as the re module to identify ZIP codes.

## Assumptions:
```
genders = ["he", "him", "his", "she", "her", "hers", "father", "mother", "girl", "boy", "man", "woman",
                "male", "female", "sister", "brother", "men", "women"]
```

**1.txt, 2.txt, 5.txt, 6.txt, 7.txt are the inputfiles I have used in this code.**
**The files folder is the output file folder where the redacted format will be available.**

## test.py
Instead of individual modules, I have added all the functions in the same test file.

Here is the testing result which was successful for all the test runs. The output is shown as below:
![image](https://user-images.githubusercontent.com/102677891/229964100-f226f781-cc13-44c2-9cd7-0ac82dc0d9f8.png)
