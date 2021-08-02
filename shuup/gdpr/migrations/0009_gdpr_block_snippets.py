# Generated by Django 2.2.24 on 2021-07-06 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuup_xtheme', '0009_gdpr_block_snippets'),
        ('shuup_gdpr', '0008_django2_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='gdprcookiecategory',
            name='block_snippets',
            field=models.ManyToManyField(blank=True, help_text="Select the snippets that shouldn't be injected if the cookie is not consented.", related_name='blocked_gdpr_cookies', to='shuup_xtheme.Snippet', verbose_name='Snippets to block if not consented'),
        ),
    ]