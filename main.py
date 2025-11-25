import os
import sys
import time
from django.core.management import execute_from_command_line

def main():
    # ১. সেটিংস লোকেশন চিনিয়ে দেওয়া
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mygrocery.settings')

    # ২. জ্যাঙ্গো সেটআপ করা (মাইগ্রেশন কমান্ড চালানোর জন্য জরুরি)
    import django
    django.setup()
    
    from django.core.management import call_command

    print("Checking Database Migrations... (Please wait)")
    
    # ৩. অটোমেটিক মাইগ্রেশন চালানো (যাতে শেল এ কমান্ড দেওয়া না লাগে)
    try:
        # 'store' অ্যাপের চেঞ্জগুলো ডিটেক্ট করা
        call_command('makemigrations', 'store')
        # ডাটাবেস আপডেট করা
        call_command('migrate')
    except Exception as e:
        print(f"Migration Warning: {e}")

    # ৪. সার্ভার রান করা (Replit এর জন্য 0.0.0.0 পোর্টে চালাতে হয়)
    print("Starting Server on Replit...")
    
    # Replit সাধারণত পোর্ট 8000 বা 8080 তে চলে। আমরা 0.0.0.0 তে বাইন্ড করছি।
    # sys.argv কে ম্যানুয়ালি সেট করে দিচ্ছি যাতে runserver কমান্ড রান হয়।
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
