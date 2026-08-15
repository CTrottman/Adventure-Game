from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
from random import randint

hide_debug_information()
set_website_title("Adventure D&D")
set_website_framed(False)

@dataclass
class Job:
    name:str
    max_health: float
    
@dataclass
class Weapon:
    name:str
    damage: int
    cost:int
    
@dataclass
class State:
    name:str
    health:float
    job:Job
    invintory:list[Weapon]
    money:int
    has_key: bool
    enemy_health: float
    

#This defines the 'jobs' that players can choose from.
Archer = Job("archer",90.0)
Fighter = Job("fighter",120.0)
Mage = Job("mage",50.0)
Tank = Job("tank",150.0)
Unemployed = Job("unemployed",100.0)

#These are the  weapons available for each job, in the same order as the jobs above
simple_bow = Weapon("simple bow", 25, 4)
sturdy_knife = Weapon("sturdy knife",30,10)
complex_crossbow = Weapon("complex crossbow", 40, 20)
simple_spear = Weapon("simple spear", 20, 4)
reliable_sword = Weapon("reliable sword", 25, 10)
masterful_halbierd = Weapon("masterful halbierd", 35, 25)
simple_staff = Weapon("simple staff", 30, 4)
spell_book = Weapon("spell book", 40, 25)
arcane_orb = Weapon("arcane orb",90, 50)
simple_mace = Weapon("simple mace",15, 4)
war_hammer = Weapon("war hammer", 20, 15)
battle_axe = Weapon("battle axe", 30, 25)

store_weapons = [sturdy_knife, complex_crossbow, reliable_sword, masterful_halbierd, spell_book, arcane_orb, war_hammer, battle_axe]


@route
def index(state: State) -> Page:
    """ The start page of the  game, letting the player create their charicter. """
    return Page(state,[
        "Welcome to the adventure! What is your name?",
        TextBox("name","Adventurer"),
        "And what do you do?",
        SelectBox("job_select",["Archer","Fighter","Mage","Tank"]),
        Button("Confirm",create)
        ])

@route
def create(state: State, name:str, job_select:str)-> Page:
    """A way to show the player a little about the job that they chose, and a chance to change."""
    state.name = name
    if job_select == "Archer":
        state.job = Archer
        return Page(state,[
            "so you are "+ name +" the archer?",
            "Archers primarally use ranged weapons, such as bows, in order to fend off opponents",
            Button("Begin",background),
            Button("Cancel", reset)
            ])
    elif job_select == "Fighter":
        state.job = Fighter
        return Page(state,[
            "so you are "+ name +" the fighter?",
            "Fighters primarally use fast, light weapons, such as swords, in order to fend off opponents",
            Button("Begin",background),
            Button("Cancel", reset)
            ])
    elif job_select == "Mage":
        state.job = Mage
        return Page(state,[
            "so you are "+ name +" the mage?",
            "Mages primarally use sources of magic, such as staffs, in order to fend off opponents",
            Button("Begin",background),
            Button("Cancel", reset)
            ])
    elif job_select == "Tank":
        state.job = Tank
        return Page(state,[
            "so you are "+ name +" the tank?",
            "Tanks primarally use heavy weapons, such as hammers, in order to fend off opponents",
            Button("Begin",background),
            Button("Cancel", reset)
            ])
@route
def reset(state:State)-> Page:
    '''
    resets the game, can happen for a multitude of reasons. The player could die, or choose to restart.
    '''
    state.invintory.clear()
    return index(State("",Unemployed,100.0,[],5,False,80.0))


@route
def background(state:State)-> Page:
    '''
    provides exposition to the player.
    '''
    return Page(state,[
        "Welcome " + state.name + " to the land of Aarorus.",
        "This land has saddly been plauged by some evil, whose nature is unkown to most.",
        "Word has traveled wide of this evil, and of the treasures that were suposedly claimed by it.",
        "Hense your arrival.",
        "Whether you are here for the treasure or to free the evil shadows over this land,"
        "you are here to help. Thank you.",
        Button("Procede",procede)
        ])

