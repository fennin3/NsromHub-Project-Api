# from . import models
# from . import serializers
# from djangochannelsrestframework import permissions
# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import (
#     ListModelMixin,
#     PatchModelMixin,
#     UpdateModelMixin,
#     CreateModelMixin,
#     DeleteModelMixin,
# )
# from constituent_operations.models import Message
# from constituent_operations.serializers import RetrieveMessageSerializer
# from rest_framework import  status
# from djangochannelsrestframework.decorators import action


# class LiveMessenger(ListModelMixin, GenericAsyncAPIConsumer):
#     permission_classes = ()
#     queryset = Message.objects.all()
#     serializer_class = RetrieveMessageSerializer
    
#     # @action()
#     # async  def messaging(self, id=None, **kwargs):
#     #     data = await  database_sync_to_async(Message.objects.filter(sender__system_id_for_user=id))

#     #     data = MessageSerializer(data=data, many=True)

#     #     data.is_valid(raise_exception=True)

#     #     return {
#     #         "status":status.HTTP_200_OK,
#     #         "data":data.data
#     #     }