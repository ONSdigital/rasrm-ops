def test_get_survey_classifer_page(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/classifiers')

    assert response.status_code == 200


def test_create_survey_classifier(client, requests_mock):
    classifier = {
        'name': 'COLLECTION_INSTRUMENT',
        'classifierTypes':
            [
                'SURVEY_ID', 'COLLECTION_EXERCISE_ID'
            ]

    }
    requests_mock.post('/surveys/BRES/classifiers', additional_matcher=lambda r: r.json() == classifier)

    response = client.post('/survey/BRES/classifiers',
                           data={'classifier_type': 'COLLECTION_INSTRUMENT', 'SURVEY_ID': 'SURVEY_ID',
                                 'COLLECTION_EXERCISE_ID': 'COLLECTION_EXERCISE_ID'})

    assert response.status_code == 302


def test_create_survey_classifier_fails(client, requests_mock):
    requests_mock.post('/surveys/BRES/classifiers', status_code=500)

    response = client.post('/survey/BRES/classifiers',
                           data={'classifier_type': 'COLLECTION_INSTRUMENT', 'SURVEY_ID': 'SURVEY_ID',
                                 'COLLECTION_EXERCISE_ID': 'COLLECTION_EXERCISE_ID'})

    assert response.status_code == 500


def test_create_survey_conflict(client, requests_mock):
    requests_mock.post('/surveys/BRES/classifiers', status_code=409)

    response = client.post('/survey/BRES/classifiers',
                           data={'classifier_type': 'COLLECTION_INSTRUMENT', 'SURVEY_ID': 'SURVEY_ID',
                                 'COLLECTION_EXERCISE_ID': 'COLLECTION_EXERCISE_ID'})

    assert response.status_code == 409


def test_create_survey_classifier_bad_classifier_selector_type(client):
    response = client.post('/survey/BRES/classifiers',
                           data={'classifier_type': 'TEST'})

    assert response.status_code == 400


def test_create_survey_classifier_no_classifiers(client):
    response = client.post('/survey/BRES/classifiers',
                           data={'classifier_type': 'COLLECTION_INSTRUMENT'})

    assert response.status_code == 400
