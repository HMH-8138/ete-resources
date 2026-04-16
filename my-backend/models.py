from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    user_id = models.CharField(max_length=50, unique=True, default='')
    phone = models.CharField(max_length=20, blank=True)
    batch = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        app_label = 'auth'
    
    def __str__(self):
        return f"{self.user_id} - {self.email}"


class Resource(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    RESOURCE_TYPE_CHOICES = [
        ('Lab', 'Lab'),
        ('Book', 'Book'),
        ('Question', 'Question'),
        ('Note', 'Note'),
        ('Resource', 'Resource'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)
    level = models.CharField(max_length=10)
    term = models.CharField(max_length=10)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    file_title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_comment = models.TextField(blank=True)
    admin_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'resources'
        ordering = ['-uploaded_at']
        app_label = 'contenttypes'
    
    def __str__(self):
        return f"{self.file_title} - {self.status}"
