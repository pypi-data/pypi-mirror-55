import pandas
from rocketchat_API.rocketchat import RocketChat

class Rocket:
    def __init__(self,
        username,
        password,
        server_url='https://chat.bedigital.io'):

        self.api = RocketChat(
            username, password,
            server_url=server_url
        )

        self._users = pandas.DataFrame(self.api.users_list().json()['users'])

        self._groups = pandas.DataFrame(self.api.groups_list().json()['groups'])

        self._ims = pandas.DataFrame(self.api.im_list().json()['ims'])

    @property
    def users(self):
        return self._users[['name', 'username', 'lastLogin']]

    @property
    def groups(self):
        return self._groups[['name', 'msgs', 'lm']]

    @property
    def ims(self):
        return self._ims[['usernames', 'msgs', 'lm']]


    # Sending a Private Message

    def send_to_user(self, username, text, file=None):
      # Example 1: send_private_message('mindey', file='/content/2019 GREPO Price list FOB Ho Chi Minh NEW.pdf', text='sveikas, čia failas')
      # Example 2: send_private_message('mindey', text='sveikas, čia tadas')

      # Find or create the private conversation with the user alone.
      im_create = self.api.im_create(username).json()
      room_id = im_create.get('room').get('_id')

      # sending test message
      if file is not None:
        im_send = self.api.rooms_upload(
            room_id,
            file=file,
            description=text
        )
        print('Send file to: %s [Success]' % username)
      else:
        im_send = self.api.chat_post_message(room_id=room_id, text=text)
        print('Send msg to: %s [Success]' % username)


    # Sending Mass Private Message to Selected Users

    def send_to_users(self, usernames, text='', file=None):
      for username in usernames:
        try:
          self.send_to_user(
              username,
              text=text,
              file=file
          )
        except Exception as e:
            print("Failed to send to: ", username)
            print(e)
            print("Retry with: me.send_to_user('{username}', text='{text}', file={file})".format(username=username, text=text, file=file is None and None or '"%s"' % file))


