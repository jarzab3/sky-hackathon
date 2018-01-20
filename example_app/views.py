from django.views.generic.base import TemplateView
from django.shortcuts import render, render_to_response, reverse, redirect
from django.http import HttpResponse

from example_app.main import FAQBot as fa

# from example_app.models import *

from example_app.models import User

from example_app.models import Problems

my_bot = fa()

import simplejson

questionIndex = 0
issue = []
person = []

def displayAnswer(request):
    json_list = simplejson.dumps("")
    return render(request, 'app.html', {'data': json_list})

def json_page(request):
    global questionIndex
    global issue
    global person

    data = str(request.GET["user_input"])

    # Get user data
    if questionIndex == 2:
        person.append(data)
    elif questionIndex == 3:
        issue.append(data)
    elif questionIndex == 4:
        issue.append(data)
    # elif questionIndex == 5:
    #     issue.append(data)

    data = my_bot.respond_to_user_request(data)

    # Save user data to db
    if(questionIndex == 3):
        personTosave = User(name=person[0], surname = "unknown", postcode = "unknown")
        personTosave.save()

    if (questionIndex == 4):
        issueToSave = Problems(title=issue[0], problemDescription=issue[1])
        issueToSave.save()

    json_list = simplejson.dumps(data)
    html = str(json_list)
    questionIndex = questionIndex + 1
    return HttpResponse(html)

def saveProblem():

    problems = Problems.objects.all()

    p = Problems(name="Fred Flintstone", shirt_size="L")

    p.save()

def chat_state(request):
	data = my_bot.get_chat_state()
	json_list = simplejson.dumps(data)
	html = str(json_list)
	return HttpResponse(html)

def reset_chat(request):
    my_bot.reset_chat()
    data = [0];
    json_list = simplejson.dumps(data)
    html = str(json_list)
    return HttpResponse(html)

