
# Using RocketChat:

```python
from digital import Rocket

rocket = Rocket('myuser', 'mypassword', server_url='https://chat.rocket.server')

rocket.send_to_users(
    ['mindey', 'tomas', 'gaile'],
    text='Sveiki, ar matote?',
    file='/content/somefile.pdf'
)
```
