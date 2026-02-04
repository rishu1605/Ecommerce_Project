💎 SIC Mart: Premium Escrow Marketplace
SIC Mart is a high-security, three-tier marketplace built with Python, Streamlit, and SQLite. It features an Atomic Architecture where the Buyer, Seller, and Admin modules operate independently but share a centralized database and security protocol.

🎨 Design Philosophy
Buyer Portal: Sapphire Blue & Silver (Trust, Security, Calm).

Seller Portal: Rose Gold & Charcoal (Premium, Business-centric).

Admin Terminal: Gold & Midnight Navy (Authority, Oversight).

📁 Project Structure
Plaintext
sic_mart/
├── main.py                 # Root Entry Point (Portal Selector)
├── database.py             # Single Source of Truth (SQLite)
├── common/                 # Shared Utilities
│   ├── auth_utils.py       # Password Hashing & Session Checks
│   ├── theme.py            # Global CSS Injection
│   └── status_codes.py     # Shared Order/Payment Statuses
├── buyer/                  # BUYER MODULE
│   ├── buyer_main.py       # Buyer Controller
│   ├── auth/               # Login & Registration
│   ├── home/               # Marketplace Product Grid
│   ├── cart/               # Persistent Database-backed Cart
│   ├── wallet/             # Sapphire Wallet (Escrow Funding)
│   ├── orders/             # Order Tracking & History
│   └── support/            # Ticket Raising System
├── seller/                 # SELLER MODULE
│   ├── seller_main.py      # Seller Controller
│   ├── inventory/          # Product Management
│   ├── sales/              # Order Fulfillment & Tracking
│   └── support/            # Forwarded Ticket Management
└── admin/                  # ADMIN MODULE
    ├── admin_main.py       # Admin Master Controller
    ├── analytics/          # Sales & Escrow Visualizations
    ├── catalog/            # Catalog Audit & Oversight
    ├── finance/            # Escrow Release & Commissions
    ├── tracking/           # Global Logistics Control Tower
    ├── users/              # Seller Verification (PAN/GST)
    └── support/            # Complaint Audit & Forwarding
🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.8+ installed.

2. Install Dependencies
Bash
pip install streamlit pandas
3. Running the App
From the root directory, run:

Bash
streamlit run main.py
4. Initial Admin Access
The system automatically seeds a default administrator on the first run:

Admin ID: admin

Password: admin123

🛠️ Core Features
🔒 Escrow Security
Funds move from the Buyer Wallet into a system-wide Escrow Pool. Money is only released to the Seller after the Admin or Buyer marks the item as Delivered.

🛒 Persistent Shopping
The Shopping Cart is backed by the database. Items added on one device will remain in the cart even after logging out, linked to the buyer_id.

📑 Support Forwarding
Buyer raises a ticket regarding an order.

Admin reviews the ticket in the Audit Hub.

Admin adds instructions and Forwards it to the specific Seller.

Seller resolves the issue to ensure the Escrow is released.

📈 Logistics Tower
Admin and Sellers share a real-time tracking system. Status updates (Pending -> Shipped -> Delivered) trigger the financial logic automatically.

🛡️ Security Note
Role-Based Access Control (RBAC): Every page check verifies st.session_state.role.

Input Sanitization: Uses SQLite parameterization to prevent SQL Injection.

Admin Privacy: No public registration for Admins; accounts must be seeded by existing administrators.

