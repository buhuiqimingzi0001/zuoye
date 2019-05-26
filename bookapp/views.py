import datetime
import os
import random
import string
import time
import re
import hashlib
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, redirect
from bookapp.models import TClass,TBook,TUser,TAdds,TOrder,TOrderInfo,Epanding
from bookapp.captcha.image import ImageCaptcha


# Create your views here.
def index(request):
    uname= request.COOKIES.get('name')
    upwd=request.COOKIES.get('password')
    result = TUser.objects.filter(username=uname, password=upwd)
    if result:
        request.session['login'] = 'ok'
        request.session['uname'] = uname
        un = uname
        una=un
    else:
        status = request.session.get('login')
        if status == 'ok':
            un = request.session.get('uname')
            una=un
        else:
            una=0
    ot=TClass.objects.filter(class_pid=None)
    ot2=TClass.objects.filter(class_pid__in=(a for a in range(1,100)))
    bt=TBook.objects.all()
    bt1=bt.order_by('-shelves_date').exclude()[:8]
    bt2=bt.order_by('-sales').exclude()[:8]
    bt3=bt.order_by('-customer_score').exclude()[:8]
    dz = request.get_full_path()
    zj = request.get_host()
    fdz = ('http://' + zj + dz)
    request.session['fdz'] = fdz
    return render(request,'index.html',{'ot':ot,'ot2':ot2,'bt':bt,'bt1':bt1,'bt2':bt2,'bt3':bt3,'una':una})
def details(request):
    uname = request.COOKIES.get('name')
    upwd = request.COOKIES.get('password')
    result = TUser.objects.filter(username=uname, password=upwd)
    if result:
        request.session['login'] = 'ok'
        request.session['uname'] = uname
        un = uname
        una = un
    else:
        status = request.session.get('login')
        if status == 'ok':
            un = request.session.get('uname')
            una = un
        else:
            una = 0
    book_id1 = request.GET.get('book_id')
    book = TBook.objects.get(book_id=book_id1)
    if book.series_name:
        series = '是'
    else:
        series = '否'
    bookpid = book.book_class.class_pid
    bookclan = book.book_class.class_name
    if bookpid:
        bookclpn = TClass.objects.get(class_id=bookpid).class_name
    else:
        bookclpn = bookclan

    discount = int(book.dd_price / book.price * 1000) / 100

    dz = request.get_full_path()
    zj = request.get_host()
    fdz=('http://'+ zj + dz)
    request.session['fdz'] = fdz

    return render(request, 'Book details.html',
                  {'book': book, 'series': series, 'bookclan': bookclan, 'bookclpn': bookclpn, 'discount': discount,'una':una})


def booklist(request):
    uname = request.COOKIES.get('name')
    upwd = request.COOKIES.get('password')
    result = TUser.objects.filter(username=uname, password=upwd)
    if result:
        request.session['login'] = 'ok'
        request.session['uname'] = uname
        un = uname
        una = un
    else:
        status = request.session.get('login')
        if status == 'ok':
            un = request.session.get('uname')
            una = un
        else:
            una = 0
    c1 = TClass.objects.filter(class_pid=None)
    c2 = TClass.objects.filter(class_pid__in=(a for a in range(1, 100)))
    cl1=request.GET.get('first_id')
    cl2=request.GET.get('second_id')
    print(cl1,cl2,'这里')
    if cl1 != None:
        cnl1 = TClass.objects.filter(class_id=cl1)
        cnl1=cnl1[0].class_name
        request.session['cl1'] = cl1
    else:
        request.session['cl1']=None
        cnl1=''
    if cl2 != None:
        cnl2=TClass.objects.filter(class_id=cl2)
        cnl2=cnl2[0].class_name
        request.session['cl2'] = cl2
    else:
        request.session['cl2'] = None
        cnl2=''
    print(cnl1,cnl2)
    number = request.GET.get('number')
    if not number:
        number = 1
    firstid = request.GET.get('first_id')
    secondid = request.GET.get('second_id')
    if firstid or secondid:
        request.session['firstid'] = firstid
        request.session['secondid'] = secondid
    else:
        firstid = request.session.get('firstid')
        secondid = request.session.get('secondid')
    if secondid is None:
        tc = TClass.objects.filter(class_pid=firstid)
        book = TBook.objects.filter(book_class__in=tc)
    else:
        tc = TClass.objects.filter(class_id=secondid)
        book = TBook.objects.filter(book_class=secondid)
    pagtor = Paginator(book, per_page=6)
    number1=pagtor.num_pages
    if int(number)>int(number1):
        number=int(number1)
    page = pagtor.page(number)
    dz = request.get_full_path()
    zj = request.get_host()
    fdz=('http://'+ zj + dz)
    request.session['fdz'] = fdz
    return render(request, 'booklist.html',
                  {'page': page, 'tc': tc, 'firstid': firstid, 'secondid': secondid, 'c1': c1,
                   'c2': c2,'cnl1':cnl1,'cnl2':cnl2,'cl1':cl1,'cl2':cl2,'una':una})
