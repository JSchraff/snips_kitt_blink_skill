# snips_kitt_blink_skill
a skill for snips that blinks leds and replaces default tone

#Installation 
add snipsuser to gpio group manually if leds are used
```
usermod -a -G gpio _snips
usermod -a -G gpio _snips-skills
```