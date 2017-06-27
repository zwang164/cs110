import pygame

class AnimCursor:
    def __init__(self):
        self.anim = None
        self.frame_num = 0
        self.current = None
        self.next = None
        self.played = []
        self.transition = 0.0
        self.playing = True
        self.playtime = 0.0
    
        self.frame_time = 0.0
        self.timeleft = 0.0
        self.playspeed = 1.0
        
    def use_anim(self, anim):
        self.anim = anim
        self.reset()
        
    def reset(self):
        self.current = self.anim.frames[0][0]
        self.timeleft = self.anim.frames[0][1]
        self.frame_time = self.timeleft
        self.next_frame = (self.frame_num + 1) % len(self.anim.frames)
        self.next = self.anim.frames[self.next_frame][0]
        self.frame_num = 0
        self.playtime = 0.0
        self.transition = 0.0
        
    def play(self, playspeed=1.0):
        self.playspeed = playspeed
        self.reset()
        self.unpause()
        
    def pause(self):
        self.playing = False
        
    def unpause(self):
        self.playing = True
        
    def update(self, td):
        td = td * self.playspeed
        self.played = []
        if self.playing:
            self.playtime += td
            self.timeleft -= td
            self.transition = self.timeleft / self.frame_time
                
            while self.timeleft <= 0.0:
                self.frame_num = (self.frame_num + 1) % len(self.anim.frames)
                if self.anim.playmode == ONCE and frame_num == 0:
                    self.pause()
                    return
                    
                next_frame = (self.frame_num + 1) % len(self.anim.frames)
                
                frame,time = self.anim.frames[self.frame_num]
                self.frame_time = time
                self.timeleft += time
                self.current = frame
                self.next = self.anim.frames[next_frame][0]
                self.played.append(frame)
                self.transition = self.timeleft / time
                
                if self.frame_num == 0:
                    self.playtime = self.timeleft
