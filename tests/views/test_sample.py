from io import BytesIO
from unittest.mock import patch, ANY


def test_get_upload_sample_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123', json={})
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Social'})
    response = client.get('/survey/BRES/collection/123/sample')

    assert response.status_code == 200


def test_upload_social_sample_file(client, requests_mock):
    requests_mock.get('/surveys/123', json={'surveyType': 'Social'})
    requests_mock.get('/actionplans',
                      json=[{'id': 'action_plan_id', 'selectors': {'collectionExerciseId': 'collex_id'}}])
    requests_mock.get(
        '/collection-instrument-api/1.0.2/collectioninstrument?searchString={"collection_exercise":"collex_id"}',
        json=[{"id": "collection_instrument_id"}]
    )
    requests_mock.get('/collectionexercises/collex_id', json={'state': 'READY_FOR_REVIEW'})
    requests_mock.get('/collectionexercises/collex_id/events', json={})

    with patch('app.views.sample.SampleLoader') as sample_loader_mock:
        response = client.post('/survey/123/collection/collex_id/sample',
                               data={'sample': (BytesIO(b'header\nline'), 'sample.csv')},
                               follow_redirects=True)

    load_sample_call = sample_loader_mock.return_value.load_sample
    load_sample_call.assert_called_once_with(ANY, 'collex_id', 'action_plan_id', 'collection_instrument_id')

    assert response.status_code == 200


def test_upload_social_sample_file_fails(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Social'})
    requests_mock.post('/samples/SOCIAL/fileupload', json={'id': '123'}, status_code=500)

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

    assert response.status_code == 500


def test_upload_social_sample_file_link_fails(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Social'})
    requests_mock.post('/samples/SOCIAL/fileupload', json={'id': '123'})
    requests_mock.put('/collectionexercises/link/123', status_code=500)

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

    assert response.status_code == 500


def test_no_sample_file_is_bad_request(client):
    response = client.post('/survey/BRES/collection/123/sample')

    assert response.status_code == 400
