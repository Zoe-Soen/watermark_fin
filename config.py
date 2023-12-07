#encoding: utf-8
import os
import pandas as pd
from datetime import datetime as dt

os.chdir("/Users/Zoe.Su/Documents/Zoe的学习资料/Python/100 days of Code- The Complete Python Pro Bootcamp for 2023/exercise code/day-85-image-wartermark")

CURRENT_DATE = dt.now().strftime('%Y%m%d')

UI_FONT = 'assets/fonts/Arial.ttf'
# WELCOME_MESSAGE = "Welcome to use Watermarkly!"
# DES_MESSAGE = '''1. Open an image from your PC.
# 2. Choose 'Add Watermark', type the watermark in to the 'Text Entry', and set the font, color, size, position, opacity and rotation.
# 3. Or choose 'Add Logo' to upload a logo onto your image file.
# 4. Click 'Remove' to clear all change you made.
# 5. Click 'Save' to output your edition and save to your local folder as a new image file.
# '''

LOGO_IMAGE = 'assets/logo/1.png'
OPEN_COLSE_BTN_IMG = ['assets/icons/up-arrow.png', 'assets/icons/right-arrow.png']

df = pd.read_csv("assets/colors/rgb_colors.csv")
COLOR_LIST = df['hex'].values.tolist()
ALL_COLOR = df.to_dict('records')

FONT_FAMILIES = [
    {'font_name': 'Arial', 'path': 'assets/fonts/Arial.ttf'},
    {'font_name': 'Degreco', 'path': 'assets/fonts/degreco-condensed-regular.otf'},
    {'font_name': 'Eagle Lake', 'path': 'assets/fonts/EagleLake-Regular.ttf'},
    {'font_name': 'IBM Plex Mono', 'path': 'assets/fonts/IBMPlexMono-Regular.ttf'},
    {'font_name': 'Jacques Francois', 'path': 'assets/fonts/JacquesFrancois-Regular.ttf'},
    {'font_name': 'Quando', 'path': 'assets/fonts/Quando-Regular.ttf'},
    {'font_name': 'Racing Sans One', 'path': 'assets/fonts/RacingSansOne-Regular.ttf'},
    {'font_name': 'Sacramento', 'path': 'assets/fonts/Sacramento-Regular.ttf'},
    {'font_name': 'Sail', 'path': 'assets/fonts/Sail-Regular.ttf'},
    {'font_name': 'Trade Winds', 'path': 'assets/fonts/TradeWinds-Regular.ttf'},
    {'font_name': 'Verdana', 'path': 'assets/fonts/verdana.ttf'},
    {'font_name': 'ZCOOL KuaiLe', 'path': 'assets/fonts/ZCOOLKuaiLe-Regular.ttf'},
    ]

POSTIONS = ['Top Left', 'Top Center', 'Top Right', 'Middle Center', 'Bottom Left', 'Bottom Center', 'Bottom Right']

IMAGEBOX_WIDTH = 1320
IMAGEBOX_HEIGHT = 700