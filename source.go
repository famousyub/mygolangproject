package main 
import (
	"fmt"
	
	)


type G struct  {
	me string  
	you string 
}

func setName(s string) string {
     g   := &G{me:"ayoub",you :"ch"}

	 fmt.Println(g.me)
	 fmt.Println(g.you)
     res := fmt.Sprintf("%s %s" , g.me,g.you)
	 return  res 

}

func main(){
	 fmt.Println("hello  wotlf")
     _test()
	 setName("ayoubo")
}