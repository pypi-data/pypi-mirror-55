major_version = 13
minor_version = 0
micro_version = 0
patch_version = "b1"
post_version = ""
version = "%i.%i.%i" % (major_version, minor_version, micro_version)
main_version = "%i.%i.0" % (major_version, minor_version)
                          
if patch_version != "":
    version += "%s" % patch_version
if post_version != "":
    version += "%s" % post_version

def main():
    print(("%s" % version))

if __name__ == "__main__":
    main()
