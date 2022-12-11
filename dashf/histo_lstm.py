from dash import Dash, dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import pandas as pd
from .dashn import Dash
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pymongo
from keras.models import load_model



clinet=pymongo.MongoClient("mongodb+srv://admin:H1IbFaRWkbw4nLpL@metatradeer.v87htex.mongodb.net/test")
db=clinet["metatrader"]
data=db['metatrader5']
list_c=list(data.find())
rates_frame=pd.DataFrame(list_c)

#rates_frame=rates_frame.set_index('time')
rates_frame=rates_frame.drop(columns=['_id'])

df = rates_frame



header = html.H4(
    "Historical Volatility", className="bg-primary text-white p-2 mb-2 text-center"
)

table = dash_table.DataTable(
    id="table",
    columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
    data=df.to_dict("records"),
    page_size=10,
    editable=True,
    cell_selectable=True,
    filter_action="native",
    sort_action="native",
    style_table={"overflowX": "auto"},
    row_selectable="multi",
)

MODEL_PATH = 'histo_model_f.h5'
model = load_model(MODEL_PATH)
training_set = rates_frame.iloc[:, 1:2].values

sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)


X_test = []
for i in range(700 , 1251):
 X_test.append(training_set_scaled[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
pred=model.predict(X_test)

data=rates_frame[700:1251]
data['train']=training_set_scaled[700:1251]
data['pred']=pred
print(df.time)

tab1 = dbc.Tab([dcc.Graph(id="line-chart", figure={'data':[{'y':df.close}]}), ], label="Close Volatility" )
tab2 = dbc.Tab([dcc.Graph(id="line-chart2" , figure={'data':[{'y':data.pred ,'name':'Pred'}, {'y':data.train,'name':'True'}   ]}   ) , ], label="Predict Close Volatility ( LSTM)")
tab3 = dbc.Tab([table], label="Table", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))

app_layout = dbc.Container(
        [
            header,
            dbc.Row(
                [
                    dbc.Col(
                        [


                            ThemeChangerAIO(aio_id="theme")
                        ],
                        width=1,
                    ),
                    dbc.Col([tabs], width=8)
                    ,
                ]
            ),
        ],
        fluid=True,
        className="dbc dbc-row-selectable",
    )






def init_dash(server):
    """Create a Plotly Dash dashboard."""
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    dash_app = Dash(__name__,server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css] , routes_pathname_prefix="/histo_lstm/", )


    dash_app.layout = app_layout







    return dash_app.server


if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    init_callbacks(app)
    app.run_server(debug=True, port=8080)
