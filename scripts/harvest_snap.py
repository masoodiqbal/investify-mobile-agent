import uiautomator2 as u2
import time
import json
import os
from datetime import datetime

def save_data(indices, output_dir="output"):
    """Save data to JSON file with proper path handling"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"investify_market_data_{timestamp}.json")
    
    try:
        with open(filename, 'w') as f:
            json.dump(indices, f, indent=2)
        print(f"✅ Saved {len(indices)} market indices to {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to save data: {e}")
        # Fallback - print to console
        print("Data extracted:")
        for idx in indices:
            print(json.dumps(idx))
        return False

def extract_market_data(d):
    """Extract market data with improved scrolling and error handling"""
    indices = []
    captured_codes = set()
    max_scrolls = 5
    scroll_count = 0
    
    while scroll_count < max_scrolls:
        try:
            # Get all market index items
            items = d(resourceId="com.blueinklabs.investifystocks.free:id/main_layout_watchlist")
            
            if not items.exists:
                print("No market items found on this screen")
                break
            
            print(f"Found {items.count} market indices on screen {scroll_count + 1}")
            
            for i in range(items.count):
                try:
                    item = items[i]
                    
                    # Extract index code
                    code_element = item.child(resourceId="com.blueinklabs.investifystocks.free:id/symbol_in_watchlist")
                    if not code_element.exists:
                        continue
                    
                    index_code = code_element.get_text()
                    if index_code in captured_codes:
                        continue
                    
                    # Extract other data with fallbacks
                    index_data = {
                        "index_code": index_code,
                        "index_description": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/company_name"
                        ).get_text() if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/company_name"
                        ).exists else "",
                        "current": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/current_price"
                        ).info.get('contentDescription', '') if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/current_price"
                        ).exists else "",
                        "high": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/high_value"
                        ).get_text() if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/high_value"
                        ).exists else "",
                        "low": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/low_value"
                        ).get_text() if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/low_value"
                        ).exists else "",
                        "volume": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/volume_value"
                        ).get_text() if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/volume_value"
                        ).exists else "",
                        "value": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/value_value"
                        ).get_text() if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/value_value"
                        ).exists else "",
                        "change": item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/change_value"
                        ).get_text() if item.child(
                            resourceId="com.blueinklabs.investifystocks.free:id/change_value"
                        ).exists else "",
                    }
                    
                    # Only add if we have meaningful data
                    if index_data["current"]:
                        indices.append(index_data)
                        captured_codes.add(index_code)
                        print(f"Extracted: {index_code} - {index_data['current']}")
                    
                except Exception as e:
                    print(f"Error extracting item {i}: {str(e)}")
                    continue
            
            # Check if we need to scroll for more items
            if len(captured_codes) >= 18:  # We know there are 13 indices
                break
                
            # Scroll to next page
            d(scrollable=True).scroll.forward()
            scroll_count += 1
            time.sleep(2)
            
        except Exception as e:
            print(f"Error during scrolling/extraction: {str(e)}")
            break
    
    return indices

def main():
    # Connect to device
    d = u2.connect()
    
    try:
        # Launch Investify app
        print("Launching Investify...")
        d.app_start("com.blueinklabs.investifystocks.free")
        time.sleep(5)
        
        # Navigate to Market tab
        print("Navigating to Market tab...")
        if d(text="Market").exists():
            d(text="Market").click()
        else:
            print("Market tab not found, trying bottom navigation...")
            d.click(0.5, 0.95)  # Try clicking bottom center of screen
        time.sleep(3)
        
        # Main scraping logic
        print("Starting market data extraction...")
        indices = extract_market_data(d)
        
        # Save results
        if indices:
            save_data(indices)
        else:
            print("❌ No market indices found")
            
    finally:
        # Close the app
        d.app_stop("com.blueinklabs.investifystocks.free")
        print("Scraping completed")

if __name__ == "__main__":
    main()