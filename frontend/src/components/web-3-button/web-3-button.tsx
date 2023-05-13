import styles from './web-3-button.module.scss';
import classNames from 'classnames';

import type { Web3ReactHooks } from '@web3-react/core';
import type { MetaMask } from '@web3-react/metamask';

import { getName } from '../../utils';
import { Accounts } from './accounts';
import { Status } from './status';
import { useState, useEffect, Dispatch, SetStateAction } from 'react';

export interface Web3ButtonProps {
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

export const Web3Button = ({
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
}: Web3ButtonProps) => {
    const [hasMetamask, setHasMetamask] = useState(false);

    useEffect(() => {
        if (typeof window.ethereum !== 'undefined') {
            setHasMetamask(true);
        }
    }, []);

    return (
        <div className={classNames(styles.root, className)}>
            <div />
            {hasMetamask ? (
                isActive ? (
                    <div>
                        <i> Wallet: {accounts} </i>
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
                    </div>
                ) : (
                    <div>
                        <div>
                            <button
                                onClick={() => {
                                    connector.activate();
                                    setHasMetamask(true);
                                }}
                            >
                                Connect
                            </button>
                        </div>
                    </div>
                )
            ) : (
                <a href="https://metamask.io/">Get Metamask</a>
            )}
        </div>
    );
};
