num_rows = 6
num_notes = 32

for cell in range(0,num_notes):
    row = cell % num_rows
    col = cell // num_rows
    # lsr_enbl.value = 0
    # selectMuxChannel(row_s0, row_s1, row_s2, row)
    # selectMuxChannel(col_s0, col_s1, col_s2, col)
    # time.sleep(0.001) # Settle time

    print(f"LED {cell}: row={row}, col={col}") 