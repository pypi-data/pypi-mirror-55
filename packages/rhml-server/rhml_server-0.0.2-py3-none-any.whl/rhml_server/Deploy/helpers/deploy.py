from . import configuration;
import json;
from os import mkdir as makeDir, getcwd as getCurrentWorkingDir;
from os.path import exists, isdir as isDir;
from rhythmic import rhythmicDB;
from datetime import datetime;
from zipfile import ZipFile;

def checkDir(dir_path):

    if not (exists(dir_path) and isDir(dir_path)):
        makeDir(dir_path);

    return True;

def deployModel(deploy_files):
    """
    deploy_files is a dictionary of werkzeug `FileStorage`s

    data passed with file:
    var data = 
    {
        "deploy_id": window.the_model_deploy_id,
        "model_name": window.the_model_name,
        "model_id": window.the_model_id,
        "version_number": window.active_version_number,
        "model_metadata": encodeURI(window.actual_metadata)
    }
    """

    deploy_result = {};

    timestamp = datetime.now();
    working_dir_path = getCurrentWorkingDir();

    storage_dir = "{}/{}".format(working_dir_path,configuration.storage_folder_name);
    checkDir(storage_dir);

    for file_name in deploy_files:
        if file_name.endswith(".json"):
            deploy_data_file_name = file_name;
        else:
            artifacts_archive_name = file_name;

    if deploy_data_file_name:
        metadata_encoded_json = deploy_files[deploy_data_file_name].read();
    else:
        return "Fault: no metadata file received";

    metadata_json = metadata_encoded_json.decode();
    metadata = json.loads(metadata_json);

    # got the metadata here, putting data to db:

    with rhythmicDB(configuration.db_name, configuration.db_file_name) as db:

        if metadata["deploy_id"] != 0:

            deploy_id_ok = db.execute(
                """
                SELECT id FROM models_table WHERE id = '{}';
                """.format(
                                    metadata["deploy_id"]
                                )
            );

            if deploy_id_ok:
                passed_deploy_id = metadata["deploy_id"];
            else:
                passed_deploy_id = 0;

        else:
            passed_deploy_id = 0;

        if passed_deploy_id == 0:

            model_deploy_id = db.execute(
                """
                INSERT INTO models_table
                (
                    model_name,
                    last_deploy_timestamp,
                    active_version,
                    build_id
                )
                VALUES
                ('{}', '{}', '{}', '{}');
                """.format(
                                    metadata["model_name"],
                                    timestamp,
                                    metadata["version_number"],
                                    metadata["model_id"]
                                )
            );

        else:
            
            model_deploy_id = passed_deploy_id;

            db.execute(
                """
                UPDATE models_table SET
                    last_deploy_timestamp = '{}',
                    active_version = '{}'
                WHERE id = '{}';
                """.format(
                                    timestamp,
                                    metadata["version_number"],
                                    model_deploy_id
                                )
            );

    # finished with db here, let's create a folder and unpack artifacts there

    deploy_dir = "{}/model{}".format(storage_dir, model_deploy_id);
    checkDir(deploy_dir);

    model_files_dir = "{}/files".format(deploy_dir);
    checkDir(model_files_dir);

    new_archive_name = "deploy_{}_{}.zip".format(metadata["model_id"], model_deploy_id);
    new_data_file_name = "deploy_{}_{}.json".format(metadata["model_id"], model_deploy_id);

    deploy_files[artifacts_archive_name].save("{}/{}".format(deploy_dir, new_archive_name));
    deploy_files[deploy_data_file_name].save("{}/{}".format(deploy_dir, new_data_file_name));

    archive_path = "{}/{}".format(deploy_dir, new_archive_name);

    with ZipFile(archive_path) as deploy_package:
        deploy_package.extractall(model_files_dir);
    
    #################################
    #Unpacking done. call runModel (got ot write it first);
    #################################

    deploy_result["model_deploy_id"] = model_deploy_id;
    deploy_result["status"] = "Success";
    return deploy_result;