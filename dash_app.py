import dash

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"},{'http-equiv': 'content-language',
                    'content': 'pt-br'}], suppress_callback_exceptions=True
)