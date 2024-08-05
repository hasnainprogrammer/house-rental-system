from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Property, Enquiry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def properties(request):
    properties = Property.objects.all()

    # Pagination 
    paginator = Paginator(properties, 6)
    page_number = request.GET.get('page')
    paged_properties = paginator.get_page(page_number)
    context = {
        'properties': paged_properties,
    }
    return render(request, 'properties/properties.html', context)

def property(request, property_id):
    if request.method == "POST":
        user_id = request.user
        enquiry_message = request.POST['message']
        property = Property.objects.get(id=property_id)
        if enquiry_message == '':
            messages.error(request, 'Please enter a message. The message field cannot be left blank.')
            return redirect('property', property_id=property_id)
        else:
            # If same user sends an enquiry for a same property twice
            enq = Enquiry.objects.filter(user_id=user_id, property_id=property_id).exists()
            if enq:
               messages.error(request, 'You have already made an enquiry for this property')
               return redirect('property', property_id=property_id)
            else:
                enquiry = Enquiry(property_id=property, user_id=user_id, message=enquiry_message)
                enquiry.save()  
                messages.success(request, 'Enquiry sends successfully')
                return redirect('property', property_id=property_id)
    else:
        property = Property.objects.get(id=property_id)
        context = {
            'property': property,
        }
        return render(request, 'properties/property.html', context)

def search_property(request):
    property = Property.objects.all()
    address = request.GET['address']
    city = request.GET['city']
    state = request.GET['state']
    maximum_price = request.GET['max-price']
    minimum_price = request.GET['min-price']
    minimum_square_feet = request.GET['min-sqft']
    minimum_rooms = request.GET['min-rooms']
    maximum_rooms = request.GET['max-rooms']
    minimum_bedrooms = request.GET['min-bedrooms']
    user_specify_something = False
    if address:
        property = property.filter(address__iexact=address)
        user_specify_something = True
    if city:
        property = property.filter(city__iexact=city)
        user_specify_something = True
    if state:
        property = property.filter(state__iexact=state)
        user_specify_something = True
    if maximum_price:
        property = property.filter(price__lte=maximum_price)
        user_specify_something = True
    if minimum_price:
        property = property.filter(price__gte=minimum_price)
        user_specify_something = True
    if minimum_square_feet:
        property = property.filter(sqft__gte=minimum_square_feet)
        user_specify_something = True
    if maximum_rooms:
        property = property.filter(rooms__lte=maximum_rooms)
        user_specify_something = True
    if minimum_rooms:
        property = property.filter(rooms__gte=minimum_rooms)
        user_specify_something = True
    if minimum_bedrooms:
        property = property.filter(bedrooms__gte=minimum_bedrooms)
        user_specify_something = True

    context = {
        'user_searched_property': property if user_specify_something else None,
    }
    return render(request, 'properties/search_property.html', context)