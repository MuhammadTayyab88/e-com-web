from core.models import *


def categories_processor(request):
    main_category = MainCategory.objects.prefetch_related("sub_category").all()
    return {"main_category": main_category}
