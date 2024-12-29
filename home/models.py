from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import uuid

class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='client_user')
    profile_pic = models.FileField(upload_to="propic", null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.PositiveIntegerField( null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.name
    


class EmergencyContact(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    phone = models.PositiveIntegerField()
    relationship = models.CharField(max_length=255, null=True, blank=True, choices=[
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('friend', 'Friend'),
        ('spouse', 'Spouse'),
        ('other', 'Other')
    ])
    
    date_added = models.DateTimeField(auto_now_add=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.relationship})"
    

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    complaint_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    complaint_type = models.CharField(max_length=100, choices=[
        ('domestic_violence', 'Domestic Violence'),
        ('harassment', 'Harassment'),
        ('assault', 'Assault'),
        ('cybercrime', 'Cybercrime'),
        ('other', 'Other'),
    ])
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    document = models.FileField(upload_to='complaints/', null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    judgment_status= models.BooleanField(default=False)

    def __str__(self):
        return f"Complaint {self.complaint_id} - {self.user.first_name}"
    

class ComplaintStatus(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name= "complaint_status")
    description = models.TextField(null=True, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    date_updated = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='complaints/', null=True, blank=True)


class EmergencyAlert(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name= "emergent")
    date_time = models.DateTimeField(auto_now_add=True)
    dispose = models.BooleanField(default=False)
