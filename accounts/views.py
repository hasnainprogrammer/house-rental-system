from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib import messages
from django.contrib import auth
from properties.models import Property, Enquiry
from .forms import AddPropertyForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Custom function
def registration(request, data, user_type):
        username = data['username']
        email_address = data['email-address']
        contact_no = data['contact-no']
        address = data['address']
        password = data['password']
        confirm_password = data['cpassword']
       
        if username == '' or email_address == '' or contact_no == '' or address == '' or password == '' or confirm_password == '':
            messages.error(request, "Please fill all the fields")
            # return HttpResponse('Please fill all the fields') 
        else:
            # check if passwords match
            if password == confirm_password:
            #     # check if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username is taken")
                    # return HttpResponse('Username is taken')
                # check if email is being used
                else:
                    if User.objects.filter(email=email_address).exists():
                        messages.error(request, "Email is being used")
                        # return HttpResponse('Email is being used')
                    else:
                        if user_type == 'owner':
                            user = User(is_owner=True, username=username, email=email_address, contact_no=contact_no, address=address)
                        elif user_type == 'user':
                             user = User(is_user=True, username=username, email=email_address, contact_no=contact_no, address=address)
                        user.set_password(password)
                        user.save()
                        messages.success(request, 'Registered Successfully!')
                        # return HttpResponse('Registered Successfully!')
                        
            else:
                messages.error(request, 'Passwords should match')
                # return HttpResponse('Passwords should match')

def owner_registration(request):
    if request.method == 'POST':
        registration(request, request.POST, 'owner')

        
    return render(request, 'accounts/owner_registration.html')

def user_registration(request):
    if request.method == 'POST':
        registration(request, request.POST, 'user')
    return render(request, 'accounts/user_registration.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '' or password == '':
            messages.error(request, 'Please fill up the fields')
            return redirect('login_user')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, 'Loggedin Successfully')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'accounts/login.html')

def logout_user(request):
    auth.logout(request)
    messages.success(request, 'Loggedout Successfully')
    return redirect('login_user')

def add_property(request):
    if request.user.is_authenticated and request.user.is_owner:
        form = AddPropertyForm()
        if request.method == 'POST':
            form = AddPropertyForm(request.POST, request.FILES)
            if form.is_valid():
                property = form.save(commit=False)
                property.owner_id = request.user
                property.save()
                messages.success(request, 'Property added successfully')
        context = {'form': form}
        return render(request, 'accounts/add_property.html', context)
    else:
        return redirect('login_user')

def manage_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email-address']
        contact_no = request.POST['contact-no']
        address = request.POST['address']
        if username == '' or email == '' or contact_no == '' or address == '':
            messages.error(request, 'Please fill up all the fields')
            return redirect('manage_profile')
        else:
            user = User.objects.get(id=request.user.id)
            user.username = username
            user.email = email
            user.contact_no = contact_no
            user.address = address
            user.save()
            messages.success(request, 'Profile updated successfully')
    return render(request, 'accounts/manage_profile.html')

def send_enquiries(request):
    if request.user.is_authenticated and request.user.is_user:
        enquiries = Enquiry.objects.filter(user_id=request.user.id).order_by('-enquiry_date')
        context = {
            'enquiries': enquiries,
        }
        return render(request, 'accounts/send_enquiries.html', context)
    else:
        return redirect('login_user')

def recieved_enquiries(request):
    if request.user.is_authenticated and request.user.is_owner:
        enquiries = Enquiry.objects.filter(property_id__owner_id=request.user.id).order_by('-enquiry_date')
        context = {
            'enquiries': enquiries,
        }
        return render(request, 'accounts/recieved_enquiries.html', context)
    else:
        return redirect('login_user')

def enquiry_details(request, enquiry_id):
    if request.user.is_authenticated:
        # Owner Remarks
        if request.method == 'POST':
            owner_remarks = request.POST['owner_remarks']
            if owner_remarks == '':
                messages.error(request, 'Remarks field cannot be left blank!')
            else:
                enquiry = Enquiry.objects.get(id=enquiry_id)
                if enquiry.owner_remarks:
                    messages.error(request, 'You have already sent your remarks for this property')
                else:
                    enquiry.owner_remarks = owner_remarks
                    enquiry.remarks_date = datetime.now()
                    enquiry.save()
                    messages.success(request, 'Your remarks have been sent successfully!')

        enquiry = Enquiry.objects.get(id=enquiry_id)
        context = {
            'enquiry': enquiry,
        }
        return render(request, 'accounts/enquiry_details.html', context)
    else:
        return redirect('login_user')

