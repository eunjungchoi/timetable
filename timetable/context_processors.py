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

#'django.contrib.auth.context_processors.auth',
# 여기에서  auth 부분을 가져와서 overwrite 한 것.
# 그리고 setting 에  추가됨. (템플릿에))
# 템플릿에 등장한 user 만  user profile image가  가져와짐.
# request.user 일때는  원래 user로...
