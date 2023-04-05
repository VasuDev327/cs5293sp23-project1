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
