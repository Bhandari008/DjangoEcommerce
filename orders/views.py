from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from .models import OrderItem
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
import weasyprint
from orders.models import Order
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()   
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],
                price=item['price'],
                quantity=item['quantity'])
        request.session['order_id'] = order.id
        # clear the cart
        cart.clear()
        return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})
    
@staff_member_required
def admin_order_pdf(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order':order})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Dispostion'] = f'filename=order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS('static/pdf.css')])
    return response

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})