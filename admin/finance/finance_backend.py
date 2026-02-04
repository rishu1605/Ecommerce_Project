import database as db
from common.status_codes import PaymentStatus

def get_financial_overview():
    """Returns separate dataframes for Escrow, Released, and Refunded transactions."""
    escrow = db.fetch_query("SELECT * FROM payments WHERE status = ?", (PaymentStatus.ESCROW,))
    released = db.fetch_query("SELECT * FROM payments WHERE status = ?", (PaymentStatus.RELEASED,))
    refunds = db.fetch_query("SELECT * FROM payments WHERE status = ?", (PaymentStatus.REFUNDED,))
    
    return escrow, released, refunds

def release_funds_to_seller(order_id):
    """
    Executes the final payout.
    Updates the payment status to 'Released' and logs the transaction.
    """
    db.execute_query("""
        UPDATE payments 
        SET status = ?, processed_at = CURRENT_TIMESTAMP 
        WHERE order_id = ?
    """, (PaymentStatus.RELEASED, order_id))
    return True