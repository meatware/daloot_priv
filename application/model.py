from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

class Item(Base):
    __tablename__ = 'items'

    name =  Column(String(50),primary_key=True)
    category =  Column(String(45))
    type = Column(String)
    lifetime = Column(Integer)
    quantmin = Column(Integer, default=-1)
    nominal =  Column(Integer, default=0)
    countmax = Column(Integer, default=-1)
    min_val = Column(Integer)
    cost = Column(Integer, default = 100)
    restock = Column(Integer)
    Military = Column(Integer, default=0)
    Prison = Column(Integer, default=0)
    School = Column(Integer, default=0)
    Coast = Column(Integer, default=0)
    Village = Column(Integer, default=0)
    Industrial = Column(Integer, default=0)
    Medic = Column(Integer, default=0)
    Police = Column(Integer, default=0)
    Hunting = Column(Integer, default=0)
    Town = Column(Integer, default=0)
    Farm = Column(Integer, default=0)
    Firefighter = Column(Integer, default=0)
    Office = Column(Integer, default=0)
    Tier1 = Column(Integer, default=0)
    Tier2 = Column(Integer, default=0)
    Tier3 = Column(Integer, default=0)
    Tier4 = Column(Integer, default=0)
    floor = Column(Integer, default=0)
    shelves = Column(Integer, default=0)
    count_in_cargo = Column(Integer, default=0)
    count_in_hoarder =  Column(Integer, default=0)
    count_in_map = Column(Integer, default=0)
    count_in_player = Column(Integer, default=0)
    crafted =  Column(Integer, default=0)
    deloot = Column(Integer, default=0)
    ingame_name = Column(String, nullable=True)
    rarity = Column(Integer, default=0)
    mods = Column(String,default="Vanilla")
    subtype = Column(String, nullable=True)
    buyprice = Column(Integer, nullable=True)
    sellprice = Column(Integer, nullable=True)
    traderExclude = Column(Integer, default=0)
    traderCat = Column(String, nullable=True)
    trader_loc = Column(Integer)
    
    

# CREATE TABLE `items` (
#   `name` varchar(50) NOT NULL,
#   `category` varchar(45) NOT NULL COMMENT 'weapons, tools, ... ',
#   `type` varchar(45) DEFAULT NULL COMMENT 'Gun, Attachment, Ammo',
#   `lifetime` int unsigned NOT NULL,
#   `quantmin` int DEFAULT '-1',
#   `nominal` int unsigned DEFAULT '0',
#   `cost` int unsigned DEFAULT '100',
#   `quantmax` int NOT NULL DEFAULT '-1',
#   `min` int unsigned NOT NULL,
#   `restock` int unsigned NOT NULL,
#   `Military` tinyint(1) unsigned zerofill NOT NULL,
#   `Prison` tinyint(1) unsigned zerofill NOT NULL,
#   `School` tinyint(1) unsigned zerofill NOT NULL,
#   `Coast` tinyint(1) unsigned zerofill NOT NULL,
#   `Village` tinyint(1) unsigned zerofill NOT NULL,
#   `Industrial` tinyint(1) unsigned zerofill NOT NULL,
#   `Medic` tinyint(1) unsigned zerofill NOT NULL,
#   `Police` tinyint(1) unsigned zerofill NOT NULL,
#   `Hunting` tinyint(1) unsigned zerofill NOT NULL,
#   `Town` tinyint(1) unsigned zerofill NOT NULL,
#   `Farm` tinyint(1) unsigned zerofill NOT NULL,
#   `Firefighter` tinyint(1) unsigned zerofill NOT NULL,
#   `Office` tinyint(1) unsigned zerofill NOT NULL,
#   `Tier1` tinyint(1) unsigned zerofill NOT NULL,
#   `Tier2` tinyint(1) unsigned zerofill NOT NULL,
#   `Tier3` tinyint(1) unsigned zerofill NOT NULL,
#   `Tier4` tinyint(1) unsigned zerofill NOT NULL,
#   `shelves` tinyint(1) unsigned zerofill NOT NULL,
#   `floor` tinyint(1) unsigned zerofill NOT NULL,
#   `count_in_cargo` tinyint(1) unsigned zerofill NOT NULL,
#   `count_in_hoarder` tinyint(1) unsigned zerofill NOT NULL,
#   `count_in_map` tinyint(1) unsigned zerofill NOT NULL,
#   `count_in_player` tinyint(1) unsigned zerofill NOT NULL,
#   `crafted` tinyint(1) unsigned zerofill NOT NULL,
#   `deloot` tinyint(1) unsigned zerofill NOT NULL,
#   `ingameName` varchar(45) DEFAULT NULL,
#   `rarity` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0',
#   `mods` varchar(25) NOT NULL DEFAULT 'Vanilla',
#   `subtype` varchar(45) DEFAULT NULL,
#   `buyprice` int DEFAULT NULL,
#   `sellprice` int DEFAULT NULL,
#   `traderCat` varchar(3) DEFAULT NULL,
#   `traderExclude` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0',
#   `trader_loc` tinyint NOT NULL,
#   PRIMARY KEY (`name`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


class Combo(Base):
    __tablename__ = 'itemcombos'
    id = Column(Integer, primary_key=True, autoincrement=True)

    item1 = Column(Integer, ForeignKey("items.name"))
    item2 = Column(Integer, ForeignKey("items.name"))

    toone = relationship("Item", foreign_keys=[item1])
    tomany = relationship("Item", foreign_keys=[item2])
