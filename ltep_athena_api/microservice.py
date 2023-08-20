from dataclasses import dataclass
from threading import Thread
from typing import List, Any

import flask as fl
from flask import Flask
from flask_cors import CORS, cross_origin

from ltep_athena_api.athena_api import AthenaAPI
from ltep_athena_api.models.CleanserResult import CleanserResult

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

    def initiate_service(self, host='http://0.0.0.0', port=27027, origins: List[str] = ["*"], start_streamers: list = ["*"]):
        """This method initializes the FLASK application.
            :params str host: server url for hosting service
            :params int port: port where application shall run
            :returns: None
            :rtype: None
        """
        self.athena_api.set_internal_address(
            f"{host}:{port}")
        if "*" in start_streamers:
            [self.__start_websocket_tasks(key) for
                key in self.athena_api.function_streaming_registry.keys()]
        else:
            [self.__start_websocket_tasks(key) for
                key in self.athena_api.function_streaming_registry.keys() if key in start_streamers]
        app_api = Flask(__name__)
        CORS(app_api, supports_credentials=True, send_wildcard=False, allow_headers=["Content-Type", "x-user-email", "Origin", "Authorization"],
             expose_headers=["Content-Type", "x-user-email",
                             "Origin", "Authorization"], origins=origins)
        app_api.register_blueprint(blueprint=blueprint)
        app_api.run(port=port)

    def __start_websocket_tasks(self, websocket_task: str):
        """This method sends a data stream to LTEP Athena Platform.
        Important is the definition of a custom_event because only with that,
        the LTEP Athena Platform can connect and emit to the correct destinition (websocket)"""
        t = Thread(target=self.athena_api.function_streaming_registry.get(websocket_task),
                   kwargs=self.athena_api.function_streaming_params_registry.get(
            websocket_task), daemon=True)
        t.start()


def get_global_athena_api_instance() -> AthenaAPI:
    global athena_api
    return athena_api


blueprint = fl.Blueprint('AthenaRestAPI', __name__)


@blueprint.route('/api/v1/athenarestapi/execute/<func_name>', methods=['GET'])
@cross_origin(origins="*")
def execute_individual_function(func_name: str):
    try:
        try:
            formdata = fl.request.get_json(force=True)
        except Exception as e:
            print(e)
            formdata = {}
        finally:
            athena_api = get_global_athena_api_instance()
            try:
                t = Thread(target=athena_api.function_streaming_registry.get(func_name, None),
                           kwargs=athena_api.function_streaming_params_registry.get(func_name, {}).update(formdata), daemon=True)
                t.start()
            except:
                print(e)
            try:
                data = athena_api.function_registy.get(func_name, None)(
                    **athena_api.function_params_registry.get(func_name, {}), **formdata)
                return fl.jsonify({"result": __data_preprocessing_for_data_cleanser(data)}), 200
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print("function_execution_failed: check if Function was registered! Details see above.")
        return AthenaRestAPI.endpoints_exception(msg="function_execution_failed: check if Function was registered!", code="400")


def __data_preprocessing_for_data_cleanser(data: Any) -> Any:
    if isinstance(data, CleanserResult):
        return data.formatted_results
    return data
