#include <iostream>
#include <assert.h>
#include <sys/errno.h>
#include <string>
#include <cstring>

#include <sys/socket.h> 
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <ifaddrs.h> // getIP

#define PORT 9048

using namespace std;

// sockaddr is a pre-defined struct {sa_family, sa_data}
// PF_INET = Protocol family 
// AF_INET = Address family  
// SOCK_STREAM = TCP socket 
// SOCK_DGRAM  = UDP socket
// htons = from unsigned host short byte order to network byte order
// htonl = from unsigned host long byte order to network byte order
// INADDR_ANY = is to connect to all interfaces (network cards)


// pre-defined in <netinet/in.h>
// struct in_addr {
//    unsigned long s_addr;    // IP address
// };

// pre-defined in <netinet/in.h>
// struct sockaddr_in {    // socket address internet
//    short int            sin_family;     // internet protocol family
//    in_addr              sin_addr;       // internet address 
//    unsigned short int   sin_port;       // internet address port
//    unsigned char        sin_zero[8];
// };

sockaddr getIP(){
    struct ifaddrs *id;
    int val;
    val = getifaddrs(&id);
    printf("Network Interface Name :- %s\n",id->ifa_name);
    printf("Network Address of %s :- %u\n",id->ifa_name,id->ifa_addr);
    return *(id->ifa_addr);
}

void server(){

    // get interface ip
    //sockaddr IP = getIP();
    //sockaddr_in *inIP = (struct sockaddr_in *)&IP;


    // set address and port
    sockaddr_in addrport;
    socklen_t addrlen = (socklen_t) sizeof(addrport);
    addrport.sin_family = AF_INET;
    addrport.sin_port = htons(PORT);
    addrport.sin_addr.s_addr = htonl(INADDR_ANY);
    //addrport.sin_addr.s_addr = inet_addr(IP);
    //addrport.sin_addr = inIP->sin_addr;
    sockaddr* sa = (sockaddr*) &addrport;

    cout << "IP:   " << inet_ntoa(addrport.sin_addr) << endl;
    cout << "Port: " << ntohs(addrport.sin_port) << endl;

    // set socket
    int sockid = socket(PF_INET, SOCK_STREAM, 0); // set socket
    if (sockid == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }

    // bind socket to address port
    int bind_status = bind(sockid, sa, sizeof(addrport)); 
    if (bind_status == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }

    // set listening for a connection
    int listen_status = listen(sockid, 3);
    if (listen_status == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }


    // listen and accept a connection
    cout << "Listening..." << endl;
    int new_socket = accept(sockid, sa, &addrlen);
    if (new_socket == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }
    cout << "Connected!" << endl;

    // send a msg
    string msg;
    cout << "Message to send: " << endl;
    cin.ignore();
    getline(cin, msg);
    int send_status = send(new_socket, &msg, msg.length()+1, 0);
    if (send_status == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }


}

void client(){

    // set address and port
    sockaddr_in addrport;
    socklen_t addrlen = (socklen_t) sizeof(addrport);
    addrport.sin_family = AF_INET;
    addrport.sin_port = htons(PORT);
    addrport.sin_addr.s_addr = htonl(INADDR_ANY);
    sockaddr* sa = (sockaddr*) &addrport;

    // set socket
    int sockid = socket(PF_INET, SOCK_STREAM, 0); // set socket
    if (sockid == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }

    // connect to server
    int conn_status = connect(sockid, sa, addrlen);
    if (conn_status == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }

    cout << "Connected!" << endl;
    cout << "Waiting for a message..." << endl;

    // receive msg 
    string msg;
    int recv_status = recv(sockid, &msg, 1024, 0);
    if (recv_status == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }

    cout << msg << endl;
        

}

int main(){

    int op = 0;
    while (op != 1 and op != 2){
        cout << "Select:";
        cout << "    1-Server: to wait for a connection" << endl;
        cout << "\t   2-Client: to connect to a server" << endl;
        cout << "Option: ";
        cin >> op; 
    }

    if (op == 1)
        server();
    else
        client();


    return 0;
}
