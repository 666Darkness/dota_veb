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
                  """Abaddon, способный лечиться за счёт вражеских атак, может пережить почти любое нападение. Он всегда готов вклиниться в битву, закрывая союзников щитом и запуская обоюдоострые витки мглы, которыми он увечит врагов и исцеляет товарищей.""",
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

        add_hero("ALCHEMIST",
                """Alchemist, синтезирующий дополнительные средства за каждое убийство, с лёгкостью получает необходимое вооружение. Он сражается во имя своей жадности, используя едкую кислоту и запас нестабильных химикатов.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/alchemist.png""",
                23,
                22,
                24,
                626,
                375,
                """50-56""",
                3.7,
                295,
                150,
                1)
        add_spell("ACID SPRAY",
                  """Распыляет в указанной области облако кислоты, которое наносит врагам периодический урон и снижает их броню.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/alchemist_acid_spray.png""",
                  2)
        
        add_spell("UNSTABLE CONCOCTION",
                  """Герой начинает встряхивать колбу с гремучей смесью, которую можно бросить во вражеского героя. При попадании колба взорвётся, оглушив всех противников в радиусе взрыва и нанеся им урон. Чем дольше смесь встряхивать, тем больше урона она нанесёт и тем дольше будет оглушение. Пока герой не бросит колбу, он передвигается быстрее. Максимальный эффект достигается после 5 сек., однако если не выбросить колбу через 5,5 секунды, она взорвётся в руках героя, подействовав и на него самого.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/alchemist_unstable_concoction.png"""
                ,2)

        add_spell("CORROSIVE WEAPONRY",
                  """Покрытое кислотой оружие героя снижает скорость передвижения и базовый урон у жертв его атак. Этот эффект складывается.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/alchemist_corrosive_weaponry.png"""
                ,2)

        add_spell("CHEMICAL RAGE",
                  """Особая химическая смесь разъяряет героя, отчего задержка перед его атакой уменьшается, а скорость его передвижения и восстановление здоровья увеличиваются.

ТИП РАЗВЕИВАНИЯ: нормальное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/alchemist_chemical_rage.png"""
                ,2)

        add_hero("JUGGERNAUT",
                """Juggernaut разрубает своих врагов шквалом рассекающих ударов. Мало кто сможет остановить или пережить его отчаянное наступление, ведь, набрав обороты, он становится практически неуязвимым.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/juggernaut.png""",
                20,
                34,
                14,
                560,
                243,
                """54-56""",
                5.7,
                300,
                150,
                2)
        add_spell("BLADE FURY",
                  """Герой крутится в вихре сокрушительных ударов клинком, становясь невосприимчивым к эффектам и получая +80% к сопротивлению магии. Наносит врагам поблизости урон с интервалом, соответствующим текущей скорости атаки, умноженной на 2. По окончании действия применяет на владельца сильное развеивание.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/juggernaut_blade_fury.png""",
                  3)
        
        add_spell("HEALING WARD",
                  """Призывает тотем, лечащий всех союзников неподалёку и передвигающийся со скоростью 325. Объём лечения зависит от максимального здоровья союзника. Действует 25 сек.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/juggernaut_healing_ward.png"""
                ,3)

        add_spell("BLADE DANCE",
                  """Даёт герою шанс нанести атакой критический урон.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/juggernaut_blade_dance.png"""
                ,3)

        add_spell("OMNISLASH",
                  """Герой прыгает к указанному врагу, а затем с повышенной скоростью атакует его и ближайших противников. На время действия способности герой становится неуязвимым.

ТИП РАЗВЕИВАНИЯ: нормальное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/juggernaut_omni_slash.png"""
                ,3)

        add_hero("CRYSTAL MAIDEN",
                """Crystal Maiden пригодится любой команде, ведь она даёт союзникам ману и не позволяет врагам сбежать. А когда представляется случай, она может уничтожить врагов своим сокрушительным ультом.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/crystal_maiden.png""",
                17,
                16,
                18,
                494,
                291,
                """48-54""",
                2.7,
                280,
                600,
                3)
        add_spell("CRYSTAL NOVA",
                  """Обдаёт выбранную область морозным ветром, который наносит врагам урон и замедляет их передвижение.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/crystal_maiden_crystal_nova.png""",
                  4)
        
        add_spell("FROSTBITE",
                  """Заковывает противника в лёд, нанося ему периодический урон и запрещая двигаться и атаковать. Наносит в 4 раза больше урона всем крипам, кроме древних.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/crystal_maiden_frostbite.png"""
                ,4)

        add_spell("ARCANE AURA",
                  """Увеличивает восстановление маны у всех союзников на карте. Действует в 3 раза сильнее на союзников в радиусе 1200.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/crystal_maiden_brilliance_aura.png"""
                ,4)

        add_spell("FREEZING FIELD",
                  """ПРЕРЫВАЕМАЯ — вокруг героя в течение 10 сек. происходят 100 случайных ледяных взрывов, замедляющих врагов и наносящих большой урон.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/crystal_maiden_freezing_field.png"""
                ,4)

        add_hero("SKYWRATH MAGE",
                """Смертоносный, но хрупкий Skywrath Mage быстро уничтожает врагов залпами мощной магии. Он сотрёт в порошок кого угодно благодаря своей способности обезмолвить противника, сделав его уязвимым к заклинаниям.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/skywrath_mage.png""",
                21,
                13,
                23,
                582,
                351,
                """39-49""",
                0.2,
                325,
                625,
                3)
        add_spell("ARCANE BOLT",
                  """Герой выпускает во врага медленный заряд магической энергии, который наносит урон, зависящий от интеллекта владельца способности. Попадание накладывает на жертву эффект, дающий владельцу способности дополнительный вампиризм от магического урона по ней.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/skywrath_mage_arcane_bolt.png""",
                  5)
        
        add_spell("CONCUSSIVE SHOT",
                  """Делает выстрел по ближайшему вражескому герою в большой области. При попадании наносит урон врагам в области действия и замедляет их. Крипам наносится 75% урона.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/skywrath_mage_concussive_shot.png"""
                ,5)

        add_spell("ANCIENT SEAL",
                  """Оставляет печать древней руны на выбранном существе, запрещая ему применять способности и увеличивая магический урон по нему""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/skywrath_mage_ancient_seal.png"""
                ,5)

        add_spell("MYSTIC FLARE",
                  """Герой создаёт направленное поле сверхъестественной силы, сокрушая врагов. Поле наносит огромный урон, который равномерно распределяется между героями в области действия в течение 2 сек.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/skywrath_mage_mystic_flare.png"""
                ,5)
        


        


