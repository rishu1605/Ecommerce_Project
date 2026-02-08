import streamlit as st
import database as db
from common.status_codes import OrderStatus, PaymentStatus

# 1. HELPER: Play Notification Sound (JS Injection)
def play_notification_sound():
    """Injects a hidden audio element to play a chime when a new order arrives."""
    sound_html = """
    <audio autoplay>
        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    """
    st.components.v1.html(sound_html, height=0)

# 2. DATA FETCHER: Core Business Logic (Corrected for your DB Schema)
def get_6_tile_metrics(seller_id):
    """Fetches data for the 6 dashboard tiles with precise SQL aliasing and CAST for ID matching."""
    try:
        s_id = str(seller_id) # Convert to string for consistent CAST matching
        
        # 1. Total Revenue (Delivered Orders)
        rev = db.fetch_query("""
            SELECT SUM(amount) as val FROM orders 
            WHERE CAST(seller_id AS TEXT) = ? AND status = 'Delivered'
        """, (s_id,))
        
        # 2. Escrow Balance (Confirmed or Shipped)
        esc = db.fetch_query("""
            SELECT SUM(amount) as val FROM orders 
            WHERE CAST(seller_id AS TEXT) = ? AND status IN ('Confirmed', 'Shipped')
        """, (s_id,))
        
        # 3. Active Shipments (Status is Shipped)
        ship = db.fetch_query("""
            SELECT COUNT(*) as val FROM orders 
            WHERE CAST(seller_id AS TEXT) = ? AND status = 'Shipped'
        """, (s_id,))
        
        # 4. Live Products (Approved & In Stock)
        prod = db.fetch_query("""
            SELECT COUNT(*) as val FROM products 
            WHERE CAST(seller_id AS TEXT) = ? AND stock > 0
        """, (s_id,))
        
        # 5. New Orders (Confirmed orders that haven't been shipped yet)
        pending = db.fetch_query("""
            SELECT COUNT(*) as val FROM orders 
            WHERE CAST(seller_id AS TEXT) = ? AND status = 'Confirmed'
        """, (s_id,))
        
        # 6. Returns/Disputes
        dispute = db.fetch_query("""
            SELECT COUNT(*) as val FROM orders 
            WHERE CAST(seller_id AS TEXT) = ? AND status = 'Returned'
        """, (s_id,))

        return {
            "Revenue": rev.iloc[0]['val'] or 0.0,
            "Escrow": esc.iloc[0]['val'] or 0.0,
            "Shipments": ship.iloc[0]['val'] or 0,
            "Live Products": prod.iloc[0]['val'] or 0,
            "New Orders": pending.iloc[0]['val'] or 0,
            "Returns": dispute.iloc[0]['val'] or 0
        }
    except Exception as e:
        print(f"Dashboard Fetch Error: {e}")
        return {"Revenue": 0.0, "Escrow": 0.0, "Shipments": 0, "Live Products": 0, "New Orders": 0, "Returns": 0}

# 3. FRAGMENT: Real-time update logic
@st.fragment(run_every=10)
def refreshable_dashboard_content(seller_id):
    metrics = get_6_tile_metrics(seller_id)
    
    # Fetch Recent Activity for the table (Using CAST to ensure match)
    recent = db.fetch_query("""
        SELECT product_name as 'Product', amount as 'Amount', status as 'Status', date as 'Date' 
        FROM orders WHERE CAST(seller_id AS TEXT) = ? ORDER BY date DESC LIMIT 5
    """, (str(seller_id),))

    # Notification Logic: Detect New Orders
    if "last_order_count" not in st.session_state:
        st.session_state.last_order_count = metrics["New Orders"]

    if metrics["New Orders"] > st.session_state.last_order_count:
        st.toast(f"🔔 New Order Received!", icon="💰")
        play_notification_sound()
    
    # Sync the count for the next refresh cycle
    st.session_state.last_order_count = metrics["New Orders"]

    # --- UI: Row 1 ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"₹{metrics['Revenue']:,.2f}")
    with col2:
        st.metric("Pending Payout (Escrow)", f"₹{metrics['Escrow']:,.2f}")
    with col3:
        st.metric("New Orders", metrics["New Orders"], 
                  delta=f"{metrics['New Orders']} Pending" if metrics["New Orders"] > 0 else None)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- UI: Row 2 ---
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Active Shipments", metrics["Shipments"])
    with col5:
        st.metric("Live Products", metrics["Live Products"])
    with col6:
        st.metric("Returns/Disputes", metrics["Returns"])

    st.markdown("<br>---")
    
    # --- TABLE SECTION ---
    st.subheader("Recent Sales Activity")
    if recent.empty:
        st.info("No sales yet. Once customers buy your products, they'll show up here!")
    else:
        st.dataframe(
            recent, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn("Amount (₹)", format="%.2f"),
                "Status": st.column_config.SelectboxColumn( # Corrected from BadgeColumn
                    "Status",
                    options=["Pending", "Confirmed", "Shipped", "Delivered", "Returned"],
                )
            }
        )

# 4. PAGE RENDERER
def render_seller_dashboard():
    # Inject Professional Dashboard CSS
    st.markdown("""
        <style>
            .dashboard-title { color: #1E1E1E; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px; }
            .sync-text { color: #2563eb; font-size: 0.85rem; font-weight: 600; margin-bottom: 25px; }
            [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.95rem !important; font-weight: 600 !important; }
            [data-testid="stMetricValue"] { color: #0f172a !important; font-size: 1.8rem !important; font-weight: 800 !important; }
            
            /* Metric Card Styling */
            div[data-testid="stHorizontalBlock"] > div {
                background: #ffffff;
                padding: 24px;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
                border: 1px solid #f1f5f9;
                transition: transform 0.2s ease;
            }
            div[data-testid="stHorizontalBlock"] > div:hover {
                transform: translateY(-5px);
                border-color: #2563eb;
            }
        </style>
    """, unsafe_allow_html=True)

    # User Resolution
    seller_id = st.session_state.user_data.get('user_id') or st.session_state.user_data.get('id')
    user_name = st.session_state.user_data.get('name', 'Seller')
    
    # UI Header
    st.markdown(f"<div class='dashboard-title'>Welcome back, {user_name}!</div>", unsafe_allow_html=True)
    st.markdown("<div class='sync-text'>📡 Live Dashboard Sync Active</div>", unsafe_allow_html=True)

    # Run the Auto-refreshing fragment
    refreshable_dashboard_content(seller_id)

    # Footer Actions
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Manual Refresh", type="secondary", use_container_width=True):
        st.rerun()