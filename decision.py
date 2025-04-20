import enum
import ztime
import action
from defs import STATS
import random

last_stat_time=0

def tick_decisionsys(myagent, curtime):
    hunger=myagent.get_stat("hungry").get_value()
    tired=myagent.get_stat("tired").get_value()
    bored=myagent.get_stat("bored").get_value()
    lonely= myagent.get_stat("lonely").get_value()
    money=myagent.get_stat("money").get_value()
    dirty=myagent.get_stat("dirty").get_value()
    sad= myagent.get_stat("sad").get_value()
    crazy= myagent.get_stat("crazy").get_value()
    frustrated= myagent.get_stat("frustrated").get_value()
    lazy= myagent.get_stat("lazy").get_value()
    confident= myagent.get_stat("confident").get_value()
    accomplished= myagent.get_stat("accomplished").get_value()

    global last_stat_time
    hour = curtime.hour()
    day= curtime.day_of_week()

    if last_stat_time is None or last_stat_time<curtime.minute:
        last_stat_time=curtime.minute+60

        myagent.change_stat("hungry", random.randint(1,15))  
        myagent.change_stat("tired", random.choice([0, 12]))  
        myagent.change_stat("bored", random.choice([0, 9]))  
        myagent.change_stat("lonely", random.choice([0,14]))  
        myagent.change_stat("money", random.randint(0,400))  
        myagent.change_stat("dirty", random.choice([0,5]))  
        myagent.change_stat("sad", random.choice([0,11]))  
        myagent.change_stat("crazy", random.choice([0,13]))  
        myagent.change_stat("frustrated", random.choice([0, 4]))  
        myagent.change_stat("lazy", random.choice([0, 10]))  

    #for morning daily
    if hour in range(6, 9):
        myagent.set_location("home")
        if hunger>10:
            myagent.state="eating breakfast"
            myagent.set_action(action.Action("Mickey is eating breakfast!!", curtime, curtime + ztime.Time(30)))
        elif dirty>2:
            myagent.state="Showering"
            myagent.set_action(action.Action("Mickey is taking a shower....", curtime, curtime + ztime.Time(20)))
        else:
            myagent.state="preparing for office"
            myagent.set_action(action.Action("Mickey is getting ready for the office.......", curtime, curtime + ztime.Time(15)))
    
    elif hour in range(9, 17):
        myagent.set_location("work")
        if money<300:
            myagent.state="working"
            myagent.set_action(action.Action("Mickey is working hard in his office to get the money. ", curtime, curtime + ztime.Time(480)))
        elif money>=300 and bored>0 or tired>4:
            myagent.state="taking a break"
            myagent.set_action(action.Action("Taking coffee break and scrolling social media!", curtime, curtime + ztime.Time(60)))
        else:
            myagent.state="daydreaming"
            myagent.set_action(action.Action("Mickey is sitting in his desk and thinking about the upcoming vacation", curtime, curtime + ztime.Time(30)))
    
    elif hour in range(17, 22):
        if lonely>10:
            myagent.state="socializing"
            if day in ["Friday", "Saturday"]:
                myagent.set_location("bar")
                myagent.set_action(action.Action("Mickey is hanging out with friends at the bar and then pizza parlor... ", curtime, curtime + ztime.Time(90)))
            else:
                myagent.set_location("home")
                myagent.set_action(action.Action("Mickey is sleeping... ", curtime, curtime + ztime.Time(60)))

        elif sad>5:
            myagent.state="relaxing"
            if day in ["Friday", "Saturday"]:
                myagent.set_location("bar")
                myagent.set_action(action.Action("Mickey is relaxing and thinking at the brink of riverside. ", curtime, curtime + ztime.Time(60)))
            else:
                myagent.set_location("home")
                myagent.set_action(action.Action("Mickey is reading books...", curtime, curtime + ztime.Time(60)))

        elif crazy>7 or confident>5:
            myagent.state="workout"
            myagent.set_location("gym")
            myagent.set_action(action.Action("Mickey is doing some workout ", curtime, curtime + ztime.Time(120)))
        elif crazy>10 and sad>10 and frustrated>10:
            myagent.state="get caught"
            myagent.set_location("jail")
            myagent.set_action(action.Action("Mickey did something crazy for limited jail time ", curtime, curtime + ztime.Time(120)))
        else:
            myagent.state="streaming"
            myagent.set_location("home")
            myagent.set_action(action.Action("Mickey is streaming new movie, released last week. ",curtime, curtime + ztime.Time(120)))
    else:
        myagent.set_location("home")
        if hunger>10:
            myagent.state="cooking"
            myagent.set_action(action.Action("Mickey is cooking for dinner", curtime, curtime + ztime.Time(30)))
        elif dirty>2:
            myagent.state="Showering"
            myagent.set_action(action.Action("Mickey is taking a shower....", curtime, curtime + ztime.Time(20)))
        else:
            myagent.state="sleeping"
            myagent.set_action(action.Action("Mickey is dreaming.......", curtime, curtime + ztime.Time(15)))
        






def make_decisionsys(myagent):
    myagent.state='idle'
    myagent.set_location("home")
