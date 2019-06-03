#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect

# Create your views here.
from .models import *
from courses.models import *
from rubrics.models import *
from accounts.models import *

# Para trabajar con queries complejas, como con negación
from django.db.models import Q


def evaluation_list(request):
    if request.method == 'POST':
        titulo = request.POST['title']
        init_date = request.POST['init_date']
        fin_date = request.POST['fin_date']
        rubric_name = request.POST['rubric']
        course_info = request.POST['course'].split('-')

        code = course_info[0]
        section = course_info[1]
        semester = course_info[2]
        year = course_info[3]

        rubric_eval = Rubric.objects.get(name=rubric_name)
        new_eval = Evaluation.objects.create(name=titulo, init_date=init_date, fin_date=fin_date, rubric=rubric_eval, state=True)
        new_eval.save()

        course_eval = Course.objects.get(code=code, section=section, semester=semester, year=year)
        new_eval_course = Evaluation_Course.objects.create(evaluation_name=new_eval, course=course_eval)
        new_eval_course.save()

        teams = Team.objects.filter(course=course_eval)

        for team in teams:
            people = Student.objects.filter(team=team)
            for student in people:
                eval = Evaluation_Student.objects.create(evaluation_id=new_eval, student=student, grade=0.0)
                eval.save()

    eval = []
    evaluations = Evaluation.objects.all().order_by('init_date')

    courses = Course.objects.all()
    rubrics = Rubric.objects.all()

    ### Seleccionar las evaluaciones, junto con la info del curso correspondiente
    for evaluation in evaluations:
        eval_course = Evaluation_Course.objects.get(evaluation_name=evaluation)
        eval.append((evaluation, eval_course))

    return render(request,'evaluation/evaluation_list.html', {'evaluations': eval,
                                                              'courses': courses,
                                                              'rubrics': rubrics})


def delete_evaluation(request):
    if request.method == 'POST':
        eval_name = request.POST['eval_name']
        code_course = request.POST['code_course']
        section_course = request.POST['section_course']
        semester_course = request.POST['semester_course']
        year_course = request.POST['year_course']

        course = Course.objects.get(code=code_course, section=section_course, semester=semester_course, year=year_course)
        del_evaluation = Evaluation.objects.get(name=eval_name)

        eval_course = Evaluation_Course.objects.get(evaluation_name=del_evaluation, course=course)
        eval_course.delete()
        del_evaluation.delete()
    eval = []
    evaluations = Evaluation.objects.all().order_by('init_date')

    courses = Course.objects.all()
    rubrics = Rubric.objects.all()

    # Seleccionar las evaluaciones, junto con la info del curso correspondiente
    for evaluation in evaluations:
        eval_course = Evaluation_Course.objects.get(evaluation_name=evaluation)
        eval.append((evaluation, eval_course))

    return render(request, 'evaluation/evaluation_list.html', {'evaluations': eval,
                                                               'courses': courses,
                                                               'rubrics': rubrics})


def evaluate(request, evaluation_id):
    evaluation = Evaluation.objects.get(id=evaluation_id)
    eval_course = Evaluation_Course.objects.get(evaluation_name=evaluation)
    course = eval_course.course

    accounts = Account.objects.all()
    evaluators = Evaluation_Account.objects.filter(evaluation_name=evaluation)
    accounts_evaluators = []
    for v in evaluators:
        accounts_evaluators.append(v.account)
    teams = Team.objects.filter(course=course)
    rubric = evaluation.rubric.get_rubric()

    ready = Evaluation_Student.objects.filter(grade__gt=0)
    ready_teams = []
    not_ready_teams = []
    for st in ready:
        team = st.student.team
    if team not in ready_teams:
        ready_teams.append(team)
    team_members = []
    for team in teams:
        if team not in ready_teams:
            not_ready_teams.append(team)
            students = Student.objects.filter(team=team)
            s = []
            for st in students:
                s.append(st.first_name + " " + st.family_name)
            team_members.append(s)
    return render(request, 'evaluation/evaluation.html', {'evaluation': evaluation,
                                                                  'course': course,
                                                                  'accounts': accounts,
                                                                  'evaluators': accounts_evaluators,
                                                                  'ready_teams': ready_teams,
                                                                  'not_ready_teams': not_ready_teams,
                                                                  'team_members': team_members,
                                                                  'rubric': rubric})


