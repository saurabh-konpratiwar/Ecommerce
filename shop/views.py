from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate,Advertise
from math import ceil
from django.views.decorators.csrf import  csrf_exempt
import json
from . import checksum
from django.contrib.auth import authenticate,login,logout
MERCHANT_KEY = "1G##R9Lyn7TMl32Y"


# Create your views here.
def index(request):
    products = Product.objects.all()
    #n = len(products)
    #nslides = n//4 + ceil((n/4)-(n//4))
    #param = {'product':products,'no_of_slide':nslides,'range':range(1,nslides)}
    #allprods = [[products,range(1,nslides),nslides],
    #           [products,range(1,nslides),nslides]]
    adv = Advertise.objects.all()
    allprods = []
    catprods = Product.objects.values('category','id')

    cats = {item['category'] for item in catprods}

    #print(catprods)
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)

        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod,range(1,nslides),nslides])
    param = {'allprods':allprods,'advertise':adv,'cats':cats}
    return render(request, "shop/index.html",param)


def showcatprod(request,catname):
    prod = Product.objects.filter(category = catname)
    param = {'catsprod':prod}
    return render(request, "shop/index.html",param)



def about(request):
    return render(request,"shop/about.html")


def contact(request):
    name = ''
    if request.method == "POST":
        name = request.POST.get('name','')
        email= request.POST.get('email','')
        phone= request.POST.get('phone','')
        desc= request.POST.get('desc','')

    if name != "":
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        Thank = True
        return render(request,"shop/contact.html",{'Thank':Thank})
        
    return render(request, "shop/contact.html")

def tracker(request):
    if request.method == "POST":
        orderId1 = request.POST.get('orderId','')
        email1 = request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id = orderId1,email = email1)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId1)

                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps(updates,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("error")
        except Exception as e:
            return HttpResponse(e)


    return render(request,"shop/tracker.html")




def imgform(request):
    if request.method == "GET":
        imgid = request.GET.get('imgid','')
        print(imgid)
        return HttpResponse('done')


def productview(request,myid):
    #jis product ki id= myid hai uska product name return karoo

    product = Product.objects.filter(id=myid)
    return render(request,"shop/productview.html",{"product":product[0]})

def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('itemjson','')    
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '')+ " " + request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        amount =  request.POST.get('amount','')
        order = Order(amount = amount,item_JSON=item_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        id = order.order_id
        data_dict = {
            'MID': 'ScLQqw03389967350484',
            'ORDER_ID': str(id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest'
        }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request, "shop/paytm.html",{'param_dict':param_dict})
    else:
        fof = []
        fil = Product.objects.values('product_name','id')
        cats = [item['id'] for item in fil]
        for cat in cats:
            fo = Product.objects.filter(id=cat)
            fof.append(fo)
    
        return render(request, "shop/checkout.html",{'fil':fof})
        



def sear(query,item):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower() or query in item.product_name or query in item.desc or query in item.category or query in item.product_name.upper() or query in item.desc.upper() or query in item.category.upper() or query in item.product_name.capitalize() or query in item.desc.capitalize() or query in item.category.capitalize():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')

    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if sear(query, item)]

        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprods.append([prod, range(1, nslides), nslides])

    param = {'allprods': allprods}
    return render(request, "shop/search.html", param)

@csrf_exempt
def handlerequest(request):
    form = request.POST
    respons_dict = {}

    for i in form.keys():
        respons_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksums = form[i]

    verify = checksum.verify_checksum(respons_dict, MERCHANT_KEY, checksums)
    
    Thank = True
    if verify:
        if respons_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print("order unsuccessful because" + respons_dict['RESPMSG'])
    else:
        print("order unsuccessful because" + respons_dict['RESPMSG'])
    return render(request,"shop/paymentstatus.html",{'respons_dict':respons_dict,'Thank':Thank})
'''

def handlelogin(request):
    if request.method == 'POST':
        loginNm = request.POST.get('loginUser')
        loginPw = request.POST.get('loginPass')
        #user ka name data base me hoga to return user karenga oterwise none karenga
        user = authenticate(username=loginNm, password=loginPw)

        if user is not None:
            login(request,user)
            messages.success(request,"user login")
            return redirect('index')
        else:
            messages.error(request,"Invalid")
            return redirect('index')
    return render(request,'shop/login.html')

def handlelogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,'successfully logout')
        return redirect('/shop')



def handlesignup(request):
    return render(request, 'shop/signup.html')
'''