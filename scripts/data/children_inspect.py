"""Inspect public Ipsos parenthood tables without inventing joint cells.

Usage: python scripts/data/children_inspect.py path/to/general-population.pdf
Requires pypdf. Output retains source table labels and relevant count rows.
"""
import hashlib
import re
import sys
from pathlib import Path
from pypdf import PdfReader

source = Path(sys.argv[1])
print("SHA256", hashlib.sha256(source.read_bytes()).hexdigest())
reader = PdfReader(source)
for index in range(171, 178):
    text = reader.pages[index].extract_text() or ""
    for match in re.finditer(r"Table (\d+)\s+(QD(?:6|9|10)\..*?)(?=Table \d+|\Z)", text, re.S):
        table, content = match.groups()
        print("\nPAGE", index + 1, "TABLE", table)
        print(content[:content.index("Base :") + 150])
        for line in content.splitlines():
            if line.startswith(("Unweighted total", "Weighted total", "1 child", "2 children", "3 children", "4 children", "Any children", "I do not", "Yes", "No", "NET:", "Prefer not")):
                print(line)
        zero = content.find("I do not have parental")
        if zero >= 0:
            print(content[zero:zero + 800])
