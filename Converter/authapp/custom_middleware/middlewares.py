from django.conf import settings
from django.core.exceptions import PermissionDenied
# class customware:
#     def __init__(self,get_response):
#         self.get_response= get_response
    
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         print("Before going inside view ")
#         response = self.get_response(request)

#         print("Middleware Working Properly")

#         return response

class IPBlacklistMiddleware:
    def __init__(self,get_response):
       self.get_response= get_response

    def __call__(self, request):
        if hasattr(settings, 'BANNED_IPS') and settings.BANNED_IPS is not None:
            # check incoming request ip address is in BANNED_IPS 
            if request.META['REMOTE_ADDR'] in settings.BANNED_IPS:
                raise PermissionDenied()
        
        response =self.get_response(request)
        return response