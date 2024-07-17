from django.test import TestCase
"""
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from assets.models import Asset, Tag, AssetTag
from django.contrib.auth import get_user_model

User = get_user_model()

class AssetTagTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com
            password='adminpass'
        )
        self.client.force_authenticate(user=self.admin_user)

        self.asset = Asset.objects.create(
            name='Laptop',
            assetType='Electronics',
            description='A high-end laptop',
            serialNumber='ABC12345',
            category_id=1,
            assignedDepartment_id=1,
            status=True
        )
        self.tag = Tag.objects.create(name='IT Equipment')
        self.asset_tag_url = reverse('asset-tag-list')

    def test_create_asset_tag(self):
        payload = {
            'asset': self.asset.id,
            'tag': self.tag.id
        }
        response = self.client.post(self.asset_tag_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert
        Equal(AssetTag.objects.count(), 1)

    def test_list_asset_tags(self):
        AssetTag.objects.create(asset=self.asset, tag=self.tag)
        response = self.client.get(self.asset_tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_asset_tag(self):
        asset_tag = AssetTag.objects.create(asset=self.asset, tag=self.tag)
        new_tag = Tag.objects.create(name='Office Equipment')
        payload = {
            'asset': self.asset.id,
            'tag': new_tag.id
        }
        url = reverse('asset-tag-detail', args=[asset_tag.id])
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code
, status.HTTP_200_OK)
        asset_tag.refresh_from_db()
        self.assertEqual(asset_tag.tag.id, new_tag.id)

    def test_delete_asset_tag(self):
        asset_tag = AssetTag.objects.create(asset=self.asset, tag=self.tag)
        url = reverse('asset-tag-detail', args=[asset_tag.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssetTag.objects.count(), 0)

"""