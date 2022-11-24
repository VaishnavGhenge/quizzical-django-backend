from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import UserData
from . serializers import UserDataSerializer


@api_view(['GET', 'POST'])
def initview(request):
    try:
        if request.session.get('user', False):
            response = {
                'status': 'ok',
                'userinfo': 'session',
                'user_data': UserData.objects.get(username=request.session.get('user'))
            }
            return Response(response)
        else:
            response = {
                'status': 'ok',
                'userinfo': 'login',
            }
            return Response(response)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e),
        }
        return Response(response)


@api_view(['GET', 'POST'])
def login(request):
    try:
        if request.method == 'POST':
            print(request.data)
            if UserData.objects.filter(username=request.data['username'], password=request.data['password']).exists():
                response = {
                    'status': 'ok',
                    'login_status': 'success',
                }
                return Response(response)
            else:
                serializer = UserDataSerializer(data={
                    'username': request.data['username'],
                    'password': request.data['password'],
                    'highestscore': 0,
                })

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': 'ok',
                        'login_status': 'success',
                    })
                else:
                    return Response({
                        'status': 'ok',
                        'login_status': 'inconsistent_data'
                    })
        else:
            return Response({
                'status': 'ok',
            })
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e),
        }
        return Response(response)


def check_user(user):
    if UserData.objects.filter(username=user).exists():
        return True
    else:
        return False


@api_view(['GET', 'POST'])
def chech_user(request):
    if UserData.objects.filter(username=request.data['user']).exists():
        return Response({
            'status': 'ok',
            'user_info': 'bad'
        })
    else:
        return Response({
            'status': 'ok',
            'user_info': 'good'
        })


@api_view(['GET', 'POST'])
def signup(request):
    try:
        if not check_user(request.data['username']):
            serializer = UserDataSerializer({
                'username': request.data['username'],
                'password': request.data['password'],
                'highestscore': 0,
            })

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'ok',
                    'login_status': 'success',
                })
            else:
                return Response({
                    'status': 'ok',
                    'login_status': 'inconsistent_data'
                })
        else:
            return Response({
                'status': 'ok',
                'login_status': 'user already exists',
            })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e),
        })

@api_view(['GET', 'POST'])
def update_high_score(request):
    try:
        print(request.data, 130)

        if UserData.objects.filter(username=request.data['user']).exists():
            print(132)
            user = UserData.objects.get(username=request.data['user'])
            print(request.data['score'], user.highestscore)
            if request.data['score'] > user.highestscore:
                UserData.objects.filter(username=request.data['user']).update(
                    highestscore=request.data['score'])
                print(request.data['score'], 138)
                return Response({
                    'status': 'ok',
                    'update_info': 'updated',
                    'score': request.data['score'],
                })
            else:
                print(user.highestscore, 144)
                return Response({
                    'status': 'ok',
                    'update_info': 'not updated',
                    'score': user.highestscore,
                })
        else:
            print('else', 151)
            return Response({
                'status': 'ok',
                'update_info': "user don't exist"
            })
    except Exception as e:
        print('ex', 157)
        return Response({
            'status': 'error',
            'message': str(e),
        })
