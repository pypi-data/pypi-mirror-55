from . import configuration;
from os import getcwd as getCurrentWorkingDir;
from os.path import exists;
from importlib import util;

class DeployMemoryStorage:

    def __init__(self):

        self.specs = {};
        working_dir_path = getCurrentWorkingDir();
        self.storage_dir = "{}/{}".format(working_dir_path,configuration.storage_folder_name);

    def deployCell(self, model_deploy_id):

        deploy_dir = "{}/model{}".format(self.storage_dir, model_deploy_id);
        wrapper_path = "{}/files/{}".format(deploy_dir, configuration.model_wrapper_class_file_name);

        if not exists(wrapper_path):
            return None;

        module_name = "RhmlModelWrapper{}".format(model_deploy_id);

        if module_name in self.specs:
            del self.specs[module_name];

        self.specs[module_name] = {};

        self.specs[module_name]["spec"] = util.spec_from_file_location(module_name, wrapper_path);
        self.specs[module_name]["module"] = util.module_from_spec(self.specs[module_name]["spec"]);

        self.specs[module_name]["spec"].loader.exec_module(self.specs[module_name]["module"]);

        self.specs[module_name]["instance"] = self.specs[module_name]["module"].ModelWrapper(deploy_dir);

        return True;

    def fetchCell(self, model_deploy_id):

        module_name = "RhmlModelWrapper{}".format(model_deploy_id);

        if module_name in self.specs:
            return self.specs[module_name]["instance"];

        else:
            return None;