import asyncio
import random
import keyboards
import text

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# пусті елементи можна заповнити новими командами
modes = ('вихід', 'допомога', '', 'додавання', 'віднімання', '', 'казино', 'монетка', 'боулінг') 
# в змінній commands знаходяться коди деяких команд
commands = (20, 21, 30, 31)

# ці 4 словника потрібні щоб зберігати данні користувача так щоб вони були прив'язані к id
score = {}             
count_example = {}     
user_in_mode = {}      
user_answers = {}      

print('Введіть токен боту:')
token = input()
bot = Bot(f'{token}')
print('Все вірно починаємо запуск...')

dp = Dispatcher()

def get_random_number(min, max):
  return random.randrange(min, max)

def clear_all_info_in_id(id):
  if id in user_in_mode:
    user_in_mode.pop(id)
    
  if id in score:
    score.pop(id)

  if id in count_example:
    count_example.pop(id)

  if id in user_answers:
    user_answers.pop(id)

@dp.message(Command('start'))
async def start(message: Message):
  clear_all_info_in_id(message.from_user.id)
  
  await message.answer(f'{text.start_message}', reply_markup=keyboards.main_kb)
  await message.answer(f'{text.commands}')

@dp.message()
async def message_handler(message: Message):
  global score
  global count_example
  
  user_input = message.text.lower()
  user_id = message.from_user.id
  
  if user_input == modes[0] or user_input == '00':
    if user_id in user_in_mode:
      await message.answer(f'Ти вийшов із режиму "{user_in_mode[user_id]}".')
      clear_all_info_in_id(user_id)

    else:
      await message.answer(text.warning2)

  elif user_input == modes[1] or user_input == '01':
    clear_all_info_in_id(user_id)
    await message.answer(text.commands)

  elif user_input == modes[3] or user_input == '20':
    if user_id in user_in_mode:
      await message.answer(text.warning1)
      
    else:
      user_in_mode[user_id] = modes[3]
      x = get_random_number(0, 100)
      y = get_random_number(0, 100)
      # якщо відповідь має вигляд як команда в змінній commands, то перше число замінити
      if (x + y) in commands: 
        x += 5
      user_answers[user_id] = f'{x + y}'
      score[user_id] = 0
      count_example[user_id] = 1
      await message.answer(f'╓ \n╠═ Режим: ➕ Додавання \n╟ Тримай перший приклад \n╟ {x} + {y} = ? \n║ \n║ \n╙')

  elif user_input == modes[4] or user_input == '21':
    if user_id in user_in_mode:
      await message.answer(text.warning1)
      
    else:
      user_in_mode[user_id] = modes[4]
      x = get_random_number(0, 100)
      y = get_random_number(0, 100)
      # якщо відповідь має вигляд як команда в змінній commands, то перше число замінити
      if (x - y) in commands: 
        x -= 5
      user_answers[user_id] = f'{x - y}'
      score[user_id] = 0
      count_example[user_id] = 1
      await message.answer(f'╓ \n╠═ Режим: ➖ Віднімання \n╟ Тримай перший приклад \n╟ {x} - {y} = ? \n║ \n║ \n╙')

  elif user_input == modes[7] or user_input == '30':
    if user_id in user_in_mode:
      await message.answer(text.warning1)
      
    else:
      user_in_mode[user_id] = modes[7]
      await message.answer('╓ \n╠═ Режим: 🪙 Монетка \n╟ Ти розпочав гру "Монетка". \n╟ Обери "орел" або "решка" та напиши в чат. \n╙')

  elif user_input == modes[8] or user_input == '31':
    if user_id in user_in_mode:
      await message.answer(text.warning1)

    else:
      user_in_mode[user_id] = modes[8]
      user_answers[user_id] = 'ще'
      x = get_random_number(0, 11)
      await message.answer('Ти зайшов в режим боулінг. Щоб кинути в кеглі ще раз пиши команду "ще"')
      if x == 0:
        await message.answer('╓ \n╟ Кидок! 🎳 \n╟ Збито кегль: 0. \n╟ Спробуй ще. \n╙')
      
      elif x == 10:
        await message.answer('╓ \n╟ Кидок! 🎳 \n╟ Збито кегль: 10. \n╟ Strike! \n╙')

      else:
        await message.answer(f'╓ \n╟ Кидок! 🎳 \n╟ Збито кегль: {x}. \n╟ Залишилося: {10 - x}. \n╙')

  # якщо гравець не ввів команду та він знаходиться в якомусь режимі
  elif user_id in user_in_mode:
    if user_in_mode[user_id] == modes[3]:
      x = get_random_number(0, 100)
      y = get_random_number(0, 100)
      # якщо відповідь має вигляд як команда в змінній commands, то перше число замінити
      if (x + y) in commands: 
        x += 5
      if user_answers[user_id] == user_input:
        score[user_id] += 1
        count_example[user_id] += 1
        await message.answer(f'╓ \n╠═ Режим: ➕ Додавання \n╟ Вірно ✅ \n╟ Приклад {count_example[user_id]} \n╟ {x} + {y} = ? \n╟ Правильних відповідей: {score[user_id]} з {count_example[user_id]} \n╙')
        
      else:
        count_example[user_id] += 1
        await message.answer(f'╓ \n╠═ Режим: ➕ Додавання \n╟ Невірно ❌ \n╟ Приклад {count_example[user_id]} \n╟ {x} + {y} = ? \n╟ Правильних відповідей: {score[user_id]} з {count_example[user_id]} \n╙')
        
      user_answers[user_id] = f'{x + y}'

    elif user_in_mode[user_id] == modes[4]:
      x = get_random_number(0, 100)
      y = get_random_number(0, 100)
      # якщо відповідь має вигляд як команда в змінній commands, то перше число замінити
      if (x - y) in commands: 
        x -= 5
      if user_answers[user_id] == user_input:
        score[user_id] += 1
        count_example[user_id] += 1
        await message.answer(f'╓ \n╠═ Режим: ➖ Віднімання \n╟ Вірно ✅ \n╟ Приклад {count_example[user_id]} \n╟ {x} - {y} = ? \n╟ Правильних відповідей: {score[user_id]} з {count_example[user_id]} \n╙')

      else:
        count_example[user_id] += 1
        await message.answer(f'╓ \n╠═ Режим: ➖ Віднімання \n╟ Невірно ❌ \n╟ Приклад {count_example[user_id]} \n╟ {x} - {y} = ? \n╟ Правильних відповідей: {score[user_id]} з {count_example[user_id]} \n╙')

      user_answers[user_id] = f'{x - y}'

    elif user_in_mode[user_id] == modes[7]:
      # 0 - орел, 1 - решка
      x = get_random_number(0, 2) 
      if x == 0:
        user_answers[user_id] = 'орел'
      
      else:
        user_answers[user_id] = 'решка'
      
      if user_answers[user_id] == user_input:  
        await message.answer(f'╓ \n╠═ Режим: 🪙 Монетка \n╟ Випало: {user_answers[user_id]}. \n╟ Ти обрав: {user_input}. \n╟ Ти виграв! 😃 \n╟ Щоб повторити, напиши орел або решку в чат. 🔄 \n╙')

      elif user_input == 'орел' or user_input == 'решка':
        await message.answer(f'╓ \n╠═ Режим: 🪙 Монетка \n╟ Випало: {user_answers[user_id]}. \n╟ Ти обрав: {user_input}. \n╟ Ти програв ☹️ \n╟ Щоб повторити, напиши орел або решку в чат. 🔄 \n╙')
      
      else:
        await message.answer('Ти ввів неправильну команду. Напиши "решка" або "орел" щоб грати чи "вихід" щоб вийти.')

    elif user_in_mode[user_id] == modes[8]:
      if user_input == user_answers[user_id]:
        x = get_random_number(0, 11)
        if x == 0:
          await message.answer('╓ \n╟ Кидок! 🎳 \n╟ Збито кегль: 0. \n╟ Спробуй ще. \n╙')

        elif x == 10:
          await message.answer('╓ \n╟ Кидок! 🎳 \n╟ Збито кегль: 10. \n╟ Strike! \n╙')

        else:
          await message.answer(f'╓ \n╟ Кидок! 🎳 \n╟ Збито кегль: {x}. \n╟ Залишилося: {10 - x}. \n╙')

      else:
        await message.answer('Я не зрозумів твоєї команди. Напиши "ще" щоб продовжити, а бо "вихід" щоб вийти з режиму.')

  else:
    await message.answer('Мені не зрозуміло, що ти написав. Щоб переглянути доступні команди, напиши "допомога" або 01.')

async def main():
  await bot.delete_webhook(drop_pending_updates=True) 
  print('Бот працює!')
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())
