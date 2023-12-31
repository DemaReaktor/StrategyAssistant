from Language import LanguageController
from Keyboards import Keyboards
from Visualizer import Visualizer
from BotWithUsers import BotWithUsers
import Config

# create telegram bot
bot = BotWithUsers(Config.BOT_TOKEN)

texts = {
    'мову змінено на українську' : 'language is English now',
    'вкажаіть що саме вас цікавить' : 'choose one of variations',
    'що робить бот':['Бот створює стратегію за вашими налаштуваннями, потім пропускає її по історичним даним, тобто '
                     'цінах вказаної крипти і виводить результат.','Bot crete strategy with your settings. Then bot use '
                    'historical prices of this crypta and in the end show result'],
    'суть стратегії': ['Стратегія полягає в поділі капіталу на 5 частин, різниця між частинами визначається в'
                       ' налаштвуаннях і є за замовчуванням 2%. Для кожної частини створюється ордер купівлі, відстань'
                       ' між ордерами також визначається в налаштвуаннях і є за замовчуванням 8.5%. Перший ордер'
                       ' ставиться на початковій ціні, решта нижче. Після купівлі певного ордеру отримана крипта створює'
                       ' новий ордер продажі на ціні вище на відстань(за замовчуванням 8.5%). Після продажу створюється'
                       ' новий ордер купівлі на старій ціні купівлі з тою ж сумою. В кінці стратегія скасовує всі ордери'
                       ' і продає всю наявну крипту по теперішній ціні.',''],
    'як налаштувати стратегію': ['Щоб розпочати стратегію, треба нажати команду "/start_strategy", після цього буде'
                                 ' виведено меню. Кнопка "почати" запустить стратегію, остальні кнопки змінюють'
                                 ' налаштування стратегії відповідно до назви. Якщо нажмете одну з кнопок налаштування,'
                                 ' вам буде запропоновано вказати нові значення для налаштування.',''],
    'які обмеження в стратегії': ['Обмеження стосуються налаштувань:\n1.початок стратегії має бути до кінця стратегії.\n'
                                  '2.кількість цін має бути менше 500, наприклад проміжок часу 1-31 січня, а інтервал'
                                  '1 день, отже цін всього 31. Інакше бот покаже результати за останьою 500-ю ціною.\n'
                                  '3.відстань може бути лише до 2%.\n'
                                  '4.різниця може бути лише до 10%.\n'
                                  '5.значення інтервалу можуть бути 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d,'
                                  ' 3d, 1w',''],
    'Стратегія':['Кнопка "почати" розпочне стратегію. Ви можете змінити налаштування стратегії за допомою інших кнопок.'
                 ' Початок - день, з якого стратегія почне відлік. Кінець відповідно - на якому закінчить. Інтервал'
                 ' вказує, який інтервал між цінами береться. Наприклад 1d означає що ціни буруться по одній на день.'
                 ' Відстань - відстань між ордерами. Різниця - різниця між частинами капіталу. Щоб зрозуміти більше,'
                 ' пропишіть команду /help і виберіть суть стратегії або які обмеження в стратегії',''],
    'Налаштування':['зміни збереглись, можете далі налаштовувати або ж розпочати',''],
    'Завантаження...':'Loading...'
}
LanguageController.add(texts)


@bot.message_handler(commands=["start"])
async def cmd_start(message):
    await bot.send_message(message.chat.id, "Привіт, " + message.from_user.first_name)
    bot.add_user(message.from_user.id)

@bot.message_handler(commands=["change_language"])
async def cmd_change_language(message):
    if not bot.get_user(message.from_user.id):
        await bot.send_message(message.chat.id, 'будь-ласка спочатку напишіть /start')
        return
    bot.get_user(message.chat.id).lang.change()
    text = translate(message,'мову змінено на українську')
    await bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["help"])
async def cmd_help(message):
    if not bot.get_user(message.from_user.id):
        await bot.send_message(message.chat.id, 'будь-ласка спочатку напишіть /start')
        return
    keyboard = Keyboards.main_keyboard(bot.get_user(message.from_user.id).lang)
    await bot.send_message(message.chat.id, translate(message,"вкажаіть що саме вас цікавить"),
                     reply_markup=keyboard)

