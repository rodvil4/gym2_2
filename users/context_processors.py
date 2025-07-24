from .models import Member

def member_context(request):
    if request.user.is_authenticated:
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            member = None
        return {'member': member}
    return {}
