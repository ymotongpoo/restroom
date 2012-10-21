package main

import (
	"testing"
)

func TestAdd(t *testing.T) {
	const n, m = 2, 3
	const out = 5
	if x := Add(n, m); x != out {
		t.Errorf("Add(%v, %v) = %v, want %v", n, m, x, out)
	}
}