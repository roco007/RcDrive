import os
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
import os
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI()

class FileStorage:
    def __init__(self):
        self.storage_path = 'Upload'

    def store_file(self, file: UploadFile, name_or_id: str):
        file_extension = self.get_file_extension(file.filename)
        file_type = self.get_file_type(file_extension)
        file_directory = os.path.join(self.storage_path, file_type)
        os.makedirs(file_directory, exist_ok=True)
        file_path = os.path.join(file_directory, name_or_id + file_extension)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    def get_file_type(self, file_extension: str):
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'images'
        elif file_extension in ['.mp4', '.avi', '.mov']:
            return 'videos'
        elif file_extension in ['.doc', '.docx', '.txt']:
            return 'documents'
        elif file_extension in ['.mp3', '.wav']:
            return 'audio'
        elif file_extension == '.pdf':
            return 'pdf'
        elif file_extension == '.zip':
            return 'zip'
        elif file_extension == '.csv':
            return 'csv'
        elif file_extension in ['.xls', '.xlsx']:
            return 'excel'
        elif file_extension == '.ppt':
            return 'powerpoint'
        elif file_extension == '.json':
            return 'json'
        elif file_extension == '.xml':
            return 'xml'
        elif file_extension == '.html':
            return 'html'
        else:
            return 'others'

    def get_file_extension(self, name_or_id: str):
        return os.path.splitext(name_or_id)[1].lower()

@app.post('/upload-file')
async def upload_file(file: UploadFile = File(...), name_or_id: str = Form(...)):
    file_storage = FileStorage()
    file_storage.store_file(file, name_or_id)
    
    html_content = """
    <html>
    <head>
        <title>Upload Success</title>
    </head>
    <body>
        <h1>Upload Successful</h1>
        <p>Your file has been uploaded successfully.</p>
        <button onclick="location.href='/'">Go to Homepage</button>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/files')
async def get_files():
    file_storage = FileStorage()
    files = []
    for root, dirs, filenames in os.walk(file_storage.storage_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_name = os.path.basename(file_path)
            files.append((file_name, file_path))
    
    html_content = """
    <html>
    <head>
        <title>File Structure</title>
    </head>
    <body>
        <h1>File Structure</h1>
        <ul>
    """
    
    for file_name, file_path in files:
        html_content += f'<li><a href="/download-file/{file_path}">{file_name}</a></li>'
    
    html_content += """
        </ul>
         <button onclick="location.href='/'">Go to Homepage</button>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/download-file/{file_path:path}')
async def download_file(file_path: str):
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))

@app.get('/')
async def homepage():
    html_content = """
    <html>
    <head>
        <title>File Management</title>
    </head>
    <body>
        <h1>Welcome to File Management</h1>
        <button onclick="location.href='/upload'">Upload</button>
        <button onclick="location.href='/files'">Download</button>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/upload')
async def upload_page():
    html_content = """
    <html>
    <head>
        <title>Upload File</title>
    </head>
    <body>
        <h1>Upload File</h1>
        <form action="/upload-file" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br><br>
            <input type="text" name="name_or_id" placeholder="Name or ID" required><br><br>
            <input type="submit" value="Upload">
        </form>
        <button onclick="location.href='/'">Go to Homepage</button>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
