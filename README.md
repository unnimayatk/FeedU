# FeedU  

**FeedU** is an Online College Canteen Management System built with **Python (Django)** and **MySQL**.  
It helps students easily browse the menu, place orders, and track delivery, while canteen staff can efficiently manage menus and process orders.  

---

## 🚀 Features  

✅ **Role-based Access**  
- **Students** → View menu, add to cart, place & track orders  
- **Canteen Staff** → Manage menu, view orders, update delivery status  
- **Admin** → Monitor system & manage users  

✅ **Order Management**  
- Live menu updates with prices  
- Cart & checkout system  
- Real-time order status tracking  

✅ **Payment & Notifications**  
- Cash or online payment options  
- Email/SMS notifications for order updates  

✅ **Other Highlights**  
- Clean, mobile-friendly UI with Bootstrap  
- Simple backend logic for easy maintenance  

---

## 🛠 Tech Stack  

- **Backend:** Python (Django)  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** MySQL  
- **Version Control:** Git & GitHub  

---

## ⚙️ Installation  

Follow these steps to run **FeedU** locally:  

```bash
# Clone the repository
git clone https://github.com/unnimayatk/FeedU.git

# Go into the project folder
cd FeedU

# Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # For Windows
source venv/bin/activate # For Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Run the development server
python manage.py runserver
