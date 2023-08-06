from rhythmic import rhythmicDB;
from datetime import datetime;
from Deploy import configuration;

general_table = \
"""
CREATE TABLE IF NOT EXISTS general
(
    id integer PRIMARY KEY,
    param_key text NOT NULL,
    param_value text NOT NULL
);
""";

models_table = \
"""
CREATE TABLE IF NOT EXISTS models_table
(
    id integer PRIMARY KEY,
    model_name text NOT NULL,
    last_deploy_timestamp text NOT NULL,
    active_version integer NOT NULL DEFAULT 0,
    build_id integer DEFAULT 0
);
""";


def main():

    with rhythmicDB(configuration.db_name, configuration.db_file_name) as db:

        db.runScript(
            general_table +
            models_table
            );

    print(   "Database is created, tables are created. DB file: \"{}\", {}".format(  configuration.db_file_name, str( datetime.now() )  )   );

if __name__ == "__main__":
    main();