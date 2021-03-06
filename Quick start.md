## Quick start.
pgUI has been conceived to be used with a minimum of effort. Please, follow the next steps.

### 1.- Download the file pgUI.py.
Basic use of pgUI needs only the file 'pgUI.py': either copy-paste it or download it to your working directory.

### 2.- Example: adding a fixed text.
#### 2.1.- Import module.
Add the 'import' command to your program

    import pgUI as UI
#### 2.2.- Instance a pgUI user.
    UIUser = UI.user(screen)                               
'screen' being the pygame window name in your program. This line of code will give access to all the pgUI module resources.

#### 2.3.- Add the text you want to be shown.
    UIUser.addInfoText(position = (160, 35),                
                       text = "Chimp says: 'Hello world!'",
                       colors = [(250,0,0), (255,255,255)])
this line will force the text "Chimp says: 'Hello world!'" to unconditionally appear at coordinates (160, 35); 'colors' first member is the text color while second color is the background for the text (normally choosen as the game background color).

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
