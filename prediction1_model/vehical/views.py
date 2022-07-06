from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import Disease,Patient,Doctor,Feedback,Status,Type,Searched_Patient,Searched_symptom2
import datetime
import json
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import TopSongPoularity

# Create your views here .
def index(request):
    return render(request, "index.html", {})
def Home(request):
    return render(request,'carousel.html')


def Admin_Home(request):
    doc=0
    pat=0
    feed=0
    dis=0
    for i in Disease.objects.all():
        dis+=1
    for i in Patient.objects.all():
        pat+=1
    for i in Doctor.objects.all():
        doc+=1
    for i in Feedback.objects.all():
        feed+=1
    d = {'doc':doc,'pat':pat,'feed':feed,'dis':dis}
    return render(request,'admin_home.html',d)

def User_Home(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error':error}
    return render(request,'patient_home.html',d)

def Doctor_Home(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error}
    return render(request,'doctor_home.html',d)


def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Gallery(request):
    return render(request,'gallery.html')

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Patient.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                stat = Status.objects.get(status="Accept")
                pure=False
                try:
                    pure = Doctor.objects.get(status=stat,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error="notmember"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            return redirect('admin_home')
            error="pat"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type=="Patient":
            Patient.objects.create(user=user,contact=con,address=add,image=im,dob=d)
        else:
            stat = Status.objects.get(status='pending')
            Doctor.objects.create(dob=d,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error}
    return render(request,'register.html',d)

def Add_Doctor(request):
    error = ""
    type=Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        cat = request.POST['type']
        add = request.POST['add']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        stat = Status.objects.get(status='Accept')
        Doctor.objects.create(category=cat,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error,'type':type}
    return render(request,'add_doctor.html',d)

def Add_Disease(request):
    type = Type.objects.all()
    error = ""
    if request.method == 'POST':
        d = request.POST['d_name']
        s = request.POST['sym']
        t = request.POST['type']
        dat = datetime.date.today()
        ty = Type.objects.get(name=t)
        Disease.objects.create(name=d,symptom=s,type=ty)
        error = "create"
    d = {'error':error,'type':type}
    return render(request,'add_disease.html',d)

def Edit_Doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    type = Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['type']
        try:
            im = request.FILES['image']
            doc.image=im
            doc.save()
        except:
            pass
        dat = datetime.date.today()
        doc.user.first_name = f
        doc.user.last_name = l
        doc.user.email = e
        doc.contact = con
        doc.category = cat
        doc.address = add
        doc.user.save()
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_doctor.html',d)

def Edit_My_deatail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    type = Type.objects.all()
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        try:
            im = request.FILES['image']
            sign.image = im
            sign.save()
        except:
            pass
        to1 = datetime.date.today()
        sign.user.first_name = f
        sign.user.last_name = l
        sign.user.email = e
        sign.contact = con
        if error != "pat":
            cat = request.POST['type']
            sign.category = cat
            sign.save()
        sign.address = add
        sign.user.save()
        sign.save()
        terror = "create"
    d = {'error':error,'terror':terror,'doc':sign,'type':type}
    return render(request,'edit_profile.html',d)

def Edit_Disease(request,pid):
    doc = Disease.objects.get(id=pid)
    type = Type.objects.all()
    error = ""
    if request.method == 'POST':
        d = request.POST['d_name']
        s = request.POST['sym']
        t = request.POST['type']
        dat = datetime.date.today()
        doc.name = d
        doc.symptom = s
        ty = Type.objects.get(name=t)
        doc.type = ty
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_disease.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def View_Doctor(request):
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)

def View_Patient(request):
    patient = Patient.objects.all()
    d = {'patient':patient}
    return render(request,'view_patient.html',d)

def View_Disease(request):
    dis = Disease.objects.all()
    d = {'dis':dis}
    return render(request,'view_disease.html',d)

def View_Feedback(request):
    dis = Feedback.objects.all()
    d = {'dis':dis}
    return render(request,'view_feedback.html',d)

def View_Notification(request):
    dis = Searched_Patient.objects.all()
    d = {'dis':dis}
    return render(request,'view_notify.html',d)

def View_My_Detail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error,'pro':sign}
    return render(request,'profile_user.html',d)

