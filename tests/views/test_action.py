def test_get_action_rule_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/actionplans', json={})

    response = client.get('/survey/BRES/collection/123/actions')

    assert response.status_code == 200


def test_get_action_rule_page_lists_action_plans(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/actionplans', json=[{'name': 'Action plan 1', 'selectors': {'collectionExerciseId': '123'}}])

    response = client.get('/survey/BRES/collection/123/actions')

    assert b'Action plan 1' in response.data


def test_create_action_rule(client, requests_mock):
    requests_mock.get('/actionplans', json={})
    requests_mock.post('/actionrules')
    response = client.post('/survey/BRES/collection/123/actions', data={
        'action_plan_id': '123',
        'action_rule_type': 'BSNOT',
        'name': 'Notification letter',
        'description': 'Notification letter',
        'timestamp': '2010-01-02T01:01',
        'priority': '3',
    })

    assert response.status_code == 302


def test_create_action_rule_fails(client, requests_mock):
    requests_mock.get('/actionplans', json={})
    requests_mock.post('/actionrules', status_code=500)
    response = client.post('/survey/BRES/collection/123/actions', data={
        'action_plan_id': '123',
        'action_rule_type': 'BSNOT',
        'name': 'Notification letter',
        'description': 'Notification letter',
        'timestamp': '2010-01-02T01:01',
        'priority': '3',
    })

    assert response.status_code == 500


def test_create_action_rule_missing_data(client, requests_mock):
    requests_mock.get('/actionplans', json={})

    response = client.post('/survey/BRES/collection/123/actions')

    assert response.status_code == 400
