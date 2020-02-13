import json
from flask import Flask, render_template, request, jsonify
import requests
from datetime import date, timedelta

# Find the date of one month ago in the format (YYYY-MM-DD)
current_date = date.today().isoformat()
days_before = (date.today() - timedelta(days=30)).isoformat()

app = Flask(__name__)

# Initializing variables
languages = ''
languages_s = []
languages_split = []
repos = ''


###################################################################################################################
# This url gives the number of repositories that use a language ( among the most trending repositories since 30 days
# ago)
@app.route('/api/repositories/number/<lang>', methods=['GET'])
def number_repositories(lang):
    # Fetch the most trending repositories that use the language 'lang'
    r = requests.get(
        'https://api.github.com/search/repositories?q=language:' + str(lang) + '+created:>' + days_before + '&sort'
                                                                                                            '=stars'
                                                                                                            '&order'
                                                                                                            '=desc'
                                                                                                            '&page=1')
    content = json.loads(r.content.decode('utf-8'))
    if r.status_code != 200:  ##### Handle an error
        return jsonify({
            'status': 'error',
            'message': "The request to Github's API has failed : ".format(
                content['message'])
        }), 500
    json_object = r.json()
    number = json_object['total_count']
    # Put the result in a dictionary
    result = {'number_repos': number}
    return result


###################################################################################################################
# This url gives the names of the repositories that use a certain language ( among the most trending ones )
@app.route('/api/repositories/<lang>', methods=['GET'])
def my_respositories_lang(lang):
    r = requests.get(
        'https://api.github.com/search/repositories?q=language:' + str(lang) + '+created:>' + days_before + '&sort'
                                                                                                            '=stars'
                                                                                                            '&order'
                                                                                                            '=desc'
                                                                                                            '&page=1')
    content = json.loads(r.content.decode('utf-8'))
    if r.status_code != 200:  ##### Handle an error
        return jsonify({
            'status': 'error',
            'message': "The request to Github's API has failed : ".format(
                content['message'])
        }), 500

    json_object = r.json()

    for item in json_object['items']:
        global repos
        repos += str(item['name']) + '<br></br>'
        repository_list = list(repos.split("<br></br>"))  # convert the string to a list

    # Fill the dictionary with the items
    result = {}
    i = 0
    for element in repository_list:
        case = {'repository_name': element}
        result[i] = case
        i += 1
    return result


###################################################################################################################
# This url gives the list of the trending repositories in order
@app.route('/api/trending_repos')
def get_trending_repos():
    # Get the first 100 trending repos from github's api
    r = requests.get(
        'https://api.github.com/search/repositories?q=created:>' + days_before + '&sort=stars&order=desc&per_page'
                                                                                 '=100&page=1')

    json_object = r.json()
    ########################################
    content = json.loads(r.content.decode('utf-8'))
    if r.status_code != 200:  ##### Handle an error
        return jsonify({
            'status': 'error',
            'message': "The request to Github's API has failed : ".format(
                content['message'])
        }), 500

    # If no error, return the result
    j = 0
    for item in json_object['items']:  # Extraction of the languages used by each item in the json list
        global languages
        languages += str(item['language']) + '<br></br>'
        global languages_s
    languages_s = list(languages.split("<br></br>"))  # convert the string 'languages' into a list

    global languages_split
    for element in languages_s:  # Eliminate redundant elements in language_s and add them to a new list
        if element not in languages_split:
            languages_split.append(element)
    ###

    ###
    result = {}
    # Adding list as value
    i = 0
    for element in languages_s:
        case = {'language_name': element}
        result[i] = case
        i += 1

    return result


if __name__ == '__main__':
    app.run(debug=True)
