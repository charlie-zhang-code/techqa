# qa/views/vote.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from qa.models import Vote
from qa.serializers.vote import VoteSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_votes(self, request):
        votes = self.get_queryset()
        serializer = self.get_serializer(votes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_vote(self, request, pk=None):
        vote = self.get_object()
        new_type = 'up' if vote.vote_type == 'down' else 'down'
        vote.vote_type = new_type
        vote.save()
        return Response({'status': 'vote changed'}, status=status.HTTP_200_OK)