def Predict_disease(request,pid):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    a = ""
    try:
        a = Searched_symptom2.objects.get(id=1)
    except:
        pass
    if not a:
        a = Searched_symptom2.objects.create(idso="",name="",name1="",name2="",num=0)
    li = []
    doc = ""
    count=0
    count2=""
    dis = ""
    symp = ""
    ids = []
    if pid != "None":
        if request.method == "POST":
            se = request.POST['sym']
            a.name1 += se + ","
            a.name2 += se + ","
            a.save()
            if a.idso:
                for k in a.idso.split(','):
                    if not k:
                        pass
                    else:
                        ids.append(int(k))
                symp = Disease.objects.filter(symptom__icontains=se, id__in=ids)
                for i in symp:
                    e = 0
                    if not str(i.id) in a.idso:
                        a.idso += str(i.id) + ","
                        a.save()
                    c = i.symptom
                    c = c.split(',')
                    for g in c:
                        try:
                            if not g in a.name:
                                if not g in a.name2:
                                    if not g in a.name1:
                                        a.name += g + ","
                                        a.save()
                                        break
                        except:
                            pass
                a.name1 += a.name
                a.save()
                terror = "start"
                count = 0
                if a.name == "":
                    li = a.name2.split(',')[-2]
                    count += 1
                    count2 = li
                else:
                    li = a.name.split(',')
                    a.name = ""
                    a.save()
                    for j in li:
                        if j != "":
                            count += 1
                            count2 = j
                if count == 1:
                    terror = "End"
                    try:
                        dis = Disease.objects.get(symptom__icontains=count2,id__in=ids)
                        doc = Doctor.objects.filter(category=dis.type.name)
                        for o in doc:
                            searched = Searched_Patient.objects.create(doctor=o, user=sign,
                                                                       date1=datetime.datetime.today(),
                                                                       type=dis.type, disease=dis.name,
                                                                       symptom=a.name2)
                    except:
                        pass

                    a.idso = ""
                    a.name1 = ""
                    a.name2 = ""
                    a.name = ""
                    a.num = 0
                    a.save()
            else:
                symp = Disease.objects.filter(symptom__icontains=se)
                for i in symp:
                    a.idso += str(i.id) + ","
                    ids.append(i.id)
                    a.save()
                    c = i.symptom
                    c = c.split(',')
                    f = 0
                    for g in c:
                        try:
                            if not g in a.name:
                                if not g in a.name2:
                                    if not g in a.name1:
                                        a.name += g + ","
                                        a.save()
                                        break
                        except:
                            pass
                a.name1 += a.name
                a.save()
                terror = "start"
                count = 0
                if a.name == "":
                    li = a.name2.split(',')[-2]
                    count += 1
                    count2 = li
                else:
                    li = a.name.split(',')
                    a.name = ""
                    a.save()
                    for j in li:
                        if j != "":
                            count += 1
                            count2 = j
                if count == 1:
                    terror = "End"
                    try:
                        dis = Disease.objects.get(symptom__icontains=count2,id__in=ids)
                        doc = Doctor.objects.filter(category=dis.type.name)
                        for o in doc:
                            searched = Searched_Patient.objects.create(doctor=o, user=sign,
                                                                       date1=datetime.datetime.today(),
                                                                       type=dis.type, disease=dis.name,
                                                                       symptom=a.name1)

                    except:
                        pass
                    a.idso = ""
                    a.name1 = ""
                    a.name2 = ""
                    a.name = ""
                    a.num = 0
                    a.save()

    else:
        terror = "start"
        for k in a.idso.split(','):
            if not k:
                pass
            else:
                ids.append(int(k))
        symp = Disease.objects.filter(id__in=ids)
        for i in symp:
            c = i.symptom
            c = c.split(',')
            for g in c:
                try:
                    if not g in a.name:
                            if not g in a.name2:
                                if not g in a.name1:
                                    a.name += g + ","
                                    a.save()
                                    break
                except:
                    pass
        a.name1 += a.name
        a.save()
        count = 0
        if a.name == "":
            li = a.name2.split(',')[-2]
            count += 1
            count2 = li
        else:
            li = a.name.split(',')
            a.name = ""
            a.save()
            for j in li:
                if j != "":
                    count += 1
                    count2 = j
        if count == 1:
            terror = "End"
            try:
                dis = Disease.objects.get(symptom__icontains=count2,id__in=ids)
                doc = Doctor.objects.filter(category=dis.type.name)
                for o in doc:
                    searched = Searched_Patient.objects.create(doctor=o, user=sign, date1=datetime.datetime.today(),
                                                               type=dis.type, disease=dis.name, symptom=a.name1)
            except:
                pass

            a.idso = ""
            a.name1 = ""
            a.name2 = ""
            a.name = ""
            a.num = 0
            a.save()
    d = {'error': error,'terror': terror,'pro':sign,'li':li,'count2':count2,'dis':dis,'doc':doc}
    return render(request,'predict_disease.html',d)

