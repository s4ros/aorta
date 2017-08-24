# Aorta Twitch Bot

## Where's the old bot?
I evolved and figured out how to do it more efficient :) However, you can still find my previous nasty code in a branch `first_attempt`. So, without further ado, I present you *AortaBot*, the new begining :D

Hope you'll enjoy :)

## Ideas
Project will be dockerized.

Any functional ideas that could be implemented in the future
- automatic ~Revlo~ bonus points for follow/subscribtion
- `!whois <username>` - checks the twitch `<username>`. Provides stuff like: how many days ago he was registered, fullname, birthdate, anything that can be harvested.
- `!give <username> <number>` - gives `<number>` of ~Revlo~ points to the. `<username>`. Cannot be executed more than once per **x** minutes.
- `!ruletka` - Russian Roulette implementation.
- `!points` - check user ~Revlo~ points. If requested more than once within **X** minutes, the answer will go as whisper.
- `!imie <imie>` - returns funny First Name definition from pre-defined dictionary
- `!sr <song>` - song request functionality
- `!skip` - skip currently playing song

### Badges
Now, when we can receive additional data from Twitch IRC, we can think about new functionalities using the badges, for example:

```
moderator/1,subscriber/0,partner/1,bits/100,broadcaster/1
```

Bot will know how many bits does user have. How long he's subscribing, if he's moderator, and so on. This opens lots of possibilities.

Badges
- premium - Twitch Prime
- moderator - channel moderator
- subscriber - user subscribes channel
- bits - user bought some bits
- partner - other streamer/Twitch partner/confirmed user
- admin
- broadcaster - streamer himself
- global_mod
- staff
- turbo
