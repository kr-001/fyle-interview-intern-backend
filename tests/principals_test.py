from core.models.assignments import AssignmentStateEnum, GradeEnum
from core import db

class TestPrincipal:

    def setup_method(self,method):
        db.session.begin_nested()

    def teardown_method(self,method):
        db.session.rollback()

    def test_get_assignments(self,client, h_principal):
        response = client.get(
            '/principal/assignments',
            headers=h_principal
        )

        assert response.status_code == 200

        data = response.json['data']
        for assignment in data:
            assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

    def test_grade_assignment_draft_assignment(self,client, h_principal):
        """
        failure case: If an assignment is in Draft state, it cannot be graded by principal
        """
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 5,
                'grade': GradeEnum.A.value
            },
            headers=h_principal
        )
        assert response.status_code == 400


    def test_grade_assignment(self,client, h_principal):
    
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 4,
                'grade': GradeEnum.C.value
            },
            headers=h_principal
        )

        assert response.status_code == 200

        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == GradeEnum.C
    


    def test_regrade_assignment(self,client, h_principal):

        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 4,
                'grade': GradeEnum.B.value
            },
            headers=h_principal
        )

        assert response.status_code == 200

        assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
        assert response.json['data']['grade'] == GradeEnum.B
  
