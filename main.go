package main

import (
	"fmt"
	"log"

	"github.com/Shopify/go-lua"
	"github.com/spf13/cobra"
)

var (
    L = lua.NewState()

    rootCmd = &cobra.Command{
        Use: "arachnid",
        Short: "package/system manager for Spider Linux",
    }
    cmdBootstrap = &cobra.Command{
        Use: "bootstrap",
        Short: "Bootstrap the system",
        Args: cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            // TODO: add check to see if argument is actually a file before running DoFile.
            err := lua.DoFile(L, args[0])
            if err != nil {
                log.Fatalf("error: %s\n", err)
            }
        },
    }
)

func createDirStructure(L *lua.State) int {
    fmt.Println("creating dir structure in ./")
    return 0
}

func init(){
    lua.BaseOpen(L)
    L.Register("create_dir_structure", createDirStructure)

    rootCmd.AddCommand(cmdBootstrap)
}

func main(){
    rootCmd.Execute()
}
