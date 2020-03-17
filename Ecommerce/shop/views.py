from django.shortcuts import render
from django.http import HttpResponse
from . models import Product, Contact, Order, OrderUpdate
from math import ceil
import json, re
from . PayTm import Checksum

from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = '3oZJ!Y9DoNd!fCga'


def index(request):
    order_id = 16  # request.POST.get('orderId', '')
    email = 'Srajani1234@gmail.com'  # request.POST.get('email', '')
    print("hello")

    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == 'POST':
        print("hello")
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        print(order_id, email)
        try:
            print("hello insde ")
            order1 = Order.objects.get(order_id=order_id, email=email)
            item = json.loads(order1.items_json).values()
            items = []
            item = list(item)
            name = []
            print("list odf item", item)
            order2 = Order.objects.filter(order_id=order_id, email=email)
            print(item)
            outer_name = []
            outer_pic = []
            for x in order2:
                itemq = list(json.loads(x.items_json).values())
                print("im inside the required  block",itemq)

                itemsq = []
                nameq=[]
                for z in itemq:
                    print("im inside the required  block  22222")
                    pictures = Product.objects.get(product_name=z[1])
                    print("im inside the required  block  22222")
                    itemsq.append(pictures.image)
                    nameq.append(z[1])
                    print("wrong ",itemsq)
                    print("name wromf", nameq)
                outer_pic.append(itemsq)
                outer_name.append(nameq)

            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                # print("updates", update)

                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp, 'products':outer_pic, 'name':outer_name})
                response = json.dumps(updates, default=str)
                print("im inside the required  updates", updates)

                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')


def about(request):
    return render(request, 'shop/about.html')


def product(request, myid):
    product = Product.objects.filter(product_id=myid)

    return render(request, 'shop/productview.html', {'product': product[0]})


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def checkout(request):

    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('firstname', '')+request.POST.get('lastname', '')
        amount = request.POST.get('amount', '')
        address = request.POST.get('address', '')+request.POST.get('address2', '')
        email = request.POST.get('email', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        if items_json != '{}':
            orders = Order(items_json=items_json, name=name, email=email,  address=address, city=city,
                       state=state, zip=zip_code, phone=phone, amount=amount)
            orders.save()
            update = OrderUpdate(order_id=orders.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = orders.order_id
            param_dict = {

                'MID': 'fwzyPB94313294054410',
                'ORDER_ID': str(orders.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'shop/paytm.html', {'param_dict': param_dict})
        #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def thank(request, order_id):
    final_order = Order.objects.get(order_id=order_id)
    return render(request, 'shop/thank.html', {'order_detail': final_order})


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    thank = False
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            print(type(response_dict))
            print(response_dict)
            thank=True
        else:
            thank=False
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict, 'thank': thank})