"""
1. get the model_deploy_id from command line arguments
2. import ModelWrapper class from according model files folder
3. launch infinite loop reading data from stdin and writiong predictions to stdout
"""

# working_dir_path = getCurrentWorkingDir();
# storage_dir = "{}/{}".format(working_dir_path, helpers.configuration.storage_folder_name);
# deploy_dir = "{}/model{}".format(storage_dir, model_deploy_id);
# model_files_dir = "{}/files".format(deploy_dir);

#  folder on a serving host with model artifacts named as follows: "model" + `deploy_id`

import sys;
from helpers import configuration;
from os import getcwd as getCurrentWorkingDir;

if (len(sys.argv) < 2):
    raise Exception("No arguments passed.");

model_deploy_id = sys.argv[1];

working_dir_path = getCurrentWorkingDir();
storage_dir = "{}/{}".format(working_dir_path,configuration.storage_folder_name);
deploy_dir = "{}/model{}".format(storage_dir, model_deploy_id);

###!!! https://docs.python.org/3/library/importlib.html#importlib.import_module