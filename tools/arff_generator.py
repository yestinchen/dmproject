import names
import analysis

if __name__ == '__main__':
    range_map = analysis.value_ranges("../data/kddcup.data_10_percent_corrected")
    with open("../data/kddcup.data_10_percent_corrected.arff", "w") as out_f:
        out_f.write("@relation kddcup\n")
        for name in names.name_list:
            if names.att_type_map.get(name) == "continuous":
                out_f.write("@attribute {0} numeric\n".format(name))
            else:
                out_f.write("@attribute {0} ".format(name))
                out_f.write("{")
                for index, value in enumerate(range_map.get(name)):
                    if index == (len(range_map.get(name)) - 1):
                        out_f.write("{0}".format(value))
                        out_f.write("}\n")
                    else:
                        out_f.write("{0},".format(value))
        # done.
        out_f.write("@attribute class {back,buffer_overflow,ftp_write,guess_passwd,imap,ipsweep,land,loadmodule,multihop,neptune,nmap,normal,perl,phf,pod,portsweep,rootkit,satan,smurf,spy,teardrop,warezclient,warezmaster}")
        out_f.write("\n")
        out_f.write("\n")
        out_f.write("\n")
        out_f.write("@data\n")
        with open("../data/kddcup.data_10_percent_corrected") as read_f:
            for line in read_f.readlines():
                out_f.write(line.replace(".", ""))

