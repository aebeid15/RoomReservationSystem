from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import HttpResponse
from .models import Room, Booking
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Room
from django.contrib import messages
# To see the last query Django executed
# print(connection.queries[-1])

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Attempt to find the user by email and password
            user = User.objects.get(email=email, password=password)

            # Save user information to session
            request.session['user_info'] = {
                'email': user.email,
                'ausID': user.ausID,
                'type': user.type,
                'fname': user.fname,
                'lname': user.lname
            }

            # Redirect based on user type
            if user.type == 1:  # Admin user
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            elif user.type == 2:  # Regular user
                return redirect('user_page')  # Redirect to user page
            else:
                messages.error(request, 'Invalid user type.')
        except User.DoesNotExist:
            # Invalid login credentials
            messages.error(request, 'Invalid email or password.')

    # Render the login page for GET request or failed POST
    return render(request, 'login.html')

def admin_view(request):
    # Render the admin dashboard template
    return render(request, 'adminDashboard.html')

def user_loc_view(request):
    # Render the user location page
    return render(request, 'location.html')

def manage_bookings(request):
    return render(request, 'userManage_Booking.html')


def user_view_history(request):
    return render(request, 'ViewBookingHistory.html')

def user_account(request):
    return render(request, 'userLibrary_account.html')



# View to render the manage rooms page
def admin_manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'adminManageRooms.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        room_number = request.POST['room_number']
        location = request.POST['location']
        capacity = request.POST['capacity']
        #is_available = request.POST['is_available'] == 'true' 
        is_available = request.POST.get('is_available') == 'true'

        # Add the room to the database
        room = Room.objects.create(
            room_number=room_number,
            location=location,
            capacity=capacity,
            is_available=is_available
        )

        # Pass room details and `room_added` flag back to the template
        context = {
            'room_added': True,
            'room': room,  # Newly added room details
            'rooms': Room.objects.all(),  # For the room list
        }
        return render(request, 'adminManageRooms.html', context)

    # Default behavior for GET requests
    return redirect('manage_rooms')  # Replace with your URL name


from django.contrib import messages
from django.core.cache import cache

def update_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        try:
            room = Room.objects.get(room_number=room_number)
            room.location = request.POST.get('location')
            room.capacity = request.POST.get('capacity')
            room.is_available = request.POST.get('is_available') == 'true'
            room.save()
            
            # Store success message in session
            messages.success(request, f'Room {room_number} has been successfully updated.')
            
            # Clear any existing messages after rendering
            storage = messages.get_messages(request)
            storage.used = True
            
            return render(request, 'adminManageRooms.html', {
                'rooms': Room.objects.all(),
                'room_updated': True,
                'room': room
            })
        except Room.DoesNotExist:
            messages.error(request, f'Room {room_number} not found.')
    return redirect('admin_manage_rooms')

def remove_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        try:
            room = Room.objects.get(room_number=room_number)
            room.delete()
            
            # Store success message in session
            messages.success(request, f'Room {room_number} has been successfully removed.')
            
            # Clear any existing messages after rendering
            storage = messages.get_messages(request)
            storage.used = True
            
            return render(request, 'adminManageRooms.html', {
                'rooms': Room.objects.all(),
                'room_removed': True,
                'removed_room_number': room_number
            })
        except Room.DoesNotExist:
            messages.error(request, f'Room {room_number} not found.')
    return redirect('admin_manage_rooms')

def admin_manage_users(request):
    return render(request, 'adminUserManagement.html')  # Ensure this template exists

def user_reserve_rooms(request):
    rooms = Room.objects.all()
    if request.method == "POST":
        #if not request.user.is_authenticated:
            #messages.error(request, "You must be logged in to book a room.")
            #return redirect("login")  # Redirect to login page

        room_id = request.POST.get("room_id")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        try:
            room = Room.objects.get(id=room_id)
            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status='active'
            )
            if overlapping_bookings.exists():
                messages.error(request, "Room is not available for the selected time.")
            else:
                Booking.objects.create(
                    user=request.user,
                    room=room,
                    start_time=start_time,
                    end_time=end_time
                )
                messages.success(request, "Room booked successfully!")
        except Room.DoesNotExist:
            messages.error(request, "Invalid room selected.")

    return render(request, "userRoomReservation.html", {"rooms": rooms})

def user_manage_bookings(request):
    bookings = Booking.objects.filter(user=request.user, status='active').order_by("start_time")
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            if action == "cancel":
                booking.status = "cancelled"
                booking.save()
                messages.success(request, "Booking cancelled successfully.")
            elif action == "update":
                # Redirect to the update booking page
                return redirect("update_booking", booking_id=booking_id)
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")

    return render(request, "userManage_Booking.html", {"bookings": bookings})


#update booking function
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = Booking.objects.get(id=booking_id)
        start_time = booking.start_time
        end_time = booking.end_time
        new_room = request.POST.get("new_room_id")
        new_start_time = request.POST.get("new_start_time")
        new_end_time = request.POST.get("new_end_time")

        try:
            new_room = Room.objects.get(id=new_room)
            overlapping_bookings = Booking.objects.filter(
                room=new_room,
                start_time__lt=new_end_time,
                end_time__gt=new_start_time,
                status='active'
            )
            if overlapping_bookings.exists():
                messages.error(request, "Room is not available for the selected time.")
            else:
                booking.room = new_room
                booking.start_time = new_start_time
                booking.end_time = new_end_time
                booking.save()
                messages.success(request, "Booking updated successfully.")
                return redirect("user_manage_bookings")  # Redirect to manage bookings page
        except Room.DoesNotExist:
            messages.error(request, "Invalid room selected.")

    return render(request, "updateBooking.html", {"booking": booking})


# Booking History Page
def user_view_history(request):
    bookings = Booking.objects.filter(user=request.user).exclude(status='active').order_by("-start_time")
    return render(request, "ViewBookingHistory.html", {"bookings": bookings})

def view_rooms(request):
    # Get all rooms from the database
    rooms = Room.objects.all()
    return render(request, 'userRoomReservation.html', {'rooms': rooms})