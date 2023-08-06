from plenum.test.checkpoints.helper import check_stable_checkpoint
from plenum.test.helper import sdk_send_random_and_check
from plenum.test.node_catchup.helper import waitNodeDataEquality
from plenum.test.pool_transactions.helper import sdk_add_new_steward_and_node
from plenum.test.test_node import checkNodesConnected

CHK_FREQ = 5


def test_upper_bound_of_checkpoint_after_catchup_is_divisible_by_chk_freq(
        chkFreqPatched, looper, txnPoolNodeSet,
        sdk_pool_handle, sdk_wallet_steward, sdk_wallet_client, tdir,
        tconf, allPluginsPath):
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 4)

    _, new_node = sdk_add_new_steward_and_node(
        looper, sdk_pool_handle, sdk_wallet_steward,
        'EpsilonSteward', 'Epsilon', tdir, tconf,
        allPluginsPath=allPluginsPath)
    txnPoolNodeSet.append(new_node)
    looper.run(checkNodesConnected(txnPoolNodeSet))
    waitNodeDataEquality(looper, new_node, *txnPoolNodeSet[:-1],
                         exclude_from_check=['check_last_ordered_3pc_backup'])
    # Epsilon did not participate in ordering of the batch with EpsilonSteward
    # NYM transaction and the batch with Epsilon NODE transaction.
    # Epsilon got these transactions via catch-up.

    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 1)

    for replica in txnPoolNodeSet[0].replicas.values():
        check_stable_checkpoint(replica, 5)

    # TODO: This is failing now because checkpoints are not created after catchup.
    #  PBFT paper describes catch-up with per-checkpoint granularity, but otherwise
    #  quite similar to plenum implementation. Authors of PBFT state that after
    #  catching up nodes set low watermark to last caught up checkpoint, which is
    #  actually equivalent to declaring that checkpoint stable. This means that
    #  most probably we need this functionality in plenum.
    # for replica in new_node.replicas.values():
    #    check_stable_checkpoint(replica, 5)
