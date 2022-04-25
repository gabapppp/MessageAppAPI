from rest_framework import viewsets, mixins, permissions, status, decorators, response, permissions, filters
from django.db.models import aggregates
from rest_framework.generics import CreateAPIView
from django.contrib import auth
from .models import * 
from .serializers import * 
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

# Create your views here.   
class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(CreateAPIView):
    queryset = auth.get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ProfileViewSet(viewsets.ModelViewSet, mixins.RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields= ['user__username']
    lookup_field = 'user__username'
    
    @decorators.action(detail=False, methods=('get',))
    def me(self, request):
        queryset=Profile.objects.all().get(user=self.request.user)
        serializer = self.get_serializer(instance=queryset)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = auth.get_user_model()
        permission_classes = (permissions.IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)