from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # 정보를 읽는 요청은 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user

# 투표자가 아니라면, 수정과 읽는 요청 모두 불가능
class IsVoter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.voter == request.user