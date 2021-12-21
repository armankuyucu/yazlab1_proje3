import os

import nltk
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from djangoProject.settings import BASE_DIR
from .models import Document
from .filters import Query1Filter, Query2Filter
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage
from nltk.tokenize import word_tokenize, line_tokenize
import pdfplumber
import re


@login_required
def userPanel(request):
    # if request.method == 'POST':
    #     uploaded_file = request.FILES['document']
        # fs = FileSystemStorage()
        # filename = uploaded_file.name  # fs.save(uploaded_file.name, uploaded_file)
        # queryset = Document.objects.filter(name=filename)
        # all_objects = Document.objects.all()
        # for document in all_objects:
        #     if document.name == os.path.join(BASE_DIR, f'media/{uploaded_file}'):
        #         print('GİRDİ!!!!')
        #         controlBool = False
        # extract_info(request, uploaded_file)
        # return render(request, 'base/userpanel.html')

    document_list = Document.objects.filter(user=request.user)  # return objects of the logged-in user
    document_filter1 = Query1Filter(request.GET, queryset=document_list)
    document_filter2 = Query2Filter(request.GET, queryset=document_list)
    # myFilter = DocumentFilter(request.GET, queryset=documents)
    # document_filter = DocumentFilter(request.GET, queryset=myFilter)
    context = {
        'myFilter1': document_filter1,
        'myFilter2': document_filter2
    }
    return render(request, 'base/userpanel.html', context)


def info(request):
    all_objects = Document.objects.all()
    context = {
        'all_objects': all_objects
    }
    return render(request, 'base/info.html', context)


@staff_member_required
def adminPanel(request):
    document_list = Document.objects.all()
    document_filter1 = Query1Filter(request.GET, queryset=document_list)
    document_filter2 = Query2Filter(request.GET, queryset=document_list)
    # myFilter = DocumentFilter(request.GET, queryset=documents)
    # document_filter = DocumentFilter(request.GET, queryset=myFilter)
    context = {
        'myFilter1': document_filter1,
        'myFilter2': document_filter2
    }
    return render(request, 'base/adminpanel.html', context)


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        extract_info(request, uploaded_file)

    return render(request, 'base/upload.html')


def extract_info(request, uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        # page 2
        page = pdf.pages[1]
        text = page.extract_text()
        lineList = line_tokenize(text)
        # print(lineList)
        lectureName = ""
        advisorName = ""
        jury_list = []

        for i in range(len(lineList)):
            if "BİLGİSAYAR MÜHENDİSLİĞİ" in lineList[i]:
                lectureName = lineList[i + 1]
                lectureName = lectureName.strip()
            elif "Danışman" in lineList[i]:
                advisorName = lineList[i - 1]
                advisorName = advisorName.strip()
            if "Jüri" in lineList[i]:
                jury_list.append(lineList[i - 1])

        for i in range(len(jury_list)):
            jury_list[i] = jury_list[i].strip()

        lastLine = word_tokenize(lineList[-1])
        # print(lastLine)
        datetime = []
        for i in range(len(lastLine)):
            if lastLine[i] == ":":
                datetime = lastLine[-1].split(".")

        year = datetime[2]
        month = int(datetime[1])

        if 3 <= month <= 8:
            term = year + " Bahar"
        else:
            term = year + " Güz"

        term = term.strip()

        # page 3

        page = pdf.pages[2]
        text = page.extract_text()
        lineList = line_tokenize(text)
        print(lineList)

        names = re.split(r".*\d{4}", lineList[-1])
        names[-1] = names[-1].strip()
        names[-1] = names[-1].split(",")
        names_list = names[-1]

        for i in range(len(names_list)):
            names_list[i] = names_list[i].strip()

        # finds the student number(s)
        page = pdf.pages[3]
        text = page.extract_text()
        lineList = line_tokenize(text)

        student_numbers = []
        for i in range(len(lineList)):
            if "Öğrenci No:" in lineList[i]:
                student_numbers.append(lineList[i].split("Öğrenci No: ")[1])

        for i in range(len(student_numbers)):
            student_numbers[i] = student_numbers[i].strip()

        # finds the evening or daytime education by checking student numbers
        type_of_education = []

        if student_numbers:
            for i in range(len(student_numbers)):
                if student_numbers[i][5] == "1":
                    type_of_education.append("birinci öğretim")
                else:
                    type_of_education.append("ikinci öğretim")

        # finds the page number containing abstract information
        pageNumber = -1
        totalpages = len(pdf.pages)

        for i in range(totalpages):
            if "ÖZET" in pdf.pages[i].extract_text():
                pageNumber = i

        page = pdf.pages[pageNumber]
        text = page.extract_text()
        lineList = line_tokenize(text)
        # print(lineList)

        title = ""
        abstract = ""
        abstractLineNumber = -1
        keywordsLineNumber = -1

        # finds line numbers of keyWords and abstract
        for i in range(len(lineList)):
            if "ÖZET" in lineList[i]:
                title = lineList[0] + lineList[1]
                abstractLineNumber = i
            elif "Anahtar" in lineList[i]:
                keywordsLineNumber = i

        title = title.strip()

        # extract abstract
        for i in range(abstractLineNumber + 1, keywordsLineNumber):
            abstract += lineList[i]

        abstract = abstract.strip()

        words_list = []
        keywords_list = []
        keywords_text = ""

        # extracts keywords
        for i in range(keywordsLineNumber, len(lineList)):
            keywords_text += lineList[i]

        keywords_text = keywords_text.split("Anahtar  kelimeler:  ", 1)[-1].strip()
        keywords_list = keywords_text.split(", ")
        # removes the dot from end of the last keyword
        keywords_list[-1] = keywords_list[-1].replace(".", "")

        for i in range(len(keywords_list)):
            keywords_list[i] = keywords_list[i].strip()

        print("----------")
        print("lectureName:", lectureName)
        print("advisorName:", advisorName)
        print("term:", term)
        print("names list:", names_list)
        print("jury list:", jury_list)
        print("student numbers:", student_numbers)
        print("title:", title)
        print("keywords:", keywords_list)
        print("abstract:", abstract)
        print("type of education:", type_of_education)

        # # Convert lists to string
        # author = ""
        # for i in names_list:
        #     author += i + " "
        #
        # student_id = ""
        # for i in student_numbers:
        #     student_id += i + " "
        #
        # type_of_education_str = ""
        # for i in type_of_education:
        #     type_of_education_str += i + " "
        #
        # keywords = ""
        # for i in keywords_list:
        #     keywords += i + " "
        #
        # jury = ""
        # for i in jury_list:
        #     jury += i + " "

        # Save to the database
        Document.objects.create(name=os.path.join(BASE_DIR, f'media/{uploaded_file}'),
                                title=title,
                                user=request.user,
                                author=names_list,
                                pdf=uploaded_file,
                                student_id=student_numbers,
                                type_of_education=type_of_education,
                                lecture_name=lectureName,
                                abstract=abstract,
                                term=term,
                                keywords=keywords_list,
                                advisor=advisorName,
                                jury=jury_list)

        # Document.objects.all().delete()  # delete all rows in the table
