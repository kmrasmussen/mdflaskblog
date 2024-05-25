import markdown2
import os
import time
from flask import Flask, render_template, send_from_directory, request
from os.path import exists, join
from config import *

assert exists(MD_DIR)
app = Flask(__name__)

@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')

def get_md_files():
    md_files = [f for f in os.listdir(MD_DIR) if f.endswith('.md')]
    file_info = []
    for file in md_files:
        stat = os.stat(join(MD_DIR,file))
        created = time.strftime("%B %d, %Y", time.localtime(stat.st_ctime))
        modified = time.strftime("%B %d, %Y", time.localtime(stat.st_mtime))
        file_info.append({
            'name': file,
            'created': created,
            'modified': modified,
            'url': f'/doc/{file}'
        })
    return file_info

@app.route('/')
def index():
    files = get_md_files()
    return render_template('index.html', files=files, frontpage_title=FRONTPAGE_TITLE)

@app.route('/doc/<filename>')
def doc(filename):
    access_key = request.args.get('access_key')
    print(f"access_key: {access_key}")
    filename = join(MD_DIR, filename)
    if not os.path.exists(filename):
        return "File not found", 404
    with open(filename, 'r') as f:
        md_content = f.read()
    
    if md_content.startswith("password: "):
        md_firstline = md_content.split("\n")[0]
        password = md_firstline.split(": ")[1].strip()
        print('checking password', repr(access_key), repr(password), '|')
        if access_key != password:
            return "Access Denied", 403
        md_content = "\n".join(md_content.split("\n")[1:])
    
    html_content = markdown2.markdown(md_content, extras=["fenced-code-blocks", "code-friendly", "code-color"])
    return render_template('doc.html', content=html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
