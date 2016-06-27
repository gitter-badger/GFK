import itertools

console.log(itertools.miter())

rgb2hex = JS.rgb2hex
color1 = rgb2hex("rgba(255,0,0,0)")
color2 = rgb2hex("rgba(255,255,0,0)")
color3 = rgb2hex("rgba(255,255,255,0)")
color4 = rgb2hex("rgba(255,0,255,0)")
color5 = rgb2hex("rgba(255,80,80,0)")
color6 = rgb2hex("rgba(255,128,0,0)")
color7 = rgb2hex("rgba(255,128,255,0)")
color8 = rgb2hex("rgba(255,0,128,0)")

colors = [color1,color2, color3, color4, color5, color6, color7, color8]
allcolors = [color for  tuplecolor in zip(colors, colors) for color in tuplecolor]
JS.shuffle(allcolors)


thingsToLoad = ["sounds/music.wav", "sounds/bounce.wav"];

# Helper Functions:
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True


# Main Grid wich contents all the cells
# Grille principale contenant les cellules
class Grid:
    def __init__(self, game, rows=4,  cols=4):
        self.offset = 4
        self.game = game
        self.rows = rows
        self.cols = rows
        self.ligs = [[0 for i in range(self.rows)] for j in range(self.cols)]
        self.spr = [[0 for i in range(self.rows)] for j in range(self.cols)]

    def  display(self):
        numcells = self.rows * self.cols
        cells = range(16)
        JS.shuffle(cells)
        JS.shuffle(colors)
        for num in cells:
            color = allcolors[num]
            i, j = num % self.cols, num // self.rows
            posx, posy  = j *(128  + self.offset ), i * (128  + self.offset ) 

            # FrontFace : Sprite or Color
            sprite = self.game.rectangle(128, 128, color)
            sprite.x = posx
            sprite.y = posy
            sprite.num = num
            sprite.content  = color
            sprite.showed = False

            # Backface 
            rectb = self.game.rectangle(128, 128, "blue")
            rectb.x = posx
            rectb.y = posy
            rectb.num = num
            self.ligs[i][j] = rectb
            self.spr[i][j] = sprite



# Game Handler
# Gestion du Jeu                                     
class Memory:
    def __init__(self, width=512, height=512):
        self.game = hexi(width, height, self.setup, thingsToLoad, self.load)
        self.game.backgroundColor = "#ffffff"
     
        self.mouse = self.game.pointer
        self.mouse.tap = self.tap
        self.grid = Grid(self.game)
        self.curcell = None
        self.counter = -1
        self.comparator = []
        self.tapped = True

    def load(self):

        self.setup()

    def tap(self):
        self.tapsound.play();
        self.tapped = True

    def setup(self):
        self.music = self.game.sound("sounds/music.wav");
        self.tapsound = self.game.sound("sounds/bounce.wav");
        self.music.loop = True        
        self.music.play()
        self.game.scaleToWindow("seaGreen")
        self.grid.display() 
        self.game.state = self.play

    def get_curcell(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                curcell = self.grid.ligs[i][j]
                if(self.game.hit(self.game.pointer, curcell)):
                    self.curcell = curcell      

    def inc_counter(self):
        self.counter += 1
        if self.counter > 1:
            self.counter = 0
            self.comparator = []

    def check_comparator(self):
        numrows = self.grid.rows
        numcols = self.grid.cols 

        def resetcell(cells):
            def _reset():
                cells[0].alpha = 1
                cells[1].alpha = 1
            return _reset 

        if len(self.comparator) > 1:
            cella, cellb = self.comparator[0], self.comparator[1]
            if (cella.num != cellb.num ):                
                    icella, jcella = cella.num % numcols, cella.num // numrows
                    icellb, jcellb = cellb.num % numcols, cellb.num // numrows
                    spritea = self.grid.spr[icella][jcella]
                    spriteb  = self.grid.spr[icellb][jcellb]
                    contenta = spritea.content 
                    contentb = spriteb.content                     
                    cellb.alpha = 0
                    cella.alpha = 0                     
                    if (contenta != contentb):
                        setTimeout(resetcell([cella, cellb]), 1000)
                    else:
                        spritea.showed = True
                        spriteb.showed = True


    def check_endgame(self):
        # flatten liste sprites
        # On 'applatit la liste des sprites'
        lst_spr = [sprite for liste_sprites in self.grid.spr for sprite in liste_sprites]
        showed_values = [s.showed for s in lst_spr]
        if (all(showed_values)):
            for s in lst_spr:
                s.alpha = 0
            self.game.state = self.end

    def play(self):
        self.check_endgame()     
        self.get_curcell()
        if (self.mouse.tapped):
            self.inc_counter()
            self.comparator[self.counter] = self.curcell
            self.mouse.tapped = False
            self.check_comparator()

    def start(self):
        self.game.start()

    def end(self):
        self.game.backgroundColor = "seagreen"
        console.log("END")

memory = Memory()
memory.start()