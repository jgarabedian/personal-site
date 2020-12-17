from flask import Flask, render_template, url_for, request, redirect
from jinja2 import TemplateNotFound
from pyisemail import is_email
import email_sender
import json
# export FLASK_APP=server.py
# export FLASK_ENV=development

app = Flask(__name__)


def get_projects() -> list:
    """
    Get the projects to show on the projects page

    :return: list
    """
    with open("projects.json") as f:
        data = json.loads(f.read())
    return [d for d in data if d['published']]


# constant
PROJECTS = get_projects()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/project/<string:proj_name>')
def project_page(proj_name):
    # first - find the project
    proj, idx = next(((proj, idx) for idx, proj in enumerate(PROJECTS) if proj['url'] == proj_name), None)
    prev_proj = PROJECTS[idx-1]
    next_proj = PROJECTS[idx+1] if idx+1 < len(PROJECTS) else PROJECTS[0]
    # make it easier for bottom nav bar

    indexes = [(len(PROJECTS) if idx == 0 else idx), idx+1]
    indexes.append(1 if idx+1 == len(PROJECTS) else idx+2)

    if proj:
        return render_template('project-base.html', project=proj, index=indexes, last=prev_proj, next=next_proj, )
    else:
        flash('This doesn\'t exist anymore')
        return render_template('project.html', projects=PROJECTS)


@app.route('/contact', methods=['GET', 'POST'])
def contact_me():
    err = None
    data = None
    if request.method == 'POST':
        try:
            # validate email then submit
            data = request.form.to_dict()
            if check_email(data['email']):
                print('Valid email, sending...')
                if email_sender.send_email(data):
                    return render_template('thank-you.html', name=data['name'])
                else:
                    err = 'Unsuccessful submission. Try again'
                    return render_template('contact.html', error=err, data=data)
            else:
                err = 'Invalid email - try again.'
                return render_template('contact.html', error=err, data=data)
        except:
            err = 'Unsuccessful submission. Try again'
            return render_template('contact.html', error=err, data=data)
    else:
        return render_template('contact.html', error=err, data=data)


@app.route('/<string:page_name>')
def page(page_name):
    """
    Render a page from the name
    :param page_name: Name of index html
    :return: html of page
    """
    try:
        if page_name == 'project':
            return render_template('project.html', projects=PROJECTS)
        return render_template(f'{page_name}.html')
    except TemplateNotFound as err:
        print(f'{err} is the culprit')
        return render_template('404.html', err=err)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', err=e), 404


def check_email(email: str):
    return is_email(email, check_dns=True)




