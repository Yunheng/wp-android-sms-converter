# Windows Phone to Android SMS / MMS Converter
The application is currently one way only (Windows Phone -> Android)

# Requirements

Windows Phone Application: https://www.microsoft.com/en-us/store/apps/contacts-message-backup/9nblgggz57gm
Android Application: https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en

# Usage

Extract the .msg file from your smsBackup folder on the Windows Phone
python wpsms.py <input file from Windows Phone, ending with .msg> <output file for Android Phone, ending with .xml>
Import the .xml file onto your Android phone and use the SMS Backup and Restore application to restore the mesages

# To-Do

Implement MMS Support (the problem is the Android end)
Android to WP Support
