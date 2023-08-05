import pytest

from plenum.common.constants import DOMAIN_LEDGER_ID
from plenum.test.delayers import lsDelay, cDelay
from plenum.test.helper import sdk_send_random_and_check
from plenum.test.node_catchup.helper import waitNodeDataInequality, \
    ensure_all_nodes_have_same_data, make_a_node_catchup_twice
from plenum.test.spy_helpers import getAllReturnVals
from plenum.test.stasher import delay_rules
from plenum.test.test_node import getNonPrimaryReplicas, \
    checkProtocolInstanceSetup
from plenum.test.view_change.helper import ensure_view_change
# noinspection PyUnresolvedReferences
from plenum.test.batching_3pc.conftest import tconf

Max3PCBatchSize = 2


@pytest.fixture(scope="module")
def tconf(tconf):
    oldMax3PCBatchSize = tconf.Max3PCBatchSize
    oldMax3PCBatchWait = tconf.Max3PCBatchWait
    tconf.Max3PCBatchSize = Max3PCBatchSize
    tconf.Max3PCBatchWait = 1000
    yield tconf

    tconf.Max3PCBatchSize = oldMax3PCBatchSize
    tconf.Max3PCBatchWait = oldMax3PCBatchWait


@pytest.mark.skip(reason="INDY-2223: Temporary skipped to create build")
def test_caught_up_for_current_view_check(looper, txnPoolNodeSet, sdk_pool_handle, sdk_wallet_client):
    """
    One of the node experiences poor network and loses 3PC messages. It has to
    do multiple rounds of catchup to be caught up
    """
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle, sdk_wallet_client, 3 * Max3PCBatchSize)
    ensure_all_nodes_have_same_data(looper, txnPoolNodeSet)

    nprs = getNonPrimaryReplicas(txnPoolNodeSet, 0)
    bad_node = nprs[-1].node
    other_nodes = [n for n in txnPoolNodeSet if n != bad_node]

    # Bad node does not process any 3 Commit messages, equivalent to messages
    with delay_rules(bad_node.nodeIbStasher, cDelay()):

        # Delay LEDGER_STAUS on slow node, so that only MESSAGE_REQUEST(LEDGER_STATUS) is sent, and the
        # node catch-ups 2 times.
        # Otherwise other nodes may receive multiple LEDGER_STATUSes from slow node, and return Consistency proof for all
        # missing txns, so no stashed ones are applied

        bad_node.nodeIbStasher.delay(lsDelay(1000))

        sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle, sdk_wallet_client, 6 * Max3PCBatchSize)
        waitNodeDataInequality(looper, bad_node, *other_nodes)

        # Patch all nodes to return ConsistencyProof of a smaller ledger to the
        # bad node but only once, so that the bad_node needs to do catchup again.

        make_a_node_catchup_twice(bad_node, other_nodes, DOMAIN_LEDGER_ID,
                                  Max3PCBatchSize)

        def is_catchup_needed_count():
            return len(getAllReturnVals(bad_node, bad_node.is_catchup_needed,
                                        compare_val_to=True))

        def is_catchup_not_needed_count():
            return len(getAllReturnVals(bad_node, bad_node.is_catchup_needed,
                                        compare_val_to=False))

        def has_ordered_till_last_prepared_certificate_count():
            return len(getAllReturnVals(bad_node,
                                        bad_node.has_ordered_till_last_prepared_certificate,
                                        compare_val_to=True))

        old_is_catchup_needed_count = is_catchup_needed_count()
        old_is_catchup_not_needed_count = is_catchup_not_needed_count()
        old_has_ordered_till_last_prepared_certificate_count = has_ordered_till_last_prepared_certificate_count()
        ensure_view_change(looper, txnPoolNodeSet)
        checkProtocolInstanceSetup(looper, txnPoolNodeSet, retryWait=1)
        ensure_all_nodes_have_same_data(looper, nodes=txnPoolNodeSet,
                                        exclude_from_check=['check_last_ordered_3pc',
                                                            'check_audit',
                                                            'check_last_ordered_3pc_backup'])

        assert is_catchup_needed_count() == old_is_catchup_needed_count
        assert is_catchup_not_needed_count() > old_is_catchup_not_needed_count
        # The bad_node caught up due to ordering till last prepared certificate
        assert has_ordered_till_last_prepared_certificate_count() > old_has_ordered_till_last_prepared_certificate_count

    ensure_all_nodes_have_same_data(looper, nodes=txnPoolNodeSet,
                                    exclude_from_check=['check_last_ordered_3pc_backup'])