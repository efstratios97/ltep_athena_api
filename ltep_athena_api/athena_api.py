import os
import sys
import json
from typing import List, Optional
import requests
import importlib
import pandas as pd

from dataclasses import dataclass

from types import FunctionType

from ltep_athena_api.models.DataSet import DataSet
from ltep_athena_api.authenticate import AthenaAuth
from ltep_athena_api.models.AnalysisBlock import AnalysisBlock
from ltep_athena_api.models.CustomOperation import CustomOperation
from ltep_athena_api.models.WorkflowOperation import WorkflowOperation
from ltep_athena_api.models.InputForm import InputField, InputFieldGroup, InputFieldGroupSelectionOption, InputFieldType


@dataclass
class AthenaAPI:

    def __post_init__(self):
        self.function_registy = {}
        self.function_params_registry = {}

    def __get_user(self, auth: AthenaAuth) -> dict:
        try:
            return requests.get(auth.host_api_address + '/user/email?email=' +
                                auth.email).json()
        except Exception as e:
            print(e)

    @AthenaAuth.authenticate_access_athena
    def get_data(self, dataset_id: str, dataset_label: str, auth: AthenaAuth) -> pd.DataFrame:
        """This method retrieves dataset data from specified Athena Platform and dataset. 
        :param str dataset_id: id of dataset of interest
        :param str dataset_label: label of dataset of interest
        :param AthenaAuth auth: AthenaAuth object
        :raises Exception: if dataset retrieval was unsuccessful
        :returns: dataframe of requested data
        :rtype: DataFrame
        """
        user = self.__get_user(auth=auth)
        try:
            response = requests.get(auth.host_api_address + '/api/v1/dataset/data?user_id=' +
                                    user.get('user_id', '') + '&dataset_id=' + dataset_id + '&dataset_label=' + dataset_label).json()
            return pd.read_json(response)
        except Exception as e:
            print(e)
            raise Exception(
                "AthenaApi: Exception raised @ get_data(*args). Data could not retrieved. Check existence of dataset/user, user's credentials or user's access rigths to dataset {dataset_id}".format(dataset_id=dataset_id))

    @AthenaAuth.authenticate_access_athena
    def get_newest_dataset_by_label(self, dataset_label: str, auth: AthenaAuth) -> pd.DataFrame:
        """This method retrieves a dataset from specified Athena Platform and dataset label. 
        :param str dataset_label: label of dataset of interest
        :param AthenaAuth auth: AthenaAuth object
        :raises Exception: if dataset retrieval was unsuccessful
        :returns: json of dataset object
        :rtype: json
        """
        try:
            response = requests.get(
                auth.host_api_address + "/api/v1/dataset/"+dataset_label+"/newest").json()
            return response
        except Exception as e:
            print(e)
            raise Exception(
                "AthenaApi: Exception raised @ get_newest_dataset_by_label(*args).")

    @AthenaAuth.authenticate_access_athena
    def save_dataset(self, dataset: DataSet, auth: AthenaAuth) -> bool:
        """This method creates new Dataset and sends it to LTEP Athena Platform.
        :param Dataset dataset: dataset
        :returns: success info
        :rtype: bool"""
        try:
            data = dataset.data.to_json()
            del dataset.__dict__['data']
            if dataset.owner is None:
                user_response = requests.get(
                    auth.host_api_address + "/api/v1/user/email?email=" + auth.email).json()
                dataset.owner = user_response['user_id']
            response = requests.post(auth.host_api_address +
                                     '/api/v1/dataset', json={"data": data, "dataset": json.dumps(dataset.__dict__, default=str)}).json()
            print(response)
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ save_dataset(*args). Dataset could not be created")
            return False

    @AthenaAuth.authenticate_access_athena
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
            response = requests.post(auth.host_api_address_sandbox +
                                     '/api/sandbox/analysis', json=analysis_block_complete_dict).json()
            print(response)
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ create_analysis_block(*args). Analysis Block could not be created. Probably alredy exists.")
            return False

    @AthenaAuth.authenticate_access_athena
    def create_workflow_operation(
            self, workflow_operation: WorkflowOperation, auth: AthenaAuth) -> bool:
        """This method creates a custom workflow operation and sends it to LTEP Athena Platform. 
        :param WorkflowOperation workflow_operation: WorkflowOperation
        :param AthenaAuth auth: AthenaAuth object
        :returns: success info
        :rtype: bool
        """
        try:
            response = requests.post(auth.host_api_address +
                                     '/api/v1/workflowoperation', json=workflow_operation.__dict__).json()
            print(response)
            return True
        except Exception as e:
            print(e)
            print(
                "AthenaApi: Exception catched @ create_workflow_operation(*args). Custom Workflow Operation could not be created. Probably alredy exists.")
            return False

    def register_function(self, function: FunctionType, params: Optional[dict[str, str]] = {},
                          packages_to_install: Optional[List[str]] = None,
                          custom_module_name: Optional[str] = None, path_to_module: Optional[str] = os.path.abspath(__file__),
                          custom_modules_and_module_paths: Optional[dict[str, str]] = None) -> None:
        """This method registers and saves custom methods and its parameters in two distinct dictionaries. furthermore, it installs user's required packages and custom written modules.
        :param FunctionType function: FunctionType, the method signature as function !not! string
        :param Optional[dict[str,str]] params: dict[str,str], the key is the passed function's parameter definition in the signature and the value the parameter passed by the user itself, e.g. {'param_by_function_defined' : 'my_param'}
        :param Optional[List[str]] packages_to_install: List[str], in case of extra needed packages pass package name and optionally version like pandas==1.0.1
        :param Optional[str] custom_module_name: str, the custom written module's name 
        :param Optional[str] path_to_module: str, the custom written module's path, use os.path.abspath(__file__) to dynamically assign path
        :param Optional[dict] custom_modules_and_module_paths: dict, in case of multiple custom written modules, map custom module name (key) to custom module path (value) via a dictionary path; use os.path.abspath(__file__) to dynamically assign path
        :returns: nothing
        :rtype: None
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

    @staticmethod
    def __install_module(package_name: str) -> None:
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name])
