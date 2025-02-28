import hazelcast
import concurrent.futures
import time

def execute_client():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map11").blocking()
    map.put_if_absent("key", 0)

    for _ in range(10000):
        map.lock("key")
        value = map.get("key")
        value += 1
        map.put("key", value)
        map.unlock("key")

if __name__ == "__main__":
    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(execute_client) for _ in range(3)]

        for future in futures:
            future.result()

    
    end_time = time.time()

    client = hazelcast.HazelcastClient()
    client.shutdown()

    map = client.get_map("my-distributed-map11").blocking()
    print(f"Final value: {map.get("key")}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