def evaluation_details(request, evaluation_id):
    evaluation= Evaluation.objects.get(id=evaluation_id)
    eval_course= Evaluation_Course.objects.get(evaluation_name=evaluation)
    course= eval_course.course

    accounts = Account.objects.all()
    evaluators = Evaluation_Account.objects.filter(evaluation_name=evaluation)
    accounts_evaluators = []
    for v in evaluators:
        accounts_evaluators.append(v.account)
    teams = Team.objects.filter(course=course)
    rubric = evaluation.rubric.get_rubric()

    ready = Evaluation_Student.objects.filter(grade__gt=0)
    ready_teams = []
    not_ready_teams = []
    for st in ready:
        team = st.student.team
        if team not in ready_teams:
            ready_teams.append(team)
    team_members=[]
    for team in teams:
        if team not in ready_teams:
            not_ready_teams.append(team)
            students = Student.objects.filter(team=team)
            s = []
            for st in students:
                s.append(st.first_name + " " + st.family_name)
            team_members.append(s)
    return render(request, 'evaluation/evaluation_details.html', {'evaluation': evaluation,
                                                                  'course': course,
                                                                  'accounts': accounts,
                                                                  'evaluators': accounts_evaluators,
                                                                  'ready_teams': ready_teams,
                                                                  'not_ready_teams': not_ready_teams,
                                                                  'team_members': team_members,
                                                                  'rubric': rubric})


def evaluation_modify(request, evaluation_id):
    evaluation= Evaluation.objects.get(id=evaluation_id)
    eval_course = Evaluation_Course.objects.get(evaluation_name=evaluation_id)

    course = eval_course.course
    rubric= evaluation.rubric
    courses=Course.objects.all();
    rubrics=Rubric.objects.all();
    otherCourses= Course.objects.filter(~Q(id=course.id))
    otherRubrics=Rubric.objects.filter(~Q(rubric=rubric))
    if request.method=='POST':
        name = request.POST['name']
        init_date = request.POST['init_date']
        fin_date = request.POST['fin_date']
        if request.POST['state']=="1":
            state= True
        else:
            state= False

        print(state)
        course= request.POST['courses']

        rubric_name= request.POST['rubric']
        rubric_eval = Rubric.objects.get(name=rubric_name)

        evaluation.name=name
        if init_date!='':
            evaluation.init_date=init_date
        if fin_date!='':
            evaluation.fin_date=fin_date
        evaluation.state=state
        evaluation.rubric=rubric_eval
        evaluation.save()

        #print(course.title)
        course_keys= course.split("-")
        coursem= Course.objects.get(code=course_keys[0], section=course_keys[1], year=course_keys[2], semester=course_keys[3])
        eval_course.delete()
        eval_course = Evaluation_Course.objects.create(evaluation_name=evaluation, course=coursem)
        #print(eval.evaluation_name)

        #new_eval_course = Evaluation_Course.objects.create(evaluation_name=evaluation, course=course)




        return redirect('/evaluation')

    return render(request, 'evaluation/evaluation_modify.html', {'evaluation': evaluation,
                                                                 'course': course,
                                                                 'otherCourses': otherCourses,
                                                                 'otherRubrics': otherRubrics,
                                                                 'courses': courses,
                                                                 'rubrics': rubrics,'rubric':rubric })


def add_evaluator(request, evaluation_id):
    evaluation = Evaluation.objects.get(id=evaluation_id)

    if request.method == 'POST':
        n_accounts = int(request.POST['number_accounts'])
        for i in range(n_accounts):
            value = 'id_eval_' + str(i)
            if value in request.POST:
                account_id = request.POST[value]
                acc = Account.objects.get(id=account_id)
                new_eval_acc = Evaluation_Account.objects.create(evaluation_name=evaluation, account=acc, count=0)
                new_eval_acc.save()

    return redirect('/evaluation/' + evaluation_id + '/')


def delete_evaluator(request, evaluation_id):
    evaluation = Evaluation.objects.get(id=evaluation_id)

    if request.method == 'POST':
        print('se recibio algo')
        evaluator_id = int(request.POST['evaluator_id'])
        evaluator = Account.objects.get(id=evaluator_id)
        print(evaluator)
        eval_acc = Evaluation_Account.objects.get(evaluation_name=evaluation, account=evaluator)
        eval_acc.delete()

    return redirect('/evaluation/' + evaluation_id + '/')
