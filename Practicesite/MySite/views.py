from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sqlite3
from django.http import HttpResponse
from .forms import ContactForm

DBPath = ''

def index(request):
    if request.POST:
        form = ContactForm(request.POST)
        # Если форма прошла валидацию
        if form.is_valid():
            cd = form.cleaned_data
            DBPath = ('Name=%s' % (cd['name']))
            # добавление cookie
            request.session['name'] = cd['name']
    else:
        form = ContactForm()
    return render(request, 'MySite/homePage.html', {'form': form})

class DataBaseWork:
    def __init__(self):
        pass

    def data_base_create(self, name):
        conn = sqlite3.connect(name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE abonents (ip_dest text, port text, login text, password text)""")
        conn.commit()

    def data_base_inserting(self, list, name):
        conn = sqlite3.connect(name)
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO abonents VALUES (?,?,?,?)", list)
        conn.commit()

    def data_base_reading(self, name):
        conn = sqlite3.connect(name)
        cursor = conn.cursor()
        sql = "SELECT * FROM abonents"
        cursor.execute(sql)
        retlist = cursor.fetchall()
        print(retlist)
        conn.commit()
        return retlist


def DBread(request):
    DB = DataBaseWork()
    Path = ''
    # использование cookie
    Path = request.session.get('name')
    try:
        tablelist = DB.data_base_reading(Path)
    except:
        return HttpResponse(Path + '  Es tut uns leid, aber diese Datenbank exsistiert nicht')

    current_page = Paginator(tablelist, 200)
    page = request.GET.get('page')
    try:
        tablelist = current_page.page(page)
    except PageNotAnInteger:
        tablelist = current_page.page(1)
    except EmptyPage:
        tablelist = current_page.page(num_pages)
    return render(request, 'MySite/Table.html', {'values': tablelist})
