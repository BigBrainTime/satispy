import pygame,copy

COLOR = {
    'BLACK':(0,0,0),
    'WHITE':(255,255,255),
    'GREY':(127,127,127),
    'RED':(255,0,0),
    'GREEN':(0,255,0),
    'BLUE':(0,0,255),
    'YELLOW':(255,255,0),
    'CYAN':(0,255,255),
    'MAGENTA':(255,0,255),
    'DARKGREY':(80,80,80),
    'PINK':(255,192,203),
    'LIGHTPINK':(255,182,193),
    'HOTPINK':(255,105,180),
    'DEEPPINK':(255,20,147),
    'ORANGE':(255,165,0),
    'DARKORANGE':(255,140,0),
    'ORANGERED':(255,69,0),
    'GOLD':(255,215,0),
    'INDIGO':(75,0,130),
    'LIMEGREEN':(50,205,50),
    'MAROON':(128,0,0),
    'BABYBLUE':(137,207,240),
    'SILVER':(192,192,192),
    'PEACH':(255,218,185),
    'CORAL':(255, 127, 80),
    'CRIMSON':(157,34,53),

}

allowed_segments = {
    '1': '01100000',
    '2': '11011010',
    '3': '11110010',
    '4': '01100110',
    '5': '10110110',
    '6': '10111110',
    '7': '11100000',
    '8': '11111110',
    '9': '11110110',
    '0': '11111100',
    '-': '00000010',
    '.': '00000001',
    'a': '11101110',
    'A': '11101110',
    '10': '11101110',
    'b': '00111110',
    'B': '00111110',
    '11': '00111110',
    'c': '00011110',
    'C': '10011100',
    '12': '10011100',
    'd': '01111010',
    'D': '01111010',
    '13': '01111010',
    'e': '10011110',
    'E': '10011110',
    '14': '10011110',
    'f': '10001110',
    'F': '10001110',
    '15': '10001110',
}


