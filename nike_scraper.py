import pandas as pd
from seleniumbase import sb_cdp
import datetime

url = "https://www.nike.com/"
sb = sb_cdp.Chrome(url)
sb.sleep(1.2)

try:
    sb.click('[data-testid="user-tools-container"] search')
except:
    sb.click('button[data-var="searchIcon"]')
    
sb.sleep(1)
search = "Pegasus"
sb.press_keys('input[type="search"]', search)
sb.sleep(4)

details = 'ul[data-testid*="products"] figure .details'
elements = sb.select_all(details)

# Create a list to store product data
products = []

if elements:
    print('**** Found results for "%s": ****' % search)
    for idx, element in enumerate(elements, 1):
        product_text = element.text
        print(f"{idx}. {product_text}")
        
        # Split text into parts
        lines = product_text.split('\n')
        
        # Add to products list
        products.append({
            "S.No": idx,
            "Product Name": lines[0] if len(lines) > 0 else product_text,
            "Price": lines[1] if len(lines) > 1 else "N/A",
            "Details": lines[2] if len(lines) > 2 else "N/A"
        })

# Export to Excel
if products:
    df = pd.DataFrame(products)
    df.to_excel(f"nike_{search}_results.xlsx", index=False)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n✅ Results exported to: nike_{search}_{timestamp}results.xlsx")
else:
    print("❌ No products found.")
    
    # Create empty Excel file
    df = pd.DataFrame(columns=["Search Term", "Status", "Timestamp"])
    df = pd.concat([df, pd.DataFrame([{
        "Search Term": search,
        "Status": "No products found",
        "Timestamp": pd.Timestamp.now()
    }])], ignore_index=True)
    df.to_excel(f"nike_{search}_no_results.xlsx", index=False)

sb.driver.stop()