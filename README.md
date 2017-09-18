# Aorta Twitch Bot

Simple and fun Twitch Bot written in Python 3 :)

## Currently supported commands

- `!ruletka` - Russian Roulette implementation.
- `!points` - check user loyalty points.
- `!pogoda <capital city>` - _example: !pogoda warsaw_, returns some useful info about current atmospheric conditions. (in Polish)
- `!lepa <nick>` - slaps _nick_ into the face. If eough hitpoints were dealt to the targeted _nick_ he will be timeouted. (in Polish)
- `!love <nick>` - counts the percentage changes of you getting laid with _nick_
- `!gamble <amount>` - typical hazardous engine :)
- `!gdzie <nick>` - returns the time period in days when _nick_ was last seen.
- `!zbluzgaj <nick>` - will swear towards _nick_
- `!przekaz <username> <number>` - gives `<number>` of loyalty points to the. `<username>`. Transaction costs 10% of the original amount.
- `!status <username>` - only for Privileged users - shows amount of loyalty points of `<username>`

## World Of Tanks Statistics API integration

- `!kills` - returns the number of all opponents fragged by you from the begining of time.
- `!ostatniagra` - returns the timestamp of the last played game of yours.
- `!trees` - returns the total count of trees that were cut by you sitting in the tank.

## Not yet implemented / Ideas
- ~automatic loyalty bonus points for follow/subscribtion~
- ~`!whois <username>` - checks the twitch `<username>`. Provides stuff like: how many days ago he was registered, fullname, birthdate, anything that can be harvested.~
- ~`!imie <imie>` - returns funny First Name definition from pre-defined dictionary~
- ~`!sr <song>` - song request functionality~
- ~`!skip` - skip currently playing song~

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
