import uiautomator2 as u2
import time
import os
import sys
# from dotenv import load_dotenv

# load_dotenv()

EMAIL  = os.getenv("INVESTIFY_EMAIL")
PASS   = os.getenv("INVESTIFY_PASS")
# SMS_TO = os.getenv("CONFIRM_SMS_TO", "+923135595352")


try:
    d = u2.connect()
except Exception as e:
    print("[-] Device not connected or uiautomator2 error:", e)
    sys.exit(1)

try:
    # Restart Investify App
    d.app_stop("com.blueinklabs.investifystocks.free")
    d.app_start("com.blueinklabs.investifystocks.free")
    time.sleep(5)

    if d(text="Login").exists:
        print("[*] Login screen found, proceeding with login...")
        d(text="Login").click()
        time.sleep(5)

        if d(text="Enter Email").exists:
            d(text="Enter Email").set_text(EMAIL)
            time.sleep(0.5)

            if d(text="Password").exists:
                d(text="Password").set_text(PASS)
                time.sleep(0.5)

                d.press("back")
                time.sleep(0.5)

                if d(text="Sign In").exists:
                    d(text="Sign In").click()
                    time.sleep(8)
                else:
                    raise Exception("Sign In button not found")
            else:
                raise Exception("Password field not found")
        else:
            raise Exception("Email field not found")

    else:
        print("[*] Login screen not found — assuming already logged in.")
        pass

    # Check for successful login
    if d(text="Portfolio").exists or d(text="Market").exists or d(text="Watchlist").exists:
        print("[+] Login successful, sending SMS...")

        # Open SMS App
        os.system("adb shell am start -a android.intent.action.SENDTO -d sms:+923135595352")
        time.sleep(5)

        # Tap on input area
        os.system("adb shell input tap 170 2150")
        time.sleep(2)

        # Input text char by char
        message = "Investify login"
        for char in message:
            if char == " ":
                os.system("adb shell input keyevent 62")
            else:
                os.system(f"adb shell input text \"{char}\"")
            time.sleep(0.1)

        d.press("back")
        time.sleep(5)

        # Tap Send
        os.system("adb shell input tap 972 2083")
        print("[+] SMS Sent successfully.")

        # Bring back Investify app
        os.system("adb shell am start -n com.blueinklabs.investifystocks.free/com.blueinklabs.investifystocks.activities.authenticator.SplashActivity")
        print("[+] Investify app brought back to front.")

    else:
        raise Exception("Login failed or Portfolio/Home screen not loaded. Check Internet or App status.")

except Exception as e:
    print("[-] ERROR:", e)

print("[*] Process Completed.")
