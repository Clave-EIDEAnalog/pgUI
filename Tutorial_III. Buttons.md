
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


