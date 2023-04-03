from security_hardener.constants import *
import re

def parse_template(**kwargs):

    parsed_lines = {}
    ctx = kwargs["ctx"]
    file_path = TEMPLATE_PATH
    if "parse_file" in kwargs:
        if kwargs["parse_file"] == "system":
            file_path = SYSTEM_PATH

    template_file = ctx[file_path]
    pat_vars = r'^#?\s*([A-Za-z]+)\s+(.+)$'

    with open(template_file, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            m = re.match(pat_vars, line)

            if m is not None:
                parsed_lines[m.group(1)] = m.group(2).strip()
    
    return parsed_lines


def parse_compiler(**kwargs):

    parsed_lines = []
    ctx = kwargs["ctx"]

    template_file = ctx[TEMPLATE_COMPILER_PATH]

    with open(template_file, "r") as f:
        lines = f.readlines()

        k = []
        for i, line in enumerate(lines):
            
            if not line.strip():
                continue

            v = [x.strip() for x in line.split(",")]

            if i == 0:
                k = v

            else:
                parsed_lines.append(dict(zip(k, v)))

    return parsed_lines
