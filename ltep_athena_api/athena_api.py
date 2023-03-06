import importlib
import json
import os
import sys
from dataclasses import dataclass
from types import FunctionType
from typing import Any, List, Optional, Union
from uuid import uuid4

import pandas as pd
import requests
import websocket
from ltep_athena_api.authenticate import AthenaAuth
from ltep_athena_api.constants import (DATASTREAM_NAME_SPACE_LTEP_ATHENA_SERVICE,
                                       EVENT_LISTENER_FUSIONCHART_LABEL_VALUE,
                                       EVENT_LISTENER_FUSIONCHART_RENDER_COMPLETE,
                                       EVENT_LISTENER_FUSIONCHART_BEFORE_RENDER,
                                       EVENT_NAME_KEY, EVENT_DATA_KEY)
from ltep_athena_api.models.AnalysisBlock import AnalysisBlock
from ltep_athena_api.models.CustomOperation import CustomOperation
from ltep_athena_api.models.DataSet import DataSet
from ltep_athena_api.models.InputForm import (InputField, InputFieldGroup,
                                              InputFieldGroupSelectionOption)
from ltep_athena_api.models.Cleanser import Cleanser
from ltep_athena_api.models.WorkflowOperation import WorkflowOperation
from threading import Thread

INTERNAL_API_ADDRESS: str = None


