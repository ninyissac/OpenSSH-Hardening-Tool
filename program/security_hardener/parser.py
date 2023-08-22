from security_hardener.constants import *
import re
import glob

def parse_template(**kwargs):
# Function for parsing context template files and system ssh config file

    parsed_lines = {}
    include_paths = []

    ctx = kwargs["ctx"]
    file_path = TEMPLATE_PATH
    if "parse_file" in kwargs:
        if kwargs["parse_file"] == "system":  # parse system ssh config (/etc/ssh/sshd_config)
            file_path = SYSTEM_PATH

    template_file = ctx[file_path]
    pat_vars = r'^#?\s*([A-Za-z]+)\s+(.+)$'

    with open(template_file, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            m = re.match(pat_vars, line)

            if m is not None:
                parsed_lines[m.group(1)] = m.group(2).strip()

            if file_path == SYSTEM_PATH:  # Check for the 'Include' keyword only in main system config file
                # Locate the line with the Include directive
                if line.startswith("Include") and not line.startswith("#Include"):
                    include_pattern = line.split()[1]

                    # Use glob to get matching file paths
                    include_paths = glob.glob(include_pattern)

    return parsed_lines, include_paths  # Return both parsed_lines and include_paths


def parse_compiler(**kwargs):
# Function for parsing context template .csv file

    parsed_lines = []
    ctx = kwargs["ctx"]

    template_file = ctx[TEMPLATE_COMPILER_PATH]

    with open(template_file, "r") as f:
        lines = f.readlines()

        k = None  # Initialize k as None

        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):  # process comments
                print("In func pc, line for #:", line)
                continue

            if k is None: # process header
                k = [x.strip() for x in line.split(",")]
                print("In func pc, k:", k)
                continue

            comma_value = False
            m = re.search(r'\\,', line)
            if m is not None:
                line = line.replace('\\,', '!')
                comma_value = True
            v = [x.strip() for x in line.split(",")]

            if comma_value:
                v[1] = v[1].replace('!', ',')

            parsed_dict = dict(zip(k, v))
            parsed_lines.append(parsed_dict)

    print("In fuc pc, parsed_lines:", parsed_lines)
    return parsed_lines