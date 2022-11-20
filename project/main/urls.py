from django.urls import path
from main.views import signup,admin_dashboard,list_user,list_category,create_category,edit_category,delete_category,list_post,create_post,edit_post,delete_post,custom_login,list_forbiddenword,create_forbiddenword,edit_forbiddenword,delete_forbiddenword,edit_blockuser,edit_adminuser,subscribe_user,unsubscribe_user,list_post_basedCategory,list_postdetails,create_comment,like_post,dislike_post,create_reply,create_tag,search,list_tag
from django.contrib.auth import views as auth_views
urlpatterns = [
   
    path('register', signup,name="signup"),
    path('signin',custom_login, name='login'), 
    path("logout",auth_views.LogoutView.as_view(), name='logout' ),
    path("admindashboard",admin_dashboard, name='admindashboard'),
    path('allcategories',list_category,name="allcategories"),
    path('createcategory',create_category,name="createcategory"),
    path('editcategory/<int:id>', edit_category,name='editcategory'), 
    path("deletecategory/<int:id>",delete_category , name='deletecategory'),
    path('allposts',list_post,name="allposts"),
    path('createpost',create_post,name="createpost"),
    path('editpost/<int:id>', edit_post,name='editpost'), 
    path("deletepost/<int:id>",delete_post, name='deletepost'),
    path('allusers',list_user,name="allusers"),
    path('allforbiddenwords',list_forbiddenword,name="allforbiddenwords"),
    path('createforbiddenword',create_forbiddenword,name="createforbiddenword"),
    path('editforbiddenword/<int:id>', edit_forbiddenword,name='editforbiddenword'),
    path('deleteforbiddenword/<int:id>', delete_forbiddenword,name='deleteforbiddenword'), 
    path('editblockuser/<int:id>', edit_blockuser,name='editblockuser'),
    path('editadminuser/<int:id>', edit_adminuser,name='editadminuser'),
    path('subscribe/<int:id>', subscribe_user,name='subscribeuser'),
    path('unsubscribe/<int:id>', unsubscribe_user,name='unsubscribeuser'),
    path('allpostsbasedcategory/<int:id>', list_post_basedCategory,name='allpostsbasedcategory'),
    path('postdetails/<int:id>', list_postdetails,name='postdetails'),
    path('createcomment/<int:id>',create_comment,name="createcomment"),
    path('likepost/<int:id>',like_post,name="likepost"),
    path('dislikepost/<int:id>',dislike_post,name="dislikepost"),
    path('createreply/<int:pid>/<int:cid>',create_reply,name="createreply"),
    path('createtag',create_tag,name="createtag"),
    path('search',search,name="search"),
    path('alltags',list_tag,name="alltags"),
]