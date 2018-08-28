def test_get_collection_exercise_events_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123/event')

    assert response.status_code == 200


def test_create_collection_exercise_events(client, requests_mock):
    requests_mock.post('/collectionexercises/123/events')

    response = client.post('/survey/BRES/collection/123/event', data={'event': 'mps', 'event_date': '2010-01-02T01:01'})

    assert response.status_code == 302


def test_create_collection_exercise_events_fails(client, requests_mock):
    requests_mock.post('/collectionexercises/123/events', status_code=500)

    response = client.post('/survey/BRES/collection/123/event', data={'event': 'mps', 'event_date': '2010-01-02T01:01'})

    assert response.status_code == 500


def test_create_collection_exercise_events_conflicts(client, requests_mock):
    requests_mock.post('/collectionexercises/123/events', status_code=409)

    response = client.post('/survey/BRES/collection/123/event', data={'event': 'mps', 'event_date': '2010-01-02T01:01'})

    assert response.status_code == 409


def test_create_collection_exercise_events_invalid_date_format(client, requests_mock):
    response = client.post('/survey/BRES/collection/123/event', data={'event': 'mps', 'event_date': '2010-01-02T'})

    assert response.status_code == 400


def test_create_collection_exercise_events_no_event_data(client):
    response = client.post('/survey/BRES/collection/123/event', data={})

    assert response.status_code == 400


def test_create_collection_exercise_events_invalid_tag(client):
    response = client.post('/survey/BRES/collection/123/event',
                           data={'event': 'invalid', 'event_date': '2010-01-02T01:01'})

    assert response.status_code == 400
