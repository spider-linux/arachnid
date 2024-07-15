package main

import (
	// "fmt"
	"log"
	"os"

	"github.com/Shopify/go-lua"
	"github.com/spf13/cobra"
)

var (
    L = lua.NewState()

    rootCmd = &cobra.Command{
        Use: "arachnid",
        Short: "package/system manager for Spider Linux",
    }
    cmdRun = &cobra.Command{
        Use: "run",
        Short: "Run script",
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
    if L.IsTable(1) {
        dirsToCreate := make([]string, 0)
        tablePos := 1
        tableLength := L.RawLength(1) + 1

        for i := 1; i <= tableLength; i++ {
            // Pushes table value (type independant) to stack
            L.RawGetInt(1, i)
        }

        for i := tablePos + 1; i <= tableLength; i++ {
            s, ok := L.ToString(i)
            if !ok {
                log.Fatalln("error: not string or number")
            }
            dirsToCreate = append(dirsToCreate, s)
        }

        for _, d := range dirsToCreate {
            os.Mkdir(d, 0755)
        }
    }
    return 0
}

func init(){
    lua.BaseOpen(L)
    L.Register("create_root_structure", createDirStructure)

    rootCmd.AddCommand(cmdRun)
}

func main(){
    rootCmd.Execute()
}
