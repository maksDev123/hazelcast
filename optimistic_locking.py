import hazelcast
import concurrent.futures
import time


def execute_client():
    client = hazelcast.HazelcastClient()

    map = client.get_map("my-distributed-map031").blocking()
    map.put_if_absent("key", 0)

    for _ in range(10000):
        success = False
        while not success:
            value = map.get("key")
            new_value = value + 1
            
            success = map.replace_if_same("key", value, new_value)
            
            if not success:
                time.sleep(0.01)

    client.shutdown()

if __name__ == "__main__":
    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(execute_client) for _ in range(3)]

        for future in futures:
            future.result()

    end_time = time.time()

    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map031").blocking()
    final_value = map.get("key")
    client.shutdown()

    print(f"Final value: {final_value}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
