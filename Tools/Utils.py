import discord
import json

class Utils:

    async def durationFormat(self, duration):
        temp_seconds = duration / 1000
        seconds = round(temp_seconds % 60)
        temp_minutes = round(temp_seconds // 60)
        minutes = round(temp_minutes % 60)
        temp_hours = round(temp_minutes // 60)
        hours = round(temp_hours % 60) 
        
        if seconds < 10:
            seconds = f"0{seconds}"
        if minutes < 10:
            minutes = f"0{minutes}"
        hours = "" if hours == 0 else f"{hours}:"

        return str(f"{hours}{minutes}:{seconds}")