import os
import sys
from tracemalloc import start
from typing import _ProtocolMeta
sys.path.append(os.path.dirname(__file__))
import asm
import idaapi, ida_idaapi, ida_nalt, ida_bytes, ida_auto, ida_kernwin

def get_assembler():
    inf = ida_idaapi.get_inf_structure()
    arch_name = inf.procname.lower()
    if arch_name == 'metapc':
        assembler = asm.AsmX86(inf)
    elif arch_name.startswith('arm'):
        assembler = asm.AsmARM(inf)
    else:
        assembler = None
        print(" - Unsupported CPU: '%s' (%s)" % (arch_name, ida_nalt.get_input_file_path()))
    return assembler

def nop_range(assembler, start_ea, end_ea):
    if start_ea == end_ea:
        return False
    nop_buffer = assembler.nop_buffer(start_ea, end_ea)
    ida_bytes.patch_bytes(start_ea, nop_buffer)
    return True

def patch_address_by_assembly(ea, assembly):
    this_assembler = get_assembler()
    patch_data = this_assembler.asm(assembly, ea)
    if patch_data == "":
        return False
    patch_size = len(patch_data)
    original_data = ida_bytes.get_bytes(ea, patch_size)
    next_address = ea + patch_size
    inst_start = ida_bytes.get_item_head(next_address)
    if ida_bytes.is_code(ida_bytes.get_flags(inst_start)):
        # if the patch clobbers part of an instruction, fill it with NOP
        if inst_start < next_address:
            inst_size = ida_bytes.get_item_size(inst_start)
            fill_size = (inst_start + inst_size) - next_address
            nop_range(this_assembler, next_address, next_address+fill_size)
            ida_auto.auto_make_code(next_address)
            print('next instruction was destroyed!')
    # write the actual patch data to the database
    ida_bytes.patch_bytes(ea, patch_data)
    ida_auto.auto_mark_range(ea, ea+patch_size, ida_auto.AU_USED)
    return True
