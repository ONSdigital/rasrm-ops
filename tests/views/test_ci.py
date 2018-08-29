def test_get_ci_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json={})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123/ci')

    assert response.status_code == 200


def test_get_ci_shows_all_selectors(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': ['RU_REF', 'COLLECTION_EXERCISE_ID']})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123/ci')

    assert b'COLLECTION_EXERCISE_ID' in response.data
    assert b'RU_REF' in response.data


def test_eq_id_selector_is_default(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/surveys/BRES/classifiertypeselectors',
                      json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': ['RU_REF', 'COLLECTION_EXERCISE_ID']})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123/ci')

    assert b'EQ_ID' in response.data


def test_form_type_selector_is_default(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/surveys/BRES/classifiertypeselectors',
                      json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': []})
    requests_mock.get('/surveys/BRES', json={})

    response = client.get('/survey/BRES/collection/123/ci')

    assert b'FORM_TYPE' in response.data


def test_create_ci_classifier_default_classifiers(client, requests_mock):
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': []})
    requests_mock.post('/collection-instrument-api/1.0.2/upload')
    requests_mock.get('/collection-instrument-api/1.0.2/collectioninstrument', json=[{'id': 'ci_id'}])
    requests_mock.post('/collection-instrument-api/1.0.2/link-exercise/ci_id/collex_id')

    response = client.post('/survey/BRES/collection/collex_id/ci', data={'EQ_ID': '1', 'FORM_TYPE': '2'})

    assert response.status_code == 302


def test_create_ci_classifier_with_non_default_selector(client, requests_mock):
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': ['COLLECTION_EXERCISE_ID']})
    requests_mock.post('/collection-instrument-api/1.0.2/upload')
    requests_mock.get('/collection-instrument-api/1.0.2/collectioninstrument', json=[{'id': 'ci_id'}])
    requests_mock.post('/collection-instrument-api/1.0.2/link-exercise/ci_id/collex_id')

    response = client.post('/survey/BRES/collection/collex_id/ci',
                           data={'COLLECTION_EXERCISE_ID': 'collex_id', 'EQ_ID': '1', 'FORM_TYPE': '2'})

    assert response.status_code == 302


def test_create_ci_classifier_link_fails(client, requests_mock):
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': []})
    requests_mock.post('/collection-instrument-api/1.0.2/upload', status_code=500)

    response = client.post('/survey/BRES/collection/collex_id/ci', data={'EQ_ID': '1', 'FORM_TYPE': '2'})

    assert response.status_code == 500


def test_create_ci_classifier_link_conflict(client, requests_mock):
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': []})
    requests_mock.post('/collection-instrument-api/1.0.2/upload')
    requests_mock.get('/collection-instrument-api/1.0.2/collectioninstrument', json=[{'id': 'ci_id'}])
    requests_mock.post('/collection-instrument-api/1.0.2/link-exercise/ci_id/collex_id', status_code=409)

    response = client.post('/survey/BRES/collection/collex_id/ci', data={'EQ_ID': '1', 'FORM_TYPE': '2'})

    assert response.status_code == 409


def test_create_ci_classifier_no_collection_exercise_classifier(client, requests_mock):
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': ['COLLECTION_EXERCISE_ID']})

    response = client.post('/survey/BRES/collection/collex_id/ci')

    assert response.status_code == 400


def test_create_ci_classifier_wrong_classifer(client, requests_mock):
    requests_mock.get('/surveys/BRES/classifiertypeselectors', json=[{'name': 'COLLECTION_INSTRUMENT', 'id': '123'}])
    requests_mock.get('/surveys/BRES/classifiertypeselectors/123',
                      json={'classifierTypes': ['COLLECTION_EXERCISE_ID']})

    response = client.post('/survey/BRES/collection/collex_id/ci', data={'RU_REF': '123'})

    assert response.status_code == 400
