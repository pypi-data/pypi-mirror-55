# Generated by Django 2.2.4 on 2019-08-27 16:29

import django.core.validators
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpress', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticlepage',
            name='content',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.StructBlock([('header_level', wagtail.core.blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')], label='Header level')), ('text', wagtail.core.blocks.CharBlock(label='Text'))])), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('quote', wagtail.core.blocks.BlockQuoteBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('imagetextoverlay', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('text', wagtail.core.blocks.CharBlock(label='Text', max_length=200)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('black', 'Black'), ('white', 'White'), ('red', 'Red'), ('blue', 'Blue'), ('green', 'Green')], label='Text color')), ('text_position', wagtail.core.blocks.ChoiceBlock(choices=[('top: 50%; left: 50%; transform: translate(-50%, -50%);', 'Centered'), ('top: 20px; left: 20px;', 'Top Left'), ('top: 20px; right: 20px;', 'Top Right'), ('bottom: 20px; left: 20px;', 'Bottom Left'), ('bottom: 20px; right: 20px;', 'Bottom Right')]))])), ('link', wagtail.core.blocks.StructBlock([('description', wagtail.core.blocks.CharBlock(label='Description')), ('url', wagtail.core.blocks.URLBlock(label='URL', validators=[django.core.validators.URLValidator(['http', 'https', 'ftp', 'ftps', 'mailto', 'xmpp', 'tel'])]))])), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('embed', wagtail.embeds.blocks.EmbedBlock())], verbose_name='content'),
        ),
    ]
