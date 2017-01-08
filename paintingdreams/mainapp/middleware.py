class XRealIPMiddleware(object):
	"""Replaces REMOTE_ADDR with the value X-Real-IP header"""

	def process_request(self, request):
		try:
			real_ip = request.META['HTTP_X_REAL_IP']
		except KeyError:
			return None
		else:
			request.META['REMOTE_ADDR'] = real_ip


class XForwardedForMiddleware(object):
    """Replaces REMOTE_ADDR with the value of the X-Forwarded-For header"""

    def process_request(self, request):
        try:
            forwarded_for = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            request.META['REMOTE_ADDR'] = forwarded_for
