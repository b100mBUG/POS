from kivymd.app import MDApp
import os
from datetime import datetime, timedelta
from kivy.lang import Builder
import hashlib
from sqlalchemy import func
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivy.properties import StringProperty, ObjectProperty
from kivy.metrics import dp, sp
from kivy.clock import Clock
from functools import partial
from sqlalchemy import func
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from sqlalchemy.exc import IntegrityError
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.widget import Widget
import sys
from kivymd.uix.card import MDCard
import uuid
from kivymd.uix.divider import MDDivider
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDExtendedFabButton, MDExtendedFabButtonIcon, MDExtendedFabButtonText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogContentContainer, MDDialogHeadlineText, MDDialogIcon, MDDialogSupportingText
import database

def resource_path(relative_path):
    return os.path.join(sys._MEIPASS, relative_path) if hasattr(sys, '_MEIPASS') else os.path.join(os.path.abspath('.'), relative_path)

class SeperatorDiv(MDDivider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = "gold"

class ProductCard(MDBoxLayout):
    prod_name = StringProperty("")
    prod_category = StringProperty("")
    prod_desc = StringProperty("")
    prod_price = StringProperty("")
    quantity = StringProperty("")
    product_image = StringProperty("")

    on_edit = ObjectProperty(allownone=True)
    on_remove = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(190)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (.9, .9, .9, .8)

        self.item_container = MDBoxLayout(orientation="vertical", spacing=dp(5), size_hint_x = 0.7)
        self.button_container = MDGridLayout(cols = 3, spacing = dp(20))
        self.edit_item_button = MDButton(
            MDButtonText(text = "Edit", theme_text_color = "Custom", text_color = "white", bold = True), 
            MDButtonIcon(icon = "pencil-outline", theme_icon_color = "Custom", icon_color = "white"), 
            style = "outlined",
            theme_bg_color = "Custom", 
            md_bg_color = "green",
            on_release = lambda x: self.on_edit()
        ) 
        self.remove_item_button = MDButton(
            MDButtonText(text = "Remove", theme_text_color = "Custom", text_color = "white", bold = True), 
            MDButtonIcon(icon = "close", theme_icon_color = "Custom", icon_color = "white"), 
            style = "outlined",
            theme_bg_color = "Custom", 
            md_bg_color = "red",
            on_release = lambda x: self.on_remove()
        ) 
        self.button_container.add_widget(Widget())
        self.button_container.add_widget(self.edit_item_button)
        self.button_container.add_widget(self.remove_item_button)

        self.image = FitImage(allow_stretch = True, keep_ratio = True, size_hint_x = 0.3, pos_hint = {"center_y":.5})
        self.name_label = MDLabel(theme_text_color="Custom", text_color="teal", bold = True, theme_font_size = "Custom", font_size = sp(21))
        self.category_label = MDLabel(theme_text_color="Custom", text_color="purple", bold = True, theme_font_size = "Custom", font_size = sp(21))
        self.price_label = MDLabel(theme_text_color="Custom", text_color="green", bold = True, theme_font_size = "Custom", font_size = sp(21))
        self.desc_label = MDLabel(theme_text_color="Custom", text_color="blue", shorten=True, shorten_from='right', bold = True, theme_font_size = "Custom", font_size = sp(21))
        self.quantity_label = MDLabel(theme_text_color="Custom", text_color="tomato", bold = True, theme_font_size = "Custom", font_size = sp(21))

        self.item_container.add_widget(self.name_label)
        self.item_container.add_widget(self.category_label)
        self.item_container.add_widget(self.desc_label)
        self.item_container.add_widget(self.price_label)
        self.item_container.add_widget(self.quantity_label)
        self.item_container.add_widget(self.button_container)

        self.add_widget(self.image)
        self.add_widget(self.item_container)

        self.bind(prod_name=lambda inst, val: setattr(self.name_label, 'text', f"Name: {val}"))
        self.bind(prod_category=lambda inst, val: setattr(self.category_label, 'text', f"Category: {val}"))
        self.bind(prod_desc=lambda inst, val: setattr(self.desc_label, 'text', f"Description: {val}"))
        self.bind(prod_price=lambda inst, val: setattr(self.price_label, 'text', f"Price: Ksh. {val}"))
        self.bind(quantity=lambda inst, val: setattr(self.quantity_label, 'text', f"Quantity: {val}"))
        self.bind(product_image=lambda inst, val: setattr(self.image, 'source', val))

class ItemCard(MDCard):
    prod_name = StringProperty("")
    prod_desc = StringProperty("")
    prod_price = StringProperty("")
    product_image = StringProperty("")

    on_touched = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(150), dp(200))
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)
        self.on_release = lambda : self.on_touched()

        self.image = FitImage(allow_stretch = True, keep_ratio = True, size_hint_y = .5)
        self.name_label = MDLabel(theme_text_color="Custom", text_color="teal", bold = True, theme_font_size = "Custom", font_size = sp(15), halign = "center", size_hint_y = .1)
        self.category_label = MDLabel(theme_text_color="Custom", text_color="purple", bold = True, theme_font_size = "Custom", font_size = sp(15), halign = "center", size_hint_y = .1)
        self.price_label = MDLabel(theme_text_color="Custom", text_color="green", bold = True, theme_font_size = "Custom", font_size = sp(15), halign = "center", size_hint_y = .1)
        self.desc_label = MDLabel(theme_text_color="Custom", text_color="blue", shorten=True, shorten_from='right', bold = True, theme_font_size = "Custom", font_size = sp(15), halign = "center", size_hint_y = .1)
        self.quantity_label = MDLabel(theme_text_color="Custom", text_color="tomato", bold = True, theme_font_size = "Custom", font_size = sp(15), halign = "center", size_hint_y = .1)
        
        self.add_widget(self.image)
        self.add_widget(self.name_label)
        self.add_widget(self.desc_label)
        self.add_widget(self.price_label)

        self.bind(prod_name=lambda inst, val: setattr(self.name_label, 'text', val))
        self.bind(prod_desc=lambda inst, val: setattr(self.desc_label, 'text', val))
        self.bind(prod_price=lambda inst, val: setattr(self.price_label, 'text', f"Price: Ksh. {val}"))
        self.bind(product_image=lambda inst, val: setattr(self.image, 'source', val))


