import aiogram

from handlers import admin, expences, other, report
from dispatcher import dp

other.register_handlers_other(dp)
admin.register_handlers_admin(dp)
report.register_handlers_report(dp)
expences.register_handlers_expences(dp)



if __name__ == "__main__":

    aiogram.executor.start_polling(dp, skip_updates=True)
