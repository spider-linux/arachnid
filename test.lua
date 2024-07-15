local meta = {
    name = "test",
    version = "v0.0.0",
}

-- Just some for examples
local dirs_to_make = {
    "spiderroot",
    "spiderroot/etc",
    "spiderroot/var",
    "spiderroot/lib64",
    "spiderroot/usr",
    "spiderroot/usr/bin",
    "spiderroot/usr/lib",
    "spiderroot/usr/sbin",

    -- "spiderroot/dev",
    -- "spiderroot/sys",
    -- "spiderroot/lib",
    -- "spiderroot/run",
    -- "spiderroot/root",
    -- "spiderroot/tmp",
}

create_root_structure(dirs_to_make)