@route
def procede(state:State)->Page:
    '''
    sets the players starting gear and stats.
    '''
    if state.job == Archer:
        state.invintory.append(simple_bow)
        state.health=state.job.max_health
    elif state.job == Fighter:
        state.invintory.append(simple_spear)
        state.health=state.job.max_health
    elif state.job == Mage:
        state.invintory.append(simple_staff)
        state.health=state.job.max_health
    elif state.job == Tank:
        state.invintory.append(simple_mace)
        state.health=state.job.max_health
    return crossroads(state)

@route
def crossroads(state:State)->Page:
    '''
    The main crossroads of the game, allows the player to traverse between the different areas.
    '''
    return Page(state,[
        "You find yourself at a crossroads.",
        "The paths ahead of you are labled with signs.",
        "Where will you choose to go?",
                Button("Cave",cave_entry),
        Button("Woods",woods),
        Button("Town",town),
        Image("field.png")
        ])

@route
def cave_entry(state:State)->Page:
    '''
    Gives the player an explenation of the fight they're about to go into, and a chance to flee.
    '''
    return Page(state,[
        "You stumble into the cave.",
        "You find that this cave is a theives den.",
        "One of the theives is home and attacks you.",
        Button("Fight",cave_fight,arguments=[Argument(name="turn", value=0)]),
        Button("Flee",crossroads)
        ])

@route
def cave_fight(state:State,turn:int)->Page:
    '''
    Does damage to the player, and reports it, allowing the player to fight or flee.
    '''
    if turn == 0:
        state.enemy_health = 80.0
    contents = ["You have " + (str((state.health/state.job.max_health)*100))[:5] +" percent health"]
    if state.health <=0:
        return player_dead(state)
    if turn !=0:
        if state.job == Archer:
            state.health -= randint(3,20)
        elif state.job == Fighter:
            state.health -= randint(5,15)
        elif state.job == Mage:
            state.health -= randint(10,20)
        elif state.job == Tank:
            state.health -= randint(20,30)
    contents.append("The thief attacks you.")
    if turn != 0:
        contents.append("You hit the thief.")
    turn += 1
    contents.append("What will you do?")
    contents.append(Button("Fight",cave_attack,arguments=[Argument(name="turn", value=turn)]))
    contents.append(Button("Flee",crossroads))
    contents.append(Image("thief.png"))
    return Page(state,contents)


@route
def cave_attack(state:State,turn:int):
    '''
    Does damage to the thief, and gives the player a reward if the thief is defeated.
    '''
    state.enemy_health -= ((state.invintory[-1].damage)+randint(-5,10))
    if state.enemy_health <=0:
        loot = randint(1,3)
        if state.job == Archer:
            if loot == 1:
                state.invintory.append(Weapon("Stolen Bow",20,10))
            elif loot == 2:
                state.invintory.append(Weapon("Stolen Knife",25,16))
            elif loot == 3:
                state.invintory.append(Weapon("Stolen Crossbow", 35,20))
        elif state.job == Fighter:
            if loot ==1:
                state.invintory.append(Weapon("Stolen Spear", 17,10))
            elif loot==2:
                state.invintory.append(Weapon("Stollen Sword",23,16))
            elif loot ==3:
                state.invintory.append(Weapon("Stollen Pike", 30, 20))
        elif state.job == Mage:
            if loot ==1:
                state.invintory.append(Weapon("Stollen Staff",25,10))
            elif loot ==2:
                state.invintory.append(Weapon("Stollen Book",35,16))
            elif loot ==3:
                state.invintory.append(Weapon("Stollen Orb", 80, 20))
        elif state.job == Tank:
            if loot ==1:
                state.invintory.append(Weapon("Stollen Mace", 10,10))
            elif loot ==2:
                state.invintory.append(Weapon("Stollen Hammer", 17,16))
            elif loot ==3:
                state.invintory.append(Weapon("Stollen Axe",28,20))
        return cave(state)
    else:
        return cave_fight(state,turn)
    
@route
def cave(state: State) -> Page:
    """ The page for the cave location, which has a locked door. """
    contents = []
    contents.append("You see a locked door.")
    if state.has_key:
        contents.append(Button("Unlock door",boss_fight,arguments=[Argument(name="turn", value=0)]))
    contents.append(Button("Leave",crossroads))
    contents.append(Image("cave.png"))
    return Page(state,contents)

