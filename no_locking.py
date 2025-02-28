import hazelcast
import concurrent.futures
import time

def execute_client():
    client = hazelcast.HazelcastClient()

    map = client.get_map("my-distributed-map15").blocking()

    map.put_if_absent("key", 0)

    for _ in range(10000):
        value = map.get("key")
        value += 1
        map.put("key", value)

    client.shutdown()

if __name__ == "__main__":
    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(execute_client) for _ in range(3)]

        for future in futures:
            future.result()

    end_time = time.time()

    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map15").blocking()        
    client.shutdown()

    print(f"Final value: {map.get("key")}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
