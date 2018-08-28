def test_get_collection_exercise_events_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={'state': 'READY_FOR_REVIEW'})
    requests_mock.get('/collectionexercises/123/events', json={})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123')

    assert response.status_code == 200


def test_get_collection_exercise_events_page_can_execute(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={'state': 'READY_FOR_REVIEW'})
    requests_mock.get('/collectionexercises/123/events', json={})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123')

    assert response.status_code == 200
    assert b'disabled' not in response.data


def test_get_collection_exercise_events_page_execute_disabled(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={'state': 'SOMETHING'})
    requests_mock.get('/collectionexercises/123/events', json={})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123')

    assert response.status_code == 200
    assert b'disabled' in response.data


def test_execute_collection_exercise(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={'state': 'READY_FOR_REVIEW'})
    requests_mock.post('/collectionexerciseexecution/123')

    response = client.post('/survey/BRES/collection/123')

    assert response.status_code == 302


def test_execute_collection_exercise_not_executable(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={'state': 'SOMETHING'})
    requests_mock.post('/collectionexerciseexecution/123')

    response = client.post('/survey/BRES/collection/123')

    assert response.status_code == 400
