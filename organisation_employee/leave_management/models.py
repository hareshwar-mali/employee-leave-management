from django.contrib.auth.models import User
from django.db import models


class EmployeeProfile(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=4)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=ACTIVE)
    total_cs_leaves = models.IntegerField(default=12)  # Casual Leave (CS)
    total_e_leaves = models.IntegerField(default=12)  # Earned Leave (E)

    def save(self, *args, **kwargs):
        if not self.user:
            # Get or create a User and assign it to self.user
            self.user, created = User.objects.get_or_create(username=self.phone_number)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EmployeeLeave(models.Model):
    SICK_CASUAL = 'CS'
    EARNED = 'E'

    LEAVE_TYPE_CHOICES = [
        (SICK_CASUAL, 'Sick-Casual Leave'),
        (EARNED, 'Earned Leave'),
    ]

    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=15, default='Pending')

    def __str__(self):
        return f"{self.employee.first_name} {self.leave_type} Leave from {self.start_date} to {self.end_date}"
