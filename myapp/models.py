

# class Users(models.Model):  # Class name should be capitalized by convention
    
#     def save(self, *args, **kwargs):
#         # Ensure ausID is set as the part before '@aus.edu' in the email
#         if self.email.endswith("@aus.edu"):
#             self.ausID = self.email.replace("@aus.edu", "")
#         super(Users, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.email  # Use `email` as the string representation
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ausID = models.CharField(max_length=25, unique=True, primary_key=True)  # Unique AUS ID as primary key
    email = models.EmailField(unique=True)  # Email as username
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    password = models.CharField(max_length=128)  # Corrected field
    type = models.IntegerField(choices=[(1, 'Admin'), (2, 'User')])  # User type: Admin or User
    fname = models.CharField(max_length=25)  # First name
    lname = models.CharField(max_length=25)  # Last name

    # Fixes for reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # Specify email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'ausID', 'fname', 'lname', 'type']  # Required fields for creating a user

    def __str__(self):
        return self.email
# Room model
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)  # Unique room number
    capacity = models.IntegerField()  # Capacity of the room
    location = models.CharField(max_length=100)  # Room location
    equipment = models.TextField(blank=True, null=True)  # Allow blank and NULL values
    is_available = models.BooleanField(default=True)  # Availability status

    def __str__(self):
        return f"Room {self.room_number} ({self.location})"

# Booking model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")  # Main user booking the room
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")  # Room being booked
    start_time = models.DateTimeField()  # Booking start time
    end_time = models.DateTimeField()  # Booking end time
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Booking status
    added_users = models.ManyToManyField(User, related_name="shared_bookings", blank=True)  # Users shared in the booking

    def __str__(self):
        return f"Booking {self.id} - Room {self.room.room_number} by {self.user.email}"

# Waiting List model
class WaitingList(models.Model):
    PRIORITY_CHOICES = [
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="waiting_list")  # Room for the waiting list
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="waiting_list_entries")  # User in the waiting list
    start_time = models.DateTimeField()  # Start time of desired booking
    end_time = models.DateTimeField()  # End time of desired booking
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)  # Priority level
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when added to the waiting list

    def __str__(self):
        return f"Waiting List - Room {self.room.room_number} by {self.user.email}"

# Notifications model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # User to notify
    message = models.TextField()  # Notification message
    is_read = models.BooleanField(default=False)  # Whether the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of notification creation

    def __str__(self):
        return f"Notification for {self.user.email}"

# QR Code Check-in/Check-out model
class CheckInCheckOut(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="check_in_out")  # Associated booking
    check_in_time = models.DateTimeField(blank=True, null=True)  # Check-in time
    check_out_time = models.DateTimeField(blank=True, null=True)  # Check-out time

    def __str__(self):
        return f"Check-In/Out for Booking {self.booking.id}"
