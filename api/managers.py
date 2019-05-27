from django.db import models


class SlotManager(models.Manager):
    def overlapping(self, interview_id):
        return self.raw('''
            SELECT c.id, c.date, ARRAY_AGG(i.user_id) AS interviewers
            FROM api_candidateslot AS c
            INNER JOIN api_interviewerslot AS i ON c.date = i.date
            WHERE c.interview_id = %s AND i.interview_id = %s
            GROUP BY c.id
            ORDER BY c.date
            ''', [interview_id] * 2
        )
