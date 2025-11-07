(define (domain vampire)
    (:requirements :conditional-effects)
    (:predicates
        (light-on ?r)
        (slayer-is-alive)
        (slayer-is-in ?r)
        (vampire-is-alive)
        (vampire-is-in ?r)
        (fighting)
        ;
        ; static predicates
        (NEXT-ROOM ?r ?rn)
        (CONTAINS-GARLIC ?r)
        (changedLight)
    )
    (:action toggle-light
        :parameters (?anti-clockwise-neighbor ?room ?clockwise-neighbor)
        :precondition (and
            (NEXT-ROOM ?anti-clockwise-neighbor ?room)
            (NEXT-ROOM ?room ?clockwise-neighbor)
            (vampire-is-alive)
            (slayer-is-alive)
            (not (fighting))
        )
        :effect (and
            (not(changedLight))
            (when
                (light-on ?room)
                (and(not(light-on ?room))(changedLight)) ;switch off the light
            )
            (when
                (and(not(light-on ?room))(not(changedLight)))
                (and(light-on ?room)(changedLight)) ; switch on the light
            )
            (
                ;When the vampire is in a bright room and there isn't light in the anti-clockwise room -> vampire in anticlockwise room
                when
                (and(vampire-is-in ?room)(light-on ?room)(not(light-on ?anti-clockwise-neighbor))) 
                (and          
                    (not(vampire-is-in ?room))
                    (vampire-is-in ?anti-clockwise-neighbor)
                    ;Check if the slayer and vampire are in the same room -> begin fighting
                    (when
                        (and(slayer-is-in ?anti-clockwise-neighbor) (vampire-is-in ?anti-clockwise-neighbor))
                        (fighting)
                    )
                ) 
            )
            (
                ;When the vampire is in a bright room and there is light in the anti-clockwise room -> vampire in clockwise room
                when
                (and(vampire-is-in ?room)(light-on ?anti-clockwise-neighbor) (light-on ?room))
                (and
                    (not(vampire-is-in ?room))
                    (vampire-is-in ?clockwise-neighbor)
                    (when
                        (and(slayer-is-in ?clockwise-neighbor) (vampire-is-in ?clockwise-neighbor))
                        (fighting)
                    )
                )
            )
           
            (
                ;When the slayer is in a dark room and there is light in both neighbors -> slayer in anti-clockwise room
                when
                (and(slayer-is-in ?room)(not(light-on ?room))(light-on ?clockwise-neighbor)(light-on ?anti-clockwise-neighbor)) 
                (and
                    (not(slayer-is-in ?room))
                    (slayer-is-in ?anti-clockwise-neighbor)                 
                    (when
                        (and(slayer-is-in ?anti-clockwise-neighbor) (vampire-is-in ?anti-clockwise-neighbor))
                        (fighting)
                    )
                )
            )
            (
                ;When the slayer is in a dark room and there is light in clockwise neighbors -> slayer in clockwise room
                when
                (and(slayer-is-in ?room)(not(light-on ?room))(light-on ?clockwise-neighbor)) 
                (and(not(slayer-is-in ?room))(slayer-is-in ?clockwise-neighbor)
                    (when
                        (and(slayer-is-in ?clockwise-neighbor) (vampire-is-in ?clockwise-neighbor))
                        (fighting)
                    )
                )  
            )
           
            (
                ;When the slayer is in a dark room and there is light in anti-clockwise neighbors -> slayer in anti-clockwise room
                when
                (and(slayer-is-in ?room)(not(light-on ?room))(not(light-on ?clockwise-neighbor)))
                (and(not(slayer-is-in ?room))(slayer-is-in ?anti-clockwise-neighbor)
                (when
                    (and(slayer-is-in ?anti-clockwise-neighbor) (vampire-is-in ?anti-clockwise-neighbor))
                    (fighting)
                ))  
            )
            
        )
    )
   
   
   
    (:action watch-fight
        :parameters (?room)
        :precondition (and (slayer-is-in ?room) (vampire-is-in ?room) (slayer-is-alive) (vampire-is-alive) )
        :effect (and
            (
                when
                (and(light-on ?room ) ); when the light is on  
                (and(not(vampire-is-alive))(slayer-is-alive)) ; kill vampire, stop fighting
            )
            (
                when
                (and(CONTAINS-GARLIC ?room) ); when room cointains garlic
                (and(not(vampire-is-alive))(slayer-is-alive)) ; kill vampire, stop fighting
            )
            (
                when
                (and(not(light-on ?room))(not(CONTAINS-GARLIC ?room))) ; when the light is off and there is no garlic
                (and(not(slayer-is-alive))(vampire-is-alive)) ; kill slayer, stop fighting
            )
        )
    )
   
)