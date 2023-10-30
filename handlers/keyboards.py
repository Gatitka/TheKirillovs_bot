from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)


# START PANEL keyboard
def get_start_kb() -> ReplyKeyboardMarkup:
    keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    keyboard_start.add('/menu')
    return keyboard_start


# START ADMIN-PANEL keyboard
def get_start_admin_kb() -> ReplyKeyboardMarkup:
    keyboard_admin_start = ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True)
    keyboard_admin_start.add('/menu').add('/admin-panel')
    return keyboard_admin_start


# MENU keyboard
def get_menu_kb() -> ReplyKeyboardMarkup:
    keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True)
    keyboard_menu.add('/add_expence').add('/report').add('/menu').add('/start')
    return keyboard_menu


# EXPENSES CATEGORY keyboard
def get_expenses_kb() -> InlineKeyboardMarkup:
    keyboard_exp = InlineKeyboardMarkup(resize_keyboard=True,
                                        one_time_keyboard=True)
    button3 = InlineKeyboardButton(text='🍽food', callback_data='food')
    button4 = InlineKeyboardButton(text='🚙auto', callback_data='auto')
    button5 = InlineKeyboardButton(text='🏕relax', callback_data='relax')
    button6 = InlineKeyboardButton(text='🤹‍♂️Stepa', callback_data='Stepa')
    button7 = InlineKeyboardButton(text='🎓education', callback_data='know-how')
    button8 = InlineKeyboardButton(text='🏠flat', callback_data='flat')
    button9 = InlineKeyboardButton(text='👘style', callback_data='style')
    button16 = InlineKeyboardButton(text='👩🏻‍🔬health', callback_data='health')
    button10 = InlineKeyboardButton(text='🔙cancel', callback_data='cancel')

    keyboard_exp.row(button3, button4, button5, button6)
    keyboard_exp.row(button7, button8, button9, button16)
    keyboard_exp.add(button10)
    return keyboard_exp


# ADMIN-PANEL keyboard
def get_admin_panel_kb() -> InlineKeyboardMarkup:
    keyboard_admin = InlineKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True)

    button11 = InlineKeyboardButton(text='create_tables',
                                    callback_data='create_tables')
    button12 = InlineKeyboardButton(text='add_user', callback_data='add_user')
    button13 = InlineKeyboardButton(text='delete_user',
                                    callback_data='delete_user')
    button14 = InlineKeyboardButton(text='add_admin',
                                    callback_data='add_admin')
    button15 = InlineKeyboardButton(text='del_admin',
                                    callback_data='delete_admin')
    button10 = InlineKeyboardButton(text='🔙cancel', callback_data='cancel')
    keyboard_admin.row(button12, button13)
    keyboard_admin.row(button14, button15)
    keyboard_admin.add(button11)
    keyboard_admin.add(button10)
    return keyboard_admin


# REPORT-PANEL keyboard
def get_report_kb() -> ReplyKeyboardMarkup:
    keyboard_report = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True)
    keyboard_report.add('/results_total_month').add('/details_day')
    keyboard_report.add('/details_month')
    return keyboard_report


# CANCEL keyboard
def get_cancel_kb() -> ReplyKeyboardMarkup:
    keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True,
                                          one_time_keyboard=True)
    keyboard_cancel.add('/cancel')
    return keyboard_cancel