@route
def boss_fight(state:State, turn:int)->Page:
    '''
    Introduces the player to the boss fight, and allows them thier first choice in attacking or giving up.
    '''
    contents = []
    if turn ==0:
        contents.append("You enter the locked chamber, beliving it to be the home of the evil that plauges this land.")
    contents.append("You have " + (str((state.health/state.job.max_health)*100))[:5] +" percent health")
    if state.job == Archer:
        if turn ==0:
            state.enemy_health = 120.0
        contents.append("You find yourself face-to-face with a fighter.")
        contents.append(Button("Fight",boss_attack,arguments=[Argument(name="turn", value=turn)]))
        contents.append(Button("Give up",reset))
        contents.append(Image("goblin.png"))
    elif state.job == Fighter:
        if turn ==0:
            state.enemy_health = 75.0
        contents.append("You find yourself face-to-face with a mage.")
        contents.append(Button("Fight",boss_attack,arguments=[Argument(name="turn", value=turn)]))
        contents.append(Button("Give up",reset))
        contents.append(Image("mage.jpg"))
    elif state.job == Mage:
        if turn ==0:
            state.enemy_health = 200.0
        contents.append("You find yourself face-to-face with a tank.")
        contents.append(Button("Fight",boss_attack,arguments=[Argument(name="turn", value=turn)]))
        contents.append(Button("Give up",reset))
        contents.append(Image("troll.jpg"))
    elif state.job == Tank:
        if turn ==0:
            state.enemy_health = 135.0
        contents.append("You find yourself face-to-face with an archer.")
        contents.append(Button("Fight",boss_attack,arguments=[Argument(name="turn", value=turn)]))
        contents.append(Button("Give up",reset))
        contents.append(Image("archer.png"))
    return Page(state,contents)

@route
def boss_attack(state:State, turn:int)->Page:
    '''
    Allows the boss to do damage to the player and the player to the boss, procedes if the boss is defeated.
    '''
    if state.job == Archer:
        if turn != 0:
            state.health -= randint(20,30)
        state.enemy_health -= ((state.invintory[0].damage)+randint(-5,10))
        if state.health <=0:
            return player_dead(state)
        elif state.enemy_health <=0:
            return ending(state)
    elif state.job == Fighter:
        if turn != 0:
            state.health -= randint(25,35)
        state.enemy_health -= ((state.invintory[0].damage)+randint(-5,10))
        if state.health <=0:
            return player_dead(state)
        elif state.enemy_health <=0:
            return ending(state)
    elif state.job == Mage:
        if turn != 0:
            state.health -= randint(20,30)
        state.enemy_health -= ((state.invintory[0].damage)+randint(-5,10))
        if state.health <=0:
            return player_dead(state)
        elif state.enemy_health <=0:
            return ending(state)
    elif state.job == Tank:
        if turn != 0:
            state.health -= randint(10,20)
        state.enemy_health -= ((state.invintory[0].damage)+randint(-5,10))
        if state.health <=0:
            return player_dead(state)
        elif state.enemy_health <=0:
            return ending(state)
    turn +=1
    return boss_fight(state,turn)

@route
def ending(state: State) -> Page:
    """ The victory screen """
    return Page(state,[
        "You land the final blow, defeating the evil that faces you.",
        "Thank you " + state.name + " for defeating this monster.",
        "Yet as time passes, you feel a sense of dread wash over you.",
        Image("victory.png"),
        "The End...",
        "For now.",
        Button("New Game",reset)
        ])


@route
def player_dead(state:State):
    '''
    The game-over screen, for when players die in battle.
    '''
    return Page(state,[
        "Sorry " + state.name + ", but you ran out of health.",
        "Next time if you're low on health, return to town to heal.",
        Button("End game",reset)])


@route
def woods(state: State) -> Page:
    """ The page for the woods location, which will have a key if the player has not yet picked it up. """
    contents = []
    contents.append("You are in the woods.")
    if not state.has_key:
        contents.append("You see a key on the ground.")
        contents.append(Button("Take key",take_key))
    contents.append(Button("Leave",crossroads))
    contents.append(Image("woods.png"))
    return Page(state,contents)

