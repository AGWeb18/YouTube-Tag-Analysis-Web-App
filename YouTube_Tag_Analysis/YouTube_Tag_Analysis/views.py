"""
Routes and views for the flask application.
https://docs.microsoft.com/en-us/visualstudio/liveshare/use/vscode
"""

from datetime import datetime
from YouTube_Tag_Analysis import app
from flask import Flask, render_template, request
from YouTube_Tag_Analysis.youtube_functions import tag_finder_main
      

#TODO: Optimize API call for Quota
#TODO: Write a function to get user channel id based on text 
#TODO: Prepare search phrase for API (replace spaces)
#TODO: Hosting to launch
#TODO: Re-Design/Format Output -- closer to the PDF that we send


@app.route('/home', methods=['GET', 'POST'])
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
            #result = get_top_50_vids_details(search_phrase) 
            #multi_var_dict = tag_finder_main(search_phrase)      
            
            #TODO: connect API results to front end

            tags = ['Runescape', 'Runescape 3', 'tet gsg', 'fggih 35', 'sfhs 34', 'dgdghdg sfh 47', 'tet gsg', 'fggih 35', 'sfhs 34', 'dgdghdg sfh 47']

            top_tag_count, top_tag_vid_count = 50, 30
            competitor_top_tag_count, competitor_top_tag_vid_count = 80, 45

            num_vids = 45
            competitor_num_vid = 50

            top_tag_score = round((top_tag_count/(num_vids*10))*100, 2)
            competitor_top_tag_score = round(competitor_top_tag_count/(competitor_num_vid*10)*100,2)

            multi_var_dict = {'top_tag_score':top_tag_score, 'competitor_top_tag_score':competitor_top_tag_score}

            return render_template(
                'results.html',
                title='Home',
                errors=errors,
                search_phrase = search_phrase,
                top_tags = top_tags,
                top_tag_score = top_tag_score,
                competitor_top_tag_score = competitor_top_tag_score,
                top_tag_vid_count = top_tag_vid_count,
                num_vids = num_vids,
                competitor_num_vid = competitor_num_vid,
                data = multi_var_dict
                #top_tags = multi_var_dict['top_tags']
            )
      
    else:
        return render_template(
        'index.html',
        title='Home',
        errors=errors
    )

    
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
