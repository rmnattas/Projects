#include <iostream>
#include <assert.h>
#include <sys/errno.h>

#include <sys/socket.h> 
#include <netinet/in.h> 

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

void server(){
    int sockid = socket(PF_INET, SOCK_STREAM, 0); // set socket
    if (sockid == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }

    sockaddr_in addrport;
    addrport.sin_family = AF_INET;
    addrport.sin_port = htons(631);
    addrport.sin_addr.s_addr = htonl(INADDR_ANY);
    sockaddr* sa = (sockaddr*) &addrport;
    int status = bind(sockid, sa, sizeof(addrport)); // bind socket to address port
    if (status == -1){
        cout << strerror(errno) << endl;
        assert(false);
    }
}

void client(){

}

int main(){
    
    server();

    return 0;
}

