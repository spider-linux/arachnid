package main

import (
    "github.com/Shopify/go-lua"
)

func main(){
    l := lua.NewState()
    lua.BaseOpen(l)
    lua.DoFile(l, "test.lua")
}
