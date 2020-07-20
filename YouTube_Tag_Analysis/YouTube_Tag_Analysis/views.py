"""
Routes and views for the flask application.
https://docs.microsoft.com/en-us/visualstudio/liveshare/use/vscode
"""

from datetime import datetime
from YouTube_Tag_Analysis.YouTube_Tag_Analysis import app
from flask import Flask, render_template, request, redirect, session, url_for
from YouTube_Tag_Analysis.YouTube_Tag_Analysis.youtube_functions import tag_finder_main

import google.oauth2.credentials
import google_auth_oauthlib.flow
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_secret_file = '/app/YouTube_Tag_Analysis/YouTube_Tag_Analysis/data.json'
scopes = ['https://www.googleapis.com/auth/youtube']

#COMPLETE: Optimize API call for Quota ---July 6th: Minimum Total call cost = ~220 units
#COMPLETE: July 09: connect API results to front end
#COMPLETE: Prepare search phrase for API (replace spaces)
#COMPLETE: Rename routing
#COMPLETE: Write a function to get user channel id based session variables
#COMPLETE: Home Page - Create template Page. Copy Home.

#TODO: Get App verified 
#TODO: Hosting to launch
#TODO: Re-Design/Format Output -- closer to the PDF that we send
#TODO: Restrict number of free searches

#AR TODO
#TODO: What's a score? how did we calculate it?
#TODO: Home Page - How do tags work? Short explanation of process.            

#GA TODO


@app.route('/search', methods=['GET', 'POST'])
def search():
    errors = ''
    if request.method == 'POST':
        search_phrase = None

        try:
            search_phrase = request.form['search_phrase']
        except:
            errors += '<p>{!r} is not a valid search phrase.</p>\n'.format(request.form['search_phrase'])

        if search_phrase is not None:

            credentials = google.oauth2.credentials.Credentials(**session['credentials'])

            main_results = tag_finder_main(credentials, search_phrase)
                     
            full_vid_response = main_results['full_vid_response']
            top_tags = main_results['top_tags']
            
            competitor_num_vid = main_results['competitor_num_vid']
            num_vids = main_results['num_vids']
    
            top_tag_count, top_tag_vid_count = main_results['top_tag_count'], main_results['top_tag_vid_count'] 
            competitor_top_tag_count, competitor_top_tag_vid_count =  main_results['competitor_top_tag_count'], main_results['competitor_top_tag_vid_count']



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
            )
      
    else:

        #flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes, redirect_uri='http%3A%2F%2Flocalhost%3A1818') #redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        #credentials = flow.run_console()

        #authurl  = flow.authorization_url(prompt='consent', include_granted_scopes='true',access_type='offline')

        #flow.run_local_server()

        #session = flow.authorized_session()

        #profile_info = session.get('https://www.googleapis.com/userinfo/v2/me').json()
        if 'credentials' not in session:
            return redirect('/authorize')
        else:
            return render_template(
            'search.html',
            title='Search',
            errors=errors
    )

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      client_secret_file, scopes=scopes)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  session['state'] = state

  return redirect(authorization_url)



@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      client_secret_file, scopes=scopes, state=state)
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)

  return redirect(url_for('search'))


@app.route('/')
@app.route('/landing')
def landing():
    
    return render_template(
                'landing.html',
                title='Home'                
                )
    
