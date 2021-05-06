

## Tutorial_III. Buttons

# Currently being in preparation!

## 4.- Buttons.
Finally, pgUI will ease you to the always hard task of adding a button to your project. Something like this:

![](https://user-images.githubusercontent.com/64075009/117153865-a4c81e00-adbb-11eb-9aa7-ad09920f3bd5.png)

Monkey with *play - pause* options.

### 4.1.- *Press* buttons.
A *press* button is a button that has a function associated, such a way that every time you press it the binded function in your code will be executed. It will allow you to start/stop the game, change parameters, display things or whatever you like.

We have designed pgUI such a way that you may add widgets to your project by using the minimum amount of effort and time: let's say that you actually want a single button to pause/restart the game (not exactly the image above: just one button). You write a function that toggles a variable -say *pause*- in between *True* and *False* and make the changes needed to achieve what you want; something like:

    pause = False
    def playPause():                                           
        """ Toggle 'pause' flag """
        global pause
        if pause:
            pause = False
        else:
            pause = True

And then, in the main loop,

    if not(pause):                                     
        allsprites.update()

This will suffice: now you may instate a button by:

    UIUser.addButton(action = playPause)
    
and you will get a game window like this:

![](https://user-images.githubusercontent.com/64075009/117265288-603c9100-ae54-11eb-90d0-3a12aa722bb1.png)

Yes: the button is ugly and has no image or text on it. But it serves for the purpose; see 4.2 'MOUSEBUTTONUP pygame event' next


### 4.2.- MOUSEBUTTONUP pygame event.

This paragraph explains the only delicate surgery you have to implement in your code to make pgUI fully operative (just if you include buttons; it's not necessary at all for texts or panels).

A typical pygame loop includes an event queue download and a series of statements to determine what to do depending on the events (that, in many times, are the continuation to the user inputs via mouse, keyboard, joystick, ...). The original monkey game one is:

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

this loop responds to a user request to leave (*event.type == pg.QUIT*; *event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE*) or if the user presses a mouse button (any of them: *event.type == pg.MOUSEBUTTONDOWN*) or releases it (*event.type == pg.MOUSEBUTTONUP*).

The point is that pgUI buttons section needs to know TOO if a mouse button has been released, and the normal procedure using pygame (monkey is a *normal* case) is to discharge completely the event queue (*for event in pg.event.get()*) every loop, such a way that the *pg.MOUSEBUTTONUP* event would disappear without leaving trace. The trick for the pgUI buttons to know whether the user has -pressed and- released a button is to, say, deceive pygame by *retriggering* the event (*pg.MOUSEBUTTONUP*) unconditionally. It's simple:

            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()
                evento = event                              ## pgUI addition
                pg.event.post(evento)                       ## pgUI addition                   

and that's all. As pgUI has it's own event detection code, it will detect this *pseudoevent* and examine if a button has been selected.

### 4.3.- Execute binded function.

Once you have refactored your software as stated, pgUI will inform you every time the user presses a button. The way it does is by means of the *pgUIUser.update()* call. This method returns the function associated to the button (remember: *action = playPause* when instancing the button). The complete code will look like this:

        todo = UIUser.update()                              
        if todo:                                            
            todo()                                          


### 4.4.- Embellishing buttons.

By this time you should have a *pausable* monkey game (try with *pgUI_CHIMP_07_playPause.py* at the CHIMP folder if not). But the button's appareance is unnaceptable: neither it has an icon, nor a help text, so you can't imagine what is it for; unless you are a developper that needed a button to quickly test something in your app, you decisively have to enhance it; something like the first image at the top of this chapter.

#### Adding images.
**WARNING**: All the image files you intend to use with pgUI have to reside in a folder *'data'* that in turn should be into your application folder -the one that holds *pgUI.py* too.

By modifying the instancing line:

       UIUser.addButton(action = playPause, images = [image1, image2])

you tell pgUI to use the graphic files *image1* and *image2* for this button. *image1* is the default button look; if you specify an *image2* file, it will be used when you move the mouse over the button, then improving the user feedback. Needless to say, those files have to be of the pygame accepted formats; the most usual any case: *png, bmp, jpg, jpeg, ...*.  
