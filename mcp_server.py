from mcp.server.fastmcp import FastMCP
import sqlite3
import pandas as pd

# 1. Initialize the FastMCP Server
mcp = FastMCP("AuraData_FinOps_Server")

# 2. Setup a dummy enterprise database for our Capstone demo
def setup_database():
    conn = sqlite3.connect("enterprise_data.db", check_same_thread=False)
    cursor = conn.cursor()
    # Create a table for Cloud Infrastructure Costs
    cursor.execute('''CREATE TABLE IF NOT EXISTS cloud_costs
                      (service TEXT, cost REAL, department TEXT)''')
    
    # Insert mock data if the table is empty
    cursor.execute("SELECT count(*) FROM cloud_costs")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ("AWS EC2", 45000.50, "Engineering"),
            ("Google Cloud SQL", 12000.75, "Data Team"),
            ("Azure Blob Storage", 8500.00, "Marketing"),
            ("Google BigQuery", 32000.00, "Data Team"),
            ("AWS Lambda", 4100.25, "Engineering")
        ]
        cursor.executemany("INSERT INTO cloud_costs VALUES (?, ?, ?)", mock_data)
        conn.commit()
    return conn

db_conn = setup_database()

# 3. Create the MCP Tool (This is the "Skill" the Agent will use)
@mcp.tool()
def query_financial_database(query: str) -> str:
    """
    Executes a SQL query on the enterprise financial database.
    Use this tool to analyze cloud costs and department budgets.
    """
    # ENTERPRISE SECURITY GUARDRAIL: Read-Only execution
    if any(keyword in query.upper() for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]):
        return "SECURITY ALERT: Write operations are strictly blocked by Policy Server. Only SELECT queries allowed."
    
    try:
        # Run the query and return the data as a string
        df = pd.read_sql_query(query, db_conn)
        return df.to_string()
    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == "__main__":
    print("Starting AuraData FinOps MCP Server on stdio...")
    # Run the server using standard input/output
    mcp.run(transport='stdio')