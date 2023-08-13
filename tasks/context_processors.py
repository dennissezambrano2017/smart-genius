def user_email(request):
    user = request.user
    email = user.email if user.is_authenticated else None
    return {'user_email': email}