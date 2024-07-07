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
        
        add_hero("AXE",
                """Axe рубит одного врага за другим, неизменно ступая впереди своей команды. Он вынуждает противников вступить в бой, а затем отвечает на их удары смертоносными взмахами топора. Нещадно круша ослабленных врагов, он всегда несётся вперёд.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/axe.png""",
                25,
                20,
                18,
                670,
                291,
                """55-59""",
                3.3,
                315,
                150,
                1)
        add_spell("BERSERKER'S CALL",
                  """Герой бросает вызов ближайшим врагам, заставляя их атаковать его, а также получает бонус к броне на время действия способности.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/axe_berserkers_call.png""",
                6)
        
        add_spell("BATTLE HUNGER",
                  """Приводит врага в бешенство, нанося ему урон, пока он кого-нибудь не убьёт или действие способности не закончится. Урон от способности увеличивается в зависимости от брони владельца способности. Скорость передвижения жертвы уменьшается, когда она не смотрит в сторону владельца способности.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/axe_battle_hunger.png"""
                ,6)

        add_spell("COUNTER HELIX",
                  """После определённого числа полученных атак герой прокручивает вокруг себя топор, нанося чистый урон всем врагам неподалёку.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/axe_counter_helix.png"""
                ,6)

        add_spell("CULLING BLADE",
                  """Герой находит слабую точку врага и наносит ему чистый урон. Если убить этой способностью вражеского героя, её перезарядка сбрасывается, а все союзники поблизости временно получат дополнительную скорость передвижения и броню.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/axe_culling_blade.png"""
                ,6)
        
        add_hero("HUSKAR",
                """Чем меньше у Huskar здоровья, тем опаснее он становится. Своим ультом он мгновенно лишает себя и противника части здоровья, а на грани смерти может обрушить на своих врагов шквал горящих копий.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/huskar.png""",
                23,
                10,
                18,
                626,
                216,
                """44-49""",
                2.7,
                295,
                400,
                1)
        add_spell("INNER FIRE",
                  """Огненная ярость героя отталкивает всех врагов неподалёку на определённое расстояние от себя, наносит им урон и накладывает на них безмолвие.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/huskar_inner_fire.png""",
                7)
        
        add_spell("BURNING SPEAR",
                  """Герой жертвует частью здоровья, чтобы поджечь своё копьё и добавить к обычной атаке складывающийся периодический урон.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/huskar_burning_spear.png"""
                ,7)

        add_spell("BERSERKER'S BLOOD",
                  """Раны делают героя сильнее, увеличивая его скорость атаки, сопротивление магии и восстановление здоровья в зависимости от доли недостающего здоровья. Восстановление равно доле от силы героя.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/huskar_berserkers_blood.png"""
                ,7)

        add_spell("LIFE BREAK",
                  """Герой наносит огромный урон ценой собственного здоровья. Он прыгает на жертву, отнимая часть её текущего здоровья и замедляя её атаку и передвижение. Во время прыжка герой невосприимчив к эффектам и получает +60% к сопротивлению магии.

ТИП РАЗВЕИВАНИЯ: нормальное""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/huskar_life_break.png"""
                ,7)
        
        add_hero("PHANTOM ASSASSIN",
                """Phantom Assassin идёт в наступление, едва завидев свою жертву. Мгновенно сблизившись с ней, Мортред легко уклоняется от атак и обрушивает на врага удар за ударом, любой из которых может оказаться роковым.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/phantom_assassin.png""",
                19,
                21,
                15,
                538,
                255,
                """56-58""",
                4.5,
                310,
                150,
                2)
        add_spell("STIFLING DAGGER",
                  """Бросает кинжал, который замедляет скорость передвижения врага, наносит ему физический урон в размере 65 + 30% от атаки героя, а также накладывает эффекты предметов и способностей.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/phantom_assassin_stifling_dagger.png""",
                8)
        
        add_spell("PHANTOM STRIKE",
                  """Герой телепортируется к выбранному существу и, если это противник, получает дополнительную скорость атаки.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/phantom_assassin_phantom_strike.png"""
                ,8)

        add_spell("BLUR",
                  """Герой размывает свои очертания, становясь невидимым и передвигаясь быстрее, пока не совершит атаку или не приблизится к вражескому герою, башне или аванпосту.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/phantom_assassin_blur.png"""
                ,8)

        add_spell("COUP DE GRACE",
                  """Герой оттачивает свои боевые навыки, с каждой атакой имея шанс войти в состояние смертельного фокуса. В нём следующая атака гарантированно нанесёт критический урон и снимет фокус. Способность Stifling Dagger даёт фокус с повышенной вероятностью.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/phantom_assassin_coup_de_grace.png"""
                ,8)
        
        add_hero("BLOODSEEKER",
                """Bloodseeker постоянно ставит противников перед непростым выбором. Окропив кровью обширную территорию, он вынуждает врагов отступать, а под его чудовищным ультом жертва либо стоит на месте, либо погибает.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/bloodseeker.png""",
                24,
                24,
                17,
                648,
                279,
                """59-65""",
                6.0,
                285,
                150,
                2)
        add_spell("BLOODRAGE",
                  """Пробуждает в существе жажду крови, из-за которой оно атакует быстрее и наносит больше урона заклинаниями, но каждую секунду теряет долю от своего здоровья. Даёт союзным героям половину от скорости атаки.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/bloodseeker_bloodrage.png""",
                9)
        
        add_spell("BLOOD RITE",
                  """Герой окропляет выбранную область святой кровью. Через 2,9 сек. ритуал завершается, нанося противникам урон и запрещая им применять способности.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/bloodseeker_blood_bath.png"""
                ,9)

        add_spell("THIRST",
                  """Герой упивается ранениями противников, отчего его передвижение ускоряется, когда здоровье любого вражеского героя становится меньше 100%. Чем ниже уровень здоровья, тем сильнее эффект. Если здоровье вражеского героя упадёт ниже 25%, его станет видно в любой точке карты, даже если он невидим. Бонусы от разных противников складываются и позволяют превысить максимальную скорость передвижения.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/bloodseeker_thirst.png"""
                ,9)

        add_spell("RUPTURE",
                  """Разрывает кожу врага, нанося жертве начальный урон, зависящий от её текущего здоровья. Если цель передвигается, то она получает урон, зависящий от преодолённого расстояния.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/bloodseeker_rupture.png"""
                ,9)

        add_hero("LION",
                """Lion не даёт врагам выбраться из своей цепкой хватки. Он оглушает жертву каменными шипами и на время превращает её в безобидную зверушку. Если одних его заклинаний не хватит, чтобы расправиться с врагом, он обязательно даст команде достаточно времени.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/lion.png""",
                18,
                15,
                20,
                516,
                315,
                """49-55""",
                2.5,
                290,
                600,
                3)
        add_spell("EARTH SPIKE",
                  """Из земли прорывается полоса каменных шипов. Они подбрасывают врагов в воздух, а по приземлении оглушают их и наносят урон.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lion_impale.png""",
                10)
        
        add_spell("HEX",
                  """Превращает врага в безобидную зверюшку, блокируя все его способности.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lion_voodoo.png"""
                ,10)

        add_spell("MANA DRAIN",
                  """ПРЕРЫВАЕМАЯ — сосредотачивает свою магическую энергию, поглощая ману жертвы и замедляя её передвижение. Можно применять на союзника, чтобы передавать ему свою ману и ускорить его передвижение на 50%.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lion_mana_drain.png"""
                ,10)

        add_spell("FINGER OF DEATH",
                  """Разрывает вражеское существо, пытаясь вывернуть его наизнанку. Наносит большой урон, который увеличивается с каждым убитым этой способностью врагом.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lion_finger_of_death.png"""
                ,10)

        add_hero("LINA",
                """Опасная и хрупкая Lina легко свалит любого одинокого врага. Она поражает противников огнём и молнией, а каждое произнесённое ей заклинание увеличивает скорость её атаки, не давая выжить никому.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/lina.png""",
                20,
                23,
                30,
                560,
                435,
                """51-59""",
                3.8,
                290,
                670,
                3)
        add_spell("DRAGON SLAVE",
                  """Герой высвобождает дыхание дракона, сжигающее всех врагов на своём пути.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lina_dragon_slave.png""",
                11)
        
        add_spell("LIGHT STRIKE ARRAY",
                  """Призывает столб пламени, который оглушает врагов и наносит им урон.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lina_light_strike_array.png"""
                ,11)

        add_spell("FIERY SOUL",
                  """Увеличивает скорость атаки и передвижения всякий раз, когда герой попадает способностью по врагу. Эффекты способности складываются друг с другом. Действует 18 сек.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lina_fiery_soul.png"""
                ,11)

        add_spell("LAGUNA BLADE",
                  """Выпускает разряд молнии в одного врага, нанося сокрушительный урон.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/lina_laguna_blade.png"""
                ,11)
        
        add_hero("DAZZLE",
                """Рождённый поддерживать своих сторонников, Dazzle не даёт соратникам умереть, пока те уничтожают врагов. Его необычные заклинания вплетаются в броню, ослабляя противников и усиливая союзников.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/dazzle.png""",
                18,
                20,
                25,
                516,
                375,
                """47-53""",
                3.3,
                305,
                575,
                4)
        add_spell("POISON TOUCH",
                  """Выпускает конус яда, поражающий нескольких врагов. Наносит жертвам периодический урон и замедляет их, а атаки владельца способности обновляют время действия эффекта и усиливают замедление.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/dazzle_poison_touch.png""",
                12)
        
        add_spell("SHALLOW GRAVE",
                  """Накладывает на союзника священную защиту, не позволяющую ему умереть. Также увеличивает его лечение в зависимости от отсутствующего у него здоровья.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/dazzle_shallow_grave.png"""
                ,12)

        add_spell("SHADOW WAVE",
                  """Выпускает мощный заряд, который передаётся от союзника к союзнику, излечивая их и нанося урон противникам неподалёку. Способность всегда лечит своего владельца.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/dazzle_shadow_wave.png"""
                ,12)

        add_spell("BAD JUJU",
                  """Уменьшает перезарядки остальных способностей. Применение этой способности временно повышает расход здоровья на неё.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/dazzle_bad_juju.png"""
                ,12)
        
        add_hero("VENOMANCER",
                """Venomancer несёт своим врагам медленную смерть. Он взращивает бесконечную армию прыскающих ядом защитников, а стоит неприятелям показаться рядом, он выпускает огромное облако яда, надолго ослабляющего недругов.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/heroes/venomancer.png""",
                19,
                24,
                19,
                538,
                303,
                """42-45""",
                4.0,
                280,
                450,
                4)
        add_spell("VENOMOUS GALE",
                  """Выплёвывает в указанном направлении ядовитый шар, который наносит урон всем задетым врагам и отравляет их. Поражённые цели медленнее передвигаются, а также получают урон каждые 3 секунды действия способности.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/venomancer_venomous_gale.png""",
                13)
        
        add_spell("PLAGUE WARD",
                  """Призывает чумной тотем, атакующий вражеских существ и сооружения. Тотем невосприимчив к магии. Он имеет текущий уровень способности Poison Sting, нанося 50% от её урона.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/venomancer_plague_ward.png"""
                ,13)

        add_spell("POISON STING",
                  """Добавляет в обычные атаки героя яд, который наносит периодический урон и снижает скорость передвижения жертвы.""",
                  """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/venomancer_poison_sting.png"""
                ,13)

        add_spell("NOXIOUS PLAGUE",
                  """Накладывает на врага смертоносную заразу, которая наносит начальный урон, а затем наносит урон в зависимости от максимального здоровья цели. Зараза замедляет жертву и врагов рядом с ней — чем они ближе, тем замедление сильнее. Когда жертва умирает или действие способности заканчивается, все враги неподалёку получают такой же эффект заразы, который не передаётся другим существам.""",
                """https://cdn.akamai.steamstatic.com/apps/dota2/images/dota_react/abilities/venomancer_noxious_plague.png"""
                ,13)


