from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Car, Category, Order
from .forms import SearchForm
from django.db import models
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

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
    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa fazer login para acessar seu carrinho")
        return redirect('login')  # Assumindo que você tem uma URL de login
    
    # Obtém todos os pedidos não finalizados do usuário
    orders = Order.objects.filter(user=request.user, completed=False)
    
    if not orders.exists():
        return render(request, 'cars/cart.html', {'empty_cart': True})
    
    # Calcula o total considerando a quantidade de cada item
    total = sum(order.total_price() for order in orders)
    
    context = {
        'orders': orders,  # Todos os itens do carrinho
        'total': total,
        'items_count': orders.aggregate(total_items=Sum('quantity'))['total_items'] or 0
    }
    return render(request, 'cars/cart.html', context)
    



@login_required
def remove_from_cart(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        order = Order.objects.get(id=order_id, user=request.user, completed=False)
        order.delete()
        messages.success(request, "Item removido do carrinho com sucesso")
    except Order.DoesNotExist:
        messages.error(request, "Item não encontrado no seu carrinho")
    
    return redirect('cars:view_cart')

def update_quantity(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            order = Order.objects.get(id=order_id, user=request.user, completed=False)
            
            if quantity > 0:
                order.quantity = quantity
                order.save()
                messages.success(request, "Quantidade atualizada com sucesso")
            else:
                order.delete()
                messages.success(request, "Item removido do carrinho")
                
        except (Order.DoesNotExist, ValueError):
            messages.error(request, "Erro ao atualizar quantidade")
    
    return redirect('cars:view_cart')

def update_quantity(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            order = Order.objects.get(id=order_id, user=request.user, completed=False)
            
            if quantity > 0:
                order.quantity = quantity
                order.save()
                messages.success(request, "Quantidade atualizada com sucesso")
            else:
                order.delete()
                messages.success(request, "Item removido do carrinho")
                
        except (Order.DoesNotExist, ValueError):
            messages.error(request, "Erro ao atualizar quantidade")
    
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

