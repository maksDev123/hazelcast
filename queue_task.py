import hazelcast
import threading
import time

def writer(queue):
    for i in range(1, 101):
        queue.offer(i)
        time.sleep(0.1)

def reader(queue, reader_id):
    while True:
        value = queue.poll()
        if value is not None:
            print(f"User {reader_id}. Reading {value}")
        time.sleep(0.05)

def main():
    client = hazelcast.HazelcastClient()
    start_time = time.time()
    queue = client.get_queue("my-distributed-queue").blocking()

    writer_thread = threading.Thread(target=writer, args=(queue,))
    writer_thread.start()

    reader_thread_1 = threading.Thread(target=reader, args=(queue, 1))
    reader_thread_2 = threading.Thread(target=reader, args=(queue, 2))

    reader_thread_1.start()
    reader_thread_2.start()

    writer_thread.join()

    print(f"Time taken {time.time() - start_time}")

    client.shutdown()

if __name__ == "__main__":
    main()
