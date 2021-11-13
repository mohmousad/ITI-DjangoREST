from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pinterest.models import Movie
from .serializers import MovieSerializer


@api_view(['GET'])  # type of request
def hello(request, mykey):
    data = {'message': 'Hello test api, your key is: {}'.format(mykey)}
    if mykey == 'yes':
        return Response(data=data, status=status.HTTP_200_OK)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(instance=movies, many=True)
    return Response(data=serialized_movies.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def movie_create(request):
    serialized_movie = MovieSerializer(data=request.data)
    if serialized_movie.is_valid():
        serialized_movie.save()
    else:
        return Response(data=serialized_movie.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response(data=serialized_movie.data, status=status.HTTP_201_CREATED)

    # ==== Manipulation Response ====#
    data = {
        'message': 'created successfully',
        'data': {'id': serialized_movie.data.get('id')}
    }
    return Response(data=data, status=status.HTTP_201_CREATED)


# ==== movie_detail using get ====#
# @api_view(['GET'])
# def movie_detail(request,pk):
#     try:
#         movie_obj = Movie.objects.get(pk=pk)
#     except Exception as e:
#         return Response(data={'message': 'No movie with id {}'.format(pk)}, status=status.HTTP_400_BAD_REQUEST)
#     serialized_movie = MovieSerializer(instance=movie_obj)
#     return Response(data=serialized_movie.data, status=status.HTTP_200_OK)

# ==== movie_detail using filter ====#
@api_view(['GET'])
def movie_detail(request, pk):
    movie_obj = Movie.objects.filter(pk=pk)
    if movie_obj.exists():
        print(movie_obj)
        movie_obj = movie_obj.first()
        print(movie_obj)
    else:
        return Response(data={'message': 'there is no movie with id {}'.format(pk)}, status=status.HTTP_400_BAD_REQUEST)
    serialized_movie = MovieSerializer(instance=movie_obj)
    return Response(data=serialized_movie.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def movie_delete(request, pk):
    response = {}
    try:
        movie_obj = Movie.objects.get(pk=pk)
        movie_obj.delete()
        response['data'] = {'message': 'Deleted Successfully'}
        response['status'] = status.HTTP_200_OK
    except Exception as e:
        response['data'] = {'message': 'No movie with this id {}'.format(str(e))}
        response['status'] = status.HTTP_400_BAD_REQUEST

    print(response)
    return Response(**response)


@api_view(['PUT', 'PATCH'])
def movie_update(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serialized_movie = MovieSerializer(instance=movie, data=request.data)
    elif request.method == 'PATCH':
        serialized_movie = MovieSerializer(instance=movie, data=request.data, partial=True)

    if serialized_movie.is_valid():
        serialized_movie.save()
        return Response(data=serialized_movie.data, status=status.HTTP_200_OK)

    return Response(data=serialized_movie.errors, status=status.HTTP_400_BAD_REQUEST)