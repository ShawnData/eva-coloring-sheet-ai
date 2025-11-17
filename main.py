from mcp_server.server import mcp

def main():
    mcp.run(transport="sse", host="localhost", port=3000)


if __name__ == "__main__":
    main()
