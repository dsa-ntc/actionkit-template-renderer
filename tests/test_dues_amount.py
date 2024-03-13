import pytest

from mydsa.models import CoreUser


@pytest.mark.django_db(databases=["default"])
def test_dues_amount(client):
    # TODO: the context from views is working. the issue is the html files use different context vars than django templates
        # so i think we'll need serializers or something on the request user to return the "profile" data
        # also since this is actionkit syntax im wondering if theres someone at actionkit we can ask about where these variables come from?
        # like maybe theres some serializers on their side i could steal instead of rewriting
        # should check documentation first tho but yeah
        # tldr look up how to do custom variables in django templates. i think its serializers you want
    # client.login(username="someone", password="something")
    user = CoreUser.objects.get()
    client.force_login(user)
    response = client.get("/accounts/recurring_update.html")
    print(response.content)
    assert "$30" in str(response.content)
