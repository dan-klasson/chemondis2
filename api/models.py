from django.db import models
from django.contrib.auth.models import User
import uuid


class Interview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate_name = models.CharField(max_length=254)
    candidate_email = models.EmailField()

    def __str__(self):
        return "{} <{}>".format(self.candidate_name, self.candidate_email)


class CandidateSlot(models.Model):
    date = models.DateTimeField(db_index=True)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(
            self.interview.candidate_name,
            self.date.strftime("%d %b %Y %H:%M")
        )


class InterviewerSlot(models.Model):
    date = models.DateTimeField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(
            self.interview.candidate_name,
            self.date.strftime("%d %b %Y %H:%M")
        )
