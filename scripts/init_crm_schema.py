"""
Initialize CRM Database Schema
==============================
Run this script to create CRM tables in the database.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_schema():
    """Run the CRM schema."""
    print("=" * 60)
    print("LABBAIK AI - CRM Schema Initializer")
    print("=" * 60)

    # Try to get database connection
    try:
        from services.database.repository import get_db
        db = get_db()

        if not db:
            print("ERROR: Database connection not available")
            print("Please set DATABASE_URL in environment or .streamlit/secrets.toml")
            return False

        print("Database connected successfully!")

    except ImportError as e:
        print(f"ERROR: Could not import database module: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        return False

    # Read schema file
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "sql",
        "travel_crm_schema.sql"
    )

    if not os.path.exists(schema_path):
        print(f"ERROR: Schema file not found: {schema_path}")
        return False

    print(f"Reading schema from: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Split into individual statements
    statements = []
    current_stmt = []
    in_function = False

    for line in schema_sql.split("\n"):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("--"):
            continue

        # Track function/trigger blocks
        if "CREATE OR REPLACE FUNCTION" in line.upper() or "CREATE FUNCTION" in line.upper():
            in_function = True

        current_stmt.append(line)

        # End of statement
        if stripped.endswith(";") and not in_function:
            statements.append("\n".join(current_stmt))
            current_stmt = []
        elif in_function and stripped == "$$ LANGUAGE plpgsql;":
            statements.append("\n".join(current_stmt))
            current_stmt = []
            in_function = False

    # Add any remaining statement
    if current_stmt:
        statements.append("\n".join(current_stmt))

    print(f"Found {len(statements)} SQL statements to execute")
    print("-" * 60)

    # Execute each statement
    success_count = 0
    error_count = 0

    for i, stmt in enumerate(statements, 1):
        stmt = stmt.strip()
        if not stmt:
            continue

        # Get first line for display
        first_line = stmt.split("\n")[0][:60]

        try:
            db.execute(stmt)
            print(f"[{i}] OK: {first_line}...")
            success_count += 1
        except Exception as e:
            error_msg = str(e)
            # Ignore "already exists" errors
            if "already exists" in error_msg.lower():
                print(f"[{i}] SKIP (exists): {first_line}...")
                success_count += 1
            else:
                print(f"[{i}] ERROR: {first_line}...")
                print(f"    {error_msg[:100]}")
                error_count += 1

    print("-" * 60)
    print(f"Completed: {success_count} success, {error_count} errors")

    if error_count == 0:
        print("Schema initialized successfully!")
        return True
    else:
        print("Schema initialized with some errors (check above)")
        return False


if __name__ == "__main__":
    success = run_schema()
    sys.exit(0 if success else 1)
