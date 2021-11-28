import json
from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from OnlineJudge.mongo.api import MonitoringClusterConnection
from collections import namedtuple
import uuid

ProblemData = namedtuple('ProblemData', 'name statement time_limit memory_limit testcases answer')
AssignmentData = namedtuple('AssignmentData', 'problems')


def display_home_page(request):
    if request.method != 'GET':
        return
    else:
        return render(request, 'OnlineJudge/homepage.html')


def show_add_problem_page(request):

    if request.method != "GET":
        return
    else:
        return render(request, 'OnlineJudge/add_problem.html')


def create_problem(request):

    if request.method != 'POST':
        return
    else:
        body = json.loads(request.body)
        db = MonitoringClusterConnection.get_instance()
        data = ProblemData(**body)
        collection = db.problem
        problem_id = uuid.uuid4()
        collection.insert({'name': data.name,
                           'statement': data.statement,
                           'time_limit': data.time_limit,
                           'memory_limit': data.memory_limit,
                           'testcases': data.testcases,
                           'problem_id': problem_id,
                           'answer': data.answer})

        return JsonResponse({'problem_id': problem_id})


def add_assignment(request):
    if request.method != 'GET':
        return
    else:
        return render(request, 'OnlineJudge/add_assignment.html')


def display_assignment(request):

    if request.method != 'POST':
        return
    else:
        assignment_id = request.GET['assignment_id']
        db = MonitoringClusterConnection.get_instance()
        collection = db.problem
        assignment = collection.find({'assignment_id': assignment_id})
        return render(request, 'OnlineJudge/show_assignment.html', {'problem_id_1': assignment['problem'][0],
                                                        'problem_id_2': assignment['problem'][1],
                                                        'problem_id_3': assignment['problem'][2]})


def attempt_problem(request):
    if request.method != 'GET':
        return
    else:
        return render(request, 'OnlineJudge/attempt_problem.html')


def attempt_assignment(request):
    if request.method != 'GET':
        return
    else:
        return render(request, 'OnlineJudge/attempt_assignment.html')

def create_assignment(request):
    if request.method != 'POST':
        return
    else:
        body = json.loads(request.body)
        db = MonitoringClusterConnection.get_instance()
        data = AssignmentData(**body)
        collection = db.assignment
        assignment_id = uuid.uuid4()
        collection.insert({'problems': data.problems,
                           'assignment_id': assignment_id})

        return JsonResponse({'assignment_id': assignment_id})


def get_problem(request):
    if request.method != 'POST':
        return
    else:
        body = json.loads(request.body)
        problem_id = body['problem_id']
        db = MonitoringClusterConnection.get_instance()
        collection = db.problem
        problem = collection.find({'problem_id': problem_id})
        return JsonResponse({'problem': problem})


def display_problem(request):
    if request.method != 'GET':
        return
    else:
        from urllib.parse import urlparse
        from urllib.parse import parse_qs
        # parsed_url = urlparse(request.url)
        # problem_id = parse_qs(parsed_url.query)['problem_id'][0]
        problem_id = request.GET['problem_id']
        db = MonitoringClusterConnection.get_instance()
        collection = db.problem
        problem = list(collection.find({'problem_id': uuid.UUID(problem_id)}))
        return render(request, 'OnlineJudge/show_problem.html', context=problem[0])


def get_results(request):
    if request.method != 'POST':
        return
    else:
        body = json.loads(request.body)
        code = body['code']
        problem_id = body['problem_id']

        with open('OnlineJudge/inputs/solution.cpp', 'w') as f:
            f.write(code)
            f.close()

        db = MonitoringClusterConnection.get_instance()
        collection = db.problem
        problem = list(collection.find({'problem_id': uuid.UUID(problem_id)}))

        with open('OnlineJudge/inputs/input.txt', 'w') as f:
            f.write(problem[0]['testcases'])
            f.close()
        import subprocess
        if subprocess.call(["g++", "OnlineJudge/inputs/solution.cpp"], shell=True) == 0:
            subprocess.call(["./a.out <'OnlineJudge/inputs/input.txt' >'inputs/output.txt'"], shell=True)
        else:
            return JsonResponse({'status': "compilation error"})

        with open('inputs/output.txt', 'r') as f:
            output = f.read()
            f.close()

        if "\n".join([s for s in output.split("\n") if s]) == problem[0]['answer']:
            return JsonResponse({'status': "accepted"})
        else:
            return JsonResponse({'status': 'wrong answer'})


