from flask import jsonify, request
from marshmallow.exceptions import ValidationError
from core import app , db
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from core.apis.decorators import authenticate_principal,accept_payload
from core.models import Teacher, User ,Student,Principal,Assignment

from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err

#APIS

#GET /pricipal/teachers
@app.route('/principal/teachers', methods=["GET"])
@authenticate_principal
def get_principal_teachers(p):
    teachers = Teacher.query.all()
    teachers_data = [{"user_id": teacher.user_id, "created_at": str(teacher.created_at)} for teacher in teachers]
    return jsonify({"data": teachers_data})


@app.route('/principal/assignments' , methods=["GET"])
@authenticate_principal
def get_principal_assignment(p):
    assignments = Assignment.query.filter(
        (Assignment.state=="SUBMITTED") | (Assignment.state=="GRADED")
    ).all()

    assignments_data=[
        {
            "content": assignment.content,
            "created_at": str(assignment.created_at),
            "grade":assignment.grade,
            "id":assignment.id,
            "state":assignment.state,
            "student_id":assignment.student_id,
            "teacher_id":assignment.teacher_id,
            "updated_at":str(assignment.updated_at),
        }
        for assignment in assignments
    ]

    return jsonify({"data": assignments_data})

@app.route("/principal/assignments/grade" , methods=["POST"])
@authenticate_principal
def grade_or_regrade_assignment(p):
    data = request.get_json()
    print(data)
    assignment_id = data.get("id")
    grade = data.get("grade")

    #assignment by id
    assignment = Assignment.query.get(assignment_id)
    #if assignment exists?
    if assignment and (assignment.teacher_id and assignment.grade!="DRAFT"):
        assignment.grade = grade
        assignment.state = "GRADED"
        db.session.commit()
        return jsonify(
            {
                "data":{
                    "content" : assignment.content,
                    "created_at": str(assignment.created_at),
                    "grade":assignment.grade,
                    "id":assignment.id,
                    "state":assignment.state,
                    "student_id":assignment.student_id,
                    "teacher_id": assignment.teacher_id,
                    "updated_at": str(assignment.updated_at),
                }
            }
        )
    else:
        return jsonify({"error": "Assignment IN DRAFT STATE or NOT Found"}) , 400