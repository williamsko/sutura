class MultiPartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            _format = request.META.get('CONTENT_TYPE', 'application/json')
        elif format == 'application/x-www-form-urlencoded':
            return request.POST
        elif format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultiPartResource, self).deserialize(request, data, _format)
