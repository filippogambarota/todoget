import pathspec
import os
import yaml
from fnmatch import fnmatch
import click
from datetime import date, datetime
import emoji

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_details(tags):
    print('  |')
    fmatches = get_freqs(tags)
    for k, v in fmatches.items():
        print('  |-- {}: {}'.format(text_blue(k), v))

def analyze_file(file, patterns):
    lines = read_lines(file)
    nmatch = 0
    linenum = []
    matches = []
    tags = []

    res = {}
    for i, line in enumerate(lines):
        is_match, tag = find_match(line, patterns)
        if is_match:
            tags.append(tag)
            matches.append(line)
            linenum.append(i)
            nmatch += 1
    res['file'] = file
    res['matches'] = matches
    res['linenum'] = linenum
    res['tags'] = flatten(tags)
    res['keep'] = nmatch > 0
    return res
    
def tick():
    return '\u2713'

def get_freqs(x):
    freqs = {}
    for el in x:
        if el in freqs:
            freqs[el] += 1
        else:
            freqs[el] = 1
    return freqs

def text_green(msg):
    out = bcolors.OKGREEN + msg + bcolors.ENDC
    return out

def text_blue(msg):
    out = bcolors.OKBLUE + msg + bcolors.ENDC
    return out

def success(msg):
    print(emoji.emojize(text_green(tick()) + " " +  msg))

def success_init():
    print(text_green(tick()) + " configuration file " + text_green(".todoget"))

def create_out_title():
    title =  "Todoget Report"
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    out_title = '# ' + title + '\n' + 'last update: ' + str(date.today()) + ' ' + '(' + current_time  + ')' + '\n'
    return out_title

def rep_string(string, times, sep = ""):
    out = [string]
    out = out * times
    out = sep.join(out)
    return(out)

def read_lines(file):
    file = open(file, 'r', encoding='utf-8', errors='ignore')
    lines = file.readlines()
    return lines

def find_match(line, patterns):
            is_match = False
            tag = []
            for p in patterns:
                if p in line:
                    tag.append(p)
                    is_match = True
            return is_match, tag

def flatten(l):
    return [item for sublist in l for item in sublist]

def format_line(line, idx):
    line = '- Line {}: {} \n'.format(idx, line)
    return line

def get_all_non_hidden_files():
    # thanks to https://www.kite.com/python/examples/4293/os-get-the-relative-paths-of-all-files-and-subdirectories-in-a-directory
    # and https://stackoverflow.com/a/13454267
    list_files = []
    for root, dirs, files in os.walk("."):
        for f in files:
            temp = os.path.relpath(os.path.join(root, f), ".")
            if temp[0] != ".":
                list_files.append(temp)
    return list_files


def get_file_info(filename):
    basename_file = os.path.basename(filename)
    name = os.path.splitext(basename_file)[0]
    ext = os.path.splitext(basename_file)[1]
    return name, ext

def ignore_files(files, remove):
    filenames = (file for file in files 
             if not any(fnmatch(file, ignore) for ignore in remove))
    return [x for x in filenames]

def init_config_file():
    config = {
        "todo":{
            "name": "todo",
            "pattern": "TODO",
            "active": True
            },
        "config":{
            "ignore": ["venv/*", "todoget.md"]
            }
        }
    with open('.todoget', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False, sort_keys=False)

def read_config_file():
    with open('.todoget', 'r') as f:
        config_file = yaml.load(f, Loader=yaml.FullLoader) # also, yaml.SafeLoader
    return config_file

def remove_comments(x):
    x = x.replace('<!--','')
    x = x.replace('-->','')
    x = x.replace("#", "")
    x = x.strip()
    return x

@click.command("todoget")
@click.argument('cmd')
def todoget(cmd):
    if cmd == "init":
        init_config_file()
        success_init()
    elif cmd == "scan":
        config_file = read_config_file()
        config = config_file.popitem()

        files = get_all_non_hidden_files()
        files = ignore_files(files, config[1]['ignore'])
        patterns = []

        for k, v in config_file.items():
            if v['active']:
                patterns.append(v['pattern'])

        results = [analyze_file(fl, patterns) for fl in files]
        details = flatten([x['tags'] for x in results])
        nfiles = len([x for x in results if x['keep']])

        if not any(x['keep'] for x in results):
            print("niente")
        else:
            with open('todoget.md', 'w') as out:
                out.write(create_out_title())
                for file in results:
                    if file['keep']:
                        out.write('\n')
                        out.write("## " + file['file'] + "\n\n")
                        array = zip(file['matches'], file['tags'], file['linenum'])
                        for elem in array:
                            line = remove_comments(elem[0])
                            out.write(format_line(line, elem[2]))
            success(text_blue(str(nfiles)) + " files scanned with " + text_blue(str(len(details))) + " stuff to do!")
            print_details(details)
    else:
        print("command not found!")

if __name__ == '__main__':
    todoget()








