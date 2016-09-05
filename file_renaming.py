import os

def 
for filename in os.listdir("."):
  if filename.startswith("[The_M1HA3L] Breaking Bad "):
    os.rename(filename, filename.replace("[The_M1HA3L] Breaking Bad ", "Breaking Bad s02e"))

ext = '.mp4'
for filename in os.listdir("."):
  filename_id, cap_name = filename.split(' - ')
  os.rename(filename, filename_id + ext)


import re
p = re.compile("s(\d{2})e(\d{2})")
for filename in os.listdir('.'):
   match = p.search(filename)
   print match.group(0), match.group(1), match.group(2)
   new_filename = re.sub(p, episode_replace, filename, count=1)
   
def episode_replace(match):
  episode_real_number = int(match.group(2)) - 20
  return "s{}e{}".format(match.group(1), str(episode_real_number))

