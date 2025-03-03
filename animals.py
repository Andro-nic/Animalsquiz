import os
from aiogram import Bot
from aiogram.types import FSInputFile
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
#переменные окружения
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)

#нулевой рейтинг животных
animals = {
        'Кинкажу': 0,
        'Сенегальский галаго': 0,
        'Амурский лесной кот': 0,
        'Малайский медведь': 0,
        'Лахтак': 0,
        'Ирбис': 0,
        'Андский кондор': 0}

# информация о животных для викторины
async def animal_info(chat_id, result):
    animals_data = {
        'Кинкажу': {
            'file_path': 'images/photo/kinkagu.jpeg',
            'facts': [
                "Ночная обезьяна, за любовь к сладкому получил прозвище «медовый медведь»."
                "Всю ночь проводят в поисках еды, возвращаясь в дупло лишь под утро",
                "Они сладкоежки и иногда в поисках мёда совершают набеги на гнезда пчёл.",
                "ЭКинкажу водятся в дождевых лесах Америки. Проводят свою жизнь на деревьях. ",
            ]
        },
        'Сенегальский галаго': {
            'file_path': 'images/photo/galago.jfif',
            'facts': [
                "Небольшой зверёк сероватой неприметной окраски с огромными глазами и огромными, очень подвижными ушами.",
                "Двигается - стремительными прыжками, отталкиваясь и приземляясь на задние конечности, не опираясь на передние.",
                "Огромные глаза помогают галаго видеть в темноте..",
                "Ушные раковины очень большие, они работают как локаторы, двигаясь независимо одна от другой."
            ]
        },
        'Амурский лесной кот': {
            'file_path': 'images/photo/lesnoy_kot.png',
            'facts': [
                "Подобно большинству видов кошачьих, дальневосточные лесные коты одиночки.",
                "Животные гораздо активнее весной, летом и в начале осени - в бесснежный период.",
                "Первые упоминания и описания этого животного появились в 1871 году.",
                "Окраска шерсти грязновато-серая с рыжим оттенком, по всему телу пятнистая, по спине идёт 3-4 узких полосы."
            ]
        },
        'Малайский медведь': {
            'file_path': 'images/photo/malayskiy_medved.jpg',
            'facts': [
                "Малайский медведь является одним из самых редких видов медведей.",
                "В длину он не превышает 1,4 м, высота в холке около 70 см, а масса тела от 30 до 65 кг.",
                "Вокальный репертуар бируангов разнообразен. Они ворчат и сопят, изредка могут издавать короткий лай.",
                "Очень любят мишки инжир, плоды тутовника, фисташки, фейхоа, едят сердцевину кокосовых пальм. "
            ]
        },
        'Лахтак': {
            'file_path': 'images/photo/morskoy_zayac.jpeg',
            'facts': [
                "Лахтак – медлительный и грузный зверь, один из самых крупных представителей семейства настоящих тюленей.",
                "Масса тела изменчива в зависимости от упитанности и по сезонам и может достигать зимой 360 кг.",
                "Они могут нырять на довольно большую глубину (более 100 метров) и оставаться под водой довольно долго – до 20 минут.",
                "Название «морской заяц», предположительно, дали зверю русские зверобои за пугливость и манеру передвигаться по суше прыжками."
            ]
        },
        'Ирбис': {
            'file_path': 'images/photo/irbis.jpeg',
            'facts': [
                "Ирбис обитает в горных районах Азии от Афганистана до западного Китая, в горах Монголии, на Алтае.",
                "Основу питания ирбиса составляют крупные копытные: сибирский горный козёл, архар.",
                "За один раз он съедает всего 2-3 кг мяса.",
                "Он может совершать прыжки до 10 метров в длину и до 3 – в высоту."
            ]
        },
        'Андский кондор': {
            'file_path': 'images/photo/andskiy_kondor.jpeg',
            'facts': [
                "Самая крупная хищная птица. Один из самых ярких символов Анд.",
                "Длина его тела колеблется от 117 до 135 см, размах крыльев – 274-310 см. Вес  достигает 7,5-15 кг.",
                "В поисках пищи они облетают большие пространства, покрывая в день до 200 км.",
                "В ежедневный рацион кондора в Московском зоопарке входит 1,5-1,7 кг мяса, 200 г рыбы и 1-2 крысы."
            ]
        }
    }

    # получаем данные для животного
    animal = animals_data.get(result)
    if animal:
        file_path = animal['file_path']
        facts = animal['facts']

        # отправляем изображение
        photo = FSInputFile(file_path)
        await bot.send_photo(chat_id, photo)

        # формируем и отправляем текст с описанием
        facts_text = "Интересные факты:\n" + "\n".join([f"— {fact}" for fact in facts])
        await bot.send_message(chat_id, facts_text)



animal_images = {
        'Кинкажу': 'images/photo/kinkagu.jpeg',
        'Сенегальский галаго': 'images/photo/galago.jfif',
        'Амурский лесной кот': 'images/photo/lesnoy_kot.png',
        'Малайский медведь': 'images/photo/malayskiy_medved.jpg',
        'Лахтак': 'images/photo/morskoy_zayac.jpeg',
        'Ирбис': 'images/photo/irbis.jpeg',
        'Андский кондор': 'images/photo/andskiy_kondor.jpeg'}