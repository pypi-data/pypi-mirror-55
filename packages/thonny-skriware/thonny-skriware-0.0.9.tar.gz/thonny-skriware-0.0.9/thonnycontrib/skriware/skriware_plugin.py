import contextlib
import io
import os
import threading
import time

import esptool
import ipdb
import thonny
from ampy.files import Files as FileHandler
from ampy.pyboard import Pyboard, PyboardError
from thonny import get_workbench
from thonny.workbench import (BasicUiThemeSettings, CompoundUiThemeSettings,
                              SyntaxThemeSettings)


class SkriwarePlugin:
  instance = None

  @staticmethod
  def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)

  def __init__(self):
    if SkriwarePlugin.instance is None:
      SkriwarePlugin.instance = self 
      self.workbench = get_workbench()
      self.scripts = (
        'boot.py',
        'scratchpad.py',
        'example_functions.py',
        'example_avoid_obstacles.py',
        'example_line_follower.py'
      )
      self.commands = (
        {
          'name': 'Debug (ipdb)',
          'handler': self.debug,
          'icon': SkriwarePlugin.relpath('debug.png'),
          'menubar': True,
          'toolbar': False,
        },
        {
          'name': 'Upload micropython',
          'handler': self.upload_micropython_handler,
          'icon': SkriwarePlugin.relpath('upload.png'),
          'menubar': True,
          'toolbar': True,
        },
        {
          'name': 'Open boot.py',
          'handler': lambda: self.open_remote_file('boot.py'),
          'icon': SkriwarePlugin.relpath('boot.png'),
          'menubar': True,
          'toolbar': True
        },
        {
          'name': 'Open scratchpad',
          'handler': lambda: self.open_remote_file('scratchpad.py'),
          'icon': SkriwarePlugin.relpath('scratchpad.png'),
          'menubar': True,
          'toolbar': True
        },
        {
          'name': 'Restart robot',
          'handler': lambda: self.run_script(
            'from machine import reset\nreset()\n'),
          'icon': SkriwarePlugin.relpath('restart.png'),
          'menubar': True,
          'toolbar': True, 
        },
        {
          'name': 'Load robot in the interpreter',
          'handler': lambda: self.run_script(
            'from skribot import Skribot\nrobot=Skribot()\n'),
          'icon': SkriwarePlugin.relpath('robot.png'),
          'menubar': True,
          'toolbar': True,
        },
      )
    else:
      pass

  # NOTE: Utilities
  def load_plugin(self):
    for cmd in self.commands:
      if cmd['menubar']:
        self.workbench.add_command(
          command_id=cmd['name'].lower().replace(' ', '_'),
          menu_name='Skriware',
          command_label=cmd['name'],
          handler=cmd['handler']
        )
    
    for example in [s for s in self.scripts if s.startswith('example_')]:
      label = example.replace('example_', '')
      label = label.replace('_', ' ').replace('.py', '').strip().title()

      self.workbench.add_command(
        command_id=example,
        menu_name='Skribot examples',
        command_label=label,
        handler=lambda example=example: self.open_remote_file(example)
      )

    self.workbench.add_ui_theme(
      'Skriware Theme',
      'Clean Sepia',
      SkriwarePlugin.theme,
      SkriwarePlugin.theme_image_map()
    )

    # Try creating toolbar buttons until success
    # The toolbar object is initialized AFTER the load_plugin is called
    toolbar_button_thread = threading.Thread(target=self.create_toolbar_buttons)
    toolbar_button_thread.start()
  
  def create_toolbar_buttons(self):
    while True:
      try:
        for cmd in self.commands:
          if cmd['toolbar']:
            self.workbench._add_toolbar_button(
              cmd['name'],
              self.workbench.get_image(cmd['icon']),
              cmd['name'],
              cmd['name'],
              None,
              None,
              cmd['handler'],
              None,
              800
            )
        break
      except:
          continue
  
  def shell_print(self, text, end='\n'):
    shell = thonny.get_shell().text
    shell._insert_text_directly('{}{}'.format(text, end))
    self.shell_scroll_down()
  
  def shell_clear(self):
    shell = thonny.get_shell().text
    shell._clear_content(0.1)
    shell._clear_shell()
  
  def shell_scroll_down(self):
    shell = thonny.get_shell().text
    shell.see('end')

  def shell_print_status(self, iostream):
    while True:
      self.shell_clear()
      self.shell_print(iostream.getvalue())
      time.sleep(1)
      if self.shell_print_status_break:
        break

  def run_script(self, script):
    shell = thonny.get_shell().text
    shell._submit_input(script)

  # NOTE: Custom commands
  def debug(self):
    shell = thonny.get_shell()
    runner = thonny.get_runner()
    ipdb.set_trace()

  def open_remote_file(self, fname):
    runner = thonny.get_runner()
    if runner.ready_for_remote_file_operations():
      notebook = self.workbench.get_editor_notebook()
      try:
        notebook.show_remote_file(fname)
      except:
        self.shell_print('No such file: {}'.format(fname))
      return True
    else:
      print('runner not ready for remote operations')
      return False
    
  def upload_micropython_handler(self):
    s = io.StringIO()
    upload_thread = threading.Thread(target=self.upload_micropython, args=(s,))
    upload_thread.start()

  def upload_micropython(self, iostream):
    self.shell_clear()
    self.shell_print('\rMicropython upload')

    self.shell_print_status_break = False
    status_thread = threading.Thread(
      target=self.shell_print_status, args=(iostream,))
    status_thread.start()

    runner = thonny.get_runner()
    try:
      port = runner.get_backend_proxy()._port
    except AttributeError:
      self.shell_print_status_break = True
      status_thread.join()
      self.shell_clear()
      self.shell_print('No board connected, aborting...')
      return

    self.shell_print('Disconnecting backend')
    runner.disconnect()

    self.shell_print('Erasing flash')
    with contextlib.redirect_stdout(iostream):
      esptool.main((
        '--port', port,
        'erase_flash'
      ))

    self.shell_print('Uploading micropython firmware')
    # upload the main micropython binary
    with contextlib.redirect_stdout(iostream):
      esptool.main((
        '--chip', 'esp32',
        '--port', port,
        '--baud', '460800',
        'write_flash', '-z',
        '--flash_mode', 'dio',
        '--flash_freq', '40m',
        '0x1000', SkriwarePlugin.relpath('micropython-skribot/firmware.bin')
      ))

    # Stop printing stdouts of commands
    self.shell_print_status_break = True
    status_thread.join()
    time.sleep(1)

    board = Pyboard(port)
    file_handler = FileHandler(board)

    for script in self.scripts:
      with open(
        SkriwarePlugin.relpath(
          'micropython-skribot/{}'.format(script)), 'r') as fh:
          data = fh.read()
          self.shell_print('Uploading {} script'.format(script))
          file_handler.put(script, data)
      time.sleep(1)

    self.shell_print('Restarting backend')
    runner.cmd_stop_restart()

    # This is required to properly load newly-uploaded boot.py
    time.sleep(1)
    self.shell_clear()
    self.run_script('from machine import reset\nreset()\n')

    # Restart backend one last time to exit boot.py loop
    runner.cmd_stop_restart()

  # NOTE: Theme methods
  @staticmethod
  def theme_image_map():
    return {
      #'run-current-script': 'media-playback-start48.png',
      #'stop': 'process-stop48.png',
      #'new-file': 'document-new48.png',
      #'open-file': 'document-open48.png',
      #'save-file': 'document-save48.png',
      #'debug-current-script': 'debug-run48.png',
      #'step-over': 'debug-step-over48.png',
      #'step-into': 'debug-step-into48.png',
      #'step-out': 'debug-step-out48.png',
      #'run-to-cursor': 'debug-run-cursor48.png',
      #'tab-close': 'window-close.png',
      #'tab-close-active': 'window-close-act.png',
      #'resume': 'resume48.png',
      #'zoom': 'zoom48.png',
      #'quit': 'quit48.png',
    }

  @staticmethod
  def theme() -> CompoundUiThemeSettings:
    '''This will be a long method'''
    return [
      {
        #'.': {'configure': {'background': '#00c7e1'}},
        'Menu': {
          'configure': {
            'background': '#f00'
          }
        },
        'Menubar': {
          'configure': {
            'foreground': '#f00'
          }
        }
      },
    ]

  @staticmethod
  def syntax_theme():
    return {}
