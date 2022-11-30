from rest_framework import serializers
from book.models import Book
from cart.models import Cart, CartItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'price', 'book', 'user', 'cart']


class DataSerializer(serializers.Serializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    quantity = serializers.IntegerField()


class CartSerializer(serializers.ModelSerializer):
    cartitem = ItemSerializer(many=True, read_only=True)
    books = DataSerializer(many=True, write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'status', 'user', 'books', 'cartitem']
        read_only_fields = ['id', 'total_price', 'status','books']

    def create(self, validated_data):
        user = validated_data.get('user')
        cart_list = Cart.objects.filter(user_id=user.id, status=False)
        if len(cart_list) == 0:
            cart = Cart.objects.create(user_id=user.id)
        else:
            cart = cart_list.first()
        for book_dict in validated_data.get('books'):
            book = book_dict.get('book_id')
            for _ in range(book_dict.get('quantity')):
                CartItem.objects.create(book_id=book.id, price=book.price, user_id=user.id,
                                        cart_id=cart.id)
        return cart
