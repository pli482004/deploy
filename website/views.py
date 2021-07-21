from django.shortcuts import render
from website.models import *
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
import tensorflow as tf
import json
from PIL import Image
from io import BytesIO
from keras.preprocessing.image import img_to_array
import numpy as np
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "website/index.html")


def about(request):
    return render(request, "website/about.html")


def select(request):
    return render(request, "website/select.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "website/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def draw(request):
    if request.method == "POST":
        ImageData = json.loads(request.body.decode())['data']
        import re
        import base64

        dataUrlPattern = re.compile("data:image/(png|jpeg);base64,(.*)$")
        ImageData = dataUrlPattern.match(ImageData).group(2)

        # If none or len 0, means illegal image data
        if ImageData is None or len(ImageData) == 0:
            print("failed image")
            pass

        im = Image.open(BytesIO(base64.b64decode(ImageData))).convert('LA')

        im = im.resize((28, 28), Image.ANTIALIAS)
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3])
        test_image = np.array([img_to_array(background)])

        model = tf.keras.models.load_model(static('website/model.h5'))

        x = np.argmax(model.predict(test_image), axis=-1)

        return JsonResponse({"hello": x}, status=200)
    else:
        return render(request, "website/draw.html", {
            'message': "Draw a number from 0 to 9"
        })


def bookmark(request):
    return render(request, "website/bookmark.html")
