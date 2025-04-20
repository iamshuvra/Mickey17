import pygame
import pygame.freetype
import math
import random
import agent_stat
import ztime
import action
import agent
import decision
from defs import *

# ###############################################################
class Display:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.run = True
        self.delta = 0
        self.font = None
        
    def draw_gobj(self, gobj):
        pygame.draw.circle(
            self.screen,
            gobj.color,
            gobj.pos(),
            gobj.radius)
    def draw_text(self, msg, x, y, color):
        surface, rect = self.font.render(msg, color)
        self.screen.blit(surface, (x, y))
    def draw_line(self, p1, p2, color,width=1):
        pygame.draw.line(
            self.screen,
            color,
            p1,
            p2,
            width)

def init_display(sw, sh):
    pygame.init()
    screen = pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    display = Display(screen, clock)
    display.font = pygame.freetype.Font('JuliaMono-Bold.ttf', 18)
    pygame.key.set_repeat(200,100)
    return display

def wrap_text(text, font, width):
    splt_text = text.split()

    lines = []

    cur = 0
    line = ""

    while cur < len(splt_text):
        new_line = ""
        if len(line) > 0:
            new_line = f"{line} {splt_text[cur]}"
        else:
            new_line = splt_text[cur]
        r = pygame.freetype.Font.get_rect(font, new_line)
        if r.width > width:
            lines.append(line)
            line = ""
        else:
            line = new_line
            cur += 1
    if len(line) > 0:
        lines.append(line)

    return lines

# #################################################################

def MakeStats():
    stats = {}
    for n,vals in STATS.items():
        astat = agent_stat.Stat(n,vals)
        stats[n] = astat
    return stats

def MakeAgent(agent_name, cur_time):
    a = agent.Agent(
        agent_name, 
        MakeStats(),
        f"{agent_name} is doin' nuthin'."
    )
    return a

def UpdateAgent(myagent, curtime):
    myagent.update_action(curtime)

def DrawUI(display,
           cur_time,
           myagent,
           winw, winh,
           stat_index,
           game_speed,
           decision_sys_running):
    display.draw_text(
        f"Day: {cur_time.day_of_week()}",
        10,10,FG_COLOR)
    display.draw_text(
        f"Hour: {cur_time.hour():02}",
        180,10,FG_COLOR)
    display.draw_text(
        f"Min: {cur_time.minit():02}",
        300,10,FG_COLOR)
    display.draw_text(
        f"{myagent.get_name()}'s stats",
        10,40,FG_COLOR)
    display.draw_text(
        f"Game: {game_speed[0]}",
        410,10,FG_COLOR)
    display.draw_text(
        f"Decision Sys: {decision_sys_running}",
        580,10,FG_COLOR)
    display.draw_line((400,0),(400,winh),"black",2)
    display.draw_text(
        f"{myagent.get_name()}'s Action",
        410,40,FG_COLOR)

    wrapped_msg = wrap_text(myagent.get_action_message(),
                            display.font, 380)
    y = 70
    for msg in wrapped_msg:
        display.draw_text(
            msg,
            410, y, FG_COLOR)
        y += 25
        
    y = 70
    x = 10
    for i,name in enumerate(STAT_NAMES):
        s = myagent.get_stat(name)
        c = FG_COLOR
        if i == stat_index:
            c = 'red'
        display.draw_text(
            f"{name:<12} {s.get_value()}",
            x,y,c)
        y += 25
        if y+25 > winh:
            x += 200
            y = 70

def MakeDecisionSys(myagent):
    decision.make_decisionsys(myagent)

def CheckDecisionSys(myagent, curtime):
    decision.tick_decisionsys(myagent, curtime)

            
def GameLoop(display, _agent, _time):

    winw, winh = pygame.display.get_window_size()
    curtime = _time
    myagent = _agent
    stat_index = 0
    old_speed = 0
    sim_speed = 0
    time_last_tick = 0
    next_behavior_update = curtime
    decision_sys_running = False

    # Here is where the behavior is created before the
    # game loop starts.
    MakeDecisionSys(myagent)
    
    while display.run:
        ticks = display.clock.tick(60)
        dt = ticks / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    myagent.change_stat(STAT_NAMES[stat_index],-1)
                elif event.key == pygame.K_RIGHT:
                    myagent.change_stat(STAT_NAMES[stat_index],1)
                elif event.key == pygame.K_UP:
                    stat_index = ((stat_index-1)+len(STAT_NAMES))%len(STAT_NAMES)
                elif event.key == pygame.K_DOWN:
                    stat_index = (stat_index+1)%len(STAT_NAMES)
                elif event.key == pygame.K_LEFTBRACKET:
                    if sim_speed > 0:
                        sim_speed -= 1
                elif event.key == pygame.K_RIGHTBRACKET:
                    if sim_speed < len(GAME_SPEEDS)-1:
                        sim_speed += 1
                elif event.key == pygame.K_p:
                    if sim_speed == 0:
                        sim_speed = old_speed
                    else:
                        old_speed = sim_speed
                        sim_speed = 0
                elif event.key == pygame.K_q:
                    display.run = False
                elif event.key == pygame.K_d:
                    curtime.tick(60*24)
                elif event.key == pygame.K_s:
                    curtime.tick(-60*24)
                elif event.key == pygame.K_h:
                    curtime.tick(60)
                elif event.key == pygame.K_g:
                    curtime.tick(-60)
                elif event.key == pygame.K_m:
                    curtime.tick(1)
                elif event.key == pygame.K_n:
                    curtime.tick(-1)
                elif event.key == pygame.K_SPACE:
                    decision_sys_running = not decision_sys_running

        # This function call checks the agent's action. If the
        # action has expired, the agent is set to idle.
        UpdateAgent(myagent, curtime)
        
        # Here is where the agent's behavior is checked.
        # and if necessary, is switched to another action.
        if decision_sys_running:
            CheckDecisionSys(myagent, curtime)

        display.screen.fill(BG_COLOR)

        DrawUI(display, curtime, myagent, winw, winh, stat_index,
               GAME_SPEEDS[sim_speed], decision_sys_running)

        pygame.display.flip()

        if GAME_SPEEDS[sim_speed][1] - time_last_tick <= 0:
            curtime.tick(GAME_SPEEDS[sim_speed][2])
            time_last_tick = 0
        else:
            time_last_tick += ticks

def simulation_week(myagent, curtime):
    for i in range(7):
        print(f"Current time: {curtime.day_of_week()}")
        for j in range(24):
            decision.tick_decisionsys(myagent, curtime)
            print(f"{curtime.hour():02}:{curtime.minit():02}-{myagent.state}")
            curtime.tick(60)
        curtime.advance_day()

    print("One week similation completed!")
        
def main():
    display = init_display(800,600)
    myagent = MakeAgent(AGENT_NAME, START_TIME)
    cur_time = ztime.Time(START_TIME)
    # user_input = input("run a simulation (y/n): ").strip().lower()
    # if user_input == 'y':
    simulation_week(myagent, cur_time) 
    GameLoop(display, myagent, cur_time)  

if __name__ == "__main__":
    main()
