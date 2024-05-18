import markdown2
import os
import time
from flask import Flask, render_template, send_from_directory
from os.path import exists, join

MD_DIR = '/home/ec2-user/docs'
FRONTPAGE_TITLE = 'kmrasmussen markdown docs'
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
    filename = join(MD_DIR, filename)
    if not os.path.exists(filename):
        return "File not found", 404
    with open(filename, 'r') as f:
        md_content = f.read()
    html_content = markdown2.markdown(md_content, extras=["fenced-code-blocks", "code-friendly", "code-color"])
    return render_template('doc.html', content=html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
