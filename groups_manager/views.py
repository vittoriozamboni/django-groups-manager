import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from groups_manager import models
from groups_manager import forms


class GroupsManagerView(TemplateView):
    template_name = 'groups_manager/groups_manager_home.html'


'''
Members
'''


class MemberMixin(object):
    context_object_name = 'member'
    model = models.Member
    form_class = forms.MemberForm

    def get_success_url(self):
        return reverse('groups_manager:member_list')


class MemberListView(LoginRequiredMixin, MemberMixin, ListView):
    template_name = 'groups_manager/member_list.html'

    def get_queryset(self):
        return models.Member.objects.all()


class MemberDetailView(LoginRequiredMixin, MemberMixin, DetailView):
    template_name = 'groups_manager/member_detail.html'


class MemberCreateView(LoginRequiredMixin, MemberMixin, CreateView):
    template_name = 'groups_manager/member_form.html'


class MemberEditView(LoginRequiredMixin, MemberMixin, UpdateView):
    template_name = 'groups_manager/member_form.html'


class MemberDeleteView(LoginRequiredMixin, MemberMixin, DeleteView):
    template_name = 'groups_manager/member_confirm_delete.html'


'''
Group Types
'''


class GroupTypeMixin(object):
    context_object_name = 'group_type'
    model = models.GroupType
    form_class = forms.GroupTypeForm

    def get_success_url(self):
        return reverse('groups_manager:group_type_list')


class GroupTypeListView(LoginRequiredMixin, GroupTypeMixin, ListView):
    template_name = 'groups_manager/group_type_list.html'

    def get_queryset(self):
        return models.GroupType.objects.all()


class GroupTypeDetailView(LoginRequiredMixin, GroupTypeMixin, DetailView):
    template_name = 'groups_manager/group_type_detail.html'


class GroupTypeCreateView(LoginRequiredMixin, GroupTypeMixin, CreateView):
    template_name = 'groups_manager/group_type_form.html'


class GroupTypeEditView(LoginRequiredMixin, GroupTypeMixin, UpdateView):
    template_name = 'groups_manager/group_type_form.html'


class GroupTypeDeleteView(LoginRequiredMixin, GroupTypeMixin, DeleteView):
    template_name = 'groups_manager/group_type_confirm_delete.html'


'''
Group Entities
'''


class GroupEntityMixin(object):
    context_object_name = 'group_entity'
    model = models.GroupEntity
    form_class = forms.GroupEntityForm

    def get_success_url(self):
        return reverse('groups_manager:group_entity_list')


class GroupEntityListView(LoginRequiredMixin, GroupEntityMixin, ListView):
    template_name = 'groups_manager/group_entity_list.html'

    def get_queryset(self):
        return models.GroupEntity.objects.all()


class GroupEntityDetailView(LoginRequiredMixin, GroupEntityMixin, DetailView):
    template_name = 'groups_manager/group_entity_detail.html'


class GroupEntityCreateView(LoginRequiredMixin, GroupEntityMixin, CreateView):
    template_name = 'groups_manager/group_entity_form.html'


class GroupEntityEditView(LoginRequiredMixin, GroupEntityMixin, UpdateView):
    template_name = 'groups_manager/group_entity_form.html'


class GroupEntityDeleteView(LoginRequiredMixin, GroupEntityMixin, DeleteView):
    template_name = 'groups_manager/group_entity_confirm_delete.html'


'''
Groups
'''


class GroupMixin(object):
    context_object_name = 'group'
    model = models.Group
    form_class = forms.GroupForm

    def get_success_url(self):
        return reverse('groups_manager:group_list')


class GroupListView(LoginRequiredMixin, GroupMixin, ListView):
    template_name = 'groups_manager/group_list.html'

    def get_queryset(self):
        return models.Group.objects.all()


class GroupDetailView(LoginRequiredMixin, GroupMixin, DetailView):
    template_name = 'groups_manager/group_detail.html'


class GroupCreateView(LoginRequiredMixin, GroupMixin, CreateView):
    template_name = 'groups_manager/group_form.html'

    def get_success_url(self):
        group = self.get_object()
        return reverse('groups_manager:group_detail', kwargs={'pk': group.id})


