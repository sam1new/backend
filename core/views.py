from django.contrib.auth.hashers import make_password
from userprofile.models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserView(APIView):
    def post(self,request,format=None):
        req = request.data
        req['password'] = make_password(req['password'])
        serializer = UserSerializer(data=req)

        if serializer.is_valid():
            serializer.save()
            return Response({'ok': True, 'data': serializer.data},status=200)

        return Response({'ok':False,'data': serializer.errors}, status=400)
    
    # def get(self,request):
    #     output = [{"rooms": output.rooms}
    #               for output in Rooms.objects.all()]
        
    #     return Response(output)
    # def post(self, request):
    #     serializer = RoomsSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #     return Response(serializer.data)