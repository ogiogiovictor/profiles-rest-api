from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """
    Custom permission to only allow users to update their own profile.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id
        # else:
        #     return obj.review_user == request.user or request.user.is_staff