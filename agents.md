### `agents.md` – Parts Locator Project

#### Overview
This document defines the agents used in the `parts-locator` app. Each agent performs a focused task in the system, including search, part management, location handling, and data enrichment. These agents can be invoked by name and composed into workflows.

---

#### Agent: `search_agent`

**Purpose:**  
Performs full-text and filtered search over parts inventory.

**Inputs:**  
- `query`: A string (e.g. "bolt", "resistor", "3mm stainless")
- `limit` (optional): Max number of results to return

**Outputs:**  
- List of matching part objects (`id`, `description`, `location`, `created`)

**Notes:**  
- Uses case-insensitive partial match (`ILIKE`) on description, location, or other relevant fields.
- Defaults to 50 results if no `limit` is given.

---

#### Agent: `add_part_agent`

**Purpose:**  
Adds a new part to the inventory.

**Inputs:**  
- `description`: Text describing the part
- `location`: Location identifier (string)
- `mcmaster_id` (optional): External catalog reference

**Outputs:**  
- `success`: `true` or `false`
- `id`: Newly created part ID (if successful)

**Constraints:**  
- `description` is required
- `location` is required

---

#### Agent: `delete_parts_agent`

**Purpose:**  
Soft-deletes a list of parts from the inventory.

**Inputs:**  
- `ids`: Array of part IDs to delete

**Outputs:**  
- `success`: `true` if all deletions succeed
- `not_found`: List of any IDs not found

**Notes:**  
- Parts are not permanently deleted; marked with a `deleted_at` timestamp.

---

#### Agent: `view_deleted_agent`

**Purpose:**  
Returns a list of parts that were soft-deleted.

**Inputs:**  
- `limit` (optional): Max number of results

**Outputs:**  
- List of deleted part records, sorted by deletion time

---

#### Agent: `undelete_agent`

**Purpose:**  
Restores a soft-deleted part to the active inventory.

**Inputs:**  
- `id`: Part ID

**Outputs:**  
- `success`: `true` if restore succeeded

---

#### Agent: `location_info_agent`

**Purpose:**  
Returns detailed info about a location/module.

**Inputs:**  
- `module_id` or `module_name`

**Outputs:**  
- Module metadata: description, layers, bins, coordinates, sub-location flags

---

#### Agent: `assign_location_agent`

**Purpose:**  
Assigns or moves a part to a specific location.

**Inputs:**  
- `part_id`
- `location_string` or structured `{module, level, row, column}`

**Outputs:**  
- `success`: `true` or `false`

**Notes:**  
- May overwrite previous location assignment.

---

### Naming and Execution
Agents can be accessed as functions in the application’s logic. For instance:

```python
search_agent(query="screw", limit=10)
```

Or used in workflows, e.g.:

1. `search_agent` → list parts
2. `select_part_id` → `delete_parts_agent(ids=[id])`
