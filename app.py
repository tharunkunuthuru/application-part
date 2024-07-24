from flask import Flask, request, render_template, redirect, url_for, session
from google.cloud import storage
import os

app = Flask(__name__)
app.secret_key = 'a9b8c7d6e5f4a3b2c1d0e9f8d7c6b5a4'  # Replace with the generated secret key

# Dummy credentials
users = {'tharun': '147589', 'prem': '4789545', 'theja': '478926'}

# Configure Google Cloud Storage
bucket_name = "processed_data112"

def list_blobs_with_prefix(bucket_name, prefix):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    return blobs

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('bucket'))
    else:
        return 'Invalid credentials'

@app.route('/bucket')
def bucket():
    if 'username' not in session:
        return redirect(url_for('login'))
    blobs = list_blobs_with_prefix(bucket_name, '')
    return render_template('bucket.html', blobs=blobs)

@app.route('/folder/<path:folder_name>')
def folder(folder_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    blobs = list_blobs_with_prefix(bucket_name, folder_name)
    return render_template('folder.html', blobs=blobs, folder_name=folder_name)

@app.route('/download/<path:blob_name>')
def download(blob_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(expiration=3600)
    return redirect(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
