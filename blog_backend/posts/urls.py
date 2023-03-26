
from django.urls import path, include
from .views import PostDetail, PostList, UserPostAPIView, CommentAPIView, PostDetailModerators, UsersViewset, PostListSearch 


urlpatterns = [
    path('user/', UsersViewset.as_view()),
	#path('post/', PostListAPIView.as_view()),
    #path('<int:pk>/', PostDetailAPIView.as_view()),
	path('postList/', PostList.as_view()),
    path('postDetail/<int:pk>/', PostDetail.as_view()),
	path('<int:pk>/', PostDetailModerators.as_view()),
    path('<int:pk>/comment/', CommentAPIView.as_view()),
    path('<name>/', UserPostAPIView.as_view()),
	path('', PostListSearch.as_view())
	#path('^search/(?P<user>.+)/$', PostListSearch.as_view())
	
]
#http://example.com/api/purchases?username=denvercoder9