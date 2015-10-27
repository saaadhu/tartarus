import sys
import re

disassembly = open(sys.argv[1])
relocs = open(sys.argv[2])
syms = open(sys.argv[3])

relocmap = {}

lines = relocs.readlines()
for line in lines:
    line = line.strip()

    reloc_section_match = re.search(r'RELOCATION RECORDS FOR \[([^\]]+)\]:', line)
    if reloc_section_match:
        current_reloc_section = {}
        relocmap[reloc_section_match.group(1)] = current_reloc_section
        continue

    reloc_match = re.search(r'([0-9a-f]+)\s+(R_AVR_[0-9A-Z_]+)\s+(.*)$', line)
    if reloc_match:
        addr = int(reloc_match.group(1), 16)
        name = reloc_match.group(2)
        # AVR_16 reloc offset is not insn start's, so adjust
        if name == 'R_AVR_16':
            addr = addr - 2
        current_reloc_section[addr] = (name, reloc_match.group(3))
        continue

bss_syms = {}
lines = syms.readlines()

for line in lines:
    line = line.strip()
    bss_match = re.search(r'([0-9a-f]+).*\s\.bss\s([0-9a-f]+)(.*)$', line)
    if bss_match:
        size = int(bss_match.group(2), 16)
        for i in range(0, size):
            bss_syms[".bss+" + '{0:#010x}'.format(int(bss_match.group(1), 16) + i)] = bss_match.group(3)

lines = disassembly.readlines()

regmap = {}

current_section = ''
for line in lines:
    line = line.strip()

    filename_match = re.search(r'([^:]+):\s+file format', line)
    if filename_match:
        regmap.clear()
        print ("FILE [{0}]".format (filename_match.group(1)))

    section_match = re.search (r'Disassembly of section (.*):', line)
    if section_match:
        regmap.clear()
        current_section = section_match.group(1)
        print ("SECTION [{0}]".format (current_section))
        continue

    function_match = re.search(r'[0-9a-f]+ <(\w+)>:', line)
    if function_match:
        regmap.clear()
        print ("  FUNCTION [{0}()]".format (function_match.group(1)))
        continue
    
    insn_match = re.search (r'([0-9a-f]+):\s+([0-9a-f]{2}\s){2,4}\s+(.*)', line)
    if insn_match:
        address = insn_match.group(1)
        insn = insn_match.group(3)

        insn = insn.split(";")[0]
        reloc = relocmap.get(current_section, {}).get(int(address, 16))
        if reloc:
            typ, sym = reloc
            sym = bss_syms.get(sym, sym)
            insn += "; " + sym

        #print ("    " + address + " : " + insn)
        print ("    " + insn)
        continue
