def test_get_survey_details(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={})
    requests_mock.get('/collectionexercises/survey/BRES', json=[{'userDescription': 'Collection period 1'}])

    response = client.get('/survey/BRES')

    assert response.status_code == 200
    assert b"Collection period 1" in response.data


def test_get_survey_details_displays_survey(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'name': 'BRES'})
    requests_mock.get('/collectionexercises/survey/BRES', json=[{'userDescription': 'Collection period 1'}])

    response = client.get('/survey/BRES')

    assert b"BRES" in response.data


def test_get_survey_details_no_collection_exercises(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={})
    requests_mock.get('/collectionexercises/survey/BRES', status_code=204)

    response = client.get('/survey/BRES')

    assert response.status_code == 200


def test_create_collection_exercise(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyRef': 'BRES', 'longName': 'BRE Survey'})
    requests_mock.post('/collectionexercises')

    response = client.post('/survey/BRES', data={'period': '0101', 'period_description': '01 January'})

    assert response.status_code == 302


def test_create_collection_exercise_fails(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyRef': 'BRES', 'longName': 'BRE Survey'})
    requests_mock.post('/collectionexercises', status_code=500)

    response = client.post('/survey/BRES', data={'period': '0101', 'period_description': '01 January'})

    assert response.status_code == 500


def test_create_collection_exercise_long_name_trimmed(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyRef': 'BRES', 'longName': 'This is a really long name'})
    requests_mock.post('/collectionexercises', additional_matcher=lambda r: r.json()['name'] == 'This is a really lon')

    response = client.post('/survey/BRES',
                           data={'period': '0101', 'period_description': '01 January'})

    assert response.status_code == 302


def test_create_collection_exercise_no_form_data(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyRef': 'BRES', 'longName': 'BRE Survey'})

    response = client.post('/survey/BRES')

    assert response.status_code == 400
