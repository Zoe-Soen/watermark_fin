# Sample：https://watermarkly.com/

from tkinter import Button, Image, messagebox, END
import tkinter as tk
import ttkbootstrap
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
from config import *

# ====================================================================================
class AddTextMenu(ttkbootstrap.Frame):
    def __init__(self, win, watermark, photo_box, add_text_btn):
        super().__init__(win)
        self.watermark = watermark 
        self.photo_box = photo_box
        self.add_text_btn = add_text_btn
        
    def kill_win(self):
        self.sub_win.destroy()
        self.add_text_btn.configure(state=NORMAL)

    def create_new_add_text_menu(self):
        self.sub_win = ttkbootstrap.Toplevel()
        self.sub_win.title('Properties')
        self.sub_win.geometry(f'420x700+1000+140')

        self.text_entry = TextEntry(self.sub_win, self.watermark, self.on_text_change)
        self.text_entry.grid(row=2, column=0, padx=15, pady=(15,5), sticky=NSEW)

        self.font_widget = FontWidget(self.sub_win, self.watermark, self.on_font_change)
        self.font_widget.grid(row=3, column=0, padx=15, pady=5, sticky=NSEW)

        self.color_widget = ColorWidget(self.sub_win, self.on_color_change)
        self.color_widget.grid(row=4, column=0, padx=15, pady=5, sticky=NSEW)

        self.size_widget = SizeWidget(self.sub_win, 'watermark', self.on_size_change, self.watermark.font_size, self.watermark.font_size_from, self.watermark.font_size_to)
        self.size_widget.grid(row=5, column=0, padx=15, pady=5, sticky=NSEW)

        self.opacity_widget = OpacityWidget(self.sub_win, self.on_opacity_change)
        self.opacity_widget.grid(row=6, column=0, padx=15, pady=5, sticky=NSEW)

        self.position_widget = PositionWidget(self.sub_win, self.watermark, self.on_position_set, self.on_position_change)
        self.position_widget.grid(row=7, column=0, padx=15, pady=5, sticky=NSEW)

        self.rotation_widget = RotationWidget(self.sub_win, self.on_rotation_change)
        self.rotation_widget.grid(row=8, column=0, padx=15, pady=5, sticky=NSEW)

        self.copy_save_widget = ClearSaveWidget(self.sub_win, self.clear, self.confirm_change)
        self.copy_save_widget.grid(row=9, column=0, padx=15, pady=(35,15))

    # --------------------------------------------------------------
    def on_text_change(self, sv):
        self.watermark.text = sv.get()
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def on_font_change(self, font):
        self.font_widget.show_font_effect.configure(image=font['photo'])
        self.font_widget.show_font_name.configure(text=font['font_name'])
        self.watermark.change_font(font)
        self.photo_box.update_watermark()
        self.font_widget.toggle_open_close()

    # --------------------------------------------------------------
    def on_color_change(self, color):
        self.color_widget.show_color_hex.configure(text=color, background=color)
        self.watermark.change_color(color)
        self.photo_box.update_watermark()
        self.color_widget.toggle_open_close()

    # --------------------------------------------------------------
    def on_size_change(self, event, selected_size):
        self.watermark.change_size(event, selected_size)
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def on_opacity_change(self, event):
        self.watermark.change_opacity(event, self.opacity_widget.slider.get())
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def on_position_set(self):
        self.watermark.selected_pos = self.position_widget.var_radio.get()
        self.watermark.get_position(
            im_w=self.photo_box.resized_im.width, 
            im_h=self.photo_box.resized_im.height,
            text_w=self.photo_box.text_w,
            text_h=self.photo_box.text_h)
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def on_position_change(self, direction):
        self.watermark.move(direction)
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def on_rotation_change(self, event, var_scale): # Scale version
        self.watermark.rotate(event, var_scale)
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def clear(self):
        self.kill_win()
        self.photo_box.remove('watermark')
        self.create_new_add_text_menu()
        self.photo_box.update_watermark()

    # --------------------------------------------------------------
    def confirm_change(self):
        if self.watermark.text == 'Your Text':
            response = messagebox.askokcancel('Confirmation', f'The current watermark text:\n {self.watermark.text}\n')
            if response is True:
                self.kill_win()
            else:
                return
        elif self.watermark.text == '':
            response = messagebox.showwarning("Warning", "The watermark text is empty.\nDo you want to go ahead?")
            if response is True:
                self.kill_win()
            else: 
                return
        else:
            self.kill_win()

    # --------------------------------------------------------------
    def save(self):
        self.photo_box.save()

