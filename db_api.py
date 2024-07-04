import sqlite3

db = None
cursor = None

def db_open():
    global db, cursor
    db = sqlite3.connect("heroes.db")
    cursor = db.cursor()
    cursor.execute("""PRAGMA foreign_keys=on""")

def db_close():
    db.commit()
    cursor.close()
    db.close()

def db_create():
    db_open()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        login VARCHAR,
                        password VARCHAR,
                        mail VARCHAR
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS hero(
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        info VARCHAR,
                        url_image VARCHAR,
                   strange INTEGER,
                   agility INTEGER,
                   intelegens INTEGER,
                   hp INTEGER,
                   manapool INTEGER,
                   attack VARCHAR,
                   armor FLOAT,
                   speed INTEGER,
                   distanse_attack INTEGER,
                        id_category INTEGER,
                        FOREIGN KEY (id_category) REFERENCES category(id)
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS spell(
                   id INTEGER PRIMARY KEY,
                   title VARCHAR,
                   info VARCHAR,
                   url_image VARCHAR,
                   id_hero INTEGER,
                        FOREIGN KEY (id_hero) REFERENCES hero(id)
                   )""")
    
    db_close()
 
def db_del():
    db_open()
    cursor.execute("""DROP TABLE user""")
    cursor.execute("""DROP TABLE spell""")
    cursor.execute("""DROP TABLE hero""")
    cursor.execute("""DROP TABLE category""")
    db_close()

#===================================== user =====================================================
def reg_user(name:str, login:str, password:str, mail:str):
    """login_user -> [id]"""
    last_id = None

    db_open()
    
    cursor.execute("""SELECT login, mail
                        FROM user
                        WHERE login == ? 
                            OR mail == ?
                    """,(login, mail))
    data = cursor.fetchall()

    if data == None or len(data) == 0:
        cursor.execute("""INSERT INTO user(name, login, password, mail)
                            VALUES (?, ?, ?, ?) 
                        """,(name, login, password, mail))
        last_id = cursor.lastrowid

    db_close()
    
    return last_id

def login_user(login:str, password:str):
    """login_user -> [id]"""
    db_open()
    cursor.execute("""SELECT id
                        FROM user
                        WHERE login == ? 
                            AND password == ?
                    """,(login,password))
    data = cursor.fetchone()
    db_close()
    return data

def get_user(id:int):
    """get_user -> [name, login, mail]"""
    db_open()
    cursor.execute("""SELECT name, login, mail
                        FROM user
                        WHERE id == ? 
                    """,(id,))
    data = cursor.fetchone()
    db_close()
    return data
#===================================== category =================================================
def add_category(title:str):
    "return id"
    db_open()
    cursor.execute("""INSERT INTO category(title)
                            VALUES (?)  
                   """,(title,))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_category(id:int):
    "id, title"
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                        WHERE id == ?  
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

def get_all_category():
    "id, title"
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                   """)
    data = cursor.fetchall()
    db_close()
    return data
