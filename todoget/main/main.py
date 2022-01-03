import yaml
import os
from todoget.wrt import wrt

def init_config_file():
    skeleton_config = {
        "todo":{
            "name": "todo",
            "pattern": "TODO",
            "active": True
            },
        "config":{
            "include_all_files": True,
            "include_files": [""],
            "exclude_files": [""],
            "outfile_name": "outfile",
            "outfile_format": "txt",
            "report_all": False
            }
        }
    with open('.todoget', 'w') as outfile:
        yaml.dump(skeleton_config, outfile, default_flow_style=False, sort_keys=False)
        
# NOTE have a look here for the istances from dictionary https://stackoverflow.com/questions/1639174/creating-class-instance-properties-from-a-dictionary

class workflow_object(object):
    def __init__(self, dict):
        self.name = dict["name"]
        self.pattern = dict["pattern"]
        self.nlines = 0
        self.line_list = []
        self.active = dict["active"]
  
    # thanks to https://stackoverflow.com/a/1639632
    #def __getattr__(self, name):
    #	return self[name]

    def get_lines_with_pattern(self, filename):
        
        with open(filename, 'r') as outfile:
            tgt_lines = outfile.readlines() # read all lines
            line_count = -1 # counter for the line
        
            # Loop and get line number, text and format
            for line in tgt_lines:
                self.nlines += 1
                if self.pattern in line:
                    line_new = wrt.format_line(line, self.nlines, self.pattern)
                    self.line_list.append(line_new)
        return self

    def create_output(self):
        out = "### " + self.name + "\n\n"
        if len(self.line_list) != 0:
            for i, line in enumerate(self.line_list):
                out += line
        """
        else:
            out += "No " + self.name + " tags in the file, well done! :)" + "\n"
        """
        return out

def init_config_file(config_file_name = '.todoget'):
    skeleton_config = {
        "todo":{
            "name": "todo",
            "pattern": "TODO",
            "active": True
            },
        "config":{
            "include_all_files": True,
            "include_files": [""],
            "exclude_files": [""],
            "outfile_name": "outfile",
            "outfile_format": "md"
            }
        }
    with open(config_file_name, 'w') as outfile:
        yaml.dump(skeleton_config, outfile, default_flow_style=False, sort_keys=False)

def get_files_to_track(setup_info):
    exclude_files = setup_info["exclude_files"]
    exclude_files.append(setup_info["outfile_name"] + "." + setup_info["outfile_format"])
    if setup_info["include_all_files"]:
        temp = get_all_non_hidden_files()
        out = remove_excluded_files(temp, exclude_files)
    else:
        out = setup_info["include_files"]
    return out

def get_config_info(config_file):
    config_info = config_file["config"]
    return config_info

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

def get_workflow_entry(config_file):
    # get only the workflow objects
    dict_objects = {a:config_file[a] for a in config_file.keys() if not a in "config"}
    return dict_objects

def create_workflow_objects(dict_objects, workflow_objects):
    out = []
    keys = list(dict_objects.keys())
    for i in range(len(dict_objects)):
        dict_i = dict_objects[keys[i]]
        out.append(workflow_objects(dict_i))
    return out

def create_worflow_list(dict_objects, workflow_object, files_to_track):
    final_list = []
    for i, targetfile in enumerate(files_to_track):
        temp_dict = {
            "file":targetfile,
            "objs":[]
        }
        objs = create_workflow_objects(dict_objects, workflow_object)
        temp_dict["objs"] = objs
        final_list.append(temp_dict)
    return final_list

def get_file_name(filename):
    basename_file = os.path.basename(filename)
    filename = os.path.splitext(basename_file)[0]
    return filename
    
def get_file_ext(filename):
    basename_file = os.path.basename(filename)
    filename = os.path.splitext(basename_file)[1]
    return filename
    

def remove_excluded_files(target_list, exclude_list):
    out = [i for i in target_list if i not in exclude_list]
    return out


def read_config_file():
    with open('.todoget', 'r') as f:
        config_file = yaml.load(f, Loader=yaml.FullLoader) # also, yaml.SafeLoader
    return config_file