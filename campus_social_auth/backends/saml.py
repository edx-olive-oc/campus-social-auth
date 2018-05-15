"""
Slightly customized python-social-auth backend for SAML 2.0 support
"""

from third_party_auth.saml import SAMLAuthBackend
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

from campus_social_auth.backends.utils import update_username_suggestion


class CampusSAMLAuthBackend(SAMLAuthBackend):
    """
    Customized version of SAMLAuthBackend that can retrieve details beyond the standard
    details supported by the canonical upstream version.
    """

    def get_user_details(self, attributes):
        """
        Overrides `get_user_details` from the base class; retrieves those details,
        then updates the dict with values from whatever additional fields are desired.
        """
        idp_slug = configuration_helpers.get_value('CAMPUS_SAML_PROVIDER_SLUG', '')
        details = super(CampusSAMLAuthBackend, self).get_user_details(attributes)
        provider = self.get_idp(idp_slug)
        details = update_username_suggestion(details, provider.conf)

        return details
