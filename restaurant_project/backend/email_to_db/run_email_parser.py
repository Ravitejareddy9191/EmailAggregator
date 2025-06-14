# restaurant_project/backend/email_to_db/run_email_parser.py
import os
import sys
import django

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from gmail_service import get_gmail_service
from parsers.parser_zoop import parse_zoop
from parsers.parser_Spicy import parse_Spicy
from parsers.parser_yatri import parse_yatri
from parsers.parser_Rajbhog import parse_Rajbhog
from base64 import urlsafe_b64decode
from django.contrib.auth.models import User
from orders.models import Order
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def identify_platform(body):
    """Identify which platform the email is from"""
    if "Order Number" in body and "ZO" in body:
        return 'zoop'
    elif "ORDER NO:" in body:
        return 'spicy'
    elif "ORDER No" in body and "MOBILE NO" in body:
        return 'yatri'
    elif "Invoice" in body:
        return 'Rajbhog'
    return None

def get_email_body(payload):
    """Extract email body from Gmail API payload"""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                return urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    else:
        data = payload['body']['data']
        return urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ""

def get_user_by_email(email):
    """Get user by email address"""
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def parse_orders_for_user(user_email):
    """Parse orders for a specific user"""
    try:
        user = get_user_by_email(user_email)
        if not user:
            logging.error(f"User with email {user_email} not found")
            return

        # Get Gmail service with user's credentials
        service = get_gmail_service()
        
        # Get recent messages (last 100)
        messages = service.users().messages().list(
            userId='me', 
            maxResults=100,
            q='from:(spicywagon OR yatrirestro OR rajbhogkhana OR zoop)'  # Filter by known senders
        ).execute().get('messages', [])

        processed_count = 0
        
        for msg in messages:
            try:
                msg_data = service.users().messages().get(
                    userId='me', 
                    id=msg['id'], 
                    format='full'
                ).execute()
                
                payload = msg_data['payload']
                headers = payload['headers']

                # Extract email metadata
                email_date = None
                sender = None
                subject = None
                
                for header in headers:
                    if header['name'].lower() == 'date':
                        email_date = header['value']
                    elif header['name'].lower() == 'from':
                        sender = header['value']
                    elif header['name'].lower() == 'subject':
                        subject = header['value']

                body = get_email_body(payload)
                platform = identify_platform(body)

                if not platform:
                    continue

                # Parse based on platform
                if platform == 'zoop':
                    order = parse_zoop(body)
                elif platform == 'spicy':
                    order = parse_Spicy(body)
                elif platform == 'yatri':
                    order = parse_yatri(body)
                elif platform == 'Rajbhog':
                    order = parse_Rajbhog(body)
                else:
                    continue

                if not order:
                    continue

                # Check if order already exists
                if Order.objects.filter(
                    user=user,
                    Order_No=order.get('Order_No')
                ).exists():
                    continue

                # Create order linked to user
                Order.objects.create(
                    user=user,
                    email_date=email_date,
                    sender=sender,
                    Order_No=order.get('Order_No'),
                    Customer_Name=order.get('Customer_Name'),
                    Mobile_No=order.get('Mobile_No'),
                    Item_Details=order.get('Item_Details'),
                    Item_Description=order.get('Item_Description'),
                    Sub_Total=order.get('Sub_Total'),
                    Delivery_Charges=order.get('Delivery_Charges'),
                    GST=order.get('GST'),
                    Grand_Total=order.get('Grand_Total'),
                    Pay_Mode=order.get('Pay_Mode'),
                    Delivery_Date=order.get('Delivery_Date'),
                    Station=order.get('Station'),
                    Train_No_Name=order.get('Train_No_Name'),
                    Coach=order.get('Coach'),
                    subject=subject or "Order Email",
                    platform=platform
                )
                
                processed_count += 1
                logging.info(f"Processed order {order.get('Order_No')} for user {user.email}")

            except Exception as e:
                logging.error(f"Error processing message: {e}")
                continue

        logging.info(f"Processed {processed_count} orders for user {user.email}")

    except Exception as e:
        logging.error(f"Error in parse_orders_for_user: {e}")

def main():
    """Main function - for testing purposes"""
    # This would typically be called from a management command or API endpoint
    # For now, you can specify a test email
    test_email = "test@example.com"  # Replace with actual user email
    parse_orders_for_user(test_email)

if __name__ == '__main__':
    main()