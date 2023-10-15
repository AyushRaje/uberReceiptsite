from django.shortcuts import render,redirect
import pandas as pd
import PyPDF2
import openpyxl
import os
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_control
from main.models import Data
import io

from django.http.response import HttpResponse

from xlsxwriter.workbook import Workbook



def index(request):
  context={'converted':False}
  return render(request,'index.html',context)

def download_excel(request):

    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'Total')
    worksheet.write(0, 1, 'Date')
    worksheet.write(0, 2, 'Time')
    worksheet.write(0, 3, 'From')
    worksheet.write(0, 4, 'To')
    worksheet.write(0, 5, 'Distance')
    data = Data.objects.all()
    data=list(data.values_list())
    row_index=1
    print(data)
    print(row_index)
    for objects in data:
      for col_index,value in enumerate(objects[1:]):
        worksheet.write(row_index,col_index,value)
      row_index=row_index+1
    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=output.xlsx"

    output.close()

    return response
# Create your views here.
@csrf_protect
def convertview(request):
    if request.method=='GET':
      context={'converted':True}
      return redirect('index')
    
    if request.method=='POST':
          pdf_file=request.FILES['pdfFile']
          if pdf_file:
            df=convertToExcel(pdf_file)
            context={'converted':True}
            return redirect('index')
          else:
            return redirect('index')
        

def convertToExcel(pdfFileObj):

    # pdfFileObj = open('/content/Receipt_13Aug2023_121314.pdf', 'rb') # uber reciept
     # Replace with the path to your excel file
    
  pdfReader = PyPDF2.PdfReader(pdfFileObj)
  all_data = ''
  for i in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[i]
    ride_data = pageObj.extract_text()
    all_data = all_data + ride_data

  not_working = all_data.split('\n')
  not_working = [i for i in not_working if i!= '']
  not_working = [i.strip() for i in not_working]
  loc = []
  data_to_append = { }
  data_to_append['Date'] = not_working[1][0:7].strip()
  data_to_append['Time'] = not_working[1][-8:].strip()
  for i in not_working[0:10]:
    if i[0] == '|':
      loc.append(i.split('|')[1].strip())
  data_to_append['From'] = loc[0]
  data_to_append['To']= loc[1]
  for i in range(len(not_working)):
    if not_working[i] == 'Total' and not_working[i+1] == '₹':
      #print(not_working[i+2])
      data_to_append['Total'] = not_working[i+2]
  for i in not_working:
    if 'meters' in i:
      data_to_append['Distance'] = i.split('|')[0].strip()
      
     
      # file_path = 'static/output.xlsx'

      # if not os.path.exists(file_path):
      #   wb = openpyxl.Workbook()
      #   wb.save(file_path)
      #   existing_df = pd.read_excel(file_path)
      #   new_df = pd.DataFrame(data_to_append, index=[0])

      #   updated_df = pd.concat([existing_df, new_df], ignore_index=True)
      #   updated_df.to_excel(file_path, index=False)
      # else :
      #   existing_df = pd.read_excel(file_path)
      #   new_df = pd.DataFrame(data_to_append, index=[0])

      #   updated_df = pd.concat([existing_df, new_df], ignore_index=True)
      #   updated_df.to_excel(file_path, index=False)
    new_data=Data.objects.create()
    new_data.Total=data_to_append['Total']
    new_data.Date=data_to_append['Date']
    new_data.Time=data_to_append['Time']
    new_data.From=data_to_append['From']
    new_data.To=data_to_append['To']
    new_data.Distance=data_to_append['Distance']
    new_data.save()
     
      
    print(new_data)
    return new_data