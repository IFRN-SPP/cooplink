from django.urls import path
from app.views.user import (
    UserList,
    UserCreate,
    UserUpdate,
    UserDelete,
    UserUpdatePassword,
    UserUpdatePermission,
    UserUpdateActive,
)

# Adicione suas URLs aqui
urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("<int:pk>/mudar-senha/", UserUpdatePassword.as_view(), name="update-user-password"),
    path("<int:pk>/mudar-permissao/", UserUpdatePermission.as_view(), name="update-user-permission"),
    path("<int:pk>/mudar-atividade/", UserUpdateActive.as_view(), name="update-user-active"),
    path("cadastrar/", UserCreate.as_view(), name="create-user"),
    # AJAX
    path("js/update/<int:pk>/", UserUpdate.as_view(), name="js-update-user"),
    path("js/delete/<int:pk>/", UserDelete.as_view(), name="js-delete-user"),
]