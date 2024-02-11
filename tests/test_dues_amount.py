from mydsa.models import CoreUser
import pytest


@pytest.mark.django_db(databases=["default"])
def test_dues_amount(client):
    #client.login(username="someone", password="something")
    user = CoreUser.objects.get()
    client.force_login(user)
    response = client.get('/accounts/recurring_update.html')
    print(response.content)
    assert "$30" in str(response.content)
