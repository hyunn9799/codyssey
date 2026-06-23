def login_user(request,user):
    request.session['user_id'] = user.id

def logout_user(request):
    request.session.clear()