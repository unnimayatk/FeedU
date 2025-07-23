from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserAddForm, FoodMenuItemForm
from .decorators import admin_only
from .models import FoodMenuItem, Order, OrderItem, DeliveryAddress

@admin_only
def Index(request):
    menu = FoodMenuItem.objects.all()

    print(menu,"--------------")
    return render(request,"index.html",{"menuitem":menu})

def FoodMenu(request):
    menu = FoodMenuItem.objects.all()

    return render(request,"foodmenu.html",{"menuitem":menu})

@login_required(login_url="SignIn")
def MerchantIndex(request):
    return render(request,"staff/staffindex.html")

# Create your views here.
def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or Password Incorrect")
            return redirect('SignIn')
    return render(request,"login.html")


def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
           

            
                
            messages.info(request,"User Created.. ")
            return redirect('SignIn')
        
    return render(request,"register.html",{"form":form})




def SignOut(request):
    logout(request)
    return redirect('SignIn')

# Merchant functions 

def Menu(request):
    fooditem = FoodMenuItem.objects.all()
    if request.method == 'POST':
        form = FoodMenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('Menu')  # Redirect to a list view
    else:
        form = FoodMenuItemForm()
    return render(request,"staff/menu.html",{"form":form, "fooditem":fooditem})


def update_menu_item(request, pk):
    item = get_object_or_404(FoodMenuItem, pk=pk)
    if request.method == 'POST':
        form = FoodMenuItemForm(request.POST, request.FILES, instance=item)
        offer = request.POST.get("offer")
        if form.is_valid():
            menu = form.save()
            menu.offer = offer
            menu.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('Menu')
    else:
        form = FoodMenuItemForm(instance=item)
    return render(request, 'staff/update_menu_item.html', {'form': form})

def Change_offer_status(request,pk):
    item = get_object_or_404(FoodMenuItem,id= pk)
    if item.offer == True:
        item.offer = False
    else:
        item.offer = True
    item.save()
    messages.info(request,"offer status changed...")
    return redirect("update_menu_item", pk = item.id )


def delete_menu_item(request, pk):
    item = get_object_or_404(FoodMenuItem, pk=pk)
    item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('Menu')




#customer bookin
@login_required(login_url="SignIn")
def my_booking(request):
    menu = FoodMenuItem.objects.all()
    
    # Get the first pending order or None if no pending order exists
    order = Order.objects.filter(order_status="pending",user=request.user).first()
    
    # Get all items in the order if an order exists, otherwise set to an empty list
    order_items = order.order_items.all() if order else []
    if request.method == "POST":
        order = get_object_or_404(Order, id=order.id, order_status="pending")
        
        # Get form data
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("class") 
        delivery_time = request.POST.get("delivery_time") # Address (Class Room in form)

        # Create DeliveryAddress entry
        delivery_address = DeliveryAddress.objects.create(
            order=order,
            name=name,
            phone=phone,
            address=address,
            order_status="Order Received",
            user = request.user,
            delivery_time = delivery_time
        )
        delivery_address.save()

        # Update order status
        order.order_status = "Order Received"
        order.save()

        # Notify user of successful order placement
        messages.success(request, "Your order has been placed successfully!")

        # Redirect to a confirmation page or order summary
        return redirect("payment_screen", pk=delivery_address.id)
    
    context = {
        'order': order,
        'order_items': order_items,
        "menu": menu,
    }
    return render(request, 'booking.html', context)


# views.py
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment_screen(request, pk):
    # Get delivery address
    delivery = get_object_or_404(DeliveryAddress, id=pk)
    
    # Calculate the amount (in paisa for Razorpay)
    amount = int(delivery.order.total_amount * 100)  # assuming `total_amount` is in INR

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(
        {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",  # Auto-capture after successful payment
        }
    )
    order_id = razorpay_order["id"]
    
    # Pass data to the template
    context = {
        "delivery": delivery,
        "amount": amount,
        "razorpay_order_id": order_id,
        "razorpay_key_id": settings.RAZOR_KEY_ID,
        "callback_url": request.build_absolute_uri('/payment/success/'),
    }
    return render(request, "payment_screen.html", context)

# views.py
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        # Get payment details from Razorpay
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            # Signature verification
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Update the order's payment status
            delivery = DeliveryAddress.objects.all().last()
            delivery.order.payment_status = "Completed"
            delivery.order.save()
            
            messages.success(request, "Payment was successful!")
            return redirect("order_summary_all")  # Redirect to an order summary page
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed.")
            return redirect("payment_failed")
        
def payment_failed(request):
    return redirect("Index")








