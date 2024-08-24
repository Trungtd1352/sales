import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import re

TOKEN = '7353880861:AAF0aabJppqjHn-xqucCw77P_sAhhEgjuZ0'
CHAT_ID = '-4591330446'
THEMES = [
    {
        'url': 'https://themeforest.net/item/herrington-business-consulting-wordpress-theme/53469711',
        'sales_file': 'sales_count_herrington.txt'
    },
    {
        'url': 'https://themeforest.net/item/breeza-business-consulting-wordpress-theme/51218851',
        'sales_file': 'sales_count_breeza.txt'
    },
    {
        'url': 'https://themeforest.net/item/playhost-game-hosting-server-wordpress-theme/50357613',
        'sales_file': 'sales_count_playhost.txt'
    },
    {
        'url': 'https://themeforest.net/item/hadkaur-fitness-and-gym-wordpress-theme/48908264',
        'sales_file': 'sales_count_hadkaur.txt'
    },
    {
        'url': 'https://themeforest.net/item/digicove-digital-marketing-agency-wordpress-theme/47814692',
        'sales_file': 'sales_count_digicover.txt'
    }
    # Thêm nhiều theme khác vào đây
]
bot = Bot(token=TOKEN)

async def send_notification(message: str):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")

async def get_current_sales(theme_url):
    try:
        response = requests.get(theme_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        sales_status = soup.find('div', class_='item-header__sales-count')
        if sales_status:
            sales_text = sales_status.get_text(strip=True)
            sales_number = int(re.findall(r'\d+', sales_text)[0])
            return sales_number
        else:
            print(f"Không tìm thấy thông tin về sale cho theme: {theme_url}")
            return None
    except requests.RequestException as e:
        print(f"Error accessing the page {theme_url}: {e}")
        return None

async def check_sales():
    for theme in THEMES:
        current_sales = await get_current_sales(theme['url'])
        if current_sales is not None:
            try:
                with open(theme['sales_file'], 'r') as file:
                    last_sales = int(file.read().strip())
            except FileNotFoundError:
                last_sales = current_sales  # Nếu file không tồn tại, khởi tạo với số sale hiện tại

            if current_sales > last_sales:
                message = f"Số lượng sale đã tăng cho theme {theme['url']}: {current_sales} (tăng {current_sales - last_sales})"
                await send_notification(message)

            with open(theme['sales_file'], 'w') as file:
                file.write(str(current_sales))

async def main():
    print("Bot is starting...")
    while True:
        await check_sales()
        await asyncio.sleep(60)  # Kiểm tra mỗi phút

if __name__ == '__main__':
    asyncio.run(main())
