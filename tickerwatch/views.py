from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from tickerwatch.forms import UserForm, UserProfileForm, StockForm
from tickerwatch.models import Stock, UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
  return render(request, 'tickerwatch/index.html')


def register(request):
  # Like before, get the request's context.
  context = RequestContext(request)

  # A boolean value for telling the template whether the registration was successful.
  # Set to False initially. Code changes value to True when registration succeeds.
  registered = False

  # If it's a HTTP POST, we're interested in processing form data.
  if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    # If the two forms are valid...
    if user_form.is_valid() and profile_form.is_valid():
      # Save the user's form data to the database.
      user = user_form.save()

      # Now we hash the password with the set_password method.
      # Once hashed, we can update the user object.
      user.set_password(user.password)
      user.save()

      # Now sort out the UserProfile instance.
      # Since we need to set the user attribute ourselves, we set commit=False.
      # This delays saving the model until we're ready to avoid integrity problems.
      profile = profile_form.save(commit=False)
      profile.user = user
      profile.phone_number = request.POST['phone_number']

      # Now we save the UserProfile model instance.
      profile.save()

      # Update our variable to tell the template registration was successful.
      registered = True

    # Invalid form or forms - mistakes or something else?
    # Print problems to the terminal.
    # They'll also be shown to the user.
    else:
      print user_form.errors, profile_form.errors

  # Not a HTTP POST, so we render our form using two ModelForm instances.
  # These forms will be blank, ready for user input.
  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  # Render the template depending on the context.
  return render_to_response(
    'tickerwatch/register.html',
    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
    context)


def user_login(request):
  # Like before, obtain the context for the user's request.
  context = RequestContext(request)

  # If the request is a HTTP POST, try to pull out the relevant information.
  if request.method == 'POST':
    # Gather the username and password provided by the user.
    # This information is obtained from the login form.
    username = request.POST['username']
    password = request.POST['password']

    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
      # Is the account active? It could have been disabled.
      if user.is_active:
        # If the account is valid and active, we can log the user in.
        # We'll send the user back to the homepage.
        login(request, user)
        return HttpResponseRedirect('/tickerwatch/')
      else:
        # An inactive account was used - no logging in!
        return HttpResponse("Your TickerWatch account is disabled.")
    else:
      # Bad login details were provided. So we can't log the user in.
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")

  # The request is not a HTTP POST, so display the login form.
  # This scenario would most likely be a HTTP GET.
  else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
    return render_to_response('tickerwatch/login.html', {}, context)


@login_required
def user_logout(request):
  # Since we know the user is logged in, we can now just log them out.
  logout(request)

  # Take the user back to the homepage.
  return HttpResponseRedirect('/tickerwatch/')


@login_required
def add_stock(request):
  # Like before, get the request's context.
  context = RequestContext(request)
  stock_added = False
  already_added = False

  # If it's a HTTP POST, we're interested in processing form data.
  if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    stock_form = StockForm(data=request.POST)

    # If the form is valid...
    ticker = request.POST['ticker']
    if stock_form.is_valid():
      stock = Stock.objects.get(ticker=ticker)
      if not stock:
        stock_form.save()
      stock = Stock.objects.get(ticker=ticker)
      if not Stock.objects.filter(ticker=ticker, users__id=request.user.id):
        stock.users.add(request.user)
        stock_added = True
      else:
        already_added = True

    # Invalid form or forms - mistakes or something else?
    # Print problems to the terminal.
    # They'll also be shown to the user.
    else:
      print stock_form.errors

  # Not a HTTP POST, so we render our form using two ModelForm instances.
  # These forms will be blank, ready for user input.
  else:
    stock_form = StockForm()

  # Render the template depending on the context.
  return render_to_response(
    'tickerwatch/add_stock.html',
    {'stock_form': stock_form, 'stock_added': stock_added, 'already_added': already_added},
    context)


@login_required
def profile(request):
  context = RequestContext(request)
  stocks = Stock.objects.filter(users__id=request.user.id)
  stocks = [stock.ticker for stock in stocks]
  profile = UserProfile.objects.get(user__id=request.user.id)

  return render(request, 'tickerwatch/profile.html',
      {'profile': profile, 'stocks': stocks})

