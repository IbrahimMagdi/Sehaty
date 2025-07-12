from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ....services.headers.authentication_checker import CheckAuthCall
from ....services.authentication.forgot_password.execute import ForgotPasswordService


@api_view(["PUT", ])
def check_account_api(request):
    call_response = CheckAuthCall(request).not_authenticated()
    if call_response[0] == status.HTTP_200_OK:
        call_response = ForgotPasswordService(request).check_account()

    response_status, response_message, response_data = call_response[0], call_response[1], call_response[2]
    if response_status == status.HTTP_100_CONTINUE:
        return response_data
    elif response_status == status.HTTP_406_NOT_ACCEPTABLE:
        return CheckAuthCall(request).mandatory_sign_out()[2]
    else:
        re_send = {
            'details': response_message,
            'data': response_data,
        }
        return Response(re_send, response_status)


@api_view(["POST", ])
def check_code_api(request):
    call_response = CheckAuthCall(request).not_authenticated()
    if call_response[0] == status.HTTP_200_OK:
        call_response = ForgotPasswordService(request).check_code()

    response_status, response_message, response_data = call_response[0], call_response[1], call_response[2]
    if response_status == status.HTTP_100_CONTINUE:
        return response_data
    elif response_status == status.HTTP_406_NOT_ACCEPTABLE:
        return CheckAuthCall(request).mandatory_sign_out()[2]
    else:
        re_send = {
            'details': response_message,
            'data': response_data,
        }
        return Response(re_send, response_status)


@api_view(["POST", ])
def new_password_api(request):
    call_response = CheckAuthCall(request).not_authenticated()
    if call_response[0] == status.HTTP_200_OK:
        call_response = ForgotPasswordService(request).new_password()

    response_status, response_message, response_data = call_response[0], call_response[1], call_response[2]
    if response_status == status.HTTP_100_CONTINUE:
        return response_data
    elif response_status == status.HTTP_406_NOT_ACCEPTABLE:
        return CheckAuthCall(request).mandatory_sign_out()[2]
    else:
        re_send = {
            'details': response_message,
            'data': response_data,
        }
        return Response(re_send, response_status)
