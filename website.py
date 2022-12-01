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

app.layout = html.Div(
    [
        html.H1("File Browser"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H2("File List"),
        html.Ul(id="file-list"),
        html.Link()
    ],
    style={"max-width": "500px"},
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
        return [html.Li("The submitted file is not a pdf. Please upload a pdf file")]
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