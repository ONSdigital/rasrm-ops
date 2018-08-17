from io import BytesIO


def get_upload_sample_page(client, requests_mock):
    requests_mock.get('/collectionexercises/123/events', json={})
    response = client.get('/survey/BRES/collection/123/sample')

    assert response.status_code == 200


def test_upload_business_sample_file(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Business'})
    requests_mock.post('/samples/B/fileupload', json={'id': '123'})
    requests_mock.put('/collectionexercises/link/123')

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

    assert response.status_code == 302


def test_upload_business_sample_file_fails(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Business'})
    requests_mock.post('/samples/B/fileupload', json={'id': '123'}, status_code=500)

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

    assert response.status_code == 500


def test_upload_business_sample_file_link_fails(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Business'})
    requests_mock.post('/samples/B/fileupload', json={'id': '123'})
    requests_mock.put('/collectionexercises/link/123', status_code=500)

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

    assert response.status_code == 500


def test_upload_social_sample_file(client, requests_mock):
    requests_mock.get('/surveys/BRES', json={'surveyType': 'Social'})
    requests_mock.post('/samples/SOCIAL/fileupload', json={'id': '123'})
    requests_mock.put('/collectionexercises/link/123')

    response = client.post('/survey/BRES/collection/123/sample', data={
        'sample': (BytesIO(b'my file contents'), 'sample.csv'),
    })

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
