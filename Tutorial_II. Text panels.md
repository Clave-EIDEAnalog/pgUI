
## Tutorial_II. Text panels.

# Currently being in preparation!

## 3.- Text panels.
Last tutorial has tought you to insert texts in the pygame window and how to modify them so that the texts show how your game skills progress. By using those *infoTexts* and having a bit of patience you may get also something this stylish:

![](https://user-images.githubusercontent.com/64075009/117021610-c95ac200-acf7-11eb-860e-3a20e9e23ee0.png)

which shows a complete set of information on the matter.

To do it by using the tools described in the last paragraph is a bit clumsy: you have to calculate widths and heights of texts so that they appear perfectly aligned into columns.

pgUI has a class *textPanel* which takes charge of placing things so that you can forget about the hard part of the task: you just tell pgUI which texts -fixed: left column; variable: right column- you want to form the panel, the position of the panel, size and colors to use and *voilá*, pgUI organizes it all so that you can concentrate again on your scenario. (Nevertheless, it may happen that you do not plan to use many *text panels* and prefer to build one by using just *infoText*: it works exactly the same; you can skip the rest of the chapter)

## 3.1.- Passing functions as arguments.
In this tutorial we take for granted that the reader has a solid basis on python/pygame. Nevertheless, we deem appropiate to insist in that, as almost everything in python, a function is an object too, and as such, it can be passed as an argument to another function or method. This property is in the root of how to instance a text panel.

## 3.2.- Building the whole text panel.
Let's see how to build the text panel on the chimp game above: the nucleus of the issue is building two lists, one with the texts on the first column -fixed texts- and other with the variable texts; this one is made up not by texts, but for functions that return the desired text -the variable text to be shown-.

This is the code:

    # pgUI functions
    def totalTrials():
        return trials
    def totalHits():
        return hits
    def percentage():
        if trials == 0: return "0 %"
        return (str(int(100*hits/trials)) + " %")
    textPanelF = [totalHits, totalTrials, percentage]
    
    textPanelT = ["Total hits", "Total trials", "Success"]

There are three functions that return the value to be shown: while the two first ones *just* return the variable, the other performs a previous calculation and then returns the value. Remember: the important thing is that the function returns the *thing* to be shown, either if it -the function- calculates it or not. The three functions are then collected into a list: *textPanelF*.

Other list -*textPanelT*- has the three headers for the variable texts. Needless to say, they are ordered the same.

Once we have the two lists, the instantiation of the panel is like this:

    UIUser.addTextPanel(position = (400, 5),
                        texts = textPanelT,
                        parameters = textPanelF,
                        size = 17,
                        colors =[(0,0,0),
                                 (255,255,255)]
                       )                                   

quite similar, by the way, to the single text -*infoText*; see 2.2- instantiation.

## 3.3.- Updating the text panel.
You don't need to specifically update the panel; the *general* pgUI update command

    UIUser.update()
    
takes care of it. Your code just needs to update the variables to be shown (see 2.3 and 2.4)






