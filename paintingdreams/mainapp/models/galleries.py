from django.db import models


class Gallery(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order',]
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return self.name

    def children(self, galleries=None, parent=None, level=1):
        if not galleries:
            galleries = list(Gallery.objects.all().order_by('parent_id', 'order'))
            if len(galleries) == 0:
                return []
        if not parent:
            parent = self

        children = []
        for gallery in galleries:
            if gallery.parent_id == parent.id:
                gallery_children = self.children(galleries, gallery, level + 1)
                branch_ids = [gallery.id]
                for child in gallery_children:
                    branch_ids += child['branch_ids']
                children += [{'gallery': gallery, 'children': gallery_children, 'branch_ids': branch_ids}]

        return children


class ImageGallery(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['gallery', 'order',]
        verbose_name_plural = 'Image galleries'