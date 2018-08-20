#menu.py
# Menu pop-up
menu_data = (
    'Barn Defense',
    'Start',
    'Quit',
)
PopupMenu(menu_data)
for e in pygame.event.get():
    if e.type == USEREVENT and e.code == 'MENU':
        print 'menu event: %s.%d: %s' % (e.name,e.item_id,e.text)
        if (e.name,e.text) == ('Main','Quit'):
            quit()
            
# Scoreboard pop-up
