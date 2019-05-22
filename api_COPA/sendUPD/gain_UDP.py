import SocketServer, threading, time
import requests, json, csv, os

tx = 0
rx = 0


fieldnames = ['tx_gain', 'rx_gain', 'cell_id', 'snr', 'brate']
csv_file = open('results.csv', 'w+', buffering=0)
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

# exists = os.path.isfile('results.csv')
# fieldnames = ['tx_gain', 'rx_gain', 'cell_id', 'snr']
# if exists:
#     csv_file = open('results.csv', 'a+', buffering=0)
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
# else:
#     csv_file = open('results.csv', 'w+', buffering=0)
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        json_data = json.loads(data)
        save_data = {'tx_gain': tx, 'rx_gain': rx, 'cell_id': json_data["id"], 'snr': json_data["snr"], 'brate': json_data["brate"]}

        print("{},{},{},{},{}".format(save_data["tx_gain"], save_data["rx_gain"],save_data["cell_id"],save_data["snr"],save_data["brate"]))
        writer.writerow(save_data)

        # print("{},{},{},{}".format(tx, rx,json_data["id"],json_data["snr"],json_data["brate"]))
        # writer.writerow({'tx_gain': tx, 'rx_gain': rx, 'cell_id': json_data["id"], 'snr': json_data["snr"], 'brate': json_data["brate"]})
        #print "%d, %d, %f" % (tx, rx,json.data["snr"])
        # socket = self.request[1]
        # current_thread = threading.current_thread()
        # print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        # print tx, rx
        # socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5005

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True:
            for tx in range(90,30,-2):
                for rx in range(76,10,-2):
                    print "\nTx = %d\nRx = %d\n" % (tx,rx)
                    requests.get("http://143.54.12.244:9080/gain/%d/%d" % (tx,rx))
                    time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()