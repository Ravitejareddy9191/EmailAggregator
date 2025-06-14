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

def extract_train_number_first(text):
    """Extract the first 4–5 digit number, assuming it's the train number"""
    match = re.search(r'\b\d{4,5}\b', text)
    return match.group(0) if match else None

def parse_zoop(body):
    if not body or "Order Number" not in body or "Order Total" not in body:
        return None

    expected_fields = [
        'Order_No', 'Mobile_No', 'Customer_Name', 'Train_No',
        'Delivery_Date', 'Coach', 'Pay_Mode', 'Station',
        'Item_Details', 'Grand_Total'
    ]

    try:
        # Extract values before putting them into the dict
        sub_total = float_or_none(extract(r'Base Price Total\s*₹\s*(\d+\.?\d*)', body))
        gst_food = float_or_none(extract(r'\(\+\) GST on food\s*₹\s*(\d+\.?\d*)', body))
        gst_delivery = float_or_none(extract(r'\(\+\) GST on Delivery Charge\s*₹\s*(\d+\.?\d*)', body))
        delivery_charge = float_or_none(extract(r'\(\+\) Delivery Charge\s*₹\s*(\d+\.?\d*)', body))
        grand_total = float_or_none(extract(r'Order Total\s*₹\s*(\d+\.?\d*)', body))

        # Combine GST if any present
        gst_total = None
        if gst_food is not None or gst_delivery is not None:
            gst_total = (gst_food or 0) + (gst_delivery or 0)

        # Main parsed order dictionary
        parsed_order = {
            'Order_No': extract(r'Order Number\s*(ZO\d+)', body),
            'Mobile_No': extract(r'Phone\s*\*:\s*\*(\d+)', body),
            'Customer_Name': extract(r'Customer Name\s*\*:\s*\*(.+?)(?=\s*Phone\s*\*:)', body),
            'Train_No_Name': extract(r'Train.*?:\s*(.+)', body),
            'Train_No': extract_train_number_first(body),
            'Delivery_Date': extract(r'Delivery Date\s*\*:\s*\*([^\n\r]+)', body),
            'Coach': extract(r'Coach/ Seat\s*\*:\s*\*([^\n\r]+)', body),
            'Station': extract(r'At\s*\*:\s*\*([^\n\r]+?/\s*\w{2,5})', body),
            'Pay_Mode': extract(r'(Paid Online|Cash on Delivery)', body),
            'Item_Description': extract(r'\*Item Description:\*\s*Item Name Description\s*(.+?)\*Restaurant Details:', body, multiline=True),
            'Sub_Total': sub_total,
            'GST': gst_total,
            'Delivery_Charges': delivery_charge,
            'Grand_Total': grand_total
        }

        # Extract item name + quantity from tabular data
        items = re.findall(r'([A-Za-z0-9 \-]+?)\s+\d+\s+(\d+)\s+\d+', body)
        item_lines = [f"{name.strip()} × {qty}" for name, qty in items]
        parsed_order['Item_Details'] = "\n".join(item_lines) if item_lines else None

        # Ensure all expected fields exist
        for field in expected_fields:
            if field not in parsed_order:
                parsed_order[field] = None

        return parsed_order

    except Exception as e:
        print(f"❌ Zoop Parsing error: {e}")
        return None

