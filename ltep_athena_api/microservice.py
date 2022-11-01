from dataclasses import dataclass
import flask as fl
from flask_cors import CORS, cross_origin
from flask import Flask

from ltep_athena_api.athena_api import AthenaAPI

athena_api: AthenaAPI = None


@dataclass
class AthenaRestAPI:
    athena_api: AthenaAPI

    def __post_init__(self):
        global athena_api
        athena_api = self.athena_api

    @staticmethod
    def endpoints_exception(code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))

    def initiate_service(self, host='0.0.0.0', port=27027):
        """This method initializes the FLASK application.
            :params str host: server url for hosting service
            :params int port: port where application shall run
            :returns: None
            :rtype: None
        """
        SandBoxServiceFlask = Flask(__name__)
        CORS(SandBoxServiceFlask)
        SandBoxServiceFlask.register_blueprint(blueprint=blueprint)
        SandBoxServiceFlask.run(host=host, port=port)


def get_global_athena_api_instance() -> AthenaAPI:
    global athena_api
    return athena_api


blueprint = fl.Blueprint('AthenaRestAPI', __name__)


@blueprint.route('/api/v1/athenarestapi/execute/<func_name>', methods=['GET'])
@cross_origin(origins="*")
def execute_individual_function(func_name: str):
    try:

        formdata = fl.request.get_json(force=True)
        athena_api = get_global_athena_api_instance()
        data = athena_api.function_registy.get(func_name, None)(
            **athena_api.function_params_registry.get(func_name, {}), **formdata)
        return fl.jsonify({"result": data}), 200
    except Exception as e:
        print(e)
        return AthenaRestAPI.endpoints_exception(msg="function_execution_failed", code="400")
