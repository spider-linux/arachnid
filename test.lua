local meta = {
    name = "test",
    version = "v0.0.0",
}

-- Just some for examples
local dirs_to_make = {
    "spiderroot",
    "spiderroot/bin",
    "spiderroot/etc",
    "spiderroot/boot",
    "spiderroot/dev",
    "spiderroot/sys",
    "spiderroot/lib",
    "spiderroot/run",
    "spiderroot/root",
    "spiderroot/tmp",
    "spiderroot/usr",
}

create_root_structure(dirs_to_make)