@dataclass
class AthenaAPI:

    def __post_init__(self):
        self.function_registy = {}
        self.function_params_registry = {}
        self.function_streaming_registry = {}
        self.function_streaming_params_registry = {}

    def __get_user(self, auth: AthenaAuth) -> dict:
        try:
            return requests.get(auth.host_api_address_sandbox + '/api/v1/user/email?email=' +
                                auth.email, headers={'Authorization': json.dumps(auth.__dict__)}).json()
        except Exception as e:
            print(e)

    def set_internal_address(self, host_address: str):
        global INTERNAL_API_ADDRESS
        INTERNAL_API_ADDRESS = host_address

    def get_data(self, dataset_id: str, auth: AthenaAuth) -> pd.DataFrame:
        """This method retrieves dataset data from specified Athena Platform and dataset. 
        :param str dataset_id: id of dataset of interest
        :param AthenaAuth auth: AthenaAuth object
        :raises Exception: if dataset retrieval was unsuccessful
        :returns: dataframe of requested data
        :rtype: DataFrame
        """
        user = self.__get_user(auth=auth)
        try:
            response = requests.get(auth.host_api_address_sandbox + '/api/v1/dataset/data?user_id=' +
                                    user.get('user_id', '') + '&dataset_id=' + dataset_id, headers={"Authorization": json.dumps(auth.__dict__)}).json()
            return pd.read_json(response)
        except Exception as e:
            print(e)
            raise Exception(
                "AthenaApi: Exception raised @ get_data(*args). Data could not retrieved. Check existence of dataset/user, user's credentials or user's access rigths to dataset {dataset_id}".format(dataset_id=dataset_id))

    def get_newest_dataset_by_label(self, dataset_label: str, auth: AthenaAuth) -> DataSet:
        """This method retrieves a dataset from specified Athena Platform and dataset label.
        Please mind that this method just returns the DataSet Object without the coresponding data.
        For retrieving data, please exclusively use `get_data`. 
        :param str dataset_label: label of dataset of interest
        :param AthenaAuth auth: AthenaAuth object
        :raises Exception: if dataset retrieval was unsuccessful
        :returns: json of dataset object
        :rtype: json
        """
        try:
            response = requests.get(
                auth.host_api_address_sandbox + "/api/v1/dataset/"+dataset_label+"/newest",
                headers={'Authorization': json.dumps(auth.__dict__)}).json()
            return DataSet(**response)
        except Exception as e:
            print(e)
            raise Exception(
                "AthenaApi: Exception raised @ get_newest_dataset_by_label(*args).")

    def save_dataset(self, dataset: DataSet, auth: AthenaAuth) -> bool:
        """This method creates new Dataset and sends it to LTEP Athena Platform.
        If you don't specify an `owner` in `DataSet` Object, you will automatically be assigned as the owner.
        :param Dataset dataset: dataset
        :returns: success info
        :rtype: bool"""
        try:
            data = dataset.data.to_json()
            del dataset.__dict__['data']
            del dataset.__dict__['size']
            del dataset.__dict__['hash_of_dataset']
            del dataset.__dict__['creation_date']
            del dataset.__dict__['dataset_id']
            if dataset.owner is None:
                user = self.__get_user(auth=auth)
                dataset.owner = user['user_id']
            requests.post(auth.host_api_address_sandbox +
                          '/api/v1/dataset', json={"data": data, "dataset": json.dumps(dataset.__dict__, default=str)},
                          headers={'Authorization': json.dumps(auth.__dict__)}).json()
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ save_dataset(*args). Dataset could not be created")
            return False

    def create_analysis_block(
            self, analysis_block: AnalysisBlock, custom_operation: CustomOperation, inputfields: List[InputField], auth: AthenaAuth,
            inputfield_group: InputFieldGroup = None, inputfield_selection_options: List[InputFieldGroupSelectionOption] = None, input_field_selection_option_dict: dict = None) -> bool:
        """This method creates a complete analysis block and sends it to LTEP Athena Platform. 
        :param AnalysisBlock analysis_block: AnalysisBlock
        :param CustomOperation custom_operation: CustomOperation
        :param List[InputField] inputfields: List[InputField]
        :param List[InputField] inputfields: List[InputField]
        :param InputFieldGroup inputfield_group: InputFieldGroup
        :param List[InputFieldGroupSelectionOption] inputfield_selection_options: List[InputFieldGroupSelectionOption]
        :param dict input_field_selection_option_dict: dict
        :param AthenaAuth auth: AthenaAuth object
        :returns: success info
        :rtype: bool
        """
        analysis_block_complete_dict = {}
        analysis_block_complete_dict.update(
            {'analysis_block': analysis_block.__dict__})
        analysis_block_complete_dict.update(
            {'custom_operation': custom_operation.__dict__})
        analysis_block_complete_dict.update(
            {'input_fields': [inputfield.__dict__ for inputfield in inputfields]})
        if not inputfield_group is None:
            analysis_block_complete_dict.update(
                {'input_field_group': inputfield_group.__dict__})
            analysis_block_complete_dict.update({
                'input_field_group_option_selections': [*inputfield_selection_options.__dict__]})
            analysis_block_complete_dict.update(
                {'input_field_selection_option_dict': input_field_selection_option_dict})
        try:
            requests.post(auth.host_api_address_sandbox +
                          '/api/sandbox/analysis', json=analysis_block_complete_dict,
                          headers={'Authorization': json.dumps(auth.__dict__)}).json()
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ create_analysis_block(*args). Analysis Block could not be created. Probably already exists.")
            return False

    def create_workflow_operation(
            self, workflow_operation: WorkflowOperation, auth: AthenaAuth) -> bool:
        """This method creates a custom workflow operation and sends it to LTEP Athena Platform. 
        :param WorkflowOperation workflow_operation: WorkflowOperation
        :param AthenaAuth auth: AthenaAuth object
        :returns: success info
        :rtype: bool
        """
        try:
            requests.post(auth.host_api_address_sandbox +
                          '/api/v1/workflowoperation', json=workflow_operation.__dict__,
                          headers={'Authorization': json.dumps(auth.__dict__)}).json()
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ create_workflow_operation(*args). Custom Workflow Operation could not be created. Probably already exists.")
            return False

    def create_cleanser(
            self, cleanser: Cleanser, auth: AthenaAuth) -> bool:
        """This method creates a cleanser and sends it to LTEP Athena Platform. 
        :param Cleanser cleanser: Cleanser
        :param AthenaAuth auth: AthenaAuth object
        :returns: success info
        :rtype: bool
        """
        try:
            requests.post(auth.host_api_address_sandbox +
                          '/api/v1/cleanser', json=cleanser.__dict__,
                          headers={'Authorization': json.dumps(auth.__dict__)}).json()
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ create_cleanser(*args). Cleanser could not be created. Probably already exists.")
            return False

    def stream_data(self, event_name: str, data: dict, auth: AthenaAuth) -> None:
        """This method creates a Websocket to LTEP Athena Streaming Service and streams the passed data. Currently, the data must be json-serializable.
        :param str event_name: name of the event (if you stream fusionChart data, the Chart id must be identical if you don't use built-in preprocessing method)
        :param dict data: data to be stream (must be json-serializable)
        :param AthenaAuth auth: AthenaAuth object
        :raises Exception: if json-serialization fails
        """
        try:
            data.update({EVENT_NAME_KEY: event_name})
            data = json.dumps(data).encode('utf-8')
        except Exception as e:
            print(e)
            raise e
        try:
            ws = websocket.WebSocket()
            ws.connect(
                "".join([auth.host_api_address_streaming, DATASTREAM_NAME_SPACE_LTEP_ATHENA_SERVICE]))
            ws.send_binary(payload=data)
        except Exception as e:
            print(e)

    def stream_fusioncharts_data_unformatted(self, event_name: str, label: Union[str, int, Any], value: Union[int, float, str], auth: AthenaAuth, message: str = "") -> None:
        """This method creates a Websocket to LTEP Athena Streaming Service and streams the passed data. Currently, the data must be json-serializable.
        :param str event_name: name of the event (if you stream fusionChart data, the Chart id must be identical if you don't use built-in preprocessing method)
        :param Union[str, int, Any] label: the X-value of Chart (label)
        :param Union[int, float, str] value: the Y-value of Chart (value)
        :param AthenaAuth auth: AthenaAuth object
        """
        stream_data = {EVENT_DATA_KEY: {
            "label": label, "value": value, "msgTitle": message, "uuid": uuid4().hex}}
        try:
            self.stream_data(event_name=event_name,
                             data=stream_data, auth=auth)
        except Exception as e:
            print(e)

    def stream_fusioncharts_data_flex(self, event_name: str, to_update_data: dict, auth: AthenaAuth) -> None:
        """This method creates a Websocket to LTEP Athena Streaming Service and streams the passed data. Currently, the data must be json-serializable.
        :param str event_name: name of the event (if you stream fusionChart data, the Chart id must be identical if you don't use built-in preprocessing method)
        :param dict to_update_data: data that should be update in real-time fusionchart
        :param AthenaAuth auth: AthenaAuth object
        """
        stream_data = {EVENT_DATA_KEY: to_update_data}
        try:
            self.stream_data(event_name=event_name,
                             data=stream_data, auth=auth)
        except Exception as e:
            print(e)

    def start_custom_streamer_function(self, function_signature: Union[str, FunctionType], function_parameters: dict = None):
        """This method is a wrapper for starting streaming functions. It creates and manages the Stream in Threads for the User.
        :param Union[str, FunctionType] function_signature: the signature of the function as string or direct reference
        :param Optional[dict[str,str]] function_parameters: dict[str,str]"""
        t = Thread(target=self.function_streaming_registry.get(function_signature) if isinstance(function_signature, str) else function_signature,
                   kwargs=self.function_streaming_params_registry.get(
            function_signature) if function_parameters is None else function_parameters, daemon=True)
        t.start()

    @staticmethod
    def preprocessing_fusionchart_real_time(complete_fusionchart_data: dict, event_name: str, auth: AthenaAuth, showMessagesButton: bool = False, add_special_function_to_execute: str = None, special_function_button_name: str = "Trigger custom Function") -> dict:
        """This methods adds EventTriggers to user-defined FusionChart dict/json. 
        User can do it accordingly the FusionChart documentation himself 
        but it is highly recommended to use this built-in function.
        :param dict complete_fusionchart_data: complete fusion chart dict/json to be send to Fronentend
        :param str event_name: name of the event; (Chart id will be replaced with event_name, so event_name should be a unique value)
        :param bool showMessagesButton: will include an option to display messages in the chart; (In case you pass a msgTitle to the stream function)
        :param str add_special_function_to_execute: will execute the passed function if triggered; (Function must be registered via the Athena API)
        :param str special_function_button_name: the passed name will be used for the button acting as a trigger for the additionaly added special function
        """
        global INTERNAL_API_ADDRESS
        if not complete_fusionchart_data.get("result", None) is None:
            data = complete_fusionchart_data.get("result")
        else:
            data = complete_fusionchart_data
        if data.get("dataSource", None) is None:
            raise ValueError(
                "No dataSource Object defined in the right place in fusionchart_data. Please refer to the oficial Dokumentaion of Fusioncharts")
        data.update({"id": event_name})
        data.update({"events": {
            "initialized":
            EVENT_LISTENER_FUSIONCHART_LABEL_VALUE.format(
                chart_id=data.get("id", event_name), streaming_host=auth.host_api_address_streaming),
            "beforeRender": EVENT_LISTENER_FUSIONCHART_BEFORE_RENDER.format(api_address=INTERNAL_API_ADDRESS, func_name=add_special_function_to_execute, button_name=special_function_button_name) if showMessagesButton or not add_special_function_to_execute is None else "",
            "renderComplete": EVENT_LISTENER_FUSIONCHART_RENDER_COMPLETE if showMessagesButton or not add_special_function_to_execute is None else "",
        }})
        return data

    def register_function(self, function: FunctionType, params: Optional[dict[str, str]] = {},
                          packages_to_install: Optional[List[str]] = None,
                          custom_module_name: Optional[str] = None, path_to_module: Optional[str] = os.path.abspath(__file__),
                          custom_modules_and_module_paths: Optional[dict[str, str]] = None, create_custom_operation: bool = True) -> Union[None, CustomOperation]:
        """This method registers and saves custom methods and its parameters in two distinct dictionaries. furthermore, it installs user's required packages and custom written modules.
        :param FunctionType function: FunctionType, the method signature as function !not! string
        :param Optional[dict[str,str]] params: dict[str,str], the key is the passed function's parameter definition in the signature and the value the parameter passed by the user itself, e.g. {'param_by_function_defined' : 'my_param'}
        :param Optional[List[str]] packages_to_install: List[str], in case of extra needed packages pass package name and optionally version like pandas==1.0.1
        :param Optional[str] custom_module_name: str, the custom written module's name 
        :param Optional[str] path_to_module: str, the custom written module's path, use os.path.abspath(__file__) to dynamically assign path
        :param Optional[dict] custom_modules_and_module_paths: dict, in case of multiple custom written modules, map custom module name (key) to custom module path (value) via a dictionary path; use os.path.abspath(__file__) to dynamically assign path
        :param Optional[bool] create_custom_operation: default is True, if True will create automatically CustomOperation 
        :returns: nothing or CustomOperation, if create_custom_operation set to True
        :rtype: Union[None, CustomOperation]
        """
        if not packages_to_install is None:
            for package_name in packages_to_install:
                AthenaAPI.__install_module(package_name=package_name)
        if not custom_modules_and_module_paths is None:
            for (custom_module_name, custom_module_path) in custom_modules_and_module_paths.items():
                sys.path.insert(0, r'{}'.format(custom_module_path))
                globals()[custom_module_name] = importlib.import_module(
                    custom_module_name)
        elif not custom_module_name is None:
            sys.path.insert(0, r'{}'.format(path_to_module))
            globals()[custom_module_name] = importlib.import_module(
                custom_module_name)
        self.function_registy.update({function.__name__: function})
        self.function_params_registry.update({function.__name__: params})
        if create_custom_operation:
            return AthenaAPI.__create_custom_operation_from_registry(custom_operation_func_signature=function.__name__)

    def register_streaming_function(self, function: FunctionType, params: Optional[dict[str, str]] = {},
                                    packages_to_install: Optional[List[str]] = None,
                                    custom_module_name: Optional[str] = None, path_to_module: Optional[str] = os.path.abspath(__file__),
                                    custom_modules_and_module_paths: Optional[dict[str, str]] = None, create_custom_operation: bool = True) -> Union[None, CustomOperation]:
        """This method registers and saves custom streaming methods and its parameters in two distinct dictionaries. furthermore, it installs user's required packages and custom written modules.
        :param FunctionType function: FunctionType, the method signature as function !not! string
        :param str event_name: unique event_name to identify the correct websocket
        :param Optional[dict[str,str]] params: dict[str,str], the key is the passed function's parameter definition in the signature and the value the parameter passed by the user itself, e.g. {'param_by_function_defined' : 'my_param'}
        :param Optional[List[str]] packages_to_install: List[str], in case of extra needed packages pass package name and optionally version like pandas==1.0.1
        :param Optional[str] custom_module_name: str, the custom written module's name 
        :param Optional[str] path_to_module: str, the custom written module's path, use os.path.abspath(__file__) to dynamically assign path
        :param Optional[dict] custom_modules_and_module_paths: dict, in case of multiple custom written modules, map custom module name (key) to custom module path (value) via a dictionary path; use os.path.abspath(__file__) to dynamically assign path
        :param Optional[bool] create_custom_operation: default is True, if True will create automatically CustomOperation 
        :returns: nothing or CustomOperation, if create_custom_operation set to True
        :rtype: Union[None, CustomOperation]
        """
        if not packages_to_install is None:
            for package_name in packages_to_install:
                AthenaAPI.__install_module(package_name=package_name)
        if not custom_modules_and_module_paths is None:
            for (custom_module_name, custom_module_path) in custom_modules_and_module_paths.items():
                sys.path.insert(0, r'{}'.format(custom_module_path))
                globals()[custom_module_name] = importlib.import_module(
                    custom_module_name)
        elif not custom_module_name is None:
            sys.path.insert(0, r'{}'.format(path_to_module))
            globals()[custom_module_name] = importlib.import_module(
                custom_module_name)
        self.function_streaming_registry.update({function.__name__: function})
        self.function_streaming_params_registry.update(
            {function.__name__: params})
        if create_custom_operation:
            return AthenaAPI.__create_custom_operation_from_registry(custom_operation_func_signature=function.__name__)

    @staticmethod
    def __install_module(package_name: str) -> None:
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name])

    @staticmethod
    def __create_custom_operation_from_registry(custom_operation_func_signature: str) -> CustomOperation:
        return CustomOperation(custom_operation_func_signature=custom_operation_func_signature)
