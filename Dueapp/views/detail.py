from rest_framework import viewsets,generics,status
from rest_framework import permissions
from utils import custom_response,custom_exceptions
from utils import permissions  as custom_permissions
from .. import serializers
from .. import models
from rest_framework.decorators import action
from ..models import DeactivatingDue, DeactivatingDue_User, Due_User
from account.models import user as  user_related_models
from account.serializers import user as user_serializer
from django.shortcuts import get_object_or_404

class AdminManageDue(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin,
    custom_permissions.Normal_Admin_Must_BelongToACHapter]
    serializer_class = serializers.AdminManageDuesSerializer

    def list(self,request):
        due = models.Due.objects.all()
        clean_data  = serializers.DueCleanSerialier(due,many=True)
        # clean_data.is_valid()
        return custom_response.Success_response(msg='Dues',data =clean_data.data,status_code=status.HTTP_200_OK)

    @action(detail=False,methods=['get'])
    def owning_members(self,request,pk=None):
        list_of_owing_members = user_related_models.Memeber.objects.filter(is_financial=False)

        clean_data = user_serializer.IsOwningSerializerCleaner(list_of_owing_members,many=True)
        return custom_response.Success_response(msg='Dues',data =clean_data.data,status_code=status.HTTP_200_OK)


    def create(self,request,format=None):
        'an admin is creating Due for the user'
        # print(request.data)
        serialized = self.serializer_class(data=request.data,context={"request":request})
        serialized.is_valid(raise_exception=True)
        due_id =serialized.save()
        due = models.Due.objects.get(id=due_id)
        return custom_response.Success_response(msg='Due created successfully',data=[
            {
        'id':due.id,
        'name':due.Name,
        're_occuring':due.re_occuring,
        'is_for_excos':due.is_for_excos,
        'amount':due.amount,
        'startDate':due.startDate,
        'startTime':due.startTime,
        'scheduletype':due.scheduletype,
        'schedule':due.schedule,
        
        }
        ],status_code=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        if(models.Due.objects.filter(id=pk).exists()):
            due = models.Due.objects.get(id=pk)
            due.delete()
            return custom_response.Success_response(msg='Due Deleted',status_code=status.HTTP_200_OK)
        # if(models,models.DeactivatingDue.objects.filter(id=pk).exists()):
        #     due = models.DeactivatingDue.objects.get(id=pk)
        #     due.delete()
        raise custom_exceptions.CustomError(message={"due":"Due does not exist"})
        




class AdminManageDeactivatingDue(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin,
    custom_permissions.Normal_Admin_Must_BelongToACHapter]
    serializer_class = serializers.AdminManageDeactivatingDuesSerializer

    def create(self,request,format=None):
        'an admin is creating Due for the user'
        # print(request.data)
        serialized = self.serializer_class(data=request.data,context={"request":request})
        serialized.is_valid(raise_exception=True)
        due_id =serialized.save()
        due = models.DeactivatingDue.objects.get(id=due_id)
        return custom_response.Success_response(msg='Deactivating Due created successfully',data=[
        {
        'id':due.id,
        'name':due.name,
        'is_for_excos':due.is_for_excos,
        'amount':due.amount,
        'startDate':due.startDate,
        'startTime':due.startTime,
        'month':due.month,
        }
        ],status_code=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        if(models.DeactivatingDue.objects.filter(id=pk).exists()):
            due = models.DeactivatingDue.objects.get(id=pk)
            due.delete()
            return custom_response.Success_response(msg='Deactivating Due Deleted',status_code=status.HTTP_200_OK)
        # if(models,models.DeactivatingDue.objects.filter(id=pk).exists()):
        #     due = models.DeactivatingDue.objects.get(id=pk)
        #     due.delete()
        raise custom_exceptions.CustomError(message={"error":"Due does not exist"})



class MemberDues(viewsets.ViewSet):
    permission_classes =[permissions.IsAuthenticated,custom_permissions.IsMember]


    def list(self,request,format=None):
        my_dues = Due_User.objects.all().filter(user=request.user).values(
            "id","user__email","due__Name","is_overdue","amount","is_paid")

        return custom_response.Success_response(msg='Success',
                        data=my_dues)
                        
    @action(detail=False,methods=['get'], permission_classes =[permissions.IsAuthenticated,])
    def get_due_detail(self,request,format=None):
        "get the data for all if it admin or super_admin"
        if request.user.user_type == 'admin' or request.user.user_type == 'super_admin':
            dues = Due_User.objects.all().filter()
        else:
            dues = Due_User.objects.all().filter(user=request.user)
        total_outstanding= dues.filter(is_paid=False).count() 
        total_paid= dues.filter(is_paid=True).count()
        data = {
            'outstanding':total_outstanding,
            'total_paid':total_paid

        }
        return custom_response.Success_response(msg='Success',data=[data])