@login_required(login_url="SignIn")
def add_item_to_order(request, product_id):
    product = get_object_or_404(FoodMenuItem, id=product_id)
    
    # Get or create a pending order
    order = Order.get_or_create_pending_order(request = request)
    
    # Add the product to the order
    OrderItem.add_or_update_item(order, product_id, quantity=1)
    
    # Redirect or return response as needed
    return redirect('my_booking')  # replace with your actual menu page URL name
    
def increase_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.quantity += 1
    item.total_price = item.quantity * item.product.rate
    item.save()

    # Update the order total amount
    order = item.order
    order.total_amount = sum(i.total_price for i in order.order_items.all())
    order.save()

    return redirect('my_booking')  # Redirect back to the order view

@login_required(login_url="SignIn")
def decrease_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.total_price = item.quantity * item.product.rate
        item.save()
    else:
        item.delete()  # Optionally delete item if quantity reaches zero

    # Update the order total amount
    order = item.order
    order.total_amount = sum(i.total_price for i in order.order_items.all())
    order.save()

    return redirect('my_booking')

@login_required(login_url="SignIn")
def delete_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    order = item.order
    item.delete()

    # Update the order total amount after item deletion
    order.total_amount = sum(i.total_price for i in order.order_items.all())
    order.save()

    return redirect('my_booking')


def place_order(request, order_id):
    
    
    return redirect("my_booking")
    

@login_required(login_url="SignIn")
def order_summary(request, order_id):
    
    delivery_address = DeliveryAddress.objects.get(id=order_id)
    order = delivery_address.order
    order_items = order.order_items.all()
    print(order_items,"kjsdfsgdgdfgkdfgdfkdjhkdfsdjdflkgff---------------------------------")
    context = {
        "order":order,
        "order_items":order_items,
        'delivery_address': delivery_address,
    }
    return render(request, 'order_summary.html', context)

@login_required(login_url="SignIn")
def order_summary_all(request):
    delivery_address_pending = DeliveryAddress.objects.filter(delivery_status = False, user=request.user)
    delivery_address_completed = DeliveryAddress.objects.filter(delivery_status = True,user=request.user)
    context = {
       "delivery_address_pending":delivery_address_pending,
       "delivery_address_completed":delivery_address_completed 
    }
    return render(request,"order_summary_all.html",context)

@login_required(login_url="SignIn")
def add_rating(request,pk):
    delivery = get_object_or_404(DeliveryAddress,id = pk)
    if request.method == "POST":
        rate = request.POST.get('rate')
        delivery.rating = rate
        delivery.save()
        messages.success(request,"Rating Added")

        return redirect("order_summary",order_id =pk )
    return redirect("order_summary",order_id =pk )

from datetime import timedelta
from django.utils import timezone

@login_required(login_url="SignIn")
def cancel_order(request,pk):
  
    # Get the delivery address instance with the provided ID
    delivery = get_object_or_404(DeliveryAddress, id=pk)

    # Calculate the time difference from the order time
    time_difference = timezone.now() - delivery.ordered_time

    # Check if the difference is within 15 minutes
    if time_difference <= timedelta(minutes=15):
        # Set the order status and delete if within 15 minutes
        delivery.order_status = "Cancelled"
        delivery.delivery_status = True
        delivery.save()
        delivery.order.order_status = "Cancelled"
        delivery.order.save()
        messages.success(request, "Order has been successfully cancelled.")
    else:
        # Display a message if the cancellation window has expired
        messages.error(request, "Cancellation period has expired. Orders can only be cancelled within 15 minutes.")

    # Redirect to the previous page or a specific page
    return redirect('order_summary_all')  # Or another appropriate page
    



#staff Orders

@login_required(login_url="SignIn")
def pending_orders(request):
    delivery = DeliveryAddress.objects.filter(delivery_status = False)

    context = {
        "delivery":delivery
    }
    return render(request,'staff/pending_orders.html',context) 

@login_required(login_url="SignIn")
def completed_orders(request):
    delivery = DeliveryAddress.objects.filter(delivery_status = True)

    context = {
        "delivery":delivery
    }
    return render(request,'staff/completed_orders.html',context) 

@login_required(login_url="SignIn")
def estimatedtimeadd(request, pk):
    if request.method == "POST":
        delivery = get_object_or_404(DeliveryAddress, id = pk)
        delivery.estimated_time = request.POST.get("time")
        delivery.save()
        return redirect("pending_orders")
    
@login_required(login_url="SignIn")
def order_status_change(request, pk, status):
    delivery = get_object_or_404(DeliveryAddress,id = pk)
    delivery.order_status = status
    delivery.save()

    if delivery.order_status == "Delivered":
        delivery.delivery_status = True
        delivery.order.order_status = "Delivered"
        delivery.order.save()
        delivery.save()
        
    return redirect("pending_orders")


