from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import User, Trip
from . forms import UserForm, TripForm


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'trip:login'
    redirect_field_name = ''

    template_name = 'trip/index.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return Trip.objects.all()


class UserTripsView(LoginRequiredMixin, generic.ListView):
    login_url = 'trip:login'
    redirect_field_name = ''

    template_name = 'trip/user_trips.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return self.request.user.profile.trips.all()


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'trip:login'
    redirect_field_name = ''
    model = Trip
    template_name = 'trip/detail.html'


class TripCreate(LoginRequiredMixin, CreateView):
    login_url = 'trip:login'
    redirect_field_name = ''
    model = Trip
    form_class = TripForm
    template_name = 'trip/trip_form.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.host= request.user.profile
            trip.destination = form.cleaned_data['destination']
            trip.save()
            return render(request, 'trip/user_trips.html')
        return render(request, 'trip/user_trips.html', {'form': form})


class TripUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'trip:login'
    redirect_field_name = ''

    model = Trip
    fields = ['destination']


class TripDelete(LoginRequiredMixin, DeleteView):
    login_url = 'trip:login'
    redirect_field_name = ''

    model = Trip
    success_url = reverse_lazy('trip:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'trip/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('trip:index')

        return render(request, self.template_name, {'form': form})


class UserLogIn(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('trip:index')
            else:
                return render(request, 'trip/login.html', {'error_message': 'Your Account is suspended.'})

        else:
            return render(request, 'trip/login.html', {'error_message': 'Invalid Log in.'})

    def get(self, request):
        return render(request, 'trip/login.html')


class UserLogOut(View):
    def get(self, request):
        logout(request)
        return redirect('trip:index')


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.save()


def attend_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    try:
        if request.user.profile.trips.filter(id=trip_id):
            request.user.profile.trips.remove(trip)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            request.user.profile.trips.add(trip)
            request.user.profile.save()
    except (KeyError, Trip.DoesNotExist):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))