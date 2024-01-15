from core.models.assignments import Assignment, GradeEnum, AssignmentStateEnum
from core.apis.decorators import AuthPrincipal
from core.libs.helpers import get_utc_now
from core.libs.assertions import assert_found, assert_valid
from core import db

def test_assignment_upsert():
    # Test case for lines 35, 49-54
    assignment_new = Assignment(
        student_id=1,
        content='Test content',
        grade=GradeEnum.A,
        state=AssignmentStateEnum.DRAFT,
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )

    # Save the new assignment using the upsert method
    updated_assignment = Assignment.upsert(assignment_new)

    # Assert that the assignment has been added or updated correctly
    assert updated_assignment is not None
    assert updated_assignment.content == 'Test content'
    assert updated_assignment.grade == GradeEnum.A
    assert updated_assignment.state == AssignmentStateEnum.DRAFT

def test_assignment_submit():
    existing_assignment = Assignment(
        student_id=1,
        content='Existing content',
        state=AssignmentStateEnum.DRAFT,
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )
    db.session.add(existing_assignment)
    db.session.commit()

    # Submit the assignment
    teacher_id = 1
    auth_principal = AuthPrincipal(student_id=1, teacher_id=teacher_id, user_id=1)
    submitted_assignment = Assignment.submit(existing_assignment.id, teacher_id, auth_principal)

    # Assert that the assignment has been submitted correctly
    assert submitted_assignment.state == AssignmentStateEnum.SUBMITTED
    assert submitted_assignment.teacher_id == teacher_id


def test_assignment_mark_grade():
    # Test case for lines 77-85
    # Assuming there's an existing assignment in SUBMITTED state
    existing_assignment = Assignment(
        student_id=1,
        content='Existing content',
        state=AssignmentStateEnum.SUBMITTED,
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )
    db.session.add(existing_assignment)
    db.session.commit()

    # Mark the grade for the assignment
    grade = GradeEnum.A
    auth_principal = AuthPrincipal(student_id=1, teacher_id=1, user_id=1)
    graded_assignment = Assignment.mark_grade(existing_assignment.id, grade, auth_principal)

    # Assert that the assignment has been graded correctly
    assert graded_assignment.state == AssignmentStateEnum.GRADED
    assert graded_assignment.grade == grade



def test_assignment_upsert_with_id():
    # Assuming there's an existing assignment with an ID
    existing_assignment = Assignment(
        id=23,
        student_id=1,
        content='Existing content',
        state=AssignmentStateEnum.DRAFT,
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )
    db.session.add(existing_assignment)
    db.session.commit()

    # Attempt to upsert the existing assignment with the same ID
    assignment_with_same_id = Assignment(
        id=23,
        student_id=1,
        content='Updated content',
        state=AssignmentStateEnum.DRAFT,
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )

    print("Before upsert:")
    print("Existing assignment content:", existing_assignment.content)
    print("New assignment content:", assignment_with_same_id.content)

    # Ensure the database is in the correct state before upsert
    assert existing_assignment.content == 'Existing content'

    # Attempt to upsert the existing assignment
    updated_assignment = Assignment.upsert(assignment_with_same_id)

    print("After upsert:")
    print("Updated assignment content:", updated_assignment.content)

    # Assert that attempting to upsert an existing assignment updates its content
    assert updated_assignment is not None
    assert updated_assignment.content == 'Updated content'

