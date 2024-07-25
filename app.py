import logging
from flask import Flask, request, render_template, redirect, url_for, session, send_file
from google.cloud import storage
import os
import io

app = Flask(__name__)
app.secret_key = os.environ.get('a9b8c7d6e5f4a3b2c1d0e9f8d7c6b5a4') 

# User credentials (Ideally from a secure database)
users = {'tharun': 'venky@1245', 'prem': 'venky@12345', 'theja': 'sunny@6163'}

# Google Cloud Storage configuration
bucket_name = os.environ.get('processed_data112') 

def list_blobs_with_prefix(bucket_name, prefix):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    return blobs

@app.route('/')
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        app.logger.error(f"Error in login route: {e}")
        return "An error occurred", 500

@app.route('/login', methods=['POST'])
def do_login():
    try:
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('bucket'))
        else:
            return 'Invalid credentials'
    except Exception as e:
        app.logger.error(f"Error in do_login route: {e}")
        return "An error occurred", 500

@app.route('/bucket')
def bucket():
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
        blobs = list_blobs_with_prefix(bucket_name, '')
        return render_template('bucket.html', blobs=blobs)
    except Exception as e:
        app.logger.error(f"Error in bucket route: {e}")
        return "An error occurred", 500

@app.route('/folder/<path:folder_name>')
def folder(folder_name):
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
        blobs = list_blobs_with_prefix(bucket_name, folder_name)
        return render_template('folder.html', blobs=blobs, folder_name=folder_name)
    except Exception as e:
        app.logger.error(f"Error in folder route: {e}")
        return "An error occurred", 500

@app.route('/download/<path:blob_name>')
def download(blob_name):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Download the blob into memory
        file_stream = io.BytesIO()
        blob.download_to_file(file_stream)
        file_stream.seek(0)  # Reset the stream position

        # Determine content type (optional, but good practice)
        content_type = blob.content_type or 'application/octet-stream'

        # Send the file to the user
        return send_file(file_stream, as_attachment=True, 
                         download_name=blob.name, mimetype=content_type)
        
    except Exception as e:
        app.logger.error(f"Error in download route: {e}")
        return "An error occurred while downloading the file.", 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Optional for debugging
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))) 
