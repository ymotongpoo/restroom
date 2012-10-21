/*
 Sample code for checking unit test feature on Go
*/

package main

import (
	"fmt"
)

func main() {
	fmt.Println("2 + 3 = %v", Add(2, 3))
}

func Add(n int, m int) int {
	return n + m
}