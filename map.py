import hazelcast

client = hazelcast.HazelcastClient()
my_map = client.get_map("my-distributed-map1").blocking()

for i in range(1000):
    my_map.put(i, "value")

client.shutdown()