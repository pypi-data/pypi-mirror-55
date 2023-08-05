import funcy as fn
from itertools import combinations_with_replacement as combinations

try:
    from dd.cudd import BDD
except ImportError:
    from dd.autoref import BDD

from fold_bdd import post_order, fold_path
from fold_bdd.folds import path


def create_manager():
    manager = BDD()
    manager.declare('x', 'y')
    manager.reorder({'x': 1, 'y': 0})
    manager.configure(reordering=False)
    return manager


def test_post_order():
    @fn.memoize
    def merge1(ctx, low=None, high=None):
        return 1 if low is None else low + high

    manager = create_manager()
    bexpr = manager.add_expr('x & y')

    val = post_order(bexpr, merge1)
    assert val == bexpr.dag_size

    # Convert BDD to function.
    def merge2(ctx, low=None, high=None):
        if ctx.is_leaf:
            return lambda _: ctx.node_val

        def _eval(vals):
            val, *vals2 = vals
            out = high(vals2) if val else low(vals2)
            return ctx.negated ^ out

        return _eval

    _eval = post_order(bexpr, merge2)
    for vals in combinations([True, False], 2):
        assert all(vals) == _eval(vals)

    def merge3(ctx, low, high):
        if ctx.is_leaf:
            return ctx.skipped_paths if ctx.node_val else 0

        return (low + high) * ctx.skipped_paths

    bexpr2 = manager.add_expr('x | y')

    assert post_order(bexpr, merge3) == 1
    assert post_order(bexpr2, merge3) == 3


def test_path():
    manager = create_manager()
    bexpr = manager.add_expr('x | y')

    questions = {
        (False, False): 3,
        (False, True): 3,
        (True, False): 2,
        (True, True): 2,
    }

    for q, a in questions.items():
        assert len(list(path(bexpr, q))) == a


def test_fold_path():
    manager = create_manager()
    bexpr = manager.add_expr('x | y')

    def merge(ctx, val, acc):
        return acc + 1

    def count_nodes(bexpr, vals):
        return fold_path(merge, bexpr, vals, initial=0)

    assert count_nodes(bexpr, (False, False)) == 3
    assert count_nodes(bexpr, (False, True)) == 3
    assert count_nodes(bexpr, (True, False)) == 2
    assert count_nodes(bexpr, (True, True)) == 2

    def merge2(ctx, val, acc):
        return acc * ctx.skipped_paths

    def count_paths(bexpr, vals):
        return fold_path(merge2, bexpr, vals, initial=1)

    assert count_paths(bexpr, (False, False)) == 1
    assert count_paths(bexpr, (False, True)) == 1
    assert count_paths(bexpr, (True, False)) == 2
    assert count_paths(bexpr, (True, True)) == 2
