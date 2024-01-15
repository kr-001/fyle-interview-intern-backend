from flask import Blueprint, jsonify , abort
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs.assertions import assert_found, assert_valid

from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    # Ensure that the teacher exists
    assert_found(p.teacher_id, 'Teacher not found')

    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    # State = DRAFT 
    teachers_assignments = [assignment for assignment in teachers_assignments if assignment.state != "DRAFT"]
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    # Ensure that the payload contains 'id' and 'grade'
    assert_valid('id' in incoming_payload and 'grade' in incoming_payload, 'Invalid payload')

    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    # Ensure that the assignment exists
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    assert_found(assignment, 'Assignment not found')

    # Ensure that the teacher is grading their own assignment
    assert_valid(assignment.teacher_id == p.teacher_id, 'Unauthorized to grade this assignment')
    if not assignment:
        abort(400, description='Assignment not found')

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
