import uuid
import json  # or import yaml if you prefer YAML
import os
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# ------------------------------------------------------------------
# MODEL DEFINITIONS
# ------------------------------------------------------------------

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)         # e.g. "Torflat"
    row_label = Column(String)    # e.g. "A", "B", etc.
    column_label = Column(String) # e.g. "1", "2", etc.

    # Relationship back to Part
    parts = relationship("Part", back_populates="location")

class Part(Base):
    __tablename__ = 'parts'
    id = Column(Integer, primary_key=True)
    guid = Column(String, unique=True, index=True)
    part_number = Column(String)
    description = Column(String)
    category = Column(String)

    # The foreign key referencing the 'locations' table
    location_id = Column(Integer, ForeignKey("locations.id"))
    # Relationship to Location
    location = relationship("Location", back_populates="parts")

# ------------------------------------------------------------------
# DATABASE & INITIALIZATION
# ------------------------------------------------------------------

def init_db():
    """
    Creates an engine, a session factory, and sets up the tables if needed.
    Uses psycopg2 behind the scenes (indicated by 'postgresql+psycopg2').
    """
    db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/testdb"
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def load_locations_from_json(session, filename="locations.json"):
    """
    Reads a JSON file describing location sets, e.g.:
    {
      "locations": [
        {
          "name": "Torflat",
          "rows": ["A","B","C"],
          "columns": [1,2,3]
        }
      ]
    }
    For each row/column combination, we create a distinct record in 'locations' if not present.
    """
    if not os.path.exists(filename):
        print(f"No {filename} file found. Skipping location import.")
        return
    
    with open(filename, "r") as f:
        data = json.load(f)
    
    # 'locations' should be a list of dictionaries
    for loc_def in data.get("locations", []):
        name = loc_def["name"]
        rows = loc_def["rows"]
        columns = loc_def["columns"]
        # For each row and column, create a location record if not exist
        for r in rows:
            for c in columns:
                existing = session.query(Location).filter_by(
                    name=name, row_label=str(r), column_label=str(c)
                ).first()
                if not existing:
                    new_loc = Location(
                        name=name,
                        row_label=str(r),
                        column_label=str(c),
                    )
                    session.add(new_loc)
    session.commit()

# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------

def format_part_number(num_str):
    """
    Zero-pads an integer up to 6 digits, then inserts a space to produce '000 123', etc.
    If it's not numeric, returns as-is.
    """
    try:
        num_int = int(num_str)
        # Zero-pad to 6 digits
        padded = f"{num_int:06d}"  # e.g. '000123'
        return padded[:3] + " " + padded[3:]  # '000 123'
    except ValueError:
        # If not numeric, just return original
        return num_str

# ------------------------------------------------------------------
# MENU OPERATIONS
# ------------------------------------------------------------------

def search_part(session):
    """
    Search for parts. Return the selected part or None if nothing chosen.
    We do a sub-menu once we find matching parts, so the user can pick a part
    and do subsequent actions on it.
    """
    term = input("Search term (part # or description): ").strip()
    if not term:
        print("No search term entered.")
        return None
    
    parts = session.query(Part).filter(
        (Part.part_number.ilike(f"%{term}%")) | (Part.description.ilike(f"%{term}%"))
    ).all()
    
    if not parts:
        print("No matching parts found.")
        return None
    
    print("\nSearch Results:")
    for idx, p in enumerate(parts, start=1):
        loc = p.location
        loc_str = f"{loc.name} (Row {loc.row_label}, Col {loc.column_label})" if loc else "None"
        print(f"{idx}) GUID={p.guid}  PartNum={p.part_number}  Desc={p.description}  Location={loc_str}")
    
    # Let user pick from the list
    choice_str = input("\nSelect a part # (or 'c' to cancel): ").strip()
    if choice_str.lower() == 'c':
        return None
    
    try:
        choice_idx = int(choice_str)
        if 1 <= choice_idx <= len(parts):
            return parts[choice_idx - 1]
    except ValueError:
        pass
    
    print("Invalid choice.")
    return None

