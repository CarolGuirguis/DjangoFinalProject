from main.models import Categories
def sections_processor(request):
    categories = Categories.get_all_objects()
    return {'categories':categories }