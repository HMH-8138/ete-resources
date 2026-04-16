from django.urls import path
from views import (
    health, register, login, materials,
    upload_resource, user_uploads, admin_all_resources,
    review_resource, delete_resource
)

urlpatterns = [
    path('api/health', health, name='health'),
    path('api/register', register, name='register'),
    path('api/login', login, name='login'),
    path('api/materials/<str:resource_type>/<str:level>/<str:term>', materials, name='materials'),
    path('api/upload', upload_resource, name='upload'),
    path('api/user/my-uploads/<str:user_id>', user_uploads, name='user_uploads'),
    path('api/admin/all-resources', admin_all_resources, name='admin_all_resources'),
    path('api/admin/review-resource', review_resource, name='review_resource'),
    path('api/admin/delete-resource/<int:resource_id>', delete_resource, name='delete_resource'),
]
