## Tutorial. Install pgUI. Texts.

### 1.- Install pgUI.
Installing pgUI does not need a special procedure. Just download or copy-paste the file pgUI.py to your working folder; once done, all pgUI functions are available by importing it:

    import pgUI as UI

### 2.- Texts.
(To demonstrate many of the pgUI library capabilities we have chosen a quite simple pygame made game, 'chimp.py'; we have copied it into this repository so that you can download it and test the add-on features. This game is about hitting a moving chimp: the only *feedback* it originally has is a *pirouette* that he -the chimp- performs every time you hit him; we will add the game texts, statistics and buttons to control its functioning).

#### 2.1.- Instance a pgUI user.
    UIUser = UI.user(screen)                               
'screen' being the pygame window name in your program. This line of code will give access to all the pgUI module resources.

#### 2.2.- Add a text you want to be shown.
Needless to say, by using pygame you can show texts
    UIUser.addInfoText(position = (160, 35),                
                       text = "Chimp says: 'Hello world!'",
                       colors = [(250,0,0), (255,255,255)])
this line will force the text "Chimp says: 'Hello world!'" to unconditionally appear at coordinates (160, 35); 'colors' first member is the text color while second color is the background for the text (normally chosen as the game background color).

#### 2.4.- Add the pgUI update line to your main loop.

Depending on your expertise and preferences, your main -game- loop may be placed at the end of the code, into a 'if __name__ == "__main__":' (more criptic) statement or in a specific function or method. Wherever it is, its look is something like:

    # Main Loop
    going = True
    while going:
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                going = False
            elif ...
            screen.blit(background, (0, 0))         # Erase window command
            # Draw elements
            ...
        pg.display.update()                         # Update screen
       
(This is a quite symplified pygame main loop; should you have already written python/pygame code you have surely identified it)

To make your pgUI added text appear you should add the line

        UIUser.update()                                     
to your code *before* the line 'pg.display.update()' and *after* the 'Erase window command'; depending on the relative position to the rest of your existing drawing commands, the pgUI objects will appear *on top of* or *behind* your game/app objects:
![](https://user-images.githubusercontent.com/64075009/116532848-05012080-a8e1-11eb-922d-f807404ca775.png)

pgUI objects ("Chimp says: Hello world!") appearing on the bottom.