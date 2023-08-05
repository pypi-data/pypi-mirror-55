import logging
import requests


class Client(object):
    __URL_BASE = r'https://smsapi.free-mobile.fr/sendmsg'

    __STATUS_CODE_DESCRIPTION_MAPPING = {
        200: 'SMS has been sent to your mobile.',
        400: 'One mandatory parameter is missing.',
        402: 'Too much SMS have been sent in too small period of time.',
        403: 'Service is not activated in your customer profile or user / pass is incorrect.',
        500: 'Server error. Please try later.',
    }

    def __init__(self, user=None, password=None):
        """
            Description: Object creator

            :param user: User value to send SMS without passing this value for each sending
            :type user: str

            :param password: Password value to send SMS without passing this value for each sending
            :type password: str
        """
        self.__logger = logging.getLogger(self.__module__)

        self.__user = user
        self.__password = password

    def send(self, message, user=None, password=None):
        """
            Description: Send SMS to FreeMobile API

            :param message: Message to send as SMS
            :type message: str

            :param user: User value to send SMS for this specific sending
            :type user: str

            :param password: Password value to send SMS for this specific sending
            :type password: str

            :return: Reply of server
            :rtype: requests.Response
        """

        if (user is not None) and (password is not None):
            data_json = {
                'user': user,
                'pass': password,
                'msg':  message,
            }
        elif (user is None) and (password is None) and (self.__user is not None) and (self.__password is not None):
            data_json = {
                'user': self.__user,
                'pass': self.__password,
                'msg': message,
            }
        else:
            raise ValueError('User or Password is empty. SMS cannot be sent.')

        reply = requests.post(self.__URL_BASE, json=data_json)

        if self.__STATUS_CODE_DESCRIPTION_MAPPING.get(reply.status_code) is not None:
            return reply
        else:
            raise NotImplementedError('Status code {code} is not yet implemented. Check FreeMobile API description.')