@route
def take_key(state: State) -> Page:
    """ Updates the state to indicate that the player has picked up the key, then redirects to the woods. """
    state.has_key = True
    return woods(state)

@route
def town(state:State)->Page:
    '''
    The main place for players to gather items and heal themselves.
    '''
    content = []
    content.append("You have " + str(state.money) +" gold, and " + (str((state.health / state.job.max_health *100))[:5]) +" percent health")
    content.append("As you walk into town, you see a bustling market place.")
    content.append("When you approach, you notice a stall that's advertized twords adventurers.")
    content.append("When you approach, you are greeted,")
    content.append('"Greetings adventurer! How can I help you on this fine day?"')
    content.append(Button("Buy",buy))
    if (len(state.invintory) >1):
        content.append(Button("Sell",sell))
    if state.health != state.job.max_health:
        content.append(Button("Heal", heal))
    content.append(Button("Leave", crossroads))
    
    return Page(state,content)

@route
def heal(state)->Page:
    '''
    heals the player to full health at the cost of 5 money.
    '''
    state.money -=5
    state.health = state.job.max_health
    return town(state)

@route
def buy(state:State)->Page:
    '''
    Makes the store for the player to get better items
    '''
    store = []
    if state.job == Archer:
        store.append("sturdy knife")
        store.append("complex crossbow")
    elif state.job == Fighter:
        store.append("reliable sword")
        store.append("masterful halbierd")
    elif state.job == Mage:
        store.append("spell book")
        store.append("arcane orb")
    elif state.job == Tank:
        store.append("war hammer")
        store.append("battle axe")
    return Page(state,[
        "You have " + str(state.money) +" gold.",
        "What would you like to purchase?",
        SelectBox("item_buy",store),
        Button("Purchase",confirm_buy),
        Button("Cancel", town)])

    
@route
def confirm_buy(state:State, item_buy:str)->Page:
    '''
    Confirms or denys the ;layers choise to buy an item from the shop.
    '''
    for item in store_weapons:
        if item.name == item_buy:
            if state.money < item.cost:
                return Page(state, [
                    "You have " + str(state.money) + " gold.",
                    "I'm sorry, but you don't seem to have enough to purchace this " + item_buy,
                    "It costs " + str(item.cost) + " gold.",
                    Button("Darn",buy)])
            else:
                return Page(state, [
                    "You have " + str(state.money) + " gold.",
                    "This particular " + item.name + " costs " + str(item.cost) + " gold.",
                    "Would you like to purchase it?",
                    Button("Yes", pay, arguments=[Argument(name="item", value=item.name)]),
                    Button("No", buy)
                    ])
@route
def pay(state:State, item:str)->Page:
    '''
    takes the money out of the state, and adds the item into the invintory when the player buys an item.
    '''
    store_weapons = [sturdy_knife, complex_crossbow, reliable_sword, masterful_halbierd, spell_book, arcane_orb, war_hammer, battle_axe]
    for weapon in store_weapons:
        if weapon.name == item:
            state.money -= weapon.cost
            state.invintory.append(weapon)
            return buy(state)

@route
def sell(state:State)->Page:
    '''
    The main screen for the player to pick an item to sell.
    '''
    items = []
    for weapon in state.invintory:
        items.append(weapon.name)
    return Page(state,[
        "You have " + str(state.money) +" gold."
        "What would you like to sell?",
        SelectBox("item_sell",items),
        Button("Sell",confirm_sell),
        Button("Cancel", town)])

