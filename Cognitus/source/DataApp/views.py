from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from rest_framework import routers, serializers, viewsets, request
from .models import Data
from .serializers import DataSerializer
from rest_framework.response import Response
import json
import requests

class MainPageView(TemplateView):
    template_name = "index.html"

    def post(self, request):
        if request.method == 'POST':
            text = request.POST.get('inputtext')
            URL = "http://0.0.0.0:8080"
            PARAMS = {"user_text":text}

            train= requests.get(url="{}/train".format(URL))


            predict= requests.post(url="{}/predict".format(URL), params=PARAMS)
            predict_json = predict.json()

            print(predict_json)
            result = predict_json['prediction']
            print(result)

        return render(request, self.template_name, {"label":result,"text":text})




class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    def put(self, request, *args, **kwargs):
        super(DataViewSet, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(DataViewSet, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(DataViewSet   , self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully deleted"}
        return Response(response)