class UserCard(MDBoxLayout):
    user_name = StringProperty("")
    user_password = StringProperty("")
    user_role = StringProperty("")
    user_image = StringProperty("")

    on_edit = ObjectProperty(allownone=True)
    on_remove = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(190)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (.9, .9, .9, .8)

        self.user_container = MDBoxLayout(orientation="vertical", spacing=dp(5), size_hint_x = 0.7)
        self.button_container = MDGridLayout(cols = 3, spacing = dp(20))
        self.edit_user_button = MDButton(
            MDButtonText(text = "Edit", theme_text_color = "Custom", text_color = "white", bold = True), 
            MDButtonIcon(icon = "pencil-outline", theme_icon_color = "Custom", icon_color = "white"), 
            style = "outlined",
            theme_bg_color = "Custom", 
            md_bg_color = "green",
            on_release = lambda x: self.on_edit()
        ) 
        self.remove_user_button = MDButton(
            MDButtonText(text = "Remove", theme_text_color = "Custom", text_color = "white", bold = True), 
            MDButtonIcon(icon = "close", theme_icon_color = "Custom", icon_color = "white"), 
            style = "outlined",
            theme_bg_color = "Custom", 
            md_bg_color = "red",
            on_release = lambda x: self.on_remove()
        ) 
        self.button_container.add_widget(Widget())
        self.button_container.add_widget(self.edit_user_button)
        self.button_container.add_widget(self.remove_user_button)

        self.image = FitImage(allow_stretch = True, keep_ratio = True, size_hint_x = 0.3, pos_hint = {"center_y":.5})
        self.name_label = MDLabel(theme_text_color="Custom", text_color="teal", bold = True, theme_font_size = "Custom", font_size = sp(21))
        self.password_label = MDLabel(theme_text_color="Custom", text_color="purple", bold = True, theme_font_size = "Custom", font_size = sp(21))
        self.role_label = MDLabel(theme_text_color="Custom", text_color="green", bold = True, theme_font_size = "Custom", font_size = sp(21))

        self.user_container.add_widget(self.name_label)
        self.user_container.add_widget(self.password_label)
        self.user_container.add_widget(self.role_label)
        self.user_container.add_widget(self.button_container)

        self.add_widget(self.image)
        self.add_widget(self.user_container)

        self.bind(user_name=lambda inst, val: setattr(self.name_label, 'text', f"Name: {val}"))
        self.bind(user_password=lambda inst, val: setattr(self.password_label, 'text', f"Password: {val}"))
        self.bind(user_role=lambda inst, val: setattr(self.role_label, 'text', f"Role: {val}"))
        self.bind(user_image=lambda inst, val: setattr(self.image, 'source', val))

