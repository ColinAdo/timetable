from django.contrib.auth import get_user_model
from django.shortcuts import render

from timetables.models import Timetable

import pandas as pd
import uuid  # Import the uuid module for generating unique IDs


def index(request, batch_id=None):
    template = 'index.html'
    context = {}

    if request.method == 'POST' and 'timetable' in request.FILES:
        # Access the uploaded file from the request
        uploaded_file = request.FILES['timetable']

        try:
            # Read the Excel file using pandas
            df = pd.read_excel(uploaded_file)

            # Generate a unique batch_id for this set of timetables
            batch_id = str(uuid.uuid4())

            # Assuming 'unit_code' and 'unit_name' are the column names in the Excel file
            unit_code_list = df['unit_code'].tolist()
            unit_name_list = df['unit_name'].tolist()

            # Now you have the lists of unit codes and unit names, you can process them further
            # For example, you can create entries in the Timetable model for each unit
            for unit_code, unit_name in zip(unit_code_list, unit_name_list):
                # Create a Timetable instance with placeholder values and assigned batch_id
                timetable_entry = Timetable(
                    owner=request.user,
                    batch_id=batch_id,
                    unit_code=unit_code,
                    unit_name=unit_name,
                    day_of_week='',
                    lesson_time='',
                    lecturer='',
                    campus='',
                    mode_of_study='regular',
                    room='',
                    group=0
                )
                timetable_entry.save()

            # Now you have created entries with unit_code and unit_name, assigned batch_id, and the day_of_week and lesson_time fields are placeholders
            # You can proceed to run the genetic algorithm to assign unique day and time slots

            # ...

        except pd.errors.EmptyDataError:
            # Handle the case where the uploaded file is empty
            context['error_message'] = 'The uploaded file is empty.'

    timetables = None
    user = request.user
    if batch_id:
        timetables = Timetable.objects.filter(owner=user, batch_id=batch_id)
    else:
        # Display the latest batch by default
        latest_batches = Timetable.objects.filter(owner=user).values(
            'batch_id').distinct().order_by('-batch_id')[:1]
        if latest_batches:
            latest_batch_id = latest_batches[0]['batch_id']
            timetables = Timetable.objects.filter(
                owner=user, batch_id=latest_batch_id)


    context = {
        'timetables': timetables,
    }

    return render(request, template, context)



# def display_timetables(request, batch_id=None):
#     # Assuming the user is authenticated
#     template = 'index.html'
#     user = request.user

#     if batch_id:
#         timetables = Timetable.objects.filter(owner=user, batch_id=batch_id)
#     else:
#         # Display the latest batch by default
#         timetables = Timetable.objects.filter(
#             owner=user).order_by('-batch_id').distinct('batch_id')

#     context = {
#         'timetables': timetables,
#     }

#     return render(request, template, context)


def display_all_users_timetables(request):
    template = 'display_all_users_timetables.html'
    User = get_user_model()
    all_users = User.objects.all()
    all_users_timetables = {}

    for user in all_users:
        user_timetables = []
        user_batches = Timetable.objects.filter(owner=user).values(
            'batch_id').distinct().order_by('-batch_id')

        for batch in user_batches:
            batch_id = batch['batch_id']
            timetables_in_batch = Timetable.objects.filter(
                owner=user, batch_id=batch_id)
            user_timetables.append(
                {'batch_id': batch_id, 'timetables': timetables_in_batch})

        all_users_timetables[user.username] = user_timetables

    context = {
        'all_users_timetables': all_users_timetables,
    }

    return render(request, template, context)
