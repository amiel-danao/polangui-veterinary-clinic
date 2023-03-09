# Generated by Django 4.0.4 on 2022-11-20 07:20

import app.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('summary', models.TextField(blank=True, null=True)),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('breed_name', models.CharField(max_length=80, primary_key=True, serialize=False, unique=True)),
                ('species', models.CharField(choices=[('Cat', 'Cat'), ('Dog', 'Dog')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.CharField(default=app.models.id_gen, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('middlename', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100)),
                ('mrp', models.FloatField()),
                ('discount', models.FloatField()),
                ('price', models.FloatField()),
                ('quantity', models.SmallIntegerField()),
                ('sold', models.SmallIntegerField()),
                ('available', models.SmallIntegerField()),
                ('defective', models.SmallIntegerField()),
                ('createdby', models.BigIntegerField(db_column='createdBy')),
                ('updatedby', models.BigIntegerField(blank=True, db_column='updatedBy', null=True)),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('brandid', models.ForeignKey(db_column='brandId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField()),
                ('status', models.SmallIntegerField()),
                ('subtotal', models.FloatField(db_column='subTotal')),
                ('itemdiscount', models.FloatField(db_column='itemDiscount')),
                ('tax', models.FloatField()),
                ('shipping', models.FloatField()),
                ('total', models.FloatField()),
                ('promo', models.CharField(blank=True, max_length=50, null=True)),
                ('discount', models.FloatField()),
                ('grandtotal', models.FloatField(db_column='grandTotal')),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('summary', models.TextField(blank=True, null=True)),
                ('type', models.SmallIntegerField()),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('name', models.CharField(max_length=80, primary_key=True, serialize=False, unique=True)),
                ('brand', models.CharField(blank=True, max_length=80)),
                ('capacity', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('side_effects', models.CharField(blank=True, max_length=80)),
                ('effect_duration', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('intake_type', models.CharField(blank=True, max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('type', models.SmallIntegerField()),
                ('mode', models.SmallIntegerField()),
                ('status', models.SmallIntegerField()),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('orderid', models.ForeignKey(db_column='orderId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.order')),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.CharField(default=app.models.id_gen, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('weight', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('height', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('species', models.CharField(choices=[('Cat', 'Cat'), ('Dog', 'Dog')], default='Cat', max_length=10)),
                ('allergies', models.CharField(blank=True, max_length=50)),
                ('existing_conditions', models.CharField(blank=True, max_length=80)),
                ('image', models.CharField(blank=True, max_length=300)),
                ('breed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.breed')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
            options={
                'unique_together': {('name', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('discount', models.FloatField()),
                ('quantity', models.SmallIntegerField()),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('itemid', models.ForeignKey(db_column='itemId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.item')),
                ('orderid', models.ForeignKey(db_column='orderId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.order')),
                ('productid', models.ForeignKey(db_column='productId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.product')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='orderid',
            field=models.ForeignKey(db_column='orderId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.order'),
        ),
        migrations.AddField(
            model_name='item',
            name='productid',
            field=models.ForeignKey(db_column='productId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.product'),
        ),
        migrations.AddField(
            model_name='item',
            name='supplierid',
            field=models.ForeignKey(db_column='supplierId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.customer'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('metatitle', models.CharField(blank=True, db_column='metaTitle', max_length=100, null=True)),
                ('slug', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('parentid', models.ForeignKey(blank=True, db_column='parentId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.CharField(default=app.models.id_gen, editable=False, max_length=30, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
        migrations.CreateModel(
            name='ProductMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('productid', models.ForeignKey(db_column='productId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.product')),
            ],
            options={
                'unique_together': {('productid', 'key')},
            },
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('veterinarian', models.CharField(max_length=50)),
                ('diagnosis', models.CharField(max_length=200)),
                ('tests_performed', models.CharField(blank=True, max_length=200, null=True)),
                ('test_results', models.CharField(max_length=200)),
                ('action', models.CharField(blank=True, max_length=200, null=True)),
                ('medication', models.CharField(blank=True, max_length=200, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
            ],
            options={
                'verbose_name_plural': 'Medical Histories',
                'unique_together': {('pet', 'date', 'veterinarian')},
            },
        ),
        migrations.CreateModel(
            name='ImmunizationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_age', models.PositiveSmallIntegerField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
                ('vaccine', models.ManyToManyField(to='app.vaccine')),
            ],
            options={
                'verbose_name_plural': 'Immunization Histories',
                'unique_together': {('pet', 'pet_age')},
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('productid', models.OneToOneField(db_column='productId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.product')),
                ('categoryid', models.ForeignKey(db_column='categoryId', on_delete=django.db.models.deletion.DO_NOTHING, to='app.category')),
            ],
            options={
                'verbose_name_plural': 'Product Categories',
                'db_table': 'product_category',
                'unique_together': {('productid', 'categoryid')},
            },
        ),
    ]
