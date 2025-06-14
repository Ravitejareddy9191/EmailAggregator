from gmail_service import get_gmail_service
from database import connect_db, setup_orders_table
from parsers.parser_zoop import parse_zoop
from parsers.parser_Spicy import parse_Spicy
from parsers.parser_yatri import parse_yatri
from parsers.parser_Rajbhog import parse_Rajbhog
from base64 import urlsafe_b64decode
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def identify_platform(body):
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
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                return urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    else:
        data = payload['body']['data']
        return urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ""

def main():
    db, cursor = connect_db()
    setup_orders_table(cursor)
    service = get_gmail_service()
    messages = service.users().messages().list(userId='me', maxResults=100).execute().get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data['payload']
        headers = payload['headers']

        email_date = None
        sender = None
        for header in headers:
             if header['name'].lower() == 'date':
                email_date = header['value']
             elif header['name'].lower() == 'from':
                sender = header['value']
        body = get_email_body(payload)
        platform = identify_platform(body)

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

        cursor.execute("""
            INSERT INTO orders_order (
                email_date, sender, Order_No, Customer_Name,
                Mobile_No, Item_Details, Item_Description,
                Sub_Total, Delivery_Charges, GST, Grand_Total,
                Pay_Mode, Delivery_Date, Station, Train_No_Name, Coach, subject
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            email_date, sender ,  order.get('Order_No'), order.get('Customer_Name'),
            order.get('Mobile_No'), order.get('Item_Details'), order.get('Item_Description'),
            order.get('Sub_Total'), order.get('Delivery_Charges'), order.get('GST'),
            order.get('Grand_Total'), order.get('Pay_Mode'), order.get('Delivery_Date'),
            order.get('Station'), order.get('Train_No_Name'), order.get('Coach'), "Fetched from Gmail"
        ))
        db.commit()

    cursor.close()
    db.close()
if __name__ == '__main__':
    main()
