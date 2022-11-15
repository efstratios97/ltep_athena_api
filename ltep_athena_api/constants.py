MAIN_DATASET_DATAFRAME = "main_dataset_df"
MAIN_DATASET = "main_dataset"
OUTPUT_METHOD_REST_API = "Save Dataset to external system via Rest-Call"
OUTPUT_METHOD_WATCHFOLDER = "Save Dataset to external Filesytem Location"

DATASTREAM_NAME_SPACE_LTEP_ATHENA_SERVICE = "/api/v1/stream/data"
EVENT_NAME_KEY = "event_name_id"
EVENT_DATA_KEY = "event_data"
EVENT_DATASTREAM_NAME_SPACE = "/ws"

EVENT_LISTENER_FUSIONCHART_LABEL_VALUE = """function(io_) {{
              function updateData(io_) {{
                var socket = io_("{streaming_host}"""+EVENT_DATASTREAM_NAME_SPACE+'"'+""", {{ path: "/ws/socket.io/", transports: ['websocket'], upgrade: false}});
                socket.on("{chart_id}", (data) => {{
                  console.log("socket: event received!");
                  var parsed_data = JSON.parse(String.fromCharCode.apply(null, new Uint8Array(data)));
                  let chartRef = FusionCharts("{chart_id}");
                  console.log(chartRef);
                  console.log(parsed_data);
                  let strData = "&label=" + parsed_data.label + "&value=" + parsed_data.value;
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
