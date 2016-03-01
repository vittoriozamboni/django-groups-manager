

class MemberDjangoUserSyncError(BaseException):
    """
    Raised when try to access to Member.django_user attribute and it is None."""
    pass


class GroupDjangoGroupSyncError(BaseException):
    """
    Raised when try to access to Group.django_group attribute and it is None."""
    pass


class GroupNotSavedError(BaseException):
    """
    Raised when try to use a group as a foreign key"""
    pass


class MemberNotSavedError(BaseException):
    """
    Raised when try to use a member as a foreign key"""
    pass


class GetGroupMemberError(BaseException):
    """
    Raised when try to get a GroupMember relation but there is no entry in database"""
    pass


class GetRoleError(BaseException):
    """
    Raised when try to fetch a Role via non-int and non-string object"""
    pass
