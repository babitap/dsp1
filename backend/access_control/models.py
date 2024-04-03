from django.contrib import auth
from django.db import models
#from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from api.graphqlapi.model_acara import AcaraSchoolMaster
from functools import reduce
from django.db.models import Q

#------------------------------------------------------------------------------

class Entity(models.Model):
    """
    id: unique id for entity
    entity_name: name of entity
    industry_id: id of entitiy wihtin specific industry
    industry_name: name of industry for entity
    """
    entity_name = models.CharField(max_length=255, null=True)
    industry_id = models.IntegerField(null=False)
    industry_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_activated = models.DateTimeField(_('date joined'), default=timezone.now)
    date_disabled = models.DateTimeField(_('date disabled'), default=None, null=True)

    class Meta:
        unique_together = ('industry_id', 'industry_name',)

#------------------------------------------------------------------------------

class PermissionManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            #content_type=ContentType.objects.db_manager(self.db).get_by_natural_key(app_label, model),
        )

class Permission(models.Model):

    name = models.CharField(_('name'), max_length=255)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    is_findex = models.BooleanField(default=False)
    is_findex_all = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this permission should be treated as active. '
            'Unselect this instead of deleting permission.'
        ),
    )
    objects = PermissionManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        #unique_together = (('codename'),)
        #ordering = ('content_type__app_label', 'content_type__model',
        #            'codename')

    '''def __str__(self):
                    return "%s | %s | %s" % (
                        self.content_type.app_label,
                        self.content_type,
                        self.name,
                    )'''

    '''def natural_key(self):
                    return (self.codename,) + self.content_type.natural_key()
                natural_key.dependencies = ['contenttypes.contenttype']'''

#------------------------------------------------------------------------------
class DownloadPermissionManager(models.Manager):
    """
    The manager for the download permissions model 
    """

    def get_mapped_folder(self, user_id, entity_id, download_id): 
        # 1, get all permitted_download
        permitted_downloads = self.get_download_list(user_id, entity_id)

        # 2, check the requested download_id is permitted or not
        for download in permitted_downloads:
            if download['id'] == download_id:
                # 3, if permitted, return the mapped folder 
                download_permission = DownloadPermission.objects.get( id = download['id'] )
                if download_permission:
                    return [ download_permission.reports_folder ]
                else:
                    return []
        return []

    # get download list for specific user and entity_id based on his download permissions
    def get_download_list(self, user_id, entity_id):
        # 1, get available download permissions ( used in the next step )
        download_permissions = list( DownloadPermission.objects.all().filter( entity_id=entity_id, is_active=True )\
                .values('id','name', 'permission_codename') )

        download_permissions_dict = {}
        for p in download_permissions:
            permission_id       = p['id']
            permission_name     = p['name']
            permission_codename = p['permission_codename']
            if permission_codename in download_permissions_dict:
                download_permissions_dict[permission_codename].append(
                    {   'id':permission_id,
                        'name': permission_name
                    }                    
                )
            else: 
                download_permissions_dict[permission_codename] = [
                    {   'id':permission_id,
                        'name': permission_name
                    }
                ]
        
        # 2, get all available permissions for the given entity
        permitted_downloads = []
        login_user = User.objects.get( id = user_id )
        user_permissions_list = login_user.get_all_permissions( entity_id )

        for user_permission in user_permissions_list:
            #if user_permission.permission_codename in all_download_permissions:
            permission_codename = user_permission['codename']
            if permission_codename in download_permissions_dict:
                for t in download_permissions_dict[permission_codename]:
                    permitted_downloads.append(t)
        return permitted_downloads

    # get download folder for a specific download id 
    def get_download_folder(self, download_id, user_id, entity_id ) : 
        return 


