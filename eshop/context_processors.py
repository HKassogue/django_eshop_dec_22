from .models import Category,Order_details,Order, Like, Review 
from datetime import date, datetime


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
    total_ventes = 100000
    total_ventes_week = [1000, 2500, 1800, 4000, 5000, 2000, 1000]
    return {'total_ventes': total_ventes, 'total_ventes_week': total_ventes_week}

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

