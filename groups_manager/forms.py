from django import forms

from django_helper_forms.forms import DictionaryFieldsForm

import models


class MemberForm(forms.ModelForm):

    class Meta:
        model = models.Member
        exclude = set()


class GroupTypeForm(forms.ModelForm):

    class Meta:
        model = models.GroupType
        exclude = set()


class GroupEntityForm(forms.ModelForm):

    class Meta:
        model = models.GroupEntity
        exclude = set()


class GroupForm(forms.ModelForm, DictionaryFieldsForm):

    class Meta:
        model = models.Group
        exclude = ('group_members', )

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.dictionary_fields = ['properties', ]
        self.format_dictionary_fields()


class GroupMemberRoleForm(forms.ModelForm):

    class Meta:
        model = models.GroupMemberRole
        exclude = set()


class GroupMemberForm(forms.ModelForm):

    class Meta:
        model = models.GroupMember
        exclude = ('group', 'member', )


class GroupMemberAddMemberForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=models.Group.objects.all(),
                                   widget=forms.HiddenInput(), )

    class Meta:
        model = models.GroupMember
        exclude = set()


class GroupMemberAddGroupForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=models.Member.objects.all(),
                                   widget=forms.HiddenInput(), )

    class Meta:
        model = models.GroupMember
        exclude = set()