#===================================== hero ==================================================
def add_hero(name:str, info:str, url_image:str, strange:int, agility:int, intelegens:int, hp:int, manapool:int, attack:str, armor:float, speed:int, distanse_attack:int, id_category:int):
    "add_hero -> id"
    db_open()
    cursor.execute("""INSERT INTO hero(name, info, url_image, strange, agility, intelegens, hp, manapool, attack, armor, speed, distanse_attack, id_category)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) 
                   """,(name, info, url_image, strange, agility, intelegens, hp, manapool, attack, armor, speed, distanse_attack, id_category))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_hero(id:int):
    " get_hero -> [id, name, info, url_image, strange, agility, intelegens, hp, manapool, attack, armor, speed, distanse_attack, id_category] "
    db_open()
    cursor.execute("""SELECT hero.id, hero.name, hero.info, hero.url_image, hero.strange, hero.agility, hero.intelegens, hero.hp, hero.manapool, hero.attack, hero.armor, hero.speed, hero.distanse_attack, category.title
                        FROM hero, category
                        WHERE hero.id_category == category.id
                        AND hero.id == ?  
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return [data]

def get_all_hero():
    " get_all_hero -> [(id, name, info, url_image, strange, agility, intelegens, hp, manapool, attack, armor, speed, distanse_attack, id_category), ...] "
    db_open()
    cursor.execute("""SELECT id, name, info, url_image, strange, agility, intelegens, hp, manapool, attack, armor, speed, distanse_attack, id_category
                        FROM hero
                   """)
    data = cursor.fetchall()
    db_close()
    return data

def get_form_category_hero(id_category:int):
    "get_form_category_hero -> [(id, name, info, url_image, strange, agility, intelegens, hp, manapool, attack, armor, speed, distanse_attack, id_category), ...] "
    db_open()
    cursor.execute("""SELECT *
                        FROM hero
                        WHERE id_category == ?  
                   """,(id_category,))
    data = cursor.fetchall()
    db_close()
    return data
#===================================== spell =================================================
def add_spell(title:str, info:str, url_image:str, id_hero:int):
    "return id"
    db_open()
    cursor.execute("""INSERT INTO spell(title, info, url_image, id_hero)
                            VALUES (?,?,?,?)  
                   """,(title, info, url_image, id_hero))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_spell(id:int):
    "id, title, info, url_image, id_hero"
    db_open()
    cursor.execute("""SELECT id, title, info, url_image, id_hero
                        FROM spell
                        WHERE id_hero == ?  
                   """,(id,))
    data = cursor.fetchall()
    db_close()
    return data

#===================================== create ===================================================
if __name__ == "__main__":
    db_del()
    db_create()
    if True:
        reg_user("name1", "login1", "password1", "mail1")
        reg_user("name2", "login2", "password2", "mail2")
        reg_user("name3", "login3", "password3", "mail3")

        add_category("СИЛА") # id = 1
        add_category("ЛОВКОСТЬ") # id = 2
        add_category("ИНТЕЛЕКТ") # id = 3
        add_category("УНИВЕРСАЛ") # id = 4

        add_hero("ABADDON",
                """Abaddon, способный лечиться за счёт вражеских атак, может пережить почти любое нападение. Он всегда готов вклиниться в битву, закрывая союзников щитом и запуская обоюдоострые витки мглы, которыми он увечит врагов и исцеляет товарищей.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/abaddon.png""",
                22,
                23,
                19,
                604,
                303,
                """40-50""",
                3.8,
                325,
                150,
                4)
        add_spell("MIST COIL",
                  """Ценой собственного здоровья герой выпускает смертельный туман, который наносит урон врагу или лечит союзника.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_death_coil.png""",
                  1)
        
        add_spell("APHOTIC SHIELD",
                  """Окружает союзника барьером из тёмной энергии, который поглощает некоторое количество урона. Если барьер пропадёт или его уничтожат, он взорвётся и нанесёт врагам вокруг урон, равный здоровью барьера. Применение снимает с цели оглушение и большинство отрицательных эффектов.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_aphotic_shield.png"""
                ,1)

        add_spell("CURSE OF AVERNUS",
                  """Атаки героя окутывают жертву ледяными чарами, которые замедляют её, наносят ей периодический урон и увеличивают скорость атаки у всех союзных существ, которые его атакуют. Наносит постройкам на 70% меньше периодического урона.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_frostmourne.png"""
                ,1)

        add_spell("BORROWED TIME",
                  """Обращает весь получаемый урон в лечение. Применение снимает большинство отрицательных эффектов. Если способность готова, то она сработает автоматически, как только здоровье владельца упадёт ниже 400.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_borrowed_time.png"""
                ,1)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

        add_hero("ABADDON2",
                """Abaddon, способный лечиться за счёт вражеских атак, может пережить почти любое нападение. Он всегда готов вклиниться в битву, закрывая союзников щитом и запуская обоюдоострые витки мглы, которыми он увечит врагов и исцеляет товарищей.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/abaddon.png""",
                22,
                23,
                19,
                604,
                303,
                """40-50""",
                3.8,
                325,
                150,
                1)
        add_spell("MIST COIL",
                  """Ценой собственного здоровья герой выпускает смертельный туман, который наносит урон врагу или лечит союзника.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_death_coil.png""",
                  2)
        
        add_spell("APHOTIC SHIELD",
                  """Окружает союзника барьером из тёмной энергии, который поглощает некоторое количество урона. Если барьер пропадёт или его уничтожат, он взорвётся и нанесёт врагам вокруг урон, равный здоровью барьера. Применение снимает с цели оглушение и большинство отрицательных эффектов.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_aphotic_shield.png"""
                ,2)

        add_spell("CURSE OF AVERNUS",
                  """Атаки героя окутывают жертву ледяными чарами, которые замедляют её, наносят ей периодический урон и увеличивают скорость атаки у всех союзных существ, которые его атакуют. Наносит постройкам на 70% меньше периодического урона.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_frostmourne.png"""
                ,2)

        add_spell("BORROWED TIME",
                  """Обращает весь получаемый урон в лечение. Применение снимает большинство отрицательных эффектов. Если способность готова, то она сработает автоматически, как только здоровье владельца упадёт ниже 400.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_borrowed_time.png"""
                ,2)

        add_hero("ABADDON3",
                """Abaddon, способный лечиться за счёт вражеских атак, может пережить почти любое нападение. Он всегда готов вклиниться в битву, закрывая союзников щитом и запуская обоюдоострые витки мглы, которыми он увечит врагов и исцеляет товарищей.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/abaddon.png""",
                22,
                23,
                19,
                604,
                303,
                """40-50""",
                3.8,
                325,
                150,
                2)
        add_spell("MIST COIL",
                  """Ценой собственного здоровья герой выпускает смертельный туман, который наносит урон врагу или лечит союзника.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_death_coil.png""",
                  3)
        
        add_spell("APHOTIC SHIELD",
                  """Окружает союзника барьером из тёмной энергии, который поглощает некоторое количество урона. Если барьер пропадёт или его уничтожат, он взорвётся и нанесёт врагам вокруг урон, равный здоровью барьера. Применение снимает с цели оглушение и большинство отрицательных эффектов.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_aphotic_shield.png"""
                ,3)

        add_spell("CURSE OF AVERNUS",
                  """Атаки героя окутывают жертву ледяными чарами, которые замедляют её, наносят ей периодический урон и увеличивают скорость атаки у всех союзных существ, которые его атакуют. Наносит постройкам на 70% меньше периодического урона.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_frostmourne.png"""
                ,3)

        add_spell("BORROWED TIME",
                  """Обращает весь получаемый урон в лечение. Применение снимает большинство отрицательных эффектов. Если способность готова, то она сработает автоматически, как только здоровье владельца упадёт ниже 400.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_borrowed_time.png"""
                ,3)

        add_hero("ABADDON4",
                """Abaddon, способный лечиться за счёт вражеских атак, может пережить почти любое нападение. Он всегда готов вклиниться в битву, закрывая союзников щитом и запуская обоюдоострые витки мглы, которыми он увечит врагов и исцеляет товарищей.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/abaddon.png""",
                22,
                23,
                19,
                604,
                303,
                """40-50""",
                3.8,
                325,
                150,
                3)
        add_spell("MIST COIL",
                  """Ценой собственного здоровья герой выпускает смертельный туман, который наносит урон врагу или лечит союзника.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_death_coil.png""",
                  4)
        
        add_spell("APHOTIC SHIELD",
                  """Окружает союзника барьером из тёмной энергии, который поглощает некоторое количество урона. Если барьер пропадёт или его уничтожат, он взорвётся и нанесёт врагам вокруг урон, равный здоровью барьера. Применение снимает с цели оглушение и большинство отрицательных эффектов.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_aphotic_shield.png"""
                ,4)

        add_spell("CURSE OF AVERNUS",
                  """Атаки героя окутывают жертву ледяными чарами, которые замедляют её, наносят ей периодический урон и увеличивают скорость атаки у всех союзных существ, которые его атакуют. Наносит постройкам на 70% меньше периодического урона.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_frostmourne.png"""
                ,4)

        add_spell("BORROWED TIME",
                  """Обращает весь получаемый урон в лечение. Применение снимает большинство отрицательных эффектов. Если способность готова, то она сработает автоматически, как только здоровье владельца упадёт ниже 400.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_borrowed_time.png"""
                ,4)

        add_hero("ABADDON5",
                """Abaddon, способный лечиться за счёт вражеских атак, может пережить почти любое нападение. Он всегда готов вклиниться в битву, закрывая союзников щитом и запуская обоюдоострые витки мглы, которыми он увечит врагов и исцеляет товарищей.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/abaddon.png""",
                22,
                23,
                19,
                604,
                303,
                """40-50""",
                3.8,
                325,
                150,
                3)
        add_spell("MIST COIL",
                  """Ценой собственного здоровья герой выпускает смертельный туман, который наносит урон врагу или лечит союзника.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_death_coil.png""",
                  5)
        
        add_spell("APHOTIC SHIELD",
                  """Окружает союзника барьером из тёмной энергии, который поглощает некоторое количество урона. Если барьер пропадёт или его уничтожат, он взорвётся и нанесёт врагам вокруг урон, равный здоровью барьера. Применение снимает с цели оглушение и большинство отрицательных эффектов.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_aphotic_shield.png"""
                ,5)

        add_spell("CURSE OF AVERNUS",
                  """Атаки героя окутывают жертву ледяными чарами, которые замедляют её, наносят ей периодический урон и увеличивают скорость атаки у всех союзных существ, которые его атакуют. Наносит постройкам на 70% меньше периодического урона.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_frostmourne.png"""
                ,5)

        add_spell("BORROWED TIME",
                  """Обращает весь получаемый урон в лечение. Применение снимает большинство отрицательных эффектов. Если способность готова, то она сработает автоматически, как только здоровье владельца упадёт ниже 400.

ТИП РАЗВЕИВАНИЯ: сильное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/abaddon_borrowed_time.png"""
                ,5)
        


        


