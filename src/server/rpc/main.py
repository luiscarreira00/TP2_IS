import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.teste import selectPlayer, selectPlayersFromOverall, listaNacionalidade, countPlayersFromOverall, countPlayersFromNationality, selectPlayersBetweenOverall, selectPlayersBetweenOverallAndAge


PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register both functions
        server.register_function(selectPlayer(player,server.register_function(listaNacionalidade))) # player - string do nome de um jogador
        server.register_function(selectPlayersFromOverall(overall)) # overall - inteiro do overall de um jogador

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
