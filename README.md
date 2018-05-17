# campus-social-auth
Contains the custom python-social-auth backends and logic for the Campus.IL project.

### Description
This app extends the default behavior for Facebook, Google and SAML backends supporting a custom username suggestion.

### Instalation
* Install this package in edx-platform env.
* Configure any supported backend by adding the corresponding module in `THIRD_PARTY_AUTH_BACKENDS`.
* Backends available:
    * `campus_social_auth.backends.oauth2.FacebookOAuth2Backend`
    * `campus_social_auth.backends.oauth2.GoogleOAuth2Backend`
    * `campus_social_auth.backends.saml.CampusSAMLAuthBackend`
