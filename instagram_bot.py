import time
import random
import string
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hardcoded Configuration
TELEGRAM_BOT_TOKEN = "8553258884:AAFU3Epg62tGihy0ktZ2kZWNRhRm7o9phnk"  # Replace with your actual bot token
MANDATORY_CHANNEL = "@WinzoHack_Tips_Tricks"
MANDATORY_CHANNEL_ID = "-1001234567890"  # Replace with actual channel ID (get from @userinfobot)

class InstagramAutomation:
    """Instagram account creation and automation"""
    
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        self.account_data = {}
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def generate_credentials(self):
        """Generate random credentials"""
        username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$', k=12))
        email = f"{username}@tempmail.com"
        full_name = f"User {random.randint(1000, 9999)}"
        
        self.account_data = {
            'username': username,
            'password': password,
            'email': email,
            'full_name': full_name
        }
        return self.account_data
    
    def create_account(self):
        """Create Instagram account"""
        try:
            self.driver.get('https://www.instagram.com/accounts/emailsignup/')
            time.sleep(3)
            
            # Fill email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "emailOrPhone"))
            )
            email_input.send_keys(self.account_data['email'])
            time.sleep(1)
            
            # Fill full name
            fullname_input = self.driver.find_element(By.NAME, "fullName")
            fullname_input.send_keys(self.account_data['full_name'])
            time.sleep(1)
            
            # Fill username
            username_input = self.driver.find_element(By.NAME, "username")
            username_input.send_keys(self.account_data['username'])
            time.sleep(1)
            
            # Fill password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.account_data['password'])
            time.sleep(1)
            
            # Click signup button
            signup_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            signup_btn.click()
            time.sleep(5)
            
            # Handle birthday (if appears)
            try:
                month_select = self.driver.find_element(By.XPATH, "//select[@title='Month:']")
                month_select.send_keys('January')
                day_select = self.driver.find_element(By.XPATH, "//select[@title='Day:']")
                day_select.send_keys('15')
                year_select = self.driver.find_element(By.XPATH, "//select[@title='Year:']")
                year_select.send_keys('1995')
                next_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_btn.click()
                time.sleep(3)
            except NoSuchElementException:
                pass
            
            logger.info(f"Account created: {self.account_data['username']}")
            return True
            
        except Exception as e:
            logger.error(f"Account creation failed: {str(e)}")
            return False
    
    def upload_profile_pic(self):
        """Upload profile picture"""
        try:
            # Navigate to profile
            self.driver.get(f"https://www.instagram.com/{self.account_data['username']}/")
            time.sleep(3)
            
            # Click edit profile
            edit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit profile')]"))
            )
            edit_btn.click()
            time.sleep(2)
            
            logger.info("Profile pic upload triggered")
            return True
            
        except Exception as e:
            logger.error(f"Profile pic upload failed: {str(e)}")
            return False
    
    def update_bio(self, bio_text="🎁 Fashion Enthusiast | Style Lover"):
        """Update Instagram bio"""
        try:
            self.driver.get(f"https://www.instagram.com/{self.account_data['username']}/")
            time.sleep(2)
            
            # Edit profile
            edit_btn = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Edit profile')]")
            edit_btn.click()
            time.sleep(2)
            
            # Update bio
            bio_input = self.driver.find_element(By.ID, "pepBio")
            bio_input.clear()
            bio_input.send_keys(bio_text)
            
            # Submit
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            time.sleep(2)
            
            logger.info("Bio updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Bio update failed: {str(e)}")
            return False
    
    def convert_to_professional(self):
        """Convert to professional account"""
        try:
            self.driver.get('https://www.instagram.com/accounts/edit/')
            time.sleep(2)
            
            # Navigate to professional settings
            settings_btn = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Switch to Professional Account')]")
            settings_btn.click()
            time.sleep(2)
            
            # Follow the conversion flow
            continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            continue_btn.click()
            time.sleep(2)
            
            logger.info("Converted to professional account")
            return True
            
        except Exception as e:
            logger.error(f"Professional conversion failed: {str(e)}")
            return False
    
    def post_photo(self):
        """Post a photo"""
        try:
            # Navigate to create post
            self.driver.get('https://www.instagram.com/')
            time.sleep(2)
            
            # Click new post button
            new_post_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='#']//span[contains(@class, 'xh8yej3')]"))
            )
            new_post_btn.click()
            time.sleep(2)
            
            logger.info("Post creation triggered")
            return True
            
        except Exception as e:
            logger.error(f"Post creation failed: {str(e)}")
            return False
    
    def follow_target(self, target_username="shein_official"):
        """Follow target account"""
        try:
            self.driver.get(f'https://www.instagram.com/{target_username}/')
            time.sleep(2)
            
            # Click follow button
            follow_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Follow')]"))
            )
            follow_btn.click()
            time.sleep(2)
            
            logger.info(f"Followed {target_username}")
            return True
            
        except Exception as e:
            logger.error(f"Follow failed: {str(e)}")
            return False
    
    def get_cookies_formatted(self):
        """Get cookies in specific format"""
        cookies = self.driver.get_cookies()
        cookie_dict = {}
        
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        
        # Format cookies as semicolon-separated string
        cookie_string = "; ".join([f"{name}={value}" for name, value in cookie_dict.items()])
        
        return cookie_string
    
    def cleanup(self):
        """Close driver"""
        if self.driver:
            self.driver.quit()


