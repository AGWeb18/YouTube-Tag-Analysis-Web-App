"""
Routes and views for the flask application.
https://docs.microsoft.com/en-us/visualstudio/liveshare/use/vscode
"""

from datetime import datetime
from YouTube_Tag_Analysis import app
from flask import Flask, render_template, request
from YouTube_Tag_Analysis.youtube_functions import get_top_50_vids_details

@app.route('/', methods=['GET', 'POST'])
def home():
    errors = ''
    if request.method == 'POST':
        search_phrase = None

        try:
            search_phrase = request.form['search_phrase']
        except:
            errors += '<p>{!r} is not a valid search phrase.</p>\n'.format(request.form['search_phrase'])

        if search_phrase is not None:
            result = get_top_50_vids_details(search_phrase)
            
            return '''
                <html>
                    <body>
                        <h1>The top videos are shown below:</h1>
						<p>{result}</p>
                        <p><a href="/">Click here to search again</a>
                    </body>
                </html>
            '''.format(result=result.to_html())
    else:
        return '''
            <html>
                <body>
                    {errors}
                    <p>Enter your YouTube search phrase:</p>
                    <form method="post" action=".">
                        <p><input name="search_phrase" /></p>
                        <p><input type="submit" value="Search" /></p>
                    </form>
                </body>
            </html>
        '''.format(errors=errors)




"""
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )



@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

"""
