from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from core.models import AboutPage, TeamMember
from django.apps import apps
from cars.models import Car, Category
from core.models import SiteConfig, Banner
from .forms import ContatoForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(is_active=True).order_by('order')[:3]
        context['featured_cars'] = Car.objects.filter(available=True)[:6]
        context['categories'] = Category.objects.all()
        context['site_config'] = SiteConfig.objects.first()
        context['contato_form'] = ContatoForm()  # Adiciona o formulário ao contexto
        return context

    def post(self, request, *args, **kwargs):
        contato_form = ContatoForm(request.POST)
        if contato_form.is_valid():
            contato_form.save()
            messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
            return redirect('home')
        
        # Se o formulário for inválido, recarrega a página com os erros
        context = self.get_context_data()
        context['contato_form'] = contato_form
        return self.render_to_response(context)


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_page = AboutPage.objects.filter(ativo=True).first()
        
        if about_page:
            context['sobre'] = about_page
            context['membros_equipe'] = about_page.membros.all().order_by('ordem')
            context['title'] = about_page.titulo
        else:
            context['sobre'] = None
            
        return context


@login_required
def profile_view(request):
    return render(request, 'core/profile.html')


@staff_member_required
def custom_admin_view(request):
    context = {
        'has_userprofile': apps.is_installed('core') and hasattr(apps.get_app_config('core'), 'userprofile'),
        'has_siteconfig': apps.is_installed('core') and hasattr(apps.get_app_config('core'), 'siteconfig'),
    }
    return render(request, 'core/custom_admin.html', context)


class ContatoView(FormView):
    template_name = 'core/contato.html'
    form_class = ContatoForm
    success_url = reverse_lazy('contato')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        return super().form_valid(form)