def login(request):
    uname= request.COOKIES.get('name')
    upwd=request.COOKIES.get('password')
    result = TUser.objects.filter(username=uname, password=upwd)
    c = request.session.get('fdz')
    if result:
        if c:
            request.session['login'] = 'ok'
            request.session['uname'] = uname
            return redirect(c)
        else:
            return redirect('index')
    if c:
        redirect(c)
    return render(request,'login.html')

def loginchance(request):
    uname = request.POST.get('txtUsername')
    upwd = request.POST.get('txtPassword')
    captcha = request.POST.get('number')
    code = request.session.get('code')
    choose = request.POST.get('remember')
    c = request.session.get('fdz')
    if captcha.upper() == code.upper():
        result=TUser.objects.filter(username=uname, password=upwd)
        if result:
            if c:
                res=redirect(c)
            else:
                res=redirect('index')
            request.session['login'] = 'ok'
            request.session['uname'] = uname
            if choose == '1':
                res.set_cookie('name', uname, max_age=60 * 60 * 24 * 7)
                res.set_cookie('password', upwd, max_age=60 * 60 * 24 * 7)
                return res
            if c:
                return redirect(c)
            return redirect('index')
        return HttpResponse(
            '<script>alert("登录失败,用户名或密码错误");location.href="http://127.0.0.1:8000/book/login/"</script>')

def logout(request):
    request.session['login'] = 'no'
    request.session['uname'] = 0
    request.delete_cookie('name')
    request.delete_cookie('password')
    c = request.session.get('fdz')
    return redirect(c)


def getcapthcha(request):
    image = ImageCaptcha(fonts=[os.path.abspath("xxx/segoesc.ttf")])
    rand_code=random.sample(string.ascii_letters+string.digits,3)
    rand_code="".join(rand_code)
    request.session['code'] = rand_code
    print(rand_code)
    data=image.generate(rand_code)
    return HttpResponse(data,"image/png")

def register(request):
    return render(request, 'register.html')

def registerchance(request):
            uname = request.POST.get('username')
            upwd = request.POST.get('txt_password')
            captcha = request.POST.get('number')
            code = request.session.get('code')
            request.session['uname'] = uname
            request.session['login'] = 'ok'
            print(uname,upwd,captcha,code)
            if captcha.upper() == code.upper():
                result = TUser.objects.create(username=uname, password=upwd)
                if result:
                    return redirect('register_ok')
                else:
                    return HttpResponse('注册失败')
def register_ok(request):
    uname = request.session.get('uname')
    print(uname,4654)
    flag1=re.match(r"^1[35678]\d{9}$", uname)
    if flag1:
        eh='手机号码'
    else:
        eh='邮箱地址'
    date=datetime.datetime.now()
    return render(request, 'register ok.html',{'uname': uname,'eh': eh})


def checkcapthcha(request):
    time.sleep(2)
    capthcha=request.GET.get("capthcha")
    code=request.session.get('code')
    if capthcha.upper()==code.upper():
        return HttpResponse(0)
    else:
        return HttpResponse(1)
def checkname(request):
    time.sleep(2)
    username=request.GET.get("username")
    result=TUser.objects.filter(username=username)
    if result:
        return HttpResponse(1)
    else:
        p1 = re.match(r"^1[35678]\d{9}$",username)
        p2 = re.match(r"^([a-z]|[A-Z]|[0-9]){1,}@{1}([a-z]|[A-Z]|[0-9]){1,}\.{1}([a-z]|[A-Z]|[0-9]){1,}$",username)
        if p1:
            request.session['phorem'] = 'phone'
            return HttpResponse(0)
        elif p2:
            request.session['phorem'] = 'email'
            return HttpResponse(3)
        else:
            return HttpResponse(2)


