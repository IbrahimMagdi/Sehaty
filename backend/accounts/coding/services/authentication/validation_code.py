import re
import random
from rest_framework import status
from ..authentication import re_message as messages
from ....models import CredibilityCodes
from datetime import datetime, timedelta
from django.utils.timezone import now

regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
)
fmt = '%Y-%m-%d %H:%M:%S'
ATTEMPTS_TIMEOUTS = {
    1: timedelta(minutes=1),
    2: timedelta(minutes=5),
    3: timedelta(minutes=5),
    4: timedelta(minutes=20),
    5: timedelta(minutes=40),
    6: timedelta(hours=2),
}

class ValidationCodeService:
    def __init__(self, request):
        self.request = request
        self.ln = self.get_language()
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = ""
        self.response_data = None

    def get_language(self):
        try:
            ln = self.request.headers.get('ln', 'en')
            if ln in messages.languages:
                return ln
            else:
                return 'en'
        except AttributeError:
            return 'en'

    def get_response(self, end_time, email_object, number_attempts):
        now_datetime = now()
        # end_time is already a datetime object
        self.response_data = {
            'end_time': end_time,
            'time_now': now_datetime,
            'object_id': email_object.id,
            'number_attempts': number_attempts,
            'send_to': 'email',
            'value': email_object.email.lower()
        }
        return self.response_data

    def send_code_email(self, email_object, case):
        self.response_status = status.HTTP_201_CREATED
        fun_msg_dir = messages.messages['validation_code']['send_code_email']
        now_datetime = now()
        random_code = "".join(str(random.randint(0, 9)) for _ in range(6))
        is_reset = (case == 'resat_pass')

        # فلترة الأكواد المنتهية لنفس العملية
        if case == "verified":
            expired_codes = CredibilityCodes.objects.filter(
                email=email_object,
                verified=True,
                is_done=False,
                expired=True,
                finished=False,
            )
        elif case == "resat_pass":
            expired_codes = CredibilityCodes.objects.filter(
                email=email_object,
                resat_pass=True,
                is_done=False,
                expired=True,
                finished=False,
            )
        else:
            expired_codes = CredibilityCodes.objects.none()

        if expired_codes.count() > 3:
            self._block_user(email_object, fun_msg_dir)
            return self.response_status, self.response_message, self.response_data

        # فلترة الأكواد النشطة لنفس العملية
        if case == "verified":
            code_qs = CredibilityCodes.objects.filter(
                email=email_object,
                is_done=False,
                expired=False,
                finished=False,
                verified=True,
            )
        elif case == "resat_pass":
            code_qs = CredibilityCodes.objects.filter(
                email=email_object,
                is_done=False,
                expired=False,
                finished=False,
                resat_pass=True,
            )
        else:
            code_qs = CredibilityCodes.objects.none()

        code_obj = code_qs.first()

        if code_obj is None:
            # لا يوجد كود نشط، أنشئ كود جديد
            create_kwargs = dict(
                email=email_object,
                code=random_code,
                is_done=False,
                expired=False,
                number_attempts=1,
                finished=False,
            )
            if case == "verified":
                create_kwargs['verified'] = True
            elif case == "resat_pass":
                create_kwargs['resat_pass'] = True

            create_new = CredibilityCodes.objects.create(**create_kwargs)
            self.response_message = fun_msg_dir['sending_email'][self.ln]
            self.response_data = self.get_response(
                now_datetime + ATTEMPTS_TIMEOUTS[1], email_object, 1
            )
            return self.response_status, self.response_message, self.response_data

        # إذا وصل المستخدم الحد الأعلى للمحاولات
        if code_obj.number_attempts >= 6:
            code_obj.expired = True
            code_obj.save()
            if expired_codes.count() + 1 >= 3:
                self._block_user(email_object, fun_msg_dir)
            else:
                # إنشاء كود جديد بعد انتهاء المحاولات
                create_kwargs = dict(
                    email=email_object,
                    code=random_code,
                    is_done=False,
                    expired=False,
                    number_attempts=1,
                    finished=False,
                )
                if case == "verified":
                    create_kwargs['verified'] = True
                elif case == "resat_pass":
                    create_kwargs['resat_pass'] = True
                create_new = CredibilityCodes.objects.create(**create_kwargs)
                self.response_message = fun_msg_dir['sending_email'][self.ln]
                self.response_data = self.get_response(
                    now_datetime + ATTEMPTS_TIMEOUTS[1], email_object, 1
                )
            return self.response_status, self.response_message, self.response_data

        # تحقق من وقت الانتظار بين المحاولات
        wait_time = ATTEMPTS_TIMEOUTS.get(code_obj.number_attempts, timedelta(hours=6))
        extra_time = code_obj.updated_at + wait_time
        if now_datetime < extra_time:
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.response_message = fun_msg_dir['not_sending_email'][self.ln]
            self.response_data = self.get_response(
                extra_time, email_object, code_obj.number_attempts
            )
            return self.response_status, self.response_message, self.response_data

        # زيادة عدد المحاولات وإرجاع بيانات الكود الحالي
        code_obj.number_attempts += 1
        code_obj.save()
        self.response_status = status.HTTP_200_OK
        self.response_message = fun_msg_dir['sending_email'][self.ln]
        self.response_data = self.get_response(
            now_datetime + wait_time, email_object, code_obj.number_attempts
        )
        return self.response_status, self.response_message, self.response_data

    def _block_user(self, email_object, fun_msg_dir):
        email_object.user.is_active = False
        email_object.user.save()
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = fun_msg_dir['block_account'][self.ln]
        self.response_data = self.get_response(now(), email_object, 0)