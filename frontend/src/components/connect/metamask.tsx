import { useEffect, useState } from 'react';

import { hooks, metaMask } from '../../connectors/metamask';
import { Connect } from './connect';

const { useChainId, useAccounts, useIsActivating, useIsActive, useProvider, useENSNames } = hooks;

export default function Metamask() {
    const chainId = useChainId();
    const accounts = useAccounts();
    const isActivating = useIsActivating();

    const isActive = useIsActive();

    const provider = useProvider();
    const ENSNames = useENSNames(provider);

    const [error, setError] = useState(undefined);

    // attempt to connect eagerly on mount
    useEffect(() => {
        void metaMask.connectEagerly().catch(() => {
            console.debug('Failed to connect eagerly to metamask');
        });
    }, []);

    return (
        <Connect
            connector={metaMask}
            activeChainId={chainId}
            isActivating={isActivating}
            isActive={isActive}
            error={error}
            setError={setError}
            accounts={accounts}
            provider={provider}
            ENSNames={ENSNames}
        />
    );
}
