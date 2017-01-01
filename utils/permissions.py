def check_permission(permission_classes, self, request, obj=None):
    #  !!! permission_class must a tuple !!! such like (a,)
    #  self = Class ViewSet self
    self.permission_classes = permission_classes
    if obj is not None:
        self.check_object_permissions(request, obj)
    self.check_permissions(request)
