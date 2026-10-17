"""TABLE graph routines generated for the fx-5800P Flash extension.

The graph rescales native TABLE BCD values into signed 64-bit frame slots,
then maps their full range to LCD coordinates. Samples sharing a column
draw a vertical span; opposing edge values trigger a four-sample pole check.
"""
CODE = (
    (0x1100, 'graph_table_gate', bytes.fromhex(
        """
        ce f8 6e f0 5e fe 1a ae 46 b0 a4 70 7e 51 03 c9 d2 70 7e 51 0b c8 10 90 91 80 85 70 07 c8 1e fe 01 f8 00
        18 01 70 08 c9 00 f8 2e 11 1e fe 2e f0 5e fe 1a ae 00 fe 9a 36 2e f0 8e f2
        """
    )),
    (0x1800, 'graph', bytes.fromhex(
        """
        ce f8 5e fe 1a ae 90 e1 6e f4 6e f8 5e fc e5 f0 f8 e0 00 02 4e f2 5e f0 e5 f0 fc e0 00 02 4e f2
        5e f0 e5 f0 f4 e0 00 02 4e f2 5e f0 e5 f0 f3 e0 00 02 4e f2 5e f0 01 02 4e f2 48 00 e7 01 5e f0
        98 00 e7 01 01 02 01 f1 74 a5 14 e1 00 70 02 c9 00 f8 78 1a 7e d0 04 70 02 c9 00 f8 78 1a 7a b0
        00 70 00 51 02 c9 00 f8 78 1a 7c b0 05 f4 04 02 2f 90 40 90 00 70 02 c8 00 f8 78 1a 00 f8 84 18
        00 00 00 00 f2 d0 00 8c 81 e4 04 02 2f 90 40 90 ff e4 02 70 02 c9 00 f8 78 1a c0 80 00 01 14 02
        24 f0 82 e0 05 f2 78 b0 27 f0 02 c4 00 f8 78 1a 80 08 7c b0 05 f4 8c e4 72 dc 01 f8 40 1c 00 72
        03 c9 87 80 01 c7 00 88 94 e4 ff 1c 00 7c 02 c9 00 f8 ba 18 80 78 01 c8 00 08 00 0d 7c d4 7d d5
        8c e4 72 dc 01 f8 00 22 00 72 02 c8 00 f8 4a 19 00 7d 0f c8 e5 f6 d0 e6 e5 fa c8 ea 01 f8 00 21
        e5 f6 d0 e6 e5 fa c0 ea 01 f8 00 21 01 0d 00 f8 4a 19 e5 f6 d0 e6 e5 fa c8 ea 01 f8 20 21 00 70
        06 c4 e5 f6 d0 e6 e5 fa c8 ea 01 f8 00 21 e5 f6 d0 e6 e5 fa c0 ea 01 f8 20 21 00 70 06 c7 e5 f6
        d0 e6 e5 fa c0 ea 01 f8 00 21 94 e4 ff 1c 00 7c 02 c9 00 f8 e4 18 00 7d 02 c8 00 f8 78 1a e5 f6
        c0 e6 e5 fa c8 ea 01 f8 20 21 ea d0 e5 f6 c0 e6 e5 fa d0 ea e8 ea 01 f8 00 21 e5 f6 d0 e6 e8 e6
        e5 fa c8 ea 01 f8 80 21 01 f8 00 24 01 f0 9a 40 e5 f6 c8 e6 e5 fa d0 ea 01 f8 20 21 00 70 02 c7
        00 f8 ce 19 e5 f6 c0 e6 e5 fa d0 ea 01 f8 20 21 00 70 02 c4 00 f8 ce 19 01 f8 20 24 00 86 00 07
        70 80 60 81 01 f0 1c 43 01 17 60 77 f9 c5 7c d4 7d d5 82 e4 04 02 2f 90 40 90 00 70 02 c9 00 f8
        f4 19 00 06 00 07 60 80 70 81 01 f0 1c 43 01 17 20 77 f9 c5 00 0d 7c d4 7d d5 8c e4 72 dc 01 7c
        04 c8 30 00 e4 d0 00 f8 18 1a 00 00 e4 d0 e2 d0 e1 d0 c0 80 ff 10 e8 d0 01 f8 80 23 00 72 03 c8
        00 0d 00 f8 2e 1a 01 f8 00 25 00 f8 2e 1a 94 e4 ff 1c 00 7c 02 c8 00 f8 66 1a 62 d0 61 d1 5f 02
        21 80 00 61 68 d7 00 71 02 c8 77 80 08 c1 00 03 78 80 39 81 64 d2 01 12 e4 d2 00 f8 46 1a e2 d0
        e1 d1 00 f8 18 1a 01 f0 be 43 01 f8 00 08 fa 70 fc c8 01 00 00 f8 7a 1a 00 00 1e fc 2e f8 2e f4
        ea a1 1e fe 8e f2
        """
    )),
    (0x1c00, 'graph_exponent', bytes.fromhex(
        """
        00 83 4c 90 00 01 0a 02 24 f0 0f 23 31 80 00 77 02 c9 05 77 03 c8 00 70 01 c9 9c 10 1f fe
        """
    )),
    (0x1c40, 'graph_valid_exponent', bytes.fromhex(
        """
        ce f8 89 e4 04 02 2f 90 40 90 f7 e4 00 87 00 70 08 c9 01 70 06 c9 05 70 04 c9 06 70 02 c9 00 f8 82 1c 04
        02 2f 90 40 90 0f 20 00 70 0a c9 88 e4 04 02 2f 90 40 90 f8 e4 01 f8 00 1c 01 02 00 f8 84 1c 00 02 8e f2
        """
    )),
    (0x1e80, 'graph_line', bytes.fromhex(
        """
        ce f8 00 86 10 87 01 f0 1c 43 00 7d 25 c9 66 d9 65 da 70 8b a8 8b 00 7b 04 c4 5f 8b ff 00 00 f8 a4 1e 01
        00 f0 d0 60 80 98 80 f1 d0 1c 90 ef d0 01 19 67 89 11 c4 6f d3 b8 83 00 73 06 c4 70 d0 01 8a 71 d0 01 83
        00 f8 ba 1e ef d3 90 80 a0 81 01 f0 1c 43 00 f8 b0 1e e6 d6 e5 d7 01 0d 8e f2
        """
    )),
    (0x2100, 'graph_copy_64', bytes.fromhex(
        """
        08 09 60 90 a1 90 81 e6 81 ea ff 19 00 79 f9 c8 1f fe
        """
    )),
    (0x2120, 'graph_compare_64', bytes.fromhex(
        """
        01 03 00 f8 28 21 00 03 5e f6 5e fa 87 e6 87 ea 08 09 60 90 a0 91 00 73 03 c9 80 40 80 41 00 03
        17 80 09 c1 0b c2 ff e6 ff ea ff 19 00 79 f1 c8 00 00 00 f8 5e 21 ff 00 00 f8 5e 21 01 00 1e fa
        1e f6 1f fe
        """
    )),
    (0x2180, 'graph_subtract_64', bytes.fromhex(
        """
        5e f6 5e fa 5e fc 08 09 00 0c 60 90 a0 91 00 82 00 03 10 80 00 01 c1 80 00 61 08 82 19 83 30 8c
        01 2c 20 80 61 90 81 e6 81 ea ff 19 00 79 ed c8 1e fc 1e fa 1e f6 1f fe
        """
    )),
    (0x2200, 'graph_bcd_15_to_fixed_64', bytes.fromhex(
        """
        ce f8 5e fc 5e f4 e5 fa d0 ea 08 09 00 00 a1 90 81 ea ff 19 00 79 fb c8 89 e4 04 02 2f 90 40 90
        f7 e4 00 87 00 77 09 c9 01 77 07 c9 05 77 05 c9 06 77 03 c9 00 02 00 f8 d0 22 88 e4 04 02 2f 90
        40 90 f8 e4 01 f8 00 1c 10 78 02 c5 00 70 3f c5 80 89 08 89 10 79 3b c4 10 0c 98 8c 00 79 01 c8
        0f 0c 00 0d 04 02 2f 90 40 90 0f 20 01 f8 00 23 ff 1c 00 7c 15 c9 81 e4 04 02 2f 90 40 90 00 7d
        04 c8 4c 90 01 0d 00 f8 8e 22 0f 20 00 0d 01 f8 00 23 ff 1c 00 7c 04 c9 00 7d ed c9 00 f8 78 22
        00 79 03 c8 00 00 01 f8 00 23 05 77 02 c9 06 77 0e c8 e5 fa d0 ea 08 09 01 06 a0 90 ff 40 61 80
        00 06 00 66 a1 90 81 ea ff 19 00 79 f6 c8 01 02 1e f4 1e fc 8e f8 1f fe
        """
    )),
    (0x2300, 'graph_decimal_digit', bytes.fromhex(
        """
        ce f8 6e f8 00 86 e5 fa d0 ea 08 09 0a 02 a0 90 00 01 24 f0 61 80 00 61 a1 90 10 86 81 ea ff 19
        00 79 f5 c8 2e f8 8e f8 1f fe
        """
    )),
    (0x2340, 'graph_multiply_31', bytes.fromhex(
        """
        6e f8 e5 fa d0 ea d8 ea 08 09 00 06 1f 02 a0 90 00 01 24 f0 61 80 00 61 a1 90 10 86 81 ea ff 19
        00 79 f5 c8 2e f8 1f fe
        """
    )),
    (0x2380, 'graph_y_pixel_64', bytes.fromhex(
        """
        ce f8 5e fc 01 f8 00 22 00 72 30 c9 6a d0 00 70 03 c8 10 00 00 f8 ea 23 e5 f6 c0 e6 e5 fa d0 ea
        e0 ea 01 f8 00 21 e5 f6 d0 e6 e0 e6 e5 fa d0 ea 01 f8 80 21 e5 f6 d0 e6 e0 e6 e5 fa d0 ea d8 ea
        01 f8 00 21 01 f8 40 23 00 0c e5 f6 d0 e6 d8 e6 e5 fa d0 ea e8 ea 01 f8 26 21 00 70 05 c5 01 f8
        80 21 01 1c 1f 7c f1 c5 c0 80 01 02 1e fc 8e f8 1f fe
        """
    )),
    (0x2400, 'graph_zero_64', bytes.fromhex(
        """
        e5 fa d0 ea 08 09 00 00 a1 90 81 ea ff 19 00 79 fb c8 1f fe
        """
    )),
    (0x2420, 'graph_zero_axis_pixel', bytes.fromhex(
        """
        ce f8 5e fc 01 f8 00 24 00 f8 8c 23
        """
    )),
    (0x2480, 'graph_inter_sample_pole', bytes.fromhex(
        """
        ce f8 5e f4 5e fc 00 02 00 7d 29 c9 6d d0 00 70 26 c9 01 7c 24 c9 65 d0 1c 70 09 c5 6c d1 03 71
        1e c6 6e d1 07 81 1b c4 01 0d 00 f8 c0 24 03 70 16 c6 6c d1 1c 71 13 c5 6e d1 07 81 10 c7 02 0d
        94 e4 01 f8 80 23 00 72 0a c9 6c d1 01 7d 04 c9 17 80 05 c4 00 f8 dc 24 17 80 01 c7 01 02 1e fc
        1e f4 8e f8 1f fe
        """
    )),
    (0x2500, 'graph_plot_sample', bytes.fromhex(
        """
        ce f8 ec d0 00 7d 13 c9 01 f8 80 24 00 72 03 c9 00 0d 00 f8 2e 25 65 d0 ee d0 01 00 ed d0 66 d0
        64 d1 17 80 06 c8 01 f8 a0 25 00 f8 32 25 00 00 ed d0 6c d1 64 d0 01 f8 80 1e 8e f8 1f fe
        """
    )),
    (0x25a0, 'graph_same_column_span', bytes.fromhex(
        """
        ce f8 64 d6 65 d7 6c d9 97 87 0b c9 03 c5 ff 17 00 f8 b6 25 01 17 60 80 70 81 01 f0 1c 43 00 f8
        a8 25 8e f8 1f fe
        """
    )),
)

