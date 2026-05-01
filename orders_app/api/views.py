from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from .permissions import IsBusinessUser, IsCustomerUser
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
)


class OrderListCreateView(APIView):
    """Lists related orders or creates a new order."""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get(self, request):
        orders = Order.objects.filter(customer_user=request.user) | Order.objects.filter(
            business_user=request.user
        )
        serializer = OrderSerializer(orders.distinct(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    """Updates or deletes a single order."""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def patch(self, request, pk):
        order = self.get_object(pk)

        if not self._can_update_order(request, order):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = OrderStatusUpdateSerializer(
            order,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(OrderSerializer(order).data)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        order = self.get_object(pk)
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _can_update_order(self, request, order):
        is_business = IsBusinessUser().has_permission(request, self)
        is_owner = order.business_user == request.user
        return is_business and is_owner


class OrderCountView(APIView):
    """Returns active order count for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        count = Order.objects.filter(
            business_user__id=pk,
            status=Order.IN_PROGRESS,
        ).count()
        return Response({"order_count": count})


class CompletedOrderCountView(APIView):
    """Returns completed order count for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        count = Order.objects.filter(
            business_user__id=pk,
            status=Order.COMPLETED,
        ).count()
        return Response({
            "completed_order_count": count,
            "order_count": count,
        })