class GroupEditView(LoginRequiredMixin, GroupMixin, UpdateView):
    template_name = 'groups_manager/group_form.html'

    def get_success_url(self):
        group = self.get_object()
        return reverse('groups_manager:group_detail', kwargs={'pk': group.id})


class GroupDeleteView(LoginRequiredMixin, GroupMixin, DeleteView):
    template_name = 'groups_manager/group_confirm_delete.html'


'''
Group Member Roles
'''


class GroupMemberRoleMixin(object):
    context_object_name = 'group_member_role'
    model = models.GroupMemberRole
    form_class = forms.GroupMemberRoleForm

    def get_success_url(self):
        return reverse('groups_manager:group_member_role_list')


class GroupMemberRoleListView(LoginRequiredMixin, GroupMemberRoleMixin, ListView):
    template_name = 'groups_manager/group_member_role_list.html'

    def get_queryset(self):
        return models.GroupMemberRole.objects.all()


class GroupMemberRoleDetailView(LoginRequiredMixin, GroupMemberRoleMixin, DetailView):
    template_name = 'groups_manager/group_member_role_detail.html'


class GroupMemberRoleCreateView(LoginRequiredMixin, GroupMemberRoleMixin, CreateView):
    template_name = 'groups_manager/group_member_role_form.html'


class GroupMemberRoleEditView(LoginRequiredMixin, GroupMemberRoleMixin, UpdateView):
    template_name = 'groups_manager/group_member_role_form.html'


class GroupMemberRoleDeleteView(LoginRequiredMixin, GroupMemberRoleMixin, DeleteView):
    template_name = 'groups_manager/group_member_role_confirm_delete.html'


'''
GroupMembers
'''


class GroupMemberMixin(object):
    context_object_name = 'group_member'
    model = models.GroupMember


class GroupMemberEditView(LoginRequiredMixin, GroupMemberMixin, UpdateView):
    template_name = 'groups_manager/group_member_form.html'
    form_class = forms.GroupMemberForm

    def get_context_data(self, **kwargs):
        context = super(GroupMemberEditView, self).get_context_data(**kwargs)
        group_member = self.get_object()
        context['group'] = group_member.group
        return context

    def get_success_url(self):
        group_member = self.get_object()
        return reverse('groups_manager:group_detail', kwargs={'pk': group_member.group.id})


class GroupMemberDeleteView(LoginRequiredMixin, GroupMemberMixin, DeleteView):
    template_name = 'groups_manager/group_member_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(GroupMemberDeleteView, self).get_context_data(**kwargs)
        group_member = self.get_object()
        context['group'] = group_member.group
        return context

    def get_success_url(self):
        group_member = self.get_object()
        return reverse('groups_manager:group_detail', kwargs={'pk': group_member.group.id})


class GroupMemberAddMemberView(LoginRequiredMixin, GroupMemberMixin, CreateView):
    template_name = 'groups_manager/group_member_add_member_form.html'
    form_class = forms.GroupMemberAddMemberForm

    def get_initial(self):
        initial = super(GroupMemberAddMemberView, self).get_initial()
        initial['group'] = models.Group.objects.get(id=self.kwargs.get('group_id'))
        return initial

    def get_context_data(self, **kwargs):
        context = super(GroupMemberAddMemberView, self).get_context_data(**kwargs)
        context['group'] = models.Group.objects.get(id=self.kwargs.get('group_id'))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(
            reverse('groups_manager:group_detail', kwargs={'pk': self.object.group.id}))


class GroupMemberAddGroupView(LoginRequiredMixin, GroupMemberMixin, CreateView):
    template_name = 'groups_manager/group_member_add_group_form.html'
    form_class = forms.GroupMemberAddGroupForm

    def get_initial(self):
        initial = super(GroupMemberAddGroupView, self).get_initial()
        initial['member'] = models.Member.objects.get(id=self.kwargs.get('member_id'))
        return initial

    def get_context_data(self, **kwargs):
        context = super(GroupMemberAddGroupView, self).get_context_data(**kwargs)
        context['member'] = models.Member.objects.get(id=self.request.GET.get('member_id'))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(
            reverse('groups_manager:group_detail', kwargs={'pk': self.object.group.id}))
