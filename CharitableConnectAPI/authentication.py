from rest_framework.authentication import *
class BearerAuthentication(TokenAuthentication):
    keyword = ['token','bearer']
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower().decode() not in self.keyword:
            return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise TokenAuthentication.exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)
