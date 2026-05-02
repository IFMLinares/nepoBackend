import pytest
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.inventory.models import Category, Product, UnitOfMeasure

@pytest.fixture
def uom(db):
    return UnitOfMeasure.objects.get_or_create(abbreviation='Und', defaults={'name': 'Unidad'})[0]

@pytest.fixture
def category(db):
    return Category.objects.create(name='Electrónica')

@pytest.mark.django_db
class TestInventoryAPI:

    def test_create_product_success(self, api_admin_client, uom, category):
        """Prueba la creación exitosa de un producto con categorías (Enfoque A)"""
        url = reverse('product-list')
        data = {
            'name': 'Laptop Dell',
            'quantity': 10.5,
            'description': 'Laptop potente',
            'unit_of_measure': uom.id,
            'categories': [category.id]
        }
        
        response = api_admin_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        assert isinstance(response.data['categories'], list)
        assert response.data['categories'][0]['name'] == 'Electrónica'

    def test_create_product_with_image(self, api_admin_client, uom, category):
        """Prueba la subida de imagen en productos"""
        url = reverse('product-list')
        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        image = SimpleUploadedFile("test_image.gif", image_content, content_type="image/gif")
        
        data = {
            'name': 'Mouse Inalámbrico',
            'quantity': 50,
            'unit_of_measure': uom.id,
            'categories': [category.id],
            'image': image
        }
        
        response = api_admin_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.get(name='Mouse Inalámbrico').image is not None

    def test_unauthorized_create_fails(self, api_client, db, uom):
        """Verifica que un usuario no admin no pueda crear productos"""
        from apps.users.models import User
        regular_user = User.objects.create_user(username='reg', email='r@t.com', password='p')
        api_client.force_authenticate(user=regular_user)
        
        url = reverse('product-list')
        data = {'name': 'Hack Product', 'quantity': 1, 'unit_of_measure': uom.id}
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_invalid_category_fails(self, api_admin_client, uom):
        """Verifica que falle si se intenta asignar una categoría inexistente"""
        url = reverse('product-list')
        data = {
            'name': 'Error Product',
            'quantity': 1,
            'unit_of_measure': uom.id,
            'categories': [999]
        }
        
        response = api_admin_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'categories' in response.data

    def test_soft_delete_product(self, api_admin_client, uom):
        """Verifica que el borrado sea lógico (is_active=False)"""
        product = Product.objects.create(name='Old Product', unit_of_measure=uom)
        url = reverse('product-detail', args=[product.id])
        
        response = api_admin_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        product.refresh_from_db()
        assert product.is_active is False

    def test_filter_by_category(self, api_client, uom, category):
        """Prueba el filtrado de productos por categoría"""
        from apps.users.models import User
        user = User.objects.create_user(username='filt', email='f@t.com', password='p')
        api_client.force_authenticate(user=user)
        
        cat2 = Category.objects.create(name='Hogar')
        p1 = Product.objects.create(name='Sofa', unit_of_measure=uom)
        p1.categories.add(cat2)
        
        p2 = Product.objects.create(name='Radio', unit_of_measure=uom)
        p2.categories.add(category)
        
        url = reverse('product-list')
        response = api_client.get(f"{url}?categories__name=Hogar")
        
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Sofa'