class ExportPermissionManager(models.Manager):
    """
    The manager for the export permissions model 
    """

    def get_mapped_folder(self, user_id, entity_id, export_id): 
        # 1, get all permitted_exports
        permitted_exports = self.get_export_pages_list(user_id, entity_id)

        # 2, check the requested export_id is permitted or not
        for export in permitted_exports:
            if export['id'] == export_id:
                # 3, if permitted, return the mapped folder 
                export_permission = ExportPermission.objects.get( id = export['id'] )
                if export_permission:
                    return [ export_permission.reports_folder ]
                else:
                    return []
        return []

    # get export list for specific user and entity_id based on his export permissions
    def get_export_pages_list(self, user_id, entity_id):
        # 1, get available export pages of entity ( used in the next step )
        export_permissions = list( ExportPermission.objects.all().filter( entity_id=entity_id, is_active=True )\
                .values('id','name', 'permission_codename') )

        export_permissions_dict = {}
        for p in export_permissions:
            permission_id       = p['id']
            permission_name     = p['name']
            permission_codename = p['permission_codename']
            if permission_codename in export_permissions_dict:
                export_permissions_dict[permission_codename].append(
                    {   'id':permission_id,
                        'name': permission_name
                    }                    
                )
            else: 
                export_permissions_dict[permission_codename] = [
                    {   'id':permission_id,
                        'name': permission_name
                    }
                ]

        # 2, get all available permissions for the given entity
        permitted_exports = []
        login_user = User.objects.get( id = user_id )
        user_permissions_list = login_user.get_all_permissions( entity_id )

        for user_permission in user_permissions_list:
            #if user_permission.permission_codename in all_download_permissions:
            permission_codename = user_permission['codename']
            if permission_codename in export_permissions_dict:
                for t in export_permissions_dict[permission_codename]:
                    permitted_exports.append(t)
        return permitted_exports

    # get export folder for a specific export id 
    def get_export_folder(self, export_id, user_id, entity_id ) : 
        return 

class DownloadPermission( models.Model):
    id         =  models.IntegerField( _('id'), unique=True, primary_key=True )
    name       =  models.CharField(_('name'), max_length=100)
    permission_codename =  models.CharField(_('permission_codename'), max_length=100, unique=True)
    entity_id           =  models.IntegerField( _('entity_id') )
    reports_folder      =  models.CharField(_('reports_folder'), max_length=100, unique=True)
    is_active = models.BooleanField( _('is_active'), default=True )

    objects = DownloadPermissionManager()

    class Meta:
        managed = False
        db_table = 'access_control_download_permissions'    


class ExportPermission( models.Model):
    id         =  models.IntegerField( _('id'), unique=True, primary_key=True )
    name       =  models.CharField(_('name'), max_length=100)
    permission_codename =  models.CharField(_('permission_codename'), max_length=100, unique=True)
    entity_id           =  models.IntegerField( _('entity_id') )
    is_active = models.BooleanField( _('is_active'), default=True )
    workspace_id =  models.CharField(_('workspace_id'), max_length=100, unique=True)
    report_id =  models.CharField(_('report_id'), max_length=100, unique=True)
    report_name =  models.CharField(_('report_name'), max_length=100, unique=True)

    objects = ExportPermissionManager()

    class Meta:
        managed = False
        db_table = 'access_control_export_permissions'    


class GroupManager(models.Manager):
    """
    The manager for the auth's Group model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

class EntityGroup(models.Model):

    name = models.CharField(_('name'), max_length=80)
    description = models.CharField(_('description'), max_length=255)
    entity = models.ForeignKey(Entity, db_index=True, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this entity group should be treated as active. '
            'Unselect this instead of deleting groups.'
        ),
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        unique_together = ('name', 'entity',)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

#-----------------------------------------------------------------------------
class ReportCategoryManager(models.Manager):
    """
    The manager for the report category model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

class ReportCategory (models.Model):
    name = models.CharField(_('name'), max_length=80, null=False)
    description = models.CharField(_('description'), max_length=255)

    objects = ReportCategoryManager()

    class Meta:
        verbose_name = _('report category')
        verbose_name_plural = _('report categories')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


