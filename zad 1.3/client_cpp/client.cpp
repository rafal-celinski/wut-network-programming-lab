#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>    
#include <sys/socket.h>   
#include <netinet/in.h>   
#include <netinet/tcp.h>

#define SERVER_IP "172.21.36.2"
#define SERVER_PORT 8080
#define MAX_MESSAGE_SIZE 200000

long long get_current_time_in_ms() {
    struct timeval time;
    gettimeofday(&time, NULL);
    return time.tv_sec * 1000LL + time.tv_usec / 1000;
}

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cout << "Failed to create socket" << std::endl;
        return -1;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    if(connect(sock, (struct sockaddr*)& server_addr, sizeof(server_addr)) < 0) {
        std::cout << "Failed to connect" << std::endl;
        return -1;
    }

    // Wyłączanie algorytmu Nagle'a - nwm czy potrzebne, wyniki jakoś się nie różnią dla tych małych pakietów
    // int flag = 1;
    // if (setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, (char*)&flag, sizeof(int)) < 0) {
    //     std::cerr << "Failed to disable Nagle's Algorithm" << std::endl;
    //     return -1;
    // }

    std::cout << "Connected to server" << std::endl;

    int message_size = 200;
    
    while(message_size <= MAX_MESSAGE_SIZE)
    {
        char* message = new char[message_size];
        memset(message, 'M', message_size);
        for (int i = 0; i < 100; i++)
        {
            long long start_time = get_current_time_in_ms();
            int bytes_send = send(sock, message, message_size, 0);
            if (bytes_send < 0) {
                std::cout << "Couldn't send message" << std::endl;
                close(sock);
                delete[] message;
                return -1;
            }

            long long end_time = get_current_time_in_ms();
            long long difference = end_time - start_time;
            std::cout << "Message " << i << " of size " << message_size << " B sent in " << difference << " ms" << std::endl;
        }
        delete[] message;
        message_size *= 10;
    }
    std::cout << "Sent all messages" << std::endl;
    close(sock);
    return 0;
}