@route
def confirm_sell(state:State, item_sell:str)->Page:
    '''
    Confirms that the player actually wants to sell the item.
    '''
    for weapon in state.invintory:
        if item_sell==weapon.name:
            return Page(state,[
                "Selling this " + item_sell + " would give you " + str(weapon.cost//2 ) + " gold.",
                "Do you want to sell it?",
                Button("Yes", sale, arguments = [Argument(name="item", value = item_sell)]),
                Button("No", sell)
                ])
        
@route
def sale(state:State, item:str)->Page:
    '''
    removes the sold item from the invintory, and pays the player for the sold item.
    '''
    new_invintory = []
    sold = 0
    for weapon in state.invintory:
        if sold== 1:
            new_invintory.append(weapon)
        elif weapon.name != item:
            new_invintory.append(weapon)
        else:
            sold += 1
            state.money += (weapon.cost//2)
        state.invintory = new_invintory
    if len(state.invintory)>1:
        return sell(state)
    else:
        return town(state)
        
        
start_server(State("",100.0,Unemployed,[],5,False,80.0))


#Unit tests:
assert_equal(reset(State("Me",100.0,Archer,[],3,True,45.1)),
    Page(State("",100.0, Unemployed, [],5, False,80.0),[
        "Welcome to the adventure! What is your name?",
        TextBox("name","Adventurer"),
        "And what do you do?",
        SelectBox("job_select",["Archer","Fighter","Mage","Tank"]),
        Button("Confirm",create)
        ])
)
assert_equal(index(State("Nobody",47.3,Fighter,[],45,True,78.3)),
             Page(State("Nobody",47.3,Fighter,[],45,True,78.3),[
                 "Welcome to the adventure! What is your name?",
                 TextBox("name","Adventurer"),
                 "And what do you do?",
                 SelectBox("job_select",["Archer","Fighter","Mage","Tank"]),
                 Button("Confirm",create)
                 ]))
assert_equal(create(State("",100.0,Unemployed,[],0,False,16.3),"Teucer","Archer"),
            Page(State("Teucer",100.0,Archer,[],0,False,16.3),[
            "so you are Teucer the archer?",
            "Archers primarally use ranged weapons, such as bows, in order to fend off opponents",
            Button("Begin",background),
            Button("Cancel", reset)
            ]))
assert_equal(background(State("Merlin", 80, Mage, [arcane_orb], 21, True,81.2)),
             Page(State("Merlin", 80, Mage, [arcane_orb], 21, True,81.2),[
                "Welcome Merlin to the land of Aarorus.",
                "This land has saddly been plauged by some evil, whose nature is unkown to most.",
                "Word has traveled wide of this evil, and of the treasures that were suposedly claimed by it.",
                "Hense your arrival.",
                "Whether you are here for the treasure or to free the evil shadows over this land,"
                "you are here to help. Thank you.",
                Button("Procede",procede)
                ]))
assert_equal(procede(State("Ajax", 150, Tank, [], 3, False,87.2)),
             Page(State("Ajax", 150, Tank, [simple_mace], 3, False,87.2),[
        "You find yourself at a crossroads.",
        "The paths ahead of you are labled with signs.",
        "Where will you choose to go?",
        Button("Cave",cave_entry),
        Button("Woods",woods),
        Button("Town",town),
        Image("field.png")
        ]))
assert_equal(crossroads(State("Achilies",120,Fighter,[simple_spear],13,False,99.0)),
             Page(State("Achilies",120,Fighter,[simple_spear],13,False,99.0),[
                "You find yourself at a crossroads.",
                "The paths ahead of you are labled with signs.",
                "Where will you choose to go?",
                Button("Cave",cave_entry),
                Button("Woods",woods),
                Button("Town",town),
                Image("field.png")
        ]))
assert_equal(woods(State("Frog",100.0, Unemployed,[],3,False,60.5)), Page(State("Frog", 100.0, Unemployed, [], 3, False,60.5),[
    "You are in the woods.",
    "You see a key on the ground.",
    Button("Take key", take_key),
    Button("Leave", crossroads),
    Image("woods.png")
    ]))
assert_equal(take_key(State("Apple", 12.5, Mage, [arcane_orb],0, False,79.5)),Page(State("Apple", 12.5, Mage, [arcane_orb],0,True,79.5),[
    "You are in the woods.",
    Button("Leave",crossroads),
    Image("woods.png")
    ]))
assert_equal(town(State("Nobody",60., Fighter, [simple_spear,reliable_sword],12,False,10.0)),
             Page(State("Nobody",60., Fighter, [simple_spear,reliable_sword],12,False,10.0),[
                 "You have 12 gold, and 50.0 percent health",
                 "As you walk into town, you see a bustling market place.",
                 "When you approach, you notice a stall that's advertized twords adventurers.",
                 "When you approach, you are greeted,",
                 '"Greetings adventurer! How can I help you on this fine day?"',
                 Button("Buy",buy),
                 Button("Sell",sell),
                 Button("Heal", heal),
                 Button("Leave", crossroads)
                 ]))
assert_equal(heal(State("Banana man", 60.0, Fighter, [], 50, False,33.3)),
             Page(State("Banana man", 120.0, Fighter, [], 45, False,33.3),[
                "You have 45 gold, and 100.0 percent health",
                "As you walk into town, you see a bustling market place.",
                "When you approach, you notice a stall that's advertized twords adventurers.",
                "When you approach, you are greeted,",
                '"Greetings adventurer! How can I help you on this fine day?"',
                Button("Buy",buy),
                Button("Leave", crossroads)
                ]))
assert_equal(buy(State("",100.0,Mage,[],100,False,11.1)), Page(
    State("",100.0,Mage,[],100,False,11.1),[
        "You have 100 gold.",
        "What would you like to purchase?",
        SelectBox("item_buy",["spell book", "arcane orb"]),
        Button("Purchase", confirm_buy),
        Button("Cancel", town)]))
assert_equal(confirm_buy(State("Tucer",90,Archer,[simple_bow],100,True,66.6),"complex crossbow"), Page(State("Tucer",90, Archer, [simple_bow],100,True,66.6),[
    "You have 100 gold.",
    "This particular complex crossbow costs 20 gold.",
    "Would you like to purchase it?",
    Button("Yes", pay, arguments=[Argument(name="item", value="complex crossbow")]),
    Button("No", buy)
    ]))
assert_equal(player_dead(State("Bob",-12.4,Archer,[simple_bow],100,True,112.3)),Page(State("Bob",-12.4,Archer,[simple_bow],100,True,112.3),[
    "Sorry Bob, but you ran out of health.",
    "Next time if you're low on health, return to town to heal.",
    Button("End game",reset)]))
assert_equal(cave_entry(State("Bog Monster",120.3,Tank, [battle_axe],12,False,80.0)),Page(State("Bog Monster", 120.3,Tank, [battle_axe],12,False,80.0),[
    "You stumble into the cave.",
    "You find that this cave is a theives den.",
    "One of the theives is home and attacks you.",
    Button("Fight",cave_fight,arguments=[Argument(name="turn", value=0)]),
    Button("Flee",crossroads)]))
assert_equal(cave(State("Jeff",100.0,Archer,[simple_bow],12,True,0.0)),Page(State("Jeff",100.0, Archer,[simple_bow],12,True,0.0),[
    "You see a locked door.",
    Button("Unlock door",boss_fight,arguments=[Argument(name="turn", value=0)]),
    Button("Leave", crossroads),
    Image("cave.png")
    ]))
assert_equal(boss_fight(State("Ody",120.0,Fighter,[simple_spear],100,True,-12.0), 0),Page(State("Ody", 120.0, Fighter, [simple_spear],100, True,75.0),[
    "You enter the locked chamber, beliving it to be the home of the evil that plauges this land.",
    "You have 100.0 percent health",
    "You find yourself face-to-face with a mage.",
    Button("Fight",boss_attack,arguments=[Argument(name="turn", value=0)]),
    Button("Give up", reset),
    Image("mage.jpg")
    ]))
assert_equal(ending(State("Cassandra", 1.0, Mage, [arcane_orb],0,True,-12.0)),Page(State("Cassandra",1.0,Mage,[arcane_orb],0,True,-12.0),[
    "You land the final blow, defeating the evil that faces you.",
    "Thank you Cassandra for defeating this monster.",
    "Yet as time passes, you feel a sense of dread wash over you.",
    Image("victory.png"),
    "The End...",
    "For now.",
    Button("New Game",reset)
    ]))
assert_equal(cave_fight(State("Jeff",90.0,Archer,[complex_crossbow],10,True,12.3),0),Page(State("Jeff",90.0,Archer,[complex_crossbow],10,True,80.0),[
    "You have 100.0 percent health",
    "The thief attacks you.",
    "What will you do?",
    Button("Fight", cave_attack,arguments=[Argument(name="turn",value=1)]),
    Button("Flee",crossroads),
    Image("thief.png")]))
