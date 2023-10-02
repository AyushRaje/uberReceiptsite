from django.shortcuts import render
import pandas as pd
import PyPDF2
import openpyxl
import os
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_control
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
    file_path = r"content/uber.xlsx"  # Replace with the path to your excel file
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
    print(updated_df)
    return updated_df