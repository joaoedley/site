from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField 
from django.utils import timezone


def user_profile_picture_path(instance, filename):
    # Salva a imagem em: media/profile_pictures/user_<id>/<filename>
    return f'profile_pictures/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
        default='profile_pictures/default_profile.png',
        blank=True
    )
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    


class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='site_logo/')
    about_text = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.site_name

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/desktop/')
    mobile_image = models.ImageField(upload_to='banners/mobile/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(default=0)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title


class Category(models.Model):  # Certifique-se que esta classe existe
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True)

    def __str__(self):
        return self.name
    
class AboutPage(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='about_banners/', blank=True, null=True)
    historia_titulo = models.CharField(max_length=100)
    historia_conteudo = RichTextField()
    missao_titulo = models.CharField(max_length=100)
    missao_conteudo = RichTextField()
    mapa_embed = models.TextField(help_text="Código iframe do Google Maps")
    botao_texto = models.CharField(max_length=50)
    botao_link = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Página Sobre"
        verbose_name_plural = "Página Sobre"

    def __str__(self):
        return self.titulo

class TeamMember(models.Model):
    pagina = models.ForeignKey(AboutPage, related_name='membros', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='team_photos/')
    ordem = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['ordem']
        verbose_name = "Membro da Equipe"
        verbose_name_plural = "Membros da Equipe"

    def __str__(self):
        return self.nome
    

#formulario de perguntas

class Contato(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Seu Nome")
    email = models.EmailField(verbose_name="Seu E-mail")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone (opcional)")
    assunto = models.CharField(max_length=100, verbose_name="Assunto")
    mensagem = models.TextField(verbose_name="Sua Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    lido = models.BooleanField(default=False, verbose_name="Mensagem Lida")

    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-data_envio']

    def __str__(self):
        return f"{self.assunto} - {self.nome}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='core_orders')
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('completed', 'Completo'),
        ('cancelled', 'Cancelado'),
    ], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Adicione outros campos necessários para pedidos
    
    class Meta:
        ordering = ['-ordered_date']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"