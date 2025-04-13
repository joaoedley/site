from django.contrib import admin
from core.models import AboutPage, TeamMember
from django.utils.html import format_html
from .models import UserProfile, SiteConfig, Banner, Contato

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    fields = ('foto_thumbnail', 'nome', 'cargo', 'ordem', 'bio')
    readonly_fields = ('foto_thumbnail',)

    def foto_thumbnail(self, obj):
        return format_html('<img src="{}" style="max-height: 50px;"/>'.format(obj.foto.url)) if obj.foto else ""
    foto_thumbnail.short_description = 'Foto'

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo', 'banner_thumbnail')
    list_editable = ('ativo',)
    inlines = [TeamMemberInline]
    readonly_fields = ('banner_thumbnail',)
    fieldsets = (
        ('Cabeçalho', {
            'fields': ('titulo', 'subtitulo', 'banner', 'banner_thumbnail')
        }),
        ('História', {
            'fields': ('historia_titulo', 'historia_conteudo')
        }),
        ('Missão', {
            'fields': ('missao_titulo', 'missao_conteudo')
        }),
        ('Mapa e Botão', {
            'fields': ('mapa_embed', 'botao_texto', 'botao_link')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

    def banner_thumbnail(self, obj):
        return format_html('<img src="{}" style="max-height: 100px;"/>'.format(obj.banner.url)) if obj.banner else ""
    banner_thumbnail.short_description = 'Miniatura'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'pagina', 'ordem', 'foto_thumbnail')
    list_editable = ('ordem',)
    list_filter = ('pagina',)
    search_fields = ('nome', 'cargo')
    readonly_fields = ('foto_thumbnail',)

    def foto_thumbnail(self, obj):
        return format_html('<img src="{}" style="max-height: 50px;"/>'.format(obj.foto.url)) if obj.foto else ""
    foto_thumbnail.short_description = 'Foto'

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'mobile_image_preview', 'get_is_active')
    readonly_fields = ('image_preview', 'mobile_image_preview')
    
    def get_is_active(self, obj):
        return obj.is_active
    get_is_active.short_description = 'Ativo'
    get_is_active.boolean = True
    
    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px;"/>'.format(obj.image.url)) if obj.image else ""
    image_preview.short_description = 'Preview Desktop'
    
    def mobile_image_preview(self, obj):
        if obj.mobile_image:
            return format_html('<img src="{}" style="max-height: 100px;"/>'.format(obj.mobile_image.url))
        return "Nenhuma imagem mobile"
    mobile_image_preview.short_description = 'Preview Mobile'

#formulario de contato 

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'assunto', 'data_envio', 'lido')
    list_filter = ('lido', 'data_envio')
    search_fields = ('nome', 'email', 'assunto')
    list_editable = ('lido',)
    date_hierarchy = 'data_envio'