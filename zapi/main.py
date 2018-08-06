
import os
import mimetypes
from flask import Flask, request, send_file
from flask_restful import Resource, Api


FILESTORE_PATH = os.environ.get("FILESTORE_PATH", "/tmp/filestore")


app = Flask(__name__)
api = Api(app)


class File(Resource):
    def __init__(self):
        if not os.path.isdir(FILESTORE_PATH):
            os.mkdir(FILESTORE_PATH)

    def get(self, file_name):
        files = self._get_file_list()

        if file_name in files:
            mime = mimetypes.guess_type(file_name)[0]
            if not mime:
                mime = "application/octet-stream"
            return send_file(os.path.join(FILESTORE_PATH, file_name), mimetype=mime)

        return {'code': 404}

    def post(self, file_name):
        """
        Add a file to file store. We only support uploading files directly to the file store.
        This mean that we can't upload file to nested folders.
        """
        files = self._get_file_list()

        if file_name in files:
            return {'code': 400, 'msg': f'File {file_name} exists'}

        if 'file' not in request.files:
            return {'code': 400, 'msg': 'Request does not contain file content'}

        # FIXME: Be capable of upload file to nested folders
        file = request.files['file']
        file.save(os.path.join(FILESTORE_PATH, file_name))

        return {'code': '200'}

    def delete(self, file_name):
        files = self._get_file_list()

        if file_name not in files:
            return {'code': 400, 'msg': f'Cannot delete. File {file_name} does not exist'}

        os.remove(os.path.join(FILESTORE_PATH, file_name))

        return {'code': '200'}

    def _get_file_list(self):
        """
        private method to help get list of files in filestore
        """
        files = [f for f in os.listdir(FILESTORE_PATH) if os.path.isfile(os.path.join(FILESTORE_PATH, f))]
        return files


api.add_resource(File, '/<string:file_name>')


if __name__ == '__main__':
    app.run(debug=True)
