# cgutils roadmap (living checklist)

Purpose: track small, reusable helpers we’ll add over time as puzzles demand them. Check items off as we implement and adopt them.

## grid.py (Board + grid helpers)
- [ ] in_bounds(p)
- [ ] get(p, default=None)
- [ ] neighbors4(p, passable: callable|set|str=None)
- [ ] neighbors8(p, passable: callable|set|str=None)
- [ ] flood_fill(start, passable)
- [ ] connected_components(passable)
- [ ] find_all(value|predicate)
- [ ] to_lines(fill=" ")
- [ ] rotate90()/mirror_h()/mirror_v()/transpose()
- [ ] from_rect(h, w, fill=" ")
- [ ] load_from_lines(lines, skip_chars=None)

## search.py (graph and grid search)
- [ ] bfs_grid(starts, goal, passable, diag=False, return_path=True)
- [ ] distance_field(starts, passable)
- [ ] zero_one_bfs(start, next_states)
- [ ] bfs(graph, start|starts, goal, return_path=True)
- [ ] dfs(graph, start, pre=None, post=None, early_stop=None)
- [ ] dijkstra(nodes|start, edges_fn, goal, weight_fn)
- [ ] a_star(nodes|start, edges_fn, goal, weight_fn, heuristic)
- [ ] reconstruct_path(parent, start, goal)

## dsu.py (disjoint set / union-find)
- [ ] DSU with add/find/union/connected/groups/size
- [ ] Path compression + union by rank/size

## geom2d.py (geometry helpers)
- [ ] bresenham(p0, p1)
- [ ] rect_bounds(pts)
- [ ] polygon_area(points)
- [ ] point_in_polygon(p, poly)
- [ ] orientation(a,b,c) and segments_intersect(a,b,c,d)
- [ ] chebyshev_distance(a,b)

## backtrack.py (constraint/backtracking)
- [ ] backtrack(state, choose_var, candidates, apply, unapply, is_goal, heuristic=None, limit=None)
- [ ] heuristics: first_fail_var, order_by_domain

## parse.py (CodinGame input helpers)
- [ ] read_ints()
- [ ] read_grid(h)
- [ ] grid_to_board(lines, skip=None)
- [ ] chunk(n, iterable), pairs(iterable)
- [ ] ints(s), tokens(s)

## pqueue.py (priority queue convenience)
- [ ] PQueue: push/prio-pop/empty or simple heap helpers

## state.py (hashing / canonicalization)
- [ ] freeze_grid(grid_obj)
- [ ] normalize_state(state)
- [ ] rolling_hash(seq) (optional)

## debug.py (toggleable debug + timing)
- [ ] Debug(enabled=False).print(*args)
- [ ] debug.grid(lines|Board)
- [ ] timeit(label) context manager

---

Adoption targets (when convenient):
- Grid BFS: refactor a puzzle like `inside-area.py` or `longest-coast.py` to use bfs_grid/distance_field.
- Backtracking: refactor `16x16_sudoku.py` to use backtrack helpers.
- Geometry: use geom2d in `pixel-polygons.py` or any polygon/line-of-sight task.
- Priority queue: use PQueue in `mars_lander_v2.py` or any Dijkstra/A* task.

Usage: as you open a new puzzle, call out a checklist item (e.g., “implement bfs_grid and use it here”), and we’ll add the function, tests/snippet if needed, and apply it in the puzzle code.
