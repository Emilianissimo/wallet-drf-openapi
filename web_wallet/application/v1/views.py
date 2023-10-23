from rest_framework.views import APIView
from rest_framework.response import Response


class HealthCheckView(APIView):
    def get(self, request):
        return Response({
            'status': 'alive'
        })
