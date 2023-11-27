def write_to_file(filename, content):
    file=open(filename,"w")
    file.write(content)
    file.close()