# VKChatBot

Usage:
```
group_access_token = os.getenv('VK_GROUP_TOKEN')
group_id = os.getenv('VK_GROUP_ID')
bot = VKChatBot(access_token=group_access_token, group_id=group_id)
bot.register_command('фио', cmd_get_name)
bot.register_command('неделя', cmd_get_week)
bot.register_command('помощь', cmd_help)
bot.register_command('время', cmd_get_time)
bot.register_command('звонки', cmd_get_timetable)
bot.unknown_command_msg = unknown_command
bot.work()
```

I'm not planning to maintain this library very active and to write verbose documentation at this moment.