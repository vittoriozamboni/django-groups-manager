

class MemberDjangoUserSyncError(BaseException):
    '''
    Raised when try to access to Member.django_user attribute and it is None.'''
    pass


class GroupDjangoGroupSyncError(BaseException):
    '''
    Raised when try to access to Group.django_group attribute and it is None.'''
    pass
