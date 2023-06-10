import { MetaMask } from '@web3-react/metamask';
import { Network } from '@web3-react/network';
import type { Connector } from '@web3-react/types';
import { WalletConnect } from '@web3-react/walletconnect';

export function getName(connector: Connector) {
    if (connector instanceof MetaMask) return 'MetaMask';
    if (connector instanceof WalletConnect) return 'WalletConnect';
    if (connector instanceof Network) return 'Network';
    return 'Unknown';
}
