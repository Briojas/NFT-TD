import styles from './connect.module.scss';
import classNames from 'classnames';

import type { Web3ReactHooks } from '@web3-react/core';
import type { MetaMask } from '@web3-react/metamask';

import { getName } from '../../utils';
import { Accounts } from './accounts';
import { Status } from './status';
import { useState, useEffect, Dispatch, SetStateAction } from 'react';

export interface Props {
    className?: string;
    connector: MetaMask;
    activeChainId: ReturnType<Web3ReactHooks['useChainId']>;
    chainIds?: ReturnType<Web3ReactHooks['useChainId']>[];
    isActivating: ReturnType<Web3ReactHooks['useIsActivating']>;
    isActive: ReturnType<Web3ReactHooks['useIsActive']>;
    error: Error | undefined;
    setError: Dispatch<SetStateAction<undefined>>;
    ENSNames: ReturnType<Web3ReactHooks['useENSNames']>;
    provider?: ReturnType<Web3ReactHooks['useProvider']>;
    accounts?: string[];
}

export function Connect({
    className,
    connector,
    activeChainId,
    chainIds,
    isActivating,
    isActive,
    error,
    setError,
    ENSNames,
    accounts,
    provider,
}: Props) {
    const [hasMetamask, setHasMetamask] = useState(false);

    useEffect(() => {
        if (typeof window.ethereum !== 'undefined') {
            setHasMetamask(true);
        }
    }, []);

    return (
        <div className={classNames(styles.root, className)}>
            <b>{getName(connector)}</b>
            <div style={{ marginBottom: '1rem' }}>
                <Status isActivating={isActivating} isActive={isActive} error={error} />
            </div>
            <div style={{ marginBottom: '1rem' }}>
                <Accounts accounts={accounts} provider={provider} ENSNames={ENSNames} />
            </div>
            <button
                onClick={() => {
                    if (connector?.deactivate) {
                        void connector.deactivate();
                    } else {
                        void connector.resetState();
                    }
                }}
            >
                Disconnect
            </button>
            {hasMetamask ? (
                isActive ? (
                    <i> Wallet: {accounts} </i>
                ) : (
                    <button
                        onClick={() => {
                            connector.activate();
                            setHasMetamask(true);
                        }}
                    >
                        Connect
                    </button>
                )
            ) : (
                <a href="https://metamask.io/"> Install Metamask </a>
            )}
        </div>
    );
}
