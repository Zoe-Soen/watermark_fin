# 参考案例：https://watermarkly.com/

from tkinter import Image, filedialog as fd, messagebox, END
import ttkbootstrap
from ttkbootstrap.constants import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageEnhance
import os
from config import *

# ====================================================================================
class ImageViewBox(ttkbootstrap.Canvas):
    """For Preview"""
    def __init__(self, frame, watermark, logo):

        super().__init__(frame)
        self.watermark = watermark
        self.logo = logo

        self.max_width = IMAGEBOX_WIDTH
        self.max_height = IMAGEBOX_HEIGHT
        self.im_box_ratio = self.max_width / self.max_height

        self.im_vs_watermark = None
        self.im_vs_logo = None
    
    # --------------------------------------------------------------
    def update_watermark(self):
        if self.im_vs_logo is None:
            img_copy = self.resized_im.copy()
        else:
            img_copy = self.im_vs_logo.copy()

        txt = Image.new('RGBA', img_copy.size)
        d = ImageDraw.Draw(txt, 'RGBA')
        font = ImageFont.truetype(self.watermark.font['path'], size=self.watermark.font_size) 

        if self.watermark.text != '':
            _, _, self.text_w, self.text_h = d.textbbox((0, 0), text=self.watermark.text, font=font)
            
            txt = txt.resize((self.text_w, self.text_h))
            d = ImageDraw.Draw(txt, 'RGBA')
            d.text((0, 0), text=self.watermark.text, fill=(self.watermark.color), font=font)
        
            rotated_txt = txt.rotate(self.watermark.rotation * -1, expand=True)
            offset_x = int((rotated_txt.width - txt.width) / 2)
            offset_y = int((rotated_txt.height - txt.height) / 2)
            img_copy.paste(rotated_txt, (self.watermark.x - offset_x, self.watermark.y - offset_y), rotated_txt)

        self.im_vs_watermark = img_copy.copy()
        self.photo = ImageTk.PhotoImage(img_copy)
        self.composite_image = img_copy
        self.create_image(0,0, anchor=NW, image=self.photo)
    
    def update_logo(self):
        if self.im_vs_watermark is None:
            img_copy = self.resized_im.copy() 
        else:
            img_copy = self.im_vs_watermark.copy()   
            self.logo.selected_pos = self.watermark.selected_pos
            self.selected_pos = self.watermark.positions[0]
            self.x, self.y = 0, 0

        if self.logo.logo_im is not None:
            self.logo_w = int(self.resized_im.width / self.logo.logo_size_to * self.logo.logo_size)
            self.logo_h = int(self.logo_w / (self.logo.logo_im.width / self.logo.logo_im.height))

            logo_copy = self.logo.logo_im.copy().resize(size=(self.logo_w, self.logo_h))  

            rotated_logo = logo_copy.rotate(self.logo.rotation * -1, expand=True)
            offset_x2 = int((rotated_logo.width - logo_copy.width) / 2)
            offset_y2 = int((rotated_logo.height - logo_copy.height) / 2)
            img_copy.paste(rotated_logo, (self.logo.x - offset_x2, self.logo.y - offset_y2), rotated_logo)
        
        self.im_vs_logo = img_copy.copy()
        self.photo = ImageTk.PhotoImage(img_copy)
        self.composite_image = img_copy
        self.create_image(0,0, anchor=NW, image=self.photo)

    # --------------------------------------------------------------
    def update_photo(self, fp):
        self.open_fp = fp
        try:
            im = Image.open(fp).convert('RGBA')

            # For Save:
            self.origin_im = im.copy()
            self.origin_im_width, self.origin_im_height = self.origin_im.size

            # For Preview: Change the size to fix into photo_box：https://qiita.com/AltGuNi/items/efcb5865bae6f756704a
            self.resized_im = im.copy()
            self.resized_im.thumbnail((self.max_width, self.max_height))
            self.resized_im_width, self.resized_im_height = self.resized_im.size

            self.ratio = self.origin_im_height / self.resized_im_height
            self.new_padx = int(abs(self.max_width - self.resized_im_width)/2)
            self.new_pady = int(abs(self.max_height - self.resized_im_height)/2)

            self.photo = ImageTk.PhotoImage(self.resized_im)
            self.configure(width=self.resized_im_width, height=self.resized_im_height)
            self.create_image(0,0, anchor=NW, image=self.photo)

        except PIL.UnidentifiedImageError:
            messagebox.showerror(f'Invalid Image: {fp}')

    # --------------------------------------------------------------
    def remove(self, obj='watermark'):
        if obj == 'watermark':
            self.watermark.text = ''
            self.watermark.font = self.watermark.font_families[0]
            self.watermark.font_size = 50
            self.watermark.opacity = 255
            self.watermark.color = self.watermark.color_list[0]['hex'] # black
            self.watermark.rotation = 0
            self.watermark.selected_pos = self.watermark.positions[3]
        elif obj == 'logo':
            self.logo.logo_im = None

    # --------------------------------------------------------------
    def save(self):
        out_put_img = self.origin_im.copy()

        # Watermark
        txt = Image.new('RGBA', out_put_img.size)
        d = ImageDraw.Draw(txt, 'RGBA')
        font = ImageFont.truetype(self.watermark.font['path'], size=self.watermark.font_size * self.ratio) 
        _, _, self.origin_text_w, self.origin_text_h = d.textbbox((0, 0), text=self.watermark.text, font=font)
        self.watermark.x = int(self.watermark.x * self.ratio)
        self.watermark.y = int(self.watermark.y * self.ratio)
        
        txt = txt.resize((self.origin_text_w, self.origin_text_h))
        d = ImageDraw.Draw(txt, 'RGBA')
        d.text((0, 0), text=self.watermark.text, fill=(self.watermark.color), font=font)

        rotated_txt = txt.rotate((self.watermark.rotation * -1), expand=True)
        offset_x = int((rotated_txt.width - txt.width) / 2)
        offset_y = int((rotated_txt.height - txt.height) / 2)
        out_put_img.paste(rotated_txt, (self.watermark.x - offset_x, self.watermark.y - offset_y), rotated_txt)
        
        # Logo:
        self.origin_logo_w = int(self.origin_im.width / self.logo.logo_size_to * self.logo.logo_size)
        self.origin_logo_h = int(self.origin_logo_w / (self.logo.logo_im.width / self.logo.logo_im.height))
        self.logo.x = int(self.logo.x * self.ratio)
        self.logo.y = int(self.logo.y * self.ratio)
        
        logo_copy = self.logo.logo_im.copy().resize(size=(self.origin_logo_w, self.origin_logo_h))  

        rotated_logo = logo_copy.rotate(self.logo.rotation * -1, expand=True)
        offset_x2 = int((rotated_logo.width - logo_copy.width) / 2)
        offset_y2 = int((rotated_logo.height - logo_copy.height) / 2)
        out_put_img.paste(rotated_logo, (self.logo.x - offset_x2, self.logo.y - offset_y2), rotated_logo) 

        output_file_name = f'{CURRENT_DATE}_{self.open_fp.split('/')[-1].split('.')[0]}' 
        file_path = fd.asksaveasfilename(
            initialfile=output_file_name,
            confirmoverwrite=True,
            defaultextension='png',
            filetypes=[('jpeg', '.jpg .jpeg'), ('png', '.png'), ('bitmap', '.bmp'), ('gif', '.gif')])
        if file_path is not None:
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension in ['.jpg', '.jpeg']:
                out_put_im = out_put_img.convert('RGB')
                out_put_im.save(file_path, quality = 95)
                print('img vs watermark has been saved!')
    # --------------------------------------------------------------