def manage_properties(request):
    if request.user.is_authenticated and request.user.is_owner:
        owner_properties = Property.objects.filter(owner_id=request.user.id)
        
        # Pagination 
        paginator = Paginator(owner_properties, 6)
        page_number = request.GET.get('page')
        paged_properties = paginator.get_page(page_number)
        context = {'owner_properties': paged_properties}

        return render(request, 'accounts/manage_properties.html', context)
    else:
        return redirect('login_user')
    
def delete_property(request, property_id):
    if request.user.is_authenticated and request.user.is_owner:
        deleted_property = Property.objects.get(id=property_id)
        deleted_property.delete()
        messages.success(request, 'Property deleted successfully')
        return redirect('manage_properties')
    else:
        return redirect('login_user')

def book_property(request, property_id):
    if request.user.is_authenticated and request.user.is_owner:
        booked_property = Property.objects.get(id=property_id)
        booked_property.delete()
        messages.success(request, 'That property has being booked/rented')
        return redirect('manage_properties')
    else:
        return redirect('login_user')

def update_property(request, property_id):
    if request.user.is_authenticated and request.user.is_owner:

        updated_property = Property.objects.get(id=property_id)
        if request.method == 'POST':
            # getting updated values
            property_title = request.POST['property_title']
            bathrooms = request.POST['bathrooms']
            bedrooms = request.POST['bedrooms']
            rooms = request.POST['rooms']
            price = request.POST['price']
            garage = request.POST['garage']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']
            sqft = request.POST['sqft']
            main_image = request.FILES.get('main_image')
            image_1 = request.FILES.get('image_1')
            image_2 = request.FILES.get('image_2')
            image_3 = request.FILES.get('image_3')

            wifi = request.POST.get('wifi', 'off')
            kitchen = request.POST.get('kitchen', 'off')
            parking = request.POST.get('parking', 'off')
            swimming_pool = request.POST.get('parking', 'off')
            air_conditioning = request.POST.get('air_conditioning', 'off')
            balcony = request.POST.get('balcony', 'off')
            tv = request.POST.get('tv', 'off')
            laundry = request.POST.get('laundry', 'off')
            elevator_access = request.POST.get('elevator_access', 'off')
            wifi = True if wifi == 'on' else False
            kitchen = True if kitchen == 'on' else False
            parking = True if parking == 'on' else False
            swimming_pool = True if swimming_pool == 'on' else False
            air_conditioning = True if air_conditioning == 'on' else False
            balcony = True if balcony == 'on' else False
            tv = True if tv == 'on' else False
            laundry = True if laundry == 'on' else False
            elevator_access = True if elevator_access == 'on' else False
        
            if property_title == '' or bathrooms == '' or bedrooms == '' or rooms == '' or price == '' or garage == '' or address == '' or city == '' or state == '' or zipcode == '' or sqft == '' or main_image is None or image_1 is None or image_2 is None or image_3 is None:
                messages.error(request, 'Please fill up all the fields')
                return redirect('update_property', property_id=property_id)
            else:
                # updating records
                updated_property.property_title = property_title
                updated_property.bathrooms = bathrooms
                updated_property.bedrooms = bedrooms
                updated_property.rooms = rooms
                updated_property.price = price
                updated_property.garage = garage
                updated_property.address = address
                updated_property.city = city
                updated_property.state = state
                updated_property.zipcode = zipcode
                updated_property.sqft = sqft
                updated_property.main_image = main_image
                updated_property.image_1 = image_1
                updated_property.image_2 = image_2
                updated_property.image_3 = image_3

                updated_property.wifi = wifi
                updated_property.kitchen = kitchen
                updated_property.parking = parking
                updated_property.swimming_pool = swimming_pool
                updated_property.air_conditioning = air_conditioning
                updated_property.balcony = balcony
                updated_property.tv = tv
                updated_property.laundry = laundry
                updated_property.elevator_access = elevator_access
                updated_property.save()
                messages.success(request, 'Property updated successfully')

        context = {
            'updated_property': updated_property,
        }
        return render(request, 'accounts/update_property.html', context)
    else:
        return redirect('login_user')
