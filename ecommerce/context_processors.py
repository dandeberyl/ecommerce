# context_processors.py
from orders.models import CartItem

def cart_item_count(request):
    session_key = request.session.session_key
    if not session_key:
        return {"cart_items_count": 0}
    total = CartItem.objects.filter(session_key=session_key).count()
    return {"cart_items_count": total}
