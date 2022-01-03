import click
from todoget.main import main
from todoget.utils import utils
from todoget.main import main
from todoget.wrt import wrt

@click.command("todoget")
@click.argument('cmd')
def todoget(cmd):
    if cmd == "init":
        main.init_config_file()
        utils.success_init()
    else:
        # Read configuration file

        config_file = main.read_config_file()

        setup_info = main.get_config_info(config_file) # general setup

        files_to_track = main.get_files_to_track(setup_info) # files to track
        
        # Get workflow entry from the config file

        dict_objects = main.get_workflow_entry(config_file)
        
        # Create the full list of dictionaries
        
        workflow_list = main.create_worflow_list(dict_objects, main.workflow_object, files_to_track)
        
        # Getting all lines from files and patterns     
        
        main.scan_all_files_and_patterns(workflow_list)
        main.check_which_include(workflow_list)
        
        # Create Output file
        
        
        outfile_name = setup_info["outfile_name"] + "." + setup_info["outfile_format"]

        with open(outfile_name, "w") as outfile:
            outfile.writelines(wrt.create_out_title())
            for i, target_file in enumerate(workflow_list):
                if target_file['include']:
                    outfile.writelines(wrt.create_file_title(target_file["file"]))
                for j, obj in enumerate(target_file["objs"]):
                    if len(obj.line_list) > 0 and obj.active > 0:
                        outfile.writelines("\n")
                        outfile.writelines(obj.create_output())
                        outfile.writelines("\n")
                        
        utils.success_output(outfile_name)