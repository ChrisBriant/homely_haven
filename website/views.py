from django.shortcuts import render
from django.conf import settings
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
import random

def home(request):
    hot_properties = Property.objects.all().order_by('date_added')[:5]
    #Get the total width that the proprties will take and pass to the carousel style to handle the animation
    slides_total_length = len(hot_properties)*500
    print(int(slides_total_length / 500))
    max_slides = int(slides_total_length / 500)
    animation_string = f'slides {max_slides*6}s infinite'
    slide_data = '@keyframes slides {'
    for i in range(0,max_slides):
        translate = (i*500) * -1
        if(i > 0):
            percent = i/max_slides * 100
        else:
            percent = 0
        # slide_data.append({
        #     'translate' : translate,
        #     'percent' : percent
        # })
        slide_data += f'{percent}% {{transform: translateX({translate}px);}}'
    slide_data += f'100% {{ transform: translateX(-{slides_total_length}px);}}' + '}'
    news_articles = NewsItem.objects.all()
    return render(request,'website/home.html',{
        'properties' : hot_properties,
        'slides_total_length' : slides_total_length, 
        'slide_data' : slide_data,
        'animation_string' : animation_string,
        'news_articles' : news_articles
    })

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

def view_property(request,property_id):
    try:
        property = Property.objects.get(id=property_id)
    except Exception as e:
        return render(request,'404.html')
    #Get a random picture
    print(settings.BASE_DIR)
    home_images_dir = os.path.join(settings.BASE_DIR,'media/rooms')
    file_list = [ os.path.join(home_images_dir,f) for f in os.listdir(home_images_dir) if os.path.isfile(os.path.join(home_images_dir, f))]
    room_src = random.sample(file_list,1)[0]
    return render(request, 'website/property.html', {'property':property, 'room_src':room_src})


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


