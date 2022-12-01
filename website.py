import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pdf2audio

UPLOAD_DIRECTORY = "uploaded_files"
CONVERTED_DIRECTORY = "converted_audios"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if not os.path.exists(CONVERTED_DIRECTORY):
    os.makedirs(CONVERTED_DIRECTORY)

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(CONVERTED_DIRECTORY, path, as_attachment=True)



app.layout = html.Header(
    [   

        html.H1("PDF2AUDIO",style={"color":"#F7EBE8",
                                   "textAlign":"center",
                                   "font-size":"50px",
                                   "font-family":"Helvetica, Sans-Serif",
                                   "background-color": "#1E1E24",
                                   "height":"150px",
                                   "width": "50%",
                                   "margin-left":"auto",
                                   "margin-right":"auto",
                                   "border-radius":"5px",
                                   "line-height":"150px",
                                   "borderStyle":"solid"}),
        html.H2("Upload your file",style={"textAlign":"center","color":"#1E1E24","font-size":"30px","font-family":"Helvetica, Sans-Serif"}),
        html.Div([
            dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            multiple=True,
            ),
        ],style={"margin-left":"auto",
                "margin-right":"auto",
                "width": "75%",
                "height": "150px",
                "font-size": "20px",
                "lineHeight": "150px",
                "borderWidth": "3px",
                "borderStyle": "dashed",
                "margin-left":"auto",
                "margin-right":"auto",
                "borderRadius": "5px",
                "textAlign": "center",
                "background-color":"#444140",
                "color":"#F7EBE8"}),
        html.Div([
            html.H2("File List",style={"textAlign": "center","font-family":"Helvetica, Sans-Serif","text-decoration":"underline"}),
            html.Ul(id="file-list",style={"font-family":"Helvetica, Sans-Serif"}),
        ],style={
            "background-color":"#D4BEBE",
            "width":"60%",
            "height":"200px",
            "margin-left":"auto",
            "margin-right":"auto",
            "border-radius":"4px"
        }),
        html.Link()
    ],
)

# (1)
# Callback for app
# Output to Ul element in app
# Input from upload element
@app.callback(
    Output("file-list", "children"),
    Input("upload-data", "filename"),
    Input("upload-data", "contents")
)

# (2), (4), (6)
# Deal with inputs automatically
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    # If there is something in uploaded files and uploaded file contents, save the file
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
    # (2) -> (3)
    # (3) -> (4)

    files = uploaded_files()
    # (4) -> (5)
    # (5) -> (6)
    error = 0
    if len(files)>0:
        error = pdf2audio.audioconvert(files[0])
    
    if error == -1:
        return [html.Li("File too big, please try a smaller file")]
    elif error == -2:
        return [html.Li("The submitted file is not a pdf. PLease upload a pdf file")]
    elif error == -3:
        return [html.Li("Miscellaneous error, try again later")]

    audio_files = converted_audios()

    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in audio_files]

# decode and save file in folder path (Editors note: no need to change)
def save_file(name, content):
    # Decode fro bnary to utf-8
    # Save in folder.
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

# Create list of files in the directory and return it
def uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

# Create list of audio files
def converted_audios():
    files = []
    for filename in os.listdir(CONVERTED_DIRECTORY):
        path = os.path.join(CONVERTED_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

# To create a html link item to enable dowload
def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)