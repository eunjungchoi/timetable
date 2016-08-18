from timeline.models import UserProxy


def auth(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user'):
        try:
            user = UserProxy.objects.get(pk=request.user.id)
        except UserProxy.DoesNotExist:
            from django.contrib.auth.models import AnonymousUser
            user = AnonymousUser()
    return {
        'user': user,
    }
