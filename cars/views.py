from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Car, Category, Order
from .forms import SearchForm
from django.db import models
from django.contrib.auth.decorators import login_required

class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 9


    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_form'] = SearchForm(self.request.GET or None)
        return context

class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_cars'] = Car.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

class SearchResultsView(ListView):
    model = Car
    template_name = 'cars/search_results.html'
    context_object_name = 'cars'

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = Car.objects.all()
            if form.cleaned_data['search_query']:
                query = form.cleaned_data['search_query']
                queryset = queryset.filter(
                    models.Q(make__icontains=query) |
                    models.Q(model__icontains=query) |
                    models.Q(description__icontains=query)
                )
            if form.cleaned_data['min_price']:
                queryset = queryset.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                queryset = queryset.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['category']:
                queryset = queryset.filter(category=form.cleaned_data['category'])
            return queryset
        return Car.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context

@login_required
def add_to_cart(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    order, created = Order.objects.get_or_create(
        user=request.user,
        car=car,
        completed=False
    )
    if not created:
        order.quantity += 1
        order.save()
    messages.success(request, f"{car} adicionado ao carrinho!")
    return redirect('cars:car_detail', pk=car.id)

@login_required
def view_cart(request):
    orders = Order.objects.filter(user=request.user, completed=False)
    total = sum(order.total_price() for order in orders)
    return render(request, 'cars/cart.html', {'orders': orders, 'total': total})

@login_required
def remove_from_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, "Item removido do carrinho!")
    return redirect('cars:view_cart')

@login_required
def checkout(request):
    orders = Order.objects.filter(user=request.user, completed=False)
    if not orders:
        messages.warning(request, "Seu carrinho está vazio!")
        return redirect('cars:view_cart')
    
    for order in orders:
        order.completed = True
        order.save()
    
    messages.success(request, "Compra realizada com sucesso!")
    return redirect('core:profile')