def addbook(request):   #加入购物车按钮
    booklist = []
    bookid1 = request.GET.get("bookid")
    count = int(request.GET.get("count"))
    book = TBook.objects.get(pk=int(bookid1))
    booklist1  = request.session.get("booklist")
    if booklist1:
        for i in booklist1:
            booklist.append(i)
            if  i["book_name"] == book.book_name:
                i["count"] = count + i["count"]
                request.session["booklist"] = booklist
                return HttpResponse("ok")
        booklist.append({"id":str(book.book_id),"pics":book.digest_image,"count":count,"book_name":book.book_name,"market_price":book.price,"dangdang_price":book.dd_price})
        request.session["booklist"] = booklist
        return HttpResponse("ok")
    booklist.append({"id": str(book.book_id), "pics": book.digest_image, "count": count, "book_name": book.book_name,"market_price": book.price, "dangdang_price": book.dd_price})
    request.session["booklist"] = booklist
    return HttpResponse("ok")



def car(request):
    uname = request.COOKIES.get('name')
    upwd = request.COOKIES.get('password')
    result = TUser.objects.filter(username=uname, password=upwd)
    if result:
        request.session['login'] = 'ok'
        request.session['uname'] = uname
        un = uname
        una = un
    else:
        status = request.session.get('login')
        if status == 'ok':
            un = request.session.get('uname')
            una = un
        else:
            una = 0
    booklist = request.session.get("booklist")
    booklist2 = request.session.get('booklist2')
    save_price = 0
    save_price2 = 0
    total_price = 0
    total_price2 = 0
    dz = request.get_full_path()
    zj = request.get_host()
    fdz=('http://'+ zj + dz)
    request.session['fdz'] = fdz
    print(booklist,booklist2,'car1')
    if booklist:
        count=0
        for i in booklist:
            total_price += i["dangdang_price"] * i["count"]
            total_price = round(total_price,2)
            save_price += (i["market_price"] - i["dangdang_price"]) * i["count"]
            save_price = round(save_price,2)
            count=count+i['count']
            if booklist2:
                count2 = 0
                for j in booklist2:
                    total_price2 += j["dangdang_price"] * j["count"]
                    total_price2 = round(total_price2, 2)
                    save_price2 += (j["market_price"] - j["dangdang_price"]) * j["count"]
                    save_price2 = round(save_price2, 2)
                    count2 = count2 + j['count']
                return render(request, 'car.html',{"booklist": booklist, "total_price": total_price, "save_price": save_price,'count': count,"booklist2": booklist2, "total_price2": total_price2, "save_price2": save_price2,'count2': count2, 'una': una})
        return render(request, 'car.html',{"booklist":booklist,"total_price":total_price,"save_price":save_price,'count':count,'una':una})
    if booklist2:
        count2 = 0
        for j in booklist2:
            total_price2 += j["dangdang_price"] * j["count"]
            total_price2 = round(total_price2, 2)
            save_price2 += (j["market_price"] - j["dangdang_price"]) * j["count"]
            save_price2 = round(save_price2, 2)
            count2 = count2 + j['count']
        return render(request, 'car.html',
                      {
                       "booklist2": booklist2, "total_price2": total_price2, "save_price2": save_price2,
                       'count2': count2, 'una': una})
    return render(request,'car.html',{'una':una})

def delcar(request):
    bookid = request.GET.get("bookid")
    booklist = request.session.get("booklist")
    booklist2 =request.session.get('booklist2')
    if booklist2:
        booklist2=booklist2
    else:
        booklist2 = []
    print(booklist,booklist2,'delcar1')
    for i in booklist:
        if bookid == i["id"]:
            for j in booklist2:
                if bookid ==  j['id']:
                    j['count']=j['count']+i['count']
                    booklist.remove(i)
                    break
            else:
                booklist.remove(i)
                booklist2.append(i)
    print(booklist,booklist2,'delcar2')
    request.session["booklist"] = booklist
    request.session['booklist2']=booklist2
    return redirect("car")

def delcar2(request):
    bookid = request.GET.get("bookid")
    booklist = request.session.get("booklist")
    booklist2 = request.session.get("booklist2")
    for i in booklist2:
        if bookid == i["id"]:
            booklist2.remove(i)
            booklist.append(i)
    request.session["booklist"] = booklist
    request.session['booklist2']=booklist2
    return redirect("car")

