Tartarus
--------

Tartarus was built to easily look at what changed in a toolchain's output. This is useful,
for example, to compare code generation between two versions of avr-gcc.

Just doing an objdump -S or -D and diffing the output doesn't work - the first additional/modified
instruction changes the address, and the diff becomes unusable from that point. Also, the disassembly
for object files is hard to read because of relocations - there are only zeros in place of symbols.

Tartarus adjusts for these and tries to produce an output that makes sense when viewed with vimdiff.

Usage:

Ensure binutils is built for avr, and invoke as ./tartarus.sh elf1 elf2.
That should open a vimdiff instance with the disassembly of the object files.

Internally, tartarus.sh invokes avr-objdump to get disassembly, relocs and symbols,
and passes those on to tartarus.py. The python script then strips out addresses, adds
reloc and symbol information and invokes vimdiff. The end result should hopefully show
only real differences.

* TODO - register rewriting
