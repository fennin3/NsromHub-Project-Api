from users.forms import SignUpContForm
from django.contrib.auth import get_user_model, login
from rest_framework.exceptions import ValidationError
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import authenticate



User = get_user_model()



def loginUser(request):
    print("________________________________---")
    if request.method == "POST":
        print("________________________________---")
        print(request.POST)
        print(request.POST.get('email_or_phone'))
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get("password")

        # if "@" and "." in email_or_phone:

        #     user = authenticate(email=email_or_phone, password=password)

        # else:
        #     user = User.objects.get(contact=email_or_phone)
        #     user = authenticate(email=user.email, password=password)

        # if user is None:
        #     raise ValidationError("A user with this email/phone and password is not found.")
        # else:
        #     login(user)
        #     # return redirect("gogo")
        return HttpResponse("You have Logged In Sucessfully")


def home(request):
    form1 = SignUpContForm()

    return render(request, "users/login.html", {'form1':form1})