# ====================================================================================
class AddLogoMenu(ttkbootstrap.Frame):
    def __init__(self, win, logo, photo_box, add_logo_btn):
        super().__init__(win)
        self.logo = logo
        self.add_logo_btn = add_logo_btn
        self.photo_box = photo_box

    def kill_win(self):
        self.sub_win.destroy()
        self.add_logo_btn.configure(state=NORMAL)

    def create_new_add_logo_menu(self):
        self.sub_win = ttkbootstrap.Toplevel() 
        self.sub_win.title('Properties')
        self.sub_win.geometry(f'420x500+1000+140')

        self.size_widget = SizeWidget(self.sub_win, 'logo', self.on_size_change, self.logo.logo_size, self.logo.logo_size_from, self.logo.logo_size_to)
        self.size_widget.grid(row=2, column=0, padx=15, pady=5, sticky=NSEW)

        self.opacity_widget = OpacityWidget(self.sub_win, self.on_opacity_change)
        self.opacity_widget.grid(row=3, column=0, padx=15, pady=5, sticky=NSEW)

        self.position_widget = PositionWidget(self.sub_win, self.logo, self.on_position_set, self.on_position_change)
        self.position_widget.grid(row=4, column=0, padx=15, pady=5, sticky=NSEW)

        self.rotation_widget = RotationWidget(self.sub_win, self.on_rotation_change)
        self.rotation_widget.grid(row=5, column=0, padx=15, pady=5, sticky=NSEW)

        self.copy_save_widget = ClearSaveWidget(self.sub_win, self.clear, self.confirm_change)  # self.save
        self.copy_save_widget.grid(row=6, column=0, padx=15, pady=(35,15))

        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def on_size_change(self, event, selected_size):
        self.logo.change_size(event, selected_size)
        # self.on_position_set()
        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def on_opacity_change(self, event):
        self.logo.change_opacity(event, self.opacity_widget.slider.get())
        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def on_position_set(self):
        self.logo.selected_pos = self.position_widget.var_radio.get()
        self.logo.get_position(
            self.photo_box.resized_im.width, 
            self.photo_box.resized_im.height,
            self.photo_box.logo_w,
            self.photo_box.logo_h
            )
        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def on_position_change(self, direction):
        self.logo.move(direction)
        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def on_rotation_change(self, event, var_scale):
        self.logo.rotate(event, var_scale)
        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def clear(self):
        self.kill_win()
        self.photo_box.remove('logo')
        self.create_new_add_logo_menu()
        self.photo_box.update_logo()

    # --------------------------------------------------------------
    def confirm_change(self):
        if self.photo_box.logo.logo_im is not None:
            response = messagebox.askokcancel('Confirmation', f'Save Image with logo?')
        else:
            response = messagebox.showwarning("Warning", "There's no LOGO added.\nAre you want to go ahead?")

        if response is True:
            self.kill_win()
        else:
            return

# ====================================================================================
class TextEntry(ttkbootstrap.Frame):
    def __init__(self, win, watermark, on_text_change):
        super().__init__(win)
        ttkbootstrap.Label(self, text='Text:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.sv = ttkbootstrap.StringVar()
        self.sv.set(watermark.text)
        self.sv.trace('w', lambda name, index, mode, sv=self.sv: on_text_change(sv))
        self.ent = ttkbootstrap.Entry(self, textvariable=self.sv, width=32)
        self.ent.focus()
        self.ent.grid(row=0, column=1)

# ====================================================================================
class FontWidget(ttkbootstrap.Frame):
    def __init__(self, win, watermark, on_font_change, **kwargs):
        super().__init__(win, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        self.base_frm = ttkbootstrap.Frame(self) 
        self.base_frm.grid(row=0, column=0, sticky=NSEW)
        
        self.up_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[0])
        self.right_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[1])

        ttkbootstrap.Label(self.base_frm, text='Font: ', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        frm = ttkbootstrap.Frame(self.base_frm, width=26)
        frm.grid(row=0, column=1, sticky=EW)
        self.show_font_effect = ttkbootstrap.Label(frm, text='') 
        self.show_font_effect.grid(row=0, column=0)
        self.show_font_name = ttkbootstrap.Label(frm, text='', width=23, anchor=CENTER) 
        self.show_font_name.grid(row=0, column=1, padx=(1,2))
        self.btn = Button(frm, text='', image=self.right_arrow_img, width=20, command=self.toggle_open_close) 
        self.btn.grid(row=0, column=2, sticky=E)

        self.canvas = ttkbootstrap.Canvas(self.base_frm, highlightthickness=0)        
        self.scrollbar = ttkbootstrap.Scrollbar(self.base_frm, orient=tk.VERTICAL, command=self.canvas.yview)        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.style = ttkbootstrap.Style()
        self.font_group = ttkbootstrap.Frame(self, padding=(20,5,0,0))
        self.font_group.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.font_group, anchor=NW)

        for num, font in enumerate(watermark.font_families):
            width, height = (60, 60)
            text_1 = 'Ag'
            d_font_1 = ImageFont.truetype(font['path'], size=26)
            d_fill = (77, 77, 77)

            font_txt = Image.new('RGB', (width, height), (256, 256, 256))
            d = ImageDraw.Draw(font_txt)
            _, _, w, h = d.textbbox((0, 0), text=text_1, font=d_font_1) 
            d.text(xy=((width-w)/2, (height-h)/2), text=text_1, font=d_font_1, fill=d_fill) 
            
            font_photo = ImageTk.PhotoImage(font_txt)
            font['photo'] = font_photo 
            font_btn = Button(self.font_group, image=font_photo, command=lambda font=font: on_font_change(font)) 
            font_btn.grid(row=int(num/5)+1, column=num%5, padx=1, pady=1, sticky=W) 

        self.show_font_effect.configure(image=watermark.font_families[0]['photo'])
        self.show_font_name.configure(text=watermark.font_families[0]['font_name'])
        
    def toggle_open_close(self):
        if self.font_group.winfo_viewable():
            self.canvas.grid_remove()
            self.scrollbar.grid_remove()
            self.btn.configure(image=self.right_arrow_img)
        else:
            self.canvas.grid(row=1, column=0, columnspan=4, padx=0, sticky=EW) 
            self.scrollbar.grid(row=1, column=3, padx=0, sticky=NS+W) 
            self.btn.configure(image=self.up_arrow_img)
    
