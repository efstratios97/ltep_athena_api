import pytest
from pytest import FixtureRequest

from ltep_athena_api.authenticate import AthenaAuth
from ltep_athena_api.athena_api import AthenaAPI
from ltep_athena_api.constants import EVENT_LISTENER_FUSIONCHART_LABEL_VALUE

import random_word


@pytest.fixture()
def input_athena_api_instance() -> AthenaAPI:
    return AthenaAPI()


@pytest.fixture()
def input_athena_auth() -> AthenaAuth:
    return AthenaAuth("http://127.0.0.1:5000", developer_token="test_token",
                      developer_name="adminDev", email="super@user.admin", host_api_address_sandbox="http://localhost:27000", host_api_address_streaming="ws://localhost:27097")


@pytest.fixture()
def input_event_name() -> str:
    return random_word.RandomWords().get_random_word()


@pytest.fixture()
def input_fusion_chart() -> dict:
    return {
        "id": "stockRealTimeChart",
        "type": 'realtimeline',
        "width": '700',
        "height": '400',
        "dataFormat": 'json',
        "dataSource": {
            "chart": {
                "caption": "Real-time stock price monitor",
              "subCaption": "Harry's SuperMart",
              "xAxisName": "Time",
              "yAxisName": "Stock Price",
              "numberPrefix": "$",
              "refreshinterval": "5",
              "yaxisminvalue": "35",
              "yaxismaxvalue": "36",
              "numdisplaysets": "10",
              "labeldisplay": "rotate",
              "showRealTimeValue": "0",
              "theme": "fusion"
            },
            "categories": [{
                "category": [{
                    "label": "Day Start"
                }]
            }],
            "dataset": [{
                "data": [{
                    "value": "35.27"
                }]
            }]
        }
    }


@pytest.mark.parametrize("fusion_chart_data, athena_api_instance, auth, event_name", [["input_fusion_chart", "input_athena_api_instance", "input_athena_auth", "input_event_name"]])
def test_fusionchart_data_preprocessing(fusion_chart_data, athena_api_instance, auth, event_name, request: FixtureRequest):
    event_name = request.getfixturevalue(event_name)
    auth: AthenaAuth = request.getfixturevalue(auth)
    athena_api: AthenaAPI = request.getfixturevalue(athena_api_instance)
    sut: dict = request.getfixturevalue(fusion_chart_data)
    processed_sut: dict = athena_api.preprocessing_fusionchart_real_time(
        complete_fusionchart_data=sut, event_name=event_name, auth=auth)
    assert processed_sut.get("events").get(
        "initialized") == EVENT_LISTENER_FUSIONCHART_LABEL_VALUE.format(chart_id=event_name, streaming_host=auth.host_api_address_streaming)
    assert processed_sut.get("id") == event_name
