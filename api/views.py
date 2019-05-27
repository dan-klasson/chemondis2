from rest_framework import viewsets
from .serializers import InterviewSerializer
from .models import Interview


class InterviewViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Retrieve an interview.

    list:
    List an interview.

    create:
    Create an interview.

    update:
    Update an interview.

    delete:
    Delete an interview.
    """
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'delete']



# Create your views here.
