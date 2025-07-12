from celery import shared_task
from django.contrib.auth.hashers import make_password
from .....models import CredibilityCodes, UserProfile, UserPasswords


@shared_task
def update_password_async(user_id, new_password, code):
    user = UserProfile.objects.get(id=user_id)

    old_pass = UserPasswords.objects.filter(user=user).first()
    if old_pass:
        old_pass.password = make_password(new_password)
        old_pass.save()
    else:
        UserPasswords.objects.create(user=user, password=make_password(new_password))

    user.set_password(new_password)
    user.save()

    CredibilityCodes.objects.filter(
        email__user=user,
        resat_pass_code=code,
        resat_pass=True,
        finished=True,
        is_done=False
    ).update(is_done=True)