def View_My_Notification(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    search = Searched_Patient.objects.filter(doctor=sign)
    d = {'error': error,'pro':search}
    return render(request,'notification.html',d)

def delete_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    doc.delete()
    return redirect('view_doctor')

def delete_notification(request,pid):
    doc = Searched_Patient.objects.get(id=pid)
    doc.delete()
    if request.user.is_staff:
        return redirect('view_notify')
    else:
        return redirect('notification')

def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

def delete_patient(request,pid):
    doc = Patient.objects.get(id=pid)
    doc.delete()
    return redirect('view_patient')

def delete_disease(request,pid):
    doc = Disease.objects.get(id=pid)
    doc.delete()
    return redirect('view_disease')


def Search_Doctor(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    doc = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    li=[]
    t = ""
    if request.method == "POST":
        t = request.POST['type']
        te = request.POST['tex']
        te1 = te.lower()
        if t == "Name":
            user1 = User.objects.filter(first_name__icontains=te1)|User.objects.filter(last_name__icontains=te1)
            for i in user1:
                li.append(i.id)
            doc= Doctor.objects.all()
        elif t == "Type":
            doc = Doctor.objects.filter(category__icontains=te)
        else:
            doc = Doctor.objects.filter(address__icontains=te)
        for i in doc:
            Searched_Patient.objects.create(user=sign,doctor=i,date1=datetime.datetime.today())
    d = {'error': error,'pro':sign,'li':li,'doc':doc,'t':t}
    return render(request,'search_doctor.html',d)

def sent_feedback(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    to1 = datetime.date.today()
    if request.method == "POST":
        t = request.POST['uname']
        te = request.POST['msg']
        Feedback.objects.create(user=sign,messages=te,date=to1)
        terror = "create"
    d = {'error': error,'user':sign,'terror':terror}
    return render(request,'sent_feedback.html',d)

def Change_Password(request):
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    if not request.user.is_staff:
        try:
            sign = Patient.objects.get(user=user)
            if sign:
                error = "pat"
        except:
            sign = Doctor.objects.get(user=user)
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign}
    return render(request,'change_password.html',d)

def Assign_Status(request,pid):
    a = Doctor.objects.get(id=pid)
    terror = False
    if request.method =="POST":
        s = request.POST['stat']
        u = request.POST['uname']
        stat = Status.objects.get(status=s)
        a.status = stat
        a.save()
        terror=True
    d = {'prod': a,'terror':terror}
    return render(request,'assign_status.html',d)
class ListTopSongs(View):
    # set default page limit as 10
    page_limit = 10 # default

    '''
    Helper method to get the pagination context
    out of queryset of given page number with limit.
    Args: 
        queryset: Filtered queryset object
        page: a number representing the page number
        limit: the result count, per page.

    Returns the JSON of queryset for the given page, 
        with pagination meta info.
    '''
    def get_paginated_context(self, queryset, page, limit):
        if not page:    page = 1 # if no page provided, set 1

        # if limit specified, set the page limit
        if limit:   
            self.page_limit = limit  

        # instantiate the paginator object with queryset and page limit
        paginator = Paginator(queryset, self.page_limit)
        # get the page object
        page_obj = paginator.get_page(page)
        # serialize the objects to json
        
        serialized_page = serialize("json", page_obj.object_list)
        # get only required fields from the serialized_page json.
        serialized_page = [obj["fields"] for obj in json.loads(serialized_page)]

        # return the context.
        return {
            "data": serialized_page,
            "pagination": {
                "page": page,
                "limit": limit,
                "has_next": page_obj.has_next(),
                "has_prev": page_obj.has_previous(),
                "total": queryset.count()
            }
        }

    '''
    GET method for this View.
    '''
    def get(self, request, *args, **kwargs):
        # fetch the query params
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        country = request.GET.get('country')
        start = request.GET.get('start')
        end = request.GET.get('end')
        pop = request.GET.get('pop')
        
        

        sort_by = request.GET.get('sort_by')
        # get all results from DB.
        queryset = TopSongPoularity.objects.all()

        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if country and country != "all":
            queryset = queryset.filter(country=country)
        # 2. On basis of date (start and end date)
        if start and end:
            if start != "0" and end != "0":
                queryset = queryset.filter(
                    year__gte = start, 
                    year__lte = end
                )
        
        if pop and pop != "all":
            queryset = queryset.filter(pop=pop)

        # 3. Sorting the filtered queryset
        if sort_by and sort_by != "0":
            queryset = queryset.order_by(sort_by)

        # return the serialized output by 
        # calling method 'get_paginated_context'
        to_return = self.get_paginated_context(queryset, page, limit)
        return JsonResponse(to_return, status = 200)

def getCountries(request):
    # get Countries from the database 
    # excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        country = TopSongPoularity.objects.all().\
                values_list('country').distinct()
        country = [c[0] for c in list(country)]

        return JsonResponse({
            "country": country, 
        }, status = 200)

def getPops(request):
    # get Countries from the database 
    # excluding null and blank values
    if request.method == "GET" and request.is_ajax():
        pop = TopSongPoularity.objects.all().\
                values_list('pop').distinct()
        pop = [c[0] for c in list(pop)]

        return JsonResponse({
            "pop": pop, 
        }, status = 200)