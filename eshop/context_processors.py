from .models import Category, Order_details, Order, Like, Review 
from datetime import date, datetime, timedelta
from django.utils import timezone
import stripe


def getCategories(request):
    categories = Category.objects.filter(active=True).order_by('name')
    total = sum([category.products.count() for category in categories])
    return {'categories': categories, 'total': total}


def stripe_payment (secret_key, token, amount, description ):
    try:
        print(secret_key, token, amount, description, )
        # Use Stripe's library to make requests...
        stripe.api_key = secret_key
        # Token is created using Stripe Checkout or Elements!
        # Get the payment token ID submitted by the form:
        charge = stripe.Charge.create(
            amount= int (amount * 100),
            currency='usd',
            description=description,
            source=token,
        )
        return charge['id']
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print('Status is: %s' % e.http_status)
        print('Code is: %s' % e.code)
        # param is '' in this case
        print('Param is: %s' % e.param)
        print('Message is: %s' % e.user_message)
    except stripe.error.RateLimitError as e:
        print (e)
    except stripe.error.InvalidRequestError as e:
        print (e)

    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print (e)

    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        print (e)

    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print (e)

    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print (e)

    return None


def getDashboardData(request):
    today = date.today()

    orders = Order.objects.filter(created_at__date=today, completed=True)
    day_sells_count = orders.count()
    day_sells_amount = sum([order.total for order in orders])

    week_sells_amount = sum([order.total for order in Order.objects.filter(created_at__date__gte=today-timedelta(days=6), completed=True)])
    week_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    week_sells = [sum([order.total for order in Order.objects.filter(created_at__date=d, completed=True)]) for d in week_days]
    week_days = [f"{d.strftime('%a')} ({d.day})" for d in week_days]

    return {
        'day_sells_count': day_sells_count, 
        'day_sells_amount': day_sells_amount, 
        'week_sells_amount': week_sells_amount,
        'week_sells': week_sells,
        'week_days': week_days,
    }


def getCountOrderByDay(request):
   current_date=datetime.now()
   order=Order.objects.filter(created_at__date = date.today())
   nombre = order.count()
#    order_details=order.order_details()
#    somme = 0
#    for order in order_details:
#        somme += order.quantity * order.product.price
   return  {"nombre":nombre}


def getCountOrderByMonth(request):
   current_date=datetime.now()
   order=Order.objects.filter(created_at__month = date.today().month)
   month = order.count()
   return  {"month":month}


def getCountLike(request):
   like = Like.objects.count()
   return  {"like":like}


def getCountReview(request):
   review = Review.objects.count()
   return  {"review":review}


def getSessionInfo(request):
    cart = request.session.get('cart', {})
    likes = request.session.get('likes', {})
    return {'cart_items_count': sum(cart.values()), 'likes_count': list(likes.values()).count(True)}
