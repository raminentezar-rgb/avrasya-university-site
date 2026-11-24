from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.html import strip_tags

from .models import Etkinlik


class EtkinliklerFeed(Feed):
    title = "Avrasya Üniversitesi Etkinlikleri"
    link = reverse_lazy('etkinlikler:liste')
    description = (
        "Avrasya Üniversitesi bünyesinde düzenlenen güncel konferans, seminer, "
        "panel, atölye ve kültürel etkinlikler."
    )

    def items(self):
        return Etkinlik.objects.filter(yayinda=True).order_by('-baslangic_tarihi')[:25]

    def item_title(self, item):
        return item.baslik

    def item_description(self, item):
        return item.get_ozet or strip_tags(item.detayli_aciklama or '')[:300]

    def item_pubdate(self, item):
        return item.olusturulma_tarihi

    def item_updateddate(self, item):
        return item.guncellenme_tarihi
