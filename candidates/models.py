from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    requirements = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    resume_text = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    ai_score = models.IntegerField(default=0)
    ai_evaluation = models.JSONField(null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
