import pytest

from tests.authentication.factories import CustomUserFactory
from tests.stores.factories import CampaignUserFactory
from api.utils import select_relevant_campaign_user_list

@pytest.mark.django_db
class TestSelectRelevantCampaignUserList:
    def test_less_than_two_campaigns(self):

        user = CustomUserFactory()
        campaign_user = CampaignUserFactory(user = user)

        result = select_relevant_campaign_user_list(user)

        assert len(result) == 1
        assert result[0] == campaign_user


        



