"""
Slightly customized python-social-auth backend for SAML 2.0 support
"""

from third_party_auth.saml import SAMLAuthBackend

from campus_social_auth.backends.utils import update_username_suggestion


class CampusSAMLAuthBackend(SAMLAuthBackend):
    """
    Customized version of SAMLIdentityProvider that can retrieve details beyond the standard
    details supported by the canonical upstream version.
    """

    def get_user_details(self, attributes):
        """
        Overrides `get_user_details` from the base class; retrieves those details,
        then updates the dict with values from whatever additional fields are desired.
        """
        details = super(CampusSAMLAuthBackend, self).get_user_details(attributes)
        details = update_username_suggestion(details, self.conf)

        return details
