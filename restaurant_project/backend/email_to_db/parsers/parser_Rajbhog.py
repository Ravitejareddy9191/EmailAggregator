import re

def extract(pattern, text, multiline=False):
    flags = re.DOTALL if multiline else 0
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None

def float_or_none(val):
    try:
        return float(val.replace(',', '').strip()) if val else None
    except:
        return None

def extract_train_number_first(text):
    match = re.search(r'\b\d{4,5}\b', text)
    return match.group(0) if match else None

def parse_Rajbhog(body):
    if not body or "Invoice" not in body or "Customer Name" not in body:
        return None

    try:
        item_lines = []
        item_description_lines = []

        # ✔️ Flexible pattern for line with item
        item_match = re.search(
            r'1\s+(.+?)\s+(.+?)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',
            body
        )

        if item_match:
            item_name = item_match.group(1).strip()
            description = item_match.group(2).strip()
            qty = item_match.group(3).strip()
            item_lines.append(f"{item_name} × {qty}")
            item_description_lines.append(f"{item_name} ({description})")

        return {
            'Order_No': extract(r'Invoice\s+(\S+ / \d+)', body),
            'Mobile_No': extract(r'Customer Contact\s*:\s*(\d+)', body),
            'Customer_Name': extract(r'Customer Name\s*:\s*(.+)', body),
            'Train_No_Name': extract(r'Train\s*:\s*(.+)', body),
            'Train_No': extract_train_number_first(body),
            'Delivery_Date': extract(r'Delivery Date\s*:\s*(.+)', body),
            'Coach': extract(r'Coach / Berth:\s*(.+)', body),
            'Station': extract(r'Delivery Station:\s*(.+)', body),
            'Pay_Mode': extract(r'Payment:\s*(\S+)', body),
            'Item_Details': "\n".join(item_lines) if item_lines else None,
            'Item_Description': "\n".join(item_description_lines) if item_description_lines else None,
            'Sub_Total': float_or_none(extract(r'Subtotal:\s*([\d.]+)', body)),
            'GST': float_or_none(extract(r'GST\s*\(5%\)\s*([\d.]+)', body)),
            'Delivery_Charges': 0.0,
            'Grand_Total': float_or_none(extract(r'Total:\s*([\d.]+)', body))
        }

    except Exception as e:
        print(f"❌ Rajbhog Khana Parsing error: {e}")
        return None

