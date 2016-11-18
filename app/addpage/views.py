from flask import Flask, Blueprint, render_template, g, request, json, jsonify, url_for
import sqlite3
from app.models.user import User
from app.models.subject import Subject
from app.models.submitWork import submitWork
from app.models.work import Work
import datetime

# create Blueprint class with name importname Blueprintfolders
Addpage = Blueprint('Addpage', __name__, url_prefix="/<url_user_id>", template_folder='', static_folder='')


@Addpage.url_value_preprocessor
def addpage(endpoint, url_user_id):
    g.user = User(url_user_id['url_user_id'])


@Addpage.route('/<url_Subject_id>/<url_Year>/add_work')
def add_assignment(url_user_id, url_Subject_id, url_Year):
    return 'boo'


@Addpage.route('/add_subject')
def add_subject(url_user_id):
    return render_template('teacher_add_subject.html')


@Addpage.route('/<url_Subject_id>/<url_Year>/add_student')
def add_student(url_user_id, url_Subject_id, url_Year):
    conn = sqlite3.connect('Data.db')
    currentAcademicYear = datetime.date.today()
    if currentAcademicYear.month <= 4:
        currentAcademicYear = currentAcademicYear.year + 542
    else:
        currentAcademicYear = currentAcademicYear.year + 543
    g.YEAR = [x + currentAcademicYear for x in range(0, 3)]
    print g.YEAR
    currentAcademicYear = str(int(str(currentAcademicYear)[2:4]))
    c = conn.cursor()
    subject_list = c.execute("SELECT Subject_ID from subject WHERE  Year =  ? ", (currentAcademicYear,))
    g.subject_list = subject_list.fetchall()
    c.close()
    print g.subject_list
    return render_template('teacher_add_TA.html')


@Addpage.route('/<url_Subject_id>/<url_Year>/<work_id>/manage_group')
def manage_group(url_user_id, url_Subject_id, url_Year, work_id):
    g.user = User(url_user_id)
    if g.user.Profile['Role'] == 'student':
        return render_template('student_grouping.html')
    else:
        return render_template('grouping.html')
