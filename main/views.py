from django.shortcuts import render
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
      for col_index,value in enumerate(objects):
        worksheet.write(row_index,col_index,value)
      row_index=row_index+1
    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    output.close()

    return response
# Create your views here.
@csrf_protect
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def convertview(request):
    if request.method=='GET':
      context={'converted':False}
      return render(request,'index.html',context)
    
    if request.method=='POST':
        pdf_file=request.FILES['pdfFile']
        df=convertToExcel(pdf_file)
        context={'output':df,'converted':True}
        return render(request,'index.html',context)
    


def convertToExcel(pdfFileObj):

    # pdfFileObj = open('/content/Receipt_13Aug2023_121314.pdf', 'rb') # uber reciept
     # Replace with the path to your excel file
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    all_data = ''
    for page in pdfReader.pages:
      all_data += page.extract_text()

      drive_info = all_data.split('\n')

      

      data_to_append = {
        'Total': drive_info[14],
        'Date': drive_info[9],
        'Time': drive_info[1][-8:].strip(),
        'From': drive_info[3].split('|')[1].strip(),
        'To': drive_info[5].split('|')[1].strip(),
        'Distance': drive_info[7].split('|')[0].strip()
      }
      
     
      file_path = 'static/output.xlsx'

      if not os.path.exists(file_path):
        wb = openpyxl.Workbook()
        wb.save(file_path)
        existing_df = pd.read_excel(file_path)
        new_df = pd.DataFrame(data_to_append, index=[0])

        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_excel(file_path, index=False)
      else :
        existing_df = pd.read_excel(file_path)
        new_df = pd.DataFrame(data_to_append, index=[0])

        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_excel(file_path, index=False)
      # new_data=Data.objects.create()
      # new_data.Total=data_to_append['Total']
      # new_data.Date=data_to_append['Date']
      # new_data.Time=data_to_append['Time']
      # new_data.From=data_to_append['From']
      # new_data.To=data_to_append['To']
      # new_data.Distance=data_to_append['Distance']
      # new_data.save()
     
      
    print(updated_df)
    return updated_df