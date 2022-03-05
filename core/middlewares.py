from core.models import Customer

def createCustomerMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated and not hasattr(request.user, 'customer'):
            Customer.objects.create(user=request.user)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware