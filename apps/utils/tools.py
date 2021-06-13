import rstr
import oath
import os


def generate_random_identifier(len):
    return rstr.digits(len)


def get_totp(period=180):
    totp = oath.totp(os.environ.get('OTP_SECRET_KEY'),
                     format='dec6', period=period)
    return totp


def is_valid_otp(totp):
    return oath.accept_totp(os.environ.get('OTP_SECRET_KEY'), totp, format='dec6', period=180, forward_drift=2)[0]


def send_sms(to, message):
    # TODO: method will be implemented soon
    pass
