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

def parse_yatri(body):
    if not body or "ORDER No" not in body or "Grand Total" not in body:
        return None

    try:
        item_lines = []
        item_description_lines = []

        # Extract item table section
        item_section = extract(
            r'Order Item Details:\s*Item\s+Description\s+Price\s+Quantity\s+Amount\s*(.*?)\s*Sub Total',
            body, multiline=True
        )

        if item_section:
            for line in item_section.strip().splitlines():
                # Match: Name, Description, Price, Quantity, Amount
                match = re.match(
                    r'^([A-Za-z0-9 \-]+)\s+([\d\w]+)\s+₹\s*([\d.]+)\s+(\d+)\s+₹\s*([\d.]+)',
                    line.strip()
                )
                if match:
                    item_name = match.group(1).strip()
                    description = match.group(2).strip()
                    quantity = match.group(4).strip()
                    item_lines.append(f"{item_name} × {quantity}")
                    item_description_lines.append(f"{item_name} ({description})")

        sub_total = float_or_none(extract(r'Sub Total\s+₹\s*([\d.]+)', body))
        gst = float_or_none(extract(r'GST\s+₹\s*([\d.]+)', body))
        grand_total = float_or_none(extract(r'Grand Total \(Inclusive of all taxes\)\s+₹\s*(\d+)', body))

        return {
            'Order_No': extract(r'ORDER No\s+(\S+)', body),
            'Mobile_No': extract(r'MOBILE NO\s+(\d+)', body),
            'Customer_Name': extract(r'CUSTOMER NAME\s+(.+?)(?:TRAIN No /NAME|\n|$)', body, True),
            'Train_No_Name': extract(r'TRAIN No /NAME\s+(.+?)(?:\n|$)', body, True),
            'Train_No': extract_train_number_first(body),
            'Delivery_Date': extract(r'DELIVERY DATE\s+(.+?)(?:\n|$)', body, True),
            'Coach': extract(r'COACH/BERTH\s+(.+?)(?:\n|$)', body, True),
            'Station': extract(r'Station Code/Name\s+(.+?)(?:\n|$)', body, True),
            'Pay_Mode': extract(r'PAYMENT STATUS\s+(.+?)(?:Station Code/Name|\n|$)', body, True),
            'Item_Details': "\n".join(item_lines) if item_lines else None,
            'Item_Description': "\n".join(item_description_lines) if item_description_lines else None,
            'Sub_Total': sub_total,
            'GST': gst,
            'Delivery_Charges': 0,
            'Grand_Total': grand_total
        }

    except Exception as e:
        print(f"❌ Yatri Parsing error: {e}")
        return None

           
