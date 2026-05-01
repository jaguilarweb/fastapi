from fastapi import status

def test_create_customer(client):
    response = client.post('/customers', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'age': 30
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['name'] == 'John Doe'
    assert data['email'] == 'john.doe@example.com'
    assert data['age'] == 30

def test_get_customer(client):
    # First, create a customer to ensure there is one to retrieve
    response = client.post('/customers', json={
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'age': 25
    })
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()['id']
    response = client.get(f'/customers/{customer_id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == 'Jane Doe'
    assert response.json()['email'] == 'jane.doe@example.com'
    assert response.json()['age'] == 25
  