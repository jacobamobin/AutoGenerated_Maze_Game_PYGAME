elif room[row][column] == "⎊":
        room[row][column] == "⎊R"
        #pygame.draw.rect(screen, EnemyColor, rectangle)
        if row < 28 and row > 3 and column > 3 and column < 28:
          #ENEMY AI
          if room[row][column] == "⎊R":
            if room[row][column+1] != "■" and room[row][column+1] != "⎊L" and room[row][column+1] != "⎊R":
              room[row][column+1] = "⎊"
              room[row][column] = " "
              screen.blit(imageE,((column*sq_sz)+1, row*sq_sz))
            elif room[row][column+1] == "■" or room[row][column+1] == "⎊R" or room[row][column+1] == "⎊L:":
              room[row][column] = "⎊L"
          elif room[row][column] == "⎊L":
            if room[row][column-1] != "■" and room[row][column-1] != "⎊L" and room[row][column-1] != "⎊R":
              room[row][column-1] = "⎊L"
              room[row][column] = " "
              screen.blit(imageF,((column*sq_sz)+1, row*sq_sz))
            elif room[row][column-1] == "■" or room[row][column-1] == "⎊R" or room[row][column-1] == "⎊L":
              room[row][column] = "⎊R"


              if lasercooldown < 5:
      for l in (len(room)):
        for j in (len(room[l])):
          if room[nA][nA] == "■" or "$":
              room[nA][nA] = "L"
          if room[nA][nA] == "P":
              lives -= 1
          else:
              room[nA][l] = "L"
    for row in range(len(room)):
        for column in range(len(room[row])):
            if room[row][column] == "L":
                rectangle = pygame.Rect(column * sq_sz, row * sq_sz, sq_sz,
                                        sq_sz)
                pygame.draw.rect(screen, PortalColor, rectangle)



while GameState != 2:  #THIS CONSTANTLY RUNS THE GAME
    if GameState == 1:
        terrain()
        score = 0
        lives = 3
        level = 1
        GameState = 0
    #player controls
    events = pygame.event.get()
    move_ticker = 0
    #for event
    for event in events:  #GETTING PLAYER INPUTS
        keys = pygame.key.get_pressed()
        if move_ticker == 0:
            #Input Collection
            if keys[pygame.K_LEFT]:
                move_ticker = 10
                move("left")
            if keys[pygame.K_RIGHT]:
                move_ticker = 10
                move("right")
            if keys[pygame.K_UP]:
                move_ticker = 10
                move("up")
            if keys[pygame.K_DOWN]:
                move_ticker = 10
                move("down")
        #move ticker
        if move_ticker > 0:  #PLAYER TICKER (PLAYER DOSENT ZOOM)
            move_ticker -= 5
    #Handles laser boss
    draw_window()  #DISPLAYS ROOM IN GAME WINDOW
    lasercooldown -= 1  
    if lasercooldown == 0:
      nA = random.randint(1, 29)
      room[nA][0] = "L"
      room[nA][28] = "L"
      lasercooldown = 10
    if lasercooldown == 0:
      for row in range(len(room)): 
        for column in range(len(room[row])):
          rectangle = pygame.Rect(column * sq_sz, row * sq_sz, sq_sz, sq_sz)
          if room[row][column] == "L":
            room[row][column] = "L2"
            pygame.draw.rect(screen, LaserColor, rectangle)
          elif room[row][column] == "L2":
            room[row][column] = "L3"
            pygame.draw.rect(screen, LaserColor, rectangle)
          elif room[row][column] == "L3":
            room[row][column] = "L4"
            pygame.draw.rect(screen, LaserColor, rectangle)
          elif room[row][column] == "L4":
            room[row][column] = "L5"
            pygame.draw.rect(screen, LaserColor, rectangle)
          elif room[row][column] == "L5":
            room[row][column] = "L6"
            pygame.draw.rect(screen, LaserColor, rectangle)
          elif room[row][column] == "L6":
            for row in range(len(room[column])):
              if room[row][column] != "|" and room[row][column] != "P":
                room[row][column] = "L6"
              if room[row][column] == "L6":
                
                pygame.draw.rect(screen, LaserColor, rectangle)
    printroom()  #DISPLAYS ROOM IN CONSLE
    #draw_window()  #DISPLAYS ROOM IN GAME WINDOW
    replit.clear()
    #print("Score: " + str(score))
    #print("Lives: " + str(lives))
    pygame.display.update()

    time.sleep(0.5)

#testing
