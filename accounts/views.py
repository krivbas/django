from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from accounts.models import User
from accounts.forms import LoginForm

from accounts.serializers import UserSerializer, UserCreationSerializer, UserChangePasswordSerializer


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('all_articles'))
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(email=data.get("email"), password=data.get("password"))
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse("all_articles"))
                else:
                    print("sorry")
        return render(request, 'sign-in.html', {'form': form})


def sign_out(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect(reverse("sign_in"))
    else:
        return HttpResponseRedirect(reverse("all_articles"))


def get_user_django(request):
    user = User.objects.get(pk=2)
    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username
    }
    return JsonResponse(user_info)


@api_view(['GET', 'POST'])
def get_user_rest(request):
    if request.method == 'GET':
        # serializer for return formatted data
        user = User.objects.get(pk=2)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'POST':
        # serializer for validation request
        serializer = UserCreationSerializer(data=request.POST)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print(validated_data)
            return Response({'success': True})
        else:
            return Response(serializer.errors)


@api_view(['POST'])
def change_user_password(request):
    user = User.objects.get(pk=2)
    serializer = UserChangePasswordSerializer(data=request.POST, context={'user': user})
    if serializer.is_valid():
        validated_data = serializer.validated_data
        user.set_password(validated_data.get('new_password'))
        user.save()
        return Response({'success': True})
    else:
        return Response(serializer.errors)


class ChangeUserPasswordView(APIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            validated_data = serializer.validated_data
            request.user.set_password(validated_data.get('new_password'))
            request.user.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)