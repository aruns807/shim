from backend.state.syntaxtokens.color_config import options


def highlight_visual_mode(graphics_state, local_state):
    """
    TODO: remove magic numbers from code here
    """
    nx, ny, nt = local_state.get_page_state()
    px, py, pt = local_state.get_visual_anchors()
    color = options['line_num_text_color']

    if py + pt == ny + nt:
        line = local_state.get_line(py + pt)
        graphics_state.draw_highlight_grid(py, px, nx)
        graphics_state.write_text_grid(0, py, line, color)
    else:
        lp = local_state.get_line(py + pt)
        ln = local_state.get_line(ny + nt)

        if py + pt > ny + nt:
            graphics_state.draw_highlight_grid(py + pt - nt, px, 0)
            graphics_state.write_text_grid(0, py + pt - nt, lp, color)
            graphics_state.draw_highlight_grid(ny, nx, len(ln))
            graphics_state.write_text_grid(0, ny, ln, color)
        else:
            graphics_state.draw_highlight_grid(py + pt - nt, px, len(lp))
            graphics_state.write_text_grid(0, py + pt - nt, lp, color)
            graphics_state.draw_highlight_grid(ny, 0, nx)
            graphics_state.write_text_grid(0, ny, ln, color)

        start, end = (
            (py + pt, ny + nt), (ny + nt, py + pt))[(ny + nt) < (py + pt)]
        for n in range(start - nt + 1, end - nt):
            l = local_state.get_line(n + nt)
            graphics_state.draw_highlight_grid(n, 0, len(l) - 1)
            graphics_state.write_text_grid(0, n, l, color)
