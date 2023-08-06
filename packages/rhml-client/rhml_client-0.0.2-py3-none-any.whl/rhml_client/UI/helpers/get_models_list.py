from . import configuration;
from rhythmic import rhythmicDB, faultReturnHandler;
from .db_record_to_dictionary import modelPropertiesDictionary;

@faultReturnHandler
def getModelsList():

    with rhythmicDB(configuration.db_name, configuration.db_file_name) as db:
        models_table = db.execute(
            """
            SELECT * FROM models_table WHERE 1 ORDER BY last_version_timestamp DESC;
            """);

    models = [];

    for model in models_table:
        models.append( modelPropertiesDictionary(model) );

    return models;