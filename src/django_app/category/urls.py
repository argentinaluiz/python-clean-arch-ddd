from django.urls import path
from .api import CategoryResource
from django_app import container

urlpatterns = [
    # path('categories/',
    #      CategoryResource.as_view(
    #          list_use_case=container.use_case_category_list_categories(),
    #          get_use_case=container.use_case_category_get_category(),
    #          create_use_case=container.use_case_category_create_category(),
    #          update_use_case=container.use_case_category_update_category(),
    #          delete_use_case=container.use_case_category_delete_category(),
    #      )
    #      ),
    # path('categories/',CategoryResource.as_view()),
    path('categories/', CategoryResource.as_view(
        list_use_case=container.use_case_category_list_categories,
        get_use_case=container.use_case_category_get_category,
        create_use_case=container.use_case_category_create_category,
        update_use_case=container.use_case_category_update_category,
        delete_use_case=container.use_case_category_delete_category,
    )),
]
