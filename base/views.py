import nltk
from django.http import HttpResponse
from django.shortcuts import render
from .models import Document
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from nltk.tokenize import sent_tokenize, word_tokenize, line_tokenize
import pdfplumber
import re

@login_required
def userPanel(request):
    context2 = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context2['url'] = fs.url(name)
        extract_info(uploaded_file)

    context = {
        'document': Document.objects.all()
    }
    return render(request, 'base/userpanel.html', context2)


def extract_info(uploaded_file):
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
                lectureName = lineList[i+1]
                lectureName = lectureName.strip()
            elif "Danışman" in lineList[i]:
                advisorName = lineList[i-1]
                advisorName = advisorName.strip()
            if "Jüri" in lineList[i]:
                jury_list.append(lineList[i-1])

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
        # print(lineList)

        names = re.split(r".*\d{4}", lineList[-1])
        names[-1] = names[-1].strip()
        names[-1] = names[-1].split(",")
        names_list = names[-1]

        for i in range(len(names_list)):
            names_list[i] = names_list[i].strip()


        # find the student number(s)
        page = pdf.pages[3]
        text = page.extract_text()
        lineList = line_tokenize(text)

        stundent_numbers = []
        for i in range(len(lineList)):
            if "Öğrenci No:" in lineList[i]:
                stundent_numbers.append(lineList[i].split("Öğrenci No: ")[1])

        for i in range(len(stundent_numbers)):
            stundent_numbers[i] = stundent_numbers[i].strip()

        # find the page number containing abstract information
        pageNumber = -1

        for i in range(15):
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

        # find line numbers of keyWords and abstract
        for i in range(len(lineList)):
            if "ÖZET" in lineList[i]:
                title = lineList[0] + lineList[1]
                abstractLineNumber = i
            elif "Anahtar" in lineList[i]:
                keywordsLineNumber = i

        title = title.strip()

        # extract abstract
        for i in range(abstractLineNumber+1, keywordsLineNumber):
            abstract += lineList[i]

        abstract = abstract.strip()

        words_list = []
        keywords_list = []
        keywords_text = ""

        # extract keywords
        for i in range(keywordsLineNumber, len(lineList)):
            keywords_text += lineList[i]

        print(keywords_text)
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
        print("student numbers:", stundent_numbers)
        print("title: ", title)
        print("keywords: ", keywords_list)
        print("abstract: ", abstract)
