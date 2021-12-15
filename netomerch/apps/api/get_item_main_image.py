def to_representation(self, instance, serializer_obj):
    """
    достаём главную картинку для товара,
    добавляем её в любой сериализатор как поле с ключом image
    добавляем картинке полный путь url https://сервер/media/итп
    """
    request = self.context.get('request')
    item = super(serializer_obj, self).to_representation(instance)  # здесь показывает ошибку, но всё норм
    images = item.pop('onitem')  # вот здесь onitem - это related_name из таблицы ItemImageSolor
    if images:
        for image in images:
            if image['is_main_color']:
                full_url = request.build_absolute_uri(image["image"])
                item['image'] = full_url
                break
    else:
        item['image'] = None
    return item