@bot.message_handler(commands=["strategy"])
async def cmd_strategy(message):
    if not bot.get_user(message.from_user.id):
        await bot.send_message(message.chat.id, 'будь-ласка спочатку напишіть /start')
        return
    keyboard = Keyboards.strategy_keyboard(bot.get_user(message.from_user.id).lang)
    text = translate(message, 'Стратегія')
    id = message.chat.id
    await bot.send_message(id, text,reply_markup= keyboard)

@bot.message_handler()
async def message(message):
    user = bot.get_user(message.from_user.id)
    if user.variant is None:
        await bot.send_message(message.chat.id, translate(message,'якщо хочеш поговорити, є чат GPT і справжні люди,'
                                                        'я лише бот.'))
        return
    if user.variant in ['pair','start','end','interval','distance','difference_capital','summa']:
        error = user.try_set_settings(user.variant, message.text)
        user.variant = None
        text = translate(message, "Налаштування" if error is None else error)
        keyboard = Keyboards.strategy_keyboard(bot.get_user(message.from_user.id).lang)
        await bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
async def correct_cmd(call):
    if not bot.get_user(call.from_user.id):
        await bot.send_message(call.message.chat.id, 'будь-ласка спочатку напишіть /start')
        return
    user = bot.get_user(call.from_user.id)
    if call.data in ['що робить бот', 'суть стратегії', 'як налаштувати стратегію' , 'які обмеження в стратегії']:
        text = translate(call.from_user.id, call.data)
        await bot.edit_message_text(text,chat_id= call.message.chat.id,message_id= call.message.id,
                              reply_markup=call.message.reply_markup)
        return
    if call.data == 'почати':
        new_message = await bot.send_message(call.message.chat.id, translate(call.from_user.id, 'Завантаження...'))
        (text, summas, dates) = user.start_strategy()
        await bot.edit_message_text(translate(call.from_user.id, text), call.message.chat.id, new_message.id)
        visual = Visualizer([(1 + element) * float(user.strategy_args['summa']) for element in summas])
        visual.plot()
        visual.save_picture(f'{user.id}.png')
        img = open(f'{user.id}.png', 'rb')
        await bot.send_photo(call.message.chat.id, img)
        return
    if call.data in ['pair', 'start', 'end', 'interval', 'distance', 'difference_capital','summa']:
        user.variant = call.data
        if call.data == 'summa':
            await bot.send_message(call.message.chat.id, translate(call.from_user.id,'Ведіть суму, наприклад: 100, 500'))
            return
        if call.data == 'pair':
            await bot.send_message(call.message.chat.id, translate(call.from_user.id,'Ведіть пару, наприклад: BTCUSDT або ETHUSDT'))
            return
        if call.data in ['start','end']:
            await bot.send_message(call.message.chat.id, translate(call.from_user.id, 'Ведіть дату( день-місяць-рік'
                ' (додатково можна година:хвилина)). наприклад: 01-01-2022, 06:45 25-11-2023'))
            return
        if call.data == 'interval':
            await bot.send_message(call.message.chat.id, translate(call.from_user.id,'Ведіть інтервал(1m або 3m або'
                    ' 5m або 15m або 30m або 1h або 2h або 4h або 6h або 8h або 12h або 1d або 3d або 1w)'))
            return
        if call.data == 'pair':
            await bot.send_message(call.message.chat.id, translate(call.from_user.id,'Ведіть пару, наприклад: BTCUSDT або ETHUSDT'))
            return
        if call.data == 'distance':
            await bot.send_message(call.message.chat.id, translate(call.from_user.id,'Ведіть число від 0 до 0.2,'
                                                                               ' наприклад: 0.1, 0.05'))
            return
        await bot.send_message(call.message.chat.id, translate(call.from_user.id,'Ведіть число від 0 до 0.25, '
                                                                           'наприклад: 0.05 або 0.21 або 0.1567'))
        return
    if call.data == 'show settings':
        await bot.edit_message_text(translate(call.from_user.id, call.message.text + '\n\nНалаштування:\n' +
                                        user.show_settings()), chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    reply_markup=call.message.reply_markup)


def translate(value, text):
    if not isinstance(value, int):
        value = value.from_user.id
    return bot.get_user(value).lang.translate(text)
