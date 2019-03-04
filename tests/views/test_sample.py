from io import BytesIO
from unittest.mock import patch


def get_upload_sample_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123/events', json={})
    response = client.get('/survey/BRES/collection/123/sample')

    assert response.status_code == 200


def test_upload_social_sample_file(client, requests_mock):
    requests_mock.get('/surveys/123', json={'surveyType': 'Social'})
    requests_mock.post('/samples/SOCIAL/fileupload', json={'id': '123'})
    requests_mock.put('/collectionexercises/link/123')

    requests_mock.get('/actionplans', json=[{'id': '123', 'selectors': {'collectionExerciseId': '123'}}])
    requests_mock.get(
        '/collection-instrument-api/1.0.2/collectioninstrument?searchString={"collection_exercise":"123"}',
        json=[{"id": "123"}]
    )
    #

    with patch('app.views.sample.SampleLoader.load_sample') as sample_loader_mock:
        response = client.post('/survey/123/collection/123/sample', data={
            'sample': (BytesIO(b'my file contents'), 'sample.csv'),
        })

        sample_loader_mock.assert_called_once_with("sample.csv", '123', '123', '123')

        assert response.status_code == 302


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


def test_upload_sample_file_for_unsupported_type(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'unsupported'})

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

    assert response.status_code == 400