# ====================================================================================
class ColorWidget(ttkbootstrap.Frame): 
    def __init__(self, win, on_color_change, **kwargs): 
        super().__init__(win, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        self.color_families = COLOR_LIST

        self.up_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[0])
        self.right_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[1])

        self.base_frm = ttkbootstrap.Frame(self) 
        self.base_frm.grid(row=0, column=0, sticky=NSEW)

        ttkbootstrap.Label(self.base_frm, text='Color: ', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        frm = ttkbootstrap.Frame(self.base_frm)
        frm.grid(row=0, column=1, sticky=NSEW)

        self.show_color_hex = ttkbootstrap.Label(frm, text='hex: ', foreground='gray', background=self.color_families[0], width=30)
        self.show_color_hex.grid(row=0, column=1, padx=(0,5), sticky=EW)
        self.btn = Button(frm, text='', width=20, image=self.right_arrow_img, command=self.toggle_open_close) 
        self.btn.grid(row=0, column=2, sticky=NSEW)

        self.canvas = ttkbootstrap.Canvas(self.base_frm)
        self.scrollbar = ttkbootstrap.Scrollbar(self.base_frm, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.style = ttkbootstrap.Style()
        self.color_group = ttkbootstrap.Frame(self.canvas, padding=(20,5,0,0))
        self.color_group.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.color_group, anchor=NW)
        
        for num, color in enumerate(self.color_families):
            self.style.configure(f'{color}.TButton', background=color, width=1)
            color_btn = ttkbootstrap.Button(self.color_group, style=f'{color}.TButton', bootstyle='light-link', command=lambda color=color: on_color_change(color))
            color_btn.grid(row=int(num/10)+1, column=num%10, padx=1, pady=1)

    def toggle_open_close(self):
        if self.color_group.winfo_viewable():
            self.canvas.grid_remove()
            self.scrollbar.grid_remove()
            self.btn.configure(image=self.right_arrow_img)
        else:
            self.canvas.grid(row=1, column=0, columnspan=3, sticky=EW)
            self.scrollbar.grid(row=1, column=3, sticky=NS)
            self.btn.configure(image=self.up_arrow_img)

# ====================================================================================
class SizeWidget(ttkbootstrap.Frame):
    def __init__(self, win, obj, on_size_change, initial_set, size_from, size_to):

        super().__init__(win)
        ttkbootstrap.Label(self, text='Size:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.selected_size = ttkbootstrap.IntVar()
        self.selected_size.set(initial_set)
        
        self.scale = ttkbootstrap.Scale(self, variable=self.selected_size, from_=size_from, to_=size_to, length=250, command=lambda s:self.selected_size.set("%d" % float(s)))
        self.scale.grid(row=0, column=2)

        if obj == 'watermark':
            lb = ttkbootstrap.Label(self, textvariable=self.selected_size, width=5)
            self.scale.bind('<Motion>', lambda event: on_size_change(event, self.selected_size.get()))
        elif obj == 'logo': 
            self.lb_text = ttkbootstrap.StringVar()
            self.lb_text.set('{:.1f}x'.format(initial_set / 10))
            lb = ttkbootstrap.Label(self, textvariable=self.lb_text, width=5)
            self.scale.bind('<Motion>', lambda event: (on_size_change(event, self.selected_size.get()), self.lb_text.set('{:.1f}x'.format(self.selected_size.get() / 10))))
        
        lb.grid(row=0, column=1)

# ====================================================================================
class OpacityWidget(ttkbootstrap.Frame):
    def __init__(self, win, on_opacity_change):

        super().__init__(win)
        ttkbootstrap.Label(self, text='Opacity:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)

        self.slider = ttkbootstrap.IntVar()
        self.slider.set(255)

        self.scale = ttkbootstrap.Scale(self, variable=self.slider, from_=0, to_=255, length=260, command=lambda s:self.slider.set("%d" % float(s)))
        self.scale.grid(row=0, column=2)
        
        lb = ttkbootstrap.Label(self, textvariable=self.slider, width=4)
        lb.grid(row=0, column=1)
        
        self.scale.bind('<Motion>', on_opacity_change)

# ====================================================================================
class PositionWidget(ttkbootstrap.Frame):
    def __init__(self, win, watermark, on_position_set, on_position_change):

        super().__init__(win)
        self.watermark = watermark

        ttkbootstrap.Label(self, text='Position:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        frm = ttkbootstrap.Frame(self)
        frm.grid(row=0, column=1, sticky=NSEW)

        sub_frm1 = ttkbootstrap.Frame(frm)
        sub_frm1.grid(row=0, column=0, pady=5)

        self.var_radio = ttkbootstrap.StringVar(value=self.watermark.selected_pos)
        for num, pos in enumerate(self.watermark.positions):
            self.radio_btn = ttkbootstrap.Radiobutton(sub_frm1, text=pos, value=pos, bootstyle='danger', variable=self.var_radio, command=on_position_set)
            self.radio_btn.grid(row=num+1, column=0, pady=2, sticky=W)

        sub_frm2 = ttkbootstrap.Frame(frm)
        sub_frm2.grid(row=0, column=1, padx=80, sticky=E)
        direction_btns = [
            {'text': '▲', 'direction': 'up', 'row': 0, 'col':1},
            {'text': '◀', 'direction': 'left', 'row': 1, 'col':0},
            {'text': '▶', 'direction': 'right', 'row': 1, 'col':2},
            {'text': '▼', 'direction': 'down', 'row': 2, 'col':1},
        ]
        for btn in direction_btns:
            self.btn = ttkbootstrap.Button(sub_frm2, text=btn['text'], width=1, bootstyle='second-outline', command=lambda dir=btn['direction']: on_position_change(dir))
            self.btn.grid(row=btn['row'], column=btn['col'], padx=2, pady=2)

# ====================================================================================
class RotationWidget(ttkbootstrap.Frame): 
    def __init__(self, win, on_rotation_change):

        super().__init__(win)
        ttkbootstrap.Label(self, text='Rotation:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.slider = ttkbootstrap.IntVar()
        self.slider.set(0)

        self.scale = ttkbootstrap.Scale(self, variable=self.slider, from_=-180, to_=180, length=210, command=lambda s:self.slider.set('%d' % float(s)))
        self.scale.grid(row=0, column=2)

        self.slider_s = ttkbootstrap.StringVar()
        self.slider_s.set('0°')
        self.lb = ttkbootstrap.Label(self, textvariable=self.slider_s, width=4)
        self.lb.grid(row=0, column=1)
        self.scale.bind('<Motion>', lambda event: (on_rotation_change(event, self.slider.get()), self.slider_s.set(f'{self.slider.get()}°')))

        self.btn = ttkbootstrap.Button(self, text='Reset', bootstyle='second-outline', command=lambda s=0:self.slider.set(0))
        self.btn.grid(row=0, column=3)
        self.btn.bind('<Button-1>', lambda event: (on_rotation_change(event, 0), self.slider_s.set('0°')))

# ====================================================================================
class AddLogoWidget(ttkbootstrap.Frame):
    def __init__(self, win, add_logo):

        super().__init__(win)
        ttkbootstrap.Label(self, text='Logo file:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.open_logo_btn = ttkbootstrap.Button(self, text='Choose file', bootstyle='secondary-outline', width=21, command=add_logo)
        self.open_logo_btn.grid(row=0, column=1, sticky=NSEW)

    def enbable_add_logo(self):
        self.open_logo_btn.configure(state=NORMAL)

# ====================================================================================
class ClearSaveWidget(ttkbootstrap.Frame):
    def __init__(self, win, clear, save):

        super().__init__(win)
        self.clear_btn = ttkbootstrap.Button(self, text='Clear', bootstyle=SECONDARY, width=8, command=clear)
        self.clear_btn.grid(row=0, column=0, padx=(0,50), sticky=NSEW)

        self.confirm = ttkbootstrap.Button(self, text='Confirm', bootstyle=SUCCESS, width=8 , command=save)
        self.confirm.grid(row=0, column=2, padx=(50,0), sticky=NSEW)


# ====================================================================================
if __name__ == "__main__":
    # print(COLOR_LIST)
    pass