class static_object():
    def __init__(self, x, y, w, h, screen_x, screen_y, color=None, text='', font='freesansbold.ttf', font_size=10, font_color=(0, 0, 0), image=None, border_px=None, border_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        self.x = (round(screen_x*x/100), x)
        self.y = (round(screen_y*y/100), y)
        self.w = (round(screen_x*w/100), w)
        self.h = (round(screen_y*h/100), h)
        self.screen_y = screen_y
        self.color = color
        self.minimized = False
        self.processing = True
        self.center = 'center'

        self.font_size = round(font_size*screen_y/1080)
        self.FONT = pygame.font.Font(font, self.font_size)
        self.raw_text = text
        self.font_color = font_color
        self.font = font
        self.text = self.FONT.render(text, True, font_color)

        if image != None:
            self.orig_image = pygame.image.load(image)
            self.image = pygame.transform.scale(
                self.orig_image, (self.w[0], self.h[0]))
        else:
            self.image = None

        if border_px != None:
            self.border_px = border_px
            self.border_color = border_color
        else:
            self.border_px = None

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        self.x = (round(screen_x*self.x[1]/100*scale_x+offset_x), self.x[1])
        # screen*scale/100=pixel
        # scale=pixel*100/screen
        self.y = (round(screen_y*self.y[1]/100*scale_y+offset_y), self.y[1])
        self.w = (round(screen_x*self.w[1]/100*scale_x), self.w[1])
        self.h = (round(screen_y*self.h[1]/100*scale_y), self.h[1])
        self.screen_y = screen_y
        self.rect = pygame.Rect(self.x[0], self.y[0], self.w[0], self.h[0])

        if self.color != None:
            pygame.draw.rect(surface, self.color, self.rect)

        if self.image != None:
            self.image = pygame.transform.scale(
                self.orig_image, (self.w[0], self.h[0]))
            self.image_rect = self.image.get_rect()

            self.image_rect.center = (
                self.x[0]+self.w[0]//2, self.y[0]+self.h[0]//2)
            surface.blit(self.image, self.image_rect)

        if self.raw_text != None and self.raw_text != '':
            if self.center == 'center':
                self.textrect = self.text.get_rect()
                self.textrect.center = (
                    self.x[0]+self.w[0]//2, self.y[0]+self.h[0]//2)

            elif self.center == 'left':
                self.textrect = self.text.get_rect()
                self.textrect.midleft = (self.x[0], self.y[0]+self.h[0]//2)

            elif self.center == 'right':
                self.textrect = self.text.get_rect()
                self.textrect.midright = (self.x[0]+self.w[0], self.y[0]+self.h[0]//2)

            surface.blit(self.text, self.textrect)

        if self.border_px != None:
            self.borders = []

            self.border_boxes = ((self.x[0], self.y[0], self.w[0], self.border_px), (self.x[0], self.y[0]+self.h[0]-self.border_px, self.w[0], self.border_px),
                                 (self.x[0], self.y[0], self.border_px, self.h[0]), (self.x[0]+self.w[0]-self.border_px, self.y[0], self.border_px, self.h[0]))

            for values in (self.border_boxes):
                self.borders.append(pygame.Rect(
                    values[0], values[1], values[2], values[3]))
            for border in self.borders:
                pygame.draw.rect(surface, self.border_color, border)

    def change_text(self, text=None, font=None, font_size=None, font_color=None):
        if font != None or font_size != None:
            if font_size != None:
                self.font_size = round(font_size*self.screen_y/1080)
            if font != None:
                self.font = font
            self.FONT = pygame.font.Font(self.font, self.font_size)

        if text != None:
            self.raw_text = text

        if font_color != None:
            self.font_color = font_color

        self.text = self.FONT.render(self.raw_text, True, self.font_color)

    def change_text_center(self, center='center'):
        self.center = center

    def change_image(self, image):
        self.orig_image = pygame.image.load(image)

    def flip_image(self, flip_x, flip_y):
        self.orig_image = pygame.transform.flip(
            self.orig_image, flip_x, flip_y)

    def set_pos(self, x, y, screen_x, screen_y):
        self.x = (x, round(x*100/screen_x))
        self.y = (y, round(y*100/screen_y))
        # screen*scale/100=pixel
        # scale=pixel*100/screen

    def set_relative_pos(self, x, y, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        self.x = (round(screen_x*x[1]/100*scale_x+offset_x), x[1])
        self.y = (round(screen_y*y[1]/100*scale_y+offset_y), y[1])

    def get_pos(self):
        return (self.x[0], self.y[0])

    def noClick(self):
        return (False, pygame.mouse.get_pressed())

    def onClick(self):
        return (False, pygame.mouse.get_pressed())

    def onPress(self, key, unicode):
        return key, unicode

    def get_self(self):
        return self

    def hide(self):
        self.minimized = True

    def show(self):
        self.minimized = False


class variable_object(static_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, text, font, font_size, font_color, value, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, text, font, font_size,
                         font_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class click_object(variable_object):
    def rawClick(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x[0] and pos[0] < self.x[0] + self.w[0] and pos[1] > self.y[0] and pos[1] < self.y[0] + self.h[0]:
            data = True
        else:
            data = False
        return data
    
    def onClick(self):
        if self.minimized or not self.processing:
            return self.noClick()
        return(self.rawClick(), pygame.mouse.get_pressed())
    
    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        super().process(surface, screen_x, screen_y, scale_x=scale_x,scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        return self.rawClick()

class base_toggle_button(click_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, value, text='', font='freesansbold.ttf', font_size=10, font_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, text, font, font_size, font_color,
                         value, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.toggle_color = toggle_color
        self.base_color = color
        self.value = value

    def onClick(self):
        if self.minimized or not self.processing:
            return self.noClick()
        data = super().onClick()
        if data[0]:
            self.value = not self.value

        if self.value:
            self.color = self.toggle_color
        else:
            self.color = self.base_color
        return data


class hover_toggle_button(base_toggle_button):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, value, false_hover_color, true_hover_color, text='', font='freesansbold.ttf', font_size=10, font_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, toggle_color, value, text, font,
                         font_size, font_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.false_hover_color = false_hover_color
        self.true_hover_color = true_hover_color

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x=scale_x,
                               scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)

        if self.value:
            if data:
                self.color = self.true_hover_color
            else:
                self.color = self.toggle_color
        else:
            if data:
                self.color = self.false_hover_color
            else:
                self.color = self.base_color

        return data


class momentary_button(base_toggle_button):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, function=None, text='', font='freesansbold.ttf', font_size=10, font_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, toggle_color, False, text, font,
                         font_size, font_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.function = function

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x=scale_x,
                               scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)

        if not data or not pygame.mouse.get_pressed()[0]:
            self.value = False
            self.color = self.base_color

        return data

    def onClick(self, args=None):
        if self.minimized or not self.processing:
            return self.noClick()
        data = super().onClick()

        if data[0]:
            self.value = True
            self.color = self.toggle_color
            if self.function != None and args == None:
                return data, self.function()
            elif self.function != None:
                return data, self.function(args)
        return data


class hover_momentary_button(momentary_button):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, toggle_color, function, false_hover_color, text='', font='freesansbold.ttf', font_size=10, font_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, toggle_color, function, text, font,
                         font_size, font_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.false_hover_color = false_hover_color

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        data = super().process(surface, screen_x, screen_y, scale_x=scale_x,
                               scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)

        if self.value:
            self.color = self.toggle_color
        else:
            if data:
                self.color = self.false_hover_color
            else:
                self.color = self.base_color

        return data


class label(static_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, text, font_size, font_color, font='freesansbold.ttf', scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, text=text, font=font, font_size=font_size,
                         font_color=font_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)


class image(static_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, image, border_px=None, border_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, image=image, border_px=border_px,
                         border_color=border_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)


class rectangle(static_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, border_px=None, border_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px=border_px,
                         border_color=border_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)


class circle(rectangle):
    def __init__(self, x, y, r, screen_x, screen_y, color, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, r, 0, screen_x, screen_y, color,
                         None, (0, 0, 0), scale_x, scale_y, offset_x, offset_y)

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        pygame.draw.circle(surface, self.color,
                           (self.x[0], self.y[0]), self.w[0])
        temp = self.color
        self.color = None
        super().process(surface, screen_x, screen_y, scale_x, scale_y, offset_x, offset_y)
        self.color = temp


class single_line_text_box(click_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, color, text='', font_size=10, font='freesansbold.ttf', font_color=(255, 255, 255), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, text, font,
                         font_size, font_color, False, scale_x, scale_y, offset_x, offset_y)
        self.center = 'left'

    def onClick(self):
        if self.minimized or not self.processing:
            return self.noClick()
        self.value = super().onClick()[0]
        return (self.value, pygame.mouse.get_pressed())

    def onPress(self, key, unicode):
        if not self.value or self.minimized or not self.processing:
            return
        keys = pygame.key.get_pressed()
        # shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        # ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        enter = keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]

        if key == pygame.K_BACKSPACE:
            self.change_text(self.raw_text[:-1])
        elif enter:
            self.value = False
        else:
            self.change_text(self.raw_text+unicode)
            if self.text.get_width() > self.rect.w:
                self.change_text(self.raw_text[:-1])
                return False, self.raw_text, key, unicode

        return True, self.raw_text
    
    def get_raw(self):
        return self.raw_text


class Container(rectangle):
    def __init__(self, x, y, w, h, screen_x, screen_y, color=None, border_px=None, border_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px=border_px,
                         border_color=border_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.objects = {}

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        super().process(surface, screen_x, screen_y, scale_x=scale_x,
                        scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        for object in self.objects:
            self.objects[object].process(
                surface, self.w[0], self.h[0], offset_x=self.x[0], offset_y=self.y[0])

    def onClick(self):
        if self.minimized or not self.processing:
            return self.noClick()
        for object in self.objects:
            self.objects[object].onClick()

    def onPress(self, key, unicode):
        if self.minimized or not self.processing:
            return self.noClick()
        for object in self.objects:
            self.objects[object].onPress(key, unicode)

    def add_object(self, name, object):
        self.objects[name] = object

    def delete_object(self, name):
        del self.objects[name]

    def clear_objects(self):
        self.objects = {}

    def get_objects(self):
        return self.objects

    def get_object(self, object):
        return self.objects[object]


class movable_container(Container):
    def __init__(self, x, y, w, h, screen_x, screen_y, top_border_size, top_border_color=None, top_border_title='', color=None, border_px=None, border_color=(0, 0, 0), top_border_font='freesansbold.ttf', top_border_font_size=10, top_border_font_color=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().__init__(x, y, w, h, screen_x, screen_y, color, border_px=border_px,
                         border_color=border_color, scale_x=scale_x, scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)
        self.moving = False
        self.top_border = momentary_button(x, y, w, top_border_size, screen_x, screen_y, top_border_color,
                                           top_border_color, None, top_border_title, top_border_font, top_border_font_size, top_border_font_color)

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        super().process(surface, screen_x, screen_y, scale_x=scale_x,
                        scale_y=scale_y, offset_x=offset_x, offset_y=offset_y)

        data = self.top_border.process(surface, screen_x, screen_y)

        if data and pygame.mouse.get_pressed()[0] and not self.moving:
            self.moving = True
            mouse_pos = pygame.mouse.get_pos()
            self.move_x_offset = mouse_pos[0]-self.x[0]
            self.move_y_offset = mouse_pos[1]-self.y[0]

        elif pygame.mouse.get_pressed()[0] and self.moving:
            # self.moving=False
            mouse_pos = pygame.mouse.get_pos()
            self.set_pos(mouse_pos[0]-self.move_x_offset,
                         mouse_pos[1]-self.move_y_offset, screen_x, screen_y)
            self.top_border.set_pos(
                mouse_pos[0]-self.move_x_offset, mouse_pos[1]-self.move_y_offset, screen_x, screen_y)

        elif not pygame.mouse.get_pressed()[0] and self.moving:
            self.moving = False


class display():
    def __init__(self, containers):
        self.containers = containers
        self.screen = 'main'

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        self.containers[self.screen].process(
            surface, screen_x, screen_y, scale_x, scale_y, offset_x, offset_y)

    def onClick(self):
        self.containers[self.screen].onClick()

    def onPress(self, key, unicode):
        self.containers[self.screen].onPress(key, unicode)

    def select_screen(self,screen):
        self.screen=screen

class seven_segment(variable_object):
    def __init__(self, x, y, w, h, screen_x, screen_y, number='0', color=(127, 127, 127), segment_color_true=(255, 0, 0), segment_color_false=(0, 0, 0), scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if type(number) is not str:
            number = str(number)
        if number not in allowed_segments or len(number) > 1:
            raise Exception(f'{number} not compatible')
        super().__init__(x, y, w, h, screen_x, screen_y, color, '', 'freesansbold.ttf',
                         10, (0, 0, 0), number, scale_x, scale_y, offset_x, offset_y)
        self.segment_color_true = segment_color_true
        self.segment_color_false = segment_color_false
        self.period = False

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        super().process(surface, screen_x, screen_y, scale_x, scale_y, offset_x, offset_y)
        self.segments = []

        zero = (self.x[0]+5, self.y[0], self.w[0]-10, 5)
        one = (self.x[0]+self.w[0]-5, self.y[0]+5, 5, self.h[0]//2-10)
        two = (self.x[0]+self.w[0]-5, self.y[0] +
               self.h[0]//2+5, 5, self.h[0]//2-10)
        three = (self.x[0]+5, self.y[0]+self.h[0]-5, self.w[0]-10, 5)
        four = (self.x[0]+1, self.y[0]+self.h[0]//2+5, 5, self.h[0]//2-10)
        five = (self.x[0]+1, self.y[0]+5, 5, self.h[0]//2-10)
        six = (self.x[0]+5, self.y[0]+self.h[0]//2-2, self.w[0]-10, 5)
        self.segment_boxes = (zero, one, two, three, four, five, six)

        for values in (self.segment_boxes):
            self.segments.append(pygame.Rect(
                values[0], values[1], values[2], values[3]))
        for segment in self.segments:
            if allowed_segments[self.value][self.segments.index(segment)] == '1':
                pygame.draw.rect(surface, self.segment_color_true, segment)
            else:
                pygame.draw.rect(surface, self.segment_color_false, segment)

        if allowed_segments[self.value][-1] == '1' or self.period:
            pygame.draw.circle(surface, self.segment_color_true,
                               (self.x[0]+self.w[0]-3, self.y[0]+self.h[0]-3), 2*1920/1080)
        else:
            pygame.draw.circle(surface, self.segment_color_false,
                               (self.x[0]+self.w[0]-3, self.y[0]+self.h[0]-3), 2*1920/1080)

    def set_value(self, value):
        if type(value) is not str:
            value = str(value)
        if '.' in value:
            self.period = True
        else:
            self.period = False
        if value not in allowed_segments:
            raise Exception(f'{value} not compatible')
        self.value = value


class radio():
    def __init__(self) -> None:
        self.objects = {}
        self.minimized = False
        self.processing = True
        self.selected = None

    def process(self, surface, screen_x, screen_y, scale_x=1, scale_y=1, offset_x=0, offset_y=0):
        if self.minimized:
            return
        for object in self.objects:
            self.objects[object][0].process(
                surface, screen_x, screen_y, offset_x=offset_x+self.objects[object][1], offset_y=offset_y+self.objects[object][2])

    def onClick(self):
        if self.minimized or not self.processing:
            return self.noClick()
        for object in self.objects:
            click = self.objects[object][0].rawClick()
            if click:
                self.selected = object
                break
        for object in self.objects:
            self.objects[object][0].value = object == self.selected
        return click, pygame.mouse.get_pressed()

    def onPress(self, key, unicode):
        if self.minimized or not self.processing:
            return self.noClick()
        if self.selected != None:
            self.objects[self.selected][0].onPress(key, unicode)

    def add_object(self, name, object, x_offset=0, y_offset=0):
        self.objects[name] = (object, x_offset, y_offset)

    def delete_object(self, name):
        del self.objects[name]

    def get_objects(self):
        return self.objects

    def get_object(self, object):
        return self.objects[object]

    def get_selected(self):
        return self.selected


class radio_buttons(radio):
    def __init__(self, x_offset, y_offset, button_class, x_buttons=1, y_buttons=1, labels={'0_0': ('', None, None, None), }):
        super().__init__()
        store_x = x_offset
        store_y = y_offset
        x_offset = 0
        y_offset = 0
        for y_ in range(y_buttons):
            x_offset = store_x
            for x_ in range(x_buttons):
                self.add_object(f'{x_}_{y_}', copy.copy(button_class), x_offset, y_offset)
                try:
                    self.objects[f'{x_}_{y_}'][0].change_text(
                        labels[f'{x_}_{y_}'][0], labels[f'{x_}_{y_}'][1], labels[f'{x_}_{y_}'][2], labels[f'{x_}_{y_}'][3])
                except:
                    pass
                x_offset += store_x
            y_offset += store_y


class linked_textbox(radio):
    def __init__(self, x_offset, y_offset, textbox_class, x_box=1, y_box=1):
        super().__init__()
        store_x = x_offset
        store_y = y_offset
        x_offset = 0
        y_offset = 0
        for y_ in range(y_box):
            x_offset = store_x
            for x_ in range(x_box):
                self.add_object(f'{x_}_{y_}', copy.copy(
                    textbox_class), x_offset, y_offset)
                x_offset += store_x
            y_offset += store_y

    def onClick(self):
        data = super().onClick()
        if not data[0]:
            self.objects[self.selected][0].value = False
            self.selected = None