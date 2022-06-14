# OTP Generator
**This generates otp codes alike Google Authenticator**

**How to**

Create a codes.json file with contents like

    [
        "otpauth://totp/<Website>:<Account>?secret=<secretkey>",
        "otpauth://totp/<Website>:<Account>?secret=<secretkey>"
    ]

**Limitations**
- All codes are generated at same interval (30 secs)
- If the number of codes generated are more than screenful, previous lines aren't overwritten
- If the window is resized, previous dirt may not be removed
