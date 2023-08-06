from flask import Flask, request;
from . import helpers;
from functools import wraps;
import json;
from os import getcwd as getCurrentWorkingDir;
from rhythmic import rhythmicDB;

app = Flask(__name__);

# working_dir_path = getCurrentWorkingDir();
# storage_dir = "{}/{}".format(working_dir_path, helpers.configuration.storage_folder_name);

deploy_storage = helpers.DeployMemoryStorage();
with rhythmicDB(db_name = "SQLite", db_filename = helpers.configuration.db_file_name) as db:
    predeployed_ids = db.execute("SELECT id FROM models_table WHERE 1");
    if len(predeployed_ids) > 0:
        for predeployed_id in predeployed_ids:
            deploy_storage.deployCell(predeployed_id[0]);

#==========================================================================
#====================      DECORATORS     =========================================
#==========================================================================
def checkPost(entry_point):

    @wraps(entry_point)
    def wrapper(*args, **kwargs):
        if request.method == "POST":

            return entry_point(*args, **kwargs);

        else:

            return "Only POST requests are presumed.";

    return wrapper;

#==========================================================================
#====================      SERVER ROUTES     ========================================
#==========================================================================

@app.route("/deploy", methods = ["POST"])
@checkPost
def deployModelData():

    global deploy_storage;

    result = helpers.deployModel(request.files);
    request.close();
    result_json = json.dumps(result);

    model_deploy_id = result["model_deploy_id"];

    deploy_storage.deployCell(model_deploy_id);

    return result_json;

@app.route("/score/<model_deploy_id>", methods = ["POST"])
@checkPost
def scoreModel(model_deploy_id):

    global deploy_storage;

    data_json = request.data.decode();
    the_model = deploy_storage.fetchCell(model_deploy_id);

    if the_model:
        result_json = the_model(data_json);
    else:
        result_json = json.dumps({"Error":"model with deploy id = {} not found".format(model_deploy_id)});

    return result_json;

#==========================================================================
#==========================================================================
#==========================================================================

def runAPI(app, host = helpers.configuration.host, port = helpers.configuration.port):
    """
    runAPI(app, host = host, port = port):  
    app is a Flask app
    """

    app.run(debug = True, host = host, port = port);

    return True;

if __name__ == "__main__":

    runAPI(app);
