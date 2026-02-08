# --- Existing Features (Preserved) ---

# Order Tracking Statuses (Legacy Support)
STATUS_PENDING = "Pending"
STATUS_SHIPPED = "Shipped"
STATUS_DELIVERED = "Delivered"
STATUS_CANCELLED = "Cancelled"

# Seller Verification Statuses
SELLER_STATUS_PENDING = "Pending"
SELLER_STATUS_APPROVED = "Approved"
SELLER_STATUS_REJECTED = "Rejected"

# Ticket/Complaint Statuses
TICKET_OPEN = "Open"
TICKET_RESOLVED = "Resolved"


# --- New Feature: Grouped Status Classes ---
# These classes are required for the new 6-tile real-time dashboard logic.

class OrderStatus:
    """Grouped order statuses for dashboard filtering and tracking."""
    PENDING = "Pending"
    SHIPPED = "Shipped"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"

class PaymentStatus:
    """Payment lifecycle statuses for financial metrics."""
    PENDING = "Pending"
    ESCROW = "Escrow"      # Payment held by platform
    RELEASED = "Released"  # Payment added to seller's wallet balance
    REFUNDED = "Refunded"