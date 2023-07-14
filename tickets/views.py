from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Guest, Movie, Reservation, Post
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer, PostSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly

# Create your views here.

# Function based views 
# GET POST
@api_view(['GET', 'POST'])
def FBV_listCreate(request):
    if request.method == 'GET':
        guest = Guest.objects.all()
        serialier = GuestSerializer(guest, many=True)
        return Response(serialier.data)
    elif request.method == 'POST':
        serialier = GuestSerializer(data=request.data)
        if serialier.is_valid():
            serialier.save()
            return Response(serialier.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serialier.data,status= status.HTTP_400_BAD_REQUEST)
# GET PUT DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_PK(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = GuestSerializer(guest, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class based views
# GET POST
class CBV_ListCreate(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET PUT DELETE
class CBV_PK(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Mixins Views
# GET POST
class Mixins_ListPost(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

# GET PUT DELETE
class Mixins_RetrieveUpdateDestroy(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)
    
# generics
# GET POST
class generics_ListPost(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

# GET PUT DELETE
class generics_RetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]

class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Viewsets
# Guest
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# Movie
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

@api_view(['GET'])
def movie_search(request):
    try:
        movie = Movie.objects.filter(movie=request.data['movie'])
    except Movie.DoesNotExist:
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)
    serialzier = MovieSerializer(movie, many=True)
    return Response(serialzier.data)

@api_view(['POST'])
def new_reservation(request):
    try:
        movie = Movie.objects.get(movie=request.data['movie'],
                                     hall=request.data['hall'],
                                     date= request.data['date']
                                     )
    except Movie.DoesNotExist:
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)
    try:
        guest = Guest.objects.get(name=request.data['name'],
                                    mobile=request.data['mobile'],
                                    
                                     )
    except guest.DoesNotExist:
        guest = Guest()
        guest.name = request.data['name']
        guest.mobile = request.data['mobile']
        guest.save()
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data)


    
