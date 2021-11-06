from general.serializers import *
from rest_framework import status
from rest_framework.response import Response
from constituent_operations.models import Message, IncidentReport, RequestForm
from constituent_operations.serializers import SendMessageSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from users.models import Country, Region, Constituency, Town, Area
from rest_framework import  status
from django.db.models import  Q
from .models import ForumMessage
from .serializers import ForumMessageSerializer



User = get_user_model()



class ListCountriesView(ListAPIView):
    permission_classes=()
    serializer_class=CountryCustomisedForEmma
    queryset=Country.objects.all()

    def list(self, request):
        countries = Country.objects.all()

        data = CountryCustomisedForEmma(countries, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "countries":data.data}, status=status.HTTP_200_OK
        )


class ListRegionView(ListAPIView):
    permission_classes=()
    serializer_class=RegionCustomisedForEmma
    queryset=Region.objects.all()

    def list(self, request, id):
        regions = Region.objects.filter(country_id=id)

        data = RegionCustomisedForEmma(regions, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "regions":data.data}, status=status.HTTP_200_OK
        )


class ListConstituencyView(ListAPIView):
    permission_classes=()
    serializer_class=ConstituencyCustomisedForEmma
    queryset=Constituency.objects.all()

    def list(self, request, id):
        const = Constituency.objects.filter(country_id=id)

        data = ConstituencyCustomisedForEmma(const, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "constituencies":data.data}, status=status.HTTP_200_OK
        )


class ListTownView(ListAPIView):
    permission_classes=()
    serializer_class=TownCustomisedForEmma
    queryset=Town.objects.all()

    def list(self, request, id):
        towns = Town.objects.filter(country_id=id)

        data = TownCustomisedForEmma(towns, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "constituencies":data.data}, status=status.HTTP_200_OK
        )


class ListAreaView(ListAPIView):
    permission_classes=()
    serializer_class=AreaCustomisedForEmma
    queryset=Area.objects.all()

    def list(self, request,id):
        areas = Area.objects.filter(country_id=id)

        data = AreaCustomisedForEmma(areas, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "constituencies":data.data}, status=status.HTTP_200_OK
        )


class SendMessageMPView(APIView):
    permission_classes = ()
    def post(self, request):
        data = SendMessageSerializer(data= request.data)

        data.is_valid(raise_exception=True)

        sender = data['sender'].value
        receiver = data['receiver'].value
        message = data['message'].value
        attached_file = data['attached_file'].value
        try:
            sender = User.objects.get(system_id_for_user=sender)
            receiver = User.objects.get(id=receiver)

            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                message=message,
                attached_file=attached_file
            )
            response = {
                "message": "Message has been sent"
                }
        except Exception as e:
            print(e)
            response = {
                "message":"sorry, something went wrong, try again."
            } 

        return Response(response, status=status.HTTP_200_OK)     


class EditProfileView(APIView):
    permission_classes =()
    def post(self, request, id):
        user = User.objects.get(system_id_for_user=id)
        data =ProfileEditConstituentSerializer(data=request.data)

        data.is_valid(raise_exception=True)


        try:

            user.profile_picture = request.data['profile_picture']

            user.save()

            print(request.data['profile_picture'])

            data = {
                "status":status.HTTP_200_OK,
                "message":"Profile has been updated.",
                # "pic":user.profile_picture
            }
            return Response(data, status=status.HTTP_200_OK)

            
        except Exception as e:
            print(e)
            data = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Profile was not updated.",
                # "pic":user.profile_picture
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



class UnreadsView(APIView):
    permission_classes=()

    def get(self, request, id):
        user = User.objects.get(system_id_for_user=id)
        const = user.active_constituency
        mp = User.objects.filter(active_constituency=const,is_mp=True).first()
                


        

        if user.is_mp or (user.is_subadmin and user.active_constituency == user.subadmin_for):
            incidents = IncidentReport.objects.filter(sender__active_constituency=user.active_constituency, receiver__active_constituency=user.active_constituency, read=False).count()
            requests_ = RequestForm.objects.filter(sender__active_constituency=user.active_constituency, receiver__active_constituency=user.active_constituency, read=False).count()
            messages = Message.objects.filter(receiver=user, sender__active_constituency=mp.active_constituency, read=False)
            unread_messages=messages.count()

            
            
            return Response({
            "status":status.HTTP_200_OK,
            "messages":unread_messages,
            "incident_reports":incidents,
            "request_forms":requests_
            }, status=status.HTTP_200_OK)
        else:

            messages = Message.objects.filter(receiver=user, sender=mp, read=False)
            unread_messages = messages.count()
            return Response({
                "status":status.HTTP_200_OK,
                "messages":unread_messages,
            }, status=status.HTTP_200_OK)


class SetMessageToReadView(APIView):
    permission_classes=()

    def post(self,request,id):
        message = Message.objects.get(id=id)

        message.read = True
        message.save()

        return Response({
            "status":status.HTTP_200_OK
        }
        )
  


class ReadMessagesView(APIView):
    permission_classes = ()
    def post(self, request, receiver, sender):
        try:
            receiver = User.objects.get(system_id_for_user=receiver)
            sender = User.objects.get(system_id_for_user=sender)

            # const = mp.active_constituency

            messages = Message.objects.filter(sender=sender, receiver=receiver).filter(read=False)
            print("---------------------------")
            print(messages)
            for message in messages:
                message.read = True

                message.save()

            
           
            data = {
                "status":status.HTTP_200_OK,
                "message":"messages has been marked as read."
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            return Response()



class SendMessageToForum(APIView):
    permission_classes=()

    def post(self, request):
        try:
            sender  = User.objects.get(system_id_for_user=request.data['sender'])

            const = sender.active_constituency

            mp  = User.objects.filter(active_constituency=const, is_mp=True).first()

            message = request.data['message']

            data = UserSerializer(sender)


            mess = ForumMessage.objects.create(
                sender = sender,
                message = message,
                constituency = const,
                current_mp = mp
            )

            mess.save()

            return Response({
                "status": status.HTTP_200_OK,
                "message":"message has been sent",
                "sender": data.data
            })

        except Exception as e:
            print(e)
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message":"message was not sent."
            })



class RetrieveForumMessages(APIView):
    permission_classes=()

    def get(self, reequest, id):
        try:
            user = User.objects.get(system_id_for_user=id)
            mp = User.objects.filter(active_constituency=user.active_constituency, is_mp=True).first()
            messages = ForumMessage.objects.filter(
                constituency=user.active_constituency,
                current_mp = mp
            )

            messages = ForumMessageSerializer(messages, many=True)

            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":messages.data
                }
            )
        except Exception:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST
                }
            )

class CheckIfMpIsAvailable(APIView):
    permission_classes = ()

    def get(self, request, id):
        user = User.objects.get(system_id_for_user=id)

        mp = User.objects.filter(active_constituency=user.active_constituency, is_mp=True)

        if len(mp) > 0:
            mp = UserSerializer(mp[0])
            return Response({
                "status":status.HTTP_200_OK,
                "is_mp_available":True,
                "mp":mp.data
            }
            )
        else:
            return Response({
                "status":status.HTTP_200_OK,
                "is_mp_available":False
            }
            )
