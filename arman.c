#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <errno.h> // Include for better error reporting


#define MAX_PACKET_SIZE 1024

typedef struct {
    char *ip_address;
    int port;
    int interval_ms;
    int num_packets;
    int thread_id;
} thread_params;

void *send_packet(void *params) {
    thread_params *thread_data = (thread_params *)params;
    int sock;
    struct sockaddr_in server_addr;
    const char *packet_data = "@MoinOwner";
    int packet_size = strlen(packet_data);
    int sent_packets = 0;
    struct timespec sleep_time;


    // Create a UDP socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        fprintf(stderr, "Thread %d: Socket creation failed: %s\n", thread_data->thread_id, strerror(errno));
        return NULL;
    }

    // Configure the server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(thread_data->port);

    // Convert the IP address string to a binary address
    if (inet_pton(AF_INET, thread_data->ip_address, &server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Thread %d: Invalid address/ Address not supported: %s\n", thread_data->thread_id, thread_data->ip_address);
        close(sock);
        return NULL;
    }

    // Set sleep time for interval
    sleep_time.tv_sec = thread_data->interval_ms / 1000;
    sleep_time.tv_nsec = (thread_data->interval_ms % 1000) * 1000000;


    // Send packets repeatedly
    while (sent_packets < thread_data->num_packets) {
        if (sendto(sock, packet_data, packet_size, 0, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            fprintf(stderr, "Thread %d: Error sending packet: %s\n", thread_data->thread_id, strerror(errno));
            break; //Exit the loop if there is an error sending
        }
        sent_packets++;
        printf("Thread %d: Sent packet %d\n", thread_data->thread_id, sent_packets);
        nanosleep(&sleep_time, NULL);
    }

    close(sock);
    return NULL;
}


int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s <ip_address> <port> <interval_ms> <num_packets>\n", argv[0]);
        return 1;
    }

    pthread_t thread;
    thread_params params;
    params.ip_address = argv[1];
    params.port = atoi(argv[2]);
    params.interval_ms = atoi(argv[3]);
    params.num_packets = atoi(argv[4]);
    params.thread_id = 1;

    if (pthread_create(&thread, NULL, send_packet, &params) != 0) {
        perror("Thread creation failed");
        return 1;
    }

    pthread_join(thread, NULL);
    printf("All packets sent\n");
    return 0;
}