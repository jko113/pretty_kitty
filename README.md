# Pretty Kitty

### Description
Pretty Kitty is a Pygame application that both calms and tantalizes the feline friend. At each turn, the player has the option to pet, feed or chase the protagonist kitty, and each action provokes a reaction and leads the player closer to game's end.

Both mouse input (on interactive buttons) and left/right arrow key input are listened for by the program. Engaging sounds punctuate game play.

### Technology
Pretty Kitty is coded in Python 3 and was tested with Pygame version 1.9.3.

### Motivation
Pretty Kitty was designed to be fun, funny, and ever-so-slightly addictive. It is suitable for children and adults alike.

### Challenges

#### Logic
Coding this game was a stimulating exercise in logic. Building the game honed my debugging skills by familiarizing me with various error messages, such as indentation mistakes or referencing variables before assignment.

A signicant logic struggle I overcame was modifying "global variables" within the scope of a function. Since excessive use of global variables is frowned upon, I aimed for the best practice and passed the objects I needed to modify as parameters. This resolved the local variable errors and, in my opinion, improved the overall integrity and portability of the code.

Here is a function that passes dictionaries relevant to the main program:

```python
def respond_to_click(key, all_prompts, active_prompts):
    points = active_prompts[key]["points"] + 1
    active_prompts[key].update({"points": points})
    all_prompts[key + "_points"].update({"points": str(points)})
```

#### Booleans
Correctly utilizing boolean values (or flags) was essential to properly directing the flow and behavior of the game. Though this is clearly part and parcel to the overall game logic, this was so crucial that it deserves its own section. If I were to refactor through more iterations, I would most likely implement a boolean dictionary to efficiently store and access flags. As it was, *sigh*, time was of the essence, so here is a sample of some booleans I set and how they affected the program's behavior:

```python
done = False
did_win = False
first_point = True
show_devil = False
```
These were declared and initialized prior to entering the game's main loop. In the game itself, `done` controls when the game ends. `did_win`, meanwhile, allowed me to start a timer after winning the game but before terminating the program. This was the perfect time to display a "winning text" message, which as you will see below, doesn't always indicate the player actually wins.

The `first_point` flag let me strictly control the accumulation of points by setting a maximum of one point per click. Without this logic, clicking once on an interactive button without releasing the mouse would continue accruing points.

Finally, `show_devil` ("devil" here refers to a spooky-looking kitty) enabled me to control when and how long the devil_cat image displays on screen. This was particularly impactful for when devil_cat displays on the "winning text" screen - the behavior is different to other situations.

#### Dictionaries
Speaking of dictionaries, implementing this data structure was vital to the coherence of the program. As I progressed through the project, I quickly realized how difficult it is to maintain well-organized code, particularly where data is concerned. Dictionaries made it quite easy to link together disparate items, such as two sets of prompts, among which 3 out of 7 constitute interactive buttons.
 
```python
active_prompts = {
    "pet": {
        "prompts": (445, 550, 75, 100),
        "points": 0,
        "end": "Good Kitty!"
    },
    "feed": {
        // data
    },
    "chase": {
        // data
    }
}

all_prompts = {
    "question": {
        "label": "What do you want to do?",
        "location": (425,50),
        "rectangle": (150,450,100,50),
        "color": None
    },
    "pet": {
        // data
    },
    "feed": {
        // data
    },
    "chase": {
        // data
    },
    "pet_points": {
        // data
    },
    "chase_points": {
        // data
    },
    "feed_points": {
        // data
    },
}
```

By keeping the naming of keys consistent, this made it simple to also link together the dictionary for tracking points in the respond_to_click() method pasted in the Logic section above:

 ```python
points_dict = {
    "fun_points": 0,
    "bad_points": 0,
    "meal_points": 0,
}

for key in all_prompts:
  if all_prompts[key]["color"]:
      pygame.draw.rect(screen, all_prompts[key]["color"], all_prompts[key]["rectangle"])

  # selectively style prompts based on if the prompt
  # tracks points or not
  has_point = "points" in all_prompts[key].keys()
  if has_point:
      label = all_prompts[key]["label"] + all_prompts[key]["points"]
  else:
      label = all_prompts[key]["label"]
  text = font.render(label, True, (0, 0, 0))
  screen.blit(text, all_prompts[key]["location"])
```
### Screenshots
![Cute Kitty](https://github.com/jko113/pretty_kitty/blob/master/images/cute_kitty.png)

![Bad Kitty](https://github.com/jko113/pretty_kitty/blob/master/images/bad_kitty.png)
