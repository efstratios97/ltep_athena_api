MAIN_DATASET_DATAFRAME = "main_dataset_df"
MAIN_DATASET = "main_dataset"
OUTPUT_METHOD_REST_API = "Save Dataset to external system via Rest-Call"
OUTPUT_METHOD_WATCHFOLDER = "Save Dataset to external Filesytem Location"

DATASTREAM_NAME_SPACE_LTEP_ATHENA_SERVICE = "/api/v1/stream/data"
EVENT_NAME_KEY = "event_name_id"
EVENT_DATA_KEY = "event_data"
EVENT_DATASTREAM_NAME_SPACE = "/ws"
INTERNAL_HOST_ADDRESS = None

EVENT_LISTENER_FUSIONCHART_LABEL_VALUE = """function(io_) {{
              function updateData(io_) {{
                var socket = io_("{streaming_host}"""+EVENT_DATASTREAM_NAME_SPACE+'"'+""", {{ path: "/ws/socket.io/", transports: ['websocket'], upgrade: false}});
                socket.on("{chart_id}", (data) => {{
                  console.log("socket: event received!");
                  var parsed_data = JSON.parse(String.fromCharCode.apply(null, new Uint8Array(data)));
                  let chartRef = FusionCharts("{chart_id}");
                  var strData = "";
                  Object.entries(parsed_data).forEach(([key, value]) => {{
                        strData += "&"+ key + "=" + value;
                  }});
                  chartRef.feedData(strData);
                }});
                socket.on('disconnect', function() {{
                  console.log("socket: disconneted!");
                  socket.disconnect();
                  socket.open();
                }});
               socket.once('connect', function() {{
                  console.log("socket: connected!");
                }});
              }}
              updateData(io_);
              }}"""

EVENT_LISTENER_FUSIONCHART_BEFORE_RENDER = """function (evt, args) {{
            var chartRef = evt.sender;
            chartRef.showMessageLog = function () {{
              chartRef.showLog();
            }};
             chartRef.makeCaptionLeft  = function () {{
             console.log("http://{api_address}" + "/api/v1/athenarestapi/execute/{func_name}");
              let response = fetch("http://{api_address}" + "/api/v1/athenarestapi/execute/{func_name}",  {{
              method: 'GET'}});
            }};
            var btnContainer = document.createElement('div'),
              str;
            str = '<button id="showLog" style="background-color: #007BFF; border: none; border-radius: 3px; color: white; padding: 4px 12px; text-align: center; cursor: pointer; outline: none; text-decoration: none; display: inline-block; font-size: 14px;">Show Messages</button>&nbsp&nbsp';
            str += '<button id="triggerSpecialFunction" style="background-color: #007BFF; border: none; border-radius: 3px; color: white; padding: 4px 12px; text-align: center; cursor: pointer; outline: none; text-decoration: none; display: inline-block; font-size: 14px;">{button_name}</button>&nbsp&nbsp';
            btnContainer.style.cssText = "text-align: center; width: 100%; margin: 10px;";
            btnContainer.innerHTML = str;
            args.container.parentNode.insertBefore(btnContainer, args.container.nextSibling);
          }}"""

EVENT_LISTENER_FUSIONCHART_RENDER_COMPLETE = """function (evt, args) {{
             var chartRef = evt.sender;
             var showLogBtn = document.getElementById('showLog');
             var triggerSpecialFunctionBtn = document.getElementById('triggerSpecialFunction');
            showLogBtn.onclick = chartRef.showMessageLog;
            triggerSpecialFunctionBtn.onclick = chartRef.makeCaptionLeft;
          }}"""
