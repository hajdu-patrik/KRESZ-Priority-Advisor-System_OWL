from owlready2 import *

# This is where classes and their relationships are defined. (Ontology + SWRL Rules)
def calculate_priority(vehicle_a_data, vehicle_b_data):
    """
    KRESZ 28. § alapján eldönti, kinek van elsőbbsége.
    Input: dict-ek a járművek adataival (típus, út típusa, tábla, irány).
    """
    # --- 1. BUILDING ONTOLOGY (In-memory) ---
    # TBox initialization (Terminology Box)
    onto = get_ontology("http://test.org/kresz_full.owl")

    with onto:
        # --- Classes (Concepts) ---
        # Representing the hierarchy of traffic entities (OWL Classes)
        class TrafficParticipant(Thing): pass
        class Vehicle(TrafficParticipant): pass
        class Tram(Vehicle): pass
        class EmergencyVehicle(Vehicle): pass
        
        class Infrastructure(Thing): pass
        class Road(Infrastructure): pass
        class PavedRoad(Road): pass
        class DirtRoad(Road): pass
        
        class TrafficSign(Thing): pass
        class PrioritySign(TrafficSign): pass # Priority road
        class YieldSign(TrafficSign): pass    # Yield / STOP (functionally equivalent here in terms of subordinance)
        class StopSign(TrafficSign): pass

    
        # --- Properties (Roles) ---
        # Object Properties connecting individuals
        class locatedOn(ObjectProperty):
            domain = [Vehicle]; range = [Road]
            
        class hasSign(ObjectProperty):
            domain = [Road]; range = [TrafficSign]
            
        class yieldsTo(ObjectProperty):
            domain = [Vehicle]; range = [Vehicle]
            # This property represents the conclusion of our reasoning
            
        class isRightOf(ObjectProperty):
            domain = [Vehicle]; range = [Vehicle]
            # Represents relative spatial positioning
        
        class relativeDirection(DataProperty):
            range = [str]
            

        # --- SWRL Rules (Logic Layer) ---
        # 1. Emergency Vehicle Rule
        # Emergency vehicles have priority over normal vehicles.
        rule_emergency = Imp()
        rule_emergency.set_as_rule("""
            Vehicle(?v1), EmergencyVehicle(?v2) -> yieldsTo(?v1, ?v2)
        """)

        # 2. Dirt Road Rule
        # A vehicle on a dirt road yields to a vehicle on a paved road.
        rule_dirtroad = Imp()
        rule_dirtroad.set_as_rule("""
            Vehicle(?v1), locatedOn(?v1, ?r1), DirtRoad(?r1),
            Vehicle(?v2), locatedOn(?v2, ?r2), PavedRoad(?r2)
            -> yieldsTo(?v1, ?v2)
        """)

        # 3.a. Sign Rule: STOP vs Priority Road
        # A vehicle with a STOP sign yields to a vehicle on a Priority road.
        rule_stop_vs_priority = Imp()
        rule_stop_vs_priority.set_as_rule("""
            Vehicle(?v1), locatedOn(?v1, ?r1), hasSign(?r1, ?s1), StopSign(?s1),
            Vehicle(?v2), locatedOn(?v2, ?r2), hasSign(?r2, ?s2), PrioritySign(?s2)
            -> yieldsTo(?v1, ?v2)
        """)

        # 3.b. Sign Rule: Yield vs Priority Road
        # A vehicle with a Yield sign yields to a vehicle on a Priority road.
        rule_yield_vs_priority = Imp()
        rule_yield_vs_priority.set_as_rule("""
            Vehicle(?v1), locatedOn(?v1, ?r1), hasSign(?r1, ?s1), YieldSign(?s1),
            Vehicle(?v2), locatedOn(?v2, ?r2), hasSign(?r2, ?s2), PrioritySign(?s2)
            -> yieldsTo(?v1, ?v2)
        """)
        
        # 3.c.1 Sign Rule: STOP vs None (Implicit Priority)
        # Assuming the other road is not a dirt road, a STOP sign implies yielding to a road with no sign (which is hierarchically higher in this context).
        rule_stop_vs_none = Imp()
        rule_stop_vs_none.set_as_rule("""
             Vehicle(?v1), locatedOn(?v1, ?r1), hasSign(?r1, ?s1), StopSign(?s1),
             Vehicle(?v2), locatedOn(?v2, ?r2)
             -> yieldsTo(?v1, ?v2)
        """)

        # 3.c.2 Sign Rule: Yield vs None
        rule_yield_vs_none = Imp()
        rule_yield_vs_none.set_as_rule("""
             Vehicle(?v1), locatedOn(?v1, ?r1), hasSign(?r1, ?s1), YieldSign(?s1),
             Vehicle(?v2), locatedOn(?v2, ?r2)
             -> yieldsTo(?v1, ?v2)
        """)

        # 4. Right-Hand Rule (Default Case)
        # If V2 is to the right of V1 on equal roads (paved), V1 yields.
        rule_righthand = Imp()
        rule_righthand.set_as_rule("""
            Vehicle(?v1), Vehicle(?v2), isRightOf(?v2, ?v1),
            locatedOn(?v1, ?r1), PavedRoad(?r1),
            locatedOn(?v2, ?r2), PavedRoad(?r2)
            -> yieldsTo(?v1, ?v2)
        """)

        # 5. Tram Rule
        # Trams have priority on equal roads.
        rule_tram = Imp()
        rule_tram.set_as_rule("""
            Vehicle(?v1), Tram(?v2), locatedOn(?v1, ?r1), locatedOn(?v2, ?r2),
            PavedRoad(?r1), PavedRoad(?r2)
            -> yieldsTo(?v1, ?v2)
        """)


        # --- ABox: Building the specific case (Assertion Box) ---
        # 1. Creating Road individuals
        road_a = PavedRoad("Road_A") if vehicle_a_data['road'] == 'paved' else DirtRoad("Road_A")
        road_b = PavedRoad("Road_B") if vehicle_b_data['road'] == 'paved' else DirtRoad("Road_B")

        # 2. Assigning Signs to Roads
        if vehicle_a_data['sign'] == 'stop': 
            road_a.hasSign.append(StopSign("Sign_A"))
        elif vehicle_a_data['sign'] == 'yield': 
            road_a.hasSign.append(YieldSign("Sign_A"))
        elif vehicle_a_data['sign'] == 'priority': 
            road_a.hasSign.append(PrioritySign("Sign_A"))

        if vehicle_b_data['sign'] == 'stop': 
            road_b.hasSign.append(StopSign("Sign_B"))
        elif vehicle_b_data['sign'] == 'yield': 
            road_b.hasSign.append(YieldSign("Sign_B"))
        elif vehicle_b_data['sign'] == 'priority': 
            road_b.hasSign.append(PrioritySign("Sign_B"))
            
        # 3. Creating Vehicle individuals
        if vehicle_a_data['type'] == 'emergency': v_a = EmergencyVehicle("Vehicle_A")
        elif vehicle_a_data['type'] == 'tram': v_a = Tram("Vehicle_A")
        else: v_a = Vehicle("Vehicle_A")
        
        v_a.locatedOn.append(road_a)

        if vehicle_b_data['type'] == 'emergency': v_b = EmergencyVehicle("Vehicle_B")
        elif vehicle_b_data['type'] == 'tram': v_b = Tram("Vehicle_B")
        else: v_b = Vehicle("Vehicle_B")
        
        v_b.locatedOn.append(road_b)
        
        # 4. Setting relative direction (Spatial relation)
        if vehicle_b_data['direction'] == 'right':
            v_b.isRightOf.append(v_a)


    # --- Inference (Reasoning) ---
    try:
        sync_reasoner(infer_property_values=True)
    except Exception as e:
        print(f"DEBUG: Reasoner error: {e}")


    # --- 2. DATA PREPARATION ---
    # Extracting raw data for Python-side logic handling
    sign_a = vehicle_a_data['sign']
    sign_b = vehicle_b_data['sign']
    type_a = vehicle_a_data['type']
    type_b = vehicle_b_data['type']
    road_a = vehicle_a_data['road']
    road_b = vehicle_b_data['road']
    dir_b = vehicle_b_data['direction']

    
    # --- 3. DECISION TREE (KRESZ Hierarchy Evaluation) ---
    # This section implements logic that is hard to express purely with basic SWRL 
    # 1. Emergency vehicle signal (Priority Level 1)
    if type_b == 'emergency' and type_a != 'emergency':
        return "⚠️ ELSŐBBSÉGET KELL ADNOD! (Megkülönböztető jelzést használó jármű)"
    if type_a == 'emergency' and type_b != 'emergency':
        return "✅ NEKED VAN ELSŐBBSÉGED! (Megkülönböztető jelzést használsz)"

    # 2. Sign-based decision (Checking SWRL inference results)
    # Exception: If both have STOP/Yield, they are equal in rank relative to each other!
    both_subordinate = (sign_a in ['stop', 'yield']) and (sign_b in ['stop', 'yield'])
    
    if v_b in v_a.yieldsTo and not both_subordinate:
        return "⚠️ ELSŐBBSÉGET KELL ADNOD! (Tábla szabályozás)"

    # 3. Dirt road rule (Priority Level 3)
    if road_a == 'dirt' and road_b == 'paved':
        return "⚠️ ELSŐBBSÉGET KELL ADNOD! (Földútról érkezel)"
    if road_b == 'dirt' and road_a == 'paved':
        return "✅ NEKED VAN ELSŐBBSÉGED! (A másik jármű földútról jön)"

    # 4. Equal-rank intersection logic (Priority Level 4)
    # Determining if the situation is "equal" (same road type, same/no signs)
    is_equal_situation = False
    if sign_a == 'none' and sign_b == 'none': is_equal_situation = True
    elif sign_a == 'priority' and sign_b == 'priority': is_equal_situation = True
    elif both_subordinate: is_equal_situation = True

    if is_equal_situation:
        # Tram rule (Special exception in equal situations)
        if type_b == 'tram' and type_a != 'tram':
            return "⚠️ ELSŐBBSÉGET KELL ADNOD! (A villamosnak egyenrangú helyzetben elsőbbsége van)"
        if type_a == 'tram' and type_b != 'tram':
            return "✅ NEKED VAN ELSŐBBSÉGED! (Villamosként elsőbbséged van)"

        # Right-hand rule (General rule for equal situations)
        if dir_b == 'right':
            return "⚠️ ELSŐBBSÉGET KELL ADNOD! (Jobbkéz-szabály)"
        if dir_b == 'left':
             return "✅ NEKED VAN ELSŐBBSÉGED! (A másik jármű balról jön)"
        if dir_b == 'opposite':
            return "⚠️/✅ Egyenesen haladva elsőbbséged van, balra kanyarodva nem."

    return "✅ NEKED VAN ELSŐBBSÉGED (vagy a másik járműnek táblája van)."