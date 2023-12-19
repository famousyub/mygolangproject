package main 

import (
	"net"
	"fmt"
	"bufio"
)

func _test(){


	ln , _ :=net.Listen("tcp",":4000")
	conn,_ :=ln.Accept()

	for  {
		 message , _ := bufio.NewReader(conn).ReadString('\n')
		 fmt.Print("Message recieved" , string(message))
	}

}