import re

def extract(pattern, text, multiline=False):
    flags = re.DOTALL if multiline else 0
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None

def float_or_none(val):
    try:
        return float(val) if val is not None else None
    except:
        return None

def parse_Spicy(body):
    if not body or "ORDER NO:" not in body or "NET TOTAL" not in body:
        return None

    expected_fields = [
        'Order_No', 'Mobile_No', 'Customer_Name', 'Train_No',
        'Delivery_Date', 'Coach', 'Pay_Mode', 'Station',
        'Item_Details', 'Grand_Total'
    ]

    try:
        parsed_order = {
            'Order_No': extract(r'ORDER NO:\s+(\S+)', body),
            'Mobile_No': extract(r'MOB:\s+(\d+)', body),
            'Customer_Name': extract(r'NAME:\s+(.+?)(?:TRAIN No /NAME|\n|$)', body, True),
            'Train_No_Name': extract(r'TRAIN:\s+(.+?)(?:\n|$)', body, True),
            'Delivery_Date': extract(r'DELIVERY:\s*(.+)', body),
            'Coach': extract(r'COACH:\s+(.+?)(?:\n|$)', body, True),
            'Pay_Mode': extract(r'PAYMODE:\s+(.+?)(?:Station Code/Name|\n|$)', body, True),
            'Station': extract(r'STATION:\s+(.+?)(?:\n|$)', body, True),
            'Item_Details': extract(r'ITEM DETAILS\s*\*+\s*(.*?)\s*DELIVERY CHARGE:', body, multiline=True),
            'Item_Description': extract(r'ITEM DETAILS\s*\*+\s*(.*?)\s*DELIVERY CHARGE:', body, multiline=True),
            'Delivery_Charges' : extract(r'DELIVERY CHARGE:\s*Rs\.?\s*(\d+(?:\.\d+)?)', body),
            'Sub_Total': float_or_none(extract(r'NET TOTAL:\s*Rs\.?\s*(\d+(?:\.\d+)?)', body)),
            'Grand_Total': float_or_none(extract(r'NET TOTAL:\s*Rs\.?\s*(\d+(?:\.\d+)?)', body))
        }

        # Fill in missing fields with None
        for field in expected_fields:
            if field not in parsed_order:
                parsed_order[field] = None

        return parsed_order

    except Exception as e:
        print(f"❌ Parsing error: {e}")
        return None

