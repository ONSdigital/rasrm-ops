def test_get_survey_details(client, requests_mock):
    requests_mock.get('/collectionexercises/survey/BRES', json=[{'userDescription': 'Collection period 1'}])

    response = client.get('/survey/BRES')

    assert response.status_code == 200
    assert b"Collection period 1" in response.data


def test_get_survey_details_no_collection_exercises(client, requests_mock):
    requests_mock.get('/collectionexercises/survey/BRES', status_code=204)

    response = client.get('/survey/BRES')

    assert response.status_code == 200
