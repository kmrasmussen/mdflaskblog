# mdflaskblog

This is a simple Flask server to turn a folder with markdown files into a little blog.
Plenty of better tools exist for this kind of thing already.

Go to config.py and specify the path to the directory with the markdown files
and specify the title of the header on the frontpage and the port you want it to run on.

There is no caching:
* When hitting the frontpage /, app.py will go through all md files in MD_DIR and
list them along with when they were modified and created and link to /doc/<filename>
* When hitting /doc/<filename>, we use markdown2 to generate the HTML. Latex Math is
supported with MathJax and basic syntax highlighting with highlight.js, see /templates/doc.html.

## Password protected documents
Currently the setup for password protected docs is:

* Make the first line in the document like this: password: 1234
* When accessing the document use the GET parameter access_key, so add ?access_key=1234 to the URL.
* If they agree, the document will be shown otherwise you get 403 Access denied

See this issue
[https://github.com/kmrasmussen/mdflaskblog/issues/1](https://github.com/kmrasmussen/mdflaskblog/issues/1)