def alldelcar(request):
    booklist=[]
    request.session["booklist"] = booklist
    return redirect('car')

def updatecar(request):
    bookid=request.GET.get('bookid')
    count=request.GET.get('count')
    booklist = request.session.get("booklist")
    for i in booklist:
        if bookid == i["id"]:
            print(bookid,count,i['count'],type(booklist))
            print(booklist)
            i["count"] = int(count)
    request.session["booklist"] = booklist
    return redirect("car")

def cartoindent(request):
    dz = request.get_full_path()
    zj = request.get_host()
    fdz = ('http://' + zj + dz)
    request.session['fdz'] = fdz
    iflo = request.session.get('login')
    if iflo == 'ok':
        return redirect('indent')
    else:
        return redirect('login')

def indent(request):
    status = request.session.get('login')
    if status == 'ok':
        un = request.session.get('uname')
        una = un
    else:
        una = 0
    address = TAdds.objects.all()
    if una !=0:
        unal = TUser.objects.filter(username=una)[0]
        uni = unal.user_id
        address = TAdds.objects.filter(user_id=uni)
    print(address)
    booklist = request.session.get("booklist")
    booklist2 = []
    request.session['booklist2']=booklist2
    total_price=0
    print(booklist)
    if booklist:
        for i in booklist:
            total_price += i["dangdang_price"] * i["count"]
            total_price = round(total_price, 2)
    return render(request,'indent.html',{'una':una,'booklist':booklist,'total_price':total_price,'address':address})

def indent_ok(request):
    booklist = request.session.get("booklist")
    oid = request.session.get('orderid')
    address = TAdds.objects.all()
    status = request.session.get('login')
    if status == 'ok':
        un = request.session.get('uname')
        una = un
    else:
        una = 0
    count=0
    total_price=0
    if booklist:
        for i in booklist:
            total_price += i["dangdang_price"] * i["count"]
            total_price = round(total_price, 2)
            count = count + i['count']
    request.session['booklist']=[]
    return render(request,'indent ok.html',{'una':una,'booklist':booklist,'total_price':total_price,'address':address,'count':count,'oid':oid})

def indentchance(request):
    booklist = request.session.get("booklist")
    name = request.POST.get('tt1')
    address = request.POST.get('tt3')
    zcode = request.POST.get('tt4')
    mphone = request.POST.get('tt5')
    tphone = request.POST.get('tt6')
    un = request.session.get('uname')
    unal =TUser.objects.filter(username=un)[0]
    uni=unal.user_id
    ab = TAdds.objects.filter(a_address=address,user_id=uni)
    if ab:
        ab = TAdds.objects.filter(a_address=address, user_id=uni)[0]
        addid = ab.id
    else:
        TAdds.objects.create(a_name=name,a_address=address,post_id=zcode,telephone=tphone,mobile_phone=mphone,user_id=uni)
        ab = TAdds.objects.filter(a_address=address,user_id=uni)[0]
        addid = ab.id
    count1=0
    for i in booklist:
        count1 = count1 + i['count']
    time1=time.time()
    TOrder.objects.create(number=count1,time=time1,address_id=addid,user_id=uni)
    oi = TOrder.objects.filter(time=time1)[0]
    oid = oi.id
    request.session['orderid']=oid
    for i in booklist:
        book_id = i['id']
        count=i['count']
        TOrderInfo.objects.create(number=count,order_id=oid,book_id=book_id)
    return redirect('indent_ok')

def sendemail(request):
    x=request.session.get('phorem')
    username=request.GET.get('username')
    if x:
        if x=='phone':
            Epanding.objects.create(username=username,code=123)
        elif x=='email':
            a = random.randint(1, 99)
            h = hashlib.md5()
            a = username + str(a)
            print(a)
            h.update(a.encode())
            code = h.hexdigest()
            Epanding.objects.create(username=username,code=code)
            sendemail1(username,code)
def sendemail1(username,code):
    subject='注册验证码'
    from_email='songfu01@sina.com'
    to=username
    text_content = '你的验证码是:'+ code
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
def deloldcode(request):
    username=request.GET.get('username')
    a=Epanding.objects.filter(username=username).delete()
    if a:
        print('yes',492)
def codecheck(request):
    code=request.GET.get('code')
    username=request.GET.get('username')
    a=Epanding.objects.filter(username=username,code=code)
    if a:
        return HttpResponse(0)
    else:
        return HttpResponse(1)