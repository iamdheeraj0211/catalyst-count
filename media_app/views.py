
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UploadDataForm
from django.views.decorators.csrf import csrf_protect
from .models import UploadDataModel
from  rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd


@csrf_protect
@login_required(login_url='login_url')
def upload_data(request):
    if request.method == 'POST':
        # print(request.data)
        print(request.FILES)
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():
            
            user = request.user if request.user.is_authenticated else None
            
            form.save(user=user)
            
            return redirect('show_url')
    else:
        form = UploadDataForm()
    
    return render(request, 'upload_data/upload_data.html', {'form': form})



@login_required(login_url='login_url')
def showorfileview(request):
    if request.session.has_key("username"):
        data = UploadDataModel.objects.filter(is_deleted=False).order_by('-created_at')
        template_name = 'upload_data/show.html'
        context = {'obj': data}
        return render(request, template_name, {'obj': data, "udata": request.session["username"]})
    else:
        return redirect("login_url")

@login_required(login_url='login_url')
def displayqueryview(request):
    if request.session.has_key("username"):
        data = UploadDataModel.objects.filter(is_deleted=False).order_by('-created_at')
        template_name = 'upload_data/query.html'
        context = {'obj': data}
        return render(request, template_name, {'obj': data, "udata": request.session["username"]})
    else:
        return redirect("login_url") 



class QueryBuildergetAPIView(APIView):
    def get(self,request):
        name=request.query_params.get('keyword',None)
        industry=request.query_params.get('industry',None)
        year_founded=request.query_params.get('year_founded',None)
        city=request.query_params.get('city',None)
        state=request.query_params.get('state',None)
        country=request.query_params.get('country',None)
        employee_from=request.query_params.get('employee_from',None)
        employee_to=request.query_params.get('employee_to',None)


        queruset=UploadDataModel.objects.filter(id=24)
        if queruset.exists():
            queryset=queruset.last()

        excel_file_path = queryset.document.path


        df = pd.read_csv(excel_file_path)
        
        count=0

        column_names = df.columns
        if name:
            # column_name='name'
            for column_name in column_names:
                count += df[column_name].eq(name).sum()
        if industry:
            print("heree")
            column_name='industry'
            if column_name in column_names:
                count += df[column_name].eq(industry).sum()

        if year_founded:
            year_founded=int(year_founded)
            column_name='year founded'
            if column_name in column_names:
                count += df[column_name].eq(year_founded).sum()
        
        if city:
            column_name='locality'
            if column_name in column_names:
                count += df[column_name].eq(city).sum()
        if state:
            column_name='locality'
            if column_name in column_names:
                print(column_name)

                count += df[column_name].eq(state).sum()
        if country:
            column_name='country'
            if column_name in column_names:
                count += df[column_name].eq(country).sum()

        if employee_from:
            employee_from=int(employee_from)
            column_name='current employee estimate'
            if column_name in column_names:
                filtered_df = df[df[column_name] > employee_from]

                count += len(filtered_df)

        if employee_to:
            employee_to=int(employee_to)
            column_name='current employee estimate'
            if column_name in column_names:

                filtered_df = df[df[column_name] > employee_to]

                count += len(filtered_df)

        from django.contrib import messages
        # messages.success(request,f'{count} Records are Found for the Query')
        return Response(f'{count} Records are Found for the Query')
        



def count_field_value(name):
    # Get the latest instance of the model
    latest_instance = UploadDataModel.objects.filter(is_deleted=False).last()

    if latest_instance:
        # Access the file from the instance
        excel_file_path = latest_instance.document.path
        print(latest_instance)

        # Read the Excel file
        df = pd.read_excel(excel_file_path,engine='openpyxl')

        # Check if the query parameter exists as a column in the DataFrame
        if 'name' in df.columns:
            count = (df['name'] == name).sum()
            return count
        else:
            return "Column 'year' not found in the Excel file."
    else:
        return "No instances of the model found."
    

# print(count_field_value('walmart'))