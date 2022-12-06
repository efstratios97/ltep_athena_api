import pytest

from flask import Flask
from ltep_athena_api.athena_api import AthenaAPI
from ltep_athena_api.models.CustomHTMLDocument import CustomHTMLDocument
import ltep_athena_api.microservice as ms
from mockito import when


class TestDataWorkflowExternalAPI:

    @staticmethod
    @pytest.mark.parametrize("test_data", [{
        'func_name': 'my_test_function_returning_custom_html_document',
        'html': '<p>Hi<p>',
        'script': '''function() => () {{
            console.log('hi');
        }}''',
        'stylesheet_ref': 'https://my.stylesheet.com'
    }])
    def test_workflow_operation_creation(test_flask_app: Flask, test_data: dict):
        def my_test_function_returning_custom_html_document(*args):
            return CustomHTMLDocument(html=test_data.get('html'), script=test_data.get('script'), stylesheet_ref=test_data.get('stylesheet_ref'))
        print('')
        athena_api: AthenaAPI = AthenaAPI()
        athena_api.register_function(
            my_test_function_returning_custom_html_document)
        when(ms).get_global_athena_api_instance().thenReturn(athena_api)
        response: dict = test_flask_app.test_client().get(
            '/api/v1/athenarestapi/execute/my_test_function_returning_custom_html_document').get_json(force=True)
        assert response.get('result').get('css') == test_data.get('css')
        assert response.get('result').get('html') == test_data.get('html')
        assert response.get('result').get(
            'javascript_library_ref') == test_data.get('javascript_library_ref')
        assert response.get('result').get('script') == test_data.get('script')
        assert response.get('result').get(
            'stylesheet_ref') == test_data.get('stylesheet_ref')