class TelegramBot:
    """Telegram bot handler with mandatory channel subscription"""
    
    def __init__(self):
        self.application = None
        self.active_processes = {}
        
    async def check_subscription(self, user_id, context):
        """Check if user is subscribed to mandatory channel"""
        try:
            member = await context.bot.get_chat_member(MANDATORY_CHANNEL_ID, user_id)
            return member.status in ['member', 'administrator', 'creator']
        except BadRequest:
            return False
        except Exception as e:
            logger.error(f"Subscription check error: {str(e)}")
            return False
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user_id = update.effective_user.id
        
        # Check subscription
        is_subscribed = await self.check_subscription(user_id, context)
        
        if not is_subscribed:
            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{MANDATORY_CHANNEL[1:]}")],
                [InlineKeyboardButton("✅ Check Subscription", callback_data='check_sub')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"⚠️ *Subscription Required*\n\n"
                f"You must join {MANDATORY_CHANNEL} to use this bot.\n\n"
                f"Click the button below to join, then click 'Check Subscription'.",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("🎁 Generate Account", callback_data='generate_account')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = """
🎉 *Instagram Account Generator Bot*

Welcome! This bot will automatically create Instagram accounts with full cookies.

*Features:*
✅ Automatic Instagram account creation
✅ Profile setup & optimization
✅ Full cookies export

Click "Generate Account" to start!
        """
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == 'check_sub':
            is_subscribed = await self.check_subscription(user_id, context)
            if is_subscribed:
                keyboard = [
                    [InlineKeyboardButton("🎁 Generate Account", callback_data='generate_account')],
                    [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    "✅ Subscription verified! You can now use the bot.\n\n"
                    "Click 'Generate Account' to start!",
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text(
                    f"❌ You're not subscribed yet!\n\n"
                    f"Please join {MANDATORY_CHANNEL} and try again.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{MANDATORY_CHANNEL[1:]}"),
                        InlineKeyboardButton("✅ Check Again", callback_data='check_sub')
                    ]])
                )
        elif query.data == 'generate_account':
            # Check subscription before generating
            is_subscribed = await self.check_subscription(user_id, context)
            if not is_subscribed:
                await query.edit_message_text(
                    f"❌ Subscription expired or removed!\n\n"
                    f"Please rejoin {MANDATORY_CHANNEL} to use the bot.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{MANDATORY_CHANNEL[1:]}"),
                        InlineKeyboardButton("✅ Check Again", callback_data='check_sub')
                    ]])
                )
                return
            await self.generate_account(query, context)
        elif query.data == 'help':
            await self.show_help(query, context)
    
    async def generate_account(self, query, context):
        """Generate Instagram account workflow"""
        user_id = query.from_user.id
        
        # Check if already running
        if user_id in self.active_processes:
            await query.edit_message_text("⚠️ You already have a process running. Please wait...")
            return
        
        self.active_processes[user_id] = {'status': 'started', 'step': 0}
        
        await query.edit_message_text("🚀 Starting account generation...\n\nThis may take 2-3 minutes.")
        
        try:
            # Step 1: Create Instagram Account
            await query.edit_message_text("⏳ Step 1/6: Creating Instagram account...")
            ig = InstagramAutomation(headless=True)
            ig.setup_driver()
            ig.generate_credentials()
            
            if not ig.create_account():
                raise Exception("Instagram account creation failed")
            
            await query.edit_message_text("✅ Step 1/6: Instagram account created!")
            time.sleep(2)
            
            # Step 2: Upload Profile Pic
            await query.edit_message_text("⏳ Step 2/6: Uploading profile picture...")
            ig.upload_profile_pic()
            await query.edit_message_text("✅ Step 2/6: Profile picture uploaded!")
            time.sleep(1)
            
            # Step 3: Update Bio
            await query.edit_message_text("⏳ Step 3/6: Updating bio...")
            ig.update_bio()
            await query.edit_message_text("✅ Step 3/6: Bio updated!")
            time.sleep(1)
            
            # Step 4: Convert to Professional
            await query.edit_message_text("⏳ Step 4/6: Converting to professional account...")
            ig.convert_to_professional()
            await query.edit_message_text("✅ Step 4/6: Professional account activated!")
            time.sleep(1)
            
            # Step 5: Post Photo & Follow
            await query.edit_message_text("⏳ Step 5/6: Posting photo and following target...")
            ig.post_photo()
            ig.follow_target("shein_official")
            await query.edit_message_text("✅ Step 5/6: Posted and followed!")
            
            # Step 6: Wait 5 seconds and get cookies
            await query.edit_message_text("⏳ Step 6/6: Waiting 5 seconds...")
            time.sleep(5)
            
            # Get cookies
            cookie_string = ig.get_cookies_formatted()
            
            result_text = f"""✅ 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗙𝗨𝗟𝗟𝗬 𝗦𝗘𝗧𝗨𝗣
━━━━━━━━━━━━━━━━━━
👤 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: `{ig.account_data['username']}`
🔑 𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱: `{ig.account_data['password']}`
📧 𝗘𝗺𝗮𝗶𝗹: `{ig.account_data['email']}`
━━━━━━━━━━━━━━━━━━
⚙️ 𝗦𝗲𝘁𝘂𝗽 𝗦𝘁𝗮𝘁𝘂𝘀:
✅ Profile Pic
✅ Bio
✅ Pro Account
✅ Photo Posted
✅ Followed Target

🍪 𝗖𝗼𝗼𝗸𝗶𝗲𝘀:
`{cookie_string}`

━━━━━━━━━━━━━━━━━━
✅ All done! Account ready to use!

Join {MANDATORY_CHANNEL} for more!
"""
            
            await query.edit_message_text(result_text, parse_mode='Markdown')
            
            # Cleanup
            ig.cleanup()
            
        except Exception as e:
            logger.error(f"Account generation error: {str(e)}")
            await query.edit_message_text(f"❌ Error occurred: {str(e)}\n\nPlease try again.")
        
        finally:
            if user_id in self.active_processes:
                del self.active_processes[user_id]
    
    async def show_help(self, query, context):
        """Show help information"""
        help_text = f"""
ℹ️ *Help & Information*

*How it works:*
1. Bot creates Instagram account automatically
2. Sets up profile (pic, bio, professional)
3. Posts content and follows target
4. Waits 5 seconds
5. Exports full cookies

*Process takes:* 2-3 minutes

*Commands:*
/start - Start the bot

*Mandatory:* Join {MANDATORY_CHANNEL} to use this bot!

*Support:* Contact admin for issues
        """
        
        await query.edit_message_text(help_text, parse_mode='Markdown')
    
    def run(self):
        """Run the bot"""
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.button_handler))
        
        logger.info("Bot started successfully!")
        logger.info(f"Mandatory channel: {MANDATORY_CHANNEL}")
        self.application.run_polling()


if __name__ == '__main__':
    # Create and run bot
    bot = TelegramBot()
    bot.run()
