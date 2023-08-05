# Generated by Django 2.2.6 on 2019-10-23 08:46

import dj_pony.ulidfield.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
import ulid.api


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('ulid', dj_pony.ulidfield.models.ULIDField(db_index=True, default=ulid.api.new, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(default=ulid.api.new, max_length=255, unique=True)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
                ('settings', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_site', to='sites.Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_sites', to='tenant.Tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_tenant_groups', to='auth.Group')),
                ('permissions', models.ManyToManyField(blank=True, related_name='user_tenant_permissions', to='auth.Permission')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='tenant.Tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'tenant')},
            },
        ),
    ]
