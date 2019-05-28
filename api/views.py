from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as APIValidationError
from rest_framework import permissions
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .serializers import SlotSerializer, InterviewSerializer
from .models import CandidateSlot, InterviewerSlot, Interview


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SlotView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    """
    create:
    Create time slots for an interview.

    list:
    List overlapping slots for an interview.
    """
    serializer_class = SlotSerializer

    def save_slots(self, cls, serializer, interview, user=None):
        objects = []
        for date in serializer.validated_data.get('slots'):
            if user:
                obj = cls(
                    interview=interview, date=date.get('date'), user=user
                )
            else:
                obj = cls(interview=interview, date=date.get('date'))
            objects.append(obj)
        try:
            cls.objects.bulk_create(objects)
        except IntegrityError:
            raise APIValidationError({'date': ['Slot(s) already taken.']})

    def create(self, request, interview_pk=None, *args, **kwargs):

        try:
            interview = Interview.objects.get(pk=interview_pk)
        except ValidationError as e:
            raise APIValidationError({'interview': e.messages})

        serializer = SlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            self.save_slots(
                InterviewerSlot, serializer, interview, request.user
            )
        else:
            self.save_slots(CandidateSlot, serializer, interview)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )

    def list(self, request, interview_pk=None, *args, **kwargs):
        slots = CandidateSlot.objects.overlapping(interview_pk)
        result = []
        for slot in slots:
            result.append(
                {'date': slot.date, 'interviewers': slot.interviewers}
            )
        return Response({"slots": result})
