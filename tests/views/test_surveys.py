def test_get_surveys(client, requests_mock):
    requests_mock.get(f"{client.application.config['SURVEY_SERVICE']}/legal-bases", json=[{"ref": "Vol"}])
    requests_mock.get(f"{client.application.config['SURVEY_SERVICE']}/surveys/surveytype/Social",
                      json=[{"longName": "BRES"}])

    response = client.get('/survey')

    assert response.status_code == 200
    assert b"BRES" in response.data


def test_get_surveys_no_legal_basis(client, requests_mock):
    requests_mock.get(f"{client.application.config['SURVEY_SERVICE']}/legal-bases", json=[])
    requests_mock.get(f"{client.application.config['SURVEY_SERVICE']}/surveys/surveytype/Social",
                      json=[{"longName": "BRES"}])

    response = client.get('/survey')

    assert response.status_code == 200
    assert b"BRES" in response.data


def test_get_surveys_no_surveys(client, requests_mock):
    requests_mock.get(f"{client.application.config['SURVEY_SERVICE']}/legal-bases", json=[{"ref": "Vol"}])
    requests_mock.get(f"{client.application.config['SURVEY_SERVICE']}/surveys/surveytype/Social", json=[])

    response = client.get('/survey')

    assert response.status_code == 200


def test_create_survey(client, requests_mock):
    requests_mock.post(f"{client.application.config['SURVEY_SERVICE']}/surveys")
    survey = {
        'survey_ref': 22,
        'short_name': "BRES",
        'long_name': "BRE survey",
        'legal_basis': "Vol",
        'survey_type': "Social"
    }

    response = client.post('/survey', data=survey)

    assert response.status_code == 302
    assert '/survey' in response.location


def test_create_survey_missing_fields(client):
    survey = {
        'long_name': "BRE survey",
        'legal_basis': "Vol",
        'survey_type': "Social"
    }

    response = client.post('/survey', data=survey)

    assert response.status_code == 400


def test_create_survey_fails(client, requests_mock):
    requests_mock.post(f"{client.application.config['SURVEY_SERVICE']}/surveys", status_code=500)
    survey = {
        'survey_ref': 22,
        'short_name': "BRES",
        'long_name': "BRE survey",
        'legal_basis': "Vol",
        'survey_type': "Social"
    }

    response = client.post('/survey', data=survey)

    assert response.status_code == 500


def test_create_survey_conflict(client, requests_mock):
    requests_mock.post(f"{client.application.config['SURVEY_SERVICE']}/surveys", status_code=409)
    survey = {
        'survey_ref': 22,
        'short_name': "BRES",
        'long_name': "BRE survey",
        'legal_basis': "Vol",
        'survey_type': "Social"
    }

    response = client.post('/survey', data=survey)

    assert response.status_code == 409