class AnalysisCard(MDBoxLayout):
    item_name = StringProperty("")
    item_category = StringProperty("")
    items_sold = StringProperty("")
    items_remain = StringProperty("")
    item_status = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)

        self.name_label = MDLabel(theme_text_color="Custom", text_color="teal", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.category_label = MDLabel(theme_text_color="Custom", text_color="purple", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.sold_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.remainder_label = MDLabel(theme_text_color="Custom", text_color="brown", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.status_label = MDLabel(bold = True, theme_font_size = "Custom", theme_text_color="Custom", text_color="green", font_size = sp(16), halign = "center")

        self.add_widget(self.name_label)
        self.add_widget(self.category_label)
        self.add_widget(self.sold_label)
        self.add_widget(self.remainder_label)
        self.add_widget(self.status_label)

        self.bind(item_name=lambda inst, val: setattr(self.name_label, 'text', val))
        self.bind(item_category=lambda inst, val: setattr(self.category_label, 'text', val))
        self.bind(items_sold=lambda inst, val: setattr(self.sold_label, 'text', val))
        self.bind(items_remain=lambda inst, val: setattr(self.remainder_label, 'text', val))
        self.bind(item_status=lambda inst, val: setattr(self.status_label, 'text', val))
        self.bind(item_status=self.on_status_change)

    def on_status_change(self, instance, value):
        self.status_label.text = value
        if value.lower() == "restock":
            self.status_label.text_color = "red"
        else:
            self.status_label.text_color = "green"


        
class TransactionsCard(MDBoxLayout):
    user_name = StringProperty("")
    item_name = StringProperty("")
    item_category = StringProperty("")
    item_quantity = StringProperty("")
    item_price = StringProperty("")
    date_sold = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)
        self.md_bg_color = (1, 1, 1, 1)

        self.user_name_label = MDLabel(theme_text_color="Custom", text_color="teal", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.item_name_label = MDLabel(theme_text_color="Custom", text_color="purple", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.category_label = MDLabel(theme_text_color="Custom", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.quantity_label = MDLabel(theme_text_color="Custom", text_color="blue", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.price_label = MDLabel(theme_text_color="Custom", text_color="brown", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")
        self.date_sold_label = MDLabel(theme_text_color="Custom", bold = True, theme_font_size = "Custom", font_size = sp(16), halign = "center")


        self.add_widget(self.user_name_label)
        self.add_widget(self.item_name_label)
        self.add_widget(self.category_label)
        self.add_widget(self.quantity_label)
        self.add_widget(self.price_label)
        self.add_widget(self.date_sold_label)

        self.bind(user_name=lambda inst, val: setattr(self.user_name_label, 'text', val))
        self.bind(item_name=lambda inst, val: setattr(self.item_name_label, 'text', val))
        self.bind(item_category=lambda inst, val: setattr(self.category_label, 'text', val))
        self.bind(item_quantity=lambda inst, val: setattr(self.quantity_label, 'text', val))
        self.bind(item_price=lambda inst, val: setattr(self.price_label, 'text', f"Ksh. {val}"))
        self.bind(date_sold=lambda inst, val: setattr(self.date_sold_label, 'text', val))

class POS(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images_path = resource_path('Images')
        self.icon = resource_path('Images/icon.png')
    def build(self):
        return Builder.load_file(resource_path('genpos.kv'))

    def on_start(self):
        database.add_admin()
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, 
            select_path=self.select_path, 
            preview=True
        )
        Clock.schedule_once(self.go_to_main, 8)

    def go_to_main(self, *args):
        self.root.current = 'intro'

    def user_dialog(self, role):
        self.username = MDTextField(MDTextFieldHintText(text='User Name'))
        self.password = MDTextField(MDTextFieldHintText(text='Password'), password=True)
        self.user_validator = MDLabel(text='', size_hint_y=None, height=dp(35), theme_text_color='Custom', text_color='red', halign='center')
        container = MDDialogContentContainer(spacing=dp(20), orientation='vertical')
        container.add_widget(self.username)
        container.add_widget(self.password)
        container.add_widget(self.user_validator)
        self.sign_in_dialog = MDDialog(
            MDDialogIcon(icon='account'), 
            MDDialogHeadlineText(text=f'Sign in as {role}'), 
            MDDialogSupportingText(text=f"You'll access all {role} privillages"), 
            container, 
            MDDialogButtonContainer(
                Widget(), 
                MDButton(
                    MDButtonText(text='Sign In'), 
                    on_release=lambda x: self.validate_user(role)
                ), 
                MDButton(
                    MDButtonText(text='Cancel'), 
                    on_release=lambda x: self.sign_in_dialog.dismiss()
                ), 
                spacing=dp(20)
            )
        )
        self.sign_in_dialog.open()

    def validate_user(self, role):
        users = database.session.query(database.User).filter_by(user_role = role.lower()).all()
        uname = self.username.text.strip().lower()
        psswrd = self.password.text.strip()
        if not users:
            self.user_validator.text = f"'{uname.capitalize()}' is not {role}!!!"
        for user in users:
            if uname.lower() == user.user_name:
                if psswrd == user.user_password:
                    if user.expiry_date < datetime.utcnow():
                        self.payment_dialog()
                        return
                    self.root.current = f"{role}_panel"
                    self.signed_in_user_id = user.user_id
                    self.show_products()
                    self.sign_in_dialog.dismiss()
                else:
                    self.user_validator.text = f"'{psswrd}' is not correct!!"
            else:
                self.user_validator.text = f"{uname} is not {role}!!"

    def show_users(self):

        users = database.session.query(database.User).all()

        self.root.ids.prev_fab_text.text = "Add User"
        self.root.ids.prev_fab_btn.on_release = lambda : self.new_user_dialog()
        self.root.ids.prev_fab_btn.disabled = False
        header = self.root.ids.admin_header
        footer = self.root.ids.admin_footer
        buttons = self.root.ids.btn_container

        header.height = dp(0)
        header.size_hint_y = None
        header.opacity = 0
        header.disabled = True

        footer.height = dp(0)
        footer.size_hint_y = None
        footer.opacity = 0
        footer.disabled = True
        
        buttons.height = dp(50)
        buttons.size_hint_y = None
        buttons.opacity = 1
        buttons.disabled = False

        prev = self.root.ids.admin_prev
        self.root.ids.rvb.default_size = (None, dp(300))
        data = []

        prev.viewclass = "UserCard"
        for user in users:
            data.append({
                'viewclass': "UserCard",
                'user_name': user.user_name,
                'user_password': user.user_password,
                'user_role': user.user_role,
                'user_image': resource_path("Images/admin.png") if user.user_role == "admin" else resource_path("Images/user.png"),
                'on_edit': lambda id = user.user_id, name = user.user_name, password = user.user_password, role = user.user_role: self.edit_users_dialog(id, name, password, role),
                'on_remove': lambda x=user.user_id: self.remove_user(x)
            })
        
        prev.data = data

    def show_products(self):

        items = database.session.query(database.Product).all()

        self.root.ids.prev_fab_text.text = "Add Product"
        self.root.ids.prev_fab_btn.on_release = lambda : self.item_dialog()
        self.root.ids.prev_fab_btn.disabled = False

        header = self.root.ids.admin_header
        footer = self.root.ids.admin_footer
        buttons = self.root.ids.btn_container

        header.height = dp(0)
        header.size_hint_y = None
        header.opacity = 0
        header.disabled = True

        footer.height = dp(0)
        footer.size_hint_y = None
        footer.opacity = 0
        footer.disabled = True

        buttons.height = dp(50)
        buttons.size_hint_y = None
        buttons.opacity = 1
        buttons.disabled = False
        
        prev = self.root.ids.admin_prev
        self.root.ids.rvb.default_size = (None, dp(300))
        data = []

        prev.viewclass = "ProductCard"

        for item in items:
            data.append({
                'viewclass': "ProductCard",
                'prod_name': item.prod_name,
                'prod_category': item.prod_category,
                'prod_desc': item.prod_desc,
                'prod_price': str(item.prod_price),
                'quantity': str(item.quantity),
                'product_image': item.product_image,
                'on_edit': lambda id = item.prod_id, name = item.prod_name, cat = item.prod_category, desc = item.prod_desc, price = item.prod_price, qty = item.quantity, img = item.product_image: self.edit_product_dialog(id, name, cat, desc, price, qty, img),
                'on_remove': lambda x=item.prod_id: self.remove_product(x)
            })
        
        prev.data = data


    def show_items(self):
        items = database.session.query(database.Product).all()
        prev = self.root.ids.standard_prev
        data = []
        prev.viewclass = "ItemCard"
        for item in items:
            data.append({
                "viewclass": "ItemCard",
                "prod_name": item.prod_name,
                "prod_desc": item.prod_desc,
                "prod_price": str(item.prod_price),
                "product_image": item.product_image,
                'on_touched': lambda name=item.prod_name, desc=item.prod_desc, price=item.prod_price, qty=item.quantity, date=item.date_added, img=item.product_image: self.preview_items(name, desc, price, qty, date, img)
            })
        
        prev.data = data

    def search_items(self, search_term):
        btn = self.root.ids.search_btn
        prev = self.root.ids.standard_prev
        if btn.icon != 'magnify':
            self.show_items()
            self.root.ids.search_btn.icon = 'magnify'
            self.root.ids.search_field.text = ''
        else:
            if not search_term:
                self.show_snack("Enter item to search")
                return
            items = database.session.query(database.Product).filter(database.Product.prod_name.ilike(f"%{search_term}%")).all()
            if not items:
                self.show_snack("Item not found!")
                return
            prev.clear_widgets()
            item_scroll = MDScrollView(pos_hint={'center_x': 0.5, 'center_y': 0.5})
            item_grid = MDGridLayout(
                cols=6, 
                spacing=dp(25), 
                padding=dp(10), 
                adaptive_height=True, 
                size_hint_y=None
            )
            item_grid.bind(minimum_height=item_grid.setter('height'))
            for item in items:
                print(item.prod_name)
                item_card = MDCard(
                    orientation='vertical', 
                    spacing=dp(10), 
                    padding=dp(4), 
                    size_hint=(None, None), 
                    size=(dp(150), dp(200)), 
                    theme_bg_color='Custom', 
                    md_bg_color=(1, 1, 1, 1), 
                    on_release=lambda btn, name=item.prod_name, desc=item.prod_desc, price=item.prod_price, qty=item.quantity, date=item.date_added, img=item.product_image: self.preview_items(name, desc, price, qty, date, img)
                )
                image = item.product_image
                img = FitImage(
                    source=image, 
                    size_hint=(None, None), 
                    size=(dp(100), dp(100)), 
                    radius=[dp(20)], 
                    pos_hint={'center_x': 0.5}
                )
                item_card.add_widget(img)
                pname = MDLabel(text=item.prod_name, halign='center', theme_text_color = "Custom", text_color = "teal")
                pdesc = MDLabel(text=item.prod_desc, shorten=True, shorten_from='right', halign='center', theme_text_color = "Custom", text_color = "navy")
                pprice = MDLabel(text=str(item.prod_price), halign='center', theme_text_color = "Custom", text_color = "purple")
                item_card.add_widget(pname)
                item_card.add_widget(pdesc)
                item_card.add_widget(pprice)
                item_grid.add_widget(item_card)
            item_scroll.add_widget(item_grid)
            prev.add_widget(item_scroll)
            self.root.ids.search_btn.icon = "close"
            self.root.ids.search_btn.icon_color = "red"



    def preview_items(self, name, desc, price, qty, date, img):
        prev = self.root.ids.item_prev
        prev.clear_widgets()
        box = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(4), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        pname = MDLabel(text=f'Name: {name}', size_hint_y=None, height=dp(30), theme_text_color = "Custom", text_color = "teal")
        pdesc = MDLabel(text=f'Description: {desc}', shorten=True, shorten_from='right', size_hint_y=None, height=dp(30), theme_text_color = "Custom", text_color = "blue")
        pprice = MDLabel(text=f'Price: Ksh. {str(price)}', size_hint_y=None, height=dp(30), theme_text_color = "Custom", text_color = "green")
        pqty = MDLabel(text=f'Quantity: {str(qty)}', size_hint_y=None, height=dp(30), theme_text_color = "Custom", text_color = "brown")
        pdate = MDLabel(text=f"Date Added: {str(date).split(' ')[0]}", size_hint_y=None, height=dp(30), theme_text_color = "Custom", text_color = "purple")
        image = img
        img_box = MDBoxLayout()
        pimg = FitImage(
            source=image, 
            allow_stretch=True, 
            keep_ratio=True, 
            pos_hint={'center_x': 0.5}
        )
        img_box.add_widget(pimg)
        box.add_widget(img_box)
        box.add_widget(pname)
        box.add_widget(pdesc)
        box.add_widget(pprice)
        box.add_widget(pqty)
        box.add_widget(pdate)
        box.add_widget(Widget(size_hint_y=None, height=dp(50)))
        prev.add_widget(box)

    def item_dialog(self):
        self.item_id = MDTextField(MDTextFieldHintText(text='Product Code: '))
        self.item_name = MDTextField(MDTextFieldHintText(text='Product Name: '))
        self.item_category = MDTextField(MDTextFieldHintText(text='Product Category: '))
        self.item_description = MDTextField(MDTextFieldHintText(text='Product Description: '))
        self.item_price = MDTextField(MDTextFieldHintText(text='Product Price: '), input_filter = "float")
        self.item_quantity = MDTextField(MDTextFieldHintText(text='Product Quantity: '), input_filter = "int")
        img_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(40))
        self.item_image = MDTextField(MDTextFieldHintText(text='Product Image: '), pos_hint = {'center_y':.5})
        img_box.add_widget(self.item_image)
        add_img_btn = MDButton(
            MDButtonText(text='Browse'), 
            pos_hint={'center_y': 0.5}, 
            on_release=lambda x: self.choose_image())
        img_box.add_widget(add_img_btn)
        container = MDDialogContentContainer(orientation='vertical', spacing=dp(20))
        container.add_widget(self.item_id)
        container.add_widget(self.item_name)
        container.add_widget(self.item_category)
        container.add_widget(self.item_description)
        container.add_widget(self.item_price)
        container.add_widget(self.item_quantity)
        container.add_widget(img_box)
        self.product_dialog = MDDialog(
            MDDialogIcon(icon='book'), 
            MDDialogHeadlineText(text='Add Items'), 
            container, 
            MDDialogButtonContainer(
                Widget(), 
                MDButton(MDButtonText(text='Add Item'), on_release=self.add_item), 
                MDButton(MDButtonText(text='Cancel'), on_release=lambda x: self.product_dialog.dismiss()), 
                spacing=dp(20)
            )
        )
        self.product_dialog.open()

    def add_item(self, *args):
        id = self.item_id.text.strip()
        name = self.item_name.text.strip()
        cat = self.item_category.text.strip()
        desc = self.item_description.text.strip()
        price = self.item_price.text.strip()
        qty = self.item_quantity.text.strip()
        img_url = self.item_image.text.strip()

        if not id.isdigit():
            self.show_snack("Invalid product ID!")
            return
        
        item = database.session.query(database.Product).filter_by(prod_id=int(id)).first()
        if item:
            self.show_snack(f'{id} already in use by {item.prod_name}!!')
        else:
            new_item = database.Product(
                prod_id = int(id) if id else 0,
                prod_name = name if name else "product_name",
                prod_category = cat if cat else "product_category",
                prod_desc = desc if desc else "product_description",
                prod_price = int(price) if price else 0,
                quantity = int(qty) if qty else 0,
                product_image = img_url if img_url else f"{self.images_path}/null_image.png",
            )
            database.session.add(new_item)
            database.session.commit()
            self.show_snack(f"{name} added successfully!!")
            self.show_products()

    def new_user_dialog(self):
        self.user_name = MDTextField(MDTextFieldHintText(text='User Name: '))
        self.user_password = MDTextField(MDTextFieldHintText(text='User Password: '))
        self.user_role = MDTextField(MDTextFieldHintText(text='User Role: '))
        self.worker_validator = MDLabel(text='', size_hint_y=None, height=dp(30), theme_text_color='Custom', text_color='red', halign='center')
        container = MDDialogContentContainer(orientation='vertical', spacing=dp(20))
        container.add_widget(self.user_name)
        container.add_widget(self.user_password)
        container.add_widget(self.user_role)
        container.add_widget(self.worker_validator)
        self.worker_dialog = MDDialog(MDDialogIcon(icon='account-plus'), MDDialogHeadlineText(text='Add Users?'), MDDialogSupportingText(text='Enter User Details: '), container, MDDialogButtonContainer(Widget(), MDButton(MDButtonText(text='Add User'), on_release=self.add_user), MDButton(MDButtonText(text='Cancel'), on_release=lambda x: self.worker_dialog.dismiss()), spacing=dp(20)))
        self.worker_dialog.open()

    def add_user(self, *args):
        uname = self.user_name.text.strip().lower()
        psswrd = self.user_password.text.strip()
        role = self.user_role.text.strip().lower()
        user = database.session.query(database.User).filter_by(user_name=uname).first()
        if user:
            self.show_snack(f'{uname} already exist as {user.user_name}!!')
            return
        new_user = database.User(
            user_name = uname,
            user_password = psswrd,
            user_role = role
        )
        database.session.add(new_user)
        database.session.commit()
        self.show_snack(f"{uname} added successfully!!")
        self.show_users()

    def preview_purchase(self, *args):
        prev = self.root.ids.purchase_prev
        prev.clear_widgets()
        self.root.current = 'purchase_screen'
        receipt_id = str(uuid.uuid4())[:8]
        prod_id = self.root.ids.prod_id_field.text.strip()
        if prod_id != '':
            item = database.session.query(database.Product).filter_by(prod_id=int(prod_id)).first()
            if item:
                item_box = MDBoxLayout()
                item_desc_box = MDBoxLayout(orientation='vertical', spacing=dp(10))
                image = FitImage(source=item.product_image, keep_ratio=True, allow_stretch=True, pos_hint={'center_y': 0.5})
                item_box.add_widget(image)
                name = MDLabel(text=item.prod_name, theme_text_color = "Custom", text_color = "teal")
                desc = MDLabel(text=item.prod_desc, theme_text_color = "Custom", text_color = "tomato")
                price = MDLabel(text=f'Ksh. {str(item.prod_price)}', theme_text_color = "Custom", text_color = "green")
                self.qty_field = MDTextField(MDTextFieldHintText(text='Quantity'), input_filter = "int")
                self.qty_field.on_text_validate = lambda user_id=self.signed_in_user_id, prod_id=item.prod_id, unit_price=item.prod_price, receipt_id=receipt_id: self.add_purchase(user_id, prod_id, unit_price, receipt_id)
                action_items = MDGridLayout(self.qty_field, cols=1, spacing=dp(20), padding=dp(10))
                item_desc_box.add_widget(Widget())
                item_desc_box.add_widget(name)
                item_desc_box.add_widget(desc)
                item_desc_box.add_widget(price)
                item_desc_box.add_widget(action_items)
                item_box.add_widget(item_desc_box)
                item_desc_box.add_widget(Widget())
                prev.add_widget(item_box)
            else:
                self.show_snack("Product not found!")
        else:
            self.show_snack("Enter product code!")

    def add_purchase(self, user_id, prod_id, unit_price, receipt_id, *args):
        prev = self.root.ids.receipt_prev
        item = database.session.query(database.Product).filter_by(prod_id=prod_id).first()
        if not hasattr(self, 'receipt_layout'):
            self.receipt_layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5), adaptive_height=True)
            self.receipt_index = 1
            self.total_value = 0
            self.receipt_layout.add_widget(MDLabel(text='ENTERPRISE RECEIPT', size_hint_y=None, height=dp(30), halign='center'))
            header = MDBoxLayout(spacing=dp(5), size_hint_y=None, height=dp(40))
            header.add_widget(MDLabel(text='Indx', halign='center', size_hint_x=0.15, bold=True))
            header.add_widget(MDLabel(text='Item', halign='center', size_hint_x=0.4, bold=True))
            header.add_widget(MDLabel(text='Qty', halign='center', size_hint_x=0.15, bold=True))
            header.add_widget(MDLabel(text='Price', halign='center', size_hint_x=0.3, bold=True))
            self.receipt_layout.add_widget(header)
            prev.clear_widgets()
            prev.add_widget(self.receipt_layout)
            prev.add_widget(Widget())
        quantity = int(self.qty_field.text.strip())
        if item.quantity > quantity:
            new_transaction = database.Transaction(user_id=user_id, prod_id=prod_id, quantity=quantity, unit_price=unit_price, receipt_id=receipt_id)
            database.session.add(new_transaction)
            receipt_row = MDBoxLayout(spacing=dp(2), size_hint_y=None, height=dp(30))
            receipt_row.add_widget(MDLabel(text=f'#{self.receipt_index}', halign='center', size_hint_x=0.15))
            receipt_row.add_widget(MDLabel(text=item.prod_name, halign='center', size_hint_x=0.4, shorten=True, shorten_from='right'))
            receipt_row.add_widget(MDLabel(text=str(quantity), halign='center', size_hint_x=0.15))
            total_price = item.prod_price * quantity
            receipt_row.add_widget(MDLabel(text=f'Ksh. {total_price}', halign='center', size_hint_x=0.3))
            self.receipt_layout.add_widget(receipt_row)
            self.receipt_layout.add_widget(MDDivider(color = "gold"))
            self.root.ids.calc_btn.on_release = lambda receipt_id=receipt_id: self.calculator(receipt_id)
            database.session.commit()
            item.quantity -= int(quantity)
            self.total_value += total_price
            self.receipt_index += 1
        else:
            self.show_snack(f"Insufficient {item.prod_name}s!")

    def calculator(self, receipt_id):
        total_value = database.session.query(func.sum(database.Transaction.quantity * database.Transaction.unit_price)).filter(database.Transaction.receipt_id == receipt_id).scalar()
        self.root.ids.total.text = f'Ksh. {str(total_value)}'
        paid = int(self.root.ids.paid.text.strip() if self.root.ids.paid.text.strip() else 0)
        bal = float(paid) - total_value
        self.root.ids.balance.text = f'Ksh. {str(bal)}'

    def remove_product(self, prod_id):
        prod = database.session.query(database.Product).filter_by(prod_id=prod_id).first()
        
        if not prod:
            self.show_snack(f'Product with ID {prod_id} not found!')
        else:
            try:
                database.session.delete(prod)
                database.session.commit()
                self.show_products()
            except IntegrityError:
                database.session.rollback()
                self.show_snack(f"'{prod.prod_name}' can't be deleted because it is used in one or more transactions.")


    def edit_product_dialog(self, prod_id, prod_name, prod_category, prod_desc, prod_price, prod_quantity, prod_img):
        self.edit_item_name = MDTextField(MDTextFieldHintText(text='Product Name: '), text=prod_name)
        self.edit_item_category = MDTextField(MDTextFieldHintText(text='Product Category: '), text=prod_category)
        self.edit_item_description = MDTextField(MDTextFieldHintText(text='Product Description: '), text=prod_desc)
        self.edit_item_price = MDTextField(MDTextFieldHintText(text='Product Price: '), text=str(prod_price), input_filter = "float")
        self.edit_item_quantity = MDTextField(MDTextFieldHintText(text='Product Quantity: '), text=str(prod_quantity), input_filter = "int")
        self.edit_item_image = MDTextField(MDTextFieldHintText(text='Product Image: '), text=prod_img)
        self.edit_item_validator = MDLabel(text='', size_hint_y=None, height=dp(30), theme_text_color='Custom', text_color='red', halign='center')
        container = MDDialogContentContainer(orientation='vertical', spacing=dp(20))
        container.add_widget(self.edit_item_name)
        container.add_widget(self.edit_item_category)
        container.add_widget(self.edit_item_description)
        container.add_widget(self.edit_item_price)
        container.add_widget(self.edit_item_quantity)
        container.add_widget(self.edit_item_image)
        container.add_widget(self.edit_item_validator)
        self.edit_item_dialog = MDDialog(
            MDDialogIcon(icon='pencil'), 
            MDDialogHeadlineText(text='Edit Items?'), 
            MDDialogSupportingText(text='Modify Item Details: '), 
            container, 
            MDDialogButtonContainer(
                Widget(), 
                MDButton(MDButtonText(text='Edit Item'), on_release=lambda x: self.edit_item(prod_id=prod_id)), 
                MDButton(MDButtonText(text='Cancel'), on_release=lambda x: self.edit_item_dialog.dismiss()), 
                spacing=dp(20)
            )
        )
        self.edit_item_dialog.open()

    def edit_item(self, prod_id, *kwargs):
        name = self.edit_item_name.text
        cat = self.edit_item_category.text
        desc = self.edit_item_description.text
        price = self.edit_item_price.text
        qty = self.edit_item_quantity.text
        img = self.edit_item_image.text
        item = database.session.query(database.Product).filter_by(prod_id=prod_id).first()
        item.prod_name = name
        item.prod_category = cat
        item.prod_desc = desc
        item.prod_price = float(price)
        item.quantity = int(qty)
        item.product_image = img
        database.session.commit()
        self.show_products()

    def remove_user(self, user_id):
        user = database.session.get(database.User, user_id)
        if not user:
            self.show_snack("User not found.")
            return

        try:
            database.session.delete(user)
            database.session.commit()
            self.show_snack(f"{user.user_name} deleted successfully.")
            self.show_users()
        except IntegrityError:
            database.session.rollback()
            self.show_snack(f"'{user.user_name}' can't be deleted since they are used in one or more transactions!")


    def edit_users_dialog(self, user_id, username, password, role):
        self.edit_user_name = MDTextField(MDTextFieldHintText(text='Username: '), text=username)
        self.edit_user_password = MDTextField(MDTextFieldHintText(text='Password: '), text=password)
        self.edit_user_role = MDTextField(MDTextFieldHintText(text='User Role: '), text=role)
        self.edit_user_validator = MDLabel(text='', size_hint_y=None, height=dp(30), theme_text_color='Custom', text_color='red', halign='center')
        container = MDDialogContentContainer(orientation='vertical', spacing=dp(20))
        container.add_widget(self.edit_user_name)
        container.add_widget(self.edit_user_password)
        container.add_widget(self.edit_user_role)
        self.edit_user_dialog = MDDialog(
            MDDialogIcon(icon='pencil'), 
            MDDialogHeadlineText(text='Edit Users?'), 
            MDDialogSupportingText(text='Modify User Details: '), 
            container, 
            MDDialogButtonContainer(
                Widget(), 
                MDButton(MDButtonText(text='Edit User'), on_release=lambda x: self.edit_user(user_id=user_id)), 
                MDButton(MDButtonText(text='Cancel'), on_release=lambda x: self.edit_user_dialog.dismiss()), 
                spacing=dp(20)
            )
        )
        self.edit_user_dialog.open()

    def edit_user(self, user_id, *kwargs):
        self.edit_user_dialog.dismiss()
        name = self.edit_user_name.text
        psswrd = self.edit_user_password.text
        role = self.edit_user_role.text
        user = database.session.query(database.User).filter_by(user_id=user_id).first()
        user.user_name = name
        user.user_password = psswrd
        user.user_role = role
        database.session.commit()
        self.show_users()

    def show_transactions(self):
        trans = database.session.query(database.Transaction).all()
        header = MDBoxLayout(size_hint_y=None, height=dp(40))
        trans_id = MDLabel(text='Cashier', halign='center', bold=True, theme_text_color = "Custom", text_color = "tomato")
        name = MDLabel(text='Prod Name', halign='center', bold=True, theme_text_color = "Custom", text_color = "tomato")
        cat = MDLabel(text='Prod Cat', halign='center', bold=True, theme_text_color = "Custom", text_color = "tomato")
        qty = MDLabel(text='Qty', halign='center', bold=True, theme_text_color = "Custom", text_color = "tomato")
        price = MDLabel(text='Price', halign='center', bold=True, theme_text_color = "Custom", text_color = "tomato")
        date = MDLabel(text='Date', halign='center', bold=True, theme_text_color = "Custom", text_color = "tomato")
        header.add_widget(trans_id)
        header.add_widget(name)
        header.add_widget(cat)
        header.add_widget(qty)
        header.add_widget(price)
        header.add_widget(date)

        ad_header = self.root.ids.admin_header
        footer = self.root.ids.admin_footer
        buttons = self.root.ids.btn_container
        ad_header.clear_widgets()
        ad_header.add_widget(header)

        ad_header.height = dp(50)
        ad_header.size_hint_y = None
        ad_header.opacity = 1
        ad_header.disabled = False

        footer.height = dp(0)
        footer.size_hint_y = None
        footer.opacity = 0
        footer.disabled = True
        
        buttons.height = dp(0)
        buttons.size_hint_y = None
        buttons.opacity = 0
        buttons.disabled = True

        prev = self.root.ids.admin_prev
        data = []

        self.root.ids.rvb.default_size = (None, dp(50))

        prev.viewclass = "TransactionsCard"
        for tran in trans:
            data.append({
                'viewclass': "TransactionsCard",
                'user_name': tran.user.user_name,
                'item_name': tran.product.prod_name,
                'item_category': tran.product.prod_category,
                'item_quantity': str(tran.quantity),
                'item_price': str(tran.unit_price*tran.quantity),
                'date_sold': str(tran.date).split(" ")[0]
            })
        
        prev.data = data
    def show_analysis(self):
        prev = self.root.ids.admin_prev
        items = database.session.query(database.Product).all()
        header = MDBoxLayout(size_hint_y=None, height=dp(40))
        name = MDLabel(text='Prod Name', halign='center', bold=True, theme_text_color = "Custom", text_color = "purple")
        cat = MDLabel(text='Prod Cat', halign='center', bold=True, theme_text_color = "Custom", text_color = "purple")
        sold_sto = MDLabel(text='Sold', halign='center', bold=True, theme_text_color = "Custom", text_color = "purple")
        rem_sto = MDLabel(text='Remaining Stock', halign='center', bold=True, theme_text_color = "Custom", text_color = "purple")
        status = MDLabel(text='Status', halign='center', bold=True, theme_text_color = "Custom", text_color = "purple")
        header.add_widget(name)
        header.add_widget(cat)
        header.add_widget(sold_sto)
        header.add_widget(rem_sto)
        header.add_widget(status)
        
        ad_header = self.root.ids.admin_header
        footer = self.root.ids.admin_footer
        buttons = self.root.ids.btn_container
        ad_header.clear_widgets()
        ad_header.add_widget(header)

        ad_header.height = dp(50)
        ad_header.size_hint_y = None
        ad_header.opacity = 1
        ad_header.disabled = False

        footer.height = dp(0)
        footer.size_hint_y = None
        footer.opacity = 0
        footer.disabled = True
        
        buttons.height = dp(0)
        buttons.size_hint_y = None
        buttons.opacity = 0
        buttons.disabled = True

        prev = self.root.ids.admin_prev
        data = []

        self.root.ids.rvb.default_size = (None, dp(50))

        prev.viewclass = "AnalysisCard"
        for item in items:
            data.append({
                'viewclass': "AnalysisCard",
                'item_name': item.prod_name,
                'item_category': item.prod_category,
                'items_sold': str(self.sold_sum(name=item.prod_name)),
                'items_remain': str(item.quantity),
                'item_status': "Sufficient" if item.quantity > 10 else "Restock"
            })
        
        prev.data = data

    def sold_sum(self, name):
        prods_sold = 0
        trans = database.session.query(database.Transaction).join(database.Product).filter(database.Product.prod_name == name).all()
        for tran in trans:
            sold = tran.quantity
            prods_sold += sold
        return prods_sold

    def choose_image(self):
        start_path = os.path.expanduser('~')
        self.file_manager.show(start_path)

    def select_path(self, path: str):
        self.item_image.text = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()

    def show_snack(self, text):
        MDSnackbar(
            MDSnackbarText(text=text), 
            pos_hint={'center_x': 0.5}, 
            size_hint_x=0.5, 
            orientation='horizontal'
        ).open()
    def payment_dialog(self):
        self.access_key = MDTextField(MDTextFieldHintText(text = "Access Key"))
        self.access_dialog = MDDialog(
            MDDialogIcon(icon = "cancel", theme_icon_color = "Custom", icon_color = "red"),
            MDDialogHeadlineText(text = "Your Plan Expired!!"),
            MDDialogSupportingText(text = "Enter access key: "),
            MDDialogContentContainer(
                self.access_key,
                MDLabel(text = "Call bellow for assistance: ", halign = "center"),
                MDLabel(text = "0737 841 451", theme_font_size = "Custom", font_size = sp(20), halign = "center", bold = True),
                orientation = "vertical",
                spacing = dp(20)
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = "Submit"),
                    on_release = self.validate_access
                ),
                Widget()
            ),
            auto_dismiss = False
        )
        self.access_dialog.open()
    def validate_access(self, *args):
        key = self.access_key.text.strip()
        SECRET_KEY = "DROSOPHILLAMELANOGASTER"

        try:
            username, expiry_str, checksum = key.split("|")
            data = f"{username}-{expiry_str}-{SECRET_KEY}"
            expected_checksum = hashlib.sha256(data.encode()).hexdigest()[:10].upper()

            if expected_checksum != checksum:
                self.show_snack("Invalid Access Key!")
                return

            user = database.session.query(database.User).filter_by(user_name=username.lower()).first()
            if not user:
                self.show_snack("User not found!")
                return

            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")

            users = database.session.query(database.User).all()
            for u in users:
                u.expiry_date = expiry_date

            database.session.commit()
            self.access_dialog.dismiss()
            self.show_snack("You've got free access for the next month. :-)")

        except Exception as e:
            self.show_snack(f"Validation Error: {e}")


from kivy.factory import Factory
Factory.register('ProductCard', cls=ProductCard)

POS().run()