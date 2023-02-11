from django.shortcuts import render
#from accounts.forms import SignInForm
#from django.http import JsonResponse, HttpResponseRedirect
#from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
from django.db.models import QuerySet
from .forms import *
from .models import *
from propertyadmin.models import *
from datetime import datetime

def home(request):
    hot_properties = Property.objects.all().order_by('date_added')[:5]
    #Get the total width that the proprties will take and pass to the carousel style to handle the animation
    #style_tag = f'style=width:{(len(hot_properties)-1)*500}px;'
    slides_total_length = len(hot_properties)*500
    return render(request,'website/home.html',{'properties' : hot_properties,'slides_total_length' : slides_total_length})

def search(request,page_no):
    #Will always return the same results for demo purposes
    properties = Property.objects.all()
    form = None
    paginator = Paginator(properties,10) # Show 10 items per page.
    #page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    # for item in page_obj:
    #     print(item.picture)
    return render(request,'website/searchresults.html', {'form' : form,'items':page_obj})

@api_view(['POST'])
def get_availabile_slots(request):
    data = request.data
    try:
        booked_viewings = Viewing.objects.filter(date_of_viewing=data['dateToView'],property_id=data['propertyId'])
    except Exception as e:
        return Response({'success':False,'message':'Unable to retrieve bookings'}, status=status.HTTP_400_BAD_REQUEST)
    #Get the available slots
    booked_slots = [bv.slot for bv in booked_viewings]
    all_slots = Slot.objects.all()
    available_slots = [{
        'id' : slot.id, 
        'startTime':slot.start_time.strftime('%H:%M'), 
        'endTime' : slot.end_time.strftime('%H:%M')
    } for slot in all_slots if slot not in booked_slots]
    return JsonResponse(available_slots, safe=False)

@api_view(['POST'])
def book_slot(request):
    data = request.data
    print(request.user)
    #Check user is a customer
    try:
        customer = Customer.objects.get(user=request.user)
    except Exception as e:
        return Response({'success':False,'message':'Unable to locate customer'}, status=status.HTTP_400_BAD_REQUEST)

    #Get agents and select a random one
    #Demo purposes - the agent is random, if real app then it would
    # require logic to select an available agent

    agents = Agent.objects.all()
    if isinstance(agents, QuerySet) and agents.exists():
        selected_agent = agents.order_by('?').first()
    else:
        return Response({'success':False,'message':'Unable to find an available agent'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        #Get the slot, date and property
        slot = Slot.objects.get(id=data['slotId'])
        property = Property.objects.get(id=data['propertyId'])
        viewing_date = datetime.strptime(data['viewingDate'], '%Y-%m-%d')
        print('selected agent', selected_agent)
        Viewing.objects.create(
            agent = selected_agent,
            customer = customer,
            date_of_viewing= viewing_date,
            slot = slot,
            property = property
        )
    except Exception as e:
        print(e)
        return Response({'success':False,'message':'Unable to make booking'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'success':True}, safe=False)