#------------------------------------------------------------------------------
class ReportManager(models.Manager):
    """
    The manager for the report model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Report (models.Model):

    name = models.CharField(_('name'), max_length=255, null=False)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    workspace_id = models.CharField(_('workspaceId'), max_length=36, null=False)
    report_id = models.CharField(_('reportId'), max_length=36, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=False)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(ReportCategory, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this report should be treated as active. '
            'Unselect this instead of deleting report.'
        ),
    )
    objects = ReportManager()
    enable_RLS = models.BooleanField(_('enableRLS'))

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

#------------------------------------------------------------------------------

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user=self.model(
            username = username,
            **extra_fields
            )
        user.save(using=self._db)
        return user

    def create_user(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, **extra_fields)

    def create_superuser(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, **extra_fields)

    def create_findexuser(self, username, **extra_fields):
        extra_fields.setdefault('is_findex', True)
        if extra_fields.get('is_findex') is not True:
            raise ValueError('Findex user must have is_findex=True.')
        return self._create_user(username, **extra_fields)

    def create_findexuser_all(self, username, **extra_fields):
        extra_fields.setdefault('is_findex_all', True)
        if extra_fields.get('is_findex_all') is not True:
            raise ValueError('Findex "all" user must have is_findex_all=True.')
        return self._create_user(username, **extra_fields)

# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions

def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False

def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False

class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        EntityGroup,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )
    entities = models.ManyToManyField(
        Entity,
        verbose_name=_('entities'),
        blank=True,
        help_text=_(
            'The entities this user belongs to.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, entityId=None, obj=None):
        """
        If user has either is_superuser, is_findex or is_findex_all set
        Simply return permissions for given user

        For all other user, only the permissions granted to the group
        where user belongs to will be returned. If entityId is provided
        only the permissions for the entity groups in that particular entity
        will be returned.  
        """
        if self.is_active:
            isActiveFiler = Q(is_active=True)
            if self.is_superuser:
                return list(Permission.objects.filter(isActiveFiler).values('id', 'codename', 'name'))
            else:
                filter = None
                if self.is_findex:
                    filter = Q(is_findex=1)
                elif self.is_findex_all:
                    filter = Q(is_findex_all=1)
                else:
                    group_list = None
                    if entityId is not None:
                        group_list = list(map(lambda x: x['id'], self.groups.filter(entity_id=entityId).values('id')))
                    else:
                        group_list = list(map(lambda x: x['id'], self.groups.values('id')))
                    group_filter = Q(id__in=group_list)
                    filter = Q(id__in=EntityGroup.objects.filter(group_filter).values('permissions'))
                return list(Permission.objects.filter(filter & isActiveFiler).values('id', 'codename', 'name'))
        else:
            return _user_get_all_permissions(self, obj)


    def has_perm(self, perm, entityId=None, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        
        #First check whether user is active
        if self.is_active:
            # Active superusers have all permissions.
            if self.is_superuser:
                return True
            else:
                permissions = self.get_all_permissions(entityId, obj)
                permission_codes = list(map(lambda x: x['codename'], permissions))
                return perm in permission_codes
        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_superuser_perm(self, obj=None): 
        if self.is_active and self.is_superuser: 
            return True
        else: 
            return False 

    def has_special_user_perm(self, obj=None):
        if self.is_active and (self.is_superuser or self.is_findex_all or self.is_findex ): 
            return True
        else: 
            return False                 

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_entities(self):
        query = None

        if self.has_perm('view_all_schools'):
            query = Entity.objects.filter(is_active=True)
        else:
            query = self.entities.filter(is_active=True)
        
        return list(query.values('id', 'industry_id', 'entity_name', 'industry_name').order_by('id'))

    def get_entity_industryIds(self):
        industryIds = list(self.entities.filter(is_active=True).values('industry_id'))
        return list(map(lambda x: x['industry_id'], industryIds))

    def get_default_school(self):
        entity_list = self.get_entity_industryIds()

        defaultEntity = []

        if self.has_perm('view_all_schools'):
            firstEntity = Entity.objects.filter(is_active=True).values('industry_id').order_by('id').first()
            defaultEntity.append(firstEntity['industry_id'])
        else:
            defaultEntity = entity_list

        q_list = map(lambda n: Q(acara_id__iexact=n), defaultEntity)
        q_list = reduce(lambda a, b: a | b, q_list)
        default_school = AcaraSchoolMaster.objects.using('public_data').get(acara_id=defaultEntity[0])
        return default_school
    
    def get_all_user_group(self, entityId):
        if self.is_active:
            isActiveFiler = Q(is_active=True)
            entityFilter  = Q(entity_id=entityId)

            if self.is_superuser:
                return list(EntityGroup.objects.filter(isActiveFiler&entityFilter).values('id', 'name', 'description'))
            else:
                return list(self.groups.filter(isActiveFiler&entityFilter).values('id','name', 'description'))
        else:
            return list()


class User(AbstractBaseUser,PermissionsMixin):
    """
    All fields stored based on the user
    id: is in base model and is referred as user_id for app - unique in this model
    oid: this id is from B2C and should be filled on first login
    """
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    given_name = models.CharField(max_length=150, null=True)
    family_name = models.CharField(max_length=150, null=True)
    oid = models.CharField(max_length=255, blank=True, null=True)
    is_findex = models.BooleanField(default=False)
    is_findex_all = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    date_disabled = models.DateTimeField(_('date disabled'), default=None, null=True)
    created_by = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
    last_selected_entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, related_name='last_selected_entity')

    objects=MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []