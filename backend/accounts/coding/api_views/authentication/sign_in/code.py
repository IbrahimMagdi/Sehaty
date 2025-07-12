from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ....services.headers.authentication_checker import CheckAuthCall
from ....services.authentication.sign_in.view import SignInService

@api_view(["PUT", ])
def form_api(request):
    call_response = CheckAuthCall(request).not_authenticated()
    if call_response[0] == status.HTTP_200_OK:
        call_response = SignInService(request).execute()

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