# ====================================================================================
class Watermark():
    def __init__(self, app):
        self.app = app

        self.color_list = ALL_COLOR
        self.font_families = FONT_FAMILIES
        self.font = self.font_families[0]
    
        self.font_size_from, self.font_size_to = 10, 200
        self.font_size = 50
        self.opacity = 255
        self.color = (0, 0, 0, self.opacity) # black
        self.rotation = 0
        self.positions = POSTIONS
        self.selected_pos = self.positions[0]
        
        self.text = 'Your Text'
        self.x, self.y = 0, 0

    # --------------------------------------------------------------
    def get_position(self, im_w, im_h, text_w, text_h):
        for pos in self.positions:
            if self.selected_pos == pos and pos == "Middle Center":
                self.x = int((im_w - text_w) / 2)
                self.y = int((im_h - text_h) / 2)
            elif self.selected_pos == pos and pos == "Top Left":
                self.x = 0
                self.y = 0
            elif self.selected_pos == pos and pos == "Top Center":
                self.x = int((im_w - text_w) / 2)
                self.y = 0
            elif self.selected_pos == pos and pos == "Top Right":
                self.x = int(im_w - text_w)
                self.y = 0
            elif self.selected_pos == pos and pos == "Bottom Left":
                self.x = 0
                self.y = im_h - text_h
            elif self.selected_pos == pos and pos == "Bottom Center":
                self.x = int((im_w - text_w) / 2)
                self.y = im_h - text_h
            elif self.selected_pos == pos and pos == "Bottom Right":
                self.x = im_w - text_w
                self.y = im_h - text_h

    # --------------------------------------------------------------
    def move(self, direction):
        if direction == "up":
            self.y -= 10
        elif direction == "down":
            self.y += 10
        elif direction == "left":
            self.x -= 10
        elif direction == "right":
            self.x += 10
    
    # --------------------------------------------------------------    
    def change_font(self, font):
        self.font = font

    # --------------------------------------------------------------
    def change_color(self, color): 
        """
        - Converting RGB to HEX:
            def rgb2hex(r,g,b):
                return "#{:02x}{:02x}{:02x}".format(r,g,b)

        - Converting HEX to RGB:
            def hex2rgb(hexcode):
                return tuple(map(ord,hexcode[1:].decode('hex')))
        """
        if color == None:
            list_color = list(self.color)[:3]  
        else:
            for item in self.color_list:
                if color == item['hex']:
                    rgb = item['rgb'].strip('()')
                    list_color = [int(i) for i in rgb.split(',')]
        list_color.append(self.opacity)
        self.color = tuple(list_color)

    # --------------------------------------------------------------
    def change_size(self, event, size):
        self.font_size = int(size)

    # --------------------------------------------------------------   
    def change_opacity(self, event, var_scale):
        list_color = list(self.color)[:3]
        self.opacity = var_scale
        list_color.append(self.opacity)
        self.color = tuple(list_color)

    # --------------------------------------------------------------
    def rotate(self, event, var_scale): 
        self.rotation = var_scale
    # --------------------------------------------------------------

