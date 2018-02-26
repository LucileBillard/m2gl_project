from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from api.serializers import InstanceSerializer, SolverSerializer
from api.models import Instance, Solver, Experimentation
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

# API views

@permission_classes((permissions.AllowAny,))
class InstanceList(APIView):
    """
    List all instances, or create a new instance.
    """

    def get(self, request, format=None):
        instances = Instance.objects.all()
        serializer = InstanceSerializer(instances, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.AllowAny,))
class InstanceDetail(APIView):
    """
    Retrieve, update or delete an instance (problem instance) .
    """

    def get(self, request, pk, format=None):
        instance = get_object_or_404(Instance, pk=pk)
        serializer = InstanceSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = get_object_or_404(Instance, pk=pk)
        serializer = InstanceSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = get_object_or_404(Instance, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((permissions.AllowAny,))
class SolverList(APIView):
    """
    List all solvers, or create a new solver.
    """

    def get(self, request, format=None):
        solvers = Solver.objects.all()
        serializer = SolverSerializer(solvers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SolverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.AllowAny,))
class SolverDetail(APIView):
    """
    Retrieve, update or delete a solver.
    """

    def get(self, request, pk, format=None):
        solver = get_object_or_404(Solver, pk=pk)
        serializer = SolverSerializer(solver)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        solver = get_object_or_404(Solver, pk=pk)
        serializer = SolverSerializer(solver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        solver = get_object_or_404(Solver, pk=pk)
        solver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
