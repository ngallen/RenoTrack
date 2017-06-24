from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Area, Base, RenoItem, User

engine = create_engine('sqlite:///renoTrack.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Papa Smurf", email="psmiddy8008@gmail.com",
                         picture='https://en.wikipedia.org/wiki/Papa_Smurf#/media/File:Papasmurf1.jpg')
session.add(User1)
session.commit()

# **************** areas ******************************
area1 = Area(name="Garage")
session.add(area1)
session.commit()

area2 = Area(name="Bedroom_West")
session.add(area2)
session.commit()

area3 = Area(name="Bathroom_West")
session.add(area3)
session.commit()

area4 = Area(name="Bedroom_East")
session.add(area4)
session.commit()

area5 = Area(name="Bathroom_East")
session.add(area5)
session.commit()

area6 = Area(name="Guest_Room")
session.add(area6)
session.commit()

area7 = Area(name="Kitchen")
session.add(area7)
session.commit()

area8 = Area(name="Living_Room")
session.add(area8)
session.commit()

area9 = Area(name="Dining_Room")
session.add(area9)
session.commit()

area10 = Area(name="Landscaping")
session.add(area10)
session.commit()

area11 = Area(name="Coat_Room")
session.add(area11)
session.commit()

area12 = Area(name="General")
session.add(area12)
session.commit()
# **************** areas ******************************

# **************** items ******************************
renoItem1 = RenoItem(user_id=1, name="Vanity Mirror", description="Installed large, multi-compartment vanity mirror above sink",
                    cost="$200", area=area5)
session.add(renoItem1)
session.commit()

renoItem2 = RenoItem(user_id=1, name="Towel Rack", description="Installed extra towel rack. Wood finish.",
                    cost="$20", area=area5)
session.add(renoItem2)
session.commit()

renoItem3 = RenoItem(user_id=1, name="Connecting doorway", description="Installed doorway between main garage rooms",
                    cost="$50", area=area1)
session.add(renoItem3)
session.commit()

renoItem4 = RenoItem(user_id=1, name="Swamp Cooler", description="Replaced float, overfloat fitting, and re-connected plumbing for swamp cooler",
                    cost="$25", area=area12)
session.add(renoItem4)
session.commit()

renoItem5 = RenoItem(user_id=1, name="Boarded hail-damaged windows", description="Boarded broken windows caused by 2017 Denver hail storm",
                    cost="$10", area=area2)
session.add(renoItem4)
session.commit()

renoItem6 = RenoItem(user_id=1, name="Boarded hail-damaged windows", description="Boarded broken windows caused by 2017 Denver hail storm",
                    cost="$10", area=area3)
session.add(renoItem6)
session.commit()

renoItem7 = RenoItem(user_id=1, name="Boarded hail-damaged windows", description="Boarded broken windows caused by 2017 Denver hail storm",
                    cost="$10", area=area7)
session.add(renoItem7)
session.commit()
# **************** items ******************************