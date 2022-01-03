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
            "outfile_format": "txt"
            }
        }
    with open(config_file_name, 'w') as outfile:
        yaml.dump(skeleton_config, outfile, default_flow_style=False, sort_keys=False)