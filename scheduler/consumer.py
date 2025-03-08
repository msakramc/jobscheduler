# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Job
# from .serializers import JobSerializer
# from django.core.paginator import Paginator

# # class JobConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         self.user = self.scope['user']
        
# #         # Accept the WebSocket connection
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         # Handle disconnection if needed
# #         pass

# #     async def receive(self, text_data):
# #         # Parse the message received from the client
# #         data = json.loads(text_data)

# #         # Filter the queryset based on status and paginate
# #         status_filter = data.get('status', 'all')
# #         page_number = data.get('page', 1)  # Default to page 1 if not provided

# #         # Fetch the jobs
# #         queryset = Job.objects.filter(user=self.user)

# #         if status_filter != 'all':
# #             queryset = queryset.filter(status=status_filter)

# #         # Paginate the results
# #         paginator = Paginator(queryset, 10)  # Show 10 jobs per page
# #         page = paginator.get_page(page_number)

# #         # Serialize the jobs
# #         serializer = JobSerializer(page, many=True)

# #         # Prepare the response data
# #         job_status = {
# #             'all': queryset.count(),
# #             'completed': queryset.filter(status="Completed").count(),
# #             'running': queryset.filter(status="Running").count(),
# #             'pending': queryset.filter(status="Pending").count(),
# #             'failed': queryset.filter(status="Failed").count(),
# #         }

# #         response_data = {
# #             'job_status': job_status,
# #             'results': serializer.data,
# #         }

# #         # Send the data back to the WebSocket client
# #         await self.send(text_data=json.dumps(response_data))

# # scheduler/consumers.py

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Join room group
#         self.room_name = 'chat_room'
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join the WebSocket group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
