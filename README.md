# GMTK-2022

A basic game engine for game jam

# Engine

It include
    
    Variable
        player      -> entity
        screen      -> pygame.Surface
        display     -> pygame.Surface
        
        camera
            scroll : list
            rect   : pygame.Rect
    
    Method
        __int__ (WINDOWN_SIZE, SCALE, FPS, img_FPS)
            render(DEBUG = False) -> None

How to use ?

    e = Engine(WINDOWN_SIZE, SCALE, FPS, img_FPS)
    DEBUG = True
    while True:
        e.render(DEBUG)
        
        game event
        key events
        
        pygame.display.update()

# Database
All file in python use same database

It include 

    tile_rects[]      -> store list of pygame.Rect
    tile_ID[]         -> store ID of tile
    object_camera[]   -> store objects collide with camera
    entity_camera[]   -> store entities collide with camera

    entities[]        -> store all entities in map
    objects[]         -> store all objects in map   

    multiply_factor   -> factor to fix drop FPS
    FPS               -> FPS of the game 

How to use ?
    
    import engine.database as db
    db.tile_rects

# Entity and Object
    
    __int__ (ID, pos, status = 'idle', tag = [])
    
        Variable
            self.tag        : list of tag
                tag: string
                    'tile'
                    'object'
                    'entity'
                    'movable'
            
            self.collision  : dictionary
                {'top': False, 
                'bottom': False, 
                'right': False, 
                'left': False}
            
            self.near_by    : dictionary 
                {'left': [],  store list of entity, object ID and 'tile' near by
                'right': [], 
                'up': [], 
                'down': [], 
                'surround': []}
    
            self.ID     : string
            self.status : string
            self.pos    : list
                [x, y]
            self.x      : float
            self.y      : float
            
            self.offset
            self.rect
            self.width
            self.height
            self.flip

            Only in entity
                self.health     : float
                self.life       : int
                self.hitbox     : pygame.Rect
        
        Method
            get_nearby_rect(direction)  -> pygame.Rect
                direction: string
                    'left'
                    'right'
                    'up'
                    'down'
                    'surround'

            move(movement)              -> None
                movement: list
                [speed_x, speed_y]
            
            change_action(status, offset = [0, 0] -> None
                status  : string
                    Ex: 'idle'
            
            add_tag(tag)                -> None
                tag : string
            
            change_tag(list_of_tag)             -> None
            
