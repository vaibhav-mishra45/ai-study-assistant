from django.db import models


class Subject(models.Model):
    """Maps to the existing 'subjects' table."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        managed = False
        db_table = 'subjects'

    def __str__(self):
        return self.name


class Topic(models.Model):
    """Maps to the existing 'topics' table."""
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, db_column='subject_id'
    )
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'topics'
        unique_together = (('subject', 'name'),)

    def __str__(self):
        return self.name


class Note(models.Model):
    """Maps to the existing 'notes' table."""
    id = models.AutoField(primary_key=True)
    topic = models.OneToOneField(
        Topic, on_delete=models.CASCADE, db_column='topic_id'
    )
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'notes'

    def __str__(self):
        return f"Note for {self.topic}"


class StudySession(models.Model):
    """Maps to the existing 'study_sessions' table."""
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, db_column='topic_id'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'study_sessions'

    def __str__(self):
        return f"Session on {self.topic} ({self.duration_minutes} min)"


class Quiz(models.Model):
    """Maps to the existing 'quizzes' table."""
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, db_column='topic_id'
    )
    score = models.IntegerField()
    total_questions = models.IntegerField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    completed_at = models.DateTimeField()
    signature = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'quizzes'

    def __str__(self):
        return f"Quiz #{self.id} — {self.score}/{self.total_questions}"