# ====================================================================================
class Logo():
    def __init__(self, app):
        self.app = app

        self.logo_im = None
        self.logo_size_from, self.logo_size_to = 1, 100
        self.logo_size = 10
        self.opacity = 1
        self.rotation = 0
        self.positions = POSTIONS
        self.selected_pos = self.positions[0]
        self.x, self.y = 0, 0

    def open_logo(self, fp):
        self.fp = fp
        try:
            self.logo_im = Image.open(fp).convert('RGBA')
            self.logo_photo = ImageTk.PhotoImage(self.logo_im)
        except PIL.UnidentifiedImageError:
            messagebox.showerror(f'Invalid Image: {fp}')   

    def change_size(self, event, size):
        self.logo_size = int(size)

    def get_position(self, im_w, im_h, logo_w, logo_h):
        for pos in self.positions:
            if self.selected_pos == pos and pos == "Middle Center":
                self.x = int((im_w - logo_w) / 2)
                self.y = int((im_h - logo_h) / 2)
            elif self.selected_pos == pos and pos == "Top Left":
                self.x = 0
                self.y = 0
            elif self.selected_pos == pos and pos == "Top Center":
                self.x = int((im_w - logo_w) / 2)
                self.y = 0
            elif self.selected_pos == pos and pos == "Top Right":
                self.x = int(im_w - logo_w)
                self.y = 0
            elif self.selected_pos == pos and pos == "Bottom Left":
                self.x = 0
                self.y = im_h - logo_h
            elif self.selected_pos == pos and pos == "Bottom Center":
                self.x = int((im_w - logo_w) / 2)
                self.y = im_h - logo_h
            elif self.selected_pos == pos and pos == "Bottom Right":
                self.x = im_w - logo_w
                self.y = im_h - logo_h

    def move(self, direction):
        if direction == "up":
            self.y -= 10
        elif direction == "down":
            self.y += 10
        elif direction == "left":
            self.x -= 10
        elif direction == "right":
            self.x += 10               

    def change_opacity(self, event, var_scale):
        self.opacity = var_scale / 255
        if self.logo_im != None:
            self.logo_im = self.logo_im.copy()

            alpha = self.logo_im.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
            self.logo_im.putalpha(alpha)

    def rotate(self, event, var_scale):
        self.rotation = var_scale

# ====================================================================================
if __name__ == "__main__":
    pass
    