def handle_selected_part(session, part):
    """
    Once a user has selected a part, show a sub-menu for update, duplicate, delete,
    assign location, or return to main menu.
    """
    while True:
        print(f"\nPart selected: GUID={part.guid}, Number={part.part_number}, Desc={part.description}")
        print("  U) Update")
        print("  D) Duplicate")
        print("  E) Delete")
        print("  L) Assign Location")
        print("  M) Main menu")
        choice = input("Enter choice: ").strip().lower()

        if choice == 'u':
            update_part(session, part)
        elif choice == 'd':
            duplicate_part(session, part)
        elif choice == 'e':
            delete_part(session, part)
            return  # once deleted, no need to keep sub-menu
        elif choice == 'l':
            assign_location(session, part)
        elif choice == 'm':
            break
        else:
            print("Invalid option. Try again.")

def create_new_part(session):
    """
    Create a new Part record from user input.
    """
    part_guid = str(uuid.uuid4())
    pn = input("Enter part number: ")
    desc = input("Enter part description: ")
    cat = input("Enter part category: ")
    
    part_number_formatted = format_part_number(pn)
    
    new_part = Part(
        guid=part_guid,
        part_number=part_number_formatted,
        description=desc,
        category=cat
    )
    session.add(new_part)
    session.commit()
    print(f"Created new Part with GUID={new_part.guid}")

def update_part(session, part):
    """
    Prompt user for new description/category/part_number, then update.
    """
    new_desc = input(f"New description (leave blank to keep '{part.description}'): ")
    if new_desc.strip():
        part.description = new_desc.strip()
    
    new_cat = input(f"New category (leave blank to keep '{part.category}'): ")
    if new_cat.strip():
        part.category = new_cat.strip()
    
    new_pn = input(f"New part number (leave blank to keep '{part.part_number}'): ")
    if new_pn.strip():
        part.part_number = format_part_number(new_pn.strip())
    
    session.commit()
    print("Part updated.")

def duplicate_part(session, part):
    """
    Create a new Part with a fresh GUID, copying the existing part’s data (except the primary key).
    """
    new_guid = str(uuid.uuid4())
    dup_part = Part(
        guid=new_guid,
        part_number=part.part_number,
        description=part.description,
        category=part.category,
        location_id=part.location_id
    )
    session.add(dup_part)
    session.commit()
    print(f"Part duplicated. New GUID={dup_part.guid}")

def delete_part(session, part):
    """
    Delete the given Part.
    """
    session.delete(part)
    session.commit()
    print("Part deleted.")

def assign_location(session, part):
    """
    Assign or change the part’s location by letting user pick from the available locations.
    """
    locations = session.query(Location).all()
    if not locations:
        print("No locations found in the database.")
        return
    print("\nAvailable Locations:")
    for idx, loc in enumerate(locations, start=1):
        print(f"{idx}) {loc.name}, Row={loc.row_label}, Col={loc.column_label}, ID={loc.id}")
    
    pick_str = input("Select location by #, or 'c' to cancel: ").strip()
    if pick_str.lower() == 'c':
        return

    try:
        pick_idx = int(pick_str)
        if 1 <= pick_idx <= len(locations):
            chosen_loc = locations[pick_idx - 1]
            part.location_id = chosen_loc.id
            session.commit()
            print(f"Assigned Part {part.guid} to location ID={chosen_loc.id} ({chosen_loc.name}, R{chosen_loc.row_label}, C{chosen_loc.column_label}).")
        else:
            print("Invalid location index.")
    except ValueError:
        print("Invalid input.")

# ------------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------------

def main_menu():
    session = init_db()
    load_locations_from_json(session, filename="locations.json")  # or "locations.yaml" if you want YAML
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1) Search for a part (and then update, duplicate, delete, assign location)")
        print("2) Create a new part")
        print("Q) Quit")
        
        choice = input("Enter choice: ").strip().lower()
        
        if choice == '1':
            part = search_part(session)
            if part:
                handle_selected_part(session, part)
        elif choice == '2':
            create_new_part(session)
        elif choice